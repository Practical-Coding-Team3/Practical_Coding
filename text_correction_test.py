from konlpy.tag import Kkma
from konlpy.utils import pprint


kkma = Kkma()
pprint(kkma.sentences(u"안녕하세요 오늘 날씨가 많이 춥네요."))