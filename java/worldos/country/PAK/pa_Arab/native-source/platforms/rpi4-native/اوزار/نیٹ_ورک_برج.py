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

مشین_پتا = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
انٹرنیٹ_پتا_قدر = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class نیٹ_ورک_برج:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), کھیچو=False, مہمان_پتا_4bde7f91=None, مہمان_پتا='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        مہمان_پتا_4bde7f91 = مہمان_پتا_4bde7f91 or 자신.ip_config['IP']
        qemu_network(자신.ip_config, مہمان_پتا_4bde7f91)
        پتا=ipaddress.IPv4Address(مہمان_پتا_4bde7f91)
        자신.مہمان_پتا_4bde7f91=str(پتا); 자신.현재주소=پتا.packed
        پتا=ipaddress.IPv4Address(مہمان_پتا)
        if پتا.is_multicast or str(پتا)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.مہمان_پتا=str(پتا)
        자신.کھیچو = کھیچو; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for فلٹر_قدر in 전달규칙들:
            راہ_جزو = فلٹر_قدر.split(':')
            if len(راہ_جزو) != 3 or راہ_جزو[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, مہمان_b78e430d, مہمان = راہ_جزو[0], int(راہ_جزو[1]), int(راہ_جزو[2])
            if not 1024 <= مہمان_b78e430d <= 65535 or not 1 <= مہمان <= 65535 or (통신규약, مہمان_b78e430d) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + فلٹر_قدر)
            사용중주소.add((통신규약, مہمان_b78e430d)); 자신.전달규칙들.append((통신규약, مہمان_b78e430d, مہمان))
        자신.수신창구들 = []
        for _ in range(2):
            سرور_قدر = socket.socket()
            سرور_قدر.bind(('127.0.0.1', 0)); سرور_قدر.listen(1); سرور_قدر.setblocking(False)
            자신.수신창구들.append(سرور_قدر)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.ایتھرنیٹ = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.توقف_کرو_واقعہ = threading.Event(); 자신.نقص = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.دورہ_قدر, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ایتھرنیٹ_دہانہ = [سٹرنگ_کوائف.getsockname()[1] for سٹرنگ_کوائف in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.مہمان_پتا_4bde7f91) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.مہمان_پتا_4bde7f91)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.مہمان_پتا_4bde7f91)
        for 통신규약, مہمان_b78e430d, مہمان in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, مہمان_b78e430d, 자신.مہمان_پتا_4bde7f91, مہمان)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.مہمان_پتا+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ایتھرنیٹ_دہانہ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, پیکٹ_کوائف):
        자신.대기중[1] += struct.pack('!I', len(پیکٹ_کوائف)) + پیکٹ_کوائف

    def 전문추적(자신, 방향, پیکٹ_کوائف):
        if not 자신.کھیچو or len(پیکٹ_کوائف)<20: return
        آف_سیٹ_قدر=(پیکٹ_کوائف[0]&15)*4
        داخلہ_قدر={'time':time.monotonic(),'direction':방향,'bytes':len(پیکٹ_کوائف),'protocol':پیکٹ_کوائف[9]}
        if پیکٹ_کوائف[9]==6 and len(پیکٹ_کوائف)>=آف_سیٹ_قدر+20:
            원본자료,منزل_مقصود_کوائف_پتا,순서번호,확인번호,설정비트,کھڑکی=struct.unpack_from('!HHIIHH',پیکٹ_کوائف,آف_سیٹ_قدر)
            داخلہ_قدر.update(source=원본자료,destination=منزل_مقصود_کوائف_پتا,seq=순서번호,ack=확인번호,flags=설정비트&255,window=کھڑکی,
                        payload=len(پیکٹ_کوائف)-آف_سیٹ_قدر-((پیکٹ_کوائف[آف_سیٹ_قدر+12]>>4)*4))
        자신.추적기록.append(داخلہ_قدر)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, کوائف):
        for کیریکٹر_کوڈ in کوائف:
            if کیریکٹر_کوڈ == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        پتا=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(پتا)))
                            자신.현재주소=پتا
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + مشین_پتا + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif کیریکٹر_کوڈ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if کیریکٹر_کوڈ not in (220, 221): 자신.잘못됨 = True
                    کیریکٹر_کوڈ = 192 if کیریکٹر_کوڈ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(کیریکٹر_کوڈ)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, کوائف):
        자신.ایتھرنیٹ += کوائف
        while len(자신.ایتھرنیٹ) >= 4:
            개수 = struct.unpack_from('!I', 자신.ایتھرنیٹ)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ایتھرنیٹ) < 개수 + 4: return
            실행틀 = bytes(자신.ایتھرنیٹ[4:4+개수]); del 자신.ایتھرنیٹ[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                پتا_جزیات_کاری_پیکٹ = 실행틀[14:42]
                if پتا_جزیات_کاری_پیکٹ[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and پتا_جزیات_کاری_پیکٹ[24:28] == 자신.현재주소:
                    응답자료 = پتا_جزیات_کاری_پیکٹ[:6] + b'\x00\x02' + مشین_پتا + 자신.현재주소 + پتا_جزیات_کاری_پیکٹ[8:18]
                    자신.실행틀(실행틀[6:12] + مشین_پتا + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                پیکٹ_کوائف = 실행틀[14:]
                자신.전문추적('to_guest',پیکٹ_کوائف)
                자신.대기중[0] += b'\xc0' + پیکٹ_کوائف.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def دورہ_قدر(자신):
        try:
            while not 자신.توقف_کرو_واقعہ.is_set():
                읽기대상들 = [سٹرنگ_کوائف for 순번, سٹرنگ_کوائف in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [سٹرنگ_کوائف for سٹرنگ_کوائف in 자신.접속자들 if سٹرنگ_کوائف is not None]
                쓰기대상들 = [سٹرنگ_کوائف for 순번, سٹرنگ_کوائف in enumerate(자신.접속자들) if سٹرنگ_کوائف is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for سٹرنگ_کوائف in 읽을수있음:
                    if سٹرنگ_کوائف in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(سٹرنگ_کوائف); 자신.접속자들[순번], _ = سٹرنگ_کوائف.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(سٹرنگ_کوائف); کوائف = سٹرنگ_کوائف.recv(16384)
                        if not کوائف: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(کوائف)
                for سٹرنگ_کوائف in 쓸수있음:
                    순번 = 자신.접속자들.index(سٹرنگ_کوائف)
                    try: 개수 = سٹرنگ_کوائف.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.توقف_کرو_واقعہ.is_set(): 자신.نقص = str(보조항목)

    def بند_کرو(자신):
        자신.توقف_کرو_واقعہ.set(); 자신.작업가닥.join(timeout=2)
        for سٹرنگ_کوائف in 자신.수신창구들 + 자신.접속자들:
            if سٹرنگ_کوائف is not None: سٹرنگ_کوائف.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *دلیل_ایرے): 자신.بند_کرو()
