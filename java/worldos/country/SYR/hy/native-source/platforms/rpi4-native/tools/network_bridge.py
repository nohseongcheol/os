#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/Ցանց_կամուրջ.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('Ցանց_կամուրջ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Ցանց_կամուրջ')
    대응 = {'response': '응답자료', 'parts': 'ուղի_բաղադրիչ', 's': 'տող_տվյալ', 'i': '순번', 'close': 'Փակ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'մուտքագրում_արժեք', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'արգումենտ_ԶԱՆԳՎԱԾ', 'server': 'սպասարկիչ_արժեք', 'data': 'տվյալ', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': '관문기계주소', 'rule': 'զտիչ_արժեք', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'հոստ', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'հյուր', 'destination': 'նպատակակետ_տվյալ_հասցե', 'ethernet_port': '이더넷접속번호', 'b': '둘째값', 'MAC': 'մեքենա_հասցե', 'arp': 'հասցե_տարլուծում_փաթեթ', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Շրջան_արժեք', 'port': '접속번호', 'offset': 'Տեղաշարժում_արժեք', 'readable': '읽을수있음', 'c': 'գրանշանի_կոդ', 'p': 'տվյալ_դիրք', 'writers': '쓰기대상들', 'IP': 'համացանցի_հասցե_արժեք', 'e': '보조항목', 'n': '개수', 'packet': 'փաթեթ_տվյալ', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Ցանց_կամուրջ', 'window': 'պատուհան', 'capture': 'նկարահանել'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
