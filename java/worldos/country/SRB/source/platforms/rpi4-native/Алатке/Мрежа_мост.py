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

рачунар_адреса = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
интернетска_адреса_вриједност = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Мрежа_мост:
    def __init__(자신, фајл_пренос_број_порта=2121, 전달규칙들=(), снимити=False, гост_адреса=None, хост_адреса='127.0.0.1'):
        if not 1024 <= фајл_пренос_број_порта <= 65535 or 50000 <= фајл_пренос_број_порта <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.фајл_пренос_број_порта = фајл_пренос_број_порта
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        гост_адреса = гост_адреса or 자신.ip_config['IP']
        qemu_network(자신.ip_config, гост_адреса)
        адреса=ipaddress.IPv4Address(гост_адреса)
        자신.гост_адреса=str(адреса); 자신.актуелно_адреса=адреса.packed
        адреса=ipaddress.IPv4Address(хост_адреса)
        if адреса.is_multicast or str(адреса)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.хост_адреса=str(адреса)
        자신.снимити = снимити; 자신.траг_евиденција = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', фајл_пренос_број_порта)} | {('tcp', подаци_позиција) for подаци_позиција in range(50000,50008)}
        for филтер_вриједност in 전달규칙들:
            пут_компонента = филтер_вриједност.split(':')
            if len(пут_компонента) != 3 or пут_компонента[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, хост, гост = пут_компонента[0], int(пут_компонента[1]), int(пут_компонента[2])
            if not 1024 <= хост <= 65535 or not 1 <= гост <= 65535 or (통신규약, хост) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + филтер_вриједност)
            사용중주소.add((통신규약, хост)); 자신.전달규칙들.append((통신규약, хост, гост))
        자신.수신창구들 = []
        for _ in range(2):
            сервер_вриједност = socket.socket()
            сервер_вриједност.bind(('127.0.0.1', 0)); сервер_вриједност.listen(1); сервер_вриједност.setblocking(False)
            자신.수신창구들.append(сервер_вриједност)
        자신.접속자들 = [None, None]
        자신.информатичко_одељење_на_чекању = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.информатичко_одељење_неважеће = False
        자신.пауза_догађај = threading.Event(); 자신.ГРЕШКА = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.круг_вриједност, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_порт = [ниска_подаци.getsockname()[1] for ниска_подаци in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.гост_адреса) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.фајл_пренос_број_порта, 자신.гост_адреса)
        for број_порта in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(број_порта, 자신.гост_адреса)
        for 통신규약, хост, гост in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, хост, 자신.гост_адреса, гост)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.хост_адреса+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_порт),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, пакет_подаци):
        자신.информатичко_одељење_на_чекању[1] += struct.pack('!I', len(пакет_подаци)) + пакет_подаци

    def траг_пакет(자신, 방향, пакет_подаци):
        if not 자신.снимити or len(пакет_подаци)<20: return
        Помак_вриједност=(пакет_подаци[0]&15)*4
        унос_вриједност={'time':time.monotonic(),'direction':방향,'bytes':len(пакет_подаци),'protocol':пакет_подаци[9]}
        if пакет_подаци[9]==6 and len(пакет_подаци)>=Помак_вриједност+20:
            원본자료,одредиште_подаци_адреса,순서번호,확인번호,конфигурација_Услуга_интелигентног_преноса_у_позадини,Прозор=struct.unpack_from('!HHIIHH',пакет_подаци,Помак_вриједност)
            унос_вриједност.update(source=원본자료,destination=одредиште_подаци_адреса,seq=순서번호,ack=확인번호,flags=конфигурација_Услуга_интелигентног_преноса_у_позадини&255,window=Прозор,
                        payload=len(пакет_подаци)-Помак_вриједност-((пакет_подаци[Помак_вриједност+12]>>4)*4))
        자신.траг_евиденција.append(унос_вриједност)
        if len(자신.траг_евиденција)>2048: del 자신.траг_евиденција[:1024]

    def 직렬전문입력(자신, подаци):
        for кôд_знака in подаци:
            if кôд_знака == 192:
                if 자신.직렬전문 and not 자신.информатичко_одељење_неважеће and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        адреса=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(адреса)))
                            자신.актуелно_адреса=адреса
                        except ValueError:
                            pass
                    자신.траг_пакет('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + рачунар_адреса + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.информатичко_одељење_неважеће = False
            elif кôд_знака == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if кôд_знака not in (220, 221): 자신.информатичко_одељење_неважеће = True
                    кôд_знака = 192 if кôд_знака == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(кôд_знака)
                else: 자신.информатичко_одељење_неважеће = True

    def 이더넷입력(자신, подаци):
        자신.이더넷자료 += подаци
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                адреса_резолуција_пакет = 실행틀[14:42]
                if адреса_резолуција_пакет[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and адреса_резолуција_пакет[24:28] == 자신.актуелно_адреса:
                    одговор_1262b476 = адреса_резолуција_пакет[:6] + b'\x00\x02' + рачунар_адреса + 자신.актуелно_адреса + адреса_резолуција_пакет[8:18]
                    자신.실행틀(실행틀[6:12] + рачунар_адреса + b'\x08\x06' + одговор_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                пакет_подаци = 실행틀[14:]
                자신.траг_пакет('to_guest',пакет_подаци)
                자신.информатичко_одељење_на_чекању[0] += b'\xc0' + пакет_подаци.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def круг_вриједност(자신):
        try:
            while not 자신.пауза_догађај.is_set():
                읽기대상들 = [ниска_подаци for 순번, ниска_подаци in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ниска_подаци for ниска_подаци in 자신.접속자들 if ниска_подаци is not None]
                쓰기대상들 = [ниска_подаци for 순번, ниска_подаци in enumerate(자신.접속자들) if ниска_подаци is not None and 자신.информатичко_одељење_на_чекању[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ниска_подаци in 읽을수있음:
                    if ниска_подаци in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ниска_подаци); 자신.접속자들[순번], _ = ниска_подаци.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ниска_подаци); подаци = ниска_подаци.recv(16384)
                        if not подаци: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(подаци)
                for ниска_подаци in 쓸수있음:
                    순번 = 자신.접속자들.index(ниска_подаци)
                    try: 개수 = ниска_подаци.send(자신.информатичко_одељење_на_чекању[순번])
                    except BlockingIOError: continue
                    del 자신.информатичко_одељење_на_чекању[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.информатичко_одељење_на_чекању):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.пауза_догађај.is_set(): 자신.ГРЕШКА = str(보조항목)

    def Затворен(자신):
        자신.пауза_догађај.set(); 자신.작업가닥.join(timeout=2)
        for ниска_подаци in 자신.수신창구들 + 자신.접속자들:
            if ниска_подаци is not None: ниска_подаци.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_низ): 자신.Затворен()
