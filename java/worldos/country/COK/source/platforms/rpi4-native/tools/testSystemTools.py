#!/usr/bin/env python3
"""actualData Native 커널의 IP/ICMP, stateValue queryValue, 현지어 command, 게스트 exitProgram validate."""
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


def run():
    Parser=argparse.ArgumentParser();Parser.add_argument('--edition',type=Path);Parser.add_argument('--output',type=Path);Parser.add_argument('--poweroff-only',action='store_true');arguments=Parser.parse_args()
    projectRoot=Path(__file__).resolve().parents[1];settings={};nameTable={}
    if arguments.edition:
        countryValue=arguments.edition.resolve();settings=json.loads((countryValue/'native.json').read_text());nameTable=settings['identifiers'];projectRoot=countryValue/settings['source']/settings['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(countryValue/'native-edition.py'),'check'])
        Host=countryValue/'host/qemu'
        if Host.is_file():os.environ['QEMU_AARCH64']=str(Host)
    tools=projectRoot/Path(settings.get('runner','tools/executeCommand.py')).parent
    sys.path.insert(0,str(tools))
    def read(name):
        path=tools/(nameTable.get(name,name)+'.py');contractValue=importlib.util.spec_from_file_location('test_'+name,str(path));moduleValue=importlib.util.module_from_spec(contractValue);contractValue.loader.exec_module(moduleValue);return moduleValue
    executionModule=read('executeCommand');networkModule=read('networkBridge');command=getattr(executionModule,nameTable.get('command','command'));bridgeType=getattr(networkModule,nameTable.get('networkBridge','networkBridge'))
    aliasValue=settings.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'ipAddress','ping':'testResponse','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'powerOff','help':'showHelp'})
    sys.path.insert(0,str(projectRoot/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(projectRoot);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Output=arguments.output or projectRoot/'build/verification/system-tools';Output.mkdir(parents=True,exist_ok=True)
    reportValue={'passed':False,'country':settings.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    logRecord=bytearray();sequenceValue=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as temporaryValue:
        controlPath=Path(temporaryValue)/'qmp.sock'
        while True:
            with socket.socket() as searchValue:searchValue.bind(('127.0.0.1',0));portNumber=searchValue.getsockname()[1]
            if not 50000<=portNumber<=50007:break
        with bridgeType(portNumber,capture=True,guestAddress=ipTestText('10.0.2.20'),hostAddress='127.0.0.2') as bridgeValue:
            processValue=subprocess.Popen(command()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(controlPath)]+bridgeValue.forwardedArgument(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            chooseItem=selectors.DefaultSelector();chooseItem.register(processValue.stdout,selectors.EVENT_READ)
            def receive(showValue,run=0,limitValue=45):
                ending=time.monotonic()+limitValue
                while showValue not in logRecord[run:]:
                    if time.monotonic()>ending or processValue.poll() is not None:raise AssertionError('Missing '+repr(showValue)+'\n'+logRecord[run:].decode('utf-8','replace'))
                    for keyValue,_ in chooseItem.select(.1):
                        data=keyValue.fileobj.read(65536)
                        if data:logRecord.extend(data)
                return logRecord[run:].decode('utf-8','replace').replace('\r\n','\n')
            def send(data):processValue.stdin.write(data);processValue.stdin.flush()
            def shell(text):
                text=ipTestText(text)
                print(reportValue['country'],text,flush=True);sequenceValue[0]+=1;showValue='__SYSTEM_DONE_'+str(sequenceValue[0])+'__';run=len(logRecord)
                send((text+'; echo; echo '+showValue+'\n').encode())
                endMarker=('\r\n'+showValue+'\r\n').encode();receive(endMarker,run)
                endPosition=logRecord.index(endMarker,run)+len(endMarker)
                receive(b'jkoros-native> ',endPosition)
                return logRecord[run:].decode('utf-8','replace').replace('\r\n','\n')
            def verify(text,*values):
                reply=shell(text)
                for value in values:assert ipTestText(value) in reply,(text,value,reply)
                return reply
            try:
                receive(b'jkoros-native> ')
                if not arguments.poweroff_only:
                    helpValue=verify('help system','ipconfig','ping','ps','top','df','poweroff')
                    for alternateName in aliasValue.values():assert alternateName in helpValue,(alternateName,helpValue)
                    verify(aliasValue['help']+' system','Network / system')
                    verify('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verify(aliasValue['ipconfig'],'inet 10.0.2.15');verify('ip addr show','sl0: UP');verify('ifconfig','sl0: UP')
                    for invalidSettings in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        error=verify('ipconfig set '+invalidSettings+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in error,error
                        verify('ipconfig','inet 10.0.2.15')
                    verify('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verify(aliasValue['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verify('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verify('ip link set dev sl0 down','sl0: DOWN');verify('ping -c 1 10.0.2.2; echo STATUS=$?','error -100','STATUS=1')
                    verify('ipconfig up','sl0: UP')
                    verify(aliasValue['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verify('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verify('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verify(aliasValue['route'],'10.0.2.2 sl0')
                    verify('ftpd start','FTP listening')
                    verify(aliasValue['netstat'],'10.0.2.20:21','LISTEN');verify('ss','LISTEN')
                    verify('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','error -16')
                    with ftplib.FTP() as clientValue:
                        clientValue.connect('127.0.0.2',portNumber,timeout=20);clientValue.login();data=b'Network address was changed in the guest.\n'
                        clientValue.storbinary('STOR net-state.txt',io.BytesIO(data));receivedData=bytearray();clientValue.retrbinary('RETR net-state.txt',receivedData.extend);assert receivedData==data;clientValue.delete('net-state.txt')
                    verify('ftpd stop','FTP stopped');verify('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    reportValue['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def saved(text):
                        foundValue=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',text);assert foundValue,text;return tuple(map(int,foundValue.groups()))
                    beforeValue=saved(verify('df','RAM only'));verify('echo disk-proof > sys-state.txt');afterState=saved(verify(aliasValue['df'],'RAM only'))
                    assert afterState[1]-beforeValue[1]==16384 and afterState[4]-beforeValue[4]==1 and afterState[3]-beforeValue[3]==11,(beforeValue,afterState)
                    verify('rm sys-state.txt');assert saved(shell('df'))==beforeValue
                    memoryValue=verify(aliasValue['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');quantityValue=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',memoryValue).groups()));assert 0<quantityValue[1]<=quantityValue[0] and quantityValue[1]+quantityValue[2]==quantityValue[0]
                    verify(aliasValue['ps'],'kernel/shell');verify(aliasValue['uptime'],'seconds')
                    statusInformation=verify(aliasValue['top']+' -n 2','kernel/shell');assert statusInformation.count('PID SLOT STATE')==2,statusInformation
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verify('terminal','TERMINAL READY');run=len(logRecord);send(b'vi process.txt\n');receive(b'NORMAL',run)
                    run=len(logRecord);send(bytes([30,2,1,0,0,0,0]));receive(b'jkoros-native> ',run)
                    entryList=verify('ps','SUSPENDED','vi process.txt');foundValue=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',entryList);assert foundValue and int(foundValue.group(2))>0,entryList
                    verify('free','EL0 mapped KiB: '+foundValue.group(2))
                    run=len(logRecord);send(b'top\n');receive(b'PID SLOT STATE',run);send(b'q');receive(b'jkoros-native> ',run)
                    # Test a multibyte prefix through the real shell completion path.
                    if aliasValue['df']!='df':
                        run=len(logRecord);send((aliasValue['df'][:-1]+'\t\n').encode());receive(b'RAM only',run);receive(b'jkoros-native> ',run)
                    reportValue['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as controlValue:
                    controlValue.settimeout(15);controlValue.connect(str(controlPath));streamValue=controlValue.makefile('rwb');json.loads(streamValue.readline());streamValue.write(b'{"execute":"qmp_capabilities"}\n');streamValue.flush()
                    while 'return' not in json.loads(streamValue.readline()):pass
                    send((('poweroff' if arguments.poweroff_only else aliasValue['poweroff'])+'\n').encode())
                    while True:
                        event=json.loads(streamValue.readline())
                        if event.get('event')=='SHUTDOWN':break
                    assert event['data']['guest'] and event['data']['reason']=='guest-shutdown',event
                    assert processValue.wait(timeout=15)==0
                    reportValue['shutdown']=event;reportValue['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                reportValue['network_trace']=bridgeValue.traceLog
                assert arguments.poweroff_only or any(entryValue['protocol']==1 and entryValue['direction']=='from_guest' for entryValue in bridgeValue.traceLog)
                reportValue['passed']=True
            finally:
                if processValue.poll() is None:os.killpg(processValue.pid,signal.SIGTERM)
                try:processValue.wait(timeout=10)
                except subprocess.TimeoutExpired:processValue.kill();processValue.wait()
                chooseItem.close();(Output/'serial.log').write_bytes(logRecord);(Output/'report.json').write_text(json.dumps(reportValue,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({keyValue:value for keyValue,value in reportValue.items() if keyValue!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':run()
