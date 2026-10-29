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

камп_ютар_адрас = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
інтэрнэт_адрас_значэнне = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Сетка_мост:
    def __init__(자신, файл_перанос_нумар_порта=2121, 전달규칙들=(), зняць=False, госць_адрас=None, вузел_адрас='127.0.0.1'):
        if not 1024 <= файл_перанос_нумар_порта <= 65535 or 50000 <= файл_перанос_нумар_порта <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.файл_перанос_нумар_порта = файл_перанос_нумар_порта
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        госць_адрас = госць_адрас or 자신.ip_config['IP']
        qemu_network(자신.ip_config, госць_адрас)
        адрас=ipaddress.IPv4Address(госць_адрас)
        자신.госць_адрас=str(адрас); 자신.현재주소=адрас.packed
        адрас=ipaddress.IPv4Address(вузел_адрас)
        if адрас.is_multicast or str(адрас)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.вузел_адрас=str(адрас)
        자신.зняць = зняць; 자신.след_журнал = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', файл_перанос_нумар_порта)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for фільтр_значэнне in 전달규칙들:
            шлях_кампанент = фільтр_значэнне.split(':')
            if len(шлях_кампанент) != 3 or шлях_кампанент[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, вузел, госць = шлях_кампанент[0], int(шлях_кампанент[1]), int(шлях_кампанент[2])
            if not 1024 <= вузел <= 65535 or not 1 <= госць <= 65535 or (통신규약, вузел) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + фільтр_значэнне)
            사용중주소.add((통신규약, вузел)); 자신.전달규칙들.append((통신규약, вузел, госць))
        자신.수신창구들 = []
        for _ in range(2):
            сервер_значэнне = socket.socket()
            сервер_значэнне.bind(('127.0.0.1', 0)); сервер_значэнне.listen(1); сервер_значэнне.setblocking(False)
            자신.수신창구들.append(сервер_значэнне)
        자신.접속자들 = [None, None]
        자신.аддзел_інфармацыйных_тэхналогій_чаканне = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.аддзел_інфармацыйных_тэхналогій_памылковы = False
        자신.прыпыніць_падзея = threading.Event(); 자신.ПАМЫЛКА = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Цыклічная_значэнне, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, 이더넷접속번호 = [радок_дадзеныя.getsockname()[1] for радок_дадзеныя in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.госць_адрас) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.файл_перанос_нумар_порта, 자신.госць_адрас)
        for нумар_порта in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(нумар_порта, 자신.госць_адрас)
        for 통신규약, вузел, госць in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, вузел, 자신.госць_адрас, госць)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.вузел_адрас+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(이더넷접속번호),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, пакет_дадзеныя):
        자신.аддзел_інфармацыйных_тэхналогій_чаканне[1] += struct.pack('!I', len(пакет_дадзеныя)) + пакет_дадзеныя

    def след_пакет(자신, 방향, пакет_дадзеныя):
        if not 자신.зняць or len(пакет_дадзеныя)<20: return
        Зрух_значэнне=(пакет_дадзеныя[0]&15)*4
        увядзенне_значэнне={'time':time.monotonic(),'direction':방향,'bytes':len(пакет_дадзеныя),'protocol':пакет_дадзеныя[9]}
        if пакет_дадзеныя[9]==6 and len(пакет_дадзеныя)>=Зрух_значэнне+20:
            원본자료,прызначэнне_дадзеныя_адрас,순서번호,확인번호,канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў,акно=struct.unpack_from('!HHIIHH',пакет_дадзеныя,Зрух_значэнне)
            увядзенне_значэнне.update(source=원본자료,destination=прызначэнне_дадзеныя_адрас,seq=순서번호,ack=확인번호,flags=канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў&255,window=акно,
                        payload=len(пакет_дадзеныя)-Зрух_значэнне-((пакет_дадзеныя[Зрух_значэнне+12]>>4)*4))
        자신.след_журнал.append(увядзенне_значэнне)
        if len(자신.след_журнал)>2048: del 자신.след_журнал[:1024]

    def 직렬전문입력(자신, дадзеныя):
        for код_сімвала in дадзеныя:
            if код_сімвала == 192:
                if 자신.직렬전문 and not 자신.аддзел_інфармацыйных_тэхналогій_памылковы and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        адрас=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(адрас)))
                            자신.현재주소=адрас
                        except ValueError:
                            pass
                    자신.след_пакет('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + камп_ютар_адрас + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.аддзел_інфармацыйных_тэхналогій_памылковы = False
            elif код_сімвала == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if код_сімвала not in (220, 221): 자신.аддзел_інфармацыйных_тэхналогій_памылковы = True
                    код_сімвала = 192 if код_сімвала == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(код_сімвала)
                else: 자신.аддзел_інфармацыйных_тэхналогій_памылковы = True

    def 이더넷입력(자신, дадзеныя):
        자신.이더넷자료 += дадзеныя
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                адрас_разрознасць_пакет = 실행틀[14:42]
                if адрас_разрознасць_пакет[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and адрас_разрознасць_пакет[24:28] == 자신.현재주소:
                    응답자료 = адрас_разрознасць_пакет[:6] + b'\x00\x02' + камп_ютар_адрас + 자신.현재주소 + адрас_разрознасць_пакет[8:18]
                    자신.실행틀(실행틀[6:12] + камп_ютар_адрас + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                пакет_дадзеныя = 실행틀[14:]
                자신.след_пакет('to_guest',пакет_дадзеныя)
                자신.аддзел_інфармацыйных_тэхналогій_чаканне[0] += b'\xc0' + пакет_дадзеныя.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Цыклічная_значэнне(자신):
        try:
            while not 자신.прыпыніць_падзея.is_set():
                읽기대상들 = [радок_дадзеныя for 순번, радок_дадзеныя in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [радок_дадзеныя for радок_дадзеныя in 자신.접속자들 if радок_дадзеныя is not None]
                쓰기대상들 = [радок_дадзеныя for 순번, радок_дадзеныя in enumerate(자신.접속자들) if радок_дадзеныя is not None and 자신.аддзел_інфармацыйных_тэхналогій_чаканне[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for радок_дадзеныя in 읽을수있음:
                    if радок_дадзеныя in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(радок_дадзеныя); 자신.접속자들[순번], _ = радок_дадзеныя.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(радок_дадзеныя); дадзеныя = радок_дадзеныя.recv(16384)
                        if not дадзеныя: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(дадзеныя)
                for радок_дадзеныя in 쓸수있음:
                    순번 = 자신.접속자들.index(радок_дадзеныя)
                    try: 개수 = радок_дадзеныя.send(자신.аддзел_інфармацыйных_тэхналогій_чаканне[순번])
                    except BlockingIOError: continue
                    del 자신.аддзел_інфармацыйных_тэхналогій_чаканне[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.аддзел_інфармацыйных_тэхналогій_чаканне):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.прыпыніць_падзея.is_set(): 자신.ПАМЫЛКА = str(보조항목)

    def Закрыць(자신):
        자신.прыпыніць_падзея.set(); 자신.작업가닥.join(timeout=2)
        for радок_дадзеныя in 자신.수신창구들 + 자신.접속자들:
            if радок_дадзеныя is not None: радок_дадзеныя.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_масіў): 자신.Закрыць()
