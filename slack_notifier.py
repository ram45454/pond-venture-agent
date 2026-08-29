import logging
import httpx
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger("SlackNotifier")

class SlackNotifier:
    def __init__(self, token: str, channel_id: str):
        self.token = token
        self.channel_id = channel_id
        self.api_url = "https://slack.com/api/chat.postMessage"

    def _build_early_signal_blocks(self, data: Dict[str, Any]) -> list:
        now_str = datetime.now().strftime("%b. %d, %Y, %I:%M %p PT")
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "EARLY YC SIGNAL — Founder Announced Before YC 🔥",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Company:*\n{data.get('company')}"},
                    {"type": "mrkdwn", "text": f"*Founder:*\n{data.get('founder')}"},
                    {"type": "mrkdwn", "text": f"*Batch:*\n{data.get('batch')}"},
                    {"type": "mrkdwn", "text": f"*Source:*\n{data.get('source')}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Status:*\n{data.get('status')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Original post:*\n\n\"{data.get('original_post')}\""
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Original post:* {data.get('post_url')}\n*Company:* {data.get('company_url')}\n*Detected:* {now_str}"
                }
            },
            {"type": "divider"}
        ]

    def _build_official_listing_blocks(self, data: Dict[str, Any]) -> list:
        now_str = datetime.now().strftime("%b. %d, %Y, %I:%M %p PT")
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "NEW YC COMPANY ✅",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Company:*\n{data.get('company')}"},
                    {"type": "mrkdwn", "text": f"*Batch:*\n{data.get('batch')}"},
                    {"type": "mrkdwn", "text": f"*Source:*\n{data.get('source')}"},
                    {"type": "mrkdwn", "text": f"*Status:*\n✅ Confirmed by YC"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:* {data.get('description')}\n*YC Profile:* {data.get('url')}\n*Detected:* {now_str}"
                }
            },
            {"type": "divider"}
        ]

    async def send_alert(self, signal_data: Dict[str, Any]) -> bool:
        if signal_data.get("type") == "EARLY_SIGNAL":
            blocks = self._build_early_signal_blocks(signal_data)
        else:
            blocks = self._build_official_listing_blocks(signal_data)

        payload = {
            "channel": self.channel_id,
            "blocks": blocks,
            "text": f"New Venture Alert: {signal_data.get('company')}"
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(self.api_url, json=payload, headers=headers)
                res_data = res.json()
                if res_data.get("ok"):
                    logger.info(f"Slack alert posted successfully for {signal_data.get('company')}")
                    return True
                else:
                    logger.error(f"Slack API error: {res_data.get('error')}")
                    return False
        except Exception as e:
            logger.error(f"Failed to post Slack notification: {e}")
            return False
