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

vél_slóð = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
veffang_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Net_brú:
    def __init__(자신, skrá_flytja_tengisnúmer=2121, 전달규칙들=(), fanga=False, gestur_slóð=None, hýsa_slóð='127.0.0.1'):
        if not 1024 <= skrá_flytja_tengisnúmer <= 65535 or 50000 <= skrá_flytja_tengisnúmer <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.skrá_flytja_tengisnúmer = skrá_flytja_tengisnúmer
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gestur_slóð = gestur_slóð or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gestur_slóð)
        slóð=ipaddress.IPv4Address(gestur_slóð)
        자신.gestur_slóð=str(slóð); 자신.현재주소=slóð.packed
        slóð=ipaddress.IPv4Address(hýsa_slóð)
        if slóð.is_multicast or str(slóð)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.hýsa_slóð=str(slóð)
        자신.fanga = fanga; 자신.spor_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', skrá_flytja_tengisnúmer)} | {('tcp', gögn_staða) for gögn_staða in range(50000,50008)}
        for sía_VALUE in 전달규칙들:
            slóð_þáttur = sía_VALUE.split(':')
            if len(slóð_þáttur) != 3 or slóð_þáttur[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, hýsa, gestur = slóð_þáttur[0], int(slóð_þáttur[1]), int(slóð_þáttur[2])
            if not 1024 <= hýsa <= 65535 or not 1 <= gestur <= 65535 or (통신규약, hýsa) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + sía_VALUE)
            사용중주소.add((통신규약, hýsa)); 자신.전달규칙들.append((통신규약, hýsa, gestur))
        자신.수신창구들 = []
        for _ in range(2):
            þjónn_VALUE = socket.socket()
            þjónn_VALUE.bind(('127.0.0.1', 0)); þjónn_VALUE.listen(1); þjónn_VALUE.setblocking(False)
            자신.수신창구들.append(þjónn_VALUE)
        자신.접속자들 = [None, None]
        자신.upplýsingatækni_Í_bið = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.upplýsingatækni_ógilt = False
        자신.gera_hlé_atvik = threading.Event(); 자신.Villa = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.starfskraftur = threading.Thread(target=자신.lota_VALUE, daemon=True)
        자신.starfskraftur.start()

    def 전달인수(자신):
        raðtengi_númer, Íðnetstengi = [strengur_gögn.getsockname()[1] for strengur_gögn in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gestur_slóð) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.skrá_flytja_tengisnúmer, 자신.gestur_slóð)
        for tengisnúmer in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(tengisnúmer, 자신.gestur_slóð)
        for 통신규약, hýsa, gestur in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, hýsa, 자신.gestur_slóð, gestur)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.hýsa_slóð+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(raðtengi_númer),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Íðnetstengi),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pakki_gögn):
        자신.upplýsingatækni_Í_bið[1] += struct.pack('!I', len(pakki_gögn)) + pakki_gögn

    def spor_pakki(자신, 방향, pakki_gögn):
        if not 자신.fanga or len(pakki_gögn)<20: return
        OFFSET_VALUE=(pakki_gögn[0]&15)*4
        færsla_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(pakki_gögn),'protocol':pakki_gögn[9]}
        if pakki_gögn[9]==6 and len(pakki_gögn)>=OFFSET_VALUE+20:
            원본자료,endastaður_gögn_slóð,röð_númer,확인번호,afbrigði_Background_Intelligent_Transfer_Service,Gluggi=struct.unpack_from('!HHIIHH',pakki_gögn,OFFSET_VALUE)
            færsla_VALUE.update(source=원본자료,destination=endastaður_gögn_slóð,seq=röð_númer,ack=확인번호,flags=afbrigði_Background_Intelligent_Transfer_Service&255,window=Gluggi,
                        payload=len(pakki_gögn)-OFFSET_VALUE-((pakki_gögn[OFFSET_VALUE+12]>>4)*4))
        자신.spor_LOG.append(færsla_VALUE)
        if len(자신.spor_LOG)>2048: del 자신.spor_LOG[:1024]

    def 직렬전문입력(자신, gögn):
        for stafkóði in gögn:
            if stafkóði == 192:
                if 자신.직렬전문 and not 자신.upplýsingatækni_ógilt and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        slóð=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(slóð)))
                            자신.현재주소=slóð
                        except ValueError:
                            pass
                    자신.spor_pakki('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + vél_slóð + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.upplýsingatækni_ógilt = False
            elif stafkóði == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if stafkóði not in (220, 221): 자신.upplýsingatækni_ógilt = True
                    stafkóði = 192 if stafkóði == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(stafkóði)
                else: 자신.upplýsingatækni_ógilt = True

    def 이더넷입력(자신, gögn):
        자신.Ethernet += gögn
        while len(자신.Ethernet) >= 4:
            vara_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if vara_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < vara_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+vara_COUNT]); del 자신.Ethernet[:4+vara_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                slóð_upplausn_pakki = 실행틀[14:42]
                if slóð_upplausn_pakki[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and slóð_upplausn_pakki[24:28] == 자신.현재주소:
                    응답자료 = slóð_upplausn_pakki[:6] + b'\x00\x02' + vél_slóð + 자신.현재주소 + slóð_upplausn_pakki[8:18]
                    자신.실행틀(실행틀[6:12] + vél_slóð + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                pakki_gögn = 실행틀[14:]
                자신.spor_pakki('to_guest',pakki_gögn)
                자신.upplýsingatækni_Í_bið[0] += b'\xc0' + pakki_gögn.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def lota_VALUE(자신):
        try:
            while not 자신.gera_hlé_atvik.is_set():
                읽기대상들 = [strengur_gögn for 순번, strengur_gögn in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [strengur_gögn for strengur_gögn in 자신.접속자들 if strengur_gögn is not None]
                쓰기대상들 = [strengur_gögn for 순번, strengur_gögn in enumerate(자신.접속자들) if strengur_gögn is not None and 자신.upplýsingatækni_Í_bið[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for strengur_gögn in 읽을수있음:
                    if strengur_gögn in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(strengur_gögn); 자신.접속자들[순번], _ = strengur_gögn.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(strengur_gögn); gögn = strengur_gögn.recv(16384)
                        if not gögn: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(gögn)
                for strengur_gögn in 쓸수있음:
                    순번 = 자신.접속자들.index(strengur_gögn)
                    try: vara_COUNT = strengur_gögn.send(자신.upplýsingatækni_Í_bið[순번])
                    except BlockingIOError: continue
                    del 자신.upplýsingatækni_Í_bið[순번][:vara_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.upplýsingatækni_Í_bið):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.gera_hlé_atvik.is_set(): 자신.Villa = str(보조항목)

    def Loka(자신):
        자신.gera_hlé_atvik.set(); 자신.starfskraftur.join(timeout=2)
        for strengur_gögn in 자신.수신창구들 + 자신.접속자들:
            if strengur_gögn is not None: strengur_gögn.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *frumbreyta_ARRAY): 자신.Loka()
