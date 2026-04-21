import asyncio
import json
import os

import httpx
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


async def get_score(http_client: httpx.AsyncClient, url: str) -> int | None:
    clean_url = url.strip()

    print(f"[*] Analyzing performance of: {clean_url}")

    if not GOOGLE_API_KEY:
        print("[-] CRITICAL ERROR: Google API Key is not loaded. Check your .env file")
        return None

    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    parameters = {"url": clean_url, "strategy": "mobile", "key": GOOGLE_API_KEY}

    try:
        response = await http_client.get(api_url, params=parameters, timeout=30.0)
        data = response.json()

        if "error" in data:
            error_message = data["error"].get("message", "Unknown error")
            print(f"[-] API Error for {clean_url}: {error_message}")
            return None

        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})
        performance = categories.get("performance", {})
        score = performance.get("score")

        if score is None:
            print(
                f"[-] Google could not calculate the score for {clean_url} (The website blocks bots, failed to render, or internal timeout)."
            )
            return None

        return int(score * 100)

    except httpx.ReadTimeout:
        print(f"[-] Timeout: Google took too long to audit {clean_url}")
        return None
    except Exception as e:
        print(f"[-] Exception analyzing {clean_url}: {e}")
        return None


def send_email(company: str, target_email: str, score: int) -> bool:
    html_body = f"""
    <p>Hi {company} team,</p>
    <p>I’ve been checking out your agency's work. You run great campaigns, but I just ran your site through Google Web Vitals and you're currently sitting at a <strong>{score}/100</strong> on mobile performance.</p>
    <p>You already know the math: sending 2026 paid traffic to a bloated WordPress/Elementor architecture means you're losing up to 20% of your conversions before the page even loads. If your own site is lagging, your clients' landing pages are likely leaking ad spend too.</p>
    <p>I’m John Doe, founder of Zero Delay. We act as the external, white-label engineering department for growth and performance agencies.</p>
    <p>We rebuild landing pages using pure native code (Astro) to guarantee sub-second load times and 100/100 PageSpeed scores. Your clients get cheaper CPAs, your campaigns scale faster, and you take all the credit.</p>
    <p>Quick proposal:<br>
    Reply to this email with the URL of your slowest client landing page. We’ll send you back a 2-minute Loom video breaking down exactly how many conversions that code bloat is costing you right now. No strings attached.</p>
    <p>Best,<br>John Doe<br>Zero Delay - Sub-second Landings for Ads<br>
    <a href="https://zeroredirect.dev">zeroredirect.dev</a></p>
    """

    try:
        resend.Emails.send(
            {
                "from": "John Doe <send@marketing.com>",
                "to": target_email,
                "subject": "Quick question about your mobile performance",
                "html": html_body,
                "reply_to": "john@marketing.com",
            }
        )
        print(f"[+] SUCCESS: Email sent to {company} ({target_email}).")
        return True
    except Exception as e:
        print(f"[-] Failed to send email to {company}: {e}")
        return False


async def main():
    try:
        with open("agencies.json", "r", encoding="utf-8") as f:
            agencies = json.load(f)
    except FileNotFoundError:
        print("[-] Error: The file agencies.json was not found")
        return

    print(f"\n[INFO] Starting audit for {len(agencies)} agencies...\n")

    async with httpx.AsyncClient() as http_client:
        for agency in agencies:
            company = agency["company"]
            target_email = agency["email"]
            url = agency["url"]

            score = await get_score(http_client, url)

            if not score or score > 85:
                print(
                    f"[SKIP] {company} ignored. Score: {score}/100 or technical failure.\n"
                )
                continue

            print(f"[TARGET] {company} detected with {score}/100. Firing cold email...")
            send_email(company, target_email, score)

            print("[INFO] 20-second safety pause...\n")
            await asyncio.sleep(20)

    print("[INFO] Sequence finished.")


if __name__ == "__main__":
    asyncio.run(main())
