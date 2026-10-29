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

motšhine_aterese = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
aterese_ya_Inthanete_Boleng = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Neteweke_leborogo:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), tshwara=False, moeng_aterese=None, pinagare_aterese='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        moeng_aterese = moeng_aterese or 자신.ip_config['IP']
        qemu_network(자신.ip_config, moeng_aterese)
        aterese=ipaddress.IPv4Address(moeng_aterese)
        자신.moeng_aterese=str(aterese); 자신.ga_jaana_aterese=aterese.packed
        aterese=ipaddress.IPv4Address(pinagare_aterese)
        if aterese.is_multicast or str(aterese)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.pinagare_aterese=str(aterese)
        자신.tshwara = tshwara; 자신.palo_tlhakanyo_rekota = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for molawana_Boleng in 전달규칙들:
            tsela_karolwana = molawana_Boleng.split(':')
            if len(tsela_karolwana) != 3 or tsela_karolwana[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, pinagare, moeng = tsela_karolwana[0], int(tsela_karolwana[1]), int(tsela_karolwana[2])
            if not 1024 <= pinagare <= 65535 or not 1 <= moeng <= 65535 or (통신규약, pinagare) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + molawana_Boleng)
            사용중주소.add((통신규약, pinagare)); 자신.전달규칙들.append((통신규약, pinagare, moeng))
        자신.수신창구들 = []
        for _ in range(2):
            sefara_Boleng = socket.socket()
            sefara_Boleng.bind(('127.0.0.1', 0)); sefara_Boleng.listen(1); sefara_Boleng.setblocking(False)
            자신.수신창구들.append(sefara_Boleng)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ithanete = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.Kgaotsa_tiragalo = threading.Event(); 자신.phoso = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Sediko_Boleng, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ithanete_gorogisetsa = [dikwalwa_tshedimosetso.getsockname()[1] for dikwalwa_tshedimosetso in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.moeng_aterese) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.moeng_aterese)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.moeng_aterese)
        for 통신규약, pinagare, moeng in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, pinagare, 자신.moeng_aterese, moeng)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.pinagare_aterese+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ithanete_gorogisetsa),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, sephuthelwana_tshedimosetso):
        자신.대기중[1] += struct.pack('!I', len(sephuthelwana_tshedimosetso)) + sephuthelwana_tshedimosetso

    def palo_tlhakanyo_sephuthelwana(자신, 방향, sephuthelwana_tshedimosetso):
        if not 자신.tshwara or len(sephuthelwana_tshedimosetso)<20: return
        Baya_ka_Tekatekanyo_Boleng=(sephuthelwana_tshedimosetso[0]&15)*4
        tsenyo_Boleng={'time':time.monotonic(),'direction':방향,'bytes':len(sephuthelwana_tshedimosetso),'protocol':sephuthelwana_tshedimosetso[9]}
        if sephuthelwana_tshedimosetso[9]==6 and len(sephuthelwana_tshedimosetso)>=Baya_ka_Tekatekanyo_Boleng+20:
            원본자료,bogorogelo_tshedimosetso_aterese,순서번호,확인번호,설정비트,fensetere=struct.unpack_from('!HHIIHH',sephuthelwana_tshedimosetso,Baya_ka_Tekatekanyo_Boleng)
            tsenyo_Boleng.update(source=원본자료,destination=bogorogelo_tshedimosetso_aterese,seq=순서번호,ack=확인번호,flags=설정비트&255,window=fensetere,
                        payload=len(sephuthelwana_tshedimosetso)-Baya_ka_Tekatekanyo_Boleng-((sephuthelwana_tshedimosetso[Baya_ka_Tekatekanyo_Boleng+12]>>4)*4))
        자신.palo_tlhakanyo_rekota.append(tsenyo_Boleng)
        if len(자신.palo_tlhakanyo_rekota)>2048: del 자신.palo_tlhakanyo_rekota[:1024]

    def 직렬전문입력(자신, tshedimosetso):
        for khoutuletshwao in tshedimosetso:
            if khoutuletshwao == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        aterese=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(aterese)))
                            자신.ga_jaana_aterese=aterese
                        except ValueError:
                            pass
                    자신.palo_tlhakanyo_sephuthelwana('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + motšhine_aterese + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif khoutuletshwao == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if khoutuletshwao not in (220, 221): 자신.잘못됨 = True
                    khoutuletshwao = 192 if khoutuletshwao == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(khoutuletshwao)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, tshedimosetso):
        자신.Ithanete += tshedimosetso
        while len(자신.Ithanete) >= 4:
            개수 = struct.unpack_from('!I', 자신.Ithanete)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ithanete) < 개수 + 4: return
            실행틀 = bytes(자신.Ithanete[4:4+개수]); del 자신.Ithanete[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                aterese_resolušene_sephuthelwana = 실행틀[14:42]
                if aterese_resolušene_sephuthelwana[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and aterese_resolušene_sephuthelwana[24:28] == 자신.ga_jaana_aterese:
                    응답자료 = aterese_resolušene_sephuthelwana[:6] + b'\x00\x02' + motšhine_aterese + 자신.ga_jaana_aterese + aterese_resolušene_sephuthelwana[8:18]
                    자신.실행틀(실행틀[6:12] + motšhine_aterese + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                sephuthelwana_tshedimosetso = 실행틀[14:]
                자신.palo_tlhakanyo_sephuthelwana('to_guest',sephuthelwana_tshedimosetso)
                자신.대기중[0] += b'\xc0' + sephuthelwana_tshedimosetso.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Sediko_Boleng(자신):
        try:
            while not 자신.Kgaotsa_tiragalo.is_set():
                읽기대상들 = [dikwalwa_tshedimosetso for 순번, dikwalwa_tshedimosetso in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [dikwalwa_tshedimosetso for dikwalwa_tshedimosetso in 자신.접속자들 if dikwalwa_tshedimosetso is not None]
                쓰기대상들 = [dikwalwa_tshedimosetso for 순번, dikwalwa_tshedimosetso in enumerate(자신.접속자들) if dikwalwa_tshedimosetso is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for dikwalwa_tshedimosetso in 읽을수있음:
                    if dikwalwa_tshedimosetso in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(dikwalwa_tshedimosetso); 자신.접속자들[순번], _ = dikwalwa_tshedimosetso.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(dikwalwa_tshedimosetso); tshedimosetso = dikwalwa_tshedimosetso.recv(16384)
                        if not tshedimosetso: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(tshedimosetso)
                for dikwalwa_tshedimosetso in 쓸수있음:
                    순번 = 자신.접속자들.index(dikwalwa_tshedimosetso)
                    try: 개수 = dikwalwa_tshedimosetso.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Kgaotsa_tiragalo.is_set(): 자신.phoso = str(보조항목)

    def tswala(자신):
        자신.Kgaotsa_tiragalo.set(); 자신.작업가닥.join(timeout=2)
        for dikwalwa_tshedimosetso in 자신.수신창구들 + 자신.접속자들:
            if dikwalwa_tshedimosetso is not None: dikwalwa_tshedimosetso.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *Thulaganyo_setlhopha): 자신.tswala()
