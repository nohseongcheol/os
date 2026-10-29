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

ਮਸ਼ੀਨ_ਪਤਾ = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
ਇੰਟਰਨੈਟ_ਪਤਾ_ਕੀਮਤ = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class ਨੈਟਵਰਕ_ਬਰਿਜ:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), ਪਕੜਨਾ=False, ਗੈਸਟ_ਪਤਾ=None, ਹੋਸਟ_ਪਤਾ='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ਗੈਸਟ_ਪਤਾ = ਗੈਸਟ_ਪਤਾ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ਗੈਸਟ_ਪਤਾ)
        ਪਤਾ=ipaddress.IPv4Address(ਗੈਸਟ_ਪਤਾ)
        자신.ਗੈਸਟ_ਪਤਾ=str(ਪਤਾ); 자신.현재주소=ਪਤਾ.packed
        ਪਤਾ=ipaddress.IPv4Address(ਹੋਸਟ_ਪਤਾ)
        if ਪਤਾ.is_multicast or str(ਪਤਾ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ਹੋਸਟ_ਪਤਾ=str(ਪਤਾ)
        자신.ਪਕੜਨਾ = ਪਕੜਨਾ; 자신.ਟਰੇਸ_ਲੌਗ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ) for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in range(50000,50008)}
        for ਨਿਯਮ_ਕੀਮਤ in 전달규칙들:
            ਰਸਤਾ_ਅੰਗ = ਨਿਯਮ_ਕੀਮਤ.split(':')
            if len(ਰਸਤਾ_ਅੰਗ) != 3 or ਰਸਤਾ_ਅੰਗ[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ਹੋਸਟ, ਗੈਸਟ = ਰਸਤਾ_ਅੰਗ[0], int(ਰਸਤਾ_ਅੰਗ[1]), int(ਰਸਤਾ_ਅੰਗ[2])
            if not 1024 <= ਹੋਸਟ <= 65535 or not 1 <= ਗੈਸਟ <= 65535 or (통신규약, ਹੋਸਟ) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ਨਿਯਮ_ਕੀਮਤ)
            사용중주소.add((통신규약, ਹੋਸਟ)); 자신.전달규칙들.append((통신규약, ਹੋਸਟ, ਗੈਸਟ))
        자신.수신창구들 = []
        for _ in range(2):
            ਸਰਵਰ_ਕੀਮਤ = socket.socket()
            ਸਰਵਰ_ਕੀਮਤ.bind(('127.0.0.1', 0)); ਸਰਵਰ_ਕੀਮਤ.listen(1); ਸਰਵਰ_ਕੀਮਤ.setblocking(False)
            자신.수신창구들.append(ਸਰਵਰ_ਕੀਮਤ)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.ਈਥਰਨੈਟ = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.ਰੁਕਣਾ_ਇਵੈਂਟ = threading.Event(); 자신.ਗਲਤੀ = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.ਸਾਇਕਲ_ਕੀਮਤ, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ਈਥਰਨੈਟ_ਪੋਰਟ = [ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ.getsockname()[1] for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ਗੈਸਟ_ਪਤਾ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.ਗੈਸਟ_ਪਤਾ)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.ਗੈਸਟ_ਪਤਾ)
        for 통신규약, ਹੋਸਟ, ਗੈਸਟ in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ਹੋਸਟ, 자신.ਗੈਸਟ_ਪਤਾ, ਗੈਸਟ)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ਹੋਸਟ_ਪਤਾ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ਈਥਰਨੈਟ_ਪੋਰਟ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, ਪੈਕੇਟ_ਸਮੱਗਰੀ):
        자신.대기중[1] += struct.pack('!I', len(ਪੈਕੇਟ_ਸਮੱਗਰੀ)) + ਪੈਕੇਟ_ਸਮੱਗਰੀ

    def ਟਰੇਸ_ਪੈਕੇਟ(자신, 방향, ਪੈਕੇਟ_ਸਮੱਗਰੀ):
        if not 자신.ਪਕੜਨਾ or len(ਪੈਕੇਟ_ਸਮੱਗਰੀ)<20: return
        ਔਫਸੈਟ_ਕੀਮਤ=(ਪੈਕੇਟ_ਸਮੱਗਰੀ[0]&15)*4
        ਦਾਖਲਾ_ਕੀਮਤ={'time':time.monotonic(),'direction':방향,'bytes':len(ਪੈਕੇਟ_ਸਮੱਗਰੀ),'protocol':ਪੈਕੇਟ_ਸਮੱਗਰੀ[9]}
        if ਪੈਕੇਟ_ਸਮੱਗਰੀ[9]==6 and len(ਪੈਕੇਟ_ਸਮੱਗਰੀ)>=ਔਫਸੈਟ_ਕੀਮਤ+20:
            원본자료,ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ,순서번호,확인번호,설정비트,ਵਿੰਡੋ=struct.unpack_from('!HHIIHH',ਪੈਕੇਟ_ਸਮੱਗਰੀ,ਔਫਸੈਟ_ਕੀਮਤ)
            ਦਾਖਲਾ_ਕੀਮਤ.update(source=원본자료,destination=ਮੰਜਿਲ_ਸਮੱਗਰੀ_ਪਤਾ,seq=순서번호,ack=확인번호,flags=설정비트&255,window=ਵਿੰਡੋ,
                        payload=len(ਪੈਕੇਟ_ਸਮੱਗਰੀ)-ਔਫਸੈਟ_ਕੀਮਤ-((ਪੈਕੇਟ_ਸਮੱਗਰੀ[ਔਫਸੈਟ_ਕੀਮਤ+12]>>4)*4))
        자신.ਟਰੇਸ_ਲੌਗ.append(ਦਾਖਲਾ_ਕੀਮਤ)
        if len(자신.ਟਰੇਸ_ਲੌਗ)>2048: del 자신.ਟਰੇਸ_ਲੌਗ[:1024]

    def 직렬전문입력(자신, ਸਮੱਗਰੀ):
        for ਵਰਣ_ਕੋਡ in ਸਮੱਗਰੀ:
            if ਵਰਣ_ਕੋਡ == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ਪਤਾ=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ਪਤਾ)))
                            자신.현재주소=ਪਤਾ
                        except ValueError:
                            pass
                    자신.ਟਰੇਸ_ਪੈਕੇਟ('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + ਮਸ਼ੀਨ_ਪਤਾ + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif ਵਰਣ_ਕੋਡ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if ਵਰਣ_ਕੋਡ not in (220, 221): 자신.잘못됨 = True
                    ਵਰਣ_ਕੋਡ = 192 if ਵਰਣ_ਕੋਡ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(ਵਰਣ_ਕੋਡ)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, ਸਮੱਗਰੀ):
        자신.ਈਥਰਨੈਟ += ਸਮੱਗਰੀ
        while len(자신.ਈਥਰਨੈਟ) >= 4:
            개수 = struct.unpack_from('!I', 자신.ਈਥਰਨੈਟ)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ਈਥਰਨੈਟ) < 개수 + 4: return
            실행틀 = bytes(자신.ਈਥਰਨੈਟ[4:4+개수]); del 자신.ਈਥਰਨੈਟ[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ਪਤਾ_ਰੂਪਾਂਤਰ_ਪੈਕੇਟ = 실행틀[14:42]
                if ਪਤਾ_ਰੂਪਾਂਤਰ_ਪੈਕੇਟ[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ਪਤਾ_ਰੂਪਾਂਤਰ_ਪੈਕੇਟ[24:28] == 자신.현재주소:
                    응답자료 = ਪਤਾ_ਰੂਪਾਂਤਰ_ਪੈਕੇਟ[:6] + b'\x00\x02' + ਮਸ਼ੀਨ_ਪਤਾ + 자신.현재주소 + ਪਤਾ_ਰੂਪਾਂਤਰ_ਪੈਕੇਟ[8:18]
                    자신.실행틀(실행틀[6:12] + ਮਸ਼ੀਨ_ਪਤਾ + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                ਪੈਕੇਟ_ਸਮੱਗਰੀ = 실행틀[14:]
                자신.ਟਰੇਸ_ਪੈਕੇਟ('to_guest',ਪੈਕੇਟ_ਸਮੱਗਰੀ)
                자신.대기중[0] += b'\xc0' + ਪੈਕੇਟ_ਸਮੱਗਰੀ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def ਸਾਇਕਲ_ਕੀਮਤ(자신):
        try:
            while not 자신.ਰੁਕਣਾ_ਇਵੈਂਟ.is_set():
                읽기대상들 = [ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ for 순번, ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 자신.접속자들 if ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ is not None]
                쓰기대상들 = [ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ for 순번, ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in enumerate(자신.접속자들) if ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 읽을수있음:
                    if ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ); 자신.접속자들[순번], _ = ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ); ਸਮੱਗਰੀ = ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ.recv(16384)
                        if not ਸਮੱਗਰੀ: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ਸਮੱਗਰੀ)
                for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 쓸수있음:
                    순번 = 자신.접속자들.index(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ)
                    try: 개수 = ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ਰੁਕਣਾ_ਇਵੈਂਟ.is_set(): 자신.ਗਲਤੀ = str(보조항목)

    def ਬੰਦ_ਕਰੋ(자신):
        자신.ਰੁਕਣਾ_ਇਵੈਂਟ.set(); 자신.작업가닥.join(timeout=2)
        for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in 자신.수신창구들 + 자신.접속자들:
            if ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ is not None: ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ): 자신.ਬੰਦ_ਕਰੋ()
