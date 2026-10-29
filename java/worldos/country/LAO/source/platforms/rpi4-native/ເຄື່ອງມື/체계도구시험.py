#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ 자체 커널의 IP/ICMP, ສະຖານະ_ຄ່າ ຄິວຣີ_ຄ່າ, 현지어 ຄໍາສັ່ງ_1f12b8e2, 게스트 ອອກ_ແອັບ ຮັບ_ຮອງ."""
import argparse
import ftplib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import selectors
import signal
import socket
import subprocess
import sys
import tempfile
import time


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ_48ee4b1b=argparse.ArgumentParser();ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--edition',type=Path);ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--output',type=Path);ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    ໂຄງ_ການ_ເລກຮາກ=Path(__file__).resolve().parents[1];ການຕັ້ງຄ່າ={};ຊື່_ຕາຕະລາງ={}
    if 인수.edition:
        나라=인수.edition.resolve();ການຕັ້ງຄ່າ=json.loads((나라/'native.json').read_text());ຊື່_ຕາຕະລາງ=ການຕັ້ງຄ່າ['identifiers'];ໂຄງ_ການ_ເລກຮາກ=나라/ການຕັ້ງຄ່າ['source']/ການຕັ້ງຄ່າ['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ໂຮສ=나라/'host/qemu'
        if ໂຮສ.is_file():os.environ['QEMU_AARCH64']=str(ໂຮສ)
    ເຄື່ອງມື=ໂຄງ_ການ_ເລກຮາກ/Path(ການຕັ້ງຄ່າ.get('runner','ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py')).parent
    sys.path.insert(0,str(ເຄື່ອງມື))
    def 읽기(ຊື່):
        ທາງໂຄຈອນ=ເຄື່ອງມື/(ຊື່_ຕາຕະລາງ.get(ຊື່,ຊື່)+'.py');ສັນຍາ_ຄ່າ=importlib.util.spec_from_file_location('test_'+ຊື່,str(ທາງໂຄຈອນ));ໂມດູນ_ຄ່າ=importlib.util.module_from_spec(ສັນຍາ_ຄ່າ);ສັນຍາ_ຄ່າ.loader.exec_module(ໂມດູນ_ຄ່າ);return ໂມດູນ_ຄ່າ
    실행모듈=읽기('ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ');ເຄືອຂ່າຍ_ໂມດູນ=읽기('ເຄືອຂ່າຍ_ຕົວເຊື່ອມ');ຄໍາສັ່ງ_1f12b8e2=getattr(실행모듈,ຊື່_ຕາຕະລາງ.get('ຄໍາສັ່ງ_1f12b8e2','ຄໍາສັ່ງ_1f12b8e2'));ຕົວເຊື່ອມ_ພິມ=getattr(ເຄືອຂ່າຍ_ໂມດູນ,ຊື່_ຕາຕະລາງ.get('ເຄືອຂ່າຍ_ຕົວເຊື່ອມ','ເຄືອຂ່າຍ_ຕົວເຊື່ອມ'))
    ຊື່ແທນ_ຄ່າ=ການຕັ້ງຄ່າ.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ທີ່ຢູ່_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'ລາຍການ_ຂໍ້ມູນຊ່ວຍ'})
    sys.path.insert(0,str(ໂຄງ_ການ_ເລກຮາກ/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(ໂຄງ_ການ_ເລກຮາກ);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or ໂຄງ_ການ_ເລກຮາກ/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    ລາຍງານ_ຄ່າ={'passed':False,'country':ການຕັ້ງຄ່າ.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    ບັນທຶກ_ແຖວ=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        ຄວບຄຸມ_ທາງໂຄຈອນ=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ຊອກຫາ_ຄ່າ:ຊອກຫາ_ຄ່າ.bind(('127.0.0.1',0));ຫມາຍເລກພອດ=ຊອກຫາ_ຄ່າ.getsockname()[1]
            if not 50000<=ຫມາຍເລກພອດ<=50007:break
        with ຕົວເຊື່ອມ_ພິມ(ຫມາຍເລກພອດ,ບັນທຶກ_ba7b8054=True,ແຂກ_ອີເມວ=ipTestText('10.0.2.20'),ໂຮສ_ອີເມວ='127.0.0.2') as ຕົວເຊື່ອມ_ຄ່າ:
            ຂະ_ບວນ_ການ_ຄ່າ=subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(ຄວບຄຸມ_ທາງໂຄຈອນ)]+ຕົວເຊື່ອມ_ຄ່າ.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ເລືອກ_ລາຍການ=selectors.DefaultSelector();ເລືອກ_ລາຍການ.register(ຂະ_ບວນ_ການ_ຄ່າ.stdout,selectors.EVENT_READ)
            def 받기(ລາຍການ_ຄ່າ,ແລ່ນ=0,제한=45):
                끝=time.monotonic()+제한
                while ລາຍການ_ຄ່າ not in ບັນທຶກ_ແຖວ[ແລ່ນ:]:
                    if time.monotonic()>끝 or ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None:raise AssertionError('Missing '+repr(ລາຍການ_ຄ່າ)+'\n'+ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8','replace'))
                    for ກະແຈ_ຄ່າ,_ in ເລືອກ_ລາຍການ.select(.1):
                        ຂໍ້ມູນ=ກະແຈ_ຄ່າ.fileobj.read(65536)
                        if ຂໍ້ມູນ:ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
                return ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8','replace').replace('\r\n','\n')
            def ສົ່ງ(ຂໍ້ມູນ):ຂະ_ບວນ_ການ_ຄ່າ.stdin.write(ຂໍ້ມູນ);ຂະ_ບວນ_ການ_ຄ່າ.stdin.flush()
            def ເຊລ(ຂໍ້ຄວາມ):
                ຂໍ້ຄວາມ=ipTestText(ຂໍ້ຄວາມ)
                print(ລາຍງານ_ຄ່າ['country'],ຂໍ້ຄວາມ,flush=True);차례[0]+=1;ລາຍການ_ຄ່າ='__SYSTEM_DONE_'+str(차례[0])+'__';ແລ່ນ=len(ບັນທຶກ_ແຖວ)
                ສົ່ງ((ຂໍ້ຄວາມ+'; echo; echo '+ລາຍການ_ຄ່າ+'\n').encode())
                끝표시=('\r\n'+ລາຍການ_ຄ່າ+'\r\n').encode();받기(끝표시,ແລ່ນ)
                ຈົບ_ຈັດຕໍາແຫນ່ງ=ບັນທຶກ_ແຖວ.index(끝표시,ແລ່ນ)+len(끝표시)
                받기(b'jkoros-native> ',ຈົບ_ຈັດຕໍາແຫນ່ງ)
                return ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8','replace').replace('\r\n','\n')
            def 확인(ຂໍ້ຄວາມ,*값들):
                ຕອບກັບ=ເຊລ(ຂໍ້ຄວາມ)
                for ຄ່າ in 값들:assert ipTestText(ຄ່າ) in ຕອບກັບ,(ຂໍ້ຄວາມ,ຄ່າ,ຕອບກັບ)
                return ຕອບກັບ
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ຂໍ້ມູນຊ່ວຍ_ຄ່າ=확인('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ຊື່ແທນ_ຄ່າ.values():assert 별칭 in ຂໍ້ມູນຊ່ວຍ_ຄ່າ,(별칭,ຂໍ້ມູນຊ່ວຍ_ຄ່າ)
                    확인(ຊື່ແທນ_ຄ່າ['help']+' system','Network / system')
                    확인('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    확인(ຊື່ແທນ_ຄ່າ['ipconfig'],'inet 10.0.2.15');확인('ip addr show','sl0: UP');확인('ifconfig','sl0: UP')
                    for ໃຊ້ບໍ່ໄດ້_ການຕັ້ງຄ່າ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ຂໍ້ຜິດພາດ=확인('ipconfig set '+ໃຊ້ບໍ່ໄດ້_ການຕັ້ງຄ່າ+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ຂໍ້ຜິດພາດ,ຂໍ້ຜິດພາດ
                        확인('ipconfig','inet 10.0.2.15')
                    확인('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    확인(ຊື່ແທນ_ຄ່າ['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    확인('ip link set dev sl0 down','sl0: DOWN');확인('ping -c 1 10.0.2.2; echo STATUS=$?','ຂໍ້ຜິດພາດ -100','STATUS=1')
                    확인('ipconfig up','sl0: UP')
                    확인(ຊື່ແທນ_ຄ່າ['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    확인('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    확인('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');확인(ຊື່ແທນ_ຄ່າ['route'],'10.0.2.2 sl0')
                    확인('ftpd start','FTP listening')
                    확인(ຊື່ແທນ_ຄ່າ['netstat'],'10.0.2.20:21','LISTEN');확인('ss','LISTEN')
                    확인('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ຂໍ້ຜິດພາດ -16')
                    with ftplib.FTP() as ລູກຂ່າຍ_ຄ່າ:
                        ລູກຂ່າຍ_ຄ່າ.connect('127.0.0.2',ຫມາຍເລກພອດ,timeout=20);ລູກຂ່າຍ_ຄ່າ.login();ຂໍ້ມູນ=b'Network address was changed in the guest.\n'
                        ລູກຂ່າຍ_ຄ່າ.storbinary('STOR net-state.txt',io.BytesIO(ຂໍ້ມູນ));받은자료=bytearray();ລູກຂ່າຍ_ຄ່າ.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==ຂໍ້ມູນ;ລູກຂ່າຍ_ຄ່າ.delete('net-state.txt')
                    확인('ftpd stop','FTP stopped');확인('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    ລາຍງານ_ຄ່າ['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(ຂໍ້ຄວາມ):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',ຂໍ້ຄວາມ);assert 찾음,ຂໍ້ຄວາມ;return tuple(map(int,찾음.groups()))
                    전=저장값(확인('df','RAM only'));확인('echo disk-proof > sys-state.txt');후=저장값(확인(ຊື່ແທນ_ຄ່າ['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    확인('rm sys-state.txt');assert 저장값(ເຊລ('df'))==전
                    ຄວາມຈໍາ_ຄ່າ=확인(ຊື່ແທນ_ຄ່າ['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',ຄວາມຈໍາ_ຄ່າ).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    확인(ຊື່ແທນ_ຄ່າ['ps'],'kernel/shell');확인(ຊື່ແທນ_ຄ່າ['uptime'],'seconds')
                    ສະຖານະ_ຂໍ້_ມູນ=확인(ຊື່ແທນ_ຄ່າ['top']+' -n 2','kernel/shell');assert ສະຖານະ_ຂໍ້_ມູນ.count('PID SLOT STATE')==2,ສະຖານະ_ຂໍ້_ມູນ
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    확인('terminal','TERMINAL READY');ແລ່ນ=len(ບັນທຶກ_ແຖວ);ສົ່ງ(b'vi process.txt\n');받기(b'NORMAL',ແລ່ນ)
                    ແລ່ນ=len(ບັນທຶກ_ແຖວ);ສົ່ງ(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',ແລ່ນ)
                    ເຂົ້າໃນ_ລາຍຊື່=확인('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',ເຂົ້າໃນ_ລາຍຊື່);assert 찾음 and int(찾음.group(2))>0,ເຂົ້າໃນ_ລາຍຊື່
                    확인('free','EL0 mapped KiB: '+찾음.group(2))
                    ແລ່ນ=len(ບັນທຶກ_ແຖວ);ສົ່ງ(b'top\n');받기(b'PID SLOT STATE',ແລ່ນ);ສົ່ງ(b'q');받기(b'jkoros-native> ',ແລ່ນ)
                    # Test a multibyte prefix through the real shell completion path.
                    if ຊື່ແທນ_ຄ່າ['df']!='df':
                        ແລ່ນ=len(ບັນທຶກ_ແຖວ);ສົ່ງ((ຊື່ແທນ_ຄ່າ['df'][:-1]+'\t\n').encode());받기(b'RAM only',ແລ່ນ);받기(b'jkoros-native> ',ແລ່ນ)
                    ລາຍງານ_ຄ່າ['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as ຄວບຄຸມ_ຄ່າ:
                    ຄວບຄຸມ_ຄ່າ.settimeout(15);ຄວບຄຸມ_ຄ່າ.connect(str(ຄວບຄຸມ_ທາງໂຄຈອນ));ສະຕຣີມ_ຄ່າ=ຄວບຄຸມ_ຄ່າ.makefile('rwb');json.loads(ສະຕຣີມ_ຄ່າ.readline());ສະຕຣີມ_ຄ່າ.write(b'{"execute":"qmp_capabilities"}\n');ສະຕຣີມ_ຄ່າ.flush()
                    while 'return' not in json.loads(ສະຕຣີມ_ຄ່າ.readline()):pass
                    ສົ່ງ((('poweroff' if 인수.poweroff_only else ຊື່ແທນ_ຄ່າ['poweroff'])+'\n').encode())
                    while True:
                        ງານ=json.loads(ສະຕຣີມ_ຄ່າ.readline())
                        if ງານ.get('event')=='SHUTDOWN':break
                    assert ງານ['data']['guest'] and ງານ['data']['reason']=='guest-shutdown',ງານ
                    assert ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=15)==0
                    ລາຍງານ_ຄ່າ['shutdown']=ງານ;ລາຍງານ_ຄ່າ['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                ລາຍງານ_ຄ່າ['network_trace']=ຕົວເຊື່ອມ_ຄ່າ.추적기록
                assert 인수.poweroff_only or any(ເຂົ້າໃນ_ຄ່າ['protocol']==1 and ເຂົ້າໃນ_ຄ່າ['direction']=='from_guest' for ເຂົ້າໃນ_ຄ່າ in ຕົວເຊື່ອມ_ຄ່າ.추적기록)
                ລາຍງານ_ຄ່າ['passed']=True
            finally:
                if ຂະ_ບວນ_ການ_ຄ່າ.poll() is None:os.killpg(ຂະ_ບວນ_ການ_ຄ່າ.pid,signal.SIGTERM)
                try:ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=10)
                except subprocess.TimeoutExpired:ຂະ_ບວນ_ການ_ຄ່າ.kill();ຂະ_ບວນ_ການ_ຄ່າ.wait()
                ເລືອກ_ລາຍການ.close();(출력/'serial.log').write_bytes(ບັນທຶກ_ແຖວ);(출력/'report.json').write_text(json.dumps(ລາຍງານ_ຄ່າ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({ກະແຈ_ຄ່າ:ຄ່າ for ກະແຈ_ຄ່າ,ຄ່າ in ລາຍງານ_ຄ່າ.items() if ກະແຈ_ຄ່າ!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ແລ່ນ()
