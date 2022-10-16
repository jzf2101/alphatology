from negative import check_violations


def test_checkviolations():
    v, b, w = check_violations([1, 2, 3, 4], [5, 6, 7, 8], [1, 2], [5, 6])
    assert v == 4
    assert b == 2
    assert w == 2

    v, b, w = check_violations([1, 2, 3, 4], [5, 6, 7, 8], [5, 6], [1, 2],)
    assert v == 0
    assert b == 0
    assert w == 0

    v, b, w = check_violations([1, 2, 3, 4], [5, 6, 7, 8], [5, 6, 3, 4,], [1, 2, 7, 8],)
    assert v == 4
    assert b == 2
    assert w == 2
