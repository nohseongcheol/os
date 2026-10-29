#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/Biro_wonin.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('Biro_wonin', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Biro_wonin')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'njumte', 'exact': '정확한값', 'network': 'mbaal', 'closed': '닫힘', 'length': 'diir_xëyma', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'dëggu_xëyma', 'resources': 'costéef_yi', 'data': 'mbir', 'shift': 'caabi_Maj', 'send': 'Yónnee', 'run_desktop': 'daw_Biro', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'dalal', 'text': 'Tekst', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'poŋ', 'kind': 'ngiir_xëyma', 'tail': '끝부분', 'size': 'tolluwaay', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'lëkkalekat', 'char': 'Araf_mbir', 'work': '작업경로', 'Keyboard': 'arafukaay', 'x': 'rëddu_iks_yi', 'down': '누르는중', 'net': 'mbaal_poŋ_dugal_xabaar', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'Tegtal_TABLO', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'yokkute', 'Desktop': 'JOKKOO_Biro', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'jalantu_anam', 'command': 'ndigel', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Yoonu_jëmale', 'cp': 'Araf_nëbbin_ci_lim', 'terminate': '종료시키기', 'security': 'kaarànge', 'vnc_port': '원격화면접속번호', 'body': 'yaxub_mool', 'index': '색인', 'exited': '종료됨', 'keysym': 'kër_sembóol', 'output': '출력결과', 'keyboard': 'arafukaay_dugal_xabaar', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'jangkat', 'NetworkBridge': 'mbaal_poŋ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
