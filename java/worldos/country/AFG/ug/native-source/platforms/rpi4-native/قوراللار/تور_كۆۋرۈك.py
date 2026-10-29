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

ماشىنا_ئادرېس = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
ئىنتېرنېت_ئادرېسى_قىممىتى = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class تور_كۆۋرۈك:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), تۇتۇش=False, مېھمان_ئادرېس=None, باقار_ئادرېس='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        مېھمان_ئادرېس = مېھمان_ئادرېس or 자신.ip_config['IP']
        qemu_network(자신.ip_config, مېھمان_ئادرېس)
        ئادرېس=ipaddress.IPv4Address(مېھمان_ئادرېس)
        자신.مېھمان_ئادرېس=str(ئادرېس); 자신.현재주소=ئادرېس.packed
        ئادرېس=ipaddress.IPv4Address(باقار_ئادرېس)
        if ئادرېس.is_multicast or str(ئادرېس)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.باقار_ئادرېس=str(ئادرېس)
        자신.تۇتۇش = تۇتۇش; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', مەلۇمات_ئورۇنلاشتۇرۇش) for مەلۇمات_ئورۇنلاشتۇرۇش in range(50000,50008)}
        for سىزىق_قىممىتى in 전달규칙들:
            يول_زاپچاس = سىزىق_قىممىتى.split(':')
            if len(يول_زاپچاس) != 3 or يول_زاپچاس[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, باقار, مېھمان = يول_زاپچاس[0], int(يول_زاپچاس[1]), int(يول_زاپچاس[2])
            if not 1024 <= باقار <= 65535 or not 1 <= مېھمان <= 65535 or (통신규약, باقار) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + سىزىق_قىممىتى)
            사용중주소.add((통신규약, باقار)); 자신.전달규칙들.append((통신규약, باقار, مېھمان))
        자신.수신창구들 = []
        for _ in range(2):
            مۇلازىمىتېر_قىممىتى = socket.socket()
            مۇلازىمىتېر_قىممىتى.bind(('127.0.0.1', 0)); مۇلازىمىتېر_قىممىتى.listen(1); مۇلازىمىتېر_قىممىتى.setblocking(False)
            자신.수신창구들.append(مۇلازىمىتېر_قىممىتى)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.ئىسېرنېت = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.تورمۇزلىماق_ھادىسە = threading.Event(); 자신.خاتالىق = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.دەۋرىي_قىممىتى, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ئىسېرنېت_ئېغىز = [ھەرپ_تىزمىسى_مەلۇمات.getsockname()[1] for ھەرپ_تىزمىسى_مەلۇمات in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.مېھمان_ئادرېس) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.مېھمان_ئادرېس)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.مېھمان_ئادرېس)
        for 통신규약, باقار, مېھمان in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, باقار, 자신.مېھمان_ئادرېس, مېھمان)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.باقار_ئادرېس+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ئىسېرنېت_ئېغىز),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.대기중[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.تۇتۇش or len(꾸러미자료)<20: return
        ئاغما_قىممىتى=(꾸러미자료[0]&15)*4
        كىرگۈزۈش_قىممىتى={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=ئاغما_قىممىتى+20:
            원본자료,نىشان_مەلۇمات_ئادرېس,순서번호,확인번호,설정비트,كۆزنەك=struct.unpack_from('!HHIIHH',꾸러미자료,ئاغما_قىممىتى)
            كىرگۈزۈش_قىممىتى.update(source=원본자료,destination=نىشان_مەلۇمات_ئادرېس,seq=순서번호,ack=확인번호,flags=설정비트&255,window=كۆزنەك,
                        payload=len(꾸러미자료)-ئاغما_قىممىتى-((꾸러미자료[ئاغما_قىممىتى+12]>>4)*4))
        자신.추적기록.append(كىرگۈزۈش_قىممىتى)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, مەلۇمات):
        for ھەرپ_كودى in مەلۇمات:
            if ھەرپ_كودى == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ئادرېس=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ئادرېس)))
                            자신.현재주소=ئادرېس
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + ماشىنا_ئادرېس + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif ھەرپ_كودى == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if ھەرپ_كودى not in (220, 221): 자신.잘못됨 = True
                    ھەرپ_كودى = 192 if ھەرپ_كودى == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(ھەرپ_كودى)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, مەلۇمات):
        자신.ئىسېرنېت += مەلۇمات
        while len(자신.ئىسېرنېت) >= 4:
            개수 = struct.unpack_from('!I', 자신.ئىسېرنېت)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ئىسېرنېت) < 개수 + 4: return
            실행틀 = bytes(자신.ئىسېرنېت[4:4+개수]); del 자신.ئىسېرنېت[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                주소찾기전문 = 실행틀[14:42]
                if 주소찾기전문[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 주소찾기전문[24:28] == 자신.현재주소:
                    응답자료 = 주소찾기전문[:6] + b'\x00\x02' + ماشىنا_ئادرېس + 자신.현재주소 + 주소찾기전문[8:18]
                    자신.실행틀(실행틀[6:12] + ماشىنا_ئادرېس + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                꾸러미자료 = 실행틀[14:]
                자신.전문추적('to_guest',꾸러미자료)
                자신.대기중[0] += b'\xc0' + 꾸러미자료.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def دەۋرىي_قىممىتى(자신):
        try:
            while not 자신.تورمۇزلىماق_ھادىسە.is_set():
                읽기대상들 = [ھەرپ_تىزمىسى_مەلۇمات for 순번, ھەرپ_تىزمىسى_مەلۇمات in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ھەرپ_تىزمىسى_مەلۇمات for ھەرپ_تىزمىسى_مەلۇمات in 자신.접속자들 if ھەرپ_تىزمىسى_مەلۇمات is not None]
                쓰기대상들 = [ھەرپ_تىزمىسى_مەلۇمات for 순번, ھەرپ_تىزمىسى_مەلۇمات in enumerate(자신.접속자들) if ھەرپ_تىزمىسى_مەلۇمات is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ھەرپ_تىزمىسى_مەلۇمات in 읽을수있음:
                    if ھەرپ_تىزمىسى_مەلۇمات in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ھەرپ_تىزمىسى_مەلۇمات); 자신.접속자들[순번], _ = ھەرپ_تىزمىسى_مەلۇمات.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ھەرپ_تىزمىسى_مەلۇمات); مەلۇمات = ھەرپ_تىزمىسى_مەلۇمات.recv(16384)
                        if not مەلۇمات: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(مەلۇمات)
                for ھەرپ_تىزمىسى_مەلۇمات in 쓸수있음:
                    순번 = 자신.접속자들.index(ھەرپ_تىزمىسى_مەلۇمات)
                    try: 개수 = ھەرپ_تىزمىسى_مەلۇمات.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.تورمۇزلىماق_ھادىسە.is_set(): 자신.خاتالىق = str(보조항목)

    def ياپ(자신):
        자신.تورمۇزلىماق_ھادىسە.set(); 자신.작업가닥.join(timeout=2)
        for ھەرپ_تىزمىسى_مەلۇمات in 자신.수신창구들 + 자신.접속자들:
            if ھەرپ_تىزمىسى_مەلۇمات is not None: ھەرپ_تىزمىسى_مەلۇمات.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *دەلىل_رەت): 자신.ياپ()
