#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/верзија_корисник_простор.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('верзија_корисник_простор', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('верзија_корисник_простор')
    대응 = {'mode': 'метод_MODE', 'header': 'Заглавие_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Архива_алатка', 'posix': '포직스경로', 'payload': 'капацитет_податоци', 'flags': 'конфигурација_Услуга_за_интелигентен_пренос_во_заднина', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'податоци', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'склад_патека', 'build_python': 'Create_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Текст', 'headers': 'Заглавие_Список', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'верзија', 'build_users': 'Create_корисник_простор', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'програма_Заглавие_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'наредба_адреса', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'Изврши_наредба', 'path': 'ПАТЕКА', 'p': 'податоци_позиционирање', 'changed': '바뀐자료', 'n': 'ставка_COUNT', 'flag': 'Параметри_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'класа_патека', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'податоци_адреса', 'symbol': 'симбол_VALUE', 'root': 'корен_адреса', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Име', 'value': 'VALUE', 'fmt': 'формат_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
