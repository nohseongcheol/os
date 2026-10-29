#!/usr/bin/env python3
"""aktual_data Asli 커널의 IP/ICMP, Status_VALUE kueri_VALUE, 현지어 perintah, 게스트 Keluar_apl validasi."""
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


def jalankan():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');argumen=parser_48ee4b1b.parse_args()
    Tugas_akar=Path(__file__).resolve().parents[1];Konfigurasi={};nama_tabel={}
    if argumen.edition:
        나라=argumen.edition.resolve();Konfigurasi=json.loads((나라/'native.json').read_text());nama_tabel=Konfigurasi['identifiers'];Tugas_akar=나라/Konfigurasi['source']/Konfigurasi['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        host=나라/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    alat=Tugas_akar/Path(Konfigurasi.get('runner','alat/Jalankan_perintah.py')).parent
    sys.path.insert(0,str(alat))
    def Baca(Nama_2):
        jalur=alat/(nama_tabel.get(Nama_2,Nama_2)+'.py');kasus_VALUE=importlib.util.spec_from_file_location('test_'+Nama_2,str(jalur));modul_VALUE=importlib.util.module_from_spec(kasus_VALUE);kasus_VALUE.loader.exec_module(modul_VALUE);return modul_VALUE
    실행모듈=Baca('Jalankan_perintah');jaringan_modul=Baca('jaringan_bridge');perintah=getattr(실행모듈,nama_tabel.get('perintah','perintah'));bridge_TYPE=getattr(jaringan_modul,nama_tabel.get('jaringan_bridge','jaringan_bridge'))
    alias_VALUE=Konfigurasi.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'alamat_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'tampilkan_bantuan'})
    sys.path.insert(0,str(Tugas_akar/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Tugas_akar);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    keluaranTeks=argumen.output or Tugas_akar/'build/verification/system-tools';keluaranTeks.mkdir(parents=True,exist_ok=True)
    lapor_VALUE={'passed':False,'country':Konfigurasi.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_baris=bytearray();urutan_VALUE_e9fa7815=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        kontrol_jalur=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Cari_VALUE:Cari_VALUE.bind(('127.0.0.1',0));nomor_port=Cari_VALUE.getsockname()[1]
            if not 50000<=nomor_port<=50007:break
        with bridge_TYPE(nomor_port,ambil=True,tamu_surel=ipTestText('10.0.2.20'),host_surel='127.0.0.2') as bridge_VALUE:
            Proses_VALUE=subprocess.Popen(perintah()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(kontrol_jalur)]+bridge_VALUE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            pilih_item=selectors.DefaultSelector();pilih_item.register(Proses_VALUE.stdout,selectors.EVENT_READ)
            def terima(show_VALUE,jalankan=0,제한=45):
                끝=time.monotonic()+제한
                while show_VALUE not in LOG_baris[jalankan:]:
                    if time.monotonic()>끝 or Proses_VALUE.poll() is not None:raise AssertionError('Missing '+repr(show_VALUE)+'\n'+LOG_baris[jalankan:].decode('utf-8','replace'))
                    for Kunci_VALUE,_ in pilih_item.select(.1):
                        data=Kunci_VALUE.fileobj.read(65536)
                        if data:LOG_baris.extend(data)
                return LOG_baris[jalankan:].decode('utf-8','replace').replace('\r\n','\n')
            def kirim(data):Proses_VALUE.stdin.write(data);Proses_VALUE.stdin.flush()
            def shell(teks):
                teks=ipTestText(teks)
                print(lapor_VALUE['country'],teks,flush=True);urutan_VALUE_e9fa7815[0]+=1;show_VALUE='__SYSTEM_DONE_'+str(urutan_VALUE_e9fa7815[0])+'__';jalankan=len(LOG_baris)
                kirim((teks+'; echo; echo '+show_VALUE+'\n').encode())
                끝표시=('\r\n'+show_VALUE+'\r\n').encode();terima(끝표시,jalankan)
                mengakhiri_posisi=LOG_baris.index(끝표시,jalankan)+len(끝표시)
                terima(b'jkoros-native> ',mengakhiri_posisi)
                return LOG_baris[jalankan:].decode('utf-8','replace').replace('\r\n','\n')
            def periksa(teks,*값들):
                balas=shell(teks)
                for VALUE in 값들:assert ipTestText(VALUE) in balas,(teks,VALUE,balas)
                return balas
            try:
                terima(b'jkoros-native> ')
                if not argumen.poweroff_only:
                    bantuan_VALUE=periksa('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALUE.values():assert 별칭 in bantuan_VALUE,(별칭,bantuan_VALUE)
                    periksa(alias_VALUE['help']+' system','Network / system')
                    periksa('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    periksa(alias_VALUE['ipconfig'],'inet 10.0.2.15');periksa('ip addr show','sl0: UP');periksa('ifconfig','sl0: UP')
                    for tidak_sahih_Pengaturan in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        galat=periksa('ipconfig set '+tidak_sahih_Pengaturan+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in galat,galat
                        periksa('ipconfig','inet 10.0.2.15')
                    periksa('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    periksa(alias_VALUE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    periksa('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    periksa('ip link set dev sl0 down','sl0: DOWN');periksa('ping -c 1 10.0.2.2; echo STATUS=$?','galat -100','STATUS=1')
                    periksa('ipconfig up','sl0: UP')
                    periksa(alias_VALUE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    periksa('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    periksa('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');periksa(alias_VALUE['route'],'10.0.2.2 sl0')
                    periksa('ftpd start','FTP listening')
                    periksa(alias_VALUE['netstat'],'10.0.2.20:21','LISTEN');periksa('ss','LISTEN')
                    periksa('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','galat -16')
                    with ftplib.FTP() as klien_VALUE:
                        klien_VALUE.connect('127.0.0.2',nomor_port,timeout=20);klien_VALUE.login();data=b'Network address was changed in the guest.\n'
                        klien_VALUE.storbinary('STOR net-state.txt',io.BytesIO(data));RECEIVED_data=bytearray();klien_VALUE.retrbinary('RETR net-state.txt',RECEIVED_data.extend);assert RECEIVED_data==data;klien_VALUE.delete('net-state.txt')
                    periksa('ftpd stop','FTP stopped');periksa('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    lapor_VALUE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(teks):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',teks);assert 찾음,teks;return tuple(map(int,찾음.groups()))
                    전=저장값(periksa('df','RAM only'));periksa('echo disk-proof > sys-state.txt');후=저장값(periksa(alias_VALUE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    periksa('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memori_VALUE=periksa(alias_VALUE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memori_VALUE).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    periksa(alias_VALUE['ps'],'kernel/shell');periksa(alias_VALUE['uptime'],'seconds')
                    status_info=periksa(alias_VALUE['top']+' -n 2','kernel/shell');assert status_info.count('PID SLOT STATE')==2,status_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    periksa('terminal','TERMINAL READY');jalankan=len(LOG_baris);kirim(b'vi process.txt\n');terima(b'NORMAL',jalankan)
                    jalankan=len(LOG_baris);kirim(bytes([30,2,1,0,0,0,0]));terima(b'jkoros-native> ',jalankan)
                    entri_Daftar=periksa('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',entri_Daftar);assert 찾음 and int(찾음.group(2))>0,entri_Daftar
                    periksa('free','EL0 mapped KiB: '+찾음.group(2))
                    jalankan=len(LOG_baris);kirim(b'top\n');terima(b'PID SLOT STATE',jalankan);kirim(b'q');terima(b'jkoros-native> ',jalankan)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALUE['df']!='df':
                        jalankan=len(LOG_baris);kirim((alias_VALUE['df'][:-1]+'\t\n').encode());terima(b'RAM only',jalankan);terima(b'jkoros-native> ',jalankan)
                    lapor_VALUE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as kontrol_VALUE:
                    kontrol_VALUE.settimeout(15);kontrol_VALUE.connect(str(kontrol_jalur));Stream_VALUE=kontrol_VALUE.makefile('rwb');json.loads(Stream_VALUE.readline());Stream_VALUE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALUE.flush()
                    while 'return' not in json.loads(Stream_VALUE.readline()):pass
                    kirim((('poweroff' if argumen.poweroff_only else alias_VALUE['poweroff'])+'\n').encode())
                    while True:
                        Even=json.loads(Stream_VALUE.readline())
                        if Even.get('event')=='SHUTDOWN':break
                    assert Even['data']['guest'] and Even['data']['reason']=='guest-shutdown',Even
                    assert Proses_VALUE.wait(timeout=15)==0
                    lapor_VALUE['shutdown']=Even;lapor_VALUE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                lapor_VALUE['network_trace']=bridge_VALUE.log_jejak
                assert argumen.poweroff_only or any(entri_VALUE['protocol']==1 and entri_VALUE['direction']=='from_guest' for entri_VALUE in bridge_VALUE.log_jejak)
                lapor_VALUE['passed']=True
            finally:
                if Proses_VALUE.poll() is None:os.killpg(Proses_VALUE.pid,signal.SIGTERM)
                try:Proses_VALUE.wait(timeout=10)
                except subprocess.TimeoutExpired:Proses_VALUE.kill();Proses_VALUE.wait()
                pilih_item.close();(keluaranTeks/'serial.log').write_bytes(LOG_baris);(keluaranTeks/'report.json').write_text(json.dumps(lapor_VALUE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Kunci_VALUE:VALUE for Kunci_VALUE,VALUE in lapor_VALUE.items() if Kunci_VALUE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':jalankan()
