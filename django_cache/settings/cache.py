import os 

# Enable/disable cacheops functionality
ENABLE_CACHEOPS = os.environ.get("ENABLE_CACHEOPS", "TRUE") == "TRUE"

CACHEOPS_REDIS = os.environ.get(
    "CACHEOPS_REDIS", "redis://localhost:6379/1"
)
CACHEOPS_DEFAULT_TIMEOUT = os.environ.get("CACHEOPS_DEFAULT_TIMEOUT", 86400)
CACHEOPS_DEFAULTS = os.environ.get(
    "CACHEOPS_DEFAULTS",
    {"timeout": CACHEOPS_DEFAULT_TIMEOUT},
)

CACHEOPS_DEGRADE_ON_FAILURE = (
    os.environ.get("CACHEOPS_DEGRADE_ON_FAILURE", "TRUE") == "TRUE"
)
CACHE_OPERATIONS = ("get", "fetch", "exists")

PRODUCT_APP_CACHEOPS = {
    "products.Product": {"ops": CACHE_OPERATIONS},
}

# Only apply caching if enabled
CACHEOPS = {}
CACHEOPS.update(**PRODUCT_APP_CACHEOPS)