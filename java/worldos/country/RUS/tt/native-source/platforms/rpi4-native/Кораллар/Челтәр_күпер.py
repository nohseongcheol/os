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

машина_адрес = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Интернеттагы_адрес_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Челтәр_күпер:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), яздыру=False, кунак_адрес=None, хост_адрес='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        кунак_адрес = кунак_адрес or 자신.ip_config['IP']
        qemu_network(자신.ip_config, кунак_адрес)
        адрес=ipaddress.IPv4Address(кунак_адрес)
        자신.кунак_адрес=str(адрес); 자신.현재주소=адрес.packed
        адрес=ipaddress.IPv4Address(хост_адрес)
        if адрес.is_multicast or str(адрес)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.хост_адрес=str(адрес)
        자신.яздыру = яздыру; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', мәгълүмат_урнаштыру) for мәгълүмат_урнаштыру in range(50000,50008)}
        for сөзгеч_VALUE in 전달규칙들:
            юл_компонент = сөзгеч_VALUE.split(':')
            if len(юл_компонент) != 3 or юл_компонент[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, хост, кунак = юл_компонент[0], int(юл_компонент[1]), int(юл_компонент[2])
            if not 1024 <= хост <= 65535 or not 1 <= кунак <= 65535 or (통신규약, хост) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + сөзгеч_VALUE)
            사용중주소.add((통신규약, хост)); 자신.전달규칙들.append((통신규약, хост, кунак))
        자신.수신창구들 = []
        for _ in range(2):
            сервер_VALUE = socket.socket()
            сервер_VALUE.bind(('127.0.0.1', 0)); сервер_VALUE.listen(1); сервер_VALUE.setblocking(False)
            자신.수신창구들.append(сервер_VALUE)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.туктатып_тору_вакыйга = threading.Event(); 자신.Хата = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Цикл_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_порт = [юл_мәгълүмат.getsockname()[1] for юл_мәгълүмат in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.кунак_адрес) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.кунак_адрес)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.кунак_адрес)
        for 통신규약, хост, кунак in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, хост, 자신.кунак_адрес, кунак)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.хост_адрес+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_порт),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.대기중[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.яздыру or len(꾸러미자료)<20: return
        OFFSET_VALUE=(꾸러미자료[0]&15)*4
        кертү_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=OFFSET_VALUE+20:
            원본자료,күчерү_урыны_мәгълүмат_адрес,순서번호,확인번호,설정비트,тәрәз=struct.unpack_from('!HHIIHH',꾸러미자료,OFFSET_VALUE)
            кертү_VALUE.update(source=원본자료,destination=күчерү_урыны_мәгълүмат_адрес,seq=순서번호,ack=확인번호,flags=설정비트&255,window=тәрәз,
                        payload=len(꾸러미자료)-OFFSET_VALUE-((꾸러미자료[OFFSET_VALUE+12]>>4)*4))
        자신.추적기록.append(кертү_VALUE)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, мәгълүмат):
        for символ_коды in мәгълүмат:
            if символ_коды == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        адрес=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(адрес)))
                            자신.현재주소=адрес
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + машина_адрес + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif символ_коды == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if символ_коды not in (220, 221): 자신.잘못됨 = True
                    символ_коды = 192 if символ_коды == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(символ_коды)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, мәгълүмат):
        자신.Ethernet += мәгълүмат
        while len(자신.Ethernet) >= 4:
            элемент_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if элемент_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < элемент_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+элемент_COUNT]); del 자신.Ethernet[:4+элемент_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                주소찾기전문 = 실행틀[14:42]
                if 주소찾기전문[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 주소찾기전문[24:28] == 자신.현재주소:
                    응답자료 = 주소찾기전문[:6] + b'\x00\x02' + машина_адрес + 자신.현재주소 + 주소찾기전문[8:18]
                    자신.실행틀(실행틀[6:12] + машина_адрес + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                꾸러미자료 = 실행틀[14:]
                자신.전문추적('to_guest',꾸러미자료)
                자신.대기중[0] += b'\xc0' + 꾸러미자료.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Цикл_VALUE(자신):
        try:
            while not 자신.туктатып_тору_вакыйга.is_set():
                읽기대상들 = [юл_мәгълүмат for 순번, юл_мәгълүмат in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [юл_мәгълүмат for юл_мәгълүмат in 자신.접속자들 if юл_мәгълүмат is not None]
                쓰기대상들 = [юл_мәгълүмат for 순번, юл_мәгълүмат in enumerate(자신.접속자들) if юл_мәгълүмат is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for юл_мәгълүмат in 읽을수있음:
                    if юл_мәгълүмат in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(юл_мәгълүмат); 자신.접속자들[순번], _ = юл_мәгълүмат.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(юл_мәгълүмат); мәгълүмат = юл_мәгълүмат.recv(16384)
                        if not мәгълүмат: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(мәгълүмат)
                for юл_мәгълүмат in 쓸수있음:
                    순번 = 자신.접속자들.index(юл_мәгълүмат)
                    try: элемент_COUNT = юл_мәгълүмат.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:элемент_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.туктатып_тору_вакыйга.is_set(): 자신.Хата = str(보조항목)

    def Yap(자신):
        자신.туктатып_тору_вакыйга.set(); 자신.작업가닥.join(timeout=2)
        for юл_мәгълүмат in 자신.수신창구들 + 자신.접속자들:
            if юл_мәгълүмат is not None: юл_мәгълүмат.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_МАССИВ): 자신.Yap()
