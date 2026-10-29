#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/àtẹ_iṣẹ́_wo.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('àtẹ_iṣẹ́_wo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('àtẹ_iṣẹ́_wo')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'àṣìṣe', 'exact': '정확한값', 'network': 'Alásopọ̀', 'closed': '닫힘', 'length': 'gígùn_iye', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'apèsè_iye', 'resources': 'àwọn_ohun_èlò', 'data': 'détà', 'shift': 'bọ́tìnnì_SHIFT', 'send': 'í_meèlì', 'run_desktop': 'ṣiṣẹ́_àtẹ_iṣẹ́', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'olùpèsè', 'text': 'SMS', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'afará', 'kind': 'ìsọ̀rí_iye', 'tail': '끝부분', 'size': 'Ìwọ̀n', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'aṣojú', 'char': 'ẹyọ_ọ̀rọ̀_détà', 'work': '작업경로', 'Keyboard': 'àtẹ_ìtẹ̀wé', 'x': 'ibi_ìtọ́kasí_x', 'down': '누르는중', 'net': 'Alásopọ̀_afará_ìgbéwọlé', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Ìlànà', 'Desktop': 'SOMỌ́_àtẹ_iṣẹ́', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ṣèpapòdà_móòdù', 'command': 'Àṣẹ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'ọ̀nà', 'cp': 'ẹyọ_ọ̀rọ̀_pípàrokò', 'terminate': '종료시키기', 'security': 'Ààbò', 'vnc_port': '원격화면접속번호', 'body': 'kókó_ọ̀rọ̀_ìkọ', 'index': '색인', 'exited': '종료됨', 'keysym': 'bọ́tìnnì_àmì', 'output': '출력결과', 'keyboard': 'àtẹ_ìtẹ̀wé_ìgbéwọlé', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'akàwé', 'NetworkBridge': 'Alásopọ̀_afará', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
