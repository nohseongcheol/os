#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/хувилбар_хэрэглэгч_орон_зай.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('хувилбар_хэрэглэгч_орон_зай', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('хувилбар_хэрэглэгч_орон_зай')
    대응 = {'mode': 'арга_горим', 'header': 'Толгой_утга', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Архив_хэрэгсэл', 'posix': '포직스경로', 'payload': 'ашигтай_ачаалал_өгөгдөл', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'өгөгдөл', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Бичвэр', 'headers': 'Толгой_Жагсаалт', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'хувилбар', 'build_users': 'үүсгэх_хэрэглэгч_орон_зай', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'програм_Толгой_Оффсет', 'offset': 'Оффсет_утга', 'text_address': 'команд_хаяг', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'Гүйцэтгэх_команд', 'path': 'ЗАМ', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Тохиргоо_утга', 'index': '색인', 'classes': 'класс_зам', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'өгөгдөл_хаяг', 'symbol': 'тэмдэг_утга', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Нэр', 'value': 'утга', 'fmt': 'формат_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
