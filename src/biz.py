from os import path
from itn.chinese.inverse_normalizer import InverseNormalizer
import sys


def _patch_file(relative_path: str, content: str):
    import itn

    file_path = path.join(path.dirname(itn.__file__), relative_path)
    if path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"_handle_blacklist_if_not: ok, path={file_path}")
    else:
        print(f"_handle_blacklist_if_not: file not found, path={file_path}")


def _patch():
    MM_TSV_CONTENT = """一月	1月
二月	2月
三月	3月
四月	4月
五月	5月
六月	6月
七月	7月
八月	8月
九月	9月
十月	10月
十一月	11月
十二月	12月
"""
    DD_TSV_CONTENT = """一日	1日
二日	2日
三日	3日
四日	4日
五日	5日
六日	6日
七日	7日
八日	8日
九日	9日
十日	10日
十一日	11日
十二日	12日
十三日	13日
十四日	14日
十五日	15日
十六日	16日
十七日	17日
十八日	18日
十九日	19日
二十日	20日
二十一日	21日
二十二日	22日
二十三日	23日
二十四日	24日
二十五日	25日
二十六日	26日
二十七日	27日
二十八日	28日
二十九日	29日
三十日	30日
三十一日	31日
一号	1号
二号	2号
三号	3号
四号	4号
五号	5号
六号	6号
七号	7号
八号	8号
九号	9号
十号	10号
十一号	11号
十二号	12号
十三号	13号
十四号	14号
十五号	15号
十六号	16号
十七号	17号
十八号	18号
十九号	19号
二十号	20号
二十一号	21号
二十二号	22号
二十三号	23号
二十四号	24号
二十五号	25号
二十六号	26号
二十七号	27号
二十八号	28号
二十九号	29号
三十号	30号
三十一号	31号
"""
    DATE_RULE_CONTENT = """from tn.processor import Processor
from tn.utils import get_abs_path

from pynini import string_file, accep
from pynini.lib.pynutil import delete, insert


class Date(Processor):

    def __init__(self):
        super().__init__(name='date')
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        digit = string_file(
            get_abs_path('../itn/chinese/data/number/digit.tsv'))  # 1 ~ 9
        zero = string_file(
            get_abs_path('../itn/chinese/data/number/zero.tsv'))  # 0

        yyyy = digit + (digit | zero)**3  # 二零零八年
        yyy = digit + (digit | zero)**2  # 公元一六八年
        yy = (digit | zero)**2  # 零八年奥运会
        mm = string_file(get_abs_path('../itn/chinese/data/date/mm.tsv'))
        dd = string_file(get_abs_path('../itn/chinese/data/date/dd.tsv'))

        # @CHANGE
        year = insert('year: "') + (yyyy | yyy | yy) + accep("年") + insert('" ')
        # year = insert('year: "') + (yyyy | yyy | yy) + \
        #     delete('年') + insert('" ')
        
        year_only = insert('year: "') + (yyyy | yyy | yy) + \
            accep('年') + insert('"')
        month = insert('month: "') + mm + insert('"')
        day = insert(' day: "') + dd + insert('"')

        # yyyy/mm/dd | yyyy/mm | mm/dd | yyyy
        date = ((year + month + day)
                | (year + month)
                | (month + day)) | year_only
        self.tagger = self.add_tokens(date)

    # @CHANGE
    def build_verbalizer(self):
        year = delete('year: "') + self.SIGMA + delete('" ')
        year_only = delete('year: "') + self.SIGMA + delete('"')
        month = delete('month: "') + self.SIGMA + delete('"')
        day = delete(' day: "') + self.SIGMA + delete('"')
        verbalizer = year.ques + month + day.ques
        verbalizer |= year_only
        self.verbalizer = self.delete_tokens(verbalizer)
    # def build_verbalizer(self):
    #     addsign = insert("/")
    #     year = delete('year: "') + self.SIGMA + delete('" ')
    #     year_only = delete('year: "') + self.SIGMA + delete('"')
    #     month = delete('month: "') + self.SIGMA + delete('"')
    #     day = delete(' day: "') + self.SIGMA + delete('"')
    #     verbalizer = (year + addsign).ques + month + (addsign + day).ques
    #     verbalizer |= year_only
    #     self.verbalizer = self.delete_tokens(verbalizer)

"""
    _patch_file("./chinese/data/date/mm.tsv", MM_TSV_CONTENT)
    _patch_file("./chinese/data/date/dd.tsv", DD_TSV_CONTENT)
    _patch_file("./chinese/rules/date.py", DATE_RULE_CONTENT)

    print("itn_source_patched")


# 修改源文件
_patch()

itn_model: InverseNormalizer = None  # type: ignore
# * Windows 平台下无法使用
if sys.platform != "win32":
    itn_model = InverseNormalizer(overwrite_cache=True)


def itn_text(text: str) -> str:
    if sys.platform == "win32":
        return text

    return itn_model.normalize(text)
