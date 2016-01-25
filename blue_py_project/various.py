import pytest

# all other code, only separated setuptools.py because it should be lean on dependencies

def run_tests(project_name):
    args = (
        '-m current '
#         '-n auto --benchmark-disable'  # parallel testing (can't and shouldn't benchmark in parallel, so --benchmark-disable)
#         '--maxfail=1 '
        '--capture=no '
        '--basetemp=test/last_runs '
        '{}/test '
    ).format(project_name)
    pytest.main(args)