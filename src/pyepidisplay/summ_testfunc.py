#Test function for summ

# test_summ_function.py

import pytest
from CSE583_summ_function import summ

def test_one_shot():
    """One-shot test: check a known input/output pair."""
    data = [1, 2, 3, 4]
    result = summ(data)
    assert result == 10  # expected sum

def test_smoke():
    """Smoke test: just verify the function runs without errors."""
    try:
        _ = summ([0, 1, 2])
    except Exception as e:
        pytest.fail(f"Smoke test failed with exception: {e}")



#testing
pytest summ_testfunc.py
