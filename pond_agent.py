import logging
from aiohttp import web
from storage import StorageEngine

logger = logging.getLogger("PondAgent")

class PondAgentRuntime:
    def __init__(self, agent_id: str, port: int, storage: StorageEngine):
        self.agent_id = agent_id
        self.port = port
        self.storage = storage
        self.app = web.Application()
        self.processed_count = 0
        self.alerts_sent_count = 0
        self._setup_routes()

    def _setup_routes(self):
        self.app.router.add_get("/healthz", self.health_check)
        self.app.router.add_get("/metrics", self.metrics_check)

    async def health_check(self, request):
        is_healthy = True
        try:
            self.storage.has_seen("healthcheck_probe")
        except Exception as e:
            is_healthy = False
            logger.error(f"Database liveness check failed: {e}")

        if is_healthy:
            return web.json_response({
                "status": "healthy",
                "agent_id": self.agent_id,
                "database": "connected",
                "uptime": "active"
            }, status=200)
        else:
            return web.json_response({
                "status": "unhealthy",
                "agent_id": self.agent_id,
                "reason": "db connection error"
            }, status=500)

    async def metrics_check(self, request):
        return web.json_response({
            "agent_id": self.agent_id,
            "processed_events": self.processed_count,
            "alerts_sent": self.alerts_sent_count
        }, status=200)

    async def start_health_server(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        logger.info(f"Pond Health Check Server listening on 0.0.0.0:{self.port}")
