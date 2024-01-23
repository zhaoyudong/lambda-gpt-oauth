import os

GPT_APP_CACHE_TABLE_NAME = os.getenv("GPTAPPCACHE_TABLE_NAME")

CACHE_KEY_NAME = "cache_key"

EXPIRATION_FIELD = "expired_at"

TEST_CLIENTS = {
    "oauth-demo-client": "oauth-demo-secret"
}

TEST_USERS = {
    "foo": {
        "password": "bar",
        "full_name": "test_user"
    }
}



