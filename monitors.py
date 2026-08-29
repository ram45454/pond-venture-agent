import logging
import httpx
from typing import List, Dict, Any
from classifier import SignalClassifier

logger = logging.getLogger("Monitors")

class BaseMonitor:
    def __init__(self, name: str):
        self.name = name

    async def fetch_signals(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

class YCDirectoryMonitor(BaseMonitor):
    def __init__(self, url: str):
        super().__init__("YC Directory")
        self.url = url

    async def fetch_signals(self) -> List[Dict[str, Any]]:
        signals = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.url, headers={"User-Agent": "PondAgent/1.0"})
                if response.status_code == 200:
                    signals.append({
                        "type": "OFFICIAL_LISTING",
                        "company": "Example Labs",
                        "batch": "YC S26",
                        "source": "YC Directory",
                        "description": "AI agents for logistics companies.",
                        "url": "https://www.ycombinator.com/companies/example",
                        "company_url": "https://examplelabs.ai"
                    })
        except Exception as e:
            logger.error(f"Error scraping YC Directory: {e}")
        return signals

class SpeedrunDirectoryMonitor(BaseMonitor):
    def __init__(self, url: str):
        super().__init__("Speedrun Directory")
        self.url = url

    async def fetch_signals(self) -> List[Dict[str, Any]]:
        signals = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                signals.append({
                    "type": "OFFICIAL_LISTING",
                    "company": "Amdahl",
                    "batch": "Speedrun Cohort 005",
                    "source": "Speedrun Directory",
                    "description": "AI Context layer for Enterprise GTM work.",
                    "url": "https://speedrun.a16z.com/companies",
                    "company_url": "https://amdahl.ai"
                })
        except Exception as e:
            logger.error(f"Error scraping Speedrun Directory: {e}")
        return signals

class XSocialMonitor(BaseMonitor):
    def __init__(self, bearer_token: str):
        super().__init__("X")
        self.bearer_token = bearer_token
        self.classifier = SignalClassifier()

    async def fetch_signals(self) -> List[Dict[str, Any]]:
        signals = []
        raw_posts = [
            {
                "id": "123456",
                "text": "We got into YC S26! Excited to move to SF and start building.",
                "author_handle": "janedoe",
                "author_name": "Jane Doe",
                "company_guess": "Acme AI",
                "company_url": "https://acme.ai",
                "post_url": "https://x.com/example/status/123456"
            }
        ]
        
        for post in raw_posts:
            signal_type, score = self.classifier.classify_social_post(post["text"])
            if signal_type == "EARLY_SIGNAL":
                batch = self.classifier.parse_batch_info(post["text"])
                signals.append({
                    "type": "EARLY_SIGNAL",
                    "company": post["company_guess"],
                    "founder": f"{post['author_name']} (@{post['author_handle']})",
                    "batch": batch,
                    "source": "X",
                    "status": "⚡ Founder announced / not yet officially announced by YC",
                    "original_post": post["text"],
                    "post_url": post["post_url"],
                    "company_url": post["company_url"]
                })
        return signals

class LinkedInSocialMonitor(BaseMonitor):
    def __init__(self, access_token: str):
        super().__init__("LinkedIn")
        self.classifier = SignalClassifier()

    async def fetch_signals(self) -> List[Dict[str, Any]]:
        signals = []
        return signals
