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

مەکینه_ناونیشان = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
ناونیشانی_ئینتەرنێتی_نرخ = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 통신다리:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), تۆمارکردن=False, 게스트주소=None, جێدەر_ناونیشان='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        게스트주소 = 게스트주소 or 자신.ip_config['IP']
        qemu_network(자신.ip_config, 게스트주소)
        ناونیشان=ipaddress.IPv4Address(게스트주소)
        자신.게스트주소=str(ناونیشان); 자신.현재주소=ناونیشان.packed
        ناونیشان=ipaddress.IPv4Address(جێدەر_ناونیشان)
        if ناونیشان.is_multicast or str(ناونیشان)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.جێدەر_ناونیشان=str(ناونیشان)
        자신.تۆمارکردن = تۆمارکردن; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for ڕێسا_نرخ in 전달규칙들:
            گوزەر_پارچە = ڕێسا_نرخ.split(':')
            if len(گوزەر_پارچە) != 3 or گوزەر_پارچە[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, جێدەر, 커널실행 = گوزەر_پارچە[0], int(گوزەر_پارچە[1]), int(گوزەر_پارچە[2])
            if not 1024 <= جێدەر <= 65535 or not 1 <= 커널실행 <= 65535 or (통신규약, جێدەر) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ڕێسا_نرخ)
            사용중주소.add((통신규약, جێدەر)); 자신.전달규칙들.append((통신규약, جێدەر, 커널실행))
        자신.수신창구들 = []
        for _ in range(2):
            ڕاژەکار_نرخ = socket.socket()
            ڕاژەکار_نرخ.bind(('127.0.0.1', 0)); ڕاژەکار_نرخ.listen(1); ڕاژەکار_نرخ.setblocking(False)
            자신.수신창구들.append(ڕاژەکار_نرخ)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.ئێتێرنێت = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.ڕاگرتن_پێشهات = threading.Event(); 자신.هەڵە = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.خول_نرخ, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ئێتێرنێت_دەرگا = [رست_دەیتا.getsockname()[1] for رست_دەیتا in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.게스트주소) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.게스트주소)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.게스트주소)
        for 통신규약, جێدەر, 커널실행 in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, جێدەر, 자신.게스트주소, 커널실행)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.جێدەر_ناونیشان+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ئێتێرنێت_دەرگا),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, پاکه_ت_دەیتا):
        자신.대기중[1] += struct.pack('!I', len(پاکه_ت_دەیتا)) + پاکه_ت_دەیتا

    def 전문추적(자신, 방향, پاکه_ت_دەیتا):
        if not 자신.تۆمارکردن or len(پاکه_ت_دەیتا)<20: return
        ئۆفسێت_نرخ=(پاکه_ت_دەیتا[0]&15)*4
        تێنووسین_نرخ={'time':time.monotonic(),'direction':방향,'bytes':len(پاکه_ت_دەیتا),'protocol':پاکه_ت_دەیتا[9]}
        if پاکه_ت_دەیتا[9]==6 and len(پاکه_ت_دەیتا)>=ئۆفسێت_نرخ+20:
            원본자료,جێمەبەست_دەیتا_ناونیشان,순서번호,확인번호,설정비트,پەنجەرە=struct.unpack_from('!HHIIHH',پاکه_ت_دەیتا,ئۆفسێت_نرخ)
            تێنووسین_نرخ.update(source=원본자료,destination=جێمەبەست_دەیتا_ناونیشان,seq=순서번호,ack=확인번호,flags=설정비트&255,window=پەنجەرە,
                        payload=len(پاکه_ت_دەیتا)-ئۆفسێت_نرخ-((پاکه_ت_دەیتا[ئۆفسێت_نرخ+12]>>4)*4))
        자신.추적기록.append(تێنووسین_نرخ)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, دەیتا):
        for کۆدی_نووسە in دەیتا:
            if کۆدی_نووسە == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ناونیشان=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ناونیشان)))
                            자신.현재주소=ناونیشان
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + مەکینه_ناونیشان + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif کۆدی_نووسە == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if کۆدی_نووسە not in (220, 221): 자신.잘못됨 = True
                    کۆدی_نووسە = 192 if کۆدی_نووسە == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(کۆدی_نووسە)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, دەیتا):
        자신.ئێتێرنێت += دەیتا
        while len(자신.ئێتێرنێت) >= 4:
            개수 = struct.unpack_from('!I', 자신.ئێتێرنێت)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ئێتێرنێت) < 개수 + 4: return
            실행틀 = bytes(자신.ئێتێرنێت[4:4+개수]); del 자신.ئێتێرنێت[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ناونیشان_وردبینی_پاکه_ت = 실행틀[14:42]
                if ناونیشان_وردبینی_پاکه_ت[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ناونیشان_وردبینی_پاکه_ت[24:28] == 자신.현재주소:
                    응답자료 = ناونیشان_وردبینی_پاکه_ت[:6] + b'\x00\x02' + مەکینه_ناونیشان + 자신.현재주소 + ناونیشان_وردبینی_پاکه_ت[8:18]
                    자신.실행틀(실행틀[6:12] + مەکینه_ناونیشان + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                پاکه_ت_دەیتا = 실행틀[14:]
                자신.전문추적('to_guest',پاکه_ت_دەیتا)
                자신.대기중[0] += b'\xc0' + پاکه_ت_دەیتا.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def خول_نرخ(자신):
        try:
            while not 자신.ڕاگرتن_پێشهات.is_set():
                읽기대상들 = [رست_دەیتا for 순번, رست_دەیتا in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [رست_دەیتا for رست_دەیتا in 자신.접속자들 if رست_دەیتا is not None]
                쓰기대상들 = [رست_دەیتا for 순번, رست_دەیتا in enumerate(자신.접속자들) if رست_دەیتا is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for رست_دەیتا in 읽을수있음:
                    if رست_دەیتا in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(رست_دەیتا); 자신.접속자들[순번], _ = رست_دەیتا.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(رست_دەیتا); دەیتا = رست_دەیتا.recv(16384)
                        if not دەیتا: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(دەیتا)
                for رست_دەیتا in 쓸수있음:
                    순번 = 자신.접속자들.index(رست_دەیتا)
                    try: 개수 = رست_دەیتا.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ڕاگرتن_پێشهات.is_set(): 자신.هەڵە = str(보조항목)

    def داخستن(자신):
        자신.ڕاگرتن_پێشهات.set(); 자신.작업가닥.join(timeout=2)
        for رست_دەیتا in 자신.수신창구들 + 자신.접속자들:
            if رست_دەیتا is not None: رست_دەیتا.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ئارگیومێنت_ڕیزی_داتا): 자신.داخستن()
