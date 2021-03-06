from . import create_scheduler


__all__ = ('setup', 'spawn', 'get_scheduler', 'get_scheduler_from_app')


def get_scheduler(request):
    scheduler = get_scheduler_from_app(request.app)
    if scheduler is None:
        raise RuntimeError(
            "Call aiojobs.aiohttp.setup() on application initialization")
    return scheduler


def get_scheduler_from_app(app):
    return app.get('AIOJOBS_SCHEDULER')


async def spawn(request, coro):
    return await get_scheduler(request).spawn(coro)


def setup(app, **kwargs):
    async def on_startup(app):
        app['AIOJOBS_SCHEDULER'] = await create_scheduler(**kwargs)

    async def on_cleanup(app):
        await app['AIOJOBS_SCHEDULER'].close()

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
