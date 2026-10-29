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

абсолютный_адрес = bytes.fromhex('525400123456')
шлюз_аппаратный_АДРЕС = bytes.fromhex('52550a000202')
адрес_в_Интернете_ЗНАЧЕН = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class мост_3de4fe3a:
    def __init__(자신, передача_файла_номер_порта=2121, 전달규칙들=(), Сбор=False, гость_АДРЕС=None, адрес_узла='127.0.0.1'):
        if not 1024 <= передача_файла_номер_порта <= 65535 or 50000 <= передача_файла_номер_порта <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.передача_файла_номер_порта = передача_файла_номер_порта
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        гость_АДРЕС = гость_АДРЕС or 자신.ip_config['IP']
        qemu_network(자신.ip_config, гость_АДРЕС)
        АДРЕС=ipaddress.IPv4Address(гость_АДРЕС)
        자신.гость_АДРЕС=str(АДРЕС); 자신.текущий_АДРЕС=АДРЕС.packed
        АДРЕС=ipaddress.IPv4Address(адрес_узла)
        if АДРЕС.is_multicast or str(АДРЕС)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.адрес_узла=str(АДРЕС)
        자신.Сбор = Сбор; 자신.журнал_трассировки = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', передача_файла_номер_порта)} | {('tcp', данные_позиция) for данные_позиция in range(50000,50008)}
        for фильтр_ЗНАЧЕН in 전달규칙들:
            путь_компонент = фильтр_ЗНАЧЕН.split(':')
            if len(путь_компонент) != 3 or путь_компонент[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            сеть_ABI, узел, гость = путь_компонент[0], int(путь_компонент[1]), int(путь_компонент[2])
            if not 1024 <= узел <= 65535 or not 1 <= гость <= 65535 or (сеть_ABI, узел) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + фильтр_ЗНАЧЕН)
            사용중주소.add((сеть_ABI, узел)); 자신.전달규칙들.append((сеть_ABI, узел, гость))
        자신.수신창구들 = []
        for _ in range(2):
            сервер_ЗНАЧЕН = socket.socket()
            сервер_ЗНАЧЕН.bind(('127.0.0.1', 0)); сервер_ЗНАЧЕН.listen(1); сервер_ЗНАЧЕН.setblocking(False)
            자신.수신창구들.append(сервер_ЗНАЧЕН)
        자신.접속자들 = [None, None]
        자신.ИТ_службы_ожидание = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.ИТ_службы_неверный = False
        자신.пауза_Событие = threading.Event(); 자신.ошибка = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.фоноваяЗадача = threading.Thread(target=자신.цикл_ЗНАЧЕН, daemon=True)
        자신.фоноваяЗадача.start()

    def 전달인수(자신):
        직렬접속번호, порт_Ethernet = [строка_данные.getsockname()[1] for строка_данные in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.гость_АДРЕС) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.передача_файла_номер_порта, 자신.гость_АДРЕС)
        for номер_порта in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(номер_порта, 자신.гость_АДРЕС)
        for сеть_ABI, узел, гость in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(сеть_ABI, узел, 자신.гость_АДРЕС, гость)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.адрес_узла+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(порт_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def выполнение_кадр(자신, пакет_данные):
        자신.ИТ_службы_ожидание[1] += struct.pack('!I', len(пакет_данные)) + пакет_данные

    def след_пакет(자신, направление, пакет_данные):
        if not 자신.Сбор or len(пакет_данные)<20: return
        СМЕЩ_ЗНАЧЕН=(пакет_данные[0]&15)*4
        ввод_ЗНАЧЕН={'time':time.monotonic(),'direction':направление,'bytes':len(пакет_данные),'protocol':пакет_данные[9]}
        if пакет_данные[9]==6 and len(пакет_данные)>=СМЕЩ_ЗНАЧЕН+20:
            원본자료,цель_данные_АДРЕС,순서번호,확인번호,настройки_BITS,Окно=struct.unpack_from('!HHIIHH',пакет_данные,СМЕЩ_ЗНАЧЕН)
            ввод_ЗНАЧЕН.update(source=원본자료,destination=цель_данные_АДРЕС,seq=순서번호,ack=확인번호,flags=настройки_BITS&255,window=Окно,
                        payload=len(пакет_данные)-СМЕЩ_ЗНАЧЕН-((пакет_данные[СМЕЩ_ЗНАЧЕН+12]>>4)*4))
        자신.журнал_трассировки.append(ввод_ЗНАЧЕН)
        if len(자신.журнал_трассировки)>2048: del 자신.журнал_трассировки[:1024]

    def SLIP_входные_данные(자신, данные):
        for код_знака in данные:
            if код_знака == 192:
                if 자신.직렬전문 and not 자신.ИТ_службы_неверный and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        АДРЕС=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(АДРЕС)))
                            자신.текущий_АДРЕС=АДРЕС
                        except ValueError:
                            pass
                    자신.след_пакет('from_guest',자신.직렬전문)
                    자신.выполнение_кадр(шлюз_аппаратный_АДРЕС + абсолютный_адрес + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.ИТ_службы_неверный = False
            elif код_знака == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if код_знака not in (220, 221): 자신.ИТ_службы_неверный = True
                    код_знака = 192 if код_знака == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(код_знака)
                else: 자신.ИТ_службы_неверный = True

    def Ethernet_входные_данные(자신, данные):
        자신.Ethernet += данные
        while len(자신.Ethernet) >= 4:
            товар_СЧЁТ = struct.unpack_from('!I', 자신.Ethernet)[0]
            if товар_СЧЁТ > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < товар_СЧЁТ + 4: return
            выполнение_кадр = bytes(자신.Ethernet[4:4+товар_СЧЁТ]); del 자신.Ethernet[:4+товар_СЧЁТ]
            if len(выполнение_кадр) < 14: continue
            if выполнение_кадр[12:14] == b'\x08\x06' and len(выполнение_кадр) >= 42:
                АДРЕС_разрешение_пакет = выполнение_кадр[14:42]
                if АДРЕС_разрешение_пакет[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and АДРЕС_разрешение_пакет[24:28] == 자신.текущий_АДРЕС:
                    ответ_1262b476 = АДРЕС_разрешение_пакет[:6] + b'\x00\x02' + абсолютный_адрес + 자신.текущий_АДРЕС + АДРЕС_разрешение_пакет[8:18]
                    자신.выполнение_кадр(выполнение_кадр[6:12] + абсолютный_адрес + b'\x08\x06' + ответ_1262b476)
            elif выполнение_кадр[12:14] == b'\x08\x00':
                пакет_данные = выполнение_кадр[14:]
                자신.след_пакет('to_guest',пакет_данные)
                자신.ИТ_службы_ожидание[0] += b'\xc0' + пакет_данные.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def цикл_ЗНАЧЕН(자신):
        try:
            while not 자신.пауза_Событие.is_set():
                읽기대상들 = [строка_данные for 순번, строка_данные in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [строка_данные for строка_данные in 자신.접속자들 if строка_данные is not None]
                쓰기대상들 = [строка_данные for 순번, строка_данные in enumerate(자신.접속자들) if строка_данные is not None and 자신.ИТ_службы_ожидание[순번]]
                읽을수있음, записываемый, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for строка_данные in 읽을수있음:
                    if строка_данные in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(строка_данные); 자신.접속자들[순번], _ = строка_данные.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(строка_данные); данные = строка_данные.recv(16384)
                        if not данные: return
                        (자신.SLIP_входные_данные if 순번 == 0 else 자신.Ethernet_входные_данные)(данные)
                for строка_данные in записываемый:
                    순번 = 자신.접속자들.index(строка_данные)
                    try: товар_СЧЁТ = строка_данные.send(자신.ИТ_службы_ожидание[순번])
                    except BlockingIOError: continue
                    del 자신.ИТ_службы_ожидание[순번][:товар_СЧЁТ]
                if any(len(СЕКУНДЫ_ЗНАЧЕН) > 1024 * 1024 for СЕКУНДЫ_ЗНАЧЕН in 자신.ИТ_службы_ожидание):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.пауза_Событие.is_set(): 자신.ошибка = str(보조항목)

    def Закрыть(자신):
        자신.пауза_Событие.set(); 자신.фоноваяЗадача.join(timeout=2)
        for строка_данные in 자신.수신창구들 + 자신.접속자들:
            if строка_данные is not None: строка_данные.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_МАССИВ): 자신.Закрыть()
