from repofactory.builder import RepoConfig, validate_config


def test_missing_required_fields():
    cfg = RepoConfig(name="", type="", language="", features=[])
    errors = validate_config(cfg)
    assert "name is required" in errors
    assert any("type" in e for e in errors)
    assert any("language" in e for e in errors)


def test_unknown_feature_rejected():
    cfg = RepoConfig(name="demo", type="cli", language="python", features=["lint", "wtf"])
    errors = validate_config(cfg)
    assert errors and "unknown features" in errors[0]


def test_valid_config_passes():
    cfg = RepoConfig(name="demo", type="cli", language="python", features=["lint", "tests"])
    errors = validate_config(cfg)
    assert errors == []
