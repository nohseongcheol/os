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

մեքենա_հասցե = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
համացանցի_հասցե_արժեք = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Ցանց_կամուրջ:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), նկարահանել=False, հյուր_հասցե=None, հոստ_հասցե='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        հյուր_հասցե = հյուր_հասցե or 자신.ip_config['IP']
        qemu_network(자신.ip_config, հյուր_հասցե)
        հասցե=ipaddress.IPv4Address(հյուր_հասցե)
        자신.հյուր_հասցե=str(հասցե); 자신.현재주소=հասցե.packed
        հասցե=ipaddress.IPv4Address(հոստ_հասցե)
        if հասցե.is_multicast or str(հասցե)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.հոստ_հասցե=str(հասցե)
        자신.նկարահանել = նկարահանել; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', տվյալ_դիրք) for տվյալ_դիրք in range(50000,50008)}
        for զտիչ_արժեք in 전달규칙들:
            ուղի_բաղադրիչ = զտիչ_արժեք.split(':')
            if len(ուղի_բաղադրիչ) != 3 or ուղի_բաղադրիչ[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, հոստ, հյուր = ուղի_բաղադրիչ[0], int(ուղի_բաղադրիչ[1]), int(ուղի_բաղադրիչ[2])
            if not 1024 <= հոստ <= 65535 or not 1 <= հյուր <= 65535 or (통신규약, հոստ) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + զտիչ_արժեք)
            사용중주소.add((통신규약, հոստ)); 자신.전달규칙들.append((통신규약, հոստ, հյուր))
        자신.수신창구들 = []
        for _ in range(2):
            սպասարկիչ_արժեք = socket.socket()
            սպասարկիչ_արժեք.bind(('127.0.0.1', 0)); սպասարկիչ_արժեք.listen(1); սպասարկիչ_արժեք.setblocking(False)
            자신.수신창구들.append(սպասարկիչ_արժեք)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.դադար_միջոցառում = threading.Event(); 자신.Սխալ = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Շրջան_արժեք, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, 이더넷접속번호 = [տող_տվյալ.getsockname()[1] for տող_տվյալ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.հյուր_հասցե) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.հյուր_հասցե)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.հյուր_հասցե)
        for 통신규약, հոստ, հյուր in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, հոստ, 자신.հյուր_հասցե, հյուր)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.հոստ_հասցե+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(이더넷접속번호),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, փաթեթ_տվյալ):
        자신.대기중[1] += struct.pack('!I', len(փաթեթ_տվյալ)) + փաթեթ_տվյալ

    def 전문추적(자신, 방향, փաթեթ_տվյալ):
        if not 자신.նկարահանել or len(փաթեթ_տվյալ)<20: return
        Տեղաշարժում_արժեք=(փաթեթ_տվյալ[0]&15)*4
        մուտքագրում_արժեք={'time':time.monotonic(),'direction':방향,'bytes':len(փաթեթ_տվյալ),'protocol':փաթեթ_տվյալ[9]}
        if փաթեթ_տվյալ[9]==6 and len(փաթեթ_տվյալ)>=Տեղաշարժում_արժեք+20:
            원본자료,նպատակակետ_տվյալ_հասցե,순서번호,확인번호,설정비트,պատուհան=struct.unpack_from('!HHIIHH',փաթեթ_տվյալ,Տեղաշարժում_արժեք)
            մուտքագրում_արժեք.update(source=원본자료,destination=նպատակակետ_տվյալ_հասցե,seq=순서번호,ack=확인번호,flags=설정비트&255,window=պատուհան,
                        payload=len(փաթեթ_տվյալ)-Տեղաշարժում_արժեք-((փաթեթ_տվյալ[Տեղաշարժում_արժեք+12]>>4)*4))
        자신.추적기록.append(մուտքագրում_արժեք)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, տվյալ):
        for գրանշանի_կոդ in տվյալ:
            if գրանշանի_կոդ == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        հասցե=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(հասցե)))
                            자신.현재주소=հասցե
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + մեքենա_հասցե + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif գրանշանի_կոդ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if գրանշանի_կոդ not in (220, 221): 자신.잘못됨 = True
                    գրանշանի_կոդ = 192 if գրանշանի_կոդ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(գրանշանի_կոդ)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, տվյալ):
        자신.이더넷자료 += տվյալ
        while len(자신.이더넷자료) >= 4:
            개수 = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < 개수 + 4: return
            실행틀 = bytes(자신.이더넷자료[4:4+개수]); del 자신.이더넷자료[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                հասցե_տարլուծում_փաթեթ = 실행틀[14:42]
                if հասցե_տարլուծում_փաթեթ[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and հասցե_տարլուծում_փաթեթ[24:28] == 자신.현재주소:
                    응답자료 = հասցե_տարլուծում_փաթեթ[:6] + b'\x00\x02' + մեքենա_հասցե + 자신.현재주소 + հասցե_տարլուծում_փաթեթ[8:18]
                    자신.실행틀(실행틀[6:12] + մեքենա_հասցե + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                փաթեթ_տվյալ = 실행틀[14:]
                자신.전문추적('to_guest',փաթեթ_տվյալ)
                자신.대기중[0] += b'\xc0' + փաթեթ_տվյալ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Շրջան_արժեք(자신):
        try:
            while not 자신.դադար_միջոցառում.is_set():
                읽기대상들 = [տող_տվյալ for 순번, տող_տվյալ in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [տող_տվյալ for տող_տվյալ in 자신.접속자들 if տող_տվյալ is not None]
                쓰기대상들 = [տող_տվյալ for 순번, տող_տվյալ in enumerate(자신.접속자들) if տող_տվյալ is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for տող_տվյալ in 읽을수있음:
                    if տող_տվյալ in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(տող_տվյալ); 자신.접속자들[순번], _ = տող_տվյալ.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(տող_տվյալ); տվյալ = տող_տվյալ.recv(16384)
                        if not տվյալ: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(տվյալ)
                for տող_տվյալ in 쓸수있음:
                    순번 = 자신.접속자들.index(տող_տվյալ)
                    try: 개수 = տող_տվյալ.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.դադար_միջոցառում.is_set(): 자신.Սխալ = str(보조항목)

    def Փակ(자신):
        자신.դադար_միջոցառում.set(); 자신.작업가닥.join(timeout=2)
        for տող_տվյալ in 자신.수신창구들 + 자신.접속자들:
            if տող_տվյալ is not None: տող_տվյալ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *արգումենտ_ԶԱՆԳՎԱԾ): 자신.Փակ()
