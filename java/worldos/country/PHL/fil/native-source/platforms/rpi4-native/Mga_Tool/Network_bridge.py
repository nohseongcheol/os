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

machine_email = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Internet_address_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Network_bridge:
    def __init__(자신, file_lipat_numero_ng_port=2121, 전달규칙들=(), mag_capture=False, bisita_email=None, host_email='127.0.0.1'):
        if not 1024 <= file_lipat_numero_ng_port <= 65535 or 50000 <= file_lipat_numero_ng_port <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.file_lipat_numero_ng_port = file_lipat_numero_ng_port
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        bisita_email = bisita_email or 자신.ip_config['IP']
        qemu_network(자신.ip_config, bisita_email)
        email=ipaddress.IPv4Address(bisita_email)
        자신.bisita_email=str(email); 자신.현재주소=email.packed
        email=ipaddress.IPv4Address(host_email)
        if email.is_multicast or str(email)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.host_email=str(email)
        자신.mag_capture = mag_capture; 자신.trace_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', file_lipat_numero_ng_port)} | {('tcp', data_posisyon) for data_posisyon in range(50000,50008)}
        for filter_VALUE in 전달규칙들:
            path_component = filter_VALUE.split(':')
            if len(path_component) != 3 or path_component[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, host, bisita = path_component[0], int(path_component[1]), int(path_component[2])
            if not 1024 <= host <= 65535 or not 1 <= bisita <= 65535 or (통신규약, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filter_VALUE)
            사용중주소.add((통신규약, host)); 자신.전달규칙들.append((통신규약, host, bisita))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALUE = socket.socket()
            server_VALUE.bind(('127.0.0.1', 0)); server_VALUE.listen(1); server_VALUE.setblocking(False)
            자신.수신창구들.append(server_VALUE)
        자신.접속자들 = [None, None]
        자신.information_technology_pending = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.information_technology_hindi_tama = False
        자신.panadaliang_ihinto_kaganapan = threading.Event(); 자신.error = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Cycle_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_port = [string_data.getsockname()[1] for string_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.bisita_email) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.file_lipat_numero_ng_port, 자신.bisita_email)
        for numero_ng_port in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(numero_ng_port, 자신.bisita_email)
        for 통신규약, host, bisita in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, host, 자신.bisita_email, bisita)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.host_email+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, packet_data):
        자신.information_technology_pending[1] += struct.pack('!I', len(packet_data)) + packet_data

    def trace_packet(자신, 방향, packet_data):
        if not 자신.mag_capture or len(packet_data)<20: return
        OFFSET_VALUE=(packet_data[0]&15)*4
        pagpasok_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(packet_data),'protocol':packet_data[9]}
        if packet_data[9]==6 and len(packet_data)>=OFFSET_VALUE+20:
            원본자료,patutunguhan_data_email,순서번호,확인번호,kompigurasyon_Background_Intelligent_Transfer_Service,window=struct.unpack_from('!HHIIHH',packet_data,OFFSET_VALUE)
            pagpasok_VALUE.update(source=원본자료,destination=patutunguhan_data_email,seq=순서번호,ack=확인번호,flags=kompigurasyon_Background_Intelligent_Transfer_Service&255,window=window,
                        payload=len(packet_data)-OFFSET_VALUE-((packet_data[OFFSET_VALUE+12]>>4)*4))
        자신.trace_LOG.append(pagpasok_VALUE)
        if len(자신.trace_LOG)>2048: del 자신.trace_LOG[:1024]

    def 직렬전문입력(자신, data):
        for character_code in data:
            if character_code == 192:
                if 자신.직렬전문 and not 자신.information_technology_hindi_tama and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        email=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(email)))
                            자신.현재주소=email
                        except ValueError:
                            pass
                    자신.trace_packet('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + machine_email + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.information_technology_hindi_tama = False
            elif character_code == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if character_code not in (220, 221): 자신.information_technology_hindi_tama = True
                    character_code = 192 if character_code == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(character_code)
                else: 자신.information_technology_hindi_tama = True

    def 이더넷입력(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            item_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if item_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < item_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+item_COUNT]); del 자신.Ethernet[:4+item_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                email_resolution_packet = 실행틀[14:42]
                if email_resolution_packet[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and email_resolution_packet[24:28] == 자신.현재주소:
                    응답자료 = email_resolution_packet[:6] + b'\x00\x02' + machine_email + 자신.현재주소 + email_resolution_packet[8:18]
                    자신.실행틀(실행틀[6:12] + machine_email + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                packet_data = 실행틀[14:]
                자신.trace_packet('to_guest',packet_data)
                자신.information_technology_pending[0] += b'\xc0' + packet_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cycle_VALUE(자신):
        try:
            while not 자신.panadaliang_ihinto_kaganapan.is_set():
                읽기대상들 = [string_data for 순번, string_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [string_data for string_data in 자신.접속자들 if string_data is not None]
                쓰기대상들 = [string_data for 순번, string_data in enumerate(자신.접속자들) if string_data is not None and 자신.information_technology_pending[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for string_data in 읽을수있음:
                    if string_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(string_data); 자신.접속자들[순번], _ = string_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(string_data); data = string_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(data)
                for string_data in 쓸수있음:
                    순번 = 자신.접속자들.index(string_data)
                    try: item_COUNT = string_data.send(자신.information_technology_pending[순번])
                    except BlockingIOError: continue
                    del 자신.information_technology_pending[순번][:item_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.information_technology_pending):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.panadaliang_ihinto_kaganapan.is_set(): 자신.error = str(보조항목)

    def isara(자신):
        자신.panadaliang_ihinto_kaganapan.set(); 자신.작업가닥.join(timeout=2)
        for string_data in 자신.수신창구들 + 자신.접속자들:
            if string_data is not None: string_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumento_ARRAY): 자신.isara()
