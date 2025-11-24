from pyepidisplay.ci_mean import ci_mean

def test_smoke():
    """
    Simple smoke test to make sure the function runs and returns a dict.
    """
    result = ci_mean([1])
    assert isinstance(result, dict)
    return