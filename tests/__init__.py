from alayatodo import create_app
from alayatodo.config import TestConfig


app = create_app(TestConfig)
app_protected = create_app()
