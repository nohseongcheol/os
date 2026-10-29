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

இயந்திரம்_முகவரி = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
இணைய_முகவரி_மதிப்பு = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class பிணையம்_பிரிட்ஜ்:
    def __init__(자신, கோப்பு_இடமாற்று_முனைய_எண்=2121, 전달규칙들=(), பிடிப்பு=False, விருந்தினர்_முகவரி=None, ஓம்பு_முகவரி='127.0.0.1'):
        if not 1024 <= கோப்பு_இடமாற்று_முனைய_எண் <= 65535 or 50000 <= கோப்பு_இடமாற்று_முனைய_எண் <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.கோப்பு_இடமாற்று_முனைய_எண் = கோப்பு_இடமாற்று_முனைய_எண்
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        விருந்தினர்_முகவரி = விருந்தினர்_முகவரி or 자신.ip_config['IP']
        qemu_network(자신.ip_config, விருந்தினர்_முகவரி)
        முகவரி=ipaddress.IPv4Address(விருந்தினர்_முகவரி)
        자신.விருந்தினர்_முகவரி=str(முகவரி); 자신.현재주소=முகவரி.packed
        முகவரி=ipaddress.IPv4Address(ஓம்பு_முகவரி)
        if முகவரி.is_multicast or str(முகவரி)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ஓம்பு_முகவரி=str(முகவரி)
        자신.பிடிப்பு = பிடிப்பு; 자신.சுவடு_பதிவு = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', கோப்பு_இடமாற்று_முனைய_எண்)} | {('tcp', தரவு_நிலை) for தரவு_நிலை in range(50000,50008)}
        for விதி_மதிப்பு in 전달규칙들:
            பாதை_உபகரணம் = விதி_மதிப்பு.split(':')
            if len(பாதை_உபகரணம்) != 3 or பாதை_உபகரணம்[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ஓம்பு, விருந்தினர் = பாதை_உபகரணம்[0], int(பாதை_உபகரணம்[1]), int(பாதை_உபகரணம்[2])
            if not 1024 <= ஓம்பு <= 65535 or not 1 <= விருந்தினர் <= 65535 or (통신규약, ஓம்பு) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + விதி_மதிப்பு)
            사용중주소.add((통신규약, ஓம்பு)); 자신.전달규칙들.append((통신규약, ஓம்பு, விருந்தினர்))
        자신.수신창구들 = []
        for _ in range(2):
            சேவையகம்_மதிப்பு = socket.socket()
            சேவையகம்_மதிப்பு.bind(('127.0.0.1', 0)); சேவையகம்_மதிப்பு.listen(1); சேவையகம்_மதிப்பு.setblocking(False)
            자신.수신창구들.append(சேவையகம்_மதிப்பு)
        자신.접속자들 = [None, None]
        자신.தகவல்_தொழில்நுட்பம்_நிலுவையில்_உள்ளவை = [bytearray(), bytearray()]
        자신.ஈத்தர்நெட் = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.தகவல்_தொழில்நுட்பம்_செல்லுபடியாகாத = False
        자신.நிற்க_நிகழ்வு = threading.Event(); 자신.பிழை = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.சுற்று_மதிப்பு, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ஈத்தர்நெட்_முணையம் = [சரம்_தரவு.getsockname()[1] for சரம்_தரவு in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.விருந்தினர்_முகவரி) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.கோப்பு_இடமாற்று_முனைய_எண், 자신.விருந்தினர்_முகவரி)
        for முனைய_எண் in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(முனைய_எண், 자신.விருந்தினர்_முகவரி)
        for 통신규약, ஓம்பு, விருந்தினர் in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ஓம்பு, 자신.விருந்தினர்_முகவரி, விருந்தினர்)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ஓம்பு_முகவரி+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ஈத்தர்நெட்_முணையம்),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, பாக்கெட்_தரவு):
        자신.தகவல்_தொழில்நுட்பம்_நிலுவையில்_உள்ளவை[1] += struct.pack('!I', len(பாக்கெட்_தரவு)) + பாக்கெட்_தரவு

    def சுவடு_பாக்கெட்(자신, 방향, பாக்கெட்_தரவு):
        if not 자신.பிடிப்பு or len(பாக்கெட்_தரவு)<20: return
        ஆஃப்செட்_மதிப்பு=(பாக்கெட்_தரவு[0]&15)*4
        உள்ளீடு_மதிப்பு={'time':time.monotonic(),'direction':방향,'bytes':len(பாக்கெட்_தரவு),'protocol':பாக்கெட்_தரவு[9]}
        if பாக்கெட்_தரவு[9]==6 and len(பாக்கெட்_தரவு)>=ஆஃப்செட்_மதிப்பு+20:
            원본자료,இலக்கு_தரவு_முகவரி,순서번호,확인번호,உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை,சாளரம்=struct.unpack_from('!HHIIHH',பாக்கெட்_தரவு,ஆஃப்செட்_மதிப்பு)
            உள்ளீடு_மதிப்பு.update(source=원본자료,destination=இலக்கு_தரவு_முகவரி,seq=순서번호,ack=확인번호,flags=உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை&255,window=சாளரம்,
                        payload=len(பாக்கெட்_தரவு)-ஆஃப்செட்_மதிப்பு-((பாக்கெட்_தரவு[ஆஃப்செட்_மதிப்பு+12]>>4)*4))
        자신.சுவடு_பதிவு.append(உள்ளீடு_மதிப்பு)
        if len(자신.சுவடு_பதிவு)>2048: del 자신.சுவடு_பதிவு[:1024]

    def 직렬전문입력(자신, தரவு):
        for எழுத்துக்குறி_குறியீடு in தரவு:
            if எழுத்துக்குறி_குறியீடு == 192:
                if 자신.직렬전문 and not 자신.தகவல்_தொழில்நுட்பம்_செல்லுபடியாகாத and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        முகவரி=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(முகவரி)))
                            자신.현재주소=முகவரி
                        except ValueError:
                            pass
                    자신.சுவடு_பாக்கெட்('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + இயந்திரம்_முகவரி + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.தகவல்_தொழில்நுட்பம்_செல்லுபடியாகாத = False
            elif எழுத்துக்குறி_குறியீடு == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if எழுத்துக்குறி_குறியீடு not in (220, 221): 자신.தகவல்_தொழில்நுட்பம்_செல்லுபடியாகாத = True
                    எழுத்துக்குறி_குறியீடு = 192 if எழுத்துக்குறி_குறியீடு == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(எழுத்துக்குறி_குறியீடு)
                else: 자신.தகவல்_தொழில்நுட்பம்_செல்லுபடியாகாத = True

    def 이더넷입력(자신, தரவு):
        자신.ஈத்தர்நெட் += தரவு
        while len(자신.ஈத்தர்நெட்) >= 4:
            개수 = struct.unpack_from('!I', 자신.ஈத்தர்நெட்)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ஈத்தர்நெட்) < 개수 + 4: return
            실행틀 = bytes(자신.ஈத்தர்நெட்[4:4+개수]); del 자신.ஈத்தர்நெட்[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                முகவரி_தெளிவுத்திறன்_பாக்கெட் = 실행틀[14:42]
                if முகவரி_தெளிவுத்திறன்_பாக்கெட்[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and முகவரி_தெளிவுத்திறன்_பாக்கெட்[24:28] == 자신.현재주소:
                    응답자료 = முகவரி_தெளிவுத்திறன்_பாக்கெட்[:6] + b'\x00\x02' + இயந்திரம்_முகவரி + 자신.현재주소 + முகவரி_தெளிவுத்திறன்_பாக்கெட்[8:18]
                    자신.실행틀(실행틀[6:12] + இயந்திரம்_முகவரி + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                பாக்கெட்_தரவு = 실행틀[14:]
                자신.சுவடு_பாக்கெட்('to_guest',பாக்கெட்_தரவு)
                자신.தகவல்_தொழில்நுட்பம்_நிலுவையில்_உள்ளவை[0] += b'\xc0' + பாக்கெட்_தரவு.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def சுற்று_மதிப்பு(자신):
        try:
            while not 자신.நிற்க_நிகழ்வு.is_set():
                읽기대상들 = [சரம்_தரவு for 순번, சரம்_தரவு in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [சரம்_தரவு for சரம்_தரவு in 자신.접속자들 if சரம்_தரவு is not None]
                쓰기대상들 = [சரம்_தரவு for 순번, சரம்_தரவு in enumerate(자신.접속자들) if சரம்_தரவு is not None and 자신.தகவல்_தொழில்நுட்பம்_நிலுவையில்_உள்ளவை[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for சரம்_தரவு in 읽을수있음:
                    if சரம்_தரவு in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(சரம்_தரவு); 자신.접속자들[순번], _ = சரம்_தரவு.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(சரம்_தரவு); தரவு = சரம்_தரவு.recv(16384)
                        if not தரவு: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(தரவு)
                for சரம்_தரவு in 쓸수있음:
                    순번 = 자신.접속자들.index(சரம்_தரவு)
                    try: 개수 = சரம்_தரவு.send(자신.தகவல்_தொழில்நுட்பம்_நிலுவையில்_உள்ளவை[순번])
                    except BlockingIOError: continue
                    del 자신.தகவல்_தொழில்நுட்பம்_நிலுவையில்_உள்ளவை[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.தகவல்_தொழில்நுட்பம்_நிலுவையில்_உள்ளவை):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.நிற்க_நிகழ்வு.is_set(): 자신.பிழை = str(보조항목)

    def மூடு(자신):
        자신.நிற்க_நிகழ்வு.set(); 자신.작업가닥.join(timeout=2)
        for சரம்_தரவு in 자신.수신창구들 + 자신.접속자들:
            if சரம்_தரவு is not None: சரம்_தரவு.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *மதிப்புரு_கோவை): 자신.மூடு()
