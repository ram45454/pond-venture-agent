import os
from pydantic import BaseModel

class Settings(BaseModel):
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "xoxb-your-slack-bot-token")
    SLACK_CHANNEL_ID: str = os.getenv("SLACK_CHANNEL_ID", "#venture-alerts")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "venture_agent.db")
    POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))
    HEALTH_PORT: int = int(os.getenv("HEALTH_PORT", "8080"))
    POND_AGENT_ID: str = os.getenv("POND_AGENT_ID", "pond-agent-yc-speedrun-v1")
    
    YC_DIRECTORY_URL: str = "https://www.ycombinator.com/companies"
    SPEEDRUN_DIRECTORY_URL: str = "https://speedrun.a16z.com/companies"
    TWITTER_BEARER_TOKEN: str = os.getenv("TWITTER_BEARER_TOKEN", "")
    LINKEDIN_ACCESS_TOKEN: str = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

settings = Settings()
