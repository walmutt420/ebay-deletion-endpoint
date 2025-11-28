import base64
import requests
import time

# ============================
# eBay OAuth Config
# ============================
EBAY_APP_ID = "JasonHub-searchen-PRD-a705dc6eb-7a92fc75"
EBAY_CERT_ID = "PRD-705d********-****-****-a75d-527e"   # masked version
EBAY_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# Cache token so we don’t request every time
_cached_token = None
_cached_expiry = 0


def get_ebay_oauth_token():
    global _cached_token, _cached_expiry

    # Return cached token if still valid
    if _cached_token and time.time() < _cached_expiry:
        return _cached_token

    # Build Basic auth header: base64(appid:certid)
    basic_auth_string = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    basic_auth_encoded = base64.b64encode(basic_auth_string.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic_auth_encoded}"
    }

    body = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    response = requests.post(EBAY_OAUTH_URL, headers=headers, data=body)

    if response.status_code != 200:
        print("ERROR requesting OAuth token:", response.text)
        return None

    data = response.json()
    access_token = data["access_token"]
    expires_in = data["expires_in"]

    # Save in memory
    _cached_token = access_token
    _cached_expiry = time.time() + expires_in - 60  # renew 60 sec early

    return access_token
