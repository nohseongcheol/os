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

دستگاه_آدرس = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
آدرس_اینترنتی_مقدار = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class شبکه_پل:
    def __init__(자신, فایل_انتقال_شماره_درگاه=2121, 전달규칙들=(), ضبط_کردن=False, مهمان_آدرس=None, میزبان_آدرس='127.0.0.1'):
        if not 1024 <= فایل_انتقال_شماره_درگاه <= 65535 or 50000 <= فایل_انتقال_شماره_درگاه <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.فایل_انتقال_شماره_درگاه = فایل_انتقال_شماره_درگاه
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        مهمان_آدرس = مهمان_آدرس or 자신.ip_config['IP']
        qemu_network(자신.ip_config, مهمان_آدرس)
        آدرس=ipaddress.IPv4Address(مهمان_آدرس)
        자신.مهمان_آدرس=str(آدرس); 자신.현재주소=آدرس.packed
        آدرس=ipaddress.IPv4Address(میزبان_آدرس)
        if آدرس.is_multicast or str(آدرس)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.میزبان_آدرس=str(آدرس)
        자신.ضبط_کردن = ضبط_کردن; 자신.اثر_ماتریس_واقعه_نگار = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', فایل_انتقال_شماره_درگاه)} | {('tcp', داده_ها_مرتب_کردن) for داده_ها_مرتب_کردن in range(50000,50008)}
        for فیلتر_مقدار in 전달규칙들:
            مسیر_مؤلفه = فیلتر_مقدار.split(':')
            if len(مسیر_مؤلفه) != 3 or مسیر_مؤلفه[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, میزبان, مهمان = مسیر_مؤلفه[0], int(مسیر_مؤلفه[1]), int(مسیر_مؤلفه[2])
            if not 1024 <= میزبان <= 65535 or not 1 <= مهمان <= 65535 or (통신규약, میزبان) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + فیلتر_مقدار)
            사용중주소.add((통신규약, میزبان)); 자신.전달규칙들.append((통신규약, میزبان, مهمان))
        자신.수신창구들 = []
        for _ in range(2):
            سرور_مقدار = socket.socket()
            سرور_مقدار.bind(('127.0.0.1', 0)); سرور_مقدار.listen(1); سرور_مقدار.setblocking(False)
            자신.수신창구들.append(سرور_مقدار)
        자신.접속자들 = [None, None]
        자신.فناوری_اطلاعات_در_تعلیق = [bytearray(), bytearray()]
        자신.اترنت = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.فناوری_اطلاعات_بی_اعتبار = False
        자신.مکث_کردن_رویداد = threading.Event(); 자신.خطا = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.چرخه_مقدار, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, درگاه_اِترنت = [رشته_داده_ها.getsockname()[1] for رشته_داده_ها in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.مهمان_آدرس) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.فایل_انتقال_شماره_درگاه, 자신.مهمان_آدرس)
        for شماره_درگاه in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(شماره_درگاه, 자신.مهمان_آدرس)
        for 통신규약, میزبان, مهمان in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, میزبان, 자신.مهمان_آدرس, مهمان)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.میزبان_آدرس+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(درگاه_اِترنت),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, بسته_داده_ها):
        자신.فناوری_اطلاعات_در_تعلیق[1] += struct.pack('!I', len(بسته_داده_ها)) + بسته_داده_ها

    def اثر_ماتریس_بسته(자신, 방향, بسته_داده_ها):
        if not 자신.ضبط_کردن or len(بسته_داده_ها)<20: return
        جابجایی_لایه_ای_مقدار=(بسته_داده_ها[0]&15)*4
        ورودی_مقدار={'time':time.monotonic(),'direction':방향,'bytes':len(بسته_داده_ها),'protocol':بسته_داده_ها[9]}
        if بسته_داده_ها[9]==6 and len(بسته_داده_ها)>=جابجایی_لایه_ای_مقدار+20:
            원본자료,مقصد_داده_ها_آدرس,순서번호,확인번호,설정비트,پنجره=struct.unpack_from('!HHIIHH',بسته_داده_ها,جابجایی_لایه_ای_مقدار)
            ورودی_مقدار.update(source=원본자료,destination=مقصد_داده_ها_آدرس,seq=순서번호,ack=확인번호,flags=설정비트&255,window=پنجره,
                        payload=len(بسته_داده_ها)-جابجایی_لایه_ای_مقدار-((بسته_داده_ها[جابجایی_لایه_ای_مقدار+12]>>4)*4))
        자신.اثر_ماتریس_واقعه_نگار.append(ورودی_مقدار)
        if len(자신.اثر_ماتریس_واقعه_نگار)>2048: del 자신.اثر_ماتریس_واقعه_نگار[:1024]

    def 직렬전문입력(자신, داده_ها):
        for کد_نویسه in داده_ها:
            if کد_نویسه == 192:
                if 자신.직렬전문 and not 자신.فناوری_اطلاعات_بی_اعتبار and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        آدرس=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(آدرس)))
                            자신.현재주소=آدرس
                        except ValueError:
                            pass
                    자신.اثر_ماتریس_بسته('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + دستگاه_آدرس + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.فناوری_اطلاعات_بی_اعتبار = False
            elif کد_نویسه == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if کد_نویسه not in (220, 221): 자신.فناوری_اطلاعات_بی_اعتبار = True
                    کد_نویسه = 192 if کد_نویسه == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(کد_نویسه)
                else: 자신.فناوری_اطلاعات_بی_اعتبار = True

    def 이더넷입력(자신, داده_ها):
        자신.اترنت += داده_ها
        while len(자신.اترنت) >= 4:
            개수 = struct.unpack_from('!I', 자신.اترنت)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.اترنت) < 개수 + 4: return
            실행틀 = bytes(자신.اترنت[4:4+개수]); del 자신.اترنت[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                آدرس_دقت_بسته = 실행틀[14:42]
                if آدرس_دقت_بسته[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and آدرس_دقت_بسته[24:28] == 자신.현재주소:
                    응답자료 = آدرس_دقت_بسته[:6] + b'\x00\x02' + دستگاه_آدرس + 자신.현재주소 + آدرس_دقت_بسته[8:18]
                    자신.실행틀(실행틀[6:12] + دستگاه_آدرس + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                بسته_داده_ها = 실행틀[14:]
                자신.اثر_ماتریس_بسته('to_guest',بسته_داده_ها)
                자신.فناوری_اطلاعات_در_تعلیق[0] += b'\xc0' + بسته_داده_ها.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def چرخه_مقدار(자신):
        try:
            while not 자신.مکث_کردن_رویداد.is_set():
                읽기대상들 = [رشته_داده_ها for 순번, رشته_داده_ها in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [رشته_داده_ها for رشته_داده_ها in 자신.접속자들 if رشته_داده_ها is not None]
                쓰기대상들 = [رشته_داده_ها for 순번, رشته_داده_ها in enumerate(자신.접속자들) if رشته_داده_ها is not None and 자신.فناوری_اطلاعات_در_تعلیق[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for رشته_داده_ها in 읽을수있음:
                    if رشته_داده_ها in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(رشته_داده_ها); 자신.접속자들[순번], _ = رشته_داده_ها.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(رشته_داده_ها); داده_ها = رشته_داده_ها.recv(16384)
                        if not داده_ها: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(داده_ها)
                for رشته_داده_ها in 쓸수있음:
                    순번 = 자신.접속자들.index(رشته_داده_ها)
                    try: 개수 = رشته_داده_ها.send(자신.فناوری_اطلاعات_در_تعلیق[순번])
                    except BlockingIOError: continue
                    del 자신.فناوری_اطلاعات_در_تعلیق[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.فناوری_اطلاعات_در_تعلیق):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.مکث_کردن_رویداد.is_set(): 자신.خطا = str(보조항목)

    def بستن(자신):
        자신.مکث_کردن_رویداد.set(); 자신.작업가닥.join(timeout=2)
        for رشته_داده_ها in 자신.수신창구들 + 자신.접속자들:
            if رشته_داده_ها is not None: رشته_داده_ها.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *آرگومان_آرايه): 자신.بستن()
