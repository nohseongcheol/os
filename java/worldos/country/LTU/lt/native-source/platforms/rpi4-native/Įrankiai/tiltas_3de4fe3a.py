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

absoliutusis_adresas = bytes.fromhex('525400123456')
šliuzas_aparatūra_ADDRESS = bytes.fromhex('52550a000202')
interneto_adresas_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class tiltas_3de4fe3a:
    def __init__(자신, failo_perdavimas_prievado_numeris=2121, 전달규칙들=(), įrašyti=False, svečias_ADDRESS=None, organizuoti_ADDRESS='127.0.0.1'):
        if not 1024 <= failo_perdavimas_prievado_numeris <= 65535 or 50000 <= failo_perdavimas_prievado_numeris <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.failo_perdavimas_prievado_numeris = failo_perdavimas_prievado_numeris
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        svečias_ADDRESS = svečias_ADDRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, svečias_ADDRESS)
        ADDRESS=ipaddress.IPv4Address(svečias_ADDRESS)
        자신.svečias_ADDRESS=str(ADDRESS); 자신.dabartinis_ADDRESS=ADDRESS.packed
        ADDRESS=ipaddress.IPv4Address(organizuoti_ADDRESS)
        if ADDRESS.is_multicast or str(ADDRESS)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.organizuoti_ADDRESS=str(ADDRESS)
        자신.įrašyti = įrašyti; 자신.sekimo_žurnalas = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', failo_perdavimas_prievado_numeris)} | {('tcp', duomenys_padėtis) for duomenys_padėtis in range(50000,50008)}
        for filtras_VALUE in 전달규칙들:
            kelias_komponentas = filtras_VALUE.split(':')
            if len(kelias_komponentas) != 3 or kelias_komponentas[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, organizuoti, svečias = kelias_komponentas[0], int(kelias_komponentas[1]), int(kelias_komponentas[2])
            if not 1024 <= organizuoti <= 65535 or not 1 <= svečias <= 65535 or (통신규약, organizuoti) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filtras_VALUE)
            사용중주소.add((통신규약, organizuoti)); 자신.전달규칙들.append((통신규약, organizuoti, svečias))
        자신.수신창구들 = []
        for _ in range(2):
            serveris_VALUE = socket.socket()
            serveris_VALUE.bind(('127.0.0.1', 0)); serveris_VALUE.listen(1); serveris_VALUE.setblocking(False)
            자신.수신창구들.append(serveris_VALUE)
        자신.접속자들 = [None, None]
        자신.informacinės_technologijos_laukiama = [bytearray(), bytearray()]
        자신.eternetas = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informacinės_technologijos_neleistinas = False
        자신.Pauzė_įvykis = threading.Event(); 자신.KLAIDA = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.darbininkas = threading.Thread(target=자신.Ciklas_VALUE, daemon=True)
        자신.darbininkas.start()

    def 전달인수(자신):
        COM_prievadas_numeris, eterneto_prievadas = [eilutė_duomenys.getsockname()[1] for eilutė_duomenys in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.svečias_ADDRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.failo_perdavimas_prievado_numeris, 자신.svečias_ADDRESS)
        for prievado_numeris in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(prievado_numeris, 자신.svečias_ADDRESS)
        for 통신규약, organizuoti, svečias in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, organizuoti, 자신.svečias_ADDRESS, svečias)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.organizuoti_ADDRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_prievadas_numeris),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(eterneto_prievadas),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paketas_duomenys):
        자신.informacinės_technologijos_laukiama[1] += struct.pack('!I', len(paketas_duomenys)) + paketas_duomenys

    def sekti_paketas(자신, 방향, paketas_duomenys):
        if not 자신.įrašyti or len(paketas_duomenys)<20: return
        OFFSET_VALUE=(paketas_duomenys[0]&15)*4
        įrašas_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paketas_duomenys),'protocol':paketas_duomenys[9]}
        if paketas_duomenys[9]==6 and len(paketas_duomenys)>=OFFSET_VALUE+20:
            원본자료,vieta_duomenys_ADDRESS,tvarka_numeris,확인번호,konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba,Langas=struct.unpack_from('!HHIIHH',paketas_duomenys,OFFSET_VALUE)
            įrašas_VALUE.update(source=원본자료,destination=vieta_duomenys_ADDRESS,seq=tvarka_numeris,ack=확인번호,flags=konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&255,window=Langas,
                        payload=len(paketas_duomenys)-OFFSET_VALUE-((paketas_duomenys[OFFSET_VALUE+12]>>4)*4))
        자신.sekimo_žurnalas.append(įrašas_VALUE)
        if len(자신.sekimo_žurnalas)>2048: del 자신.sekimo_žurnalas[:1024]

    def 직렬전문입력(자신, duomenys):
        for simbolio_kodas in duomenys:
            if simbolio_kodas == 192:
                if 자신.직렬전문 and not 자신.informacinės_technologijos_neleistinas and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADDRESS=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADDRESS)))
                            자신.dabartinis_ADDRESS=ADDRESS
                        except ValueError:
                            pass
                    자신.sekti_paketas('from_guest',자신.직렬전문)
                    자신.실행틀(šliuzas_aparatūra_ADDRESS + absoliutusis_adresas + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informacinės_technologijos_neleistinas = False
            elif simbolio_kodas == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if simbolio_kodas not in (220, 221): 자신.informacinės_technologijos_neleistinas = True
                    simbolio_kodas = 192 if simbolio_kodas == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(simbolio_kodas)
                else: 자신.informacinės_technologijos_neleistinas = True

    def 이더넷입력(자신, duomenys):
        자신.eternetas += duomenys
        while len(자신.eternetas) >= 4:
            prekė_COUNT = struct.unpack_from('!I', 자신.eternetas)[0]
            if prekė_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.eternetas) < prekė_COUNT + 4: return
            실행틀 = bytes(자신.eternetas[4:4+prekė_COUNT]); del 자신.eternetas[:4+prekė_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ADDRESS_skiriamoji_geba_paketas = 실행틀[14:42]
                if ADDRESS_skiriamoji_geba_paketas[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADDRESS_skiriamoji_geba_paketas[24:28] == 자신.dabartinis_ADDRESS:
                    atsakas = ADDRESS_skiriamoji_geba_paketas[:6] + b'\x00\x02' + absoliutusis_adresas + 자신.dabartinis_ADDRESS + ADDRESS_skiriamoji_geba_paketas[8:18]
                    자신.실행틀(실행틀[6:12] + absoliutusis_adresas + b'\x08\x06' + atsakas)
            elif 실행틀[12:14] == b'\x08\x00':
                paketas_duomenys = 실행틀[14:]
                자신.sekti_paketas('to_guest',paketas_duomenys)
                자신.informacinės_technologijos_laukiama[0] += b'\xc0' + paketas_duomenys.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Ciklas_VALUE(자신):
        try:
            while not 자신.Pauzė_įvykis.is_set():
                읽기대상들 = [eilutė_duomenys for 순번, eilutė_duomenys in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [eilutė_duomenys for eilutė_duomenys in 자신.접속자들 if eilutė_duomenys is not None]
                쓰기대상들 = [eilutė_duomenys for 순번, eilutė_duomenys in enumerate(자신.접속자들) if eilutė_duomenys is not None and 자신.informacinės_technologijos_laukiama[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for eilutė_duomenys in 읽을수있음:
                    if eilutė_duomenys in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(eilutė_duomenys); 자신.접속자들[순번], _ = eilutė_duomenys.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(eilutė_duomenys); duomenys = eilutė_duomenys.recv(16384)
                        if not duomenys: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(duomenys)
                for eilutė_duomenys in 쓸수있음:
                    순번 = 자신.접속자들.index(eilutė_duomenys)
                    try: prekė_COUNT = eilutė_duomenys.send(자신.informacinės_technologijos_laukiama[순번])
                    except BlockingIOError: continue
                    del 자신.informacinės_technologijos_laukiama[순번][:prekė_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.informacinės_technologijos_laukiama):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pauzė_įvykis.is_set(): 자신.KLAIDA = str(보조항목)

    def Užverti(자신):
        자신.Pauzė_įvykis.set(); 자신.darbininkas.join(timeout=2)
        for eilutė_duomenys in 자신.수신창구들 + 자신.접속자들:
            if eilutė_duomenys is not None: eilutė_duomenys.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumentas_ARRAY): 자신.Užverti()
