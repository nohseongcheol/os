#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/хувилбар_систем.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('хувилбар_систем', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('хувилбар_систем')
    대응 = {'network': 'Сүлжээ', 'BUILD': 'хувилбар_зам', 'ar': 'Архив_хэрэгсэл', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'үсгийн_хэв_өгөгдөл', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_олонлог', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'арга_оролт', 'main': 'Ажиллуулах', 'objcopy': 'объект_файл_хувиргуур', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'үүсгэх_хэрэглэгч_орон_зай', 'f': 'файл_оролт', 'extra': '추가영역', 'exports': 'экспортлох_хүснэгт', 'jobs': '빌드작업', 'run': 'Гүйцэтгэх_команд', 'path': 'ЗАМ', 'REPO': '저장소', 'tool': 'Хэрэгслүүд', 'classes': 'класс_зам', 'output': '출력결과', 'samples': '예제들', 'symbol': 'тэмдэг_утга', 'source': '원본자료', 'name': 'Нэр', 'build_network': 'үүсгэх_Сүлжээ', 'font_info': 'үсгийн_хэв_мэдээлэл', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
