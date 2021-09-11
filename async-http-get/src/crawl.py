import logging
import asyncio
import aiohttp
import datetime
import random

LOGGER_FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=LOGGER_FORMAT, datefmt="[%H:%M:%S]")
log = logging.getLogger()
log.setLevel(logging.INFO)


async def on_request_start(session, trace_config_ctx, params):
    ctx = trace_config_ctx.trace_request_ctx
    log.info(f"{ctx['idx']} Start {params.url}: {datetime.datetime.utcnow()}")
    trace_config_ctx.start = asyncio.get_event_loop().time()

async def on_request_end(session, trace_config_ctx, params):
    ctx = trace_config_ctx.trace_request_ctx
    payload = ctx.get("payload", dict())

    elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start

    now = datetime.datetime.utcnow()

    metrics = dict(
        dt=now,
        ds=now.date(),
        url=str(params.url),
        status_code=params.response.status,
        payload={k:v for k,v in payload.items() if k != "api_key"},
        host=params.url.host,
        path=params.url.path,
        resp_bytes=None,
        latency_secs=elapsed,
    )

    try:
        metrics["resp_bytes"] = len(await params.response.text())
    except Exception as ex:
        log.exception("Problem building request metrics", ex)
    finally:
        log.info(f"{ctx['idx']} Metrics: {metrics}")

async def fetch(session, idx, url, payload, window_secs, sem):
    async with sem:
        is_json = None
        async with session.request(
            method="GET", url=url, params=payload,
            trace_request_ctx={"idx": idx, "payload": payload}
        ) as response:
            status = response.status
            log.info(f"{idx} Made request: {url}. Status: {status}")

            try:
                if status == 200:
                    json = await response.json()
                    is_json = True
                else:
                    text = await response.text()
                    is_json = False
            finally:            
                await asyncio.sleep(window_secs)
                return is_json

async def main(urls, window_secs, concurrent_limit):
    sem = asyncio.Semaphore(concurrent_limit)  # used to limit concurrent requests

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)

    async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
        tasks = [fetch(session, idx, url, payload, window_secs, sem) for idx, (url, payload) in enumerate(urls)]

        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    base_url = "http://server"
    urls = [
        (base_url + "/json", dict(a=1, b="a")),
        (base_url + f"/delay/{random.randint(1, 3)}", dict()),
        (base_url + "/status/404", dict(a=3, b="c")),
        (base_url + "/json", dict(a=4, b="d")),
        (base_url + "/json", dict(a=5, b="e")),
    ]
    
    # Max of 2 requests in every 4 seconds
    window_secs = 4
    concurrent_limit = 2

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(urls, window_secs, concurrent_limit))

    # results = asyncio.run(main(urls, window_secs, concurrent_limit))
    log.info(f"Num results: {len(results)}")
    log.info(results)
