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

mashine_anwani = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Anwani_tovuti_thamani = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Mtandao_daraja:
    def __init__(자신, faili_hamisha_namba_ya_kituo=2121, 전달규칙들=(), unasaji=False, mgeni_anwani=None, mwenyeji_anwani='127.0.0.1'):
        if not 1024 <= faili_hamisha_namba_ya_kituo <= 65535 or 50000 <= faili_hamisha_namba_ya_kituo <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.faili_hamisha_namba_ya_kituo = faili_hamisha_namba_ya_kituo
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        mgeni_anwani = mgeni_anwani or 자신.ip_config['IP']
        qemu_network(자신.ip_config, mgeni_anwani)
        anwani=ipaddress.IPv4Address(mgeni_anwani)
        자신.mgeni_anwani=str(anwani); 자신.현재주소=anwani.packed
        anwani=ipaddress.IPv4Address(mwenyeji_anwani)
        if anwani.is_multicast or str(anwani)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.mwenyeji_anwani=str(anwani)
        자신.unasaji = unasaji; 자신.idadi_ya_maingizo_mlalo_batli = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', faili_hamisha_namba_ya_kituo)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for kanuni_thamani in 전달규칙들:
            njia_kijenzi = kanuni_thamani.split(':')
            if len(njia_kijenzi) != 3 or njia_kijenzi[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, mwenyeji, mgeni = njia_kijenzi[0], int(njia_kijenzi[1]), int(njia_kijenzi[2])
            if not 1024 <= mwenyeji <= 65535 or not 1 <= mgeni <= 65535 or (통신규약, mwenyeji) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + kanuni_thamani)
            사용중주소.add((통신규약, mwenyeji)); 자신.전달규칙들.append((통신규약, mwenyeji, mgeni))
        자신.수신창구들 = []
        for _ in range(2):
            seva_thamani = socket.socket()
            seva_thamani.bind(('127.0.0.1', 0)); seva_thamani.listen(1); seva_thamani.setblocking(False)
            자신.수신창구들.append(seva_thamani)
        자신.접속자들 = [None, None]
        자신.teknolojia_ya_maelezo_inayosubiri = [bytearray(), bytearray()]
        자신.Ethaneti = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.teknolojia_ya_maelezo_batili = False
        자신.sitisha_tukio = threading.Event(); 자신.kosa = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Mzunguko_thamani, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethaneti_kituo = [tungo_data.getsockname()[1] for tungo_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.mgeni_anwani) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.faili_hamisha_namba_ya_kituo, 자신.mgeni_anwani)
        for namba_ya_kituo in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(namba_ya_kituo, 자신.mgeni_anwani)
        for 통신규약, mwenyeji, mgeni in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, mwenyeji, 자신.mgeni_anwani, mgeni)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.mwenyeji_anwani+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethaneti_kituo),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pakiti_data):
        자신.teknolojia_ya_maelezo_inayosubiri[1] += struct.pack('!I', len(pakiti_data)) + pakiti_data

    def idadi_ya_maingizo_mlalo_pakiti(자신, 방향, pakiti_data):
        if not 자신.unasaji or len(pakiti_data)<20: return
        Chipua_thamani=(pakiti_data[0]&15)*4
        ingizo_thamani={'time':time.monotonic(),'direction':방향,'bytes':len(pakiti_data),'protocol':pakiti_data[9]}
        if pakiti_data[9]==6 and len(pakiti_data)>=Chipua_thamani+20:
            원본자료,fikio_data_anwani,순서번호,확인번호,usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma,dirisha=struct.unpack_from('!HHIIHH',pakiti_data,Chipua_thamani)
            ingizo_thamani.update(source=원본자료,destination=fikio_data_anwani,seq=순서번호,ack=확인번호,flags=usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&255,window=dirisha,
                        payload=len(pakiti_data)-Chipua_thamani-((pakiti_data[Chipua_thamani+12]>>4)*4))
        자신.idadi_ya_maingizo_mlalo_batli.append(ingizo_thamani)
        if len(자신.idadi_ya_maingizo_mlalo_batli)>2048: del 자신.idadi_ya_maingizo_mlalo_batli[:1024]

    def 직렬전문입력(자신, data):
        for msimbo_wa_kibambo in data:
            if msimbo_wa_kibambo == 192:
                if 자신.직렬전문 and not 자신.teknolojia_ya_maelezo_batili and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        anwani=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(anwani)))
                            자신.현재주소=anwani
                        except ValueError:
                            pass
                    자신.idadi_ya_maingizo_mlalo_pakiti('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + mashine_anwani + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.teknolojia_ya_maelezo_batili = False
            elif msimbo_wa_kibambo == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if msimbo_wa_kibambo not in (220, 221): 자신.teknolojia_ya_maelezo_batili = True
                    msimbo_wa_kibambo = 192 if msimbo_wa_kibambo == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(msimbo_wa_kibambo)
                else: 자신.teknolojia_ya_maelezo_batili = True

    def 이더넷입력(자신, data):
        자신.Ethaneti += data
        while len(자신.Ethaneti) >= 4:
            개수 = struct.unpack_from('!I', 자신.Ethaneti)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethaneti) < 개수 + 4: return
            실행틀 = bytes(자신.Ethaneti[4:4+개수]); del 자신.Ethaneti[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                anwani_mwonekano_pakiti = 실행틀[14:42]
                if anwani_mwonekano_pakiti[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and anwani_mwonekano_pakiti[24:28] == 자신.현재주소:
                    응답자료 = anwani_mwonekano_pakiti[:6] + b'\x00\x02' + mashine_anwani + 자신.현재주소 + anwani_mwonekano_pakiti[8:18]
                    자신.실행틀(실행틀[6:12] + mashine_anwani + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                pakiti_data = 실행틀[14:]
                자신.idadi_ya_maingizo_mlalo_pakiti('to_guest',pakiti_data)
                자신.teknolojia_ya_maelezo_inayosubiri[0] += b'\xc0' + pakiti_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Mzunguko_thamani(자신):
        try:
            while not 자신.sitisha_tukio.is_set():
                읽기대상들 = [tungo_data for 순번, tungo_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [tungo_data for tungo_data in 자신.접속자들 if tungo_data is not None]
                쓰기대상들 = [tungo_data for 순번, tungo_data in enumerate(자신.접속자들) if tungo_data is not None and 자신.teknolojia_ya_maelezo_inayosubiri[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for tungo_data in 읽을수있음:
                    if tungo_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(tungo_data); 자신.접속자들[순번], _ = tungo_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(tungo_data); data = tungo_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(data)
                for tungo_data in 쓸수있음:
                    순번 = 자신.접속자들.index(tungo_data)
                    try: 개수 = tungo_data.send(자신.teknolojia_ya_maelezo_inayosubiri[순번])
                    except BlockingIOError: continue
                    del 자신.teknolojia_ya_maelezo_inayosubiri[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.teknolojia_ya_maelezo_inayosubiri):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.sitisha_tukio.is_set(): 자신.kosa = str(보조항목)

    def funga(자신):
        자신.sitisha_tukio.set(); 자신.작업가닥.join(timeout=2)
        for tungo_data in 자신.수신창구들 + 자신.접속자들:
            if tungo_data is not None: tungo_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *hoja_ARRAY): 자신.funga()
