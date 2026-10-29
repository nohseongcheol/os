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

дійсна_адреса = bytes.fromhex('525400123456')
шлюз_обладнання_адреса = bytes.fromhex('52550a000202')
адреса_в_Інтернеті_значення = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class міст_3de4fe3a:
    def __init__(자신, передавання_файлу_номер_порту=2121, 전달규칙들=(), записувати=False, гість_адреса=None, хост_адреса='127.0.0.1'):
        if not 1024 <= передавання_файлу_номер_порту <= 65535 or 50000 <= передавання_файлу_номер_порту <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.передавання_файлу_номер_порту = передавання_файлу_номер_порту
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        гість_адреса = гість_адреса or 자신.ip_config['IP']
        qemu_network(자신.ip_config, гість_адреса)
        Адреса=ipaddress.IPv4Address(гість_адреса)
        자신.гість_адреса=str(Адреса); 자신.чинний_адреса=Адреса.packed
        Адреса=ipaddress.IPv4Address(хост_адреса)
        if Адреса.is_multicast or str(Адреса)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.хост_адреса=str(Адреса)
        자신.записувати = записувати; 자신.журнал_трасування = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', передавання_файлу_номер_порту)} | {('tcp', дані_посада) for дані_посада in range(50000,50008)}
        for лінія_значення in 전달규칙들:
            шлях_компонент = лінія_значення.split(':')
            if len(шлях_компонент) != 3 or шлях_компонент[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, хост, гість = шлях_компонент[0], int(шлях_компонент[1]), int(шлях_компонент[2])
            if not 1024 <= хост <= 65535 or not 1 <= гість <= 65535 or (통신규약, хост) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + лінія_значення)
            사용중주소.add((통신규약, хост)); 자신.전달규칙들.append((통신규약, хост, гість))
        자신.수신창구들 = []
        for _ in range(2):
            сервер_значення = socket.socket()
            сервер_значення.bind(('127.0.0.1', 0)); сервер_значення.listen(1); сервер_значення.setblocking(False)
            자신.수신창구들.append(сервер_значення)
        자신.접속자들 = [None, None]
        자신.ІТ_відділ_необроблений = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.ІТ_відділ_недійсний = False
        자신.Пауза_подія = threading.Event(); 자신.ПОМИЛКА = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.фоноваЗадача = threading.Thread(target=자신.цикл_значення, daemon=True)
        자신.фоноваЗадача.start()

    def 전달인수(자신):
        직렬접속번호, порт_Ethernet = [рядок_дані.getsockname()[1] for рядок_дані in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.гість_адреса) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.передавання_файлу_номер_порту, 자신.гість_адреса)
        for номер_порту in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(номер_порту, 자신.гість_адреса)
        for 통신규약, хост, гість in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, хост, 자신.гість_адреса, гість)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.хост_адреса+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(порт_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, пакет_дані):
        자신.ІТ_відділ_необроблений[1] += struct.pack('!I', len(пакет_дані)) + пакет_дані

    def слід_пакет(자신, 방향, пакет_дані):
        if not 자신.записувати or len(пакет_дані)<20: return
        Зміщена_копія_значення=(пакет_дані[0]&15)*4
        запис_значення_962f286b={'time':time.monotonic(),'direction':방향,'bytes':len(пакет_дані),'protocol':пакет_дані[9]}
        if пакет_дані[9]==6 and len(пакет_дані)>=Зміщена_копія_значення+20:
            원본자료,місце_дані_адреса,순서번호,확인번호,конфігурація_служба_фонового_передавання_файлів,Вікно=struct.unpack_from('!HHIIHH',пакет_дані,Зміщена_копія_значення)
            запис_значення_962f286b.update(source=원본자료,destination=місце_дані_адреса,seq=순서번호,ack=확인번호,flags=конфігурація_служба_фонового_передавання_файлів&255,window=Вікно,
                        payload=len(пакет_дані)-Зміщена_копія_значення-((пакет_дані[Зміщена_копія_значення+12]>>4)*4))
        자신.журнал_трасування.append(запис_значення_962f286b)
        if len(자신.журнал_трасування)>2048: del 자신.журнал_трасування[:1024]

    def 직렬전문입력(자신, дані):
        for код_символу in дані:
            if код_символу == 192:
                if 자신.직렬전문 and not 자신.ІТ_відділ_недійсний and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        Адреса=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(Адреса)))
                            자신.чинний_адреса=Адреса
                        except ValueError:
                            pass
                    자신.слід_пакет('from_guest',자신.직렬전문)
                    자신.실행틀(шлюз_обладнання_адреса + дійсна_адреса + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.ІТ_відділ_недійсний = False
            elif код_символу == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if код_символу not in (220, 221): 자신.ІТ_відділ_недійсний = True
                    код_символу = 192 if код_символу == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(код_символу)
                else: 자신.ІТ_відділ_недійсний = True

    def 이더넷입력(자신, дані):
        자신.이더넷자료 += дані
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                адреса_роздільна_здатність_пакет = 실행틀[14:42]
                if адреса_роздільна_здатність_пакет[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and адреса_роздільна_здатність_пакет[24:28] == 자신.чинний_адреса:
                    відгук = адреса_роздільна_здатність_пакет[:6] + b'\x00\x02' + дійсна_адреса + 자신.чинний_адреса + адреса_роздільна_здатність_пакет[8:18]
                    자신.실행틀(실행틀[6:12] + дійсна_адреса + b'\x08\x06' + відгук)
            elif 실행틀[12:14] == b'\x08\x00':
                пакет_дані = 실행틀[14:]
                자신.слід_пакет('to_guest',пакет_дані)
                자신.ІТ_відділ_необроблений[0] += b'\xc0' + пакет_дані.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def цикл_значення(자신):
        try:
            while not 자신.Пауза_подія.is_set():
                읽기대상들 = [рядок_дані for 순번, рядок_дані in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [рядок_дані for рядок_дані in 자신.접속자들 if рядок_дані is not None]
                쓰기대상들 = [рядок_дані for 순번, рядок_дані in enumerate(자신.접속자들) if рядок_дані is not None and 자신.ІТ_відділ_необроблений[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for рядок_дані in 읽을수있음:
                    if рядок_дані in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(рядок_дані); 자신.접속자들[순번], _ = рядок_дані.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(рядок_дані); дані = рядок_дані.recv(16384)
                        if not дані: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(дані)
                for рядок_дані in 쓸수있음:
                    순번 = 자신.접속자들.index(рядок_дані)
                    try: 개수 = рядок_дані.send(자신.ІТ_відділ_необроблений[순번])
                    except BlockingIOError: continue
                    del 자신.ІТ_відділ_необроблений[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.ІТ_відділ_необроблений):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Пауза_подія.is_set(): 자신.ПОМИЛКА = str(보조항목)

    def Закрити(자신):
        자신.Пауза_подія.set(); 자신.фоноваЗадача.join(timeout=2)
        for рядок_дані in 자신.수신창구들 + 자신.접속자들:
            if рядок_дані is not None: рядок_дані.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_масив): 자신.Закрити()
