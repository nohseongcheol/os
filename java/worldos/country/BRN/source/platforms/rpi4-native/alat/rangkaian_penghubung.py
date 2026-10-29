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

mesin_e_mel = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
alamat_Internet_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class rangkaian_penghubung:
    def __init__(자신, pemindahan_fail_nombor_port=2121, 전달규칙들=(), rakam=False, tetamu_e_mel=None, hos_e_mel='127.0.0.1'):
        if not 1024 <= pemindahan_fail_nombor_port <= 65535 or 50000 <= pemindahan_fail_nombor_port <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.pemindahan_fail_nombor_port = pemindahan_fail_nombor_port
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        tetamu_e_mel = tetamu_e_mel or 자신.ip_config['IP']
        qemu_network(자신.ip_config, tetamu_e_mel)
        e_mel=ipaddress.IPv4Address(tetamu_e_mel)
        자신.tetamu_e_mel=str(e_mel); 자신.현재주소=e_mel.packed
        e_mel=ipaddress.IPv4Address(hos_e_mel)
        if e_mel.is_multicast or str(e_mel)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.hos_e_mel=str(e_mel)
        자신.rakam = rakam; 자신.jejak_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', pemindahan_fail_nombor_port)} | {('tcp', data_jawatan) for data_jawatan in range(50000,50008)}
        for penapis_VALUE in 전달규칙들:
            laluan_komponen = penapis_VALUE.split(':')
            if len(laluan_komponen) != 3 or laluan_komponen[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, hos, tetamu = laluan_komponen[0], int(laluan_komponen[1]), int(laluan_komponen[2])
            if not 1024 <= hos <= 65535 or not 1 <= tetamu <= 65535 or (통신규약, hos) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + penapis_VALUE)
            사용중주소.add((통신규약, hos)); 자신.전달규칙들.append((통신규약, hos, tetamu))
        자신.수신창구들 = []
        for _ in range(2):
            pelayan_VALUE = socket.socket()
            pelayan_VALUE.bind(('127.0.0.1', 0)); pelayan_VALUE.listen(1); pelayan_VALUE.setblocking(False)
            자신.수신창구들.append(pelayan_VALUE)
        자신.접속자들 = [None, None]
        자신.teknologi_maklumat_belum_selesai = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.teknologi_maklumat_tak_sah = False
        자신.Jeda_acara = threading.Event(); 자신.RALAT = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Kitaran_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, port_Ethernet = [rentetan_data.getsockname()[1] for rentetan_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.tetamu_e_mel) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.pemindahan_fail_nombor_port, 자신.tetamu_e_mel)
        for nombor_port in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(nombor_port, 자신.tetamu_e_mel)
        for 통신규약, hos, tetamu in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, hos, 자신.tetamu_e_mel, tetamu)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.hos_e_mel+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(port_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paket_data):
        자신.teknologi_maklumat_belum_selesai[1] += struct.pack('!I', len(paket_data)) + paket_data

    def jejak_paket(자신, 방향, paket_data):
        if not 자신.rakam or len(paket_data)<20: return
        Ofset_VALUE=(paket_data[0]&15)*4
        pemasukan_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paket_data),'protocol':paket_data[9]}
        if paket_data[9]==6 and len(paket_data)>=Ofset_VALUE+20:
            원본자료,destinasi_data_e_mel,순서번호,확인번호,konfigurasi_Background_Intelligent_Transfer_Service,Tetingkap=struct.unpack_from('!HHIIHH',paket_data,Ofset_VALUE)
            pemasukan_VALUE.update(source=원본자료,destination=destinasi_data_e_mel,seq=순서번호,ack=확인번호,flags=konfigurasi_Background_Intelligent_Transfer_Service&255,window=Tetingkap,
                        payload=len(paket_data)-Ofset_VALUE-((paket_data[Ofset_VALUE+12]>>4)*4))
        자신.jejak_LOG.append(pemasukan_VALUE)
        if len(자신.jejak_LOG)>2048: del 자신.jejak_LOG[:1024]

    def 직렬전문입력(자신, data):
        for titik_kod in data:
            if titik_kod == 192:
                if 자신.직렬전문 and not 자신.teknologi_maklumat_tak_sah and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        e_mel=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(e_mel)))
                            자신.현재주소=e_mel
                        except ValueError:
                            pass
                    자신.jejak_paket('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + mesin_e_mel + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.teknologi_maklumat_tak_sah = False
            elif titik_kod == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if titik_kod not in (220, 221): 자신.teknologi_maklumat_tak_sah = True
                    titik_kod = 192 if titik_kod == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(titik_kod)
                else: 자신.teknologi_maklumat_tak_sah = True

    def 이더넷입력(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            item_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if item_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < item_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+item_COUNT]); del 자신.Ethernet[:4+item_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                e_mel_resolusi_paket = 실행틀[14:42]
                if e_mel_resolusi_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and e_mel_resolusi_paket[24:28] == 자신.현재주소:
                    respons = e_mel_resolusi_paket[:6] + b'\x00\x02' + mesin_e_mel + 자신.현재주소 + e_mel_resolusi_paket[8:18]
                    자신.실행틀(실행틀[6:12] + mesin_e_mel + b'\x08\x06' + respons)
            elif 실행틀[12:14] == b'\x08\x00':
                paket_data = 실행틀[14:]
                자신.jejak_paket('to_guest',paket_data)
                자신.teknologi_maklumat_belum_selesai[0] += b'\xc0' + paket_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Kitaran_VALUE(자신):
        try:
            while not 자신.Jeda_acara.is_set():
                읽기대상들 = [rentetan_data for 순번, rentetan_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [rentetan_data for rentetan_data in 자신.접속자들 if rentetan_data is not None]
                쓰기대상들 = [rentetan_data for 순번, rentetan_data in enumerate(자신.접속자들) if rentetan_data is not None and 자신.teknologi_maklumat_belum_selesai[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for rentetan_data in 읽을수있음:
                    if rentetan_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(rentetan_data); 자신.접속자들[순번], _ = rentetan_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(rentetan_data); data = rentetan_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(data)
                for rentetan_data in 쓸수있음:
                    순번 = 자신.접속자들.index(rentetan_data)
                    try: item_COUNT = rentetan_data.send(자신.teknologi_maklumat_belum_selesai[순번])
                    except BlockingIOError: continue
                    del 자신.teknologi_maklumat_belum_selesai[순번][:item_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.teknologi_maklumat_belum_selesai):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Jeda_acara.is_set(): 자신.RALAT = str(보조항목)

    def Tutup(자신):
        자신.Jeda_acara.set(); 자신.작업가닥.join(timeout=2)
        for rentetan_data in 자신.수신창구들 + 자신.접속자들:
            if rentetan_data is not None: rentetan_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumen_ARRAY): 자신.Tutup()
