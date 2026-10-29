#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/دێسکتۆپ_دیمەن.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('دێسکتۆپ_دیمەن', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('دێسکتۆپ_دیمەن')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'هەڵە', 'exact': '정확한값', 'network': 'تۆڕ', 'closed': '닫힘', 'length': 'درێژی_نرخ', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'ڕاژەکار_نرخ', 'resources': 'سەرچاوە_50487cae', 'data': 'دەیتا', 'shift': 'کلیلی_SHIFT', 'send': 'ناردن', 'run_desktop': 'ڕادان_دێسکتۆپ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'جێدەر', 'text': 'دەق', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'پۆل_نرخ', 'tail': '끝부분', 'size': 'گۆڕینی_ئەندازە', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'کلایەنت', 'char': 'نووسە_دەیتا', 'work': '작업경로', 'Keyboard': 'تەختەکلیل', 'x': 'پۆوتانی_x', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'پرۆسە', 'Desktop': 'لكاندن_دێسکتۆپ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'گۆڕین_دۆخ', 'command': 'فەرمان', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'گوزەر', 'cp': 'نووسە_نهێنبەندی', 'terminate': '종료시키기', 'security': 'ئاسایش', 'vnc_port': '원격화면접속번호', 'body': 'دەقی_تێکستەکە', 'index': '색인', 'exited': '종료됨', 'keysym': 'کلیل_سیمبۆل', 'output': '출력결과', 'keyboard': 'تەختەکلیل_تێنووسین', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'خوێنەر', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
