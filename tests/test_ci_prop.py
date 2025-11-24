from pyepidisplay.ci_prop import ci_prop

def test_smoke():
    """
    Simple smoke test to make sure the function runs and returns a dict.
    """
    result = ci_prop([1])
    assert isinstance(result, dict)
    return