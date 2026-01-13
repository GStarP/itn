from src.biz import itn_text


def test_multi_bit_num():
    raw_text = "买一百手上海电气"
    expected_text = "买100手上海电气"

    assert itn_text(raw_text) == expected_text


def test_continuous_num():
    raw_text = "东方财富代码为三零零五九"
    expected_text = "东方财富代码为30059"

    assert itn_text(raw_text) == expected_text


def test_date():
    # 日
    # ! X号 不支持，因为和其它含义冲突（如 五号球员）
    raw_text = "我十五日回家"
    expected_text = "我15日回家"
    assert itn_text(raw_text) == expected_text

    # 月
    raw_text = "我十二月回家"
    expected_text = "我12月回家"
    assert itn_text(raw_text) == expected_text

    # 年
    raw_text = "我二零三零年回家"
    expected_text = "我2030年回家"
    assert itn_text(raw_text) == expected_text

    # 年月
    raw_text = "我二零二六年七月回家"
    expected_text = "我2026年7月回家"
    assert itn_text(raw_text) == expected_text

    # 月日
    raw_text = "我七月八号回家"
    expected_text = "我7月8号回家"

    assert itn_text(raw_text) == expected_text

    # 年月日
    raw_text = "我二零二五年七月八号回家"
    expected_text = "我2025年7月8号回家"

    assert itn_text(raw_text) == expected_text


def test_money():
    raw_text = "金价是一千三百元"
    expected_text = "金价是1300元"

    assert itn_text(raw_text) == expected_text
