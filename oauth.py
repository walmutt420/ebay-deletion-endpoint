import base64
import os
import time
import requests

# ============================
# eBay OAuth Config
# ============================

# From your eBay Dev Portal (Production)
EBAY_APP_ID = "JasonHub-searchen-PRD-a705dc6eb-7a92fc75"

# DO NOT hardcode the full Cert ID in code.
# We'll read it from an environment variable instead.
EBAY_CERT_ID = os.environ.get("EBAY_CERT_ID")

EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# Simple in-memory token cache
_cached_token = None
_cached_expiry = 0


def get_ebay_oauth_token() -> str | None:
    """
    Get (or refresh) an OAuth token from eBay using the Client Credentials flow.
    Uses the 'EBAY_CERT_ID' from environment variables.
    """
    global _cached_token, _cached_expiry

    if not EBAY_CERT_ID:
        print("ERROR: EBAY_CERT_ID is not set in environment variables.")
        return None

    # Return cached token if still valid
    now = time.time()
    if _cached_token and now < _cached_expiry:
        return _cached_token

    # Build Basic auth: base64(appid:certid)
    basic_auth_string = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    basic_auth_encoded = base64.b64encode(basic_auth_string.encode("utf-8")).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic_auth_encoded}",
    }

    body = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }

    try:
        resp = requests.post(EBAY_OAUTH_URL, headers=headers, data=body, timeout=20)
    except Exception as e:
        print("ERROR: Exception while requesting eBay OAuth token:", e)
        return None

    if resp.status_code != 200:
        print("ERROR: eBay OAuth token request failed:", resp.status_code, resp.text)
        return None

    data = resp.json()
    access_token = data.get("access_token")
    expires_in = data.get("expires_in", 0)

    if not access_token:
        print("ERROR: No access_token in eBay OAuth response:", data)
        return None

    # cache token
    _cached_token = access_token
    _cached_expiry = now + int(expires_in) - 60  # renew 1 minute early

    print("Got new eBay OAuth token, expires in", expires_in, "seconds")
    return access_token

