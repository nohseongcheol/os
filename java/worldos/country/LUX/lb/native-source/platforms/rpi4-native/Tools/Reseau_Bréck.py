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

Computer_Adress = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Internetsadress_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Reseau_Bréck:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), ophuelen=False, Gaascht_Adress=None, Host_Adress='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        Gaascht_Adress = Gaascht_Adress or 자신.ip_config['IP']
        qemu_network(자신.ip_config, Gaascht_Adress)
        Adress=ipaddress.IPv4Address(Gaascht_Adress)
        자신.Gaascht_Adress=str(Adress); 자신.현재주소=Adress.packed
        Adress=ipaddress.IPv4Address(Host_Adress)
        if Adress.is_multicast or str(Adress)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.Host_Adress=str(Adress)
        자신.ophuelen = ophuelen; 자신.추적기록 = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', Daten_positionéieren) for Daten_positionéieren in range(50000,50008)}
        for Regel_VALUE in 전달규칙들:
            Wee_Komponent = Regel_VALUE.split(':')
            if len(Wee_Komponent) != 3 or Wee_Komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, Host, Gaascht = Wee_Komponent[0], int(Wee_Komponent[1]), int(Wee_Komponent[2])
            if not 1024 <= Host <= 65535 or not 1 <= Gaascht <= 65535 or (통신규약, Host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + Regel_VALUE)
            사용중주소.add((통신규약, Host)); 자신.전달규칙들.append((통신규약, Host, Gaascht))
        자신.수신창구들 = []
        for _ in range(2):
            Server_VALUE = socket.socket()
            Server_VALUE.bind(('127.0.0.1', 0)); Server_VALUE.listen(1); Server_VALUE.setblocking(False)
            자신.수신창구들.append(Server_VALUE)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.pausen_Evenement = threading.Event(); 자신.Feeler = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Zyklus_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_Port = [Zeechefolleg_Daten.getsockname()[1] for Zeechefolleg_Daten in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.Gaascht_Adress) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.Gaascht_Adress)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.Gaascht_Adress)
        for 통신규약, Host, Gaascht in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, Host, 자신.Gaascht_Adress, Gaascht)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.Host_Adress+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_Port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, Pak_Daten):
        자신.대기중[1] += struct.pack('!I', len(Pak_Daten)) + Pak_Daten

    def 전문추적(자신, 방향, Pak_Daten):
        if not 자신.ophuelen or len(Pak_Daten)<20: return
        OFFSET_VALUE=(Pak_Daten[0]&15)*4
        Agab_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(Pak_Daten),'protocol':Pak_Daten[9]}
        if Pak_Daten[9]==6 and len(Pak_Daten)>=OFFSET_VALUE+20:
            원본자료,Zil_Daten_Adress,순서번호,확인번호,설정비트,Fënster=struct.unpack_from('!HHIIHH',Pak_Daten,OFFSET_VALUE)
            Agab_VALUE.update(source=원본자료,destination=Zil_Daten_Adress,seq=순서번호,ack=확인번호,flags=설정비트&255,window=Fënster,
                        payload=len(Pak_Daten)-OFFSET_VALUE-((Pak_Daten[OFFSET_VALUE+12]>>4)*4))
        자신.추적기록.append(Agab_VALUE)
        if len(자신.추적기록)>2048: del 자신.추적기록[:1024]

    def 직렬전문입력(자신, Daten):
        for Zeechecode in Daten:
            if Zeechecode == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        Adress=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(Adress)))
                            자신.현재주소=Adress
                        except ValueError:
                            pass
                    자신.전문추적('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + Computer_Adress + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif Zeechecode == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if Zeechecode not in (220, 221): 자신.잘못됨 = True
                    Zeechecode = 192 if Zeechecode == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(Zeechecode)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, Daten):
        자신.Ethernet += Daten
        while len(자신.Ethernet) >= 4:
            Element_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if Element_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < Element_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+Element_COUNT]); del 자신.Ethernet[:4+Element_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                Adress_Opléisung_Pak = 실행틀[14:42]
                if Adress_Opléisung_Pak[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and Adress_Opléisung_Pak[24:28] == 자신.현재주소:
                    응답자료 = Adress_Opléisung_Pak[:6] + b'\x00\x02' + Computer_Adress + 자신.현재주소 + Adress_Opléisung_Pak[8:18]
                    자신.실행틀(실행틀[6:12] + Computer_Adress + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                Pak_Daten = 실행틀[14:]
                자신.전문추적('to_guest',Pak_Daten)
                자신.대기중[0] += b'\xc0' + Pak_Daten.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Zyklus_VALUE(자신):
        try:
            while not 자신.pausen_Evenement.is_set():
                읽기대상들 = [Zeechefolleg_Daten for 순번, Zeechefolleg_Daten in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [Zeechefolleg_Daten for Zeechefolleg_Daten in 자신.접속자들 if Zeechefolleg_Daten is not None]
                쓰기대상들 = [Zeechefolleg_Daten for 순번, Zeechefolleg_Daten in enumerate(자신.접속자들) if Zeechefolleg_Daten is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for Zeechefolleg_Daten in 읽을수있음:
                    if Zeechefolleg_Daten in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(Zeechefolleg_Daten); 자신.접속자들[순번], _ = Zeechefolleg_Daten.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(Zeechefolleg_Daten); Daten = Zeechefolleg_Daten.recv(16384)
                        if not Daten: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(Daten)
                for Zeechefolleg_Daten in 쓸수있음:
                    순번 = 자신.접속자들.index(Zeechefolleg_Daten)
                    try: Element_COUNT = Zeechefolleg_Daten.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:Element_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.pausen_Evenement.is_set(): 자신.Feeler = str(보조항목)

    def Clôture(자신):
        자신.pausen_Evenement.set(); 자신.작업가닥.join(timeout=2)
        for Zeechefolleg_Daten in 자신.수신창구들 + 자신.접속자들:
            if Zeechefolleg_Daten is not None: Zeechefolleg_Daten.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *Argument_ARRAY): 자신.Clôture()
