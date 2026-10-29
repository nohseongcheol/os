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

مشین_پتہ = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
انٹرنیٹ_پتہ_قدر = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class نیٹ_ورک_برج:
    def __init__(자신, فائل_منتقلی_دہانہ_نمبر=2121, 전달규칙들=(), کیپچر_کریں=False, مہمان_پتہ=None, میزبان_پتہ='127.0.0.1'):
        if not 1024 <= فائل_منتقلی_دہانہ_نمبر <= 65535 or 50000 <= فائل_منتقلی_دہانہ_نمبر <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.فائل_منتقلی_دہانہ_نمبر = فائل_منتقلی_دہانہ_نمبر
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        مہمان_پتہ = مہمان_پتہ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, مہمان_پتہ)
        پتہ=ipaddress.IPv4Address(مہمان_پتہ)
        자신.مہمان_پتہ=str(پتہ); 자신.현재주소=پتہ.packed
        پتہ=ipaddress.IPv4Address(میزبان_پتہ)
        if پتہ.is_multicast or str(پتہ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.میزبان_پتہ=str(پتہ)
        자신.کیپچر_کریں = کیپچر_کریں; 자신.ٹریس_لاگ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', فائل_منتقلی_دہانہ_نمبر)} | {('tcp', کوائف_پوزیشن_ٹھیک_کریں) for کوائف_پوزیشن_ٹھیک_کریں in range(50000,50008)}
        for فلٹر_قدر in 전달규칙들:
            راہ_جزو = فلٹر_قدر.split(':')
            if len(راہ_جزو) != 3 or راہ_جزو[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, میزبان, مہمان = راہ_جزو[0], int(راہ_جزو[1]), int(راہ_جزو[2])
            if not 1024 <= میزبان <= 65535 or not 1 <= مہمان <= 65535 or (통신규약, میزبان) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + فلٹر_قدر)
            사용중주소.add((통신규약, میزبان)); 자신.전달규칙들.append((통신규약, میزبان, مہمان))
        자신.수신창구들 = []
        for _ in range(2):
            سرور_قدر = socket.socket()
            سرور_قدر.bind(('127.0.0.1', 0)); سرور_قدر.listen(1); سرور_قدر.setblocking(False)
            자신.수신창구들.append(سرور_قدر)
        자신.접속자들 = [None, None]
        자신.معلومات_ٹیکنالوجی_زیر_التواء = [bytearray(), bytearray()]
        자신.ایتھرنیٹ = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.معلومات_ٹیکنالوجی_بے_جواز = False
        자신.توقف_ایونٹ = threading.Event(); 자신.غلطی = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.گردش_قدر, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ایتھرنیٹ_پورٹ = [سلک_کوائف.getsockname()[1] for سلک_کوائف in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.مہمان_پتہ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.فائل_منتقلی_دہانہ_نمبر, 자신.مہمان_پتہ)
        for دہانہ_نمبر in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(دہانہ_نمبر, 자신.مہمان_پتہ)
        for 통신규약, میزبان, مہمان in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, میزبان, 자신.مہمان_پتہ, مہمان)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.میزبان_پتہ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ایتھرنیٹ_پورٹ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, پیکٹ_کوائف):
        자신.معلومات_ٹیکنالوجی_زیر_التواء[1] += struct.pack('!I', len(پیکٹ_کوائف)) + پیکٹ_کوائف

    def ٹریس_پیکٹ(자신, 방향, پیکٹ_کوائف):
        if not 자신.کیپچر_کریں or len(پیکٹ_کوائف)<20: return
        آفسٹ_قدر=(پیکٹ_کوائف[0]&15)*4
        اندراج_قدر={'time':time.monotonic(),'direction':방향,'bytes':len(پیکٹ_کوائف),'protocol':پیکٹ_کوائف[9]}
        if پیکٹ_کوائف[9]==6 and len(پیکٹ_کوائف)>=آفسٹ_قدر+20:
            원본자료,منزل_مقصود_کوائف_پتہ,순서번호,확인번호,설정비트,ونڈو=struct.unpack_from('!HHIIHH',پیکٹ_کوائف,آفسٹ_قدر)
            اندراج_قدر.update(source=원본자료,destination=منزل_مقصود_کوائف_پتہ,seq=순서번호,ack=확인번호,flags=설정비트&255,window=ونڈو,
                        payload=len(پیکٹ_کوائف)-آفسٹ_قدر-((پیکٹ_کوائف[آفسٹ_قدر+12]>>4)*4))
        자신.ٹریس_لاگ.append(اندراج_قدر)
        if len(자신.ٹریس_لاگ)>2048: del 자신.ٹریس_لاگ[:1024]

    def 직렬전문입력(자신, کوائف):
        for کریکٹر_ضابطہ in کوائف:
            if کریکٹر_ضابطہ == 192:
                if 자신.직렬전문 and not 자신.معلومات_ٹیکنالوجی_بے_جواز and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        پتہ=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(پتہ)))
                            자신.현재주소=پتہ
                        except ValueError:
                            pass
                    자신.ٹریس_پیکٹ('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + مشین_پتہ + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.معلومات_ٹیکنالوجی_بے_جواز = False
            elif کریکٹر_ضابطہ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if کریکٹر_ضابطہ not in (220, 221): 자신.معلومات_ٹیکنالوجی_بے_جواز = True
                    کریکٹر_ضابطہ = 192 if کریکٹر_ضابطہ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(کریکٹر_ضابطہ)
                else: 자신.معلومات_ٹیکنالوجی_بے_جواز = True

    def 이더넷입력(자신, کوائف):
        자신.ایتھرنیٹ += کوائف
        while len(자신.ایتھرنیٹ) >= 4:
            개수 = struct.unpack_from('!I', 자신.ایتھرنیٹ)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ایتھرنیٹ) < 개수 + 4: return
            실행틀 = bytes(자신.ایتھرنیٹ[4:4+개수]); del 자신.ایتھرنیٹ[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                پتہ_جزیات_کاری_پیکٹ = 실행틀[14:42]
                if پتہ_جزیات_کاری_پیکٹ[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and پتہ_جزیات_کاری_پیکٹ[24:28] == 자신.현재주소:
                    응답자료 = پتہ_جزیات_کاری_پیکٹ[:6] + b'\x00\x02' + مشین_پتہ + 자신.현재주소 + پتہ_جزیات_کاری_پیکٹ[8:18]
                    자신.실행틀(실행틀[6:12] + مشین_پتہ + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                پیکٹ_کوائف = 실행틀[14:]
                자신.ٹریس_پیکٹ('to_guest',پیکٹ_کوائف)
                자신.معلومات_ٹیکنالوجی_زیر_التواء[0] += b'\xc0' + پیکٹ_کوائف.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def گردش_قدر(자신):
        try:
            while not 자신.توقف_ایونٹ.is_set():
                읽기대상들 = [سلک_کوائف for 순번, سلک_کوائف in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [سلک_کوائف for سلک_کوائف in 자신.접속자들 if سلک_کوائف is not None]
                쓰기대상들 = [سلک_کوائف for 순번, سلک_کوائف in enumerate(자신.접속자들) if سلک_کوائف is not None and 자신.معلومات_ٹیکنالوجی_زیر_التواء[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for سلک_کوائف in 읽을수있음:
                    if سلک_کوائف in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(سلک_کوائف); 자신.접속자들[순번], _ = سلک_کوائف.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(سلک_کوائف); کوائف = سلک_کوائف.recv(16384)
                        if not کوائف: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(کوائف)
                for سلک_کوائف in 쓸수있음:
                    순번 = 자신.접속자들.index(سلک_کوائف)
                    try: 개수 = سلک_کوائف.send(자신.معلومات_ٹیکنالوجی_زیر_التواء[순번])
                    except BlockingIOError: continue
                    del 자신.معلومات_ٹیکنالوجی_زیر_التواء[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.معلومات_ٹیکنالوجی_زیر_التواء):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.توقف_ایونٹ.is_set(): 자신.غلطی = str(보조항목)

    def بند_کریں(자신):
        자신.توقف_ایونٹ.set(); 자신.작업가닥.join(timeout=2)
        for سلک_کوائف in 자신.수신창구들 + 자신.접속자들:
            if سلک_کوائف is not None: سلک_کوائف.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *دلائل_لڑی): 자신.بند_کریں()
