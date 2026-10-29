#!/usr/bin/env python3
"""πραγματικός_δεδομένα ίδιο 커널의 IP/ICMP, Κατάσταση_τιμή ερώτημα_τιμή, 현지어 Εντολή, 게스트 Έξοδος_εφαρμογή επικυρώνω."""
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


def Εκτέλεση_2():
    ανάλυση_48ee4b1b=argparse.ArgumentParser();ανάλυση_48ee4b1b.add_argument('--edition',type=Path);ανάλυση_48ee4b1b.add_argument('--output',type=Path);ανάλυση_48ee4b1b.add_argument('--poweroff-only',action='store_true');Παράμετροι=ανάλυση_48ee4b1b.parse_args()
    έργο_ρίζα=Path(__file__).resolve().parents[1];Ρυθμίσεις={};όνομα_πίνακας={}
    if Παράμετροι.edition:
        Κάντρυ_τιμή=Παράμετροι.edition.resolve();Ρυθμίσεις=json.loads((Κάντρυ_τιμή/'native.json').read_text());όνομα_πίνακας=Ρυθμίσεις['identifiers'];έργο_ρίζα=Κάντρυ_τιμή/Ρυθμίσεις['source']/Ρυθμίσεις['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Κάντρυ_τιμή/'native-edition.py'),'check'])
        φιλοξενώ=Κάντρυ_τιμή/'host/qemu'
        if φιλοξενώ.is_file():os.environ['QEMU_AARCH64']=str(φιλοξενώ)
    Εργαλεία=έργο_ρίζα/Path(Ρυθμίσεις.get('runner','Εργαλεία/εκτελώ_εντολή.py')).parent
    sys.path.insert(0,str(Εργαλεία))
    def Ανάγνωση(Όνομα):
        ΔΙΑΔΡΟΜΗ=Εργαλεία/(όνομα_πίνακας.get(Όνομα,Όνομα)+'.py');εργασία_τιμή=importlib.util.spec_from_file_location('test_'+Όνομα,str(ΔΙΑΔΡΟΜΗ));μονάδα_τιμή=importlib.util.module_from_spec(εργασία_τιμή);εργασία_τιμή.loader.exec_module(μονάδα_τιμή);return μονάδα_τιμή
    εκτέλεση_μονάδα=Ανάγνωση('εκτελώ_εντολή');δίκτυο_μονάδα=Ανάγνωση('γέφυρα_3de4fe3a');Εντολή=getattr(εκτέλεση_μονάδα,όνομα_πίνακας.get('Εντολή','Εντολή'));γέφυρα_Τύπος=getattr(δίκτυο_μονάδα,όνομα_πίνακας.get('γέφυρα_3de4fe3a','γέφυρα_3de4fe3a'))
    ψευδώνυμο_τιμή=Ρυθμίσεις.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'διεύθυνση_IP','ping':'δοκιμή_απάντηση','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'εμφανίζω_βοήθεια'})
    sys.path.insert(0,str(έργο_ρίζα/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(έργο_ρίζα);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Έξοδος=Παράμετροι.output or έργο_ρίζα/'build/verification/system-tools';Έξοδος.mkdir(parents=True,exist_ok=True)
    έκθεση_τιμή={'passed':False,'country':Ρυθμίσεις.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    καταγράφω_ρεκόρ=bytearray();ακολουθία_τιμή=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        έλεγχος_διαδρομή=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as αναζητώ_τιμή:αναζητώ_τιμή.bind(('127.0.0.1',0));αριθμός_θύρας=αναζητώ_τιμή.getsockname()[1]
            if not 50000<=αριθμός_θύρας<=50007:break
        with γέφυρα_Τύπος(αριθμός_θύρας,δεσμεύω=True,Επισκέπτης_διεύθυνση=ipTestText('10.0.2.20'),φιλοξενώ_διεύθυνση='127.0.0.2') as γέφυρα_τιμή:
            διεργασία_τιμή=subprocess.Popen(Εντολή()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(έλεγχος_διαδρομή)]+γέφυρα_τιμή.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            επιλέγω_στοιχείο=selectors.DefaultSelector();επιλέγω_στοιχείο.register(διεργασία_τιμή.stdout,selectors.EVENT_READ)
            def λαμβάνω(εμφανίζω_τιμή,Εκτέλεση_2=0,제한=45):
                끝=time.monotonic()+제한
                while εμφανίζω_τιμή not in καταγράφω_ρεκόρ[Εκτέλεση_2:]:
                    if time.monotonic()>끝 or διεργασία_τιμή.poll() is not None:raise AssertionError('Missing '+repr(εμφανίζω_τιμή)+'\n'+καταγράφω_ρεκόρ[Εκτέλεση_2:].decode('utf-8','replace'))
                    for Κλειδί_τιμή,_ in επιλέγω_στοιχείο.select(.1):
                        δεδομένα=Κλειδί_τιμή.fileobj.read(65536)
                        if δεδομένα:καταγράφω_ρεκόρ.extend(δεδομένα)
                return καταγράφω_ρεκόρ[Εκτέλεση_2:].decode('utf-8','replace').replace('\r\n','\n')
            def στέλνω(δεδομένα):διεργασία_τιμή.stdin.write(δεδομένα);διεργασία_τιμή.stdin.flush()
            def κέλυφος(Κείμενο):
                Κείμενο=ipTestText(Κείμενο)
                print(έκθεση_τιμή['country'],Κείμενο,flush=True);ακολουθία_τιμή[0]+=1;εμφανίζω_τιμή='__SYSTEM_DONE_'+str(ακολουθία_τιμή[0])+'__';Εκτέλεση_2=len(καταγράφω_ρεκόρ)
                στέλνω((Κείμενο+'; echo; echo '+εμφανίζω_τιμή+'\n').encode())
                Τελική_οντότητα_δείκτης=('\r\n'+εμφανίζω_τιμή+'\r\n').encode();λαμβάνω(Τελική_οντότητα_δείκτης,Εκτέλεση_2)
                Τελική_οντότητα_θέση=καταγράφω_ρεκόρ.index(Τελική_οντότητα_δείκτης,Εκτέλεση_2)+len(Τελική_οντότητα_δείκτης)
                λαμβάνω(b'jkoros-native> ',Τελική_οντότητα_θέση)
                return καταγράφω_ρεκόρ[Εκτέλεση_2:].decode('utf-8','replace').replace('\r\n','\n')
            def επαληθεύω(Κείμενο,*값들):
                απαντώ=κέλυφος(Κείμενο)
                for τιμή in 값들:assert ipTestText(τιμή) in απαντώ,(Κείμενο,τιμή,απαντώ)
                return απαντώ
            try:
                λαμβάνω(b'jkoros-native> ')
                if not Παράμετροι.poweroff_only:
                    βοήθεια_τιμή=επαληθεύω('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in ψευδώνυμο_τιμή.values():assert 별칭 in βοήθεια_τιμή,(별칭,βοήθεια_τιμή)
                    επαληθεύω(ψευδώνυμο_τιμή['help']+' system','Network / system')
                    επαληθεύω('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    επαληθεύω(ψευδώνυμο_τιμή['ipconfig'],'inet 10.0.2.15');επαληθεύω('ip addr show','sl0: UP');επαληθεύω('ifconfig','sl0: UP')
                    for άκυρος_Ρυθμίσεις in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ΣΦΑΛΜΑ=επαληθεύω('ipconfig set '+άκυρος_Ρυθμίσεις+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ΣΦΑΛΜΑ,ΣΦΑΛΜΑ
                        επαληθεύω('ipconfig','inet 10.0.2.15')
                    επαληθεύω('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    επαληθεύω(ψευδώνυμο_τιμή['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    επαληθεύω('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    επαληθεύω('ip link set dev sl0 down','sl0: DOWN');επαληθεύω('ping -c 1 10.0.2.2; echo STATUS=$?','ΣΦΑΛΜΑ -100','STATUS=1')
                    επαληθεύω('ipconfig up','sl0: UP')
                    επαληθεύω(ψευδώνυμο_τιμή['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    επαληθεύω('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    επαληθεύω('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');επαληθεύω(ψευδώνυμο_τιμή['route'],'10.0.2.2 sl0')
                    επαληθεύω('ftpd start','FTP listening')
                    επαληθεύω(ψευδώνυμο_τιμή['netstat'],'10.0.2.20:21','LISTEN');επαληθεύω('ss','LISTEN')
                    επαληθεύω('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ΣΦΑΛΜΑ -16')
                    with ftplib.FTP() as πελάτης_τιμή:
                        πελάτης_τιμή.connect('127.0.0.2',αριθμός_θύρας,timeout=20);πελάτης_τιμή.login();δεδομένα=b'Network address was changed in the guest.\n'
                        πελάτης_τιμή.storbinary('STOR net-state.txt',io.BytesIO(δεδομένα));받은자료=bytearray();πελάτης_τιμή.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==δεδομένα;πελάτης_τιμή.delete('net-state.txt')
                    επαληθεύω('ftpd stop','FTP stopped');επαληθεύω('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    έκθεση_τιμή['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Κείμενο):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Κείμενο);assert 찾음,Κείμενο;return tuple(map(int,찾음.groups()))
                    전=저장값(επαληθεύω('df','RAM only'));επαληθεύω('echo disk-proof > sys-state.txt');후=저장값(επαληθεύω(ψευδώνυμο_τιμή['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    επαληθεύω('rm sys-state.txt');assert 저장값(κέλυφος('df'))==전
                    Μνήμη_τιμή=επαληθεύω(ψευδώνυμο_τιμή['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Μνήμη_τιμή).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    επαληθεύω(ψευδώνυμο_τιμή['ps'],'kernel/shell');επαληθεύω(ψευδώνυμο_τιμή['uptime'],'seconds')
                    κατάσταση_πληροφορία=επαληθεύω(ψευδώνυμο_τιμή['top']+' -n 2','kernel/shell');assert κατάσταση_πληροφορία.count('PID SLOT STATE')==2,κατάσταση_πληροφορία
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    επαληθεύω('terminal','TERMINAL READY');Εκτέλεση_2=len(καταγράφω_ρεκόρ);στέλνω(b'vi process.txt\n');λαμβάνω(b'NORMAL',Εκτέλεση_2)
                    Εκτέλεση_2=len(καταγράφω_ρεκόρ);στέλνω(bytes([30,2,1,0,0,0,0]));λαμβάνω(b'jkoros-native> ',Εκτέλεση_2)
                    καταχώρηση_Λίστα=επαληθεύω('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',καταχώρηση_Λίστα);assert 찾음 and int(찾음.group(2))>0,καταχώρηση_Λίστα
                    επαληθεύω('free','EL0 mapped KiB: '+찾음.group(2))
                    Εκτέλεση_2=len(καταγράφω_ρεκόρ);στέλνω(b'top\n');λαμβάνω(b'PID SLOT STATE',Εκτέλεση_2);στέλνω(b'q');λαμβάνω(b'jkoros-native> ',Εκτέλεση_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if ψευδώνυμο_τιμή['df']!='df':
                        Εκτέλεση_2=len(καταγράφω_ρεκόρ);στέλνω((ψευδώνυμο_τιμή['df'][:-1]+'\t\n').encode());λαμβάνω(b'RAM only',Εκτέλεση_2);λαμβάνω(b'jkoros-native> ',Εκτέλεση_2)
                    έκθεση_τιμή['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as έλεγχος_τιμή:
                    έλεγχος_τιμή.settimeout(15);έλεγχος_τιμή.connect(str(έλεγχος_διαδρομή));ροή_τιμή=έλεγχος_τιμή.makefile('rwb');json.loads(ροή_τιμή.readline());ροή_τιμή.write(b'{"execute":"qmp_capabilities"}\n');ροή_τιμή.flush()
                    while 'return' not in json.loads(ροή_τιμή.readline()):pass
                    στέλνω((('poweroff' if Παράμετροι.poweroff_only else ψευδώνυμο_τιμή['poweroff'])+'\n').encode())
                    while True:
                        Συμβάν=json.loads(ροή_τιμή.readline())
                        if Συμβάν.get('event')=='SHUTDOWN':break
                    assert Συμβάν['data']['guest'] and Συμβάν['data']['reason']=='guest-shutdown',Συμβάν
                    assert διεργασία_τιμή.wait(timeout=15)==0
                    έκθεση_τιμή['shutdown']=Συμβάν;έκθεση_τιμή['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                έκθεση_τιμή['network_trace']=γέφυρα_τιμή.αρχείο_καταγραφής_ανίχνευσης
                assert Παράμετροι.poweroff_only or any(καταχώρηση_τιμή['protocol']==1 and καταχώρηση_τιμή['direction']=='from_guest' for καταχώρηση_τιμή in γέφυρα_τιμή.αρχείο_καταγραφής_ανίχνευσης)
                έκθεση_τιμή['passed']=True
            finally:
                if διεργασία_τιμή.poll() is None:os.killpg(διεργασία_τιμή.pid,signal.SIGTERM)
                try:διεργασία_τιμή.wait(timeout=10)
                except subprocess.TimeoutExpired:διεργασία_τιμή.kill();διεργασία_τιμή.wait()
                επιλέγω_στοιχείο.close();(Έξοδος/'serial.log').write_bytes(καταγράφω_ρεκόρ);(Έξοδος/'report.json').write_text(json.dumps(έκθεση_τιμή,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Κλειδί_τιμή:τιμή for Κλειδί_τιμή,τιμή in έκθεση_τιμή.items() if Κλειδί_τιμή!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Εκτέλεση_2()
