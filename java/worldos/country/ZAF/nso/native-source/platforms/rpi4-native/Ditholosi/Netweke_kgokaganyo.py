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

atrese_ya_kgonthe = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
atrese_ya_Inthanete_boleng = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Netweke_kgokaganyo:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), tšea=False, moeng_atrese=None, go_nea_ditirelo_atrese='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        moeng_atrese = moeng_atrese or 자신.ip_config['IP']
        qemu_network(자신.ip_config, moeng_atrese)
        atrese=ipaddress.IPv4Address(moeng_atrese)
        자신.moeng_atrese=str(atrese); 자신.현재주소=atrese.packed
        atrese=ipaddress.IPv4Address(go_nea_ditirelo_atrese)
        if atrese.is_multicast or str(atrese)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.go_nea_ditirelo_atrese=str(atrese)
        자신.tšea = tšea; 자신.latišiša_pego = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for filthara_boleng in 전달규칙들:
            tsela_karolo = filthara_boleng.split(':')
            if len(tsela_karolo) != 3 or tsela_karolo[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, go_nea_ditirelo, moeng = tsela_karolo[0], int(tsela_karolo[1]), int(tsela_karolo[2])
            if not 1024 <= go_nea_ditirelo <= 65535 or not 1 <= moeng <= 65535 or (통신규약, go_nea_ditirelo) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filthara_boleng)
            사용중주소.add((통신규약, go_nea_ditirelo)); 자신.전달규칙들.append((통신규약, go_nea_ditirelo, moeng))
        자신.수신창구들 = []
        for _ in range(2):
            seba_boleng = socket.socket()
            seba_boleng.bind(('127.0.0.1', 0)); seba_boleng.listen(1); seba_boleng.setblocking(False)
            자신.수신창구들.append(seba_boleng)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.Ethenete = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.emiša_nakwana_tiragalo = threading.Event(); 자신.Phošo = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.sediko_boleng, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethenete_phote = [molokoloko_data.getsockname()[1] for molokoloko_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.moeng_atrese) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.moeng_atrese)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.moeng_atrese)
        for 통신규약, go_nea_ditirelo, moeng in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, go_nea_ditirelo, 자신.moeng_atrese, moeng)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.go_nea_ditirelo_atrese+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethenete_phote),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, sephuthelwana_data):
        자신.대기중[1] += struct.pack('!I', len(sephuthelwana_data)) + sephuthelwana_data

    def latišiša_sephuthelwana(자신, 방향, sephuthelwana_data):
        if not 자신.tšea or len(sephuthelwana_data)<20: return
        E_Šetšego_boleng=(sephuthelwana_data[0]&15)*4
        go_tsenya_tshedimošo_boleng={'time':time.monotonic(),'direction':방향,'bytes':len(sephuthelwana_data),'protocol':sephuthelwana_data[9]}
        if sephuthelwana_data[9]==6 and len(sephuthelwana_data)>=E_Šetšego_boleng+20:
            원본자료,boyo_data_atrese,순서번호,확인번호,설정비트,lefastere=struct.unpack_from('!HHIIHH',sephuthelwana_data,E_Šetšego_boleng)
            go_tsenya_tshedimošo_boleng.update(source=원본자료,destination=boyo_data_atrese,seq=순서번호,ack=확인번호,flags=설정비트&255,window=lefastere,
                        payload=len(sephuthelwana_data)-E_Šetšego_boleng-((sephuthelwana_data[E_Šetšego_boleng+12]>>4)*4))
        자신.latišiša_pego.append(go_tsenya_tshedimošo_boleng)
        if len(자신.latišiša_pego)>2048: del 자신.latišiša_pego[:1024]

    def 직렬전문입력(자신, data):
        for khouto_ya_tlhaka in data:
            if khouto_ya_tlhaka == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        atrese=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(atrese)))
                            자신.현재주소=atrese
                        except ValueError:
                            pass
                    자신.latišiša_sephuthelwana('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + atrese_ya_kgonthe + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif khouto_ya_tlhaka == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if khouto_ya_tlhaka not in (220, 221): 자신.잘못됨 = True
                    khouto_ya_tlhaka = 192 if khouto_ya_tlhaka == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(khouto_ya_tlhaka)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, data):
        자신.Ethenete += data
        while len(자신.Ethenete) >= 4:
            개수 = struct.unpack_from('!I', 자신.Ethenete)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethenete) < 개수 + 4: return
            실행틀 = bytes(자신.Ethenete[4:4+개수]); del 자신.Ethenete[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                atrese_sephetho_sephuthelwana = 실행틀[14:42]
                if atrese_sephetho_sephuthelwana[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and atrese_sephetho_sephuthelwana[24:28] == 자신.현재주소:
                    응답자료 = atrese_sephetho_sephuthelwana[:6] + b'\x00\x02' + atrese_ya_kgonthe + 자신.현재주소 + atrese_sephetho_sephuthelwana[8:18]
                    자신.실행틀(실행틀[6:12] + atrese_ya_kgonthe + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                sephuthelwana_data = 실행틀[14:]
                자신.latišiša_sephuthelwana('to_guest',sephuthelwana_data)
                자신.대기중[0] += b'\xc0' + sephuthelwana_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def sediko_boleng(자신):
        try:
            while not 자신.emiša_nakwana_tiragalo.is_set():
                읽기대상들 = [molokoloko_data for 순번, molokoloko_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [molokoloko_data for molokoloko_data in 자신.접속자들 if molokoloko_data is not None]
                쓰기대상들 = [molokoloko_data for 순번, molokoloko_data in enumerate(자신.접속자들) if molokoloko_data is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for molokoloko_data in 읽을수있음:
                    if molokoloko_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(molokoloko_data); 자신.접속자들[순번], _ = molokoloko_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(molokoloko_data); data = molokoloko_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(data)
                for molokoloko_data in 쓸수있음:
                    순번 = 자신.접속자들.index(molokoloko_data)
                    try: 개수 = molokoloko_data.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.emiša_nakwana_tiragalo.is_set(): 자신.Phošo = str(보조항목)

    def Tswalela(자신):
        자신.emiša_nakwana_tiragalo.set(); 자신.작업가닥.join(timeout=2)
        for molokoloko_data in 자신.수신창구들 + 자신.접속자들:
            if molokoloko_data is not None: molokoloko_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *akumente_arei): 자신.Tswalela()
