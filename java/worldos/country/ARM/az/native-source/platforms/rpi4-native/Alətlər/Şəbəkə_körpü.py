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

maşın_ünvan = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
İnternet_ünvanı_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Şəbəkə_körpü:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), çəkmək=False, qonaq_ünvan=None, host_ünvan='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        qonaq_ünvan = qonaq_ünvan or 자신.ip_config['IP']
        qemu_network(자신.ip_config, qonaq_ünvan)
        ünvan=ipaddress.IPv4Address(qonaq_ünvan)
        자신.qonaq_ünvan=str(ünvan); 자신.현재주소=ünvan.packed
        ünvan=ipaddress.IPv4Address(host_ünvan)
        if ünvan.is_multicast or str(ünvan)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.host_ünvan=str(ünvan)
        자신.çəkmək = çəkmək; 자신.iz_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', verilənlər_yerinə_qoymaq) for verilənlər_yerinə_qoymaq in range(50000,50008)}
        for qayda_VALUE in 전달규칙들:
            yol_komponent = qayda_VALUE.split(':')
            if len(yol_komponent) != 3 or yol_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, host, qonaq = yol_komponent[0], int(yol_komponent[1]), int(yol_komponent[2])
            if not 1024 <= host <= 65535 or not 1 <= qonaq <= 65535 or (통신규약, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + qayda_VALUE)
            사용중주소.add((통신규약, host)); 자신.전달규칙들.append((통신규약, host, qonaq))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALUE = socket.socket()
            server_VALUE.bind(('127.0.0.1', 0)); server_VALUE.listen(1); server_VALUE.setblocking(False)
            자신.수신창구들.append(server_VALUE)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.pauza_hadisə = threading.Event(); 자신.XƏTA = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Dövrə_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_ə_qoşma_yuvası = [sətir_verilənlər.getsockname()[1] for sətir_verilənlər in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.qonaq_ünvan) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.qonaq_ünvan)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.qonaq_ünvan)
        for 통신규약, host, qonaq in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, host, 자신.qonaq_ünvan, qonaq)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.host_ünvan+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_ə_qoşma_yuvası),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paket_verilənlər):
        자신.대기중[1] += struct.pack('!I', len(paket_verilənlər)) + paket_verilənlər

    def iz_paket(자신, 방향, paket_verilənlər):
        if not 자신.çəkmək or len(paket_verilənlər)<20: return
        OFFSET_VALUE=(paket_verilənlər[0]&15)*4
        daxiletmə_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paket_verilənlər),'protocol':paket_verilənlər[9]}
        if paket_verilənlər[9]==6 and len(paket_verilənlər)>=OFFSET_VALUE+20:
            원본자료,təyinat_verilənlər_ünvan,순서번호,확인번호,konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti,pəncərə=struct.unpack_from('!HHIIHH',paket_verilənlər,OFFSET_VALUE)
            daxiletmə_VALUE.update(source=원본자료,destination=təyinat_verilənlər_ünvan,seq=순서번호,ack=확인번호,flags=konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&255,window=pəncərə,
                        payload=len(paket_verilənlər)-OFFSET_VALUE-((paket_verilənlər[OFFSET_VALUE+12]>>4)*4))
        자신.iz_LOG.append(daxiletmə_VALUE)
        if len(자신.iz_LOG)>2048: del 자신.iz_LOG[:1024]

    def 직렬전문입력(자신, verilənlər):
        for simvol_kodu in verilənlər:
            if simvol_kodu == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ünvan=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ünvan)))
                            자신.현재주소=ünvan
                        except ValueError:
                            pass
                    자신.iz_paket('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + maşın_ünvan + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif simvol_kodu == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if simvol_kodu not in (220, 221): 자신.잘못됨 = True
                    simvol_kodu = 192 if simvol_kodu == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(simvol_kodu)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, verilənlər):
        자신.Ethernet += verilənlər
        while len(자신.Ethernet) >= 4:
            element_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if element_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < element_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+element_COUNT]); del 자신.Ethernet[:4+element_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ünvan_əksetmə_qabiliyyəti_paket = 실행틀[14:42]
                if ünvan_əksetmə_qabiliyyəti_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ünvan_əksetmə_qabiliyyəti_paket[24:28] == 자신.현재주소:
                    video_münasibət = ünvan_əksetmə_qabiliyyəti_paket[:6] + b'\x00\x02' + maşın_ünvan + 자신.현재주소 + ünvan_əksetmə_qabiliyyəti_paket[8:18]
                    자신.실행틀(실행틀[6:12] + maşın_ünvan + b'\x08\x06' + video_münasibət)
            elif 실행틀[12:14] == b'\x08\x00':
                paket_verilənlər = 실행틀[14:]
                자신.iz_paket('to_guest',paket_verilənlər)
                자신.대기중[0] += b'\xc0' + paket_verilənlər.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Dövrə_VALUE(자신):
        try:
            while not 자신.pauza_hadisə.is_set():
                읽기대상들 = [sətir_verilənlər for 순번, sətir_verilənlər in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [sətir_verilənlər for sətir_verilənlər in 자신.접속자들 if sətir_verilənlər is not None]
                쓰기대상들 = [sətir_verilənlər for 순번, sətir_verilənlər in enumerate(자신.접속자들) if sətir_verilənlər is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for sətir_verilənlər in 읽을수있음:
                    if sətir_verilənlər in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(sətir_verilənlər); 자신.접속자들[순번], _ = sətir_verilənlər.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(sətir_verilənlər); verilənlər = sətir_verilənlər.recv(16384)
                        if not verilənlər: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(verilənlər)
                for sətir_verilənlər in 쓸수있음:
                    순번 = 자신.접속자들.index(sətir_verilənlər)
                    try: element_COUNT = sətir_verilənlər.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:element_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.pauza_hadisə.is_set(): 자신.XƏTA = str(보조항목)

    def Bağla(자신):
        자신.pauza_hadisə.set(); 자신.작업가닥.join(timeout=2)
        for sətir_verilənlər in 자신.수신창구들 + 자신.접속자들:
            if sətir_verilənlər is not None: sətir_verilənlər.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *arqument_ARRAY): 자신.Bağla()
