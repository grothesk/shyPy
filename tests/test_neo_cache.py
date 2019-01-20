import pytest

from shypy.caching import NeoCache


demo_cnt = 0


@pytest.fixture(scope="function")
def dummy_cache():
    global demo_cnt
    demo_cnt = 0
    c = NeoCache(context='test')
    yield c
    c.clear_cache()
    del c


def test_basic_functionality(dummy_cache):

    @dummy_cache.register()
    def demo():
        global demo_cnt
        demo_cnt = demo_cnt + 1
        return 'demo'

    s = demo()

    assert demo_cnt == 1
    assert s == 'demo'

    s = demo()

    assert demo_cnt == 1
    assert s == 'demo'

    dummy_cache.clear_cache()
    s = demo()

    assert demo_cnt == 2
    assert s == 'demo'

    s = demo()

    assert demo_cnt == 2
    assert s == 'demo'

    dummy_cache.update()
    assert demo_cnt == 3


def test_function_with_input_argument(dummy_cache):

    def func_with_input(input):
        pass

    with pytest.raises(TypeError):
        assert dummy_cache.register(func_with_input)
