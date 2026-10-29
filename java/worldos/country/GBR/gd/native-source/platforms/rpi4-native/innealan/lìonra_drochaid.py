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

inneal_ADDRESS = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Seòladh_eadar_lìn_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class lìonra_drochaid:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), glac=False, aoigh_ADDRESS=None, òstair_ADDRESS='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        aoigh_ADDRESS = aoigh_ADDRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, aoigh_ADDRESS)
        ADDRESS=ipaddress.IPv4Address(aoigh_ADDRESS)
        자신.aoigh_ADDRESS=str(ADDRESS); 자신.현재주소=ADDRESS.packed
        ADDRESS=ipaddress.IPv4Address(òstair_ADDRESS)
        if ADDRESS.is_multicast or str(ADDRESS)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.òstair_ADDRESS=str(ADDRESS)
        자신.glac = glac; 자신.treus_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', dàta_suidhich) for dàta_suidhich in range(50000,50008)}
        for criathrag_VALUE in 전달규칙들:
            slighe_co_phàirt = criathrag_VALUE.split(':')
            if len(slighe_co_phàirt) != 3 or slighe_co_phàirt[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, òstair, aoigh = slighe_co_phàirt[0], int(slighe_co_phàirt[1]), int(slighe_co_phàirt[2])
            if not 1024 <= òstair <= 65535 or not 1 <= aoigh <= 65535 or (통신규약, òstair) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + criathrag_VALUE)
            사용중주소.add((통신규약, òstair)); 자신.전달규칙들.append((통신규약, òstair, aoigh))
        자신.수신창구들 = []
        for _ in range(2):
            frithealaiche_VALUE = socket.socket()
            frithealaiche_VALUE.bind(('127.0.0.1', 0)); frithealaiche_VALUE.listen(1); frithealaiche_VALUE.setblocking(False)
            자신.수신창구들.append(frithealaiche_VALUE)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.cuir_na_stad_tachartas = threading.Event(); 자신.Mearachd = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.cuairt_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_port = [sreang_dàta.getsockname()[1] for sreang_dàta in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.aoigh_ADDRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.aoigh_ADDRESS)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.aoigh_ADDRESS)
        for 통신규약, òstair, aoigh in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, òstair, 자신.aoigh_ADDRESS, aoigh)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.òstair_ADDRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.대기중[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.glac or len(꾸러미자료)<20: return
        OFFSET_VALUE=(꾸러미자료[0]&15)*4
        cur_a_steach_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=OFFSET_VALUE+20:
            원본자료,ceann_uidhe_dàta_ADDRESS,순서번호,확인번호,설정비트,uinneag=struct.unpack_from('!HHIIHH',꾸러미자료,OFFSET_VALUE)
            cur_a_steach_VALUE.update(source=원본자료,destination=ceann_uidhe_dàta_ADDRESS,seq=순서번호,ack=확인번호,flags=설정비트&255,window=uinneag,
                        payload=len(꾸러미자료)-OFFSET_VALUE-((꾸러미자료[OFFSET_VALUE+12]>>4)*4))
        자신.treus_LOG.append(cur_a_steach_VALUE)
        if len(자신.treus_LOG)>2048: del 자신.treus_LOG[:1024]

    def 직렬전문입력(자신, dàta):
        for còd_a_charactair in dàta:
            if còd_a_charactair == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADDRESS=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADDRESS)))
                            자신.현재주소=ADDRESS
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + inneal_ADDRESS + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif còd_a_charactair == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if còd_a_charactair not in (220, 221): 자신.잘못됨 = True
                    còd_a_charactair = 192 if còd_a_charactair == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(còd_a_charactair)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, dàta):
        자신.Ethernet += dàta
        while len(자신.Ethernet) >= 4:
            nì_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if nì_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < nì_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+nì_COUNT]); del 자신.Ethernet[:4+nì_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                주소찾기전문 = 실행틀[14:42]
                if 주소찾기전문[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 주소찾기전문[24:28] == 자신.현재주소:
                    응답자료 = 주소찾기전문[:6] + b'\x00\x02' + inneal_ADDRESS + 자신.현재주소 + 주소찾기전문[8:18]
                    자신.실행틀(실행틀[6:12] + inneal_ADDRESS + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                꾸러미자료 = 실행틀[14:]
                자신.전문추적('to_guest',꾸러미자료)
                자신.대기중[0] += b'\xc0' + 꾸러미자료.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def cuairt_VALUE(자신):
        try:
            while not 자신.cuir_na_stad_tachartas.is_set():
                읽기대상들 = [sreang_dàta for 순번, sreang_dàta in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [sreang_dàta for sreang_dàta in 자신.접속자들 if sreang_dàta is not None]
                쓰기대상들 = [sreang_dàta for 순번, sreang_dàta in enumerate(자신.접속자들) if sreang_dàta is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for sreang_dàta in 읽을수있음:
                    if sreang_dàta in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(sreang_dàta); 자신.접속자들[순번], _ = sreang_dàta.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(sreang_dàta); dàta = sreang_dàta.recv(16384)
                        if not dàta: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(dàta)
                for sreang_dàta in 쓸수있음:
                    순번 = 자신.접속자들.index(sreang_dàta)
                    try: nì_COUNT = sreang_dàta.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:nì_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.cuir_na_stad_tachartas.is_set(): 자신.Mearachd = str(보조항목)

    def dùin(자신):
        자신.cuir_na_stad_tachartas.set(); 자신.작업가닥.join(timeout=2)
        for sreang_dàta in 자신.수신창구들 + 자신.접속자들:
            if sreang_dàta is not None: sreang_dàta.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argamaid_ARRAY): 자신.dùin()
