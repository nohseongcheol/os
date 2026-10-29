#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/નેટવર્ક_બ્રિજ.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('નેટવર્ક_બ્રિજ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('નેટવર્ક_બ્રિજ')
    대응 = {'response': 'પ્રતિસાદ', 'parts': 'પાથ_ઘટક', 's': 'સ્ટ્રિંગ_ડેટા', 'i': '순번', 'close': 'બંધ_કરો', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'પ્રવેશ_મૂલ્ય', 'flags': '설정비트', 'ftp_port': 'ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર', 'args': 'દલીલ_અરે', 'server': 'સર્વર_મૂલ્ય', 'data': 'ડેટા', 'ethernet_input': '이더넷입력', 'trace_packet': 'ટ્રૅસ_પૅકેટ', 'GATEWAY': 'ગેટવે_હાર્ડવેર_સરનામું', 'rule': 'નિયમ_મૂલ્ય', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'હોસ્ટ', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'અતિથિ', 'destination': 'ગંતવ્ય_ડેટા_સરનામું', 'ethernet_port': 'ઇથરનેટ_પૉર્ટ', 'b': '둘째값', 'MAC': 'મશીન_સરનામું', 'arp': 'સરનામું_રિઝોલ્યૂશન_પૅકેટ', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'સાયકલ_મૂલ્ય', 'port': 'પોર્ટ_નંબર', 'offset': 'ઑફસેટ_મૂલ્ય', 'readable': '읽을수있음', 'c': 'વર્ણ_કોડ', 'p': 'ડેટા_સ્થિતિ', 'writers': '쓰기대상들', 'IP': 'ઇન્ટરનેટ_સરનામું_મૂલ્ય', 'e': '보조항목', 'n': '개수', 'packet': 'પૅકેટ_ડેટા', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'નેટવર્ક_બ્રિજ', 'window': 'વિંડો', 'capture': 'કૅપ્ચર_કરો'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
