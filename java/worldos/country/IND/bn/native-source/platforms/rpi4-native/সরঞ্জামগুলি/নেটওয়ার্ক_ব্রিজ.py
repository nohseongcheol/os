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

মেশিন_ইমেইল = bytes.fromhex('525400123456')
গেটওয়ে_হার্ডওয়্যার_ইমেইল = bytes.fromhex('52550a000202')
ইন্টারনেট_ঠিকানা_মান = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class নেটওয়ার্ক_ব্রিজ:
    def __init__(자신, ফাইল_স্থানান্তর_পোর্ট_নম্বর=2121, 전달규칙들=(), ক্যাপচার=False, অতিথি_ইমেইল=None, হোস্ট_ইমেইল='127.0.0.1'):
        if not 1024 <= ফাইল_স্থানান্তর_পোর্ট_নম্বর <= 65535 or 50000 <= ফাইল_স্থানান্তর_পোর্ট_নম্বর <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ফাইল_স্থানান্তর_পোর্ট_নম্বর = ফাইল_স্থানান্তর_পোর্ট_নম্বর
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        অতিথি_ইমেইল = অতিথি_ইমেইল or 자신.ip_config['IP']
        qemu_network(자신.ip_config, অতিথি_ইমেইল)
        ইমেইল=ipaddress.IPv4Address(অতিথি_ইমেইল)
        자신.অতিথি_ইমেইল=str(ইমেইল); 자신.현재주소=ইমেইল.packed
        ইমেইল=ipaddress.IPv4Address(হোস্ট_ইমেইল)
        if ইমেইল.is_multicast or str(ইমেইল)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.হোস্ট_ইমেইল=str(ইমেইল)
        자신.ক্যাপচার = ক্যাপচার; 자신.ট্রেস_লগ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ফাইল_স্থানান্তর_পোর্ট_নম্বর)} | {('tcp', ডাটা_পদ) for ডাটা_পদ in range(50000,50008)}
        for নিয়ম_মান in 전달규칙들:
            পথ_অঙ্গ = নিয়ম_মান.split(':')
            if len(পথ_অঙ্গ) != 3 or পথ_অঙ্গ[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, হোস্ট, অতিথি = পথ_অঙ্গ[0], int(পথ_অঙ্গ[1]), int(পথ_অঙ্গ[2])
            if not 1024 <= হোস্ট <= 65535 or not 1 <= অতিথি <= 65535 or (통신규약, হোস্ট) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + নিয়ম_মান)
            사용중주소.add((통신규약, হোস্ট)); 자신.전달규칙들.append((통신규약, হোস্ট, অতিথি))
        자신.수신창구들 = []
        for _ in range(2):
            সার্ভার_মান = socket.socket()
            সার্ভার_মান.bind(('127.0.0.1', 0)); সার্ভার_মান.listen(1); সার্ভার_মান.setblocking(False)
            자신.수신창구들.append(সার্ভার_মান)
        자신.접속자들 = [None, None]
        자신.তথ্য_প্রযুক্তি_মুলতবি = [bytearray(), bytearray()]
        자신.ইথারনেট = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.তথ্য_প্রযুক্তি_অবৈধ = False
        자신.বিরতি_ঘটনা = threading.Event(); 자신.ত্রুটি = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.চক্র_মান, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ইথারনেট_পোর্ট = [স্ট্রিং_ডাটা.getsockname()[1] for স্ট্রিং_ডাটা in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.অতিথি_ইমেইল) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ফাইল_স্থানান্তর_পোর্ট_নম্বর, 자신.অতিথি_ইমেইল)
        for পোর্ট_নম্বর in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(পোর্ট_নম্বর, 자신.অতিথি_ইমেইল)
        for 통신규약, হোস্ট, অতিথি in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, হোস্ট, 자신.অতিথি_ইমেইল, অতিথি)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.হোস্ট_ইমেইল+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ইথারনেট_পোর্ট),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, প্যাকেট_ডাটা):
        자신.তথ্য_প্রযুক্তি_মুলতবি[1] += struct.pack('!I', len(প্যাকেট_ডাটা)) + প্যাকেট_ডাটা

    def ট্রেস_প্যাকেট(자신, 방향, প্যাকেট_ডাটা):
        if not 자신.ক্যাপচার or len(প্যাকেট_ডাটা)<20: return
        অফসেট_মান=(প্যাকেট_ডাটা[0]&15)*4
        ভুক্তি_মান={'time':time.monotonic(),'direction':방향,'bytes':len(প্যাকেট_ডাটা),'protocol':প্যাকেট_ডাটা[9]}
        if প্যাকেট_ডাটা[9]==6 and len(প্যাকেট_ডাটা)>=অফসেট_মান+20:
            원본자료,গন্তব্য_ডাটা_ইমেইল,순서번호,확인번호,বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস,উইন্ডো=struct.unpack_from('!HHIIHH',প্যাকেট_ডাটা,অফসেট_মান)
            ভুক্তি_মান.update(source=원본자료,destination=গন্তব্য_ডাটা_ইমেইল,seq=순서번호,ack=확인번호,flags=বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস&255,window=উইন্ডো,
                        payload=len(প্যাকেট_ডাটা)-অফসেট_মান-((প্যাকেট_ডাটা[অফসেট_মান+12]>>4)*4))
        자신.ট্রেস_লগ.append(ভুক্তি_মান)
        if len(자신.ট্রেস_লগ)>2048: del 자신.ট্রেস_লগ[:1024]

    def 직렬전문입력(자신, ডাটা):
        for অক্ষর_কোড in ডাটা:
            if অক্ষর_কোড == 192:
                if 자신.직렬전문 and not 자신.তথ্য_প্রযুক্তি_অবৈধ and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ইমেইল=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ইমেইল)))
                            자신.현재주소=ইমেইল
                        except ValueError:
                            pass
                    자신.ট্রেস_প্যাকেট('from_guest',자신.직렬전문)
                    자신.실행틀(গেটওয়ে_হার্ডওয়্যার_ইমেইল + মেশিন_ইমেইল + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.তথ্য_প্রযুক্তি_অবৈধ = False
            elif অক্ষর_কোড == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if অক্ষর_কোড not in (220, 221): 자신.তথ্য_প্রযুক্তি_অবৈধ = True
                    অক্ষর_কোড = 192 if অক্ষর_কোড == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(অক্ষর_কোড)
                else: 자신.তথ্য_প্রযুক্তি_অবৈধ = True

    def 이더넷입력(자신, ডাটা):
        자신.ইথারনেট += ডাটা
        while len(자신.ইথারনেট) >= 4:
            개수 = struct.unpack_from('!I', 자신.ইথারনেট)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ইথারনেট) < 개수 + 4: return
            실행틀 = bytes(자신.ইথারনেট[4:4+개수]); del 자신.ইথারনেট[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ইমেইল_রেজোলিউশন_প্যাকেট = 실행틀[14:42]
                if ইমেইল_রেজোলিউশন_প্যাকেট[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ইমেইল_রেজোলিউশন_প্যাকেট[24:28] == 자신.현재주소:
                    응답자료 = ইমেইল_রেজোলিউশন_প্যাকেট[:6] + b'\x00\x02' + মেশিন_ইমেইল + 자신.현재주소 + ইমেইল_রেজোলিউশন_প্যাকেট[8:18]
                    자신.실행틀(실행틀[6:12] + মেশিন_ইমেইল + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                প্যাকেট_ডাটা = 실행틀[14:]
                자신.ট্রেস_প্যাকেট('to_guest',প্যাকেট_ডাটা)
                자신.তথ্য_প্রযুক্তি_মুলতবি[0] += b'\xc0' + প্যাকেট_ডাটা.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def চক্র_মান(자신):
        try:
            while not 자신.বিরতি_ঘটনা.is_set():
                읽기대상들 = [স্ট্রিং_ডাটা for 순번, স্ট্রিং_ডাটা in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [স্ট্রিং_ডাটা for স্ট্রিং_ডাটা in 자신.접속자들 if স্ট্রিং_ডাটা is not None]
                쓰기대상들 = [স্ট্রিং_ডাটা for 순번, স্ট্রিং_ডাটা in enumerate(자신.접속자들) if স্ট্রিং_ডাটা is not None and 자신.তথ্য_প্রযুক্তি_মুলতবি[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for স্ট্রিং_ডাটা in 읽을수있음:
                    if স্ট্রিং_ডাটা in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(স্ট্রিং_ডাটা); 자신.접속자들[순번], _ = স্ট্রিং_ডাটা.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(স্ট্রিং_ডাটা); ডাটা = স্ট্রিং_ডাটা.recv(16384)
                        if not ডাটা: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ডাটা)
                for স্ট্রিং_ডাটা in 쓸수있음:
                    순번 = 자신.접속자들.index(স্ট্রিং_ডাটা)
                    try: 개수 = স্ট্রিং_ডাটা.send(자신.তথ্য_প্রযুক্তি_মুলতবি[순번])
                    except BlockingIOError: continue
                    del 자신.তথ্য_প্রযুক্তি_মুলতবি[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.তথ্য_প্রযুক্তি_মুলতবি):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.বিরতি_ঘটনা.is_set(): 자신.ত্রুটি = str(보조항목)

    def বন্ধ_করুন(자신):
        자신.বিরতি_ঘটনা.set(); 자신.작업가닥.join(timeout=2)
        for স্ট্রিং_ডাটা in 자신.수신창구들 + 자신.접속자들:
            if স্ট্রিং_ডাটা is not None: স্ট্রিং_ডাটা.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *যুক্তি_অ্যারে): 자신.বন্ধ_করুন()
