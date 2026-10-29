#!/usr/bin/env python3
"""sebenar_data Asli 커널의 IP/ICMP, status_VALUE pertanyaan_VALUE, 현지어 Perintah, 게스트 Keluar_aplikasi sahkan."""
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


def Jalan():
    penghurai_48ee4b1b=argparse.ArgumentParser();penghurai_48ee4b1b.add_argument('--edition',type=Path);penghurai_48ee4b1b.add_argument('--output',type=Path);penghurai_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=penghurai_48ee4b1b.parse_args()
    projek_akar=Path(__file__).resolve().parents[1];Tetapan={};nama_jadual={}
    if 인수.edition:
        나라=인수.edition.resolve();Tetapan=json.loads((나라/'native.json').read_text());nama_jadual=Tetapan['identifiers'];projek_akar=나라/Tetapan['source']/Tetapan['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        hos=나라/'host/qemu'
        if hos.is_file():os.environ['QEMU_AARCH64']=str(hos)
    alat=projek_akar/Path(Tetapan.get('runner','alat/laksanakan_perintah.py')).parent
    sys.path.insert(0,str(alat))
    def Baca(Nama):
        LALUAN=alat/(nama_jadual.get(Nama,Nama)+'.py');kes_VALUE=importlib.util.spec_from_file_location('test_'+Nama,str(LALUAN));modul_VALUE=importlib.util.module_from_spec(kes_VALUE);kes_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Baca('laksanakan_perintah');rangkaian_modul=Baca('rangkaian_penghubung');Perintah=getattr(실행모듈,nama_jadual.get('Perintah','Perintah'));penghubung_TYPE=getattr(rangkaian_modul,nama_jadual.get('rangkaian_penghubung','rangkaian_penghubung'))
    alias_VALUE=Tetapan.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'alamat_IP','ping':'ujian_respons','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'paparkan_bantuan'})
    sys.path.insert(0,str(projek_akar/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(projek_akar);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or projek_akar/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    lapor_VALUE={'passed':False,'country':Tetapan.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_baris=bytearray();jujukan_VALUE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kawalan_laluan=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Cari_VALUE:Cari_VALUE.bind(('127.0.0.1',0));nombor_port=Cari_VALUE.getsockname()[1]
            if not 50000<=nombor_port<=50007:break
        with penghubung_TYPE(nombor_port,rakam=True,tetamu_e_mel=ipTestText('10.0.2.20'),hos_e_mel='127.0.0.2') as penghubung_VALUE:
            Proses_VALUE=subprocess.Popen(Perintah()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kawalan_laluan)]+penghubung_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            pilih_item=selectors.DefaultSelector();pilih_item.register(Proses_VALUE.stdout,selectors.EVENT_READ)
            def 받기(tayang_VALUE,Jalan=0,제한=45):
                끝=time.monotonic()+제한
                while tayang_VALUE not in LOG_baris[Jalan:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:raise AssertionError('Missing '+repr(tayang_VALUE)+'\n'+LOG_baris[Jalan:].decode('utf-8','replace'))
                    for Kunci_VALUE,_ in pilih_item.select(.1):
                        data=Kunci_VALUE.fileobj.read(65536)
                        if data:LOG_baris.extend(data)
                return LOG_baris[Jalan:].decode('utf-8','replace').replace('\r\n','\n')
            def e_mel_9aee63bd(data):Proses_VALUE.stdin.write(data);Proses_VALUE.stdin.flush()
            def cangkerang(Teks):
                Teks=ipTestText(Teks)
                print(lapor_VALUE['country'],Teks,flush=True);jujukan_VALUE[0]+=1;tayang_VALUE='__SYSTEM_DONE_'+str(jujukan_VALUE[0])+'__';Jalan=len(LOG_baris)
                e_mel_9aee63bd((Teks+'; echo; echo '+tayang_VALUE+'\n').encode())
                tamat_penanda=('\r\n'+tayang_VALUE+'\r\n').encode();받기(tamat_penanda,Jalan)
                tamat_jawatan=LOG_baris.index(tamat_penanda,Jalan)+len(tamat_penanda)
                받기(b'jkoros-native> ',tamat_jawatan)
                return LOG_baris[Jalan:].decode('utf-8','replace').replace('\r\n','\n')
            def tentu_sahkan(Teks,*값들):
                balas=cangkerang(Teks)
                for VALUE in 값들:assert ipTestText(VALUE) in balas,(Teks,VALUE,balas)
                return balas
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    bantu_VALUE=tentu_sahkan('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in bantu_VALUE,(별칭,bantu_VALUE)
                    tentu_sahkan(alias_VALUE['help']+' system','Network / system')
                    tentu_sahkan('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    tentu_sahkan(alias_VALUE['ipconfig'],'inet 10.0.2.15');tentu_sahkan('ip addr show','sl0: UP');tentu_sahkan('ifconfig','sl0: UP')
                    for tak_sah_Seting in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        RALAT=tentu_sahkan('ipconfig set '+tak_sah_Seting+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in RALAT,RALAT
                        tentu_sahkan('ipconfig','inet 10.0.2.15')
                    tentu_sahkan('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    tentu_sahkan(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tentu_sahkan('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    tentu_sahkan('ip link set dev sl0 down','sl0: DOWN');tentu_sahkan('ping -c 1 10.0.2.2; echo STATUS=$?','RALAT -100','STATUS=1')
                    tentu_sahkan('ipconfig up','sl0: UP')
                    tentu_sahkan(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    tentu_sahkan('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    tentu_sahkan('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');tentu_sahkan(alias_VALUE['route'],'10.0.2.2 sl0')
                    tentu_sahkan('ftpd start','FTP listening')
                    tentu_sahkan(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');tentu_sahkan('ss','LISTEN')
                    tentu_sahkan('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','RALAT -16')
                    with ftplib.FTP() as klien_VALUE:
                        klien_VALUE.connect('127.0.0.2',nombor_port,timeout=20);klien_VALUE.login();data=b'Network address was changed in the guest.\n'
                        klien_VALUE.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();klien_VALUE.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;klien_VALUE.delete('net-state.txt')
                    tentu_sahkan('ftpd stop','FTP stopped');tentu_sahkan('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    lapor_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Teks):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Teks);assert 찾음,Teks;return tuple(map(int,찾음.groups()))
                    전=저장값(tentu_sahkan('df','RAM only'));tentu_sahkan('echo disk-proof > sys-state.txt');후=저장값(tentu_sahkan(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    tentu_sahkan('rm sys-state.txt');assert 저장값(cangkerang('df'))==전
                    Memori_VALUE=tentu_sahkan(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memori_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    tentu_sahkan(alias_VALUE['ps'],'kernel/shell');tentu_sahkan(alias_VALUE['uptime'],'seconds')
                    status_info=tentu_sahkan(alias_VALUE['top']+' -n 2','kernel/shell');assert status_info.count('PID SLOT STATE')==2,status_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    tentu_sahkan('terminal','TERMINAL READY');Jalan=len(LOG_baris);e_mel_9aee63bd(b'vi process.txt\n');받기(b'NORMAL',Jalan)
                    Jalan=len(LOG_baris);e_mel_9aee63bd(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Jalan)
                    pemasukan_Senarai=tentu_sahkan('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',pemasukan_Senarai);assert 찾음 and int(찾음.group(2))>0,pemasukan_Senarai
                    tentu_sahkan('free','EL0 mapped KiB: '+찾음.group(2))
                    Jalan=len(LOG_baris);e_mel_9aee63bd(b'top\n');받기(b'PID SLOT STATE',Jalan);e_mel_9aee63bd(b'q');받기(b'jkoros-native> ',Jalan)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        Jalan=len(LOG_baris);e_mel_9aee63bd((alias_VALUE['df'][:-1]+'\t\n').encode());받기(b'RAM only',Jalan);받기(b'jkoros-native> ',Jalan)
                    lapor_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kawalan_VALUE:
                    kawalan_VALUE.settimeout(15);kawalan_VALUE.connect(str(kawalan_laluan));strim_VALUE=kawalan_VALUE.makefile('rwb');json.loads(strim_VALUE.readline());strim_VALUE.write(b'{"execute":"qmp_capabilities"}\n');strim_VALUE.flush()
                    while 'return' not in json.loads(strim_VALUE.readline()):pass
                    e_mel_9aee63bd((('poweroff' if 인수.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        Peristiwa=json.loads(strim_VALUE.readline())
                        if Peristiwa.get('event')=='SHUTDOWN':break
                    assert Peristiwa['data']['guest'] and Peristiwa['data']['reason']=='guest-shutdown',Peristiwa
                    assert Proses_VALUE.wait(timeout=15)==0
                    lapor_VALUE['shutdown']=Peristiwa;lapor_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                lapor_VALUE['network_trace']=penghubung_VALUE.jejak_LOG
                assert 인수.poweroff_only or any(pemasukan_VALUE['protocol']==1 and pemasukan_VALUE['direction']=='from_guest' for pemasukan_VALUE in penghubung_VALUE.jejak_LOG)
                lapor_VALUE['passed']=True
            finally:
                if Proses_VALUE.poll() is None:os.killpg(Proses_VALUE.pid,signal.SIGTERM)
                try:Proses_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
                pilih_item.close();(출력/'serial.log').write_bytes(LOG_baris);(출력/'report.json').write_text(json.dumps(lapor_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Kunci_VALUE:VALUE for Kunci_VALUE,VALUE in lapor_VALUE.items() if Kunci_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Jalan()
