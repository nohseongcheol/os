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

absoluuttinen_osoite = bytes.fromhex('525400123456')
yhdyskäytävä_laitteisto_OSOITE = bytes.fromhex('52550a000202')
Internet_osoite_ARVO = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class silta_3de4fe3a:
    def __init__(자신, tiedostonsiirto_portin_numero=2121, 전달규칙들=(), siepata=False, vieras_OSOITE=None, isäntä_OSOITE='127.0.0.1'):
        if not 1024 <= tiedostonsiirto_portin_numero <= 65535 or 50000 <= tiedostonsiirto_portin_numero <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.tiedostonsiirto_portin_numero = tiedostonsiirto_portin_numero
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        vieras_OSOITE = vieras_OSOITE or 자신.ip_config['IP']
        qemu_network(자신.ip_config, vieras_OSOITE)
        OSOITE=ipaddress.IPv4Address(vieras_OSOITE)
        자신.vieras_OSOITE=str(OSOITE); 자신.nykyinen_OSOITE=OSOITE.packed
        OSOITE=ipaddress.IPv4Address(isäntä_OSOITE)
        if OSOITE.is_multicast or str(OSOITE)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.isäntä_OSOITE=str(OSOITE)
        자신.siepata = siepata; 자신.tapahtumaloki = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', tiedostonsiirto_portin_numero)} | {('tcp', data_toimi) for data_toimi in range(50000,50008)}
        for sääntö_ARVO in 전달규칙들:
            polku_osa = sääntö_ARVO.split(':')
            if len(polku_osa) != 3 or polku_osa[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, isäntä, vieras = polku_osa[0], int(polku_osa[1]), int(polku_osa[2])
            if not 1024 <= isäntä <= 65535 or not 1 <= vieras <= 65535 or (통신규약, isäntä) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + sääntö_ARVO)
            사용중주소.add((통신규약, isäntä)); 자신.전달규칙들.append((통신규약, isäntä, vieras))
        자신.수신창구들 = []
        for _ in range(2):
            palvelin_ARVO = socket.socket()
            palvelin_ARVO.bind(('127.0.0.1', 0)); palvelin_ARVO.listen(1); palvelin_ARVO.setblocking(False)
            자신.수신창구들.append(palvelin_ARVO)
        자신.접속자들 = [None, None]
        자신.tietojärjestelmät_Odottaa = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.tietojärjestelmät_pätemätön = False
        자신.Keskeytä_tapahtuma = threading.Event(); 자신.VIRHE = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.työntekijä = threading.Thread(target=자신.kehä_ARVO, daemon=True)
        자신.työntekijä.start()

    def 전달인수(자신):
        COM_portti_numero, Ethernet_portti = [merkkijono_data.getsockname()[1] for merkkijono_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.vieras_OSOITE) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.tiedostonsiirto_portin_numero, 자신.vieras_OSOITE)
        for portin_numero in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portin_numero, 자신.vieras_OSOITE)
        for 통신규약, isäntä, vieras in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, isäntä, 자신.vieras_OSOITE, vieras)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.isäntä_OSOITE+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_portti_numero),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_portti),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def suoritus_kuva(자신, paketti_data):
        자신.tietojärjestelmät_Odottaa[1] += struct.pack('!I', len(paketti_data)) + paketti_data

    def jälki_paketti(자신, 방향, paketti_data):
        if not 자신.siepata or len(paketti_data)<20: return
        SIIRTYMÄ_ARVO=(paketti_data[0]&15)*4
        merkintä_ARVO_962f286b={'time':time.monotonic(),'direction':방향,'bytes':len(paketti_data),'protocol':paketti_data[9]}
        if paketti_data[9]==6 and len(paketti_data)>=SIIRTYMÄ_ARVO+20:
            원본자료,kohde_data_OSOITE,tilata_numero,확인번호,määritys_Background_Intelligent_Transfer_Service,Ikkuna=struct.unpack_from('!HHIIHH',paketti_data,SIIRTYMÄ_ARVO)
            merkintä_ARVO_962f286b.update(source=원본자료,destination=kohde_data_OSOITE,seq=tilata_numero,ack=확인번호,flags=määritys_Background_Intelligent_Transfer_Service&255,window=Ikkuna,
                        payload=len(paketti_data)-SIIRTYMÄ_ARVO-((paketti_data[SIIRTYMÄ_ARVO+12]>>4)*4))
        자신.tapahtumaloki.append(merkintä_ARVO_962f286b)
        if len(자신.tapahtumaloki)>2048: del 자신.tapahtumaloki[:1024]

    def SLIP_syöte(자신, data):
        for merkkikoodi in data:
            if merkkikoodi == 192:
                if 자신.직렬전문 and not 자신.tietojärjestelmät_pätemätön and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        OSOITE=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(OSOITE)))
                            자신.nykyinen_OSOITE=OSOITE
                        except ValueError:
                            pass
                    자신.jälki_paketti('from_guest',자신.직렬전문)
                    자신.suoritus_kuva(yhdyskäytävä_laitteisto_OSOITE + absoluuttinen_osoite + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.tietojärjestelmät_pätemätön = False
            elif merkkikoodi == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if merkkikoodi not in (220, 221): 자신.tietojärjestelmät_pätemätön = True
                    merkkikoodi = 192 if merkkikoodi == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(merkkikoodi)
                else: 자신.tietojärjestelmät_pätemätön = True

    def Ethernet_syöte(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            kohde_LASKE = struct.unpack_from('!I', 자신.Ethernet)[0]
            if kohde_LASKE > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < kohde_LASKE + 4: return
            suoritus_kuva = bytes(자신.Ethernet[4:4+kohde_LASKE]); del 자신.Ethernet[:4+kohde_LASKE]
            if len(suoritus_kuva) < 14: continue
            if suoritus_kuva[12:14] == b'\x08\x06' and len(suoritus_kuva) >= 42:
                OSOITE_tarkkuus_paketti = suoritus_kuva[14:42]
                if OSOITE_tarkkuus_paketti[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and OSOITE_tarkkuus_paketti[24:28] == 자신.nykyinen_OSOITE:
                    vastaus = OSOITE_tarkkuus_paketti[:6] + b'\x00\x02' + absoluuttinen_osoite + 자신.nykyinen_OSOITE + OSOITE_tarkkuus_paketti[8:18]
                    자신.suoritus_kuva(suoritus_kuva[6:12] + absoluuttinen_osoite + b'\x08\x06' + vastaus)
            elif suoritus_kuva[12:14] == b'\x08\x00':
                paketti_data = suoritus_kuva[14:]
                자신.jälki_paketti('to_guest',paketti_data)
                자신.tietojärjestelmät_Odottaa[0] += b'\xc0' + paketti_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def kehä_ARVO(자신):
        try:
            while not 자신.Keskeytä_tapahtuma.is_set():
                읽기대상들 = [merkkijono_data for 순번, merkkijono_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [merkkijono_data for merkkijono_data in 자신.접속자들 if merkkijono_data is not None]
                쓰기대상들 = [merkkijono_data for 순번, merkkijono_data in enumerate(자신.접속자들) if merkkijono_data is not None and 자신.tietojärjestelmät_Odottaa[순번]]
                읽을수있음, kirjoitettava, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for merkkijono_data in 읽을수있음:
                    if merkkijono_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(merkkijono_data); 자신.접속자들[순번], _ = merkkijono_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(merkkijono_data); data = merkkijono_data.recv(16384)
                        if not data: return
                        (자신.SLIP_syöte if 순번 == 0 else 자신.Ethernet_syöte)(data)
                for merkkijono_data in kirjoitettava:
                    순번 = 자신.접속자들.index(merkkijono_data)
                    try: kohde_LASKE = merkkijono_data.send(자신.tietojärjestelmät_Odottaa[순번])
                    except BlockingIOError: continue
                    del 자신.tietojärjestelmät_Odottaa[순번][:kohde_LASKE]
                if any(len(SEKUNNIT_ARVO) > 1024 * 1024 for SEKUNNIT_ARVO in 자신.tietojärjestelmät_Odottaa):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Keskeytä_tapahtuma.is_set(): 자신.VIRHE = str(보조항목)

    def Sulje(자신):
        자신.Keskeytä_tapahtuma.set(); 자신.työntekijä.join(timeout=2)
        for merkkijono_data in 자신.수신창구들 + 자신.접속자들:
            if merkkijono_data is not None: merkkijono_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumentti_MATRIISI): 자신.Sulje()
