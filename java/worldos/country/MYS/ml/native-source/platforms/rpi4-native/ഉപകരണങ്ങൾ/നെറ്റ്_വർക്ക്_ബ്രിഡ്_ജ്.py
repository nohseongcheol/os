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

മെഷീൻ_ഇമെയിൽ = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
ഇന്_റര്_നെറ്റ്_വിലാസം_മൂല്യം = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്:
    def __init__(자신, ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്=2121, 전달규칙들=(), ക്യാപ്_ചർ_ചെയ്യുക=False, അതിഥി_ഇമെയിൽ=None, ഹോസ്റ്റ്_ഇമെയിൽ='127.0.0.1'):
        if not 1024 <= ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര് <= 65535 or 50000 <= ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര് <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര് = ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        അതിഥി_ഇമെയിൽ = അതിഥി_ഇമെയിൽ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, അതിഥി_ഇമെയിൽ)
        ഇമെയിൽ=ipaddress.IPv4Address(അതിഥി_ഇമെയിൽ)
        자신.അതിഥി_ഇമെയിൽ=str(ഇമെയിൽ); 자신.현재주소=ഇമെയിൽ.packed
        ഇമെയിൽ=ipaddress.IPv4Address(ഹോസ്റ്റ്_ഇമെയിൽ)
        if ഇമെയിൽ.is_multicast or str(ഇമെയിൽ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ഹോസ്റ്റ്_ഇമെയിൽ=str(ഇമെയിൽ)
        자신.ക്യാപ്_ചർ_ചെയ്യുക = ക്യാപ്_ചർ_ചെയ്യുക; 자신.ട്രെയ്സ്_ലോഗ് = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്)} | {('tcp', ഡാറ്റാ_പദവി) for ഡാറ്റാ_പദവി in range(50000,50008)}
        for നിയമം_മൂല്യം in 전달규칙들:
            പാത_ഘടകഭാഗം = നിയമം_മൂല്യം.split(':')
            if len(പാത_ഘടകഭാഗം) != 3 or പാത_ഘടകഭാഗം[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ഹോസ്റ്റ്, അതിഥി = പാത_ഘടകഭാഗം[0], int(പാത_ഘടകഭാഗം[1]), int(പാത_ഘടകഭാഗം[2])
            if not 1024 <= ഹോസ്റ്റ് <= 65535 or not 1 <= അതിഥി <= 65535 or (통신규약, ഹോസ്റ്റ്) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + നിയമം_മൂല്യം)
            사용중주소.add((통신규약, ഹോസ്റ്റ്)); 자신.전달규칙들.append((통신규약, ഹോസ്റ്റ്, അതിഥി))
        자신.수신창구들 = []
        for _ in range(2):
            സെര്_വര്_മൂല്യം = socket.socket()
            സെര്_വര്_മൂല്യം.bind(('127.0.0.1', 0)); സെര്_വര്_മൂല്യം.listen(1); സെര്_വര്_മൂല്യം.setblocking(False)
            자신.수신창구들.append(സെര്_വര്_മൂല്യം)
        자신.접속자들 = [None, None]
        자신.വിവര_സാങ്കേതികവിദ്യ_ശേഷിക്കുന്നു = [bytearray(), bytearray()]
        자신.ഇതര്_നെറ്റ് = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.വിവര_സാങ്കേതികവിദ്യ_അസാധുവായ = False
        자신.അല്_പം_നിര്_ത്തുക_ഇവന്റ് = threading.Event(); 자신.പിശക് = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.സൈക്കിൾ_മൂല്യം, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ഇതര്_നെറ്റ്_പോര്_ട്ട് = [സ്ട്രിംഗ്_ഡാറ്റാ.getsockname()[1] for സ്ട്രിംഗ്_ഡാറ്റാ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.അതിഥി_ഇമെയിൽ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്, 자신.അതിഥി_ഇമെയിൽ)
        for പോര്_ട്ട്_നമ്പര് in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(പോര്_ട്ട്_നമ്പര്, 자신.അതിഥി_ഇമെയിൽ)
        for 통신규약, ഹോസ്റ്റ്, അതിഥി in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ഹോസ്റ്റ്, 자신.അതിഥി_ഇമെയിൽ, അതിഥി)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ഹോസ്റ്റ്_ഇമെയിൽ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ഇതര്_നെറ്റ്_പോര്_ട്ട്),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, പാക്കറ്റ്_ഡാറ്റാ):
        자신.വിവര_സാങ്കേതികവിദ്യ_ശേഷിക്കുന്നു[1] += struct.pack('!I', len(പാക്കറ്റ്_ഡാറ്റാ)) + പാക്കറ്റ്_ഡാറ്റാ

    def ട്രെയ്സ്_പാക്കറ്റ്(자신, 방향, പാക്കറ്റ്_ഡാറ്റാ):
        if not 자신.ക്യാപ്_ചർ_ചെയ്യുക or len(പാക്കറ്റ്_ഡാറ്റാ)<20: return
        ഓഫ്_സെറ്റ്_മൂല്യം=(പാക്കറ്റ്_ഡാറ്റാ[0]&15)*4
        എന്_ട്രി_മൂല്യം={'time':time.monotonic(),'direction':방향,'bytes':len(പാക്കറ്റ്_ഡാറ്റാ),'protocol':പാക്കറ്റ്_ഡാറ്റാ[9]}
        if പാക്കറ്റ്_ഡാറ്റാ[9]==6 and len(പാക്കറ്റ്_ഡാറ്റാ)>=ഓഫ്_സെറ്റ്_മൂല്യം+20:
            원본자료,ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ_ഇമെയിൽ,순서번호,확인번호,കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്,ജാലകം=struct.unpack_from('!HHIIHH',പാക്കറ്റ്_ഡാറ്റാ,ഓഫ്_സെറ്റ്_മൂല്യം)
            എന്_ട്രി_മൂല്യം.update(source=원본자료,destination=ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ_ഇമെയിൽ,seq=순서번호,ack=확인번호,flags=കോണ്_ഫിഗറേഷന്_ബാക്_ഗ്രൗണ്ട്_ഇന്റലിജന്റ്_ട്രാൻസ്_ഫർ_സർവീസ്&255,window=ജാലകം,
                        payload=len(പാക്കറ്റ്_ഡാറ്റാ)-ഓഫ്_സെറ്റ്_മൂല്യം-((പാക്കറ്റ്_ഡാറ്റാ[ഓഫ്_സെറ്റ്_മൂല്യം+12]>>4)*4))
        자신.ട്രെയ്സ്_ലോഗ്.append(എന്_ട്രി_മൂല്യം)
        if len(자신.ട്രെയ്സ്_ലോഗ്)>2048: del 자신.ട്രെയ്സ്_ലോഗ്[:1024]

    def 직렬전문입력(자신, ഡാറ്റാ):
        for പ്രതീകകോഡ് in ഡാറ്റാ:
            if പ്രതീകകോഡ് == 192:
                if 자신.직렬전문 and not 자신.വിവര_സാങ്കേതികവിദ്യ_അസാധുവായ and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ഇമെയിൽ=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ഇമെയിൽ)))
                            자신.현재주소=ഇമെയിൽ
                        except ValueError:
                            pass
                    자신.ട്രെയ്സ്_പാക്കറ്റ്('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + മെഷീൻ_ഇമെയിൽ + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.വിവര_സാങ്കേതികവിദ്യ_അസാധുവായ = False
            elif പ്രതീകകോഡ് == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if പ്രതീകകോഡ് not in (220, 221): 자신.വിവര_സാങ്കേതികവിദ്യ_അസാധുവായ = True
                    പ്രതീകകോഡ് = 192 if പ്രതീകകോഡ് == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(പ്രതീകകോഡ്)
                else: 자신.വിവര_സാങ്കേതികവിദ്യ_അസാധുവായ = True

    def 이더넷입력(자신, ഡാറ്റാ):
        자신.ഇതര്_നെറ്റ് += ഡാറ്റാ
        while len(자신.ഇതര്_നെറ്റ്) >= 4:
            개수 = struct.unpack_from('!I', 자신.ഇതര്_നെറ്റ്)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ഇതര്_നെറ്റ്) < 개수 + 4: return
            실행틀 = bytes(자신.ഇതര്_നെറ്റ്[4:4+개수]); del 자신.ഇതര്_നെറ്റ്[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ഇമെയിൽ_റെസലൂഷന്_പാക്കറ്റ് = 실행틀[14:42]
                if ഇമെയിൽ_റെസലൂഷന്_പാക്കറ്റ്[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ഇമെയിൽ_റെസലൂഷന്_പാക്കറ്റ്[24:28] == 자신.현재주소:
                    응답자료 = ഇമെയിൽ_റെസലൂഷന്_പാക്കറ്റ്[:6] + b'\x00\x02' + മെഷീൻ_ഇമെയിൽ + 자신.현재주소 + ഇമെയിൽ_റെസലൂഷന്_പാക്കറ്റ്[8:18]
                    자신.실행틀(실행틀[6:12] + മെഷീൻ_ഇമെയിൽ + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                പാക്കറ്റ്_ഡാറ്റാ = 실행틀[14:]
                자신.ട്രെയ്സ്_പാക്കറ്റ്('to_guest',പാക്കറ്റ്_ഡാറ്റാ)
                자신.വിവര_സാങ്കേതികവിദ്യ_ശേഷിക്കുന്നു[0] += b'\xc0' + പാക്കറ്റ്_ഡാറ്റാ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def സൈക്കിൾ_മൂല്യം(자신):
        try:
            while not 자신.അല്_പം_നിര്_ത്തുക_ഇവന്റ്.is_set():
                읽기대상들 = [സ്ട്രിംഗ്_ഡാറ്റാ for 순번, സ്ട്രിംഗ്_ഡാറ്റാ in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [സ്ട്രിംഗ്_ഡാറ്റാ for സ്ട്രിംഗ്_ഡാറ്റാ in 자신.접속자들 if സ്ട്രിംഗ്_ഡാറ്റാ is not None]
                쓰기대상들 = [സ്ട്രിംഗ്_ഡാറ്റാ for 순번, സ്ട്രിംഗ്_ഡാറ്റാ in enumerate(자신.접속자들) if സ്ട്രിംഗ്_ഡാറ്റാ is not None and 자신.വിവര_സാങ്കേതികവിദ്യ_ശേഷിക്കുന്നു[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for സ്ട്രിംഗ്_ഡാറ്റാ in 읽을수있음:
                    if സ്ട്രിംഗ്_ഡാറ്റാ in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(സ്ട്രിംഗ്_ഡാറ്റാ); 자신.접속자들[순번], _ = സ്ട്രിംഗ്_ഡാറ്റാ.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(സ്ട്രിംഗ്_ഡാറ്റാ); ഡാറ്റാ = സ്ട്രിംഗ്_ഡാറ്റാ.recv(16384)
                        if not ഡാറ്റാ: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ഡാറ്റാ)
                for സ്ട്രിംഗ്_ഡാറ്റാ in 쓸수있음:
                    순번 = 자신.접속자들.index(സ്ട്രിംഗ്_ഡാറ്റാ)
                    try: 개수 = സ്ട്രിംഗ്_ഡാറ്റാ.send(자신.വിവര_സാങ്കേതികവിദ്യ_ശേഷിക്കുന്നു[순번])
                    except BlockingIOError: continue
                    del 자신.വിവര_സാങ്കേതികവിദ്യ_ശേഷിക്കുന്നു[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.വിവര_സാങ്കേതികവിദ്യ_ശേഷിക്കുന്നു):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.അല്_പം_നിര്_ത്തുക_ഇവന്റ്.is_set(): 자신.പിശക് = str(보조항목)

    def അടയ്ക്കു(자신):
        자신.അല്_പം_നിര്_ത്തുക_ഇവന്റ്.set(); 자신.작업가닥.join(timeout=2)
        for സ്ട്രിംഗ്_ഡാറ്റാ in 자신.수신창구들 + 자신.접속자들:
            if സ്ട്രിംഗ്_ഡാറ്റാ is not None: സ്ട്രിംഗ്_ഡാറ്റാ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ആര്_ഗ്യുമെന്_റ്_അരേ): 자신.അടയ്ക്കു()
