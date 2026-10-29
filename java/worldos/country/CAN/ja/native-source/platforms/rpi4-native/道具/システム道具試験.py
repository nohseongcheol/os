#!/usr/bin/env python3
"""実際データ 内蔵 커널의 IP/ICMP, 状況値 照会値, 현지어 命令, 게스트 終了点プログラム 妥当性検査."""
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


def 起動処理():
    構文解析器=argparse.ArgumentParser();構文解析器.add_argument('--edition',type=Path);構文解析器.add_argument('--output',type=Path);構文解析器.add_argument('--poweroff-only',action='store_true');引数=構文解析器.parse_args()
    計画根=Path(__file__).resolve().parents[1];設定値={};名前表={}
    if 引数.edition:
        国別値=引数.edition.resolve();設定値=json.loads((国別値/'native.json').read_text());名前表=設定値['identifiers'];計画根=国別値/設定値['source']/設定値['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(国別値/'native-edition.py'),'check'])
        ホスト=国別値/'host/qemu'
        if ホスト.is_file():os.environ['QEMU_AARCH64']=str(ホスト)
    道具=計画根/Path(設定値.get('runner','道具/命令実行.py')).parent
    sys.path.insert(0,str(道具))
    def 読取(名前):
        経路=道具/(名前表.get(名前,名前)+'.py');契約値=importlib.util.spec_from_file_location('test_'+名前,str(経路));モジュール値=importlib.util.module_from_spec(契約値);契約値.loader.exec_module(モジュール値);return モジュール値
    実行状態モジュール=読取('命令実行');通信網モジュール=読取('通信網橋渡し');命令=getattr(実行状態モジュール,名前表.get('命令','命令'));橋渡し型=getattr(通信網モジュール,名前表.get('通信網橋渡し','通信網橋渡し'))
    別名値=設定値.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'IP番地','ping':'応答試験','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'電源停止側','help':'ヘルプ表示'})
    sys.path.insert(0,str(計画根/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(計画根);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    出力=引数.output or 計画根/'build/verification/system-tools';出力.mkdir(parents=True,exist_ok=True)
    報告値={'passed':False,'country':設定値.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    履歴記録記録=bytearray();列順値=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 一時値:
        制御経路=Path(一時値)/'qmp.sock'
        while True:
            with socket.socket() as 値捜索:値捜索.bind(('127.0.0.1',0));ポート番号=値捜索.getsockname()[1]
            if not 50000<=ポート番号<=50007:break
        with 橋渡し型(ポート番号,捕獲=True,ゲスト番地=ipTestText('10.0.2.20'),ホスト番地='127.0.0.2') as 橋渡し値:
            プロセス値=subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(制御経路)]+橋渡し値.転送済み引数(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            項目選択=selectors.DefaultSelector();項目選択.register(プロセス値.stdout,selectors.EVENT_READ)
            def 受取(値表示,起動処理=0,上限値=45):
                終端=time.monotonic()+上限値
                while 値表示 not in 履歴記録記録[起動処理:]:
                    if time.monotonic()>終端 or プロセス値.poll() is not None:raise AssertionError('Missing '+repr(値表示)+'\n'+履歴記録記録[起動処理:].decode('utf-8','replace'))
                    for キー値,_ in 項目選択.select(.1):
                        データ=キー値.fileobj.read(65536)
                        if データ:履歴記録記録.extend(データ)
                return 履歴記録記録[起動処理:].decode('utf-8','replace').replace('\r\n','\n')
            def 送信(データ):プロセス値.stdin.write(データ);プロセス値.stdin.flush()
            def シェル(文):
                文=ipTestText(文)
                print(報告値['country'],文,flush=True);列順値[0]+=1;値表示='__SYSTEM_DONE_'+str(列順値[0])+'__';起動処理=len(履歴記録記録)
                送信((文+'; echo; echo '+値表示+'\n').encode())
                終端位置標識=('\r\n'+値表示+'\r\n').encode();受取(終端位置標識,起動処理)
                終端位置位置=履歴記録記録.index(終端位置標識,起動処理)+len(終端位置標識)
                受取(b'jkoros-native> ',終端位置位置)
                return 履歴記録記録[起動処理:].decode('utf-8','replace').replace('\r\n','\n')
            def 検証(文,*値一覧):
                返答=シェル(文)
                for 値 in 値一覧:assert ipTestText(値) in 返答,(文,値,返答)
                return 返答
            try:
                受取(b'jkoros-native> ')
                if not 引数.poweroff_only:
                    ヘルプ値=検証('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 代替用名前 in 別名値.values():assert 代替用名前 in ヘルプ値,(代替用名前,ヘルプ値)
                    検証(別名値['help']+' system','Network / system')
                    検証('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    検証(別名値['ipconfig'],'inet 10.0.2.15');検証('ip addr show','sl0: UP');検証('ifconfig','sl0: UP')
                    for 無効設定値 in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        エラー=検証('ipconfig set '+無効設定値+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in エラー,エラー
                        検証('ipconfig','inet 10.0.2.15')
                    検証('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    検証(別名値['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    検証('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    検証('ip link set dev sl0 down','sl0: DOWN');検証('ping -c 1 10.0.2.2; echo STATUS=$?','エラー -100','STATUS=1')
                    検証('ipconfig up','sl0: UP')
                    検証(別名値['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    検証('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    検証('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');検証(別名値['route'],'10.0.2.2 sl0')
                    検証('ftpd start','FTP listening')
                    検証(別名値['netstat'],'10.0.2.20:21','LISTEN');検証('ss','LISTEN')
                    検証('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','エラー -16')
                    with ftplib.FTP() as 接続元値:
                        接続元値.connect('127.0.0.2',ポート番号,timeout=20);接続元値.login();データ=b'Network address was changed in the guest.\n'
                        接続元値.storbinary('STOR net-state.txt',io.BytesIO(データ));受信済みデータ=bytearray();接続元値.retrbinary('RETR net-state.txt',受信済みデータ.extend);assert 受信済みデータ==データ;接続元値.delete('net-state.txt')
                    検証('ftpd stop','FTP stopped');検証('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    報告値['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 保存済み(文):
                        発見結果値=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',文);assert 発見結果値,文;return tuple(map(int,発見結果値.groups()))
                    直前側値=保存済み(検証('df','RAM only'));検証('echo disk-proof > sys-state.txt');後続側状況=保存済み(検証(別名値['df'],'RAM only'))
                    assert 後続側状況[1]-直前側値[1]==16384 and 後続側状況[4]-直前側値[4]==1 and 後続側状況[3]-直前側値[3]==11,(直前側値,後続側状況)
                    検証('rm sys-state.txt');assert 保存済み(シェル('df'))==直前側値
                    記憶=検証(別名値['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');数量値=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',記憶).groups()));assert 0<数量値[1]<=数量値[0] and 数量値[1]+数量値[2]==数量値[0]
                    検証(別名値['ps'],'kernel/shell');検証(別名値['uptime'],'seconds')
                    状態情報=検証(別名値['top']+' -n 2','kernel/shell');assert 状態情報.count('PID SLOT STATE')==2,状態情報
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    検証('terminal','TERMINAL READY');起動処理=len(履歴記録記録);送信(b'vi process.txt\n');受取(b'NORMAL',起動処理)
                    起動処理=len(履歴記録記録);送信(bytes([30,2,1,0,0,0,0]));受取(b'jkoros-native> ',起動処理)
                    入口一覧=検証('ps','SUSPENDED','vi process.txt');発見結果値=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',入口一覧);assert 発見結果値 and int(発見結果値.group(2))>0,入口一覧
                    検証('free','EL0 mapped KiB: '+発見結果値.group(2))
                    起動処理=len(履歴記録記録);送信(b'top\n');受取(b'PID SLOT STATE',起動処理);送信(b'q');受取(b'jkoros-native> ',起動処理)
                    # Test a multibyte prefix through the real shell completion path.
                    if 別名値['df']!='df':
                        起動処理=len(履歴記録記録);送信((別名値['df'][:-1]+'\t\n').encode());受取(b'RAM only',起動処理);受取(b'jkoros-native> ',起動処理)
                    報告値['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as 制御値:
                    制御値.settimeout(15);制御値.connect(str(制御経路));ストリーム値=制御値.makefile('rwb');json.loads(ストリーム値.readline());ストリーム値.write(b'{"execute":"qmp_capabilities"}\n');ストリーム値.flush()
                    while 'return' not in json.loads(ストリーム値.readline()):pass
                    送信((('poweroff' if 引数.poweroff_only else 別名値['poweroff'])+'\n').encode())
                    while True:
                        イベント=json.loads(ストリーム値.readline())
                        if イベント.get('event')=='SHUTDOWN':break
                    assert イベント['data']['guest'] and イベント['data']['reason']=='guest-shutdown',イベント
                    assert プロセス値.wait(timeout=15)==0
                    報告値['shutdown']=イベント;報告値['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                報告値['network_trace']=橋渡し値.追跡履歴記録
                assert 引数.poweroff_only or any(入口値['protocol']==1 and 入口値['direction']=='from_guest' for 入口値 in 橋渡し値.追跡履歴記録)
                報告値['passed']=True
            finally:
                if プロセス値.poll() is None:os.killpg(プロセス値.pid,signal.SIGTERM)
                try:プロセス値.wait(timeout=10)
                except subprocess.TimeoutExpired:プロセス値.kill();プロセス値.wait()
                項目選択.close();(出力/'serial.log').write_bytes(履歴記録記録);(出力/'report.json').write_text(json.dumps(報告値,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({キー値:値 for キー値,値 in 報告値.items() if キー値!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':起動処理()
