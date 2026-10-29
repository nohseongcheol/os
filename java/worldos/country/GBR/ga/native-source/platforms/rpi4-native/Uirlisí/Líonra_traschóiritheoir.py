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

meaisín_ADDRESS = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
seoladh_Idirlín_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Líonra_traschóiritheoir:
    def __init__(자신, comhad_traschur_uimhir_phoirt=2121, 전달규칙들=(), taifead=False, aoi_ADDRESS=None, óstach_ADDRESS='127.0.0.1'):
        if not 1024 <= comhad_traschur_uimhir_phoirt <= 65535 or 50000 <= comhad_traschur_uimhir_phoirt <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.comhad_traschur_uimhir_phoirt = comhad_traschur_uimhir_phoirt
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        aoi_ADDRESS = aoi_ADDRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, aoi_ADDRESS)
        ADDRESS=ipaddress.IPv4Address(aoi_ADDRESS)
        자신.aoi_ADDRESS=str(ADDRESS); 자신.현재주소=ADDRESS.packed
        ADDRESS=ipaddress.IPv4Address(óstach_ADDRESS)
        if ADDRESS.is_multicast or str(ADDRESS)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.óstach_ADDRESS=str(ADDRESS)
        자신.taifead = taifead; 자신.rian_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', comhad_traschur_uimhir_phoirt)} | {('tcp', sonraí_suíomh) for sonraí_suíomh in range(50000,50008)}
        for riail_VALUE in 전달규칙들:
            cosán_comhpháirt = riail_VALUE.split(':')
            if len(cosán_comhpháirt) != 3 or cosán_comhpháirt[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, óstach, aoi = cosán_comhpháirt[0], int(cosán_comhpháirt[1]), int(cosán_comhpháirt[2])
            if not 1024 <= óstach <= 65535 or not 1 <= aoi <= 65535 or (통신규약, óstach) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + riail_VALUE)
            사용중주소.add((통신규약, óstach)); 자신.전달규칙들.append((통신규약, óstach, aoi))
        자신.수신창구들 = []
        for _ in range(2):
            freastalaí_VALUE = socket.socket()
            freastalaí_VALUE.bind(('127.0.0.1', 0)); freastalaí_VALUE.listen(1); freastalaí_VALUE.setblocking(False)
            자신.수신창구들.append(freastalaí_VALUE)
        자신.접속자들 = [None, None]
        자신.teicneolaíocht_faisnéise_Ar_feitheamh = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.teicneolaíocht_faisnéise_neamhbhailí = False
        자신.cuir_ar_shos_ócáid = threading.Event(); 자신.ERREÁID = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Timthriall_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_port = [teaghrán_sonraí.getsockname()[1] for teaghrán_sonraí in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.aoi_ADDRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.comhad_traschur_uimhir_phoirt, 자신.aoi_ADDRESS)
        for uimhir_phoirt in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(uimhir_phoirt, 자신.aoi_ADDRESS)
        for 통신규약, óstach, aoi in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, óstach, 자신.aoi_ADDRESS, aoi)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.óstach_ADDRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paicéad_sonraí):
        자신.teicneolaíocht_faisnéise_Ar_feitheamh[1] += struct.pack('!I', len(paicéad_sonraí)) + paicéad_sonraí

    def rian_paicéad(자신, 방향, paicéad_sonraí):
        if not 자신.taifead or len(paicéad_sonraí)<20: return
        OFFSET_VALUE=(paicéad_sonraí[0]&15)*4
        iontráil_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paicéad_sonraí),'protocol':paicéad_sonraí[9]}
        if paicéad_sonraí[9]==6 and len(paicéad_sonraí)>=OFFSET_VALUE+20:
            원본자료,sprioc_sonraí_ADDRESS,순서번호,확인번호,설정비트,fuinneog=struct.unpack_from('!HHIIHH',paicéad_sonraí,OFFSET_VALUE)
            iontráil_VALUE.update(source=원본자료,destination=sprioc_sonraí_ADDRESS,seq=순서번호,ack=확인번호,flags=설정비트&255,window=fuinneog,
                        payload=len(paicéad_sonraí)-OFFSET_VALUE-((paicéad_sonraí[OFFSET_VALUE+12]>>4)*4))
        자신.rian_LOG.append(iontráil_VALUE)
        if len(자신.rian_LOG)>2048: del 자신.rian_LOG[:1024]

    def 직렬전문입력(자신, sonraí):
        for pointe_cóid in sonraí:
            if pointe_cóid == 192:
                if 자신.직렬전문 and not 자신.teicneolaíocht_faisnéise_neamhbhailí and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADDRESS=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADDRESS)))
                            자신.현재주소=ADDRESS
                        except ValueError:
                            pass
                    자신.rian_paicéad('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + meaisín_ADDRESS + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.teicneolaíocht_faisnéise_neamhbhailí = False
            elif pointe_cóid == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if pointe_cóid not in (220, 221): 자신.teicneolaíocht_faisnéise_neamhbhailí = True
                    pointe_cóid = 192 if pointe_cóid == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(pointe_cóid)
                else: 자신.teicneolaíocht_faisnéise_neamhbhailí = True

    def 이더넷입력(자신, sonraí):
        자신.Ethernet += sonraí
        while len(자신.Ethernet) >= 4:
            mír_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if mír_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < mír_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+mír_COUNT]); del 자신.Ethernet[:4+mír_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ADDRESS_taifeach_paicéad = 실행틀[14:42]
                if ADDRESS_taifeach_paicéad[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADDRESS_taifeach_paicéad[24:28] == 자신.현재주소:
                    응답자료 = ADDRESS_taifeach_paicéad[:6] + b'\x00\x02' + meaisín_ADDRESS + 자신.현재주소 + ADDRESS_taifeach_paicéad[8:18]
                    자신.실행틀(실행틀[6:12] + meaisín_ADDRESS + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                paicéad_sonraí = 실행틀[14:]
                자신.rian_paicéad('to_guest',paicéad_sonraí)
                자신.teicneolaíocht_faisnéise_Ar_feitheamh[0] += b'\xc0' + paicéad_sonraí.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Timthriall_VALUE(자신):
        try:
            while not 자신.cuir_ar_shos_ócáid.is_set():
                읽기대상들 = [teaghrán_sonraí for 순번, teaghrán_sonraí in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [teaghrán_sonraí for teaghrán_sonraí in 자신.접속자들 if teaghrán_sonraí is not None]
                쓰기대상들 = [teaghrán_sonraí for 순번, teaghrán_sonraí in enumerate(자신.접속자들) if teaghrán_sonraí is not None and 자신.teicneolaíocht_faisnéise_Ar_feitheamh[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for teaghrán_sonraí in 읽을수있음:
                    if teaghrán_sonraí in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(teaghrán_sonraí); 자신.접속자들[순번], _ = teaghrán_sonraí.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(teaghrán_sonraí); sonraí = teaghrán_sonraí.recv(16384)
                        if not sonraí: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(sonraí)
                for teaghrán_sonraí in 쓸수있음:
                    순번 = 자신.접속자들.index(teaghrán_sonraí)
                    try: mír_COUNT = teaghrán_sonraí.send(자신.teicneolaíocht_faisnéise_Ar_feitheamh[순번])
                    except BlockingIOError: continue
                    del 자신.teicneolaíocht_faisnéise_Ar_feitheamh[순번][:mír_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.teicneolaíocht_faisnéise_Ar_feitheamh):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.cuir_ar_shos_ócáid.is_set(): 자신.ERREÁID = str(보조항목)

    def Dún(자신):
        자신.cuir_ar_shos_ócáid.set(); 자신.작업가닥.join(timeout=2)
        for teaghrán_sonraí in 자신.수신창구들 + 자신.접속자들:
            if teaghrán_sonraí is not None: teaghrán_sonraí.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argóint_ARRAY): 자신.Dún()
