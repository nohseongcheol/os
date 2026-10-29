#!/usr/bin/env python3
"""内蔵 커널의 シェル, 프로세스 入力出力, Unicode GUI 터미널을 実際データ raspi4b에서 試験."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 命令実行 import 計画根, 命令


def 起動処理():
    出力結果 = 計画根 / 'build/verification/shell'; 出力結果.mkdir(parents=True, exist_ok=True)
    妥当性報告 = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((計画根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    実行記録 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 作業中経路:
        試験用模擬制御接続状態 = Path(作業中経路) / 'qmp.sock'
        プロセス = subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(試験用模擬制御接続状態)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        準備状態監視器=selectors.DefaultSelector(); 準備状態監視器.register(プロセス.stdout,selectors.EVENT_READ)
        def メッセージ受取(標識, 実行状態待機期限=45):
            データ=bytearray(); 終端位置変位量=time.monotonic()+実行状態待機期限
            while 標識 not in データ:
                if time.monotonic()>終端位置変位量 or プロセス.poll() is not None: raise AssertionError('UART timeout/exit: '+データ.decode('utf-8','replace'))
                for 押下済み値,_ in 準備状態監視器.select(.1):
                    断片値=押下済み値.fileobj.read(4096)
                    if 断片値: データ.extend(断片値); 実行記録.extend(断片値)
                if b'PANIC:' in データ or b'FAIL ' in データ: raise AssertionError(データ)
            return データ.decode('utf-8','replace').replace('\r\n','\n')
        def 送信(データ, 標識=b'jkoros-native> '):
            プロセス.stdin.write(データ); プロセス.stdin.flush(); return メッセージ受取(標識)
        def シェル(行, *期待):
            結果=送信(行.encode()+b'\n')
            for 値 in 期待: assert 値 in 結果, (行,値,結果)
            return 結果
        def ファイル(名前):
            文=シェル('hex '+名前,'HEX BEGIN','HEX END'); 結果捜索=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',文,re.S)
            データ=bytes.fromhex(''.join(結果捜索.group(2).split())); assert len(データ)==int(結果捜索.group(1)); return データ
        try:
            メッセージ受取(b'jkoros-native> ')
            シェル('mkdir 作業; cd 作業; pwd','/作業')
            シェル('mkdir 하위; echo "한글 データ 😀" > 挨拶例.txt')
            assert ファイル('挨拶例.txt')=='한글 データ 😀\n'.encode()
            シェル('cp 挨拶例.txt 値複写.txt; mv 値複写.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 データ 😀')
            シェル('cd 하위; cat ../挨拶例.txt; cat /作業/挨拶例.txt; pwd','한글 データ 😀','/作業/하위')
            シェル('cd ..; rmdir 하위; echo $?','1\n')
            シェル('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            シェル('cp 挨拶例.txt 挨拶例.txt; echo $?','1\n'); assert ファイル('挨拶例.txt')=='한글 データ 😀\n'.encode()
            シェル('export 挨拶例=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/作業','GOOD')
            assert b'BAD\n' not in ファイル('挨拶例.txt')
            シェル("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ファイル('리터럴')=='$인사\n누리\n'.encode()
            シェル('echo one > 文値; echo two >> 文値; echo three >> 文値')
            シェル('cat < 文値 | grep t | tee 추림 | wc -l','2\n'); assert ファイル('추림')==b'two\nthree\n'
            シェル('head -n 1 文値 > 前面値; tail -n 1 文値 > 後端値'); assert ファイル('앞')==b'one\n'; assert ファイル('뒤')==b'three\n'
            シェル('grep absent 文値; echo $?','1\n')
            シェル('echo untouched > 値防護')
            シェル('echo destroyed > 値防護 |','명령이 빠졌습니다'); assert ファイル('値防護')==b'untouched\n'
            シェル('echo "oops','따옴표가 닫히지 않았습니다')
            シェル('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            シェル('echo bad 2> 値防護','번호를 지정한 ファイル 記述子入口 入力出力 切替方式'); assert ファイル('値防護')==b'untouched\n'
            シェル('rm 빈파일 리터럴 文値 추림 前面値 後端値 値防護')
            妥当性報告['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            シェル("python -c 'print(123)' | wc -c",'4\n')
            シェル("python -c 'print(456)' > プログラム.txt"); assert ファイル('プログラム.txt')==b'456\n'
            シェル("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            シェル("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < プログラム.txt", "b'456\\n'", "b''")
            シェル("python -c 'print(\"x\"*17000)' | wc -c", 'エラー -28')
            シェル('echo recovered | wc -c','10\n')
            シェル("python -c 'import jkoros; print(jkoros.read("+'"/作業/プログラム.txt"'+"))'",'456','exit 0')
            シェル('cd /; javac Hello.java','Compiled:','exit 0')
            シェル('java Hello > /作業/Java.txt'); assert '안녕하세요'.encode() in ファイル('/作業/Java.txt')
            シェル('cd 作業; echo "echo script > 実行状態結果" > 命令.sh; echo "false || echo recovered >> 実行状態結果" >> 命令.sh; sh 命令.sh')
            assert ファイル('実行状態結果')==b'script\nrecovered\n'
            シェル('rm 実行状態結果; echo "exit 7" > 終了点プログラム.sh; sh 終了点プログラム.sh; echo $?','7\n')
            シェル('rm 終了点プログラム.sh 命令.sh プログラム.txt Java.txt 挨拶例.txt; cd /; rmdir 作業')
            妥当性報告['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            シェル('echo history-proof','history-proof')
            結果=送信(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 結果.count('history-proof')>=2, 結果
            送信(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            結果=送信(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 結果, 結果
            結果=送信(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 結果,結果
            結果=送信('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 結果,結果
            長整数本文='한글'*50
            結果=送信(('echo '+長整数本文+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+長整数本文+'\r\njkoros-native> ').encode()); assert '\n'+長整数本文+'\n' in 結果
            シェル('terminal','TERMINAL READY')
            シェル('clear')
            シェル('echo "한글 端末 ABC xyz 012 😀"','한글 端末 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as 接続元:
                接続元.settimeout(10); 接続元.connect(str(試験用模擬制御接続状態))
                with 接続元.makefile('rwb') as ストリーム値:
                    json.loads(ストリーム値.readline())
                    def 呼出(名前,引数配列=None):
                        通信網メッセージ={'execute':名前}
                        if 引数配列: 通信網メッセージ['arguments']=引数配列
                        ストリーム値.write((json.dumps(通信網メッセージ)+'\n').encode()); ストリーム値.flush()
                        while True:
                            返答=json.loads(ストリーム値.readline())
                            if 'error' in 返答: raise AssertionError(返答)
                            if 'return' in 返答: return 返答['return']
                    呼出('qmp_capabilities')
                    イメージ=出力結果/'terminal.ppm'; 呼出('screendump',{'filename':str(イメージ),'format':'ppm'})
                    呼出('screendump',{'filename':str(出力結果/'terminal.png'),'format':'png'})
                    データ=イメージ.read_bytes().split(b'\n',3)[3]
                    def 画素(横座標,縦座標): return tuple(データ[(縦座標*640+横座標)*3:(縦座標*640+横座標)*3+3])
                    assert 画素(12,48)==(32,80,144),画素(12,48)
                    assert len(set(画素(横座標,縦座標) for 縦座標 in range(100,116) for 横座標 in range(24,56)))>1,'Hangul glyphs missing'
                    シェル('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    シェル("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    呼出('screendump',{'filename':str(イメージ),'format':'ppm'})
                    復元済みデータ=イメージ.read_bytes().split(b'\n',3)[3]
                    assert tuple(復元済みデータ[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    シェル('echo test > visible.txt; cat visible.txt','test')
                    for 序数添字 in range(27): シェル('echo scroll-'+str(序数添字),'scroll-'+str(序数添字))
                    送信(b'\x1b[5~\x1b[6~\n')
                    呼出('screendump',{'filename':str(出力結果/'terminal-scroll.png'),'format':'png'})
                    結果=送信(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 結果,結果
                    シェル('rm visible.txt')
                    呼出('quit')
            プロセス.wait(timeout=5)
            妥当性報告['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            妥当性報告['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if プロセス.poll() is None:
                プロセス.terminate()
                try: プロセス.wait(timeout=5)
                except subprocess.TimeoutExpired: プロセス.kill(); プロセス.wait()
            準備状態監視器.close(); プロセス.stdin.close(); プロセス.stdout.close()
            (出力結果/'serial.log').write_bytes(実行記録)
            (出力結果/'report.json').write_text(json.dumps(妥当性報告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': 起動処理()
