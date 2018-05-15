import pytest

from shypy.util.decorators import CheckRaiseDecorator


def test_check_raise_decorator():

    def is_int(data):
        return isinstance(data, int)

    def is_pos(data):
        return data > 0

    def is_str(data):
        return isinstance(data, str)


    class NoInt(Exception):
        pass

    class NotPos(Exception):
        pass

    class NoStr(Exception):
        pass


    CheckInt = CheckRaiseDecorator(is_int, NoInt)
    CheckPos = CheckRaiseDecorator(is_pos, NotPos)
    CheckStr = CheckRaiseDecorator(is_str, NoStr)


    @CheckInt([0, 1])
    @CheckPos([1])
    @CheckStr([2])
    def print_int_posint_str(a, b, c):
        print()
        print(a)
        print(b)
        print(c)


    assert print_int_posint_str(-1, 1, 'Test') is None

    with pytest.raises(NoInt):
        assert print_int_posint_str('-1',   1, 'Test')
        assert print_int_posint_str(  -1, '1', 'Test')
        assert print_int_posint_str(-1.0,   1, 'Test')
        assert print_int_posint_str(  -1, 1.0, 'Test')

    with pytest.raises(NotPos):
        assert print_int_posint_str(  -1,  -1, 'Test')
        assert print_int_posint_str(  -1,   0, 'Test')

    with pytest.raises(NoStr):
        assert print_int_posint_str(  -1,   1,     -1)
        assert print_int_posint_str(  -1,   1,    1.0)



