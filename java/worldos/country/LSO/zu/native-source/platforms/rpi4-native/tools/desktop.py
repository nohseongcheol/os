#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/ideskithophu_buka.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('ideskithophu_buka', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ideskithophu_buka')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Iphutha', 'exact': '정확한값', 'network': 'iNethiwekhi', 'closed': '닫힘', 'length': 'ubude_inani', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'Iseva_inani', 'resources': 'izinsiza', 'data': 'imininingwane', 'shift': 'inkinobho_ye_SHIFT', 'send': 'Thumela', 'run_desktop': 'sebenzisa_ideskithophu', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'singatha', 'text': 'Itekisi', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ibhuloho', 'kind': 'umunxa_inani', 'tail': '끝부분', 'size': 'Ubungako', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'iklayenti', 'char': 'uhlamvusimo_imininingwane', 'work': '작업경로', 'Keyboard': 'ikhibhodi', 'x': 'okuxhumanisa_u_x', 'down': '누르는중', 'net': 'iNethiwekhi_ibhuloho_okufakwayo', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Inqubo', 'Desktop': 'xhuma_ideskithophu', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'guqulela_kokunye_inqubo', 'command': 'Umlayelo', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'i_CTRL', 'path': 'Indlela_2', 'cp': 'uhlamvusimo_ukubhala_ngokufihla', 'terminate': '종료시키기', 'security': 'ukuphepha', 'vnc_port': '원격화면접속번호', 'body': 'umzimba_wombhalo', 'index': '색인', 'exited': '종료됨', 'keysym': 'inkomba_uphawu', 'output': '출력결과', 'keyboard': 'ikhibhodi_okufakwayo', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'umfundi', 'NetworkBridge': 'iNethiwekhi_ibhuloho', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
