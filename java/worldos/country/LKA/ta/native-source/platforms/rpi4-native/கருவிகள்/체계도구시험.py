#!/usr/bin/env python3
"""அசல்_தரவு 자체 커널의 IP/ICMP, நிலை_மதிப்பு_e10195a1 வினவல்_மதிப்பு, 현지어 கட்டளை, 게스트 முடிவு_நிரல் சரிபார்_5fb2b747."""
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


def செயல்படுத்துக():
    பார்சர்_48ee4b1b=argparse.ArgumentParser();பார்சர்_48ee4b1b.add_argument('--edition',type=Path);பார்சர்_48ee4b1b.add_argument('--output',type=Path);பார்சர்_48ee4b1b.add_argument('--poweroff-only',action='store_true');செயலுருபுகள்=பார்சர்_48ee4b1b.parse_args()
    திட்டப்பணி_மூலம்=Path(__file__).resolve().parents[1];அமைப்புகள்={};பெயர்_அட்டவணை={}
    if செயலுருபுகள்.edition:
        나라=செயலுருபுகள்.edition.resolve();அமைப்புகள்=json.loads((나라/'native.json').read_text());பெயர்_அட்டவணை=அமைப்புகள்['identifiers'];திட்டப்பணி_மூலம்=나라/அமைப்புகள்['source']/அமைப்புகள்['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        ஓம்பு=나라/'host/qemu'
        if ஓம்பு.is_file():os.environ['QEMU_AARCH64']=str(ஓம்பு)
    கருவிகள்=திட்டப்பணி_மூலம்/Path(அமைப்புகள்.get('runner','கருவிகள்/இயக்கு_கட்டளை.py')).parent
    sys.path.insert(0,str(கருவிகள்))
    def படி(பெயர்):
        பாதை_2=கருவிகள்/(பெயர்_அட்டவணை.get(பெயர்,பெயர்)+'.py');வேலை_மதிப்பு_102996da=importlib.util.spec_from_file_location('test_'+பெயர்,str(பாதை_2));தொகுதி_மதிப்பு=importlib.util.module_from_spec(வேலை_மதிப்பு_102996da);வேலை_மதிப்பு_102996da.loader.exec_module(தொகுதி_மதிப்பு);return தொகுதி_மதிப்பு
    실행모듈=படி('இயக்கு_கட்டளை');பிணையம்_தொகுதி=படி('பிணையம்_பிரிட்ஜ்');கட்டளை=getattr(실행모듈,பெயர்_அட்டவணை.get('கட்டளை','கட்டளை'));பிரிட்ஜ்_வகை=getattr(பிணையம்_தொகுதி,பெயர்_அட்டவணை.get('பிணையம்_பிரிட்ஜ்','பிணையம்_பிரிட்ஜ்'))
    குறுக்குவழி_மதிப்பு_0a38607b=அமைப்புகள்.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_முகவரி','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'உதவியைக்_காட்டு'})
    sys.path.insert(0,str(திட்டப்பணி_மூலம்/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(திட்டப்பணி_மூலம்);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    வெளியீட்டு_இடம்=செயலுருபுகள்.output or திட்டப்பணி_மூலம்/'build/verification/system-tools';வெளியீட்டு_இடம்.mkdir(parents=True,exist_ok=True)
    அறிக்கை_மதிப்பு={'passed':False,'country':அமைப்புகள்.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    பதிவு_பதிவு=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        கட்டுப்பாடு_பாதை=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as தேடு_மதிப்பு:தேடு_மதிப்பு.bind(('127.0.0.1',0));முனைய_எண்=தேடு_மதிப்பு.getsockname()[1]
            if not 50000<=முனைய_எண்<=50007:break
        with பிரிட்ஜ்_வகை(முனைய_எண்,பிடிப்பு=True,விருந்தினர்_முகவரி=ipTestText('10.0.2.20'),ஓம்பு_முகவரி='127.0.0.2') as பிரிட்ஜ்_மதிப்பு:
            செயலகம்_மதிப்பு=subprocess.Popen(கட்டளை()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(கட்டுப்பாடு_பாதை)]+பிரிட்ஜ்_மதிப்பு.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            தேர்வுசெய்_உருப்படி=selectors.DefaultSelector();தேர்வுசெய்_உருப்படி.register(செயலகம்_மதிப்பு.stdout,selectors.EVENT_READ)
            def 받기(காட்சி_மதிப்பு_487749b8,செயல்படுத்துக=0,제한=45):
                끝=time.monotonic()+제한
                while காட்சி_மதிப்பு_487749b8 not in பதிவு_பதிவு[செயல்படுத்துக:]:
                    if time.monotonic()>끝 or செயலகம்_மதிப்பு.poll() is not None:raise AssertionError('Missing '+repr(காட்சி_மதிப்பு_487749b8)+'\n'+பதிவு_பதிவு[செயல்படுத்துக:].decode('utf-8','replace'))
                    for சாவி_மதிப்பு,_ in தேர்வுசெய்_உருப்படி.select(.1):
                        தரவு=சாவி_மதிப்பு.fileobj.read(65536)
                        if தரவு:பதிவு_பதிவு.extend(தரவு)
                return பதிவு_பதிவு[செயல்படுத்துக:].decode('utf-8','replace').replace('\r\n','\n')
            def அனுப்பு(தரவு):செயலகம்_மதிப்பு.stdin.write(தரவு);செயலகம்_மதிப்பு.stdin.flush()
            def கூடு(உரை):
                உரை=ipTestText(உரை)
                print(அறிக்கை_மதிப்பு['country'],உரை,flush=True);차례[0]+=1;காட்சி_மதிப்பு_487749b8='__SYSTEM_DONE_'+str(차례[0])+'__';செயல்படுத்துக=len(பதிவு_பதிவு)
                அனுப்பு((உரை+'; echo; echo '+காட்சி_மதிப்பு_487749b8+'\n').encode())
                끝표시=('\r\n'+காட்சி_மதிப்பு_487749b8+'\r\n').encode();받기(끝표시,செயல்படுத்துக)
                முடி_நிலை=பதிவு_பதிவு.index(끝표시,செயல்படுத்துக)+len(끝표시)
                받기(b'jkoros-native> ',முடி_நிலை)
                return பதிவு_பதிவு[செயல்படுத்துக:].decode('utf-8','replace').replace('\r\n','\n')
            def சரிபார்(உரை,*값들):
                பதிலளி=கூடு(உரை)
                for மதிப்பு in 값들:assert ipTestText(மதிப்பு) in பதிலளி,(உரை,மதிப்பு,பதிலளி)
                return பதிலளி
            try:
                받기(b'jkoros-native> ')
                if not செயலுருபுகள்.poweroff_only:
                    உதவி_மதிப்பு=சரிபார்('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in குறுக்குவழி_மதிப்பு_0a38607b.values():assert 별칭 in உதவி_மதிப்பு,(별칭,உதவி_மதிப்பு)
                    சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['help']+' system','Network / system')
                    சரிபார்('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['ipconfig'],'inet 10.0.2.15');சரிபார்('ip addr show','sl0: UP');சரிபார்('ifconfig','sl0: UP')
                    for செல்லுபடியாகாத_அமைப்புகள் in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        பிழை=சரிபார்('ipconfig set '+செல்லுபடியாகாத_அமைப்புகள்+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in பிழை,பிழை
                        சரிபார்('ipconfig','inet 10.0.2.15')
                    சரிபார்('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    சரிபார்('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    சரிபார்('ip link set dev sl0 down','sl0: DOWN');சரிபார்('ping -c 1 10.0.2.2; echo STATUS=$?','பிழை -100','STATUS=1')
                    சரிபார்('ipconfig up','sl0: UP')
                    சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    சரிபார்('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    சரிபார்('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['route'],'10.0.2.2 sl0')
                    சரிபார்('ftpd start','FTP listening')
                    சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['netstat'],'10.0.2.20:21','LISTEN');சரிபார்('ss','LISTEN')
                    சரிபார்('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','பிழை -16')
                    with ftplib.FTP() as பயனகம்_மதிப்பு:
                        பயனகம்_மதிப்பு.connect('127.0.0.2',முனைய_எண்,timeout=20);பயனகம்_மதிப்பு.login();தரவு=b'Network address was changed in the guest.\n'
                        பயனகம்_மதிப்பு.storbinary('STOR net-state.txt',io.BytesIO(தரவு));받은자료=bytearray();பயனகம்_மதிப்பு.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==தரவு;பயனகம்_மதிப்பு.delete('net-state.txt')
                    சரிபார்('ftpd stop','FTP stopped');சரிபார்('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    அறிக்கை_மதிப்பு['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(உரை):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',உரை);assert 찾음,உரை;return tuple(map(int,찾음.groups()))
                    전=저장값(சரிபார்('df','RAM only'));சரிபார்('echo disk-proof > sys-state.txt');후=저장값(சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    சரிபார்('rm sys-state.txt');assert 저장값(கூடு('df'))==전
                    நினைவகம்_மதிப்பு=சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',நினைவகம்_மதிப்பு).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['ps'],'kernel/shell');சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['uptime'],'seconds')
                    நிலை_தகவல்=சரிபார்(குறுக்குவழி_மதிப்பு_0a38607b['top']+' -n 2','kernel/shell');assert நிலை_தகவல்.count('PID SLOT STATE')==2,நிலை_தகவல்
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    சரிபார்('terminal','TERMINAL READY');செயல்படுத்துக=len(பதிவு_பதிவு);அனுப்பு(b'vi process.txt\n');받기(b'NORMAL',செயல்படுத்துக)
                    செயல்படுத்துக=len(பதிவு_பதிவு);அனுப்பு(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',செயல்படுத்துக)
                    உள்ளீடு_பட்டியல்=சரிபார்('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',உள்ளீடு_பட்டியல்);assert 찾음 and int(찾음.group(2))>0,உள்ளீடு_பட்டியல்
                    சரிபார்('free','EL0 mapped KiB: '+찾음.group(2))
                    செயல்படுத்துக=len(பதிவு_பதிவு);அனுப்பு(b'top\n');받기(b'PID SLOT STATE',செயல்படுத்துக);அனுப்பு(b'q');받기(b'jkoros-native> ',செயல்படுத்துக)
                    # Test a multibyte prefix through the real shell completion path.
                    if குறுக்குவழி_மதிப்பு_0a38607b['df']!='df':
                        செயல்படுத்துக=len(பதிவு_பதிவு);அனுப்பு((குறுக்குவழி_மதிப்பு_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',செயல்படுத்துக);받기(b'jkoros-native> ',செயல்படுத்துக)
                    அறிக்கை_மதிப்பு['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as கட்டுப்பாடு_மதிப்பு:
                    கட்டுப்பாடு_மதிப்பு.settimeout(15);கட்டுப்பாடு_மதிப்பு.connect(str(கட்டுப்பாடு_பாதை));தொடரோடி_மதிப்பு=கட்டுப்பாடு_மதிப்பு.makefile('rwb');json.loads(தொடரோடி_மதிப்பு.readline());தொடரோடி_மதிப்பு.write(b'{"execute":"qmp_capabilities"}\n');தொடரோடி_மதிப்பு.flush()
                    while 'return' not in json.loads(தொடரோடி_மதிப்பு.readline()):pass
                    அனுப்பு((('poweroff' if செயலுருபுகள்.poweroff_only else குறுக்குவழி_மதிப்பு_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        நிகழ்வு=json.loads(தொடரோடி_மதிப்பு.readline())
                        if நிகழ்வு.get('event')=='SHUTDOWN':break
                    assert நிகழ்வு['data']['guest'] and நிகழ்வு['data']['reason']=='guest-shutdown',நிகழ்வு
                    assert செயலகம்_மதிப்பு.wait(timeout=15)==0
                    அறிக்கை_மதிப்பு['shutdown']=நிகழ்வு;அறிக்கை_மதிப்பு['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                அறிக்கை_மதிப்பு['network_trace']=பிரிட்ஜ்_மதிப்பு.சுவடு_பதிவு
                assert செயலுருபுகள்.poweroff_only or any(உள்ளீடு_மதிப்பு['protocol']==1 and உள்ளீடு_மதிப்பு['direction']=='from_guest' for உள்ளீடு_மதிப்பு in பிரிட்ஜ்_மதிப்பு.சுவடு_பதிவு)
                அறிக்கை_மதிப்பு['passed']=True
            finally:
                if செயலகம்_மதிப்பு.poll() is None:os.killpg(செயலகம்_மதிப்பு.pid,signal.SIGTERM)
                try:செயலகம்_மதிப்பு.wait(timeout=10)
                except subprocess.TimeoutExpired:செயலகம்_மதிப்பு.kill();செயலகம்_மதிப்பு.wait()
                தேர்வுசெய்_உருப்படி.close();(வெளியீட்டு_இடம்/'serial.log').write_bytes(பதிவு_பதிவு);(வெளியீட்டு_இடம்/'report.json').write_text(json.dumps(அறிக்கை_மதிப்பு,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({சாவி_மதிப்பு:மதிப்பு for சாவி_மதிப்பு,மதிப்பு in அறிக்கை_மதிப்பு.items() if சாவி_மதிப்பு!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':செயல்படுத்துக()
