import synthbean
import asyncio

if __name__ == '__main__':
    apm_config = synthbean.render_apm_config()

    synth_config = synthbean.render_synth_config()
    loop = asyncio.get_event_loop()

    num_workers = synth_config.get('instance_count', 1)
    for i in range(0, num_workers):
        client = synthbean.apm_preflight(apm_config['elasticapm'], f"synthbean-python-{str(i)}", synth_config.get('smoothing_strategy'))
        synthbean.create_span_pool(synth_config, loop, client)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Interrupt received. Shutting down gracefully.")

    tasks = asyncio.all_tasks(loop=loop)

    for t in tasks:
        t.cancel()

    group = asyncio.gather(*tasks, return_exceptions=True)

    loop.run_until_complete(group)
    loop.close()
