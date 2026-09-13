from integration_hub.core.config import Settings


def test_settings_reads_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg2://user:pass@host:5432/db")

    settings = Settings(_env_file=None)

    assert settings.database_url == "postgresql+psycopg2://user:pass@host:5432/db"


def test_settings_has_sane_default():
    settings = Settings(_env_file=None)

    assert settings.database_url.startswith("postgresql+psycopg2://")
