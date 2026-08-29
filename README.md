# Pond Venture Intelligence Agent

An autonomous venture monitoring agent built for the Pond AI Agent infrastructure. Continuously tracks Y Combinator (YC Directory), a16z Speedrun, X (Twitter), and LinkedIn for early founder batch announcements and official accelerator listings.

---

## 🌟 Key Features

* **Multi-Source Surveillance:** Continuously polls YC Directory, a16z Speedrun Directory, X/Twitter streams, and LinkedIn posts.
* **Early Founder Announcement Detection:** Uses heuristic regular expressions and intent scoring to catch founder posts *before* official YC directory updates.
* **Stateful Persistence:** Uses an SQLite WAL engine with SHA-256 event fingerprinting to guarantee zero duplicate alerts across restarts.
* **Pond Infrastructure Integration:** Exposes an asynchronous HTTP server on port `8080` with `/healthz` and `/metrics` endpoints for network liveness probes.
* **Rich Slack Alerts:** Sends visually formatted Slack Block Kit cards directly to designated channels via OAuth Bot Tokens.

---

## 🛠️ Environment Configuration

Set the following environment variables before running the agent:

| Variable | Description | Default |
| --- | --- | --- |
| `SLACK_BOT_TOKEN` | Slack OAuth Bot User Token (`xoxb-...`) | *Required* |
| `SLACK_CHANNEL_ID` | Slack Target Channel or DM ID | `#venture-alerts` |
| `POLL_INTERVAL_SECONDS` | Polling loop sleep duration (in seconds) | `300` |
| `HEALTH_PORT` | Port exposed for Pond health checks | `8080` |
| `POND_AGENT_ID` | Identifier for Pond network health check | `pond-agent-yc-speedrun-v1` |
| `DATABASE_PATH` | Path to SQLite database file | `venture_agent.db` |

---

## 🚀 Local Quickstart

### 1. Install Dependenciesbash

pip install -r requirements.txt
python -m playwright install chromium

```

### 2. Export Required Environment Variables
```bash
export SLACK_BOT_TOKEN="xoxb-your-slack-bot-token"
export SLACK_CHANNEL_ID="C0123456789"

```

### 3. Run the Main Agent Loop

```bash
python main.py

```

---

## 🐳 Running with Docker

```bash
# Build the Docker container
docker build -t pond-venture-agent .

# Run the container with environment variables
docker run -d \
  -p 8080:8080 \
  -e SLACK_BOT_TOKEN="xoxb-your-slack-bot-token" \
  -e SLACK_CHANNEL_ID="C0123456789" \
  --name venture-agent \
  pond-venture-agent

```

---

## 🩺 Pond Network Health Checks

The agent serves active liveness probes on port `8080`:

* **Health Probe:** `GET http://localhost:8080/healthz`
```json
{
  "status": "healthy",
  "agent_id": "pond-agent-yc-speedrun-v1",
  "database": "connected",
  "uptime": "active"
}

```


* **Telemetry Metrics:** `GET http://localhost:8080/metrics`
```json
{
  "agent_id": "pond-agent-yc-speedrun-v1",
  "processed_events": 4,
  "alerts_sent": 2
}

```



---

## 📩 Alert Sample Outputs

### Example 1 — Early YC Founder Signal (X/LinkedIn)

```text
🔥 EARLY YC SIGNAL — Founder Announced Before YC

Company: Acme AI
Founder: Jane Doe (@janedoe)
Batch: YC S26
Source: X
Status: ⚡ Founder announced / not yet officially announced by YC

Original post:
"We got into YC S26! Excited to move to SF and start building."

Original post: [https://x.com/example/status/123456](https://x.com/example/status/123456)
Company: [https://acme.ai](https://acme.ai)
Detected: Aug. 28, 2026, 9:14 AM PT

```

### Example 2 — Official Directory Listing (YC / Speedrun)

```text
NEW YC COMPANY ✅

Company: Example Labs
Batch: YC S26
Source: YC Directory
Status: ✅ Confirmed by YC

Description: AI agents for logistics companies.
YC Profile: [https://www.ycombinator.com/companies/example](https://www.ycombinator.com/companies/example)
Detected: Aug. 28, 2026, 2:03 PM PT

```

```

```
