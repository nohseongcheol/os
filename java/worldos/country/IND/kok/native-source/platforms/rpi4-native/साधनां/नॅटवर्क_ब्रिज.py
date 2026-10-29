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

यंत्र_नामो = bytes.fromhex('525400123456')
गेटवे_हार्डवॅर_नामो = bytes.fromhex('52550a000202')
माजाळ्याचो_नामो_मोल = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class नॅटवर्क_ब्रिज:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), कॅप्चर=False, सोयरो_नामो=None, येजमान_नामो='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        सोयरो_नामो = सोयरो_नामो or 자신.ip_config['IP']
        qemu_network(자신.ip_config, सोयरो_नामो)
        नामो=ipaddress.IPv4Address(सोयरो_नामो)
        자신.सोयरो_नामो=str(नामो); 자신.현재주소=नामो.packed
        नामो=ipaddress.IPv4Address(येजमान_नामो)
        if नामो.is_multicast or str(नामो)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.येजमान_नामो=str(नामो)
        자신.कॅप्चर = कॅप्चर; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', डेटा_स्थिती) for डेटा_स्थिती in range(50000,50008)}
        for नेम_मोल in 전달규칙들:
            पाथ_घटक = नेम_मोल.split(':')
            if len(पाथ_घटक) != 3 or पाथ_घटक[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, येजमान, सोयरो = पाथ_घटक[0], int(पाथ_घटक[1]), int(पाथ_घटक[2])
            if not 1024 <= येजमान <= 65535 or not 1 <= सोयरो <= 65535 or (통신규약, येजमान) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + नेम_मोल)
            사용중주소.add((통신규약, येजमान)); 자신.전달규칙들.append((통신규약, येजमान, सोयरो))
        자신.수신창구들 = []
        for _ in range(2):
            सर्वर_मोल = socket.socket()
            सर्वर_मोल.bind(('127.0.0.1', 0)); सर्वर_मोल.listen(1); सर्वर_मोल.setblocking(False)
            자신.수신창구들.append(सर्वर_मोल)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.इथरनॅट = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.थांबणी_प्रसंग = threading.Event(); 자신.चूक = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.सायकल_मोल, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, इथरनॅट_पोर्ट = [स्ट्रिंग_डेटा.getsockname()[1] for स्ट्रिंग_डेटा in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.सोयरो_नामो) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.सोयरो_नामो)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.सोयरो_नामो)
        for 통신규약, येजमान, सोयरो in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, येजमान, 자신.सोयरो_नामो, सोयरो)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.येजमान_नामो+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(इथरनॅट_पोर्ट),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, पॅकेट_डेटा):
        자신.대기중[1] += struct.pack('!I', len(पॅकेट_डेटा)) + पॅकेट_डेटा

    def 전문추적(자신, 방향, पॅकेट_डेटा):
        if not 자신.कॅप्चर or len(पॅकेट_डेटा)<20: return
        ऑफसॅट_मोल=(पॅकेट_डेटा[0]&15)*4
        प्रवेश_मोल={'time':time.monotonic(),'direction':방향,'bytes':len(पॅकेट_डेटा),'protocol':पॅकेट_डेटा[9]}
        if पॅकेट_डेटा[9]==6 and len(पॅकेट_डेटा)>=ऑफसॅट_मोल+20:
            원본자료,नियुक्त_स्थान_डेटा_नामो,순서번호,확인번호,설정비트,विंडो=struct.unpack_from('!HHIIHH',पॅकेट_डेटा,ऑफसॅट_मोल)
            प्रवेश_मोल.update(source=원본자료,destination=नियुक्त_स्थान_डेटा_नामो,seq=순서번호,ack=확인번호,flags=설정비트&255,window=विंडो,
                        payload=len(पॅकेट_डेटा)-ऑफसॅट_मोल-((पॅकेट_डेटा[ऑफसॅट_मोल+12]>>4)*4))
        자신.추적기록.append(प्रवेश_मोल)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, डेटा):
        for वर्ण_कोड in डेटा:
            if वर्ण_कोड == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        नामो=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(नामो)))
                            자신.현재주소=नामो
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(गेटवे_हार्डवॅर_नामो + यंत्र_नामो + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif वर्ण_कोड == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if वर्ण_कोड not in (220, 221): 자신.잘못됨 = True
                    वर्ण_कोड = 192 if वर्ण_कोड == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(वर्ण_कोड)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, डेटा):
        자신.इथरनॅट += डेटा
        while len(자신.इथरनॅट) >= 4:
            आयटम_COUNT = struct.unpack_from('!I', 자신.इथरनॅट)[0]
            if आयटम_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.इथरनॅट) < आयटम_COUNT + 4: return
            실행틀 = bytes(자신.इथरनॅट[4:4+आयटम_COUNT]); del 자신.इथरनॅट[:4+आयटम_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                नामो_रिजोल्युशन_पॅकेट = 실행틀[14:42]
                if नामो_रिजोल्युशन_पॅकेट[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and नामो_रिजोल्युशन_पॅकेट[24:28] == 자신.현재주소:
                    응답자료 = नामो_रिजोल्युशन_पॅकेट[:6] + b'\x00\x02' + यंत्र_नामो + 자신.현재주소 + नामो_रिजोल्युशन_पॅकेट[8:18]
                    자신.실행틀(실행틀[6:12] + यंत्र_नामो + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                पॅकेट_डेटा = 실행틀[14:]
                자신.전문추적('to_guest',पॅकेट_डेटा)
                자신.대기중[0] += b'\xc0' + पॅकेट_डेटा.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def सायकल_मोल(자신):
        try:
            while not 자신.थांबणी_प्रसंग.is_set():
                읽기대상들 = [स्ट्रिंग_डेटा for 순번, स्ट्रिंग_डेटा in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [स्ट्रिंग_डेटा for स्ट्रिंग_डेटा in 자신.접속자들 if स्ट्रिंग_डेटा is not None]
                쓰기대상들 = [स्ट्रिंग_डेटा for 순번, स्ट्रिंग_डेटा in enumerate(자신.접속자들) if स्ट्रिंग_डेटा is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for स्ट्रिंग_डेटा in 읽을수있음:
                    if स्ट्रिंग_डेटा in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(स्ट्रिंग_डेटा); 자신.접속자들[순번], _ = स्ट्रिंग_डेटा.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(स्ट्रिंग_डेटा); डेटा = स्ट्रिंग_डेटा.recv(16384)
                        if not डेटा: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(डेटा)
                for स्ट्रिंग_डेटा in 쓸수있음:
                    순번 = 자신.접속자들.index(स्ट्रिंग_डेटा)
                    try: आयटम_COUNT = स्ट्रिंग_डेटा.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:आयटम_COUNT]
                if any(len(SECOND_मोल) > 1024 * 1024 for SECOND_मोल in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.थांबणी_प्रसंग.is_set(): 자신.चूक = str(보조항목)

    def शेवट(자신):
        자신.थांबणी_प्रसंग.set(); 자신.작업가닥.join(timeout=2)
        for स्ट्रिंग_डेटा in 자신.수신창구들 + 자신.접속자들:
            if स्ट्रिंग_डेटा is not None: स्ट्रिंग_डेटा.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *युक्तीवाद_क्रम): 자신.शेवट()
