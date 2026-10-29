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

peiriant_ADDRESS = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
cyfeiriad_rhyngrwyd_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Rhwydwaith_pont:
    def __init__(자신, ffeil_trosglwyddo_rhif_porth=2121, 전달규칙들=(), recordio=False, gwestai_ADDRESS=None, lletya_ADDRESS='127.0.0.1'):
        if not 1024 <= ffeil_trosglwyddo_rhif_porth <= 65535 or 50000 <= ffeil_trosglwyddo_rhif_porth <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ffeil_trosglwyddo_rhif_porth = ffeil_trosglwyddo_rhif_porth
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gwestai_ADDRESS = gwestai_ADDRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gwestai_ADDRESS)
        ADDRESS=ipaddress.IPv4Address(gwestai_ADDRESS)
        자신.gwestai_ADDRESS=str(ADDRESS); 자신.현재주소=ADDRESS.packed
        ADDRESS=ipaddress.IPv4Address(lletya_ADDRESS)
        if ADDRESS.is_multicast or str(ADDRESS)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.lletya_ADDRESS=str(ADDRESS)
        자신.recordio = recordio; 자신.olrhain_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ffeil_trosglwyddo_rhif_porth)} | {('tcp', data_safle) for data_safle in range(50000,50008)}
        for hidlo_VALUE in 전달규칙들:
            llwybr_cydran = hidlo_VALUE.split(':')
            if len(llwybr_cydran) != 3 or llwybr_cydran[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, lletya, gwestai = llwybr_cydran[0], int(llwybr_cydran[1]), int(llwybr_cydran[2])
            if not 1024 <= lletya <= 65535 or not 1 <= gwestai <= 65535 or (통신규약, lletya) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + hidlo_VALUE)
            사용중주소.add((통신규약, lletya)); 자신.전달규칙들.append((통신규약, lletya, gwestai))
        자신.수신창구들 = []
        for _ in range(2):
            gweinydd_VALUE = socket.socket()
            gweinydd_VALUE.bind(('127.0.0.1', 0)); gweinydd_VALUE.listen(1); gweinydd_VALUE.setblocking(False)
            자신.수신창구들.append(gweinydd_VALUE)
        자신.접속자들 = [None, None]
        자신.technoleg_gwybodaeth_yn_disgwyl = [bytearray(), bytearray()]
        자신.Ether_rwyd = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.technoleg_gwybodaeth_annilys = False
        자신.rhewi_digwyddiad = threading.Event(); 자신.Gwall = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Cylch_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, porth_ether_rwyd = [testun_data.getsockname()[1] for testun_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gwestai_ADDRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ffeil_trosglwyddo_rhif_porth, 자신.gwestai_ADDRESS)
        for rhif_porth in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(rhif_porth, 자신.gwestai_ADDRESS)
        for 통신규약, lletya, gwestai in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, lletya, 자신.gwestai_ADDRESS, gwestai)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.lletya_ADDRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(porth_ether_rwyd),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.technoleg_gwybodaeth_yn_disgwyl[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.recordio or len(꾸러미자료)<20: return
        OFFSET_VALUE=(꾸러미자료[0]&15)*4
        cofnod_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=OFFSET_VALUE+20:
            원본자료,cyrchfan_data_ADDRESS,순서번호,확인번호,설정비트,ffenestr=struct.unpack_from('!HHIIHH',꾸러미자료,OFFSET_VALUE)
            cofnod_VALUE.update(source=원본자료,destination=cyrchfan_data_ADDRESS,seq=순서번호,ack=확인번호,flags=설정비트&255,window=ffenestr,
                        payload=len(꾸러미자료)-OFFSET_VALUE-((꾸러미자료[OFFSET_VALUE+12]>>4)*4))
        자신.olrhain_LOG.append(cofnod_VALUE)
        if len(자신.olrhain_LOG)>2048: del 자신.olrhain_LOG[:1024]

    def 직렬전문입력(자신, data):
        for cod_nod in data:
            if cod_nod == 192:
                if 자신.직렬전문 and not 자신.technoleg_gwybodaeth_annilys and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADDRESS=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADDRESS)))
                            자신.현재주소=ADDRESS
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + peiriant_ADDRESS + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.technoleg_gwybodaeth_annilys = False
            elif cod_nod == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if cod_nod not in (220, 221): 자신.technoleg_gwybodaeth_annilys = True
                    cod_nod = 192 if cod_nod == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(cod_nod)
                else: 자신.technoleg_gwybodaeth_annilys = True

    def 이더넷입력(자신, data):
        자신.Ether_rwyd += data
        while len(자신.Ether_rwyd) >= 4:
            eitem_COUNT = struct.unpack_from('!I', 자신.Ether_rwyd)[0]
            if eitem_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ether_rwyd) < eitem_COUNT + 4: return
            실행틀 = bytes(자신.Ether_rwyd[4:4+eitem_COUNT]); del 자신.Ether_rwyd[:4+eitem_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                주소찾기전문 = 실행틀[14:42]
                if 주소찾기전문[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 주소찾기전문[24:28] == 자신.현재주소:
                    응답자료 = 주소찾기전문[:6] + b'\x00\x02' + peiriant_ADDRESS + 자신.현재주소 + 주소찾기전문[8:18]
                    자신.실행틀(실행틀[6:12] + peiriant_ADDRESS + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                꾸러미자료 = 실행틀[14:]
                자신.전문추적('to_guest',꾸러미자료)
                자신.technoleg_gwybodaeth_yn_disgwyl[0] += b'\xc0' + 꾸러미자료.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cylch_VALUE(자신):
        try:
            while not 자신.rhewi_digwyddiad.is_set():
                읽기대상들 = [testun_data for 순번, testun_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [testun_data for testun_data in 자신.접속자들 if testun_data is not None]
                쓰기대상들 = [testun_data for 순번, testun_data in enumerate(자신.접속자들) if testun_data is not None and 자신.technoleg_gwybodaeth_yn_disgwyl[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for testun_data in 읽을수있음:
                    if testun_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(testun_data); 자신.접속자들[순번], _ = testun_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(testun_data); data = testun_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(data)
                for testun_data in 쓸수있음:
                    순번 = 자신.접속자들.index(testun_data)
                    try: eitem_COUNT = testun_data.send(자신.technoleg_gwybodaeth_yn_disgwyl[순번])
                    except BlockingIOError: continue
                    del 자신.technoleg_gwybodaeth_yn_disgwyl[순번][:eitem_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.technoleg_gwybodaeth_yn_disgwyl):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.rhewi_digwyddiad.is_set(): 자신.Gwall = str(보조항목)

    def Cau(자신):
        자신.rhewi_digwyddiad.set(); 자신.작업가닥.join(timeout=2)
        for testun_data in 자신.수신창구들 + 자신.접속자들:
            if testun_data is not None: testun_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *arg_ARAE): 자신.Cau()
