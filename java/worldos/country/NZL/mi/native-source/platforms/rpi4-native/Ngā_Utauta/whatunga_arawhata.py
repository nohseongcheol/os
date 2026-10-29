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

mīhini_ADDRESS = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Wāhitau_ipurangi_uara = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class whatunga_arawhata:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), hopu=False, manuhiri_ADDRESS=None, taurima_ADDRESS='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        manuhiri_ADDRESS = manuhiri_ADDRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, manuhiri_ADDRESS)
        ADDRESS=ipaddress.IPv4Address(manuhiri_ADDRESS)
        자신.manuhiri_ADDRESS=str(ADDRESS); 자신.현재주소=ADDRESS.packed
        ADDRESS=ipaddress.IPv4Address(taurima_ADDRESS)
        if ADDRESS.is_multicast or str(ADDRESS)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.taurima_ADDRESS=str(ADDRESS)
        자신.hopu = hopu; 자신.tapeke_hauroki_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', raraunga_tūranga) for raraunga_tūranga in range(50000,50008)}
        for ture_uara in 전달규칙들:
            ara_wae = ture_uara.split(':')
            if len(ara_wae) != 3 or ara_wae[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, taurima, manuhiri = ara_wae[0], int(ara_wae[1]), int(ara_wae[2])
            if not 1024 <= taurima <= 65535 or not 1 <= manuhiri <= 65535 or (통신규약, taurima) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ture_uara)
            사용중주소.add((통신규약, taurima)); 자신.전달규칙들.append((통신규약, taurima, manuhiri))
        자신.수신창구들 = []
        for _ in range(2):
            tūmau_uara = socket.socket()
            tūmau_uara.bind(('127.0.0.1', 0)); tūmau_uara.listen(1); tūmau_uara.setblocking(False)
            자신.수신창구들.append(tūmau_uara)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Itarangi = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.tatari_hui = threading.Event(); 자신.Pōhēhē = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Porohita_uara, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Itarangi_kawe = [aho_raraunga.getsockname()[1] for aho_raraunga in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.manuhiri_ADDRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.manuhiri_ADDRESS)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.manuhiri_ADDRESS)
        for 통신규약, taurima, manuhiri in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, taurima, 자신.manuhiri_ADDRESS, manuhiri)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.taurima_ADDRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Itarangi_kawe),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pākete_raraunga):
        자신.대기중[1] += struct.pack('!I', len(pākete_raraunga)) + pākete_raraunga

    def tapeke_hauroki_pākete(자신, 방향, pākete_raraunga):
        if not 자신.hopu or len(pākete_raraunga)<20: return
        OFFSET_uara=(pākete_raraunga[0]&15)*4
        tāurunga_uara={'time':time.monotonic(),'direction':방향,'bytes':len(pākete_raraunga),'protocol':pākete_raraunga[9]}
        if pākete_raraunga[9]==6 and len(pākete_raraunga)>=OFFSET_uara+20:
            원본자료,ūnga_raraunga_ADDRESS,순서번호,확인번호,설정비트,matapihi=struct.unpack_from('!HHIIHH',pākete_raraunga,OFFSET_uara)
            tāurunga_uara.update(source=원본자료,destination=ūnga_raraunga_ADDRESS,seq=순서번호,ack=확인번호,flags=설정비트&255,window=matapihi,
                        payload=len(pākete_raraunga)-OFFSET_uara-((pākete_raraunga[OFFSET_uara+12]>>4)*4))
        자신.tapeke_hauroki_LOG.append(tāurunga_uara)
        if len(자신.tapeke_hauroki_LOG)>2048: del 자신.tapeke_hauroki_LOG[:1024]

    def 직렬전문입력(자신, raraunga):
        for waehere_pūāhua in raraunga:
            if waehere_pūāhua == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADDRESS=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADDRESS)))
                            자신.현재주소=ADDRESS
                        except ValueError:
                            pass
                    자신.tapeke_hauroki_pākete('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + mīhini_ADDRESS + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif waehere_pūāhua == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if waehere_pūāhua not in (220, 221): 자신.잘못됨 = True
                    waehere_pūāhua = 192 if waehere_pūāhua == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(waehere_pūāhua)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, raraunga):
        자신.Itarangi += raraunga
        while len(자신.Itarangi) >= 4:
            tuemi_COUNT = struct.unpack_from('!I', 자신.Itarangi)[0]
            if tuemi_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Itarangi) < tuemi_COUNT + 4: return
            실행틀 = bytes(자신.Itarangi[4:4+tuemi_COUNT]); del 자신.Itarangi[:4+tuemi_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ADDRESS_taumira_pākete = 실행틀[14:42]
                if ADDRESS_taumira_pākete[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADDRESS_taumira_pākete[24:28] == 자신.현재주소:
                    응답자료 = ADDRESS_taumira_pākete[:6] + b'\x00\x02' + mīhini_ADDRESS + 자신.현재주소 + ADDRESS_taumira_pākete[8:18]
                    자신.실행틀(실행틀[6:12] + mīhini_ADDRESS + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                pākete_raraunga = 실행틀[14:]
                자신.tapeke_hauroki_pākete('to_guest',pākete_raraunga)
                자신.대기중[0] += b'\xc0' + pākete_raraunga.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Porohita_uara(자신):
        try:
            while not 자신.tatari_hui.is_set():
                읽기대상들 = [aho_raraunga for 순번, aho_raraunga in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [aho_raraunga for aho_raraunga in 자신.접속자들 if aho_raraunga is not None]
                쓰기대상들 = [aho_raraunga for 순번, aho_raraunga in enumerate(자신.접속자들) if aho_raraunga is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for aho_raraunga in 읽을수있음:
                    if aho_raraunga in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(aho_raraunga); 자신.접속자들[순번], _ = aho_raraunga.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(aho_raraunga); raraunga = aho_raraunga.recv(16384)
                        if not raraunga: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(raraunga)
                for aho_raraunga in 쓸수있음:
                    순번 = 자신.접속자들.index(aho_raraunga)
                    try: tuemi_COUNT = aho_raraunga.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:tuemi_COUNT]
                if any(len(SECOND_uara) > 1024 * 1024 for SECOND_uara in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.tatari_hui.is_set(): 자신.Pōhēhē = str(보조항목)

    def Kati(자신):
        자신.tatari_hui.set(); 자신.작업가닥.join(timeout=2)
        for aho_raraunga in 자신.수신창구들 + 자신.접속자들:
            if aho_raraunga is not None: aho_raraunga.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *tohenga_HUĀNGA): 자신.Kati()
