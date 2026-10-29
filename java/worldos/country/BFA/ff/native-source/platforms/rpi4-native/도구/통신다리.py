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

기계주소 = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
ñiiɓirde_enternet_njaru = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 통신다리:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), 포착여부=False, 게스트주소=None, njaatigi_ñiiɓirde='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        게스트주소 = 게스트주소 or 자신.ip_config['IP']
        qemu_network(자신.ip_config, 게스트주소)
        ñiiɓirde=ipaddress.IPv4Address(게스트주소)
        자신.게스트주소=str(ñiiɓirde); 자신.현재주소=ñiiɓirde.packed
        ñiiɓirde=ipaddress.IPv4Address(njaatigi_ñiiɓirde)
        if ñiiɓirde.is_multicast or str(ñiiɓirde)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.njaatigi_ñiiɓirde=str(ñiiɓirde)
        자신.포착여부 = 포착여부; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for doosgal_njaru in 전달규칙들:
            laawol_komponal = doosgal_njaru.split(':')
            if len(laawol_komponal) != 3 or laawol_komponal[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, njaatigi, 커널실행 = laawol_komponal[0], int(laawol_komponal[1]), int(laawol_komponal[2])
            if not 1024 <= njaatigi <= 65535 or not 1 <= 커널실행 <= 65535 or (통신규약, njaatigi) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + doosgal_njaru)
            사용중주소.add((통신규약, njaatigi)); 자신.전달규칙들.append((통신규약, njaatigi, 커널실행))
        자신.수신창구들 = []
        for _ in range(2):
            sarworde_njaru = socket.socket()
            sarworde_njaru.bind(('127.0.0.1', 0)); sarworde_njaru.listen(1); sarworde_njaru.setblocking(False)
            자신.수신창구들.append(sarworde_njaru)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.fooftinde_saɗteende = threading.Event(); 자신.juumre = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Yiildu_njaru, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_poor = [ɓoggol_keɓe.getsockname()[1] for ɓoggol_keɓe in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.게스트주소) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.게스트주소)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.게스트주소)
        for 통신규약, njaatigi, 커널실행 in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, njaatigi, 자신.게스트주소, 커널실행)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.njaatigi_ñiiɓirde+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_poor),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.대기중[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.포착여부 or len(꾸러미자료)<20: return
        변위=(꾸러미자료[0]&15)*4
        naatnugol_njaru={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=변위+20:
            원본자료,tiindaare_keɓe_ñiiɓirde,순서번호,확인번호,설정비트,falanteere=struct.unpack_from('!HHIIHH',꾸러미자료,변위)
            naatnugol_njaru.update(source=원본자료,destination=tiindaare_keɓe_ñiiɓirde,seq=순서번호,ack=확인번호,flags=설정비트&255,window=falanteere,
                        payload=len(꾸러미자료)-변위-((꾸러미자료[변위+12]>>4)*4))
        자신.추적기록.append(naatnugol_njaru)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, keɓe):
        for 문자값 in keɓe:
            if 문자값 == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ñiiɓirde=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ñiiɓirde)))
                            자신.현재주소=ñiiɓirde
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + 기계주소 + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif 문자값 == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if 문자값 not in (220, 221): 자신.잘못됨 = True
                    문자값 = 192 if 문자값 == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(문자값)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, keɓe):
        자신.Ethernet += keɓe
        while len(자신.Ethernet) >= 4:
            개수 = struct.unpack_from('!I', 자신.Ethernet)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < 개수 + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+개수]); del 자신.Ethernet[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                주소찾기전문 = 실행틀[14:42]
                if 주소찾기전문[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 주소찾기전문[24:28] == 자신.현재주소:
                    응답자료 = 주소찾기전문[:6] + b'\x00\x02' + 기계주소 + 자신.현재주소 + 주소찾기전문[8:18]
                    자신.실행틀(실행틀[6:12] + 기계주소 + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                꾸러미자료 = 실행틀[14:]
                자신.전문추적('to_guest',꾸러미자료)
                자신.대기중[0] += b'\xc0' + 꾸러미자료.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Yiildu_njaru(자신):
        try:
            while not 자신.fooftinde_saɗteende.is_set():
                읽기대상들 = [ɓoggol_keɓe for 순번, ɓoggol_keɓe in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ɓoggol_keɓe for ɓoggol_keɓe in 자신.접속자들 if ɓoggol_keɓe is not None]
                쓰기대상들 = [ɓoggol_keɓe for 순번, ɓoggol_keɓe in enumerate(자신.접속자들) if ɓoggol_keɓe is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ɓoggol_keɓe in 읽을수있음:
                    if ɓoggol_keɓe in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ɓoggol_keɓe); 자신.접속자들[순번], _ = ɓoggol_keɓe.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ɓoggol_keɓe); keɓe = ɓoggol_keɓe.recv(16384)
                        if not keɓe: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(keɓe)
                for ɓoggol_keɓe in 쓸수있음:
                    순번 = 자신.접속자들.index(ɓoggol_keɓe)
                    try: 개수 = ɓoggol_keɓe.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.fooftinde_saɗteende.is_set(): 자신.juumre = str(보조항목)

    def uddude(자신):
        자신.fooftinde_saɗteende.set(); 자신.작업가닥.join(timeout=2)
        for ɓoggol_keɓe in 자신.수신창구들 + 자신.접속자들:
            if ɓoggol_keɓe is not None: ɓoggol_keɓe.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *인수배열): 자신.uddude()
