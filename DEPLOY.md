# 🚀 Deployment Guide

## Option A: Streamlit Community Cloud (Recommended)
This is the easiest and most stable way to host your dashboard.

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Sign in with **GitHub**.
3.  Click **"New App"**.
4.  Select your repository: `madsonpapito/btc-smart2.0`.
5.  **Main File Path**: `dashboard.py`.
6.  **Advanced Settings (Secrets)**:
    *   You MUST add your passwords here because `.env` is ignored by Git (for security).
    *   Copy contents of your local `.env` and paste them into the "Secrets" box:
    ```toml
    TELEGRAM_TOKEN = "..."
    TELEGRAM_CHAT_ID = "..."
    WALLET_ADDRESS = "..."
    ```
7.  Click **Deploy**.

## Option B: Vercel (Not Recommended for Streamlit)
Vercel is great for Next.js/React but struggles with Streamlit's "Always On" connection (WebSockets). Your dashboard might disconnect frequently or lose state (the logic variables).

If you really want Vercel, you need to:
1.  Add a `vercel.json` config.
2.  Likely wrap it in a Docker container or use a specific runtime, which is complex.

**My Advice**: Use Streamlit Cloud for this version.
