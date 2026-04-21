# SpeedHunter

**Automated PageSpeed Auditing & Cold Email Outreach**

SpeedHunter is a Growth Engineering script designed to automate B2B prospecting. It reads a list of target companies, audits their mobile website performance in real-time using the Google PageSpeed Insights API, and automatically fires off highly personalized cold emails via Resend if their score falls below a certain threshold.

Built for performance marketing agencies, web development studios, and freelancers who want to prove their value using hard data before even starting a conversation.

## Features

- **Real-Time Auditing:** Connects to Google's Lighthouse API to fetch actual mobile performance scores.
- **Hyper-Personalized Outreach:** Injects the target's exact PageSpeed score into the cold email to instantly build credibility.
- **Async Execution:** Uses `httpx` and `asyncio` for non-blocking API calls.
- **Smart Filtering:** Automatically skips targets with good scores (>85/100) to avoid sending irrelevant emails.

## Prerequisites

- Python 3.10+
- `uv` (recommended) or `pip`
- A [Resend](https://resend.com/) API Key.
- A [Google Cloud](https://console.cloud.google.com/) API Key with the PageSpeed Insights API enabled.

## Setup

**1. Clone the repository and install dependencies:**

```python
git clone https://github.com/yourusername/SpeedHunter.git
cd SpeedHunter

# Using uv (as an example)
uv venv
source .venv/bin/activate
uv pip install resend httpx python-dotenv
```

**2. Configure your Environment Variables:**

Create a .env file in the root directory and add your API keys:

```bash
RESEND_API_KEY=re_your_resend_api_key_here
GOOGLE_API_KEY=AIzaSy_your_google_api_key_here
```

**3. Prepare your targets list:**

Create an agencias.json file in the root directory containing the companies you want to audit. Use the following format:

```json
[
  {
    "company": "Jhon Doe Agency",
    "email": "hello@acmeagency.com",
    "url": "https://acmeagency.com"
  },
  {
    "company": "Growth Bros",
    "email": "founders@growthbros.io",
    "url": "https://growthbros.io"
  }
]
```

## Usage

**Important Configuration:**
Before running the script, you **must** open `main.py` and update the sender details and email copy. 

**1. Locate the `send_email` function and replace the placeholder emails with your verified Resend domain:**

```python
resend.Emails.send({
    "from": "Your Name <hello@yourdomain.com>", # <-- Update this
    "to": target_email,
    "subject": "Quick question about your mobile performance",
    "html": html_body,
    "reply_to": "founders@yourdomain.com" # <-- Update this
})
```

**2. Modify the cuerpo_html variable to match your own brand, name, and specific offer.**

Once configured, run the script:

```bash
python main.py
```

The script will iterate through your JSON list, output the real-time scores to the console, and send the emails to the targets that need your help.

## Disclaimer
This tool is meant for targeted, relevant B2B outreach. Ensure your email copy is compliant with anti-spam laws (like CAN-SPAM or GDPR) in your target region. Do not use this to spam thousands of irrelevant contacts.