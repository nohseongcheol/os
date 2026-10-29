#!/usr/bin/env python3
"""內建 커널의 命令殼, 프로세스 輸入輸出, Unicode GUI 터미널을 實際資料 raspi4b에서 測試."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 執行命令 import 項目根, 命令


def 運行():
    輸出結果 = 項目根 / 'build/verification/shell'; 輸出結果.mkdir(parents=True, exist_ok=True)
    有效性驗證報告 = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((項目根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    執行記錄 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 工作中路徑:
        測試替身控制連接狀態 = Path(工作中路徑) / 'qmp.sock'
        程序 = subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(測試替身控制連接狀態)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        就緒情況監視器=selectors.DefaultSelector(); 就緒情況監視器.register(程序.stdout,selectors.EVENT_READ)
        def 接收消息(標記, 執行狀態超時=45):
            資料=bytearray(); 結束偏移=time.monotonic()+執行狀態超時
            while 標記 not in 資料:
                if time.monotonic()>結束偏移 or 程序.poll() is not None: raise AssertionError('UART timeout/exit: '+資料.decode('utf-8','replace'))
                for 已按下值,_ in 就緒情況監視器.select(.1):
                    片段值=已按下值.fileobj.read(4096)
                    if 片段值: 資料.extend(片段值); 執行記錄.extend(片段值)
                if b'PANIC:' in 資料 or b'FAIL ' in 資料: raise AssertionError(資料)
            return 資料.decode('utf-8','replace').replace('\r\n','\n')
        def 發送(資料, 標記=b'jkoros-native> '):
            程序.stdin.write(資料); 程序.stdin.flush(); return 接收消息(標記)
        def 命令殼(行, *預期):
            結果=發送(行.encode()+b'\n')
            for 值 in 預期: assert 值 in 結果, (行,值,結果)
            return 結果
        def 檔案(名稱):
            文本=命令殼('hex '+名稱,'HEX BEGIN','HEX END'); 搜索結果=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',文本,re.S)
            資料=bytes.fromhex(''.join(搜索結果.group(2).split())); assert len(資料)==int(搜索結果.group(1)); return 資料
        try:
            接收消息(b'jkoros-native> ')
            命令殼('mkdir 任務; cd 任務; pwd','/任務')
            命令殼('mkdir 하위; echo "한글 資料 😀" > 問候例.txt')
            assert 檔案('問候例.txt')=='한글 資料 😀\n'.encode()
            命令殼('cp 問候例.txt 複製值.txt; mv 複製值.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 資料 😀')
            命令殼('cd 하위; cat ../問候例.txt; cat /任務/問候例.txt; pwd','한글 資料 😀','/任務/하위')
            命令殼('cd ..; rmdir 하위; echo $?','1\n')
            命令殼('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            命令殼('cp 問候例.txt 問候例.txt; echo $?','1\n'); assert 檔案('問候例.txt')=='한글 資料 😀\n'.encode()
            命令殼('export 問候例=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/任務','GOOD')
            assert b'BAD\n' not in 檔案('問候例.txt')
            命令殼("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert 檔案('리터럴')=='$인사\n누리\n'.encode()
            命令殼('echo one > 語句值; echo two >> 語句值; echo three >> 語句值')
            命令殼('cat < 語句值 | grep t | tee 추림 | wc -l','2\n'); assert 檔案('추림')==b'two\nthree\n'
            命令殼('head -n 1 語句值 > 前端值; tail -n 1 語句值 > 後端值'); assert 檔案('앞')==b'one\n'; assert 檔案('뒤')==b'three\n'
            命令殼('grep absent 語句值; echo $?','1\n')
            命令殼('echo untouched > 保護值')
            命令殼('echo destroyed > 保護值 |','명령이 빠졌습니다'); assert 檔案('保護值')==b'untouched\n'
            命令殼('echo "oops','따옴표가 닫히지 않았습니다')
            命令殼('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            命令殼('echo bad 2> 保護值','번호를 지정한 檔案 描述符條目 輸入輸出 切換模式'); assert 檔案('保護值')==b'untouched\n'
            命令殼('rm 빈파일 리터럴 語句值 추림 前端值 後端值 保護值')
            有效性驗證報告['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            命令殼("python -c 'print(123)' | wc -c",'4\n')
            命令殼("python -c 'print(456)' > 程式.txt"); assert 檔案('程式.txt')==b'456\n'
            命令殼("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            命令殼("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < 程式.txt", "b'456\\n'", "b''")
            命令殼("python -c 'print(\"x\"*17000)' | wc -c", '錯誤 -28')
            命令殼('echo recovered | wc -c','10\n')
            命令殼("python -c 'import jkoros; print(jkoros.read("+'"/任務/程式.txt"'+"))'",'456','exit 0')
            命令殼('cd /; javac Hello.java','Compiled:','exit 0')
            命令殼('java Hello > /任務/Java.txt'); assert '안녕하세요'.encode() in 檔案('/任務/Java.txt')
            命令殼('cd 任務; echo "echo script > 執行狀態結果" > 命令.sh; echo "false || echo recovered >> 執行狀態結果" >> 命令.sh; sh 命令.sh')
            assert 檔案('執行狀態結果')==b'script\nrecovered\n'
            命令殼('rm 執行狀態結果; echo "exit 7" > 退出程式.sh; sh 退出程式.sh; echo $?','7\n')
            命令殼('rm 退出程式.sh 命令.sh 程式.txt Java.txt 問候例.txt; cd /; rmdir 任務')
            有效性驗證報告['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            命令殼('echo history-proof','history-proof')
            結果=發送(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 結果.count('history-proof')>=2, 結果
            發送(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            結果=發送(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 結果, 結果
            結果=發送(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 結果,結果
            結果=發送('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 結果,結果
            長整數文本='한글'*50
            結果=發送(('echo '+長整數文本+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+長整數文本+'\r\njkoros-native> ').encode()); assert '\n'+長整數文本+'\n' in 結果
            命令殼('terminal','TERMINAL READY')
            命令殼('clear')
            命令殼('echo "한글 終端 ABC xyz 012 😀"','한글 終端 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as 客戶端:
                客戶端.settimeout(10); 客戶端.connect(str(測試替身控制連接狀態))
                with 客戶端.makefile('rwb') as 流值:
                    json.loads(流值.readline())
                    def 調用(名稱,實際參數陣列=None):
                        網路消息={'execute':名稱}
                        if 實際參數陣列: 網路消息['arguments']=實際參數陣列
                        流值.write((json.dumps(網路消息)+'\n').encode()); 流值.flush()
                        while True:
                            回覆=json.loads(流值.readline())
                            if 'error' in 回覆: raise AssertionError(回覆)
                            if 'return' in 回覆: return 回覆['return']
                    調用('qmp_capabilities')
                    映像=輸出結果/'terminal.ppm'; 調用('screendump',{'filename':str(映像),'format':'ppm'})
                    調用('screendump',{'filename':str(輸出結果/'terminal.png'),'format':'png'})
                    資料=映像.read_bytes().split(b'\n',3)[3]
                    def 像素(橫座標座標,Y_按鈕座標): return tuple(資料[(Y_按鈕座標*640+橫座標座標)*3:(Y_按鈕座標*640+橫座標座標)*3+3])
                    assert 像素(12,48)==(32,80,144),像素(12,48)
                    assert len(set(像素(橫座標座標,Y_按鈕座標) for Y_按鈕座標 in range(100,116) for 橫座標座標 in range(24,56)))>1,'Hangul glyphs missing'
                    命令殼('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    命令殼("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    調用('screendump',{'filename':str(映像),'format':'ppm'})
                    已恢復資料=映像.read_bytes().split(b'\n',3)[3]
                    assert tuple(已恢復資料[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    命令殼('echo test > visible.txt; cat visible.txt','test')
                    for 序數索引 in range(27): 命令殼('echo scroll-'+str(序數索引),'scroll-'+str(序數索引))
                    發送(b'\x1b[5~\x1b[6~\n')
                    調用('screendump',{'filename':str(輸出結果/'terminal-scroll.png'),'format':'png'})
                    結果=發送(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 結果,結果
                    命令殼('rm visible.txt')
                    調用('quit')
            程序.wait(timeout=5)
            有效性驗證報告['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            有效性驗證報告['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if 程序.poll() is None:
                程序.terminate()
                try: 程序.wait(timeout=5)
                except subprocess.TimeoutExpired: 程序.kill(); 程序.wait()
            就緒情況監視器.close(); 程序.stdin.close(); 程序.stdout.close()
            (輸出結果/'serial.log').write_bytes(執行記錄)
            (輸出結果/'report.json').write_text(json.dumps(有效性驗證報告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': 運行()
