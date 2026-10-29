#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/хувилбар_Сүлжээ.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('хувилбар_Сүлжээ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('хувилбар_Сүлжээ')
    대응 = {'obj': 'товлосон_файл', 'objects': 'товлосон_газар_Файлууд', 'library': 'сан', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'файл_Жагсаалт', 'source': '원본자료', 'run': 'Гүйцэтгэх_команд', 'flags': '설정비트', 'path': 'ЗАМ', 'build_network': 'үүсгэх_Сүлжээ', 'cc': '시언어번역기', 'ar': 'Архив_хэрэгсэл'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
