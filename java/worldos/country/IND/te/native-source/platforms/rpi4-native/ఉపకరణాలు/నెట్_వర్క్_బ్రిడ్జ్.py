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

యంత్రం_ఇమెయిల్ = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
ఇంటర్నెట్_చిరునామా_మూల్యం = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class నెట్_వర్క్_బ్రిడ్జ్:
    def __init__(자신, ఫైలు_బదిలీ_పోర్ట్_సంఖ్య=2121, 전달규칙들=(), సంగ్రహణ=False, అతిథి_ఇమెయిల్=None, హోస్ట్_ఇమెయిల్='127.0.0.1'):
        if not 1024 <= ఫైలు_బదిలీ_పోర్ట్_సంఖ్య <= 65535 or 50000 <= ఫైలు_బదిలీ_పోర్ట్_సంఖ్య <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ఫైలు_బదిలీ_పోర్ట్_సంఖ్య = ఫైలు_బదిలీ_పోర్ట్_సంఖ్య
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        అతిథి_ఇమెయిల్ = అతిథి_ఇమెయిల్ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, అతిథి_ఇమెయిల్)
        ఇమెయిల్=ipaddress.IPv4Address(అతిథి_ఇమెయిల్)
        자신.అతిథి_ఇమెయిల్=str(ఇమెయిల్); 자신.현재주소=ఇమెయిల్.packed
        ఇమెయిల్=ipaddress.IPv4Address(హోస్ట్_ఇమెయిల్)
        if ఇమెయిల్.is_multicast or str(ఇమెయిల్)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.హోస్ట్_ఇమెయిల్=str(ఇమెయిల్)
        자신.సంగ్రహణ = సంగ్రహణ; 자신.జాడ_లాగ్ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ఫైలు_బదిలీ_పోర్ట్_సంఖ్య)} | {('tcp', డేటా_స్థాయి) for డేటా_స్థాయి in range(50000,50008)}
        for నియమం_మూల్యం in 전달규칙들:
            పథం_భాగం = నియమం_మూల్యం.split(':')
            if len(పథం_భాగం) != 3 or పథం_భాగం[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, హోస్ట్, అతిథి = పథం_భాగం[0], int(పథం_భాగం[1]), int(పథం_భాగం[2])
            if not 1024 <= హోస్ట్ <= 65535 or not 1 <= అతిథి <= 65535 or (통신규약, హోస్ట్) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + నియమం_మూల్యం)
            사용중주소.add((통신규약, హోస్ట్)); 자신.전달규칙들.append((통신규약, హోస్ట్, అతిథి))
        자신.수신창구들 = []
        for _ in range(2):
            సర్వర్_మూల్యం = socket.socket()
            సర్వర్_మూల్యం.bind(('127.0.0.1', 0)); సర్వర్_మూల్యం.listen(1); సర్వర్_మూల్యం.setblocking(False)
            자신.수신창구들.append(సర్వర్_మూల్యం)
        자신.접속자들 = [None, None]
        자신.సమాచార_టెక్నాలజీ_పెండింగ్ = [bytearray(), bytearray()]
        자신.ఇథర్నెట్ = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.సమాచార_టెక్నాలజీ_చెల్లని = False
        자신.నిలుపు_ఈవెంట్ = threading.Event(); 자신.దోషం = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.చక్రం_మూల్యం, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ఇథర్నెట్_పోర్టు = [అక్షరసరం_డేటా.getsockname()[1] for అక్షరసరం_డేటా in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.అతిథి_ఇమెయిల్) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ఫైలు_బదిలీ_పోర్ట్_సంఖ్య, 자신.అతిథి_ఇమెయిల్)
        for పోర్ట్_సంఖ్య in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(పోర్ట్_సంఖ్య, 자신.అతిథి_ఇమెయిల్)
        for 통신규약, హోస్ట్, అతిథి in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, హోస్ట్, 자신.అతిథి_ఇమెయిల్, అతిథి)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.హోస్ట్_ఇమెయిల్+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ఇథర్నెట్_పోర్టు),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, ప్యాకెట్_డేటా):
        자신.సమాచార_టెక్నాలజీ_పెండింగ్[1] += struct.pack('!I', len(ప్యాకెట్_డేటా)) + ప్యాకెట్_డేటా

    def జాడ_ప్యాకెట్(자신, 방향, ప్యాకెట్_డేటా):
        if not 자신.సంగ్రహణ or len(ప్యాకెట్_డేటా)<20: return
        ఆఫ్_సెట్_మూల్యం=(ప్యాకెట్_డేటా[0]&15)*4
        ప్రవేశం_మూల్యం={'time':time.monotonic(),'direction':방향,'bytes':len(ప్యాకెట్_డేటా),'protocol':ప్యాకెట్_డేటా[9]}
        if ప్యాకెట్_డేటా[9]==6 and len(ప్యాకెట్_డేటా)>=ఆఫ్_సెట్_మూల్యం+20:
            원본자료,గమ్యం_డేటా_ఇమెయిల్,순서번호,확인번호,నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ,విండో=struct.unpack_from('!HHIIHH',ప్యాకెట్_డేటా,ఆఫ్_సెట్_మూల్యం)
            ప్రవేశం_మూల్యం.update(source=원본자료,destination=గమ్యం_డేటా_ఇమెయిల్,seq=순서번호,ack=확인번호,flags=నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ&255,window=విండో,
                        payload=len(ప్యాకెట్_డేటా)-ఆఫ్_సెట్_మూల్యం-((ప్యాకెట్_డేటా[ఆఫ్_సెట్_మూల్యం+12]>>4)*4))
        자신.జాడ_లాగ్.append(ప్రవేశం_మూల్యం)
        if len(자신.జాడ_లాగ్)>2048: del 자신.జాడ_లాగ్[:1024]

    def 직렬전문입력(자신, డేటా):
        for అక్షర_కోడ్ in డేటా:
            if అక్షర_కోడ్ == 192:
                if 자신.직렬전문 and not 자신.సమాచార_టెక్నాలజీ_చెల్లని and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ఇమెయిల్=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ఇమెయిల్)))
                            자신.현재주소=ఇమెయిల్
                        except ValueError:
                            pass
                    자신.జాడ_ప్యాకెట్('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + యంత్రం_ఇమెయిల్ + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.సమాచార_టెక్నాలజీ_చెల్లని = False
            elif అక్షర_కోడ్ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if అక్షర_కోడ్ not in (220, 221): 자신.సమాచార_టెక్నాలజీ_చెల్లని = True
                    అక్షర_కోడ్ = 192 if అక్షర_కోడ్ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(అక్షర_కోడ్)
                else: 자신.సమాచార_టెక్నాలజీ_చెల్లని = True

    def 이더넷입력(자신, డేటా):
        자신.ఇథర్నెట్ += డేటా
        while len(자신.ఇథర్నెట్) >= 4:
            개수 = struct.unpack_from('!I', 자신.ఇథర్నెట్)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ఇథర్నెట్) < 개수 + 4: return
            실행틀 = bytes(자신.ఇథర్నెట్[4:4+개수]); del 자신.ఇథర్నెట్[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ఇమెయిల్_స్పష్టత_ప్యాకెట్ = 실행틀[14:42]
                if ఇమెయిల్_స్పష్టత_ప్యాకెట్[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ఇమెయిల్_స్పష్టత_ప్యాకెట్[24:28] == 자신.현재주소:
                    응답자료 = ఇమెయిల్_స్పష్టత_ప్యాకెట్[:6] + b'\x00\x02' + యంత్రం_ఇమెయిల్ + 자신.현재주소 + ఇమెయిల్_స్పష్టత_ప్యాకెట్[8:18]
                    자신.실행틀(실행틀[6:12] + యంత్రం_ఇమెయిల్ + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                ప్యాకెట్_డేటా = 실행틀[14:]
                자신.జాడ_ప్యాకెట్('to_guest',ప్యాకెట్_డేటా)
                자신.సమాచార_టెక్నాలజీ_పెండింగ్[0] += b'\xc0' + ప్యాకెట్_డేటా.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def చక్రం_మూల్యం(자신):
        try:
            while not 자신.నిలుపు_ఈవెంట్.is_set():
                읽기대상들 = [అక్షరసరం_డేటా for 순번, అక్షరసరం_డేటా in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [అక్షరసరం_డేటా for అక్షరసరం_డేటా in 자신.접속자들 if అక్షరసరం_డేటా is not None]
                쓰기대상들 = [అక్షరసరం_డేటా for 순번, అక్షరసరం_డేటా in enumerate(자신.접속자들) if అక్షరసరం_డేటా is not None and 자신.సమాచార_టెక్నాలజీ_పెండింగ్[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for అక్షరసరం_డేటా in 읽을수있음:
                    if అక్షరసరం_డేటా in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(అక్షరసరం_డేటా); 자신.접속자들[순번], _ = అక్షరసరం_డేటా.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(అక్షరసరం_డేటా); డేటా = అక్షరసరం_డేటా.recv(16384)
                        if not డేటా: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(డేటా)
                for అక్షరసరం_డేటా in 쓸수있음:
                    순번 = 자신.접속자들.index(అక్షరసరం_డేటా)
                    try: 개수 = అక్షరసరం_డేటా.send(자신.సమాచార_టెక్నాలజీ_పెండింగ్[순번])
                    except BlockingIOError: continue
                    del 자신.సమాచార_టెక్నాలజీ_పెండింగ్[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.సమాచార_టెక్నాలజీ_పెండింగ్):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.నిలుపు_ఈవెంట్.is_set(): 자신.దోషం = str(보조항목)

    def మూసివేయి(자신):
        자신.నిలుపు_ఈవెంట్.set(); 자신.작업가닥.join(timeout=2)
        for అక్షరసరం_డేటా in 자신.수신창구들 + 자신.접속자들:
            if అక్షరసరం_డేటా is not None: అక్షరసరం_డేటా.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *కారకం_శ్రేణి): 자신.మూసివేయి()
