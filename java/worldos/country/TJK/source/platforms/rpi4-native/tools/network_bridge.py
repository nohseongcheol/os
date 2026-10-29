#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/Шабака_кӯпрук.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('Шабака_кӯпрук', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Шабака_кӯпрук')
    대응 = {'response': '응답자료', 'parts': 'масир_ҷузъ', 's': 'сатр_иттилоот', 'i': '순번', 'close': 'Пӯшидан', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ворида_қимат', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'аргумент_қатор', 'server': 'сервер_қимат', 'data': 'иттилоот', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'филтр_қимат', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'мизбон', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'меҳмон', 'destination': 'ҷои_таъинот_иттилоот_суроға', 'ethernet_port': 'Итранет_порт', 'b': '둘째값', 'MAC': 'компютер_суроға', 'arp': '주소찾기전문', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Ҳалқа_қимат', 'port': '접속번호', 'offset': 'Интиқолшавӣ_қимат', 'readable': '읽을수있음', 'c': 'рамзи_аломат', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'суроғаи_Интернет_қимат', 'e': '보조항목', 'n': '개수', 'packet': '꾸러미자료', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Шабака_кӯпрук', 'window': 'равзана', 'capture': 'акс_гирифтан'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
