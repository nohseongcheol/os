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

реален_адрес = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Интернет_адрес_стойност = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class мост_3de4fe3a:
    def __init__(자신, прехвърляне_на_файл_номер_на_порт=2121, 전달규칙들=(), заснемам=False, гост_адрес=None, хост_адрес='127.0.0.1'):
        if not 1024 <= прехвърляне_на_файл_номер_на_порт <= 65535 or 50000 <= прехвърляне_на_файл_номер_на_порт <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.прехвърляне_на_файл_номер_на_порт = прехвърляне_на_файл_номер_на_порт
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        гост_адрес = гост_адрес or 자신.ip_config['IP']
        qemu_network(자신.ip_config, гост_адрес)
        адрес=ipaddress.IPv4Address(гост_адрес)
        자신.гост_адрес=str(адрес); 자신.в_срок_адрес=адрес.packed
        адрес=ipaddress.IPv4Address(хост_адрес)
        if адрес.is_multicast or str(адрес)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.хост_адрес=str(адрес)
        자신.заснемам = заснемам; 자신.регистрационен_файл_за_проследяванията = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', прехвърляне_на_файл_номер_на_порт)} | {('tcp', данни_позиция) for данни_позиция in range(50000,50008)}
        for филтър_стойност in 전달규칙들:
            път_компонент = филтър_стойност.split(':')
            if len(път_компонент) != 3 or път_компонент[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, хост, гост = път_компонент[0], int(път_компонент[1]), int(път_компонент[2])
            if not 1024 <= хост <= 65535 or not 1 <= гост <= 65535 or (통신규약, хост) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + филтър_стойност)
            사용중주소.add((통신규약, хост)); 자신.전달규칙들.append((통신규약, хост, гост))
        자신.수신창구들 = []
        for _ in range(2):
            сървър_стойност = socket.socket()
            сървър_стойност.bind(('127.0.0.1', 0)); сървър_стойност.listen(1); сървър_стойност.setblocking(False)
            자신.수신창구들.append(сървър_стойност)
        자신.접속자들 = [None, None]
        자신.информационни_технологии_чакащ = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.информационни_технологии_невалиден = False
        자신.Пауза_събитие = threading.Event(); 자신.ГРЕШКА = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Цикъл_стойност, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_порт = [низ_данни.getsockname()[1] for низ_данни in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.гост_адрес) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.прехвърляне_на_файл_номер_на_порт, 자신.гост_адрес)
        for номер_на_порт in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(номер_на_порт, 자신.гост_адрес)
        for 통신규약, хост, гост in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, хост, 자신.гост_адрес, гост)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.хост_адрес+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_порт),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, пакет_данни):
        자신.информационни_технологии_чакащ[1] += struct.pack('!I', len(пакет_данни)) + пакет_данни

    def следа_пакет(자신, 방향, пакет_данни):
        if not 자신.заснемам or len(пакет_данни)<20: return
        Изместване_стойност=(пакет_данни[0]&15)*4
        запис_стойност={'time':time.monotonic(),'direction':방향,'bytes':len(пакет_данни),'protocol':пакет_данни[9]}
        if пакет_данни[9]==6 and len(пакет_данни)>=Изместване_стойност+20:
            원본자료,местоназначение_данни_адрес,순서번호,확인번호,конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим,Прозорец=struct.unpack_from('!HHIIHH',пакет_данни,Изместване_стойност)
            запис_стойност.update(source=원본자료,destination=местоназначение_данни_адрес,seq=순서번호,ack=확인번호,flags=конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим&255,window=Прозорец,
                        payload=len(пакет_данни)-Изместване_стойност-((пакет_данни[Изместване_стойност+12]>>4)*4))
        자신.регистрационен_файл_за_проследяванията.append(запис_стойност)
        if len(자신.регистрационен_файл_за_проследяванията)>2048: del 자신.регистрационен_файл_за_проследяванията[:1024]

    def 직렬전문입력(자신, данни):
        for знаков_код in данни:
            if знаков_код == 192:
                if 자신.직렬전문 and not 자신.информационни_технологии_невалиден and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        адрес=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(адрес)))
                            자신.в_срок_адрес=адрес
                        except ValueError:
                            pass
                    자신.следа_пакет('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + реален_адрес + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.информационни_технологии_невалиден = False
            elif знаков_код == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if знаков_код not in (220, 221): 자신.информационни_технологии_невалиден = True
                    знаков_код = 192 if знаков_код == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(знаков_код)
                else: 자신.информационни_технологии_невалиден = True

    def 이더넷입력(자신, данни):
        자신.이더넷자료 += данни
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                адрес_разделителна_способност_пакет = 실행틀[14:42]
                if адрес_разделителна_способност_пакет[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and адрес_разделителна_способност_пакет[24:28] == 자신.в_срок_адрес:
                    отговор_1262b476 = адрес_разделителна_способност_пакет[:6] + b'\x00\x02' + реален_адрес + 자신.в_срок_адрес + адрес_разделителна_способност_пакет[8:18]
                    자신.실행틀(실행틀[6:12] + реален_адрес + b'\x08\x06' + отговор_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                пакет_данни = 실행틀[14:]
                자신.следа_пакет('to_guest',пакет_данни)
                자신.информационни_технологии_чакащ[0] += b'\xc0' + пакет_данни.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Цикъл_стойност(자신):
        try:
            while not 자신.Пауза_събитие.is_set():
                읽기대상들 = [низ_данни for 순번, низ_данни in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [низ_данни for низ_данни in 자신.접속자들 if низ_данни is not None]
                쓰기대상들 = [низ_данни for 순번, низ_данни in enumerate(자신.접속자들) if низ_данни is not None and 자신.информационни_технологии_чакащ[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for низ_данни in 읽을수있음:
                    if низ_данни in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(низ_данни); 자신.접속자들[순번], _ = низ_данни.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(низ_данни); данни = низ_данни.recv(16384)
                        if not данни: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(данни)
                for низ_данни in 쓸수있음:
                    순번 = 자신.접속자들.index(низ_данни)
                    try: 개수 = низ_данни.send(자신.информационни_технологии_чакащ[순번])
                    except BlockingIOError: continue
                    del 자신.информационни_технологии_чакащ[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.информационни_технологии_чакащ):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Пауза_събитие.is_set(): 자신.ГРЕШКА = str(보조항목)

    def Затворен(자신):
        자신.Пауза_събитие.set(); 자신.작업가닥.join(timeout=2)
        for низ_данни in 자신.수신창구들 + 자신.접속자들:
            if низ_данни is not None: низ_данни.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_масив): 자신.Затворен()
