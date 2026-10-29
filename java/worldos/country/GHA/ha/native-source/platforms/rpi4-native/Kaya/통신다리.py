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

cikakken_gurbin_adireshi = bytes.fromhex('525400123456')
Mashiga_kayan_haɗi_na_kwamfuta_imel = bytes.fromhex('52550a000202')
Adireshin_yanar_gizo_Daraja = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 통신다리:
    def __init__(자신, Fayil_Gusar_da_lambar_kafa=2121, 전달규칙들=(), ɗauka=False, baƙo_imel=None, sauka_imel='127.0.0.1'):
        if not 1024 <= Fayil_Gusar_da_lambar_kafa <= 65535 or 50000 <= Fayil_Gusar_da_lambar_kafa <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.Fayil_Gusar_da_lambar_kafa = Fayil_Gusar_da_lambar_kafa
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        baƙo_imel = baƙo_imel or 자신.ip_config['IP']
        qemu_network(자신.ip_config, baƙo_imel)
        imel=ipaddress.IPv4Address(baƙo_imel)
        자신.baƙo_imel=str(imel); 자신.현재주소=imel.packed
        imel=ipaddress.IPv4Address(sauka_imel)
        if imel.is_multicast or str(imel)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.sauka_imel=str(imel)
        자신.ɗauka = ɗauka; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', Fayil_Gusar_da_lambar_kafa)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for mataci_Daraja in 전달규칙들:
            Hanyar_shiga_Ƙunshiyar_na_urori = mataci_Daraja.split(':')
            if len(Hanyar_shiga_Ƙunshiyar_na_urori) != 3 or Hanyar_shiga_Ƙunshiyar_na_urori[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, sauka, baƙo = Hanyar_shiga_Ƙunshiyar_na_urori[0], int(Hanyar_shiga_Ƙunshiyar_na_urori[1]), int(Hanyar_shiga_Ƙunshiyar_na_urori[2])
            if not 1024 <= sauka <= 65535 or not 1 <= baƙo <= 65535 or (통신규약, sauka) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + mataci_Daraja)
            사용중주소.add((통신규약, sauka)); 자신.전달규칙들.append((통신규약, sauka, baƙo))
        자신.수신창구들 = []
        for _ in range(2):
            Saba_Daraja = socket.socket()
            Saba_Daraja.bind(('127.0.0.1', 0)); Saba_Daraja.listen(1); Saba_Daraja.setblocking(False)
            자신.수신창구들.append(Saba_Daraja)
        자신.접속자들 = [None, None]
        자신.kimiyar_bayanai_mai_jira = [bytearray(), bytearray()]
        자신.Wayar_kwamfuta_ta_yanar_gizo = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.kimiyar_bayanai_mara_ƙarfi = False
        자신.dakata_Faruwa = threading.Event(); 자신.Kuskure = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Aikin_na_ura_a_kai_a_kai_Daraja, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Wayar_kwamfuta_ta_yanar_gizo_fot = [Zare_Tarin_bayani.getsockname()[1] for Zare_Tarin_bayani in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.baƙo_imel) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.Fayil_Gusar_da_lambar_kafa, 자신.baƙo_imel)
        for lambar_kafa in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(lambar_kafa, 자신.baƙo_imel)
        for 통신규약, sauka, baƙo in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, sauka, 자신.baƙo_imel, baƙo)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.sauka_imel+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Wayar_kwamfuta_ta_yanar_gizo_fot),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, makunshi_Tarin_bayani):
        자신.kimiyar_bayanai_mai_jira[1] += struct.pack('!I', len(makunshi_Tarin_bayani)) + makunshi_Tarin_bayani

    def 전문추적(자신, 방향, makunshi_Tarin_bayani):
        if not 자신.ɗauka or len(makunshi_Tarin_bayani)<20: return
        Sassautawa_Daraja=(makunshi_Tarin_bayani[0]&15)*4
        Mashigar_bayanai_Daraja={'time':time.monotonic(),'direction':방향,'bytes':len(makunshi_Tarin_bayani),'protocol':makunshi_Tarin_bayani[9]}
        if makunshi_Tarin_bayani[9]==6 and len(makunshi_Tarin_bayani)>=Sassautawa_Daraja+20:
            원본자료,Zangon_ƙarshe_Tarin_bayani_imel,순서번호,확인번호,saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango,taga=struct.unpack_from('!HHIIHH',makunshi_Tarin_bayani,Sassautawa_Daraja)
            Mashigar_bayanai_Daraja.update(source=원본자료,destination=Zangon_ƙarshe_Tarin_bayani_imel,seq=순서번호,ack=확인번호,flags=saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&255,window=taga,
                        payload=len(makunshi_Tarin_bayani)-Sassautawa_Daraja-((makunshi_Tarin_bayani[Sassautawa_Daraja+12]>>4)*4))
        자신.추적기록.append(Mashigar_bayanai_Daraja)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, Tarin_bayani):
        for Lambar_sirrin_harafi in Tarin_bayani:
            if Lambar_sirrin_harafi == 192:
                if 자신.직렬전문 and not 자신.kimiyar_bayanai_mara_ƙarfi and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        imel=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(imel)))
                            자신.현재주소=imel
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(Mashiga_kayan_haɗi_na_kwamfuta_imel + cikakken_gurbin_adireshi + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.kimiyar_bayanai_mara_ƙarfi = False
            elif Lambar_sirrin_harafi == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if Lambar_sirrin_harafi not in (220, 221): 자신.kimiyar_bayanai_mara_ƙarfi = True
                    Lambar_sirrin_harafi = 192 if Lambar_sirrin_harafi == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(Lambar_sirrin_harafi)
                else: 자신.kimiyar_bayanai_mara_ƙarfi = True

    def 이더넷입력(자신, Tarin_bayani):
        자신.Wayar_kwamfuta_ta_yanar_gizo += Tarin_bayani
        while len(자신.Wayar_kwamfuta_ta_yanar_gizo) >= 4:
            개수 = struct.unpack_from('!I', 자신.Wayar_kwamfuta_ta_yanar_gizo)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Wayar_kwamfuta_ta_yanar_gizo) < 개수 + 4: return
            실행틀 = bytes(자신.Wayar_kwamfuta_ta_yanar_gizo[4:4+개수]); del 자신.Wayar_kwamfuta_ta_yanar_gizo[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                imel_Kyawon_tarkacen_hoto_makunshi = 실행틀[14:42]
                if imel_Kyawon_tarkacen_hoto_makunshi[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and imel_Kyawon_tarkacen_hoto_makunshi[24:28] == 자신.현재주소:
                    응답자료 = imel_Kyawon_tarkacen_hoto_makunshi[:6] + b'\x00\x02' + cikakken_gurbin_adireshi + 자신.현재주소 + imel_Kyawon_tarkacen_hoto_makunshi[8:18]
                    자신.실행틀(실행틀[6:12] + cikakken_gurbin_adireshi + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                makunshi_Tarin_bayani = 실행틀[14:]
                자신.전문추적('to_guest',makunshi_Tarin_bayani)
                자신.kimiyar_bayanai_mai_jira[0] += b'\xc0' + makunshi_Tarin_bayani.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Aikin_na_ura_a_kai_a_kai_Daraja(자신):
        try:
            while not 자신.dakata_Faruwa.is_set():
                읽기대상들 = [Zare_Tarin_bayani for 순번, Zare_Tarin_bayani in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [Zare_Tarin_bayani for Zare_Tarin_bayani in 자신.접속자들 if Zare_Tarin_bayani is not None]
                쓰기대상들 = [Zare_Tarin_bayani for 순번, Zare_Tarin_bayani in enumerate(자신.접속자들) if Zare_Tarin_bayani is not None and 자신.kimiyar_bayanai_mai_jira[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for Zare_Tarin_bayani in 읽을수있음:
                    if Zare_Tarin_bayani in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(Zare_Tarin_bayani); 자신.접속자들[순번], _ = Zare_Tarin_bayani.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(Zare_Tarin_bayani); Tarin_bayani = Zare_Tarin_bayani.recv(16384)
                        if not Tarin_bayani: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(Tarin_bayani)
                for Zare_Tarin_bayani in 쓸수있음:
                    순번 = 자신.접속자들.index(Zare_Tarin_bayani)
                    try: 개수 = Zare_Tarin_bayani.send(자신.kimiyar_bayanai_mai_jira[순번])
                    except BlockingIOError: continue
                    del 자신.kimiyar_bayanai_mai_jira[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.kimiyar_bayanai_mai_jira):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.dakata_Faruwa.is_set(): 자신.Kuskure = str(보조항목)

    def Rufe(자신):
        자신.dakata_Faruwa.set(); 자신.작업가닥.join(timeout=2)
        for Zare_Tarin_bayani in 자신.수신창구들 + 자신.접속자들:
            if Zare_Tarin_bayani is not None: Zare_Tarin_bayani.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *Tubalin_aiki_TSARI): 자신.Rufe()
