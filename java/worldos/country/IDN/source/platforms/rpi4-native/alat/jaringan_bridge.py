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

mesin_surel = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Alamat_internet_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class jaringan_bridge:
    def __init__(자신, transfer_file_nomor_port=2121, 전달규칙들=(), ambil=False, tamu_surel=None, host_surel='127.0.0.1'):
        if not 1024 <= transfer_file_nomor_port <= 65535 or 50000 <= transfer_file_nomor_port <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.transfer_file_nomor_port = transfer_file_nomor_port
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        tamu_surel = tamu_surel or 자신.ip_config['IP']
        qemu_network(자신.ip_config, tamu_surel)
        surel=ipaddress.IPv4Address(tamu_surel)
        자신.tamu_surel=str(surel); 자신.saat_ini_surel=surel.packed
        surel=ipaddress.IPv4Address(host_surel)
        if surel.is_multicast or str(surel)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.host_surel=str(surel)
        자신.ambil = ambil; 자신.log_jejak = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', transfer_file_nomor_port)} | {('tcp', data_posisi) for data_posisi in range(50000,50008)}
        for aturan_VALUE in 전달규칙들:
            jalur_komponen = aturan_VALUE.split(':')
            if len(jalur_komponen) != 3 or jalur_komponen[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, host, tamu = jalur_komponen[0], int(jalur_komponen[1]), int(jalur_komponen[2])
            if not 1024 <= host <= 65535 or not 1 <= tamu <= 65535 or (통신규약, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + aturan_VALUE)
            사용중주소.add((통신규약, host)); 자신.전달규칙들.append((통신규약, host, tamu))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALUE = socket.socket()
            server_VALUE.bind(('127.0.0.1', 0)); server_VALUE.listen(1); server_VALUE.setblocking(False)
            자신.수신창구들.append(server_VALUE)
        자신.접속자들 = [None, None]
        자신.teknologi_informasi_sedang_diproses = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.teknologi_informasi_tidak_sahih = False
        자신.Jeda_acara = threading.Event(); 자신.galat = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.tugasLatar = threading.Thread(target=자신.Siklus_VALUE, daemon=True)
        자신.tugasLatar.start()

    def 전달인수(자신):
        직렬접속번호, port_Ethernet = [string_data.getsockname()[1] for string_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.tamu_surel) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.transfer_file_nomor_port, 자신.tamu_surel)
        for nomor_port in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(nomor_port, 자신.tamu_surel)
        for 통신규약, host, tamu in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, host, 자신.tamu_surel, tamu)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.host_surel+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(port_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paket_data):
        자신.teknologi_informasi_sedang_diproses[1] += struct.pack('!I', len(paket_data)) + paket_data

    def trace_paket(자신, 방향, paket_data):
        if not 자신.ambil or len(paket_data)<20: return
        OFFSET_VALUE=(paket_data[0]&15)*4
        entri_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paket_data),'protocol':paket_data[9]}
        if paket_data[9]==6 and len(paket_data)>=OFFSET_VALUE+20:
            원본자료,tujuan_data_surel,순서번호,확인번호,konfigurasi_Background_Intelligent_Transfer_Service,Jendela=struct.unpack_from('!HHIIHH',paket_data,OFFSET_VALUE)
            entri_VALUE.update(source=원본자료,destination=tujuan_data_surel,seq=순서번호,ack=확인번호,flags=konfigurasi_Background_Intelligent_Transfer_Service&255,window=Jendela,
                        payload=len(paket_data)-OFFSET_VALUE-((paket_data[OFFSET_VALUE+12]>>4)*4))
        자신.log_jejak.append(entri_VALUE)
        if len(자신.log_jejak)>2048: del 자신.log_jejak[:1024]

    def 직렬전문입력(자신, data):
        for kode_karakter in data:
            if kode_karakter == 192:
                if 자신.직렬전문 and not 자신.teknologi_informasi_tidak_sahih and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        surel=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(surel)))
                            자신.saat_ini_surel=surel
                        except ValueError:
                            pass
                    자신.trace_paket('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + mesin_surel + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.teknologi_informasi_tidak_sahih = False
            elif kode_karakter == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if kode_karakter not in (220, 221): 자신.teknologi_informasi_tidak_sahih = True
                    kode_karakter = 192 if kode_karakter == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(kode_karakter)
                else: 자신.teknologi_informasi_tidak_sahih = True

    def 이더넷입력(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            item_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if item_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < item_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+item_COUNT]); del 자신.Ethernet[:4+item_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                surel_resolusi_paket = 실행틀[14:42]
                if surel_resolusi_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and surel_resolusi_paket[24:28] == 자신.saat_ini_surel:
                    respons = surel_resolusi_paket[:6] + b'\x00\x02' + mesin_surel + 자신.saat_ini_surel + surel_resolusi_paket[8:18]
                    자신.실행틀(실행틀[6:12] + mesin_surel + b'\x08\x06' + respons)
            elif 실행틀[12:14] == b'\x08\x00':
                paket_data = 실행틀[14:]
                자신.trace_paket('to_guest',paket_data)
                자신.teknologi_informasi_sedang_diproses[0] += b'\xc0' + paket_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Siklus_VALUE(자신):
        try:
            while not 자신.Jeda_acara.is_set():
                읽기대상들 = [string_data for 순번, string_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [string_data for string_data in 자신.접속자들 if string_data is not None]
                쓰기대상들 = [string_data for 순번, string_data in enumerate(자신.접속자들) if string_data is not None and 자신.teknologi_informasi_sedang_diproses[순번]]
                읽을수있음, bisa_tulis, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for string_data in 읽을수있음:
                    if string_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(string_data); 자신.접속자들[순번], _ = string_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(string_data); data = string_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(data)
                for string_data in bisa_tulis:
                    순번 = 자신.접속자들.index(string_data)
                    try: item_COUNT = string_data.send(자신.teknologi_informasi_sedang_diproses[순번])
                    except BlockingIOError: continue
                    del 자신.teknologi_informasi_sedang_diproses[순번][:item_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.teknologi_informasi_sedang_diproses):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Jeda_acara.is_set(): 자신.galat = str(보조항목)

    def Tutup(자신):
        자신.Jeda_acara.set(); 자신.tugasLatar.join(timeout=2)
        for string_data in 자신.수신창구들 + 자신.접속자들:
            if string_data is not None: string_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumen_ARRAY): 자신.Tutup()
