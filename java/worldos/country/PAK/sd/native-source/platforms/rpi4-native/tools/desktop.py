#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/ڊيسڪٽاپ_منظر.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('ڊيسڪٽاپ_منظر', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ڊيسڪٽاپ_منظر')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'نقص', 'exact': '정확한값', 'network': 'نيٽ_ورڪ', 'closed': '닫힘', 'length': 'لمبائي_قدر', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'سرور_قدر', 'resources': 'وسيلا', 'data': 'ڪوائف', 'shift': 'ڪليد_SHIFT', 'send': 'اي_ميل', 'run_desktop': 'هلائڻ_ڊيسڪٽاپ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'مهمان', 'text': 'متن', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'قسم_قدر_4b6d6445', 'tail': '끝부분', 'size': 'سائيز', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'گراهڪ', 'char': 'ڪريڪٽر_ڪوائف', 'work': '작업경로', 'Keyboard': 'ڪليدي_تختو', 'x': 'x_رطبو', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'دليل_ترتيب', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'عمل_a7054519', 'Desktop': 'ڪنيڪٽ_ڊيسڪٽاپ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'سوئچ_موڊ', 'command': 'حڪم', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'ڪرنسي_علامت', 'path': 'راههه', 'cp': 'ڪريڪٽر_ضابطه_ربائي', 'terminate': '종료시키기', 'security': 'سلامتي', 'vnc_port': '원격화면접속번호', 'body': 'باڊي_متن', 'index': '색인', 'exited': '종료됨', 'keysym': 'ڪليد_نشاني', 'output': '출력결과', 'keyboard': 'ڪليدي_تختو_داخلا', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ريڊر', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
