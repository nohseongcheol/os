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

absolut_adresse = bytes.fromhex('525400123456')
gateway_hardware_mail = bytes.fromhex('52550a000202')
internetadresse_VÆRDI = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class bro_3de4fe3a:
    def __init__(자신, filoverførsel_portnummer=2121, 전달규칙들=(), optage=False, gæst_mail=None, vært_mail='127.0.0.1'):
        if not 1024 <= filoverførsel_portnummer <= 65535 or 50000 <= filoverførsel_portnummer <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.filoverførsel_portnummer = filoverførsel_portnummer
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gæst_mail = gæst_mail or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gæst_mail)
        mail=ipaddress.IPv4Address(gæst_mail)
        자신.gæst_mail=str(mail); 자신.aktuel_mail=mail.packed
        mail=ipaddress.IPv4Address(vært_mail)
        if mail.is_multicast or str(mail)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.vært_mail=str(mail)
        자신.optage = optage; 자신.sporingslogfil = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', filoverførsel_portnummer)} | {('tcp', data_placere) for data_placere in range(50000,50008)}
        for regel_VÆRDI in 전달규칙들:
            sti_komponent = regel_VÆRDI.split(':')
            if len(sti_komponent) != 3 or sti_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, vært, gæst = sti_komponent[0], int(sti_komponent[1]), int(sti_komponent[2])
            if not 1024 <= vært <= 65535 or not 1 <= gæst <= 65535 or (통신규약, vært) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + regel_VÆRDI)
            사용중주소.add((통신규약, vært)); 자신.전달규칙들.append((통신규약, vært, gæst))
        자신.수신창구들 = []
        for _ in range(2):
            server_VÆRDI = socket.socket()
            server_VÆRDI.bind(('127.0.0.1', 0)); server_VÆRDI.listen(1); server_VÆRDI.setblocking(False)
            자신.수신창구들.append(server_VÆRDI)
        자신.접속자들 = [None, None]
        자신.it_Afventer = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.it_ugyldig = False
        자신.Afbryd_midlertidigt_hændelse = threading.Event(); 자신.fejl = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.arbejder = threading.Thread(target=자신.Cyklus_VÆRDI, daemon=True)
        자신.arbejder.start()

    def 전달인수(자신):
        COM_port_tal, Ethernet_port = [streng_data.getsockname()[1] for streng_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gæst_mail) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.filoverførsel_portnummer, 자신.gæst_mail)
        for portnummer in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portnummer, 자신.gæst_mail)
        for 통신규약, vært, gæst in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, vært, 자신.gæst_mail, gæst)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.vært_mail+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_port_tal),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def udførelse_ramme(자신, pakke_data):
        자신.it_Afventer[1] += struct.pack('!I', len(pakke_data)) + pakke_data

    def spor_pakke(자신, 방향, pakke_data):
        if not 자신.optage or len(pakke_data)<20: return
        FORSKYDNING_VÆRDI=(pakke_data[0]&15)*4
        post_VÆRDI_962f286b={'time':time.monotonic(),'direction':방향,'bytes':len(pakke_data),'protocol':pakke_data[9]}
        if pakke_data[9]==6 and len(pakke_data)>=FORSKYDNING_VÆRDI+20:
            원본자료,destination_data_mail,ordre_tal,확인번호,konfiguration_BITS,Vindue=struct.unpack_from('!HHIIHH',pakke_data,FORSKYDNING_VÆRDI)
            post_VÆRDI_962f286b.update(source=원본자료,destination=destination_data_mail,seq=ordre_tal,ack=확인번호,flags=konfiguration_BITS&255,window=Vindue,
                        payload=len(pakke_data)-FORSKYDNING_VÆRDI-((pakke_data[FORSKYDNING_VÆRDI+12]>>4)*4))
        자신.sporingslogfil.append(post_VÆRDI_962f286b)
        if len(자신.sporingslogfil)>2048: del 자신.sporingslogfil[:1024]

    def 직렬전문입력(자신, data):
        for tegnkode in data:
            if tegnkode == 192:
                if 자신.직렬전문 and not 자신.it_ugyldig and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        mail=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(mail)))
                            자신.aktuel_mail=mail
                        except ValueError:
                            pass
                    자신.spor_pakke('from_guest',자신.직렬전문)
                    자신.udførelse_ramme(gateway_hardware_mail + absolut_adresse + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.it_ugyldig = False
            elif tegnkode == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if tegnkode not in (220, 221): 자신.it_ugyldig = True
                    tegnkode = 192 if tegnkode == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(tegnkode)
                else: 자신.it_ugyldig = True

    def Ethernet_input(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            vare_TÆL = struct.unpack_from('!I', 자신.Ethernet)[0]
            if vare_TÆL > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < vare_TÆL + 4: return
            udførelse_ramme = bytes(자신.Ethernet[4:4+vare_TÆL]); del 자신.Ethernet[:4+vare_TÆL]
            if len(udførelse_ramme) < 14: continue
            if udførelse_ramme[12:14] == b'\x08\x06' and len(udførelse_ramme) >= 42:
                mail_opløsning_pakke = udførelse_ramme[14:42]
                if mail_opløsning_pakke[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and mail_opløsning_pakke[24:28] == 자신.aktuel_mail:
                    svar_1262b476 = mail_opløsning_pakke[:6] + b'\x00\x02' + absolut_adresse + 자신.aktuel_mail + mail_opløsning_pakke[8:18]
                    자신.udførelse_ramme(udførelse_ramme[6:12] + absolut_adresse + b'\x08\x06' + svar_1262b476)
            elif udførelse_ramme[12:14] == b'\x08\x00':
                pakke_data = udførelse_ramme[14:]
                자신.spor_pakke('to_guest',pakke_data)
                자신.it_Afventer[0] += b'\xc0' + pakke_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cyklus_VÆRDI(자신):
        try:
            while not 자신.Afbryd_midlertidigt_hændelse.is_set():
                읽기대상들 = [streng_data for 순번, streng_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [streng_data for streng_data in 자신.접속자들 if streng_data is not None]
                쓰기대상들 = [streng_data for 순번, streng_data in enumerate(자신.접속자들) if streng_data is not None and 자신.it_Afventer[순번]]
                읽을수있음, skrivbar, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for streng_data in 읽을수있음:
                    if streng_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(streng_data); 자신.접속자들[순번], _ = streng_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(streng_data); data = streng_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.Ethernet_input)(data)
                for streng_data in skrivbar:
                    순번 = 자신.접속자들.index(streng_data)
                    try: vare_TÆL = streng_data.send(자신.it_Afventer[순번])
                    except BlockingIOError: continue
                    del 자신.it_Afventer[순번][:vare_TÆL]
                if any(len(SEKUND_VÆRDI) > 1024 * 1024 for SEKUND_VÆRDI in 자신.it_Afventer):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Afbryd_midlertidigt_hændelse.is_set(): 자신.fejl = str(보조항목)

    def Luk(자신):
        자신.Afbryd_midlertidigt_hændelse.set(); 자신.arbejder.join(timeout=2)
        for streng_data in 자신.수신창구들 + 자신.접속자들:
            if streng_data is not None: streng_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_MATRIX): 자신.Luk()
