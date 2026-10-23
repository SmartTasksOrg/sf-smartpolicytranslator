"""The command line: `sf-smartpolicytranslator --demo` runs with no input file and saves nothing."""
import json, os, sys
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
os.environ["SPT_SQLITE_PATH"] = os.path.join(os.path.dirname(__file__), "_t.db")

from sf_smartpolicytranslator import cli, iaiso_policy, audit


def test_bundled_sample_is_the_examples_file():
    with open(os.path.join(ROOT, "examples", "sample_regulation.txt"), encoding="utf-8") as f:
        assert cli.sample_regulation() == f.read()


def test_demo_prints_a_valid_strict_policy(capsys):
    before = len(audit.audit_trail(1000))
    assert cli.main(["--demo"]) == 0
    out = capsys.readouterr()
    policy = json.loads(out.out)
    assert iaiso_policy.validate(policy) == []
    assert policy["enforcement_mode"] == "strict"
    assert "valid=True" in out.err
    assert len(audit.audit_trail(1000)) == before          # --demo persists nothing


def test_a_source_file_still_works(capsys):
    path = os.path.join(ROOT, "examples", "sample_regulation.txt")
    assert cli.main([path, "--no-persist"]) == 0
    assert json.loads(capsys.readouterr().out)["version"] == "1"


def test_no_input_is_an_error_not_a_crash(capsys):
    with pytest.raises(SystemExit) as e:
        cli.main([])
    assert e.value.code == 2
    assert "--demo" in capsys.readouterr().err


def test_demo_and_source_together_are_refused():
    with pytest.raises(SystemExit) as e:
        cli.main(["--demo", "regulation.txt"])
    assert e.value.code == 2


def test_version(capsys):
    with pytest.raises(SystemExit) as e:
        cli.main(["--version"])
    assert e.value.code == 0
    assert capsys.readouterr().out.startswith("SmartPolicyTranslator ")
