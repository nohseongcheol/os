#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'өгөгдөл', 'img': 'зураг_утга_c143fe9e', 'bits': '비트들', 'x': 'х_координат', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'зам_Жагсаалт', 'y': '세로좌표', 'main': 'Ажиллуулах', 'src': '원본주소', 'fonts': 'үсгийн_хэв_Жагсаалт', 'ROOT': '기준', 'p': '자료위치', 'cp': 'тэмдэгт_кодчлол', 'target': 'зорилго'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
