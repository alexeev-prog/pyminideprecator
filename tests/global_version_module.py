from pyminideprecator import deprecate


@deprecate("2.0.0", "Test global function")
def test_global():
    pass
