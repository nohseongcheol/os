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

عنوان_حقيقي = bytes.fromhex('525400123456')
بوابة_أجهزة_عنوان = bytes.fromhex('52550a000202')
عنوان_الإنترنت_قيمة = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class جسر_3de4fe3a:
    def __init__(자신, نقل_الملفات_رقم_المنفذ=2121, 전달규칙들=(), يسجل=False, ضيف_عنوان=None, مضيف_عنوان='127.0.0.1'):
        if not 1024 <= نقل_الملفات_رقم_المنفذ <= 65535 or 50000 <= نقل_الملفات_رقم_المنفذ <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.نقل_الملفات_رقم_المنفذ = نقل_الملفات_رقم_المنفذ
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ضيف_عنوان = ضيف_عنوان or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ضيف_عنوان)
        عنوان=ipaddress.IPv4Address(ضيف_عنوان)
        자신.ضيف_عنوان=str(عنوان); 자신.حديث_عنوان=عنوان.packed
        عنوان=ipaddress.IPv4Address(مضيف_عنوان)
        if عنوان.is_multicast or str(عنوان)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.مضيف_عنوان=str(عنوان)
        자신.يسجل = يسجل; 자신.سجل_التتبّع = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', نقل_الملفات_رقم_المنفذ)} | {('tcp', بيانات_منصب) for بيانات_منصب in range(50000,50008)}
        for تصفية_قيمة in 전달규칙들:
            مسار_مكون = تصفية_قيمة.split(':')
            if len(مسار_مكون) != 3 or مسار_مكون[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, مضيف, ضيف = مسار_مكون[0], int(مسار_مكون[1]), int(مسار_مكون[2])
            if not 1024 <= مضيف <= 65535 or not 1 <= ضيف <= 65535 or (통신규약, مضيف) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + تصفية_قيمة)
            사용중주소.add((통신규약, مضيف)); 자신.전달규칙들.append((통신규약, مضيف, ضيف))
        자신.수신창구들 = []
        for _ in range(2):
            خادم_قيمة = socket.socket()
            خادم_قيمة.bind(('127.0.0.1', 0)); خادم_قيمة.listen(1); خادم_قيمة.setblocking(False)
            자신.수신창구들.append(خادم_قيمة)
        자신.접속자들 = [None, None]
        자신.أنظمة_المعلومات_معلق = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.أنظمة_المعلومات_غير_صالح = False
        자신.إيقاف_مؤقت_حدث = threading.Event(); 자신.خطأ = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.خيطالعمل = threading.Thread(target=자신.دورة_قيمة, daemon=True)
        자신.خيطالعمل.start()

    def 전달인수(자신):
        منفذ_COM_رقم, منفذ_Ethernet = [سلسلة_بيانات.getsockname()[1] for سلسلة_بيانات in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ضيف_عنوان) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.نقل_الملفات_رقم_المنفذ, 자신.ضيف_عنوان)
        for رقم_المنفذ in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(رقم_المنفذ, 자신.ضيف_عنوان)
        for 통신규약, مضيف, ضيف in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, مضيف, 자신.ضيف_عنوان, ضيف)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.مضيف_عنوان+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(منفذ_COM_رقم),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(منفذ_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, حزمة_بيانات):
        자신.أنظمة_المعلومات_معلق[1] += struct.pack('!I', len(حزمة_بيانات)) + حزمة_بيانات

    def أثر_حزمة(자신, 방향, حزمة_بيانات):
        if not 자신.يسجل or len(حزمة_بيانات)<20: return
        إزاحة_قيمة=(حزمة_بيانات[0]&15)*4
        إدخال_قيمة_962f286b={'time':time.monotonic(),'direction':방향,'bytes':len(حزمة_بيانات),'protocol':حزمة_بيانات[9]}
        if حزمة_بيانات[9]==6 and len(حزمة_بيانات)>=إزاحة_قيمة+20:
            원본자료,وجهة_بيانات_عنوان,أمر_رقم,확인번호,تكوين_خدمة_النقل_الذكي_في_الخلفية,نافذة=struct.unpack_from('!HHIIHH',حزمة_بيانات,إزاحة_قيمة)
            إدخال_قيمة_962f286b.update(source=원본자료,destination=وجهة_بيانات_عنوان,seq=أمر_رقم,ack=확인번호,flags=تكوين_خدمة_النقل_الذكي_في_الخلفية&255,window=نافذة,
                        payload=len(حزمة_بيانات)-إزاحة_قيمة-((حزمة_بيانات[إزاحة_قيمة+12]>>4)*4))
        자신.سجل_التتبّع.append(إدخال_قيمة_962f286b)
        if len(자신.سجل_التتبّع)>2048: del 자신.سجل_التتبّع[:1024]

    def بروتوكول_الخط_التسلسلي_للإنترنت_إدخال(자신, بيانات):
        for رمز_الحرف in بيانات:
            if رمز_الحرف == 192:
                if 자신.직렬전문 and not 자신.أنظمة_المعلومات_غير_صالح and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        عنوان=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(عنوان)))
                            자신.حديث_عنوان=عنوان
                        except ValueError:
                            pass
                    자신.أثر_حزمة('from_guest',자신.직렬전문)
                    자신.실행틀(بوابة_أجهزة_عنوان + عنوان_حقيقي + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.أنظمة_المعلومات_غير_صالح = False
            elif رمز_الحرف == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if رمز_الحرف not in (220, 221): 자신.أنظمة_المعلومات_غير_صالح = True
                    رمز_الحرف = 192 if رمز_الحرف == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(رمز_الحرف)
                else: 자신.أنظمة_المعلومات_غير_صالح = True

    def 이더넷입력(자신, بيانات):
        자신.이더넷자료 += بيانات
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                عنوان_دقة_حزمة = 실행틀[14:42]
                if عنوان_دقة_حزمة[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and عنوان_دقة_حزمة[24:28] == 자신.حديث_عنوان:
                    رد_1262b476 = عنوان_دقة_حزمة[:6] + b'\x00\x02' + عنوان_حقيقي + 자신.حديث_عنوان + عنوان_دقة_حزمة[8:18]
                    자신.실행틀(실행틀[6:12] + عنوان_حقيقي + b'\x08\x06' + رد_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                حزمة_بيانات = 실행틀[14:]
                자신.أثر_حزمة('to_guest',حزمة_بيانات)
                자신.أنظمة_المعلومات_معلق[0] += b'\xc0' + حزمة_بيانات.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def دورة_قيمة(자신):
        try:
            while not 자신.إيقاف_مؤقت_حدث.is_set():
                읽기대상들 = [سلسلة_بيانات for 순번, سلسلة_بيانات in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [سلسلة_بيانات for سلسلة_بيانات in 자신.접속자들 if سلسلة_بيانات is not None]
                쓰기대상들 = [سلسلة_بيانات for 순번, سلسلة_بيانات in enumerate(자신.접속자들) if سلسلة_بيانات is not None and 자신.أنظمة_المعلومات_معلق[순번]]
                읽을수있음, قابل_للكتابة, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for سلسلة_بيانات in 읽을수있음:
                    if سلسلة_بيانات in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(سلسلة_بيانات); 자신.접속자들[순번], _ = سلسلة_بيانات.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(سلسلة_بيانات); بيانات = سلسلة_بيانات.recv(16384)
                        if not بيانات: return
                        (자신.بروتوكول_الخط_التسلسلي_للإنترنت_إدخال if 순번 == 0 else 자신.이더넷입력)(بيانات)
                for سلسلة_بيانات in قابل_للكتابة:
                    순번 = 자신.접속자들.index(سلسلة_بيانات)
                    try: 개수 = سلسلة_بيانات.send(자신.أنظمة_المعلومات_معلق[순번])
                    except BlockingIOError: continue
                    del 자신.أنظمة_المعلومات_معلق[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.أنظمة_المعلومات_معلق):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.إيقاف_مؤقت_حدث.is_set(): 자신.خطأ = str(보조항목)

    def إغلاق(자신):
        자신.إيقاف_مؤقت_حدث.set(); 자신.خيطالعمل.join(timeout=2)
        for سلسلة_بيانات in 자신.수신창구들 + 자신.접속자들:
            if سلسلة_بيانات is not None: سلسلة_بيانات.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *وسيطة_صفيف): 자신.إغلاق()
