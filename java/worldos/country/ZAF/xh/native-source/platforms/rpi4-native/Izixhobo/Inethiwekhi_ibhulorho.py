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

umatshini_idilesi = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
idilesi_yeintanethi_ixabiso = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Inethiwekhi_ibhulorho:
    def __init__(자신, 파일전송접속번호=2121, 전달규칙들=(), bamba=False, undwendwe_idilesi=None, umsingathi_idilesi='127.0.0.1'):
        if not 1024 <= 파일전송접속번호 <= 65535 or 50000 <= 파일전송접속번호 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.파일전송접속번호 = 파일전송접속번호
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        undwendwe_idilesi = undwendwe_idilesi or 자신.ip_config['IP']
        qemu_network(자신.ip_config, undwendwe_idilesi)
        idilesi=ipaddress.IPv4Address(undwendwe_idilesi)
        자신.undwendwe_idilesi=str(idilesi); 자신.현재주소=idilesi.packed
        idilesi=ipaddress.IPv4Address(umsingathi_idilesi)
        if idilesi.is_multicast or str(idilesi)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.umsingathi_idilesi=str(idilesi)
        자신.bamba = bamba; 자신.ithreyisi_ilog = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', 파일전송접속번호)} | {('tcp', 자료위치) for 자료위치 in range(50000,50008)}
        for umgaqo_ixabiso in 전달규칙들:
            indlela_inxenye_yento = umgaqo_ixabiso.split(':')
            if len(indlela_inxenye_yento) != 3 or indlela_inxenye_yento[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, umsingathi, undwendwe = indlela_inxenye_yento[0], int(indlela_inxenye_yento[1]), int(indlela_inxenye_yento[2])
            if not 1024 <= umsingathi <= 65535 or not 1 <= undwendwe <= 65535 or (통신규약, umsingathi) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + umgaqo_ixabiso)
            사용중주소.add((통신규약, umsingathi)); 자신.전달규칙들.append((통신규약, umsingathi, undwendwe))
        자신.수신창구들 = []
        for _ in range(2):
            iseva_ixabiso = socket.socket()
            iseva_ixabiso.bind(('127.0.0.1', 0)); iseva_ixabiso.listen(1); iseva_ixabiso.setblocking(False)
            자신.수신창구들.append(iseva_ixabiso)
        자신.접속자들 = [None, None]
        자신.대기중 = [bytearray(), bytearray()]
        자신.i_Ithanethi = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.잘못됨 = False
        자신.nqumama_umcimbi = threading.Event(); 자신.Impazamo = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Umjikelo_ixabiso, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, i_Ithanethi_iphothi = [uluhlu_lweekharektha_iingcombolo.getsockname()[1] for uluhlu_lweekharektha_iingcombolo in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.undwendwe_idilesi) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.파일전송접속번호, 자신.undwendwe_idilesi)
        for 접속번호 in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(접속번호, 자신.undwendwe_idilesi)
        for 통신규약, umsingathi, undwendwe in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, umsingathi, 자신.undwendwe_idilesi, undwendwe)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.umsingathi_idilesi+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(i_Ithanethi_iphothi),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, ipakethe_iingcombolo):
        자신.대기중[1] += struct.pack('!I', len(ipakethe_iingcombolo)) + ipakethe_iingcombolo

    def ithreyisi_ipakethe(자신, 방향, ipakethe_iingcombolo):
        if not 자신.bamba or len(ipakethe_iingcombolo)<20: return
        Ukulinganisa_ixabiso=(ipakethe_iingcombolo[0]&15)*4
        ufako_nkcukacha_ixabiso={'time':time.monotonic(),'direction':방향,'bytes':len(ipakethe_iingcombolo),'protocol':ipakethe_iingcombolo[9]}
        if ipakethe_iingcombolo[9]==6 and len(ipakethe_iingcombolo)>=Ukulinganisa_ixabiso+20:
            원본자료,indawo_ekuyiwa_kuyo_iingcombolo_idilesi,순서번호,확인번호,설정비트,i_window=struct.unpack_from('!HHIIHH',ipakethe_iingcombolo,Ukulinganisa_ixabiso)
            ufako_nkcukacha_ixabiso.update(source=원본자료,destination=indawo_ekuyiwa_kuyo_iingcombolo_idilesi,seq=순서번호,ack=확인번호,flags=설정비트&255,window=i_window,
                        payload=len(ipakethe_iingcombolo)-Ukulinganisa_ixabiso-((ipakethe_iingcombolo[Ukulinganisa_ixabiso+12]>>4)*4))
        자신.ithreyisi_ilog.append(ufako_nkcukacha_ixabiso)
        if len(자신.ithreyisi_ilog)>2048: del 자신.ithreyisi_ilog[:1024]

    def 직렬전문입력(자신, iingcombolo):
        for ikhowudi_yekharakhtha in iingcombolo:
            if ikhowudi_yekharakhtha == 192:
                if 자신.직렬전문 and not 자신.잘못됨 and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        idilesi=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(idilesi)))
                            자신.현재주소=idilesi
                        except ValueError:
                            pass
                    자신.ithreyisi_ipakethe('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + umatshini_idilesi + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.잘못됨 = False
            elif ikhowudi_yekharakhtha == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if ikhowudi_yekharakhtha not in (220, 221): 자신.잘못됨 = True
                    ikhowudi_yekharakhtha = 192 if ikhowudi_yekharakhtha == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(ikhowudi_yekharakhtha)
                else: 자신.잘못됨 = True

    def 이더넷입력(자신, iingcombolo):
        자신.i_Ithanethi += iingcombolo
        while len(자신.i_Ithanethi) >= 4:
            개수 = struct.unpack_from('!I', 자신.i_Ithanethi)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.i_Ithanethi) < 개수 + 4: return
            실행틀 = bytes(자신.i_Ithanethi[4:4+개수]); del 자신.i_Ithanethi[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                idilesi_isisombululo_ipakethe = 실행틀[14:42]
                if idilesi_isisombululo_ipakethe[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and idilesi_isisombululo_ipakethe[24:28] == 자신.현재주소:
                    응답자료 = idilesi_isisombululo_ipakethe[:6] + b'\x00\x02' + umatshini_idilesi + 자신.현재주소 + idilesi_isisombululo_ipakethe[8:18]
                    자신.실행틀(실행틀[6:12] + umatshini_idilesi + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                ipakethe_iingcombolo = 실행틀[14:]
                자신.ithreyisi_ipakethe('to_guest',ipakethe_iingcombolo)
                자신.대기중[0] += b'\xc0' + ipakethe_iingcombolo.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Umjikelo_ixabiso(자신):
        try:
            while not 자신.nqumama_umcimbi.is_set():
                읽기대상들 = [uluhlu_lweekharektha_iingcombolo for 순번, uluhlu_lweekharektha_iingcombolo in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [uluhlu_lweekharektha_iingcombolo for uluhlu_lweekharektha_iingcombolo in 자신.접속자들 if uluhlu_lweekharektha_iingcombolo is not None]
                쓰기대상들 = [uluhlu_lweekharektha_iingcombolo for 순번, uluhlu_lweekharektha_iingcombolo in enumerate(자신.접속자들) if uluhlu_lweekharektha_iingcombolo is not None and 자신.대기중[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for uluhlu_lweekharektha_iingcombolo in 읽을수있음:
                    if uluhlu_lweekharektha_iingcombolo in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(uluhlu_lweekharektha_iingcombolo); 자신.접속자들[순번], _ = uluhlu_lweekharektha_iingcombolo.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(uluhlu_lweekharektha_iingcombolo); iingcombolo = uluhlu_lweekharektha_iingcombolo.recv(16384)
                        if not iingcombolo: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(iingcombolo)
                for uluhlu_lweekharektha_iingcombolo in 쓸수있음:
                    순번 = 자신.접속자들.index(uluhlu_lweekharektha_iingcombolo)
                    try: 개수 = uluhlu_lweekharektha_iingcombolo.send(자신.대기중[순번])
                    except BlockingIOError: continue
                    del 자신.대기중[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.대기중):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.nqumama_umcimbi.is_set(): 자신.Impazamo = str(보조항목)

    def Vala(자신):
        자신.nqumama_umcimbi.set(); 자신.작업가닥.join(timeout=2)
        for uluhlu_lweekharektha_iingcombolo in 자신.수신창구들 + 자신.접속자들:
            if uluhlu_lweekharektha_iingcombolo is not None: uluhlu_lweekharektha_iingcombolo.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *isiniki_myalelo_ULUHLU): 자신.Vala()
