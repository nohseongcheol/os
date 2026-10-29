#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/Create_фото.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('Create_фото', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('Create_фото')
    сопоставление_ЗНАЧЕН = {'total': 'итог_емкость', 'start': 'запустить', 'firmware': 'встроенное_ПО_ЗНАЧЕН', 'files': 'список_файлов', 'archive_base': 'Архив_база', 'partition': 'раздел_файл', 'archive': 'Архив', 'main': 'запустить', 'block': 'блок_данных', 'ROOT': 'задача_корень', 'boot': '부팅경로', 'stage': 'этап_ЗНАЧЕН', 'out': 'KR_данные', 'expected': '예상결과', 'f': 'файл_ввод', 'src': '원본주소', 'path': 'путь', 'p': 'данные_позиция', 'extracted': '추출자료', 'member': 'член', 'mbr': 'главная_загрузочная_запись', 'image': 'фото', 'sector_count': '섹터개수', 'dist': 'распределение_путь', 'sha': '해시계산', 'license_': 'лицензия', 'source': '원본자료', 'name': 'Название', 'value': 'ЗНАЧЕН', 'manifest': 'пакет_манифест', 'dest': 'цель_ЗНАЧЕН_позиция', 'work': '작업경로'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
