#!/usr/bin/env python3
"""taannallarik_titiqqat 자체 커널의 IP/ICMP, qanuilinganiq_atuutilik kiggusiqarialik_atuutilik, 현지어 piqujijjut, 게스트 taima_pilirijjut naammannirarli."""
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


def 시작():
    해석기=argparse.ArgumentParser();해석기.add_argument('--edition',type=Path);해석기.add_argument('--output',type=Path);해석기.add_argument('--poweroff-only',action='store_true');인수=해석기.parse_args()
    기준=Path(__file__).resolve().parents[1];설정={};atiq_kipu={}
    if 인수.edition:
        나라=인수.edition.resolve();설정=json.loads((나라/'native.json').read_text());atiq_kipu=설정['identifiers'];기준=나라/설정['source']/설정['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        tuttarvik=나라/'host/qemu'
        if tuttarvik.is_file():os.environ['QEMU_AARCH64']=str(tuttarvik)
    도구=기준/Path(설정.get('runner','도구/실행.py')).parent
    sys.path.insert(0,str(도구))
    def 읽기(atiq):
        aqqut=도구/(atiq_kipu.get(atiq,atiq)+'.py');pijatsaq_atuutilik=importlib.util.spec_from_file_location('test_'+atiq,str(aqqut));모듈=importlib.util.module_from_spec(pijatsaq_atuutilik);pijatsaq_atuutilik.loader.exec_module(모듈);return 모듈
    실행모듈=읽기('실행');망모듈=읽기('통신다리');piqujijjut=getattr(실행모듈,atiq_kipu.get('piqujijjut','piqujijjut'));다리형=getattr(망모듈,atiq_kipu.get('통신다리','통신다리'))
    nangarut_atuutilik_0a38607b=설정.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP_Turaarut','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'saqqilli_Ikajuqtau'})
    sys.path.insert(0,str(기준/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(기준);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    출력=인수.output or 기준/'build/verification/system-tools';출력.mkdir(parents=True,exist_ok=True)
    unikkaaq_atuutilik={'passed':False,'country':설정.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    papattivik_sanimukutaak=bytearray();차례=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        aulattivik_aqqut=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Qinirli_atuutilik:Qinirli_atuutilik.bind(('127.0.0.1',0));접속번호=Qinirli_atuutilik.getsockname()[1]
            if not 50000<=접속번호<=50007:break
        with 다리형(접속번호,포착여부=True,게스트주소=ipTestText('10.0.2.20'),tuttarvik_turaarut='127.0.0.2') as 다리:
            Pivallianiq_atuutilik=subprocess.Popen(piqujijjut()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(aulattivik_aqqut)]+다리.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            niruarli_kisu=selectors.DefaultSelector();niruarli_kisu.register(Pivallianiq_atuutilik.stdout,selectors.EVENT_READ)
            def 받기(saqqilli_atuutilik,시작=0,제한=45):
                끝=time.monotonic()+제한
                while saqqilli_atuutilik not in papattivik_sanimukutaak[시작:]:
                    if time.monotonic()>끝 or Pivallianiq_atuutilik.poll() is not None:raise AssertionError('Missing '+repr(saqqilli_atuutilik)+'\n'+papattivik_sanimukutaak[시작:].decode('utf-8','replace'))
                    for naqigaq_atuutilik,_ in niruarli_kisu.select(.1):
                        titiqqat=naqigaq_atuutilik.fileobj.read(65536)
                        if titiqqat:papattivik_sanimukutaak.extend(titiqqat)
                return papattivik_sanimukutaak[시작:].decode('utf-8','replace').replace('\r\n','\n')
            def nassiutili(titiqqat):Pivallianiq_atuutilik.stdin.write(titiqqat);Pivallianiq_atuutilik.stdin.flush()
            def piqujijjutiliriji(titiqqaq):
                titiqqaq=ipTestText(titiqqaq)
                print(unikkaaq_atuutilik['country'],titiqqaq,flush=True);차례[0]+=1;saqqilli_atuutilik='__SYSTEM_DONE_'+str(차례[0])+'__';시작=len(papattivik_sanimukutaak)
                nassiutili((titiqqaq+'; echo; echo '+saqqilli_atuutilik+'\n').encode())
                끝표시=('\r\n'+saqqilli_atuutilik+'\r\n').encode();받기(끝표시,시작)
                끝자리=papattivik_sanimukutaak.index(끝표시,시작)+len(끝표시)
                받기(b'jkoros-native> ',끝자리)
                return papattivik_sanimukutaak[시작:].decode('utf-8','replace').replace('\r\n','\n')
            def nalunairli_1aacb54c(titiqqaq,*값들):
                응답=piqujijjutiliriji(titiqqaq)
                for atuutilik in 값들:assert ipTestText(atuutilik) in 응답,(titiqqaq,atuutilik,응답)
                return 응답
            try:
                받기(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    Ikajuqtau_atuutilik=nalunairli_1aacb54c('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in nangarut_atuutilik_0a38607b.values():assert 별칭 in Ikajuqtau_atuutilik,(별칭,Ikajuqtau_atuutilik)
                    nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['help']+' system','Network / system')
                    nalunairli_1aacb54c('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['ipconfig'],'inet 10.0.2.15');nalunairli_1aacb54c('ip addr show','sl0: UP');nalunairli_1aacb54c('ifconfig','sl0: UP')
                    for 잘못된설정 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        tammarniq=nalunairli_1aacb54c('ipconfig set '+잘못된설정+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in tammarniq,tammarniq
                        nalunairli_1aacb54c('ipconfig','inet 10.0.2.15')
                    nalunairli_1aacb54c('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    nalunairli_1aacb54c('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    nalunairli_1aacb54c('ip link set dev sl0 down','sl0: DOWN');nalunairli_1aacb54c('ping -c 1 10.0.2.2; echo STATUS=$?','tammarniq -100','STATUS=1')
                    nalunairli_1aacb54c('ipconfig up','sl0: UP')
                    nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    nalunairli_1aacb54c('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    nalunairli_1aacb54c('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['route'],'10.0.2.2 sl0')
                    nalunairli_1aacb54c('ftpd start','FTP listening')
                    nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['netstat'],'10.0.2.20:21','LISTEN');nalunairli_1aacb54c('ss','LISTEN')
                    nalunairli_1aacb54c('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','tammarniq -16')
                    with ftplib.FTP() as pijittiqtaq_atuutilik:
                        pijittiqtaq_atuutilik.connect('127.0.0.2',접속번호,timeout=20);pijittiqtaq_atuutilik.login();titiqqat=b'Network address was changed in the guest.\n'
                        pijittiqtaq_atuutilik.storbinary('STOR net-state.txt',io.BytesIO(titiqqat));받은자료=bytearray();pijittiqtaq_atuutilik.retrbinary('RETR net-state.txt',받은자료.extend);assert 받은자료==titiqqat;pijittiqtaq_atuutilik.delete('net-state.txt')
                    nalunairli_1aacb54c('ftpd stop','FTP stopped');nalunairli_1aacb54c('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    unikkaaq_atuutilik['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(titiqqaq):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',titiqqaq);assert 찾음,titiqqaq;return tuple(map(int,찾음.groups()))
                    전=저장값(nalunairli_1aacb54c('df','RAM only'));nalunairli_1aacb54c('echo disk-proof > sys-state.txt');후=저장값(nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    nalunairli_1aacb54c('rm sys-state.txt');assert 저장값(piqujijjutiliriji('df'))==전
                    puigujjaikkut_atuutilik=nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',puigujjaikkut_atuutilik).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['ps'],'kernel/shell');nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['uptime'],'seconds')
                    qanuilinganiq_tukisigiarut=nalunairli_1aacb54c(nangarut_atuutilik_0a38607b['top']+' -n 2','kernel/shell');assert qanuilinganiq_tukisigiarut.count('PID SLOT STATE')==2,qanuilinganiq_tukisigiarut
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    nalunairli_1aacb54c('terminal','TERMINAL READY');시작=len(papattivik_sanimukutaak);nassiutili(b'vi process.txt\n');받기(b'NORMAL',시작)
                    시작=len(papattivik_sanimukutaak);nassiutili(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',시작)
                    Iliniku_Titiqpalliagaq=nalunairli_1aacb54c('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',Iliniku_Titiqpalliagaq);assert 찾음 and int(찾음.group(2))>0,Iliniku_Titiqpalliagaq
                    nalunairli_1aacb54c('free','EL0 mapped KiB: '+찾음.group(2))
                    시작=len(papattivik_sanimukutaak);nassiutili(b'top\n');받기(b'PID SLOT STATE',시작);nassiutili(b'q');받기(b'jkoros-native> ',시작)
                    # Test a multibyte prefix through the real shell completion path.
                    if nangarut_atuutilik_0a38607b['df']!='df':
                        시작=len(papattivik_sanimukutaak);nassiutili((nangarut_atuutilik_0a38607b['df'][:-1]+'\t\n').encode());받기(b'RAM only',시작);받기(b'jkoros-native> ',시작)
                    unikkaaq_atuutilik['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as aulattivik_atuutilik:
                    aulattivik_atuutilik.settimeout(15);aulattivik_atuutilik.connect(str(aulattivik_aqqut));ingirrania_aulataup_atuutilik=aulattivik_atuutilik.makefile('rwb');json.loads(ingirrania_aulataup_atuutilik.readline());ingirrania_aulataup_atuutilik.write(b'{"execute":"qmp_capabilities"}\n');ingirrania_aulataup_atuutilik.flush()
                    while 'return' not in json.loads(ingirrania_aulataup_atuutilik.readline()):pass
                    nassiutili((('poweroff' if 인수.poweroff_only else nangarut_atuutilik_0a38607b['poweroff'])+'\n').encode())
                    while True:
                        piniku=json.loads(ingirrania_aulataup_atuutilik.readline())
                        if piniku.get('event')=='SHUTDOWN':break
                    assert piniku['data']['guest'] and piniku['data']['reason']=='guest-shutdown',piniku
                    assert Pivallianiq_atuutilik.wait(timeout=15)==0
                    unikkaaq_atuutilik['shutdown']=piniku;unikkaaq_atuutilik['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                unikkaaq_atuutilik['network_trace']=다리.추적기록
                assert 인수.poweroff_only or any(Iliniku_atuutilik['protocol']==1 and Iliniku_atuutilik['direction']=='from_guest' for Iliniku_atuutilik in 다리.추적기록)
                unikkaaq_atuutilik['passed']=True
            finally:
                if Pivallianiq_atuutilik.poll() is None:os.killpg(Pivallianiq_atuutilik.pid,signal.SIGTERM)
                try:Pivallianiq_atuutilik.wait(timeout=10)
                except subprocess.TimeoutExpired:Pivallianiq_atuutilik.kill();Pivallianiq_atuutilik.wait()
                niruarli_kisu.close();(출력/'serial.log').write_bytes(papattivik_sanimukutaak);(출력/'report.json').write_text(json.dumps(unikkaaq_atuutilik,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({naqigaq_atuutilik:atuutilik for naqigaq_atuutilik,atuutilik in unikkaaq_atuutilik.items() if naqigaq_atuutilik!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':시작()
