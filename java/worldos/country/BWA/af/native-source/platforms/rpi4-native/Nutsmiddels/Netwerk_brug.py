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

masjien_adres = bytes.fromhex('525400123456')
deurgang_hardeware_adres = bytes.fromhex('52550a000202')
internetadres_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Netwerk_brug:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), lê_vas=False, gas_adres=None, hou_adres='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gas_adres = gas_adres or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gas_adres)
        adres=ipaddress.IPv4Address(gas_adres)
        자신.gas_adres=str(adres); 자신.현재주소=adres.packed
        adres=ipaddress.IPv4Address(hou_adres)
        if adres.is_multicast or str(adres)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.hou_adres=str(adres)
        자신.lê_vas = lê_vas; 자신.spoor_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', data_plaas) for data_plaas in range(50000,50008)}
        for reël_VALUE in 전달규칙들:
            pad_komponent = reël_VALUE.split(':')
            if len(pad_komponent) != 3 or pad_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, hou, gas = pad_komponent[0], int(pad_komponent[1]), int(pad_komponent[2])
            if not 1024 <= hou <= 65535 or not 1 <= gas <= 65535 or (통신규약, hou) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + reël_VALUE)
            사용중주소.add((통신규약, hou)); 자신.전달규칙들.append((통신규약, hou, gas))
        자신.수신창구들 = []
        for _ in range(2):
            bediener_VALUE = socket.socket()
            bediener_VALUE.bind(('127.0.0.1', 0)); bediener_VALUE.listen(1); bediener_VALUE.setblocking(False)
            자신.수신창구들.append(bediener_VALUE)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.pouseer_gebeurtenis = threading.Event(); 자신.Fout = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Siklus_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Eternetpoort = [string_data.getsockname()[1] for string_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gas_adres) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.gas_adres)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.gas_adres)
        for 통신규약, hou, gas in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, hou, 자신.gas_adres, gas)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.hou_adres+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Eternetpoort),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pakket_data):
        자신.대기중[1] += struct.pack('!I', len(pakket_data)) + pakket_data

    def spoor_pakket(자신, 방향, pakket_data):
        if not 자신.lê_vas or len(pakket_data)<20: return
        OFFSET_VALUE=(pakket_data[0]&15)*4
        inskrywing_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(pakket_data),'protocol':pakket_data[9]}
        if pakket_data[9]==6 and len(pakket_data)>=OFFSET_VALUE+20:
            원본자료,bestemming_data_adres,순서번호,확인번호,konfigurasie_Agtergrond_intelligente_oordragdiens,venster=struct.unpack_from('!HHIIHH',pakket_data,OFFSET_VALUE)
            inskrywing_VALUE.update(source=원본자료,destination=bestemming_data_adres,seq=순서번호,ack=확인번호,flags=konfigurasie_Agtergrond_intelligente_oordragdiens&255,window=venster,
                        payload=len(pakket_data)-OFFSET_VALUE-((pakket_data[OFFSET_VALUE+12]>>4)*4))
        자신.spoor_LOG.append(inskrywing_VALUE)
        if len(자신.spoor_LOG)>2048: del 자신.spoor_LOG[:1024]

    def 직렬전문입력(자신, data):
        for karakterkode in data:
            if karakterkode == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        adres=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(adres)))
                            자신.현재주소=adres
                        except ValueError:
                            pass
                    자신.spoor_pakket('from_guest',자신.직렬전문)
                    자신.실행틀(deurgang_hardeware_adres + masjien_adres + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif karakterkode == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if karakterkode not in (220, 221): 자신.잘못됨 = True
                    karakterkode = 192 if karakterkode == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(karakterkode)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            item_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if item_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < item_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+item_COUNT]); del 자신.Ethernet[:4+item_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                adres_resolusie_pakket = 실행틀[14:42]
                if adres_resolusie_pakket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and adres_resolusie_pakket[24:28] == 자신.현재주소:
                    응답자료 = adres_resolusie_pakket[:6] + b'\x00\x02' + masjien_adres + 자신.현재주소 + adres_resolusie_pakket[8:18]
                    자신.실행틀(실행틀[6:12] + masjien_adres + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                pakket_data = 실행틀[14:]
                자신.spoor_pakket('to_guest',pakket_data)
                자신.대기중[0] += b'\xc0' + pakket_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Siklus_VALUE(자신):
        try:
            while not 자신.pouseer_gebeurtenis.is_set():
                읽기대상들 = [string_data for 순번, string_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [string_data for string_data in 자신.접속자들 if string_data is not None]
                쓰기대상들 = [string_data for 순번, string_data in enumerate(자신.접속자들) if string_data is not None and 자신.대기중[순번]]
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
                    try: item_COUNT = string_data.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:item_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.pouseer_gebeurtenis.is_set(): 자신.Fout = str(보조항목)

    def Sluit(자신):
        자신.pouseer_gebeurtenis.set(); 자신.작업가닥.join(timeout=2)
        for string_data in 자신.수신창구들 + 자신.접속자들:
            if string_data is not None: string_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_ARRAY): 자신.Sluit()
