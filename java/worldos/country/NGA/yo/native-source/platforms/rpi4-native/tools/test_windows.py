#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/창시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'ibi_ìtọ́kasí_x', 's': 'fọ́nrán_détà', 'xy': 'ohun_aṣàpèjúwe_adálérí_ọ̀pọ̀_ẹ̀yà_abèjì', 'sel': 'olùyàn_a916db4e', 'seconds': '초단위', 'log': 'àkọsílẹ̀_ìṣe_ìlà_ìbú', 'at': '현재위치', 'send': 'í_meèlì', 'main': 'Rọ́ọ̀nù', 'req': '요청값', 'hot': 'àbùjá_iye', 'pump': 'èkù_ìgbéṣẹ̀', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Àṣẹ', 'shell': 'ṣẹ́ẹ̀lì', 'f': 'fáìlì_ìgbéwọlé', 'color': '색상', 'click': 'ṣíra_tẹ_bọ́tìnnì', 'k': '셋째순번', 'c': 'kóòdù_ẹyọ_ọ̀rọ̀', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'parí_Ìtayọ', 'command_mode': 'àṣẹ_móòdù', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'Àfọwọ́sí_ìjábọ̀', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
