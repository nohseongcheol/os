"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

મશીન_સરનામું = bytes.fromhex('525400123456')
ગેટવે_હાર્ડવેર_સરનામું = bytes.fromhex('52550a000202')
ઇન્ટરનેટ_સરનામું_મૂલ્ય = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class નેટવર્ક_બ્રિજ:
    def __init__(자신, ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર=2121, 전달규칙들=(), કૅપ્ચર_કરો=False, અતિથિ_સરનામું=None, હોસ્ટ_સરનામું='127.0.0.1'):
        if not 1024 <= ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર <= 65535 or 50000 <= ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર = ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        અતિથિ_સરનામું = અતિથિ_સરનામું or 자신.ip_config['IP']
        qemu_network(자신.ip_config, અતિથિ_સરનામું)
        સરનામું=ipaddress.IPv4Address(અતિથિ_સરનામું)
        자신.અતિથિ_સરનામું=str(સરનામું); 자신.현재주소=સરનામું.packed
        સરનામું=ipaddress.IPv4Address(હોસ્ટ_સરનામું)
        if સરનામું.is_multicast or str(સરનામું)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.હોસ્ટ_સરનામું=str(સરનામું)
        자신.કૅપ્ચર_કરો = કૅપ્ચર_કરો; 자신.ટ્રૅસ_લૉગ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર)} | {('tcp', ડેટા_સ્થિતિ) for ડેટા_સ્થિતિ in range(50000,50008)}
        for નિયમ_મૂલ્ય in 전달규칙들:
            પાથ_ઘટક = નિયમ_મૂલ્ય.split(':')
            if len(પાથ_ઘટક) != 3 or પાથ_ઘટક[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, હોસ્ટ, અતિથિ = પાથ_ઘટક[0], int(પાથ_ઘટક[1]), int(પાથ_ઘટક[2])
            if not 1024 <= હોસ્ટ <= 65535 or not 1 <= અતિથિ <= 65535 or (통신규약, હોસ્ટ) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + નિયમ_મૂલ્ય)
            사용중주소.add((통신규약, હોસ્ટ)); 자신.전달규칙들.append((통신규약, હોસ્ટ, અતિથિ))
        자신.수신창구들 = []
        for _ in range(2):
            સર્વર_મૂલ્ય = socket.socket()
            સર્વર_મૂલ્ય.bind(('127.0.0.1', 0)); સર્વર_મૂલ્ય.listen(1); સર્વર_મૂલ્ય.setblocking(False)
            자신.수신창구들.append(સર્વર_મૂલ્ય)
        자신.접속자들 = [None, None]
        자신.ઇન્ટરમિટેંટ_બાકી = [bytearray(), bytearray()]
        자신.ઇથરનેટ = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.ઇન્ટરમિટેંટ_અમાન્ય = False
        자신.થોભો_ઇવેંટ = threading.Event(); 자신.ભૂલ = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.સાયકલ_મૂલ્ય, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ઇથરનેટ_પૉર્ટ = [સ્ટ્રિંગ_ડેટા.getsockname()[1] for સ્ટ્રિંગ_ડેટા in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.અતિથિ_સરનામું) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર, 자신.અતિથિ_સરનામું)
        for પોર્ટ_નંબર in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(પોર્ટ_નંબર, 자신.અતિથિ_સરનામું)
        for 통신규약, હોસ્ટ, અતિથિ in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, હોસ્ટ, 자신.અતિથિ_સરનામું, અતિથિ)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.હોસ્ટ_સરનામું+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ઇથરનેટ_પૉર્ટ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, પૅકેટ_ડેટા):
        자신.ઇન્ટરમિટેંટ_બાકી[1] += struct.pack('!I', len(પૅકેટ_ડેટા)) + પૅકેટ_ડેટા

    def ટ્રૅસ_પૅકેટ(자신, 방향, પૅકેટ_ડેટા):
        if not 자신.કૅપ્ચર_કરો or len(પૅકેટ_ડેટા)<20: return
        ઑફસેટ_મૂલ્ય=(પૅકેટ_ડેટા[0]&15)*4
        પ્રવેશ_મૂલ્ય={'time':time.monotonic(),'direction':방향,'bytes':len(પૅકેટ_ડેટા),'protocol':પૅકેટ_ડેટા[9]}
        if પૅકેટ_ડેટા[9]==6 and len(પૅકેટ_ડેટા)>=ઑફસેટ_મૂલ્ય+20:
            원본자료,ગંતવ્ય_ડેટા_સરનામું,순서번호,확인번호,설정비트,વિંડો=struct.unpack_from('!HHIIHH',પૅકેટ_ડેટા,ઑફસેટ_મૂલ્ય)
            પ્રવેશ_મૂલ્ય.update(source=원본자료,destination=ગંતવ્ય_ડેટા_સરનામું,seq=순서번호,ack=확인번호,flags=설정비트&255,window=વિંડો,
                        payload=len(પૅકેટ_ડેટા)-ઑફસેટ_મૂલ્ય-((પૅકેટ_ડેટા[ઑફસેટ_મૂલ્ય+12]>>4)*4))
        자신.ટ્રૅસ_લૉગ.append(પ્રવેશ_મૂલ્ય)
        if len(자신.ટ્રૅસ_લૉગ)>2048: del 자신.ટ્રૅસ_લૉગ[:1024]

    def 직렬전문입력(자신, ડેટા):
        for વર્ણ_કોડ in ડેટા:
            if વર્ણ_કોડ == 192:
                if 자신.직렬전문 and not 자신.ઇન્ટરમિટેંટ_અમાન્ય and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        સરનામું=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(સરનામું)))
                            자신.현재주소=સરનામું
                        except ValueError:
                            pass
                    자신.ટ્રૅસ_પૅકેટ('from_guest',자신.직렬전문)
                    자신.실행틀(ગેટવે_હાર્ડવેર_સરનામું + મશીન_સરનામું + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.ઇન્ટરમિટેંટ_અમાન્ય = False
            elif વર્ણ_કોડ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if વર્ણ_કોડ not in (220, 221): 자신.ઇન્ટરમિટેંટ_અમાન્ય = True
                    વર્ણ_કોડ = 192 if વર્ણ_કોડ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(વર્ણ_કોડ)
                else: 자신.ઇન્ટરમિટેંટ_અમાન્ય = True

    def 이더넷입력(자신, ડેટા):
        자신.ઇથરનેટ += ડેટા
        while len(자신.ઇથરનેટ) >= 4:
            개수 = struct.unpack_from('!I', 자신.ઇથરનેટ)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ઇથરનેટ) < 개수 + 4: return
            실행틀 = bytes(자신.ઇથરનેટ[4:4+개수]); del 자신.ઇથરનેટ[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                સરનામું_રિઝોલ્યૂશન_પૅકેટ = 실행틀[14:42]
                if સરનામું_રિઝોલ્યૂશન_પૅકેટ[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and સરનામું_રિઝોલ્યૂશન_પૅકેટ[24:28] == 자신.현재주소:
                    પ્રતિસાદ = સરનામું_રિઝોલ્યૂશન_પૅકેટ[:6] + b'\x00\x02' + મશીન_સરનામું + 자신.현재주소 + સરનામું_રિઝોલ્યૂશન_પૅકેટ[8:18]
                    자신.실행틀(실행틀[6:12] + મશીન_સરનામું + b'\x08\x06' + પ્રતિસાદ)
            elif 실행틀[12:14] == b'\x08\x00':
                પૅકેટ_ડેટા = 실행틀[14:]
                자신.ટ્રૅસ_પૅકેટ('to_guest',પૅકેટ_ડેટા)
                자신.ઇન્ટરમિટેંટ_બાકી[0] += b'\xc0' + પૅકેટ_ડેટા.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def સાયકલ_મૂલ્ય(자신):
        try:
            while not 자신.થોભો_ઇવેંટ.is_set():
                읽기대상들 = [સ્ટ્રિંગ_ડેટા for 순번, સ્ટ્રિંગ_ડેટા in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [સ્ટ્રિંગ_ડેટા for સ્ટ્રિંગ_ડેટા in 자신.접속자들 if સ્ટ્રિંગ_ડેટા is not None]
                쓰기대상들 = [સ્ટ્રિંગ_ડેટા for 순번, સ્ટ્રિંગ_ડેટા in enumerate(자신.접속자들) if સ્ટ્રિંગ_ડેટા is not None and 자신.ઇન્ટરમિટેંટ_બાકી[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for સ્ટ્રિંગ_ડેટા in 읽을수있음:
                    if સ્ટ્રિંગ_ડેટા in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(સ્ટ્રિંગ_ડેટા); 자신.접속자들[순번], _ = સ્ટ્રિંગ_ડેટા.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(સ્ટ્રિંગ_ડેટા); ડેટા = સ્ટ્રિંગ_ડેટા.recv(16384)
                        if not ડેટા: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ડેટા)
                for સ્ટ્રિંગ_ડેટા in 쓸수있음:
                    순번 = 자신.접속자들.index(સ્ટ્રિંગ_ડેટા)
                    try: 개수 = સ્ટ્રિંગ_ડેટા.send(자신.ઇન્ટરમિટેંટ_બાકી[순번])
                    except BlockingIOError: continue
                    del 자신.ઇન્ટરમિટેંટ_બાકી[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.ઇન્ટરમિટેંટ_બાકી):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.થોભો_ઇવેંટ.is_set(): 자신.ભૂલ = str(보조항목)

    def બંધ_કરો(자신):
        자신.થોભો_ઇવેંટ.set(); 자신.작업가닥.join(timeout=2)
        for સ્ટ્રિંગ_ડેટા in 자신.수신창구들 + 자신.접속자들:
            if સ્ટ્રિંગ_ડેટા is not None: સ્ટ્રિંગ_ડેટા.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *દલીલ_અરે): 자신.બંધ_કરો()
