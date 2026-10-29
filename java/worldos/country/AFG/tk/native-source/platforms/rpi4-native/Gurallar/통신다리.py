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

kompýuter_salgy = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Internet_salgy_baha = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 통신다리:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), düşüriş=False, 게스트주소=None, esasy_salgy='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        게스트주소 = 게스트주소 or 자신.ip_config['IP']
        qemu_network(자신.ip_config, 게스트주소)
        salgy=ipaddress.IPv4Address(게스트주소)
        자신.게스트주소=str(salgy); 자신.현재주소=salgy.packed
        salgy=ipaddress.IPv4Address(esasy_salgy)
        if salgy.is_multicast or str(salgy)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.esasy_salgy=str(salgy)
        자신.düşüriş = düşüriş; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for kada_baha in 전달규칙들:
            ýol_komponent = kada_baha.split(':')
            if len(ýol_komponent) != 3 or ýol_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, esasy, 커널실행 = ýol_komponent[0], int(ýol_komponent[1]), int(ýol_komponent[2])
            if not 1024 <= esasy <= 65535 or not 1 <= 커널실행 <= 65535 or (통신규약, esasy) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + kada_baha)
            사용중주소.add((통신규약, esasy)); 자신.전달규칙들.append((통신규약, esasy, 커널실행))
        자신.수신창구들 = []
        for _ in range(2):
            serwer_baha = socket.socket()
            serwer_baha.bind(('127.0.0.1', 0)); serwer_baha.listen(1); serwer_baha.setblocking(False)
            자신.수신창구들.append(serwer_baha)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.sägin_waka = threading.Event(); 자신.Hata = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Gaýtalanyş_baha, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_port = [setir_maglumat.getsockname()[1] for setir_maglumat in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.게스트주소) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.게스트주소)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.게스트주소)
        for 통신규약, esasy, 커널실행 in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, esasy, 자신.게스트주소, 커널실행)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.esasy_salgy+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.대기중[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.düşüriş or len(꾸러미자료)<20: return
        Süýşüriş_baha=(꾸러미자료[0]&15)*4
        girizmeklik_baha={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=Süýşüriş_baha+20:
            원본자료,barylmaly_ýer_maglumat_salgy,순서번호,확인번호,설정비트,penjire=struct.unpack_from('!HHIIHH',꾸러미자료,Süýşüriş_baha)
            girizmeklik_baha.update(source=원본자료,destination=barylmaly_ýer_maglumat_salgy,seq=순서번호,ack=확인번호,flags=설정비트&255,window=penjire,
                        payload=len(꾸러미자료)-Süýşüriş_baha-((꾸러미자료[Süýşüriş_baha+12]>>4)*4))
        자신.추적기록.append(girizmeklik_baha)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, maglumat):
        for nyşanyň_kody in maglumat:
            if nyşanyň_kody == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        salgy=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(salgy)))
                            자신.현재주소=salgy
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + kompýuter_salgy + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif nyşanyň_kody == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if nyşanyň_kody not in (220, 221): 자신.잘못됨 = True
                    nyşanyň_kody = 192 if nyşanyň_kody == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(nyşanyň_kody)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, maglumat):
        자신.Ethernet += maglumat
        while len(자신.Ethernet) >= 4:
            개수 = struct.unpack_from('!I', 자신.Ethernet)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < 개수 + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+개수]); del 자신.Ethernet[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                주소찾기전문 = 실행틀[14:42]
                if 주소찾기전문[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 주소찾기전문[24:28] == 자신.현재주소:
                    응답자료 = 주소찾기전문[:6] + b'\x00\x02' + kompýuter_salgy + 자신.현재주소 + 주소찾기전문[8:18]
                    자신.실행틀(실행틀[6:12] + kompýuter_salgy + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                꾸러미자료 = 실행틀[14:]
                자신.전문추적('to_guest',꾸러미자료)
                자신.대기중[0] += b'\xc0' + 꾸러미자료.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Gaýtalanyş_baha(자신):
        try:
            while not 자신.sägin_waka.is_set():
                읽기대상들 = [setir_maglumat for 순번, setir_maglumat in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [setir_maglumat for setir_maglumat in 자신.접속자들 if setir_maglumat is not None]
                쓰기대상들 = [setir_maglumat for 순번, setir_maglumat in enumerate(자신.접속자들) if setir_maglumat is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for setir_maglumat in 읽을수있음:
                    if setir_maglumat in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(setir_maglumat); 자신.접속자들[순번], _ = setir_maglumat.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(setir_maglumat); maglumat = setir_maglumat.recv(16384)
                        if not maglumat: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(maglumat)
                for setir_maglumat in 쓸수있음:
                    순번 = 자신.접속자들.index(setir_maglumat)
                    try: 개수 = setir_maglumat.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.sägin_waka.is_set(): 자신.Hata = str(보조항목)

    def Ýap(자신):
        자신.sägin_waka.set(); 자신.작업가닥.join(timeout=2)
        for setir_maglumat in 자신.수신창구들 + 자신.접속자들:
            if setir_maglumat is not None: setir_maglumat.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_ARRAY): 자신.Ýap()
