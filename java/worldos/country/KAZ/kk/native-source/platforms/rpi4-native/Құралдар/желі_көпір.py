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

нақпа_нақ_мекенжай = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Интернет_мекенжайы_мән = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class желі_көпір:
    def __init__(자신, файл_тасымалдау_порт_нөмірі=2121, 전달규칙들=(), түсіру=False, қонақ_мекенжай=None, орналастыру_мекенжай='127.0.0.1'):
        if not 1024 <= файл_тасымалдау_порт_нөмірі <= 65535 or 50000 <= файл_тасымалдау_порт_нөмірі <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.файл_тасымалдау_порт_нөмірі = файл_тасымалдау_порт_нөмірі
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        қонақ_мекенжай = қонақ_мекенжай or 자신.ip_config['IP']
        qemu_network(자신.ip_config, қонақ_мекенжай)
        мекенжай=ipaddress.IPv4Address(қонақ_мекенжай)
        자신.қонақ_мекенжай=str(мекенжай); 자신.ток_мекенжай=мекенжай.packed
        мекенжай=ipaddress.IPv4Address(орналастыру_мекенжай)
        if мекенжай.is_multicast or str(мекенжай)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.орналастыру_мекенжай=str(мекенжай)
        자신.түсіру = түсіру; 자신.трассалау_журналы = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', файл_тасымалдау_порт_нөмірі)} | {('tcp', деректер_лауазым) for деректер_лауазым in range(50000,50008)}
        for ереже_мән in 전달규칙들:
            жол_құрамдас = ереже_мән.split(':')
            if len(жол_құрамдас) != 3 or жол_құрамдас[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, орналастыру, қонақ = жол_құрамдас[0], int(жол_құрамдас[1]), int(жол_құрамдас[2])
            if not 1024 <= орналастыру <= 65535 or not 1 <= қонақ <= 65535 or (통신규약, орналастыру) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ереже_мән)
            사용중주소.add((통신규약, орналастыру)); 자신.전달규칙들.append((통신규약, орналастыру, қонақ))
        자신.수신창구들 = []
        for _ in range(2):
            сервер_мән = socket.socket()
            сервер_мән.bind(('127.0.0.1', 0)); сервер_мән.listen(1); сервер_мән.setblocking(False)
            자신.수신창구들.append(сервер_мән)
        자신.접속자들 = [None, None]
        자신.ақпараттық_жүйелер_Бөгеліс = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.ақпараттық_жүйелер_дұрыс_емес = False
        자신.Тоқтата_тұру_оқиға = threading.Event(); 자신.Қате = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Айналым_мән, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_порты = [жол_деректер.getsockname()[1] for жол_деректер in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.қонақ_мекенжай) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.файл_тасымалдау_порт_нөмірі, 자신.қонақ_мекенжай)
        for порт_нөмірі in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(порт_нөмірі, 자신.қонақ_мекенжай)
        for 통신규약, орналастыру, қонақ in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, орналастыру, 자신.қонақ_мекенжай, қонақ)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.орналастыру_мекенжай+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_порты),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, пакет_деректер):
        자신.ақпараттық_жүйелер_Бөгеліс[1] += struct.pack('!I', len(пакет_деректер)) + пакет_деректер

    def із_пакет(자신, 방향, пакет_деректер):
        if not 자신.түсіру or len(пакет_деректер)<20: return
        жылжыту_мән_450fc799=(пакет_деректер[0]&15)*4
        енгізу_мән={'time':time.monotonic(),'direction':방향,'bytes':len(пакет_деректер),'protocol':пакет_деректер[9]}
        if пакет_деректер[9]==6 and len(пакет_деректер)>=жылжыту_мән_450fc799+20:
            원본자료,тағайындау_деректер_мекенжай,순서번호,확인번호,конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі,Терезе=struct.unpack_from('!HHIIHH',пакет_деректер,жылжыту_мән_450fc799)
            енгізу_мән.update(source=원본자료,destination=тағайындау_деректер_мекенжай,seq=순서번호,ack=확인번호,flags=конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі&255,window=Терезе,
                        payload=len(пакет_деректер)-жылжыту_мән_450fc799-((пакет_деректер[жылжыту_мән_450fc799+12]>>4)*4))
        자신.трассалау_журналы.append(енгізу_мән)
        if len(자신.трассалау_журналы)>2048: del 자신.трассалау_журналы[:1024]

    def 직렬전문입력(자신, деректер):
        for таңба_коды in деректер:
            if таңба_коды == 192:
                if 자신.직렬전문 and not 자신.ақпараттық_жүйелер_дұрыс_емес and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        мекенжай=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(мекенжай)))
                            자신.ток_мекенжай=мекенжай
                        except ValueError:
                            pass
                    자신.із_пакет('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + нақпа_нақ_мекенжай + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.ақпараттық_жүйелер_дұрыс_емес = False
            elif таңба_коды == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if таңба_коды not in (220, 221): 자신.ақпараттық_жүйелер_дұрыс_емес = True
                    таңба_коды = 192 if таңба_коды == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(таңба_коды)
                else: 자신.ақпараттық_жүйелер_дұрыс_емес = True

    def 이더넷입력(자신, деректер):
        자신.이더넷자료 += деректер
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                мекенжай_ажыратымдылық_пакет = 실행틀[14:42]
                if мекенжай_ажыратымдылық_пакет[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and мекенжай_ажыратымдылық_пакет[24:28] == 자신.ток_мекенжай:
                    жауап_1262b476 = мекенжай_ажыратымдылық_пакет[:6] + b'\x00\x02' + нақпа_нақ_мекенжай + 자신.ток_мекенжай + мекенжай_ажыратымдылық_пакет[8:18]
                    자신.실행틀(실행틀[6:12] + нақпа_нақ_мекенжай + b'\x08\x06' + жауап_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                пакет_деректер = 실행틀[14:]
                자신.із_пакет('to_guest',пакет_деректер)
                자신.ақпараттық_жүйелер_Бөгеліс[0] += b'\xc0' + пакет_деректер.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Айналым_мән(자신):
        try:
            while not 자신.Тоқтата_тұру_оқиға.is_set():
                읽기대상들 = [жол_деректер for 순번, жол_деректер in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [жол_деректер for жол_деректер in 자신.접속자들 if жол_деректер is not None]
                쓰기대상들 = [жол_деректер for 순번, жол_деректер in enumerate(자신.접속자들) if жол_деректер is not None and 자신.ақпараттық_жүйелер_Бөгеліс[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for жол_деректер in 읽을수있음:
                    if жол_деректер in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(жол_деректер); 자신.접속자들[순번], _ = жол_деректер.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(жол_деректер); деректер = жол_деректер.recv(16384)
                        if not деректер: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(деректер)
                for жол_деректер in 쓸수있음:
                    순번 = 자신.접속자들.index(жол_деректер)
                    try: 개수 = жол_деректер.send(자신.ақпараттық_жүйелер_Бөгеліс[순번])
                    except BlockingIOError: continue
                    del 자신.ақпараттық_жүйелер_Бөгеліс[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.ақпараттық_жүйелер_Бөгеліс):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Тоқтата_тұру_оқиға.is_set(): 자신.Қате = str(보조항목)

    def Жабу(자신):
        자신.Тоқтата_тұру_оқиға.set(); 자신.작업가닥.join(timeout=2)
        for жол_деректер in 자신.수신창구들 + 자신.접속자들:
            if жол_деректер is not None: жол_деректер.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *аргумент_массив): 자신.Жабу()
