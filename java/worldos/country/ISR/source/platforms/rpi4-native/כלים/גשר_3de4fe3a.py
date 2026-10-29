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

כתובת_ממשית = bytes.fromhex('525400123456')
שער_חומרה_למען = bytes.fromhex('52550a000202')
כתובת_אינטרנט_ערך = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class גשר_3de4fe3a:
    def __init__(자신, העברת_קבצים_מספר_יציאה=2121, 전달규칙들=(), לכוד=False, אורח_למען=None, ארח_למען='127.0.0.1'):
        if not 1024 <= העברת_קבצים_מספר_יציאה <= 65535 or 50000 <= העברת_קבצים_מספר_יציאה <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.העברת_קבצים_מספר_יציאה = העברת_קבצים_מספר_יציאה
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        אורח_למען = אורח_למען or 자신.ip_config['IP']
        qemu_network(자신.ip_config, אורח_למען)
        למען=ipaddress.IPv4Address(אורח_למען)
        자신.אורח_למען=str(למען); 자신.נוכחי_למען=למען.packed
        למען=ipaddress.IPv4Address(ארח_למען)
        if למען.is_multicast or str(למען)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ארח_למען=str(למען)
        자신.לכוד = לכוד; 자신.יומן_מעקב = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', העברת_קבצים_מספר_יציאה)} | {('tcp', נתונים_עמדה) for נתונים_עמדה in range(50000,50008)}
        for כלל_ערך in 전달규칙들:
            נתיב_רכיב = כלל_ערך.split(':')
            if len(נתיב_רכיב) != 3 or נתיב_רכיב[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ארח, אורח = נתיב_רכיב[0], int(נתיב_רכיב[1]), int(נתיב_רכיב[2])
            if not 1024 <= ארח <= 65535 or not 1 <= אורח <= 65535 or (통신규약, ארח) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + כלל_ערך)
            사용중주소.add((통신규약, ארח)); 자신.전달규칙들.append((통신규약, ארח, אורח))
        자신.수신창구들 = []
        for _ in range(2):
            שרת_ערך = socket.socket()
            שרת_ערך.bind(('127.0.0.1', 0)); שרת_ערך.listen(1); שרת_ערך.setblocking(False)
            자신.수신창구들.append(שרת_ערך)
        자신.접속자들 = [None, None]
        자신.מערכות_מידע_ממתין = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.מערכות_מידע_לא_חוקי = False
        자신.השהה_אירוע = threading.Event(); 자신.שגיאה = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.משימתרקע = threading.Thread(target=자신.מחזור_ערך, daemon=True)
        자신.משימתרקע.start()

    def 전달인수(자신):
        직렬접속번호, 이더넷접속번호 = [מחרוזת_נתונים.getsockname()[1] for מחרוזת_נתונים in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.אורח_למען) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.העברת_קבצים_מספר_יציאה, 자신.אורח_למען)
        for מספר_יציאה in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(מספר_יציאה, 자신.אורח_למען)
        for 통신규약, ארח, אורח in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ארח, 자신.אורח_למען, אורח)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ארח_למען+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(이더넷접속번호),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, מנה_נתונים):
        자신.מערכות_מידע_ממתין[1] += struct.pack('!I', len(מנה_נתונים)) + מנה_נתונים

    def עקבה_מנה(자신, 방향, מנה_נתונים):
        if not 자신.לכוד or len(מנה_נתונים)<20: return
        היסט_ערך=(מנה_נתונים[0]&15)*4
        ערך_ערך={'time':time.monotonic(),'direction':방향,'bytes':len(מנה_נתונים),'protocol':מנה_נתונים[9]}
        if מנה_נתונים[9]==6 and len(מנה_נתונים)>=היסט_ערך+20:
            원본자료,יעד_נתונים_למען,순서번호,확인번호,설정비트,חלון=struct.unpack_from('!HHIIHH',מנה_נתונים,היסט_ערך)
            ערך_ערך.update(source=원본자료,destination=יעד_נתונים_למען,seq=순서번호,ack=확인번호,flags=설정비트&255,window=חלון,
                        payload=len(מנה_נתונים)-היסט_ערך-((מנה_נתונים[היסט_ערך+12]>>4)*4))
        자신.יומן_מעקב.append(ערך_ערך)
        if len(자신.יומן_מעקב)>2048: del 자신.יומן_מעקב[:1024]

    def פרוטוקול_אינטרנט_לקו_טורי_קלט(자신, נתונים):
        for נקודת_קוד in נתונים:
            if נקודת_קוד == 192:
                if 자신.직렬전문 and not 자신.מערכות_מידע_לא_חוקי and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        למען=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(למען)))
                            자신.נוכחי_למען=למען
                        except ValueError:
                            pass
                    자신.עקבה_מנה('from_guest',자신.직렬전문)
                    자신.실행틀(שער_חומרה_למען + כתובת_ממשית + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.מערכות_מידע_לא_חוקי = False
            elif נקודת_קוד == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if נקודת_קוד not in (220, 221): 자신.מערכות_מידע_לא_חוקי = True
                    נקודת_קוד = 192 if נקודת_קוד == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(נקודת_קוד)
                else: 자신.מערכות_מידע_לא_חוקי = True

    def 이더넷입력(자신, נתונים):
        자신.이더넷자료 += נתונים
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                למען_רזולוציה_מנה = 실행틀[14:42]
                if למען_רזולוציה_מנה[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and למען_רזולוציה_מנה[24:28] == 자신.נוכחי_למען:
                    תגובה = למען_רזולוציה_מנה[:6] + b'\x00\x02' + כתובת_ממשית + 자신.נוכחי_למען + למען_רזולוציה_מנה[8:18]
                    자신.실행틀(실행틀[6:12] + כתובת_ממשית + b'\x08\x06' + תגובה)
            elif 실행틀[12:14] == b'\x08\x00':
                מנה_נתונים = 실행틀[14:]
                자신.עקבה_מנה('to_guest',מנה_נתונים)
                자신.מערכות_מידע_ממתין[0] += b'\xc0' + מנה_נתונים.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def מחזור_ערך(자신):
        try:
            while not 자신.השהה_אירוע.is_set():
                읽기대상들 = [מחרוזת_נתונים for 순번, מחרוזת_נתונים in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [מחרוזת_נתונים for מחרוזת_נתונים in 자신.접속자들 if מחרוזת_נתונים is not None]
                쓰기대상들 = [מחרוזת_נתונים for 순번, מחרוזת_נתונים in enumerate(자신.접속자들) if מחרוזת_נתונים is not None and 자신.מערכות_מידע_ממתין[순번]]
                읽을수있음, ניתן_לכתיבה, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for מחרוזת_נתונים in 읽을수있음:
                    if מחרוזת_נתונים in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(מחרוזת_נתונים); 자신.접속자들[순번], _ = מחרוזת_נתונים.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(מחרוזת_נתונים); נתונים = מחרוזת_נתונים.recv(16384)
                        if not נתונים: return
                        (자신.פרוטוקול_אינטרנט_לקו_טורי_קלט if 순번 == 0 else 자신.이더넷입력)(נתונים)
                for מחרוזת_נתונים in ניתן_לכתיבה:
                    순번 = 자신.접속자들.index(מחרוזת_נתונים)
                    try: 개수 = מחרוזת_נתונים.send(자신.מערכות_מידע_ממתין[순번])
                    except BlockingIOError: continue
                    del 자신.מערכות_מידע_ממתין[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.מערכות_מידע_ממתין):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.השהה_אירוע.is_set(): 자신.שגיאה = str(보조항목)

    def סגירה(자신):
        자신.השהה_אירוע.set(); 자신.משימתרקע.join(timeout=2)
        for מחרוזת_נתונים in 자신.수신창구들 + 자신.접속자들:
            if מחרוזת_נתונים is not None: מחרוזת_נתונים.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ארגומנט_מערך): 자신.סגירה()
