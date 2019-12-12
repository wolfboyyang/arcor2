from openapi_spec_validator import validate_spec  # type: ignore
import yaml
from subprocess import check_output


def test_execution_proxy_openapi():
    validate_spec(yaml.full_load(check_output(["arcor2_execution_proxy", "--swagger"])))
