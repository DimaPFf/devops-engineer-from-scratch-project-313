from src.services.utils.get_range import get_range

def test_get_range():
    result_1 = get_range('[1,10]')
    assert result_1 == (1, 9)
    result_2 = get_range('[2,1]')
    assert result_2 == None
    result_3 = get_range('[-1,10]')
    assert result_3 == None
    result_4 = get_range('[10,-1]')
    assert result_4 == None
    result_5 = get_range('[1,5]')
    assert result_5 == (1, 4)