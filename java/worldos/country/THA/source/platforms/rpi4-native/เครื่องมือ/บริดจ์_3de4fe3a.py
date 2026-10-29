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

เลขที่อยู่จริง = bytes.fromhex('525400123456')
เกตเวย์_ฮาร์ดแวร์_อีเมล = bytes.fromhex('52550a000202')
ที่อยู่อินเทอร์เน็ต_ค่า = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class บริดจ์_3de4fe3a:
    def __init__(자신, การถ่ายโอนแฟ้ม_หมายเลขพอร์ต=2121, 전달규칙들=(), จับ=False, ผู้เยี่ยมชม_อีเมล=None, โฮสต์_อีเมล='127.0.0.1'):
        if not 1024 <= การถ่ายโอนแฟ้ม_หมายเลขพอร์ต <= 65535 or 50000 <= การถ่ายโอนแฟ้ม_หมายเลขพอร์ต <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.การถ่ายโอนแฟ้ม_หมายเลขพอร์ต = การถ่ายโอนแฟ้ม_หมายเลขพอร์ต
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ผู้เยี่ยมชม_อีเมล = ผู้เยี่ยมชม_อีเมล or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ผู้เยี่ยมชม_อีเมล)
        อีเมล=ipaddress.IPv4Address(ผู้เยี่ยมชม_อีเมล)
        자신.ผู้เยี่ยมชม_อีเมล=str(อีเมล); 자신.ปัจจุบัน_อีเมล=อีเมล.packed
        อีเมล=ipaddress.IPv4Address(โฮสต์_อีเมล)
        if อีเมล.is_multicast or str(อีเมล)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.โฮสต์_อีเมล=str(อีเมล)
        자신.จับ = จับ; 자신.แฟ้มบันทึกการติดตาม = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', การถ่ายโอนแฟ้ม_หมายเลขพอร์ต)} | {('tcp', ข้อมูล_ตําแหน่ง) for ข้อมูล_ตําแหน่ง in range(50000,50008)}
        for กฎ_ค่า in 전달규칙들:
            พาธ_คอมโพเนนต์ = กฎ_ค่า.split(':')
            if len(พาธ_คอมโพเนนต์) != 3 or พาธ_คอมโพเนนต์[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, โฮสต์, ผู้เยี่ยมชม = พาธ_คอมโพเนนต์[0], int(พาธ_คอมโพเนนต์[1]), int(พาธ_คอมโพเนนต์[2])
            if not 1024 <= โฮสต์ <= 65535 or not 1 <= ผู้เยี่ยมชม <= 65535 or (통신규약, โฮสต์) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + กฎ_ค่า)
            사용중주소.add((통신규약, โฮสต์)); 자신.전달규칙들.append((통신규약, โฮสต์, ผู้เยี่ยมชม))
        자신.수신창구들 = []
        for _ in range(2):
            เซิร์ฟเวอร์_ค่า = socket.socket()
            เซิร์ฟเวอร์_ค่า.bind(('127.0.0.1', 0)); เซิร์ฟเวอร์_ค่า.listen(1); เซิร์ฟเวอร์_ค่า.setblocking(False)
            자신.수신창구들.append(เซิร์ฟเวอร์_ค่า)
        자신.접속자들 = [None, None]
        자신.เทคโนโลยีสารสนเทศ_รอดําเนินการ = [bytearray(), bytearray()]
        자신.อีเทอร์เน็ต = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.เทคโนโลยีสารสนเทศ_ไม่ถูกต้อง = False
        자신.หยุดชั่วคราว_กิจกรรม = threading.Event(); 자신.ข้อผิดพลาด = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.งานเบื้องหลัง = threading.Thread(target=자신.วงกลม_ค่า, daemon=True)
        자신.งานเบื้องหลัง.start()

    def 전달인수(자신):
        พอร์ต_COM_หมายเลข, พอร์ตอีเทอร์เน็ต = [สตริง_ข้อมูล.getsockname()[1] for สตริง_ข้อมูล in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ผู้เยี่ยมชม_อีเมล) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.การถ่ายโอนแฟ้ม_หมายเลขพอร์ต, 자신.ผู้เยี่ยมชม_อีเมล)
        for หมายเลขพอร์ต in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(หมายเลขพอร์ต, 자신.ผู้เยี่ยมชม_อีเมล)
        for 통신규약, โฮสต์, ผู้เยี่ยมชม in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, โฮสต์, 자신.ผู้เยี่ยมชม_อีเมล, ผู้เยี่ยมชม)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.โฮสต์_อีเมล+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(พอร์ต_COM_หมายเลข),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(พอร์ตอีเทอร์เน็ต),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, แพคเก็ต_ข้อมูล):
        자신.เทคโนโลยีสารสนเทศ_รอดําเนินการ[1] += struct.pack('!I', len(แพคเก็ต_ข้อมูล)) + แพคเก็ต_ข้อมูล

    def เทรซ_แพคเก็ต(자신, 방향, แพคเก็ต_ข้อมูล):
        if not 자신.จับ or len(แพคเก็ต_ข้อมูล)<20: return
        ออฟเซต_ค่า=(แพคเก็ต_ข้อมูล[0]&15)*4
        รายการ_ค่า={'time':time.monotonic(),'direction':방향,'bytes':len(แพคเก็ต_ข้อมูล),'protocol':แพคเก็ต_ข้อมูล[9]}
        if แพคเก็ต_ข้อมูล[9]==6 and len(แพคเก็ต_ข้อมูล)>=ออฟเซต_ค่า+20:
            원본자료,ปลายทาง_ข้อมูล_อีเมล,ลําดับ_หมายเลข,확인번호,설정비트,หน้าต่าง=struct.unpack_from('!HHIIHH',แพคเก็ต_ข้อมูล,ออฟเซต_ค่า)
            รายการ_ค่า.update(source=원본자료,destination=ปลายทาง_ข้อมูล_อีเมล,seq=ลําดับ_หมายเลข,ack=확인번호,flags=설정비트&255,window=หน้าต่าง,
                        payload=len(แพคเก็ต_ข้อมูล)-ออฟเซต_ค่า-((แพคเก็ต_ข้อมูล[ออฟเซต_ค่า+12]>>4)*4))
        자신.แฟ้มบันทึกการติดตาม.append(รายการ_ค่า)
        if len(자신.แฟ้มบันทึกการติดตาม)>2048: del 자신.แฟ้มบันทึกการติดตาม[:1024]

    def 직렬전문입력(자신, ข้อมูล):
        for รหัสอักขระ in ข้อมูล:
            if รหัสอักขระ == 192:
                if 자신.직렬전문 and not 자신.เทคโนโลยีสารสนเทศ_ไม่ถูกต้อง and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        อีเมล=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(อีเมล)))
                            자신.ปัจจุบัน_อีเมล=อีเมล
                        except ValueError:
                            pass
                    자신.เทรซ_แพคเก็ต('from_guest',자신.직렬전문)
                    자신.실행틀(เกตเวย์_ฮาร์ดแวร์_อีเมล + เลขที่อยู่จริง + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.เทคโนโลยีสารสนเทศ_ไม่ถูกต้อง = False
            elif รหัสอักขระ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if รหัสอักขระ not in (220, 221): 자신.เทคโนโลยีสารสนเทศ_ไม่ถูกต้อง = True
                    รหัสอักขระ = 192 if รหัสอักขระ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(รหัสอักขระ)
                else: 자신.เทคโนโลยีสารสนเทศ_ไม่ถูกต้อง = True

    def 이더넷입력(자신, ข้อมูล):
        자신.อีเทอร์เน็ต += ข้อมูล
        while len(자신.อีเทอร์เน็ต) >= 4:
            개수 = struct.unpack_from('!I', 자신.อีเทอร์เน็ต)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.อีเทอร์เน็ต) < 개수 + 4: return
            실행틀 = bytes(자신.อีเทอร์เน็ต[4:4+개수]); del 자신.อีเทอร์เน็ต[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                อีเมล_ความละเอียด_แพคเก็ต = 실행틀[14:42]
                if อีเมล_ความละเอียด_แพคเก็ต[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and อีเมล_ความละเอียด_แพคเก็ต[24:28] == 자신.ปัจจุบัน_อีเมล:
                    การตอบ = อีเมล_ความละเอียด_แพคเก็ต[:6] + b'\x00\x02' + เลขที่อยู่จริง + 자신.ปัจจุบัน_อีเมล + อีเมล_ความละเอียด_แพคเก็ต[8:18]
                    자신.실행틀(실행틀[6:12] + เลขที่อยู่จริง + b'\x08\x06' + การตอบ)
            elif 실행틀[12:14] == b'\x08\x00':
                แพคเก็ต_ข้อมูล = 실행틀[14:]
                자신.เทรซ_แพคเก็ต('to_guest',แพคเก็ต_ข้อมูล)
                자신.เทคโนโลยีสารสนเทศ_รอดําเนินการ[0] += b'\xc0' + แพคเก็ต_ข้อมูล.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def วงกลม_ค่า(자신):
        try:
            while not 자신.หยุดชั่วคราว_กิจกรรม.is_set():
                읽기대상들 = [สตริง_ข้อมูล for 순번, สตริง_ข้อมูล in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [สตริง_ข้อมูล for สตริง_ข้อมูล in 자신.접속자들 if สตริง_ข้อมูล is not None]
                쓰기대상들 = [สตริง_ข้อมูล for 순번, สตริง_ข้อมูล in enumerate(자신.접속자들) if สตริง_ข้อมูล is not None and 자신.เทคโนโลยีสารสนเทศ_รอดําเนินการ[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for สตริง_ข้อมูล in 읽을수있음:
                    if สตริง_ข้อมูล in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(สตริง_ข้อมูล); 자신.접속자들[순번], _ = สตริง_ข้อมูล.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(สตริง_ข้อมูล); ข้อมูล = สตริง_ข้อมูล.recv(16384)
                        if not ข้อมูล: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ข้อมูล)
                for สตริง_ข้อมูล in 쓸수있음:
                    순번 = 자신.접속자들.index(สตริง_ข้อมูล)
                    try: 개수 = สตริง_ข้อมูล.send(자신.เทคโนโลยีสารสนเทศ_รอดําเนินการ[순번])
                    except BlockingIOError: continue
                    del 자신.เทคโนโลยีสารสนเทศ_รอดําเนินการ[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.เทคโนโลยีสารสนเทศ_รอดําเนินการ):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.หยุดชั่วคราว_กิจกรรม.is_set(): 자신.ข้อผิดพลาด = str(보조항목)

    def ปิด(자신):
        자신.หยุดชั่วคราว_กิจกรรม.set(); 자신.งานเบื้องหลัง.join(timeout=2)
        for สตริง_ข้อมูล in 자신.수신창구들 + 자신.접속자들:
            if สตริง_ข้อมูล is not None: สตริง_ข้อมูล.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *อาร์กิวเมนต์_อาร์เรย์): 자신.ปิด()
