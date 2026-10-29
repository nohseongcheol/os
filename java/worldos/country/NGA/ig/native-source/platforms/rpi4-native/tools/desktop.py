#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/desktọpụ_lèe.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('desktọpụ_lèe', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('desktọpụ_lèe')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'mmejọ', 'exact': '정확한값', 'network': 'Netwọọkụ', 'closed': '닫힘', 'length': 'ogologo_valuu', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'savà_valuu', 'resources': 'Iheejiarụ_gasị', 'data': 'datà', 'shift': 'ọtụgwo_SHIFT', 'send': 'zìga', 'run_desktop': 'mee_desktọpụ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'usu', 'text': 'SMS', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'otu_valuu_4b6d6445', 'tail': '끝부분', 'size': 'Ụhara', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klayènt', 'char': 'mkpụrụedemede_datà', 'work': '작업경로', 'Keyboard': 'ụgbọọtụgwo', 'x': 'ngakọrịta_x', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'agụment_MKPOKỌTA', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ùsòrò', 'Desktop': 'JIKỌ_desktọpụ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ngbanwụ_moòdù', 'command': 'Ntiiwu', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'ụzọ_ozi', 'cp': 'mkpụrụedemede_ntinye_koòdù', 'terminate': '종료시키기', 'security': 'Nche', 'vnc_port': '원격화면접속번호', 'body': 'àhụngwè', 'index': '색인', 'exited': '종료됨', 'keysym': 'ọtụgwo_adimara', 'output': '출력결과', 'keyboard': 'ụgbọọtụgwo_ndebà', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Ọgụụ', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
