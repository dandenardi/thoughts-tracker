import os

def is_production():
    return os.getenv("ENVIRONMENT") == "production"

def is_development():
    return not is_production()