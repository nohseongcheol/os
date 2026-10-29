#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍')
    대응 = {'response': '응답자료', 'parts': 'ପଥ_ଉପାଦାନ', 's': 'ଷ୍ଟ୍ରିଂ_ଡାଟା', 'i': '순번', 'close': 'ବନ୍ଦ_କରନ୍ତୁ', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ', 'flags': '설정비트', 'ftp_port': 'ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍', 'args': 'ଯୁକ୍ତି_ଆରେ', 'server': 'ସର୍ଭର୍_ମୂଲ୍ୟ', 'data': 'ଡାଟା', 'ethernet_input': '이더넷입력', 'trace_packet': 'ଚିହ୍ନଟ_ପ୍ୟାକେଟ୍', 'GATEWAY': 'ପ୍ରବେଶ_ପଥ_ହାର୍ଡୱେର୍_ଠିକଣା', 'rule': 'ନିୟମ_ମୂଲ୍ୟ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ଆୟୋଜକ', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'ଅତିଥି', 'destination': 'ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା', 'ethernet_port': 'ଇଥରନେଟ୍_ପୋର୍ଟ', 'b': '둘째값', 'MAC': 'ମେସିନ୍_ଠିକଣା', 'arp': 'ଠିକଣା_ସ୍ପଷ୍ଟତା_ପ୍ୟାକେଟ୍', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'ଚକ୍ରାକାର_ମୂଲ୍ୟ', 'port': 'ପୋର୍ଟ୍_ନମ୍ଵର୍', 'offset': 'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ', 'readable': '읽을수있음', 'c': 'ବର୍ଣ୍ଣ_କୋଡ଼୍', 'p': 'ଡାଟା_ସ୍ଥିତି', 'writers': '쓰기대상들', 'IP': 'ଇଣ୍ଟର୍ନେଟ୍_ଠିକଣା_ମୂଲ୍ୟ', 'e': '보조항목', 'n': '개수', 'packet': 'ପ୍ୟାକେଟ୍_ଡାଟା', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍', 'window': 'ଓ୍ୱିଣ୍ଡୋ', 'capture': 'କ୍ୟାପଚର୍_କରିବା'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
