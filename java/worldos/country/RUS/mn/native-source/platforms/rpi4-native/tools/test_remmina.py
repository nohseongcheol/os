#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/원격한글시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Ажиллуулах', 'profile': 'Хувийн_тохиргоо', 'focused': 'Төвлөрсөн', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'сервер_утга', 'log': 'бичих_мөр_6e8b375a', 'args': 'аргумент_олонлог', 'deadline': '마감시각', 'data': 'өгөгдөл', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Ажиллуулах', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Бичвэр', 'out': '결과자료', 'env': '환경', 'f': 'файл_оролт', 'port': '접속번호', 'offset': 'Оффсет_утга', 'version': '판번호', 'p': '자료위치', 'selector': 'сонгогч', 'xvfb': 'виртуал_дэлгэц', 'display': 'дэлгэц_d6881d24', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Нэр', 'window': 'цонх', 'report': 'баталгаажуулалт_тайлан', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
