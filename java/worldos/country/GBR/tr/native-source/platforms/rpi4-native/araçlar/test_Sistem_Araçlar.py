#!/usr/bin/env python3
"""fiili_veri Öz 커널의 IP/ICMP, Durum_değer sorgu_değer, 현지어 komut, 게스트 Çıkış_program doğrulamak_5fb2b747."""
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


def çalıştır():
    ayrıştırıcı_48ee4b1b=argparse.ArgumentParser();ayrıştırıcı_48ee4b1b.add_argument('--edition',type=Path);ayrıştırıcı_48ee4b1b.add_argument('--output',type=Path);ayrıştırıcı_48ee4b1b.add_argument('--poweroff-only',action='store_true');bağımsız_değişkenler=ayrıştırıcı_48ee4b1b.parse_args()
    işlem_kök=Path(__file__).resolve().parents[1];Ayarlar={};ad_tablo={}
    if bağımsız_değişkenler.edition:
        Country_değer=bağımsız_değişkenler.edition.resolve();Ayarlar=json.loads((Country_değer/'native.json').read_text());ad_tablo=Ayarlar['identifiers'];işlem_kök=Country_değer/Ayarlar['source']/Ayarlar['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_değer/'native-edition.py'),'check'])
        konak=Country_değer/'host/qemu'
        if konak.is_file():os.environ['QEMU_AARCH64']=str(konak)
    araçlar=işlem_kök/Path(Ayarlar.get('runner','araçlar/yürütmek_komut.py')).parent
    sys.path.insert(0,str(araçlar))
    def Okuma(İsim):
        yol=araçlar/(ad_tablo.get(İsim,İsim)+'.py');sözleşme_değeri=importlib.util.spec_from_file_location('test_'+İsim,str(yol));modül_değer=importlib.util.module_from_spec(sözleşme_değeri);sözleşme_değeri.loader.exec_module(modül_değer);return modül_değer
    yürütme_modül=Okuma('yürütmek_komut');ağ_modül=Okuma('köprü_3de4fe3a');komut=getattr(yürütme_modül,ad_tablo.get('komut','komut'));köprü_TÜR=getattr(ağ_modül,ad_tablo.get('köprü_3de4fe3a','köprü_3de4fe3a'))
    kısayol_değer_0a38607b=Ayarlar.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_adresi','ping':'test_cevap','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'yardım_göster'})
    sys.path.insert(0,str(işlem_kök/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(işlem_kök);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    metinÇıktısı=bağımsız_değişkenler.output or işlem_kök/'build/verification/system-tools';metinÇıktısı.mkdir(parents=True,exist_ok=True)
    Rapor_değer={'passed':False,'country':Ayarlar.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_KAYIT=bytearray();dizi_değer=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        denetim_yol=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Ara_değer:Ara_değer.bind(('127.0.0.1',0));bağlantı_noktası_numarası=Ara_değer.getsockname()[1]
            if not 50000<=bağlantı_noktası_numarası<=50007:break
        with köprü_TÜR(bağlantı_noktası_numarası,çekmek=True,konuk_ADRES=ipTestText('10.0.2.20'),konak_ADRES='127.0.0.2') as köprü_değer_982037b1:
            işlem_değer=subprocess.Popen(komut()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(denetim_yol)]+köprü_değer_982037b1.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ELEMAN_öğe=selectors.DefaultSelector();ELEMAN_öğe.register(işlem_değer.stdout,selectors.EVENT_READ)
            def almak(şov_değer,çalıştır=0,제한=45):
                끝=time.monotonic()+제한
                while şov_değer not in LOG_KAYIT[çalıştır:]:
                    if time.monotonic()>끝 or işlem_değer.poll() is not None:raise AssertionError('Missing '+repr(şov_değer)+'\n'+LOG_KAYIT[çalıştır:].decode('utf-8','replace'))
                    for tuş_değer,_ in ELEMAN_öğe.select(.1):
                        veri=tuş_değer.fileobj.read(65536)
                        if veri:LOG_KAYIT.extend(veri)
                return LOG_KAYIT[çalıştır:].decode('utf-8','replace').replace('\r\n','\n')
            def göndermek(veri):işlem_değer.stdin.write(veri);işlem_değer.stdin.flush()
            def kabuk(metin):
                metin=ipTestText(metin)
                print(Rapor_değer['country'],metin,flush=True);dizi_değer[0]+=1;şov_değer='__SYSTEM_DONE_'+str(dizi_değer[0])+'__';çalıştır=len(LOG_KAYIT)
                göndermek((metin+'; echo; echo '+şov_değer+'\n').encode())
                Bitiş_işaret=('\r\n'+şov_değer+'\r\n').encode();almak(Bitiş_işaret,çalıştır)
                Bitiş_konum=LOG_KAYIT.index(Bitiş_işaret,çalıştır)+len(Bitiş_işaret)
                almak(b'jkoros-native> ',Bitiş_konum)
                return LOG_KAYIT[çalıştır:].decode('utf-8','replace').replace('\r\n','\n')
            def doğrulamak(metin,*값들):
                yanıt=kabuk(metin)
                for değer in 값들:assert ipTestText(değer) in yanıt,(metin,değer,yanıt)
                return yanıt
            try:
                almak(b'jkoros-native> ')
                if not bağımsız_değişkenler.poweroff_only:
                    yardım_değer=doğrulamak('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in kısayol_değer_0a38607b.values():assert 별칭 in yardım_değer,(별칭,yardım_değer)
                    doğrulamak(kısayol_değer_0a38607b['help']+' system','Network / system')
                    doğrulamak('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    doğrulamak(kısayol_değer_0a38607b['ipconfig'],'inet 10.0.2.15');doğrulamak('ip addr show','sl0: UP');doğrulamak('ifconfig','sl0: UP')
                    for geçersiz_Ayarlar in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        hata=doğrulamak('ipconfig set '+geçersiz_Ayarlar+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in hata,hata
                        doğrulamak('ipconfig','inet 10.0.2.15')
                    doğrulamak('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    doğrulamak(kısayol_değer_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    doğrulamak('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    doğrulamak('ip link set dev sl0 down','sl0: DOWN');doğrulamak('ping -c 1 10.0.2.2; echo STATUS=$?','hata -100','STATUS=1')
                    doğrulamak('ipconfig up','sl0: UP')
                    doğrulamak(kısayol_değer_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    doğrulamak('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    doğrulamak('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');doğrulamak(kısayol_değer_0a38607b['route'],'10.0.2.2 sl0')
                    doğrulamak('ftpd start','FTP listening')
                    doğrulamak(kısayol_değer_0a38607b['netstat'],'10.0.2.20:21','LISTEN');doğrulamak('ss','LISTEN')
                    doğrulamak('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','hata -16')
                    with ftplib.FTP() as istemci_değer:
                        istemci_değer.connect('127.0.0.2',bağlantı_noktası_numarası,timeout=20);istemci_değer.login();veri=b'Network address was changed in the guest.\n'
                        istemci_değer.storbinary('STOR net-state.txt',io.BytesIO(veri));GETİRİ_veri=bytearray();istemci_değer.retrbinary('RETR net-state.txt',GETİRİ_veri.extend);assert GETİRİ_veri==veri;istemci_değer.delete('net-state.txt')
                    doğrulamak('ftpd stop','FTP stopped');doğrulamak('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Rapor_değer['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(metin):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',metin);assert 찾음,metin;return tuple(map(int,찾음.groups()))
                    전=저장값(doğrulamak('df','RAM only'));doğrulamak('echo disk-proof > sys-state.txt');후=저장값(doğrulamak(kısayol_değer_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    doğrulamak('rm sys-state.txt');assert 저장값(kabuk('df'))==전
                    Bellek_değer=doğrulamak(kısayol_değer_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Bellek_değer).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    doğrulamak(kısayol_değer_0a38607b['ps'],'kernel/shell');doğrulamak(kısayol_değer_0a38607b['uptime'],'seconds')
                    Durum_bilgi=doğrulamak(kısayol_değer_0a38607b['top']+' -n 2','kernel/shell');assert Durum_bilgi.count('PID SLOT STATE')==2,Durum_bilgi
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    doğrulamak('terminal','TERMINAL READY');çalıştır=len(LOG_KAYIT);göndermek(b'vi process.txt\n');almak(b'NORMAL',çalıştır)
                    çalıştır=len(LOG_KAYIT);göndermek(bytes([30,2,1,0,0,0,0]));almak(b'jkoros-native> ',çalıştır)
                    girdi_Liste=doğrulamak('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',girdi_Liste);assert 찾음 and int(찾음.group(2))>0,girdi_Liste
                    doğrulamak('free','EL0 mapped KiB: '+찾음.group(2))
                    çalıştır=len(LOG_KAYIT);göndermek(b'top\n');almak(b'PID SLOT STATE',çalıştır);göndermek(b'q');almak(b'jkoros-native> ',çalıştır)
                    # Test a multibyte prefix through the real shell completion path.
                    if kısayol_değer_0a38607b['df']!='df':
                        çalıştır=len(LOG_KAYIT);göndermek((kısayol_değer_0a38607b['df'][:-1]+'\t\n').encode());almak(b'RAM only',çalıştır);almak(b'jkoros-native> ',çalıştır)
                    Rapor_değer['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as denetim_değer:
                    denetim_değer.settimeout(15);denetim_değer.connect(str(denetim_yol));akış_değer=denetim_değer.makefile('rwb');json.loads(akış_değer.readline());akış_değer.write(b'{"execute":"qmp_capabilities"}\n');akış_değer.flush()
                    while 'return' not in json.loads(akış_değer.readline()):pass
                    göndermek((('poweroff' if bağımsız_değişkenler.poweroff_only else kısayol_değer_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        Olay=json.loads(akış_değer.readline())
                        if Olay.get('event')=='SHUTDOWN':break
                    assert Olay['data']['guest'] and Olay['data']['reason']=='guest-shutdown',Olay
                    assert işlem_değer.wait(timeout=15)==0
                    Rapor_değer['shutdown']=Olay;Rapor_değer['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Rapor_değer['network_trace']=köprü_değer_982037b1.izleme_günlüğü
                assert bağımsız_değişkenler.poweroff_only or any(girdi_değer['protocol']==1 and girdi_değer['direction']=='from_guest' for girdi_değer in köprü_değer_982037b1.izleme_günlüğü)
                Rapor_değer['passed']=True
            finally:
                if işlem_değer.poll() is None:os.killpg(işlem_değer.pid,signal.SIGTERM)
                try:işlem_değer.wait(timeout=10)
                except subprocess.TimeoutExpired:işlem_değer.kill();işlem_değer.wait()
                ELEMAN_öğe.close();(metinÇıktısı/'serial.log').write_bytes(LOG_KAYIT);(metinÇıktısı/'report.json').write_text(json.dumps(Rapor_değer,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tuş_değer:değer for tuş_değer,değer in Rapor_değer.items() if tuş_değer!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':çalıştır()
