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
ᎠᏏᎳᏕᏫᏒᎢ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏧᎬᏩᎶᏗᏯ = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 통신다리:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), 포착여부=False, ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=None, ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)
        ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ipaddress.IPv4Address(ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)
        자신.ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=str(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ); 자신.현재주소=ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.packed
        ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ipaddress.IPv4Address(ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)
        if ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.is_multicast or str(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=str(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)
        자신.포착여부 = 포착여부; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for ᎬᎫᏍᏗ_ᏧᎬᏩᎶᏗᏯ in 전달규칙들:
            ᎠᏍᏓᏩᏛᏍᏗ_ᏏᏴᏫᎭ_ᏄᏍᏗᏓᏅ = ᎬᎫᏍᏗ_ᏧᎬᏩᎶᏗᏯ.split(':')
            if len(ᎠᏍᏓᏩᏛᏍᏗ_ᏏᏴᏫᎭ_ᏄᏍᏗᏓᏅ) != 3 or ᎠᏍᏓᏩᏛᏍᏗ_ᏏᏴᏫᎭ_ᏄᏍᏗᏓᏅ[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ᎠᏁᏢᏍᎩ, ᎠᏓᏩᏛᎯᏙᎯ = ᎠᏍᏓᏩᏛᏍᏗ_ᏏᏴᏫᎭ_ᏄᏍᏗᏓᏅ[0], int(ᎠᏍᏓᏩᏛᏍᏗ_ᏏᏴᏫᎭ_ᏄᏍᏗᏓᏅ[1]), int(ᎠᏍᏓᏩᏛᏍᏗ_ᏏᏴᏫᎭ_ᏄᏍᏗᏓᏅ[2])
            if not 1024 <= ᎠᏁᏢᏍᎩ <= 65535 or not 1 <= ᎠᏓᏩᏛᎯᏙᎯ <= 65535 or (통신규약, ᎠᏁᏢᏍᎩ) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ᎬᎫᏍᏗ_ᏧᎬᏩᎶᏗᏯ)
            사용중주소.add((통신규약, ᎠᏁᏢᏍᎩ)); 자신.전달규칙들.append((통신규약, ᎠᏁᏢᏍᎩ, ᎠᏓᏩᏛᎯᏙᎯ))
        자신.수신창구들 = []
        for _ in range(2):
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = socket.socket()
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.bind(('127.0.0.1', 0)); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.listen(1); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.setblocking(False)
            자신.수신창구들.append(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.ᎯᏲᎯᏍᏓ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ = threading.Event(); 자신.ᎦᎵᏓᏍᏔᏅ = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.ᎤᏕᏲᏅ_ᏧᎬᏩᎶᏗᏯ, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_ᎫᏓᎸᏗ = [ᎠᏍᏘ_ᎦᏟᏌᏅᎯ.getsockname()[1] for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)
        for 통신규약, ᎠᏁᏢᏍᎩ, ᎠᏓᏩᏛᎯᏙᎯ in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ᎠᏁᏢᏍᎩ, 자신.ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎠᏓᏩᏛᎯᏙᎯ)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_ᎫᏓᎸᏗ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.대기중[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.포착여부 or len(꾸러미자료)<20: return
        변위=(꾸러미자료[0]&15)*4
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=변위+20:
            원본자료,ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,순서번호,확인번호,설정비트,ᏦᎳᏂ=struct.unpack_from('!HHIIHH',꾸러미자료,변위)
            Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.update(source=원본자료,destination=ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,seq=순서번호,ack=확인번호,flags=설정비트&255,window=ᏦᎳᏂ,
                        payload=len(꾸러미자료)-변위-((꾸러미자료[변위+12]>>4)*4))
        자신.추적기록.append(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, ᎦᏟᏌᏅᎯ):
        for 문자값 in ᎦᏟᏌᏅᎯ:
            if 문자값 == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)))
                            자신.현재주소=ᎪᏪᎵ_ᏫᏗᎦᏅᏗ
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

    def 이더넷입력(자신, ᎦᏟᏌᏅᎯ):
        자신.Ethernet += ᎦᏟᏌᏅᎯ
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

    def ᎤᏕᏲᏅ_ᏧᎬᏩᎶᏗᏯ(자신):
        try:
            while not 자신.ᎯᏲᎯᏍᏓ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.is_set():
                읽기대상들 = [ᎠᏍᏘ_ᎦᏟᏌᏅᎯ for 순번, ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ᎠᏍᏘ_ᎦᏟᏌᏅᎯ for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 자신.접속자들 if ᎠᏍᏘ_ᎦᏟᏌᏅᎯ is not None]
                쓰기대상들 = [ᎠᏍᏘ_ᎦᏟᏌᏅᎯ for 순번, ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in enumerate(자신.접속자들) if ᎠᏍᏘ_ᎦᏟᏌᏅᎯ is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 읽을수있음:
                    if ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ); 자신.접속자들[순번], _ = ᎠᏍᏘ_ᎦᏟᏌᏅᎯ.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ); ᎦᏟᏌᏅᎯ = ᎠᏍᏘ_ᎦᏟᏌᏅᎯ.recv(16384)
                        if not ᎦᏟᏌᏅᎯ: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ᎦᏟᏌᏅᎯ)
                for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 쓸수있음:
                    순번 = 자신.접속자들.index(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ)
                    try: 개수 = ᎠᏍᏘ_ᎦᏟᏌᏅᎯ.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ᎯᏲᎯᏍᏓ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.is_set(): 자신.ᎦᎵᏓᏍᏔᏅ = str(보조항목)

    def ᎯᏍᏚᎲᎦ(자신):
        자신.ᎯᏲᎯᏍᏓ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.set(); 자신.작업가닥.join(timeout=2)
        for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in 자신.수신창구들 + 자신.접속자들:
            if ᎠᏍᏘ_ᎦᏟᏌᏅᎯ is not None: ᎠᏍᏘ_ᎦᏟᏌᏅᎯ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ᏗᏓᎦᏘᎸᏍᏗ_array): 자신.ᎯᏍᏚᎲᎦ()
