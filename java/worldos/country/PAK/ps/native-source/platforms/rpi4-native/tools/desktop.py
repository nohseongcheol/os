#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/سرپاڼه_ليد.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('سرپاڼه_ليد', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('سرپاڼه_ليد')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'تېروتنه', 'exact': '정확한값', 'network': 'جال', 'closed': '닫힘', 'length': 'اوږدوالى_ارزښت', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': '서버', 'resources': '자원관리', 'data': 'اومتوک', 'shift': 'SHIFT_کيلي', 'send': 'استول', 'run_desktop': '바탕화면실행', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'کوربه', 'text': 'ليکنه', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'ټولۍ_ارزښت', 'tail': '끝부분', 'size': 'کچ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'پېرن', 'char': 'لوښه_اومتوک', 'work': '작업경로', 'Keyboard': 'کيليدړه', 'x': '가로좌표', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ارزښتوړى_لړوند', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'بهير', 'Desktop': 'پيوستول_سرپاڼه', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': '전환', 'command': 'بولۍ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_کيلي', 'path': 'يونلور', 'cp': 'لوښه_کوډييزونه', 'terminate': '종료시키기', 'security': 'خونديتوب', 'vnc_port': '원격화면접속번호', 'body': 'تنه_متن', 'index': '색인', 'exited': '종료됨', 'keysym': '글쇠기호', 'output': '출력결과', 'keyboard': 'کيليدړه_ننوت', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'لوستونکی', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
