#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/예제시험.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'اومتوک', 'graphics_command': '그림명령', 'main': 'ځغلول', 'row': '행위치', 'init': '초기값', 'target': '대상', 'ROOT': '기준', 'text': 'ليکنه', 'binary': 'دويال', 'out': '결과자료', 'entry': 'ننوت_ټکى', 'got': '받은수', 'port': '접속번호', 'graphics_start': '그림시작', 'col': '열위치', 'begin': '시작위치', 'kind': 'ټولۍ_ارزښت', 'selector': '준비선택기', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'پېرن', 'line': 'ليکه', 'report': 'باورکړن_راپور', 'language': 'کمپیوټر_ژبه', 'x': '가로좌표', 'start': 'ځغلول', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': '목록보내기', 'payload': '내용자료', 'proc': 'بهير', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': '이름표', 'content': 'منځپانګه_ارزښت', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': '파일이름', 'shell': 'سیپۍ', 'color': '색상', 'transcript': '대화기록', 'offset': '변위', 'h': '높이값', 'run': '실행', 'c': '문자값', 'path': 'يونلور', 'encoding': 'لوښه_غونډ', 'end': '끝위치', 'ftp': 'دوتنه_لېږدول_پيوستون', 'pixels': '화소들', 'symbol': '심볼', 'source': '원본자료', 'name': 'نوم', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
