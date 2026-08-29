import asyncio
import logging
from config import settings
from storage import StorageEngine
from monitors import (
    YCDirectoryMonitor,
    SpeedrunDirectoryMonitor,
    XSocialMonitor,
    LinkedInSocialMonitor
)
from slack_notifier import SlackNotifier
from pond_agent import PondAgentRuntime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MainLoop")

async def main():
    logger.info("Initializing Venture Intelligence Agent on Pond Infrastructure...")
    
    storage = StorageEngine(settings.DATABASE_PATH)
    slack = SlackNotifier(settings.SLACK_BOT_TOKEN, settings.SLACK_CHANNEL_ID)
    pond_runtime = PondAgentRuntime(settings.POND_AGENT_ID, settings.HEALTH_PORT, storage)
    
    await pond_runtime.start_health_server()

    monitors = [
        YCDirectoryMonitor(settings.YC_DIRECTORY_URL),
        SpeedrunDirectoryMonitor(settings.SPEEDRUN_DIRECTORY_URL),
        XSocialMonitor(settings.TWITTER_BEARER_TOKEN),
        LinkedInSocialMonitor(settings.LINKEDIN_ACCESS_TOKEN)
    ]

    logger.info("Agent initialization complete. Entering continuous surveillance loop...")

    while True:
        try:
            for monitor in monitors:
                logger.debug(f"Polling source: {monitor.name}")
                signals = await monitor.fetch_signals()
                
                for signal in signals:
                    pond_runtime.processed_count += 1
                    
                    identifier = signal.get("post_url") if signal.get("post_url") else signal.get("url")
                    if not identifier:
                        identifier = signal.get("company", "unknown")
                        
                    fp = storage.generate_fingerprint(
                        source=signal.get("source", "generic"),
                        identifier=identifier,
                        batch=signal.get("batch", "")
                    )

                    if not storage.has_seen(fp):
                        logger.info(f"New signal detected: {signal.get('company')} via {signal.get('source')}")
                        success = await slack.send_alert(signal)
                        if success:
                            storage.record_event(
                                fingerprint=fp,
                                company_name=signal.get("company", "Unknown"),
                                source=signal.get("source", "Unknown"),
                                batch=signal.get("batch")
                            )
                            pond_runtime.alerts_sent_count += 1
                    else:
                        logger.debug(f"Duplicate signal ignored for key: {fp}")

        except Exception as e:
            logger.error(f"Unhandled error in surveillance execution loop: {e}")

        logger.debug(f"Sleeping for {settings.POLL_INTERVAL_SECONDS} seconds...")
        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
