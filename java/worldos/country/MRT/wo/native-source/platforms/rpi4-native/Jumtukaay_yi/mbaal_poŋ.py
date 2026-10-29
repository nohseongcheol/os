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

masin_dëkkuwaay = bytes.fromhex('525400123456')
bunt_jumtukaay_dëkkuwaay = bytes.fromhex('52550a000202')
dëkkuwaayu_Internet_xëyma = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class mbaal_poŋ:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), jël=False, gan_dëkkuwaay=None, dalal_dëkkuwaay='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gan_dëkkuwaay = gan_dëkkuwaay or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gan_dëkkuwaay)
        dëkkuwaay=ipaddress.IPv4Address(gan_dëkkuwaay)
        자신.gan_dëkkuwaay=str(dëkkuwaay); 자신.현재주소=dëkkuwaay.packed
        dëkkuwaay=ipaddress.IPv4Address(dalal_dëkkuwaay)
        if dëkkuwaay.is_multicast or str(dëkkuwaay)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.dalal_dëkkuwaay=str(dëkkuwaay)
        자신.jël = jël; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for sart_xëyma in 전달규칙들:
            Yoonu_jëmale_bu_ci_bokk = sart_xëyma.split(':')
            if len(Yoonu_jëmale_bu_ci_bokk) != 3 or Yoonu_jëmale_bu_ci_bokk[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, dalal, gan = Yoonu_jëmale_bu_ci_bokk[0], int(Yoonu_jëmale_bu_ci_bokk[1]), int(Yoonu_jëmale_bu_ci_bokk[2])
            if not 1024 <= dalal <= 65535 or not 1 <= gan <= 65535 or (통신규약, dalal) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + sart_xëyma)
            사용중주소.add((통신규약, dalal)); 자신.전달규칙들.append((통신규약, dalal, gan))
        자신.수신창구들 = []
        for _ in range(2):
            dëggu_xëyma = socket.socket()
            dëggu_xëyma.bind(('127.0.0.1', 0)); dëggu_xëyma.listen(1); dëggu_xëyma.setblocking(False)
            자신.수신창구들.append(dëggu_xëyma)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.Ajandi_xewxew = threading.Event(); 자신.njumte = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Wërngal_xëyma, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_jël = [araf_yu_bennoo_mbir.getsockname()[1] for araf_yu_bennoo_mbir in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gan_dëkkuwaay) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.gan_dëkkuwaay)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.gan_dëkkuwaay)
        for 통신규약, dalal, gan in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, dalal, 자신.gan_dëkkuwaay, gan)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.dalal_dëkkuwaay+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_jël),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, 꾸러미자료):
        자신.대기중[1] += struct.pack('!I', len(꾸러미자료)) + 꾸러미자료

    def 전문추적(자신, 방향, 꾸러미자료):
        if not 자신.jël or len(꾸러미자료)<20: return
        Randal_xëyma=(꾸러미자료[0]&15)*4
        dugal_xabaar_xëyma={'time':time.monotonic(),'direction':방향,'bytes':len(꾸러미자료),'protocol':꾸러미자료[9]}
        if 꾸러미자료[9]==6 and len(꾸러미자료)>=Randal_xëyma+20:
            원본자료,jëmmukaay_mbir_dëkkuwaay,순서번호,확인번호,설정비트,palanteer=struct.unpack_from('!HHIIHH',꾸러미자료,Randal_xëyma)
            dugal_xabaar_xëyma.update(source=원본자료,destination=jëmmukaay_mbir_dëkkuwaay,seq=순서번호,ack=확인번호,flags=설정비트&255,window=palanteer,
                        payload=len(꾸러미자료)-Randal_xëyma-((꾸러미자료[Randal_xëyma+12]>>4)*4))
        자신.추적기록.append(dugal_xabaar_xëyma)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, mbir):
        for kotu_araf in mbir:
            if kotu_araf == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        dëkkuwaay=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(dëkkuwaay)))
                            자신.현재주소=dëkkuwaay
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(bunt_jumtukaay_dëkkuwaay + masin_dëkkuwaay + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif kotu_araf == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if kotu_araf not in (220, 221): 자신.잘못됨 = True
                    kotu_araf = 192 if kotu_araf == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(kotu_araf)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, mbir):
        자신.Ethernet += mbir
        while len(자신.Ethernet) >= 4:
            개수 = struct.unpack_from('!I', 자신.Ethernet)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < 개수 + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+개수]); del 자신.Ethernet[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                주소찾기전문 = 실행틀[14:42]
                if 주소찾기전문[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 주소찾기전문[24:28] == 자신.현재주소:
                    응답자료 = 주소찾기전문[:6] + b'\x00\x02' + masin_dëkkuwaay + 자신.현재주소 + 주소찾기전문[8:18]
                    자신.실행틀(실행틀[6:12] + masin_dëkkuwaay + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                꾸러미자료 = 실행틀[14:]
                자신.전문추적('to_guest',꾸러미자료)
                자신.대기중[0] += b'\xc0' + 꾸러미자료.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Wërngal_xëyma(자신):
        try:
            while not 자신.Ajandi_xewxew.is_set():
                읽기대상들 = [araf_yu_bennoo_mbir for 순번, araf_yu_bennoo_mbir in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [araf_yu_bennoo_mbir for araf_yu_bennoo_mbir in 자신.접속자들 if araf_yu_bennoo_mbir is not None]
                쓰기대상들 = [araf_yu_bennoo_mbir for 순번, araf_yu_bennoo_mbir in enumerate(자신.접속자들) if araf_yu_bennoo_mbir is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for araf_yu_bennoo_mbir in 읽을수있음:
                    if araf_yu_bennoo_mbir in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(araf_yu_bennoo_mbir); 자신.접속자들[순번], _ = araf_yu_bennoo_mbir.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(araf_yu_bennoo_mbir); mbir = araf_yu_bennoo_mbir.recv(16384)
                        if not mbir: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(mbir)
                for araf_yu_bennoo_mbir in 쓸수있음:
                    순번 = 자신.접속자들.index(araf_yu_bennoo_mbir)
                    try: 개수 = araf_yu_bennoo_mbir.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Ajandi_xewxew.is_set(): 자신.njumte = str(보조항목)

    def Tej(자신):
        자신.Ajandi_xewxew.set(); 자신.작업가닥.join(timeout=2)
        for araf_yu_bennoo_mbir in 자신.수신창구들 + 자신.접속자들:
            if araf_yu_bennoo_mbir is not None: araf_yu_bennoo_mbir.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *Tegtal_TABLO): 자신.Tej()
