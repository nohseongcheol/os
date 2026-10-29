#!/usr/bin/env python3
"""内置 커널의 命令壳, 프로세스 输入输出, Unicode GUI 터미널을 实际数据 raspi4b에서 测试."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 执行命令 import 项目根, 命令


def 运行():
    输出结果 = 项目根 / 'build/verification/shell'; 输出结果.mkdir(parents=True, exist_ok=True)
    有效性验证报告 = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((项目根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    执行记录 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 工作中路径:
        测试替身控制连接状态 = Path(工作中路径) / 'qmp.sock'
        进程 = subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(测试替身控制连接状态)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        就绪情况监视器=selectors.DefaultSelector(); 就绪情况监视器.register(进程.stdout,selectors.EVENT_READ)
        def 接收消息(标记, 执行状态超时=45):
            数据=bytearray(); 结束偏移=time.monotonic()+执行状态超时
            while 标记 not in 数据:
                if time.monotonic()>结束偏移 or 进程.poll() is not None: raise AssertionError('UART timeout/exit: '+数据.decode('utf-8','replace'))
                for 已按下值,_ in 就绪情况监视器.select(.1):
                    片段值=已按下值.fileobj.read(4096)
                    if 片段值: 数据.extend(片段值); 执行记录.extend(片段值)
                if b'PANIC:' in 数据 or b'FAIL ' in 数据: raise AssertionError(数据)
            return 数据.decode('utf-8','replace').replace('\r\n','\n')
        def 发送(数据, 标记=b'jkoros-native> '):
            进程.stdin.write(数据); 进程.stdin.flush(); return 接收消息(标记)
        def 命令壳(行, *预期):
            结果=发送(行.encode()+b'\n')
            for 值 in 预期: assert 值 in 结果, (行,值,结果)
            return 结果
        def 文件(名称):
            文本=命令壳('hex '+名称,'HEX BEGIN','HEX END'); 搜索结果=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',文本,re.S)
            数据=bytes.fromhex(''.join(搜索结果.group(2).split())); assert len(数据)==int(搜索结果.group(1)); return 数据
        try:
            接收消息(b'jkoros-native> ')
            命令壳('mkdir 任务; cd 任务; pwd','/任务')
            命令壳('mkdir 하위; echo "한글 数据 😀" > 问候例.txt')
            assert 文件('问候例.txt')=='한글 数据 😀\n'.encode()
            命令壳('cp 问候例.txt 复制值.txt; mv 复制值.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 数据 😀')
            命令壳('cd 하위; cat ../问候例.txt; cat /任务/问候例.txt; pwd','한글 数据 😀','/任务/하위')
            命令壳('cd ..; rmdir 하위; echo $?','1\n')
            命令壳('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            命令壳('cp 问候例.txt 问候例.txt; echo $?','1\n'); assert 文件('问候例.txt')=='한글 数据 😀\n'.encode()
            命令壳('export 问候例=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/任务','GOOD')
            assert b'BAD\n' not in 文件('问候例.txt')
            命令壳("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert 文件('리터럴')=='$인사\n누리\n'.encode()
            命令壳('echo one > 语句值; echo two >> 语句值; echo three >> 语句值')
            命令壳('cat < 语句值 | grep t | tee 추림 | wc -l','2\n'); assert 文件('추림')==b'two\nthree\n'
            命令壳('head -n 1 语句值 > 前端值; tail -n 1 语句值 > 后端值'); assert 文件('앞')==b'one\n'; assert 文件('뒤')==b'three\n'
            命令壳('grep absent 语句值; echo $?','1\n')
            命令壳('echo untouched > 保护值')
            命令壳('echo destroyed > 保护值 |','명령이 빠졌습니다'); assert 文件('保护值')==b'untouched\n'
            命令壳('echo "oops','따옴표가 닫히지 않았습니다')
            命令壳('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            命令壳('echo bad 2> 保护值','번호를 지정한 文件 描述符条目 输入输出 切换模式'); assert 文件('保护值')==b'untouched\n'
            命令壳('rm 빈파일 리터럴 语句值 추림 前端值 后端值 保护值')
            有效性验证报告['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            命令壳("python -c 'print(123)' | wc -c",'4\n')
            命令壳("python -c 'print(456)' > 程序.txt"); assert 文件('程序.txt')==b'456\n'
            命令壳("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            命令壳("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < 程序.txt", "b'456\\n'", "b''")
            命令壳("python -c 'print(\"x\"*17000)' | wc -c", '错误 -28')
            命令壳('echo recovered | wc -c','10\n')
            命令壳("python -c 'import jkoros; print(jkoros.read("+'"/任务/程序.txt"'+"))'",'456','exit 0')
            命令壳('cd /; javac Hello.java','Compiled:','exit 0')
            命令壳('java Hello > /任务/Java.txt'); assert '안녕하세요'.encode() in 文件('/任务/Java.txt')
            命令壳('cd 任务; echo "echo script > 执行状态结果" > 命令.sh; echo "false || echo recovered >> 执行状态结果" >> 命令.sh; sh 命令.sh')
            assert 文件('执行状态结果')==b'script\nrecovered\n'
            命令壳('rm 执行状态结果; echo "exit 7" > 退出程序.sh; sh 退出程序.sh; echo $?','7\n')
            命令壳('rm 退出程序.sh 命令.sh 程序.txt Java.txt 问候例.txt; cd /; rmdir 任务')
            有效性验证报告['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            命令壳('echo history-proof','history-proof')
            结果=发送(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 结果.count('history-proof')>=2, 结果
            发送(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            结果=发送(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 结果, 结果
            结果=发送(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 结果,结果
            结果=发送('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 结果,结果
            长整数文本='한글'*50
            结果=发送(('echo '+长整数文本+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+长整数文本+'\r\njkoros-native> ').encode()); assert '\n'+长整数文本+'\n' in 结果
            命令壳('terminal','TERMINAL READY')
            命令壳('clear')
            命令壳('echo "한글 终端 ABC xyz 012 😀"','한글 终端 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as 客户端:
                客户端.settimeout(10); 客户端.connect(str(测试替身控制连接状态))
                with 客户端.makefile('rwb') as 流值:
                    json.loads(流值.readline())
                    def 调用(名称,参数数组=None):
                        网络消息={'execute':名称}
                        if 参数数组: 网络消息['arguments']=参数数组
                        流值.write((json.dumps(网络消息)+'\n').encode()); 流值.flush()
                        while True:
                            回复=json.loads(流值.readline())
                            if 'error' in 回复: raise AssertionError(回复)
                            if 'return' in 回复: return 回复['return']
                    调用('qmp_capabilities')
                    映像=输出结果/'terminal.ppm'; 调用('screendump',{'filename':str(映像),'format':'ppm'})
                    调用('screendump',{'filename':str(输出结果/'terminal.png'),'format':'png'})
                    数据=映像.read_bytes().split(b'\n',3)[3]
                    def 像素(横坐标坐标,Y_按钮坐标): return tuple(数据[(Y_按钮坐标*640+横坐标坐标)*3:(Y_按钮坐标*640+横坐标坐标)*3+3])
                    assert 像素(12,48)==(32,80,144),像素(12,48)
                    assert len(set(像素(横坐标坐标,Y_按钮坐标) for Y_按钮坐标 in range(100,116) for 横坐标坐标 in range(24,56)))>1,'Hangul glyphs missing'
                    命令壳('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    命令壳("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    调用('screendump',{'filename':str(映像),'format':'ppm'})
                    已恢复数据=映像.read_bytes().split(b'\n',3)[3]
                    assert tuple(已恢复数据[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    命令壳('echo test > visible.txt; cat visible.txt','test')
                    for 序数索引 in range(27): 命令壳('echo scroll-'+str(序数索引),'scroll-'+str(序数索引))
                    发送(b'\x1b[5~\x1b[6~\n')
                    调用('screendump',{'filename':str(输出结果/'terminal-scroll.png'),'format':'png'})
                    结果=发送(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 结果,结果
                    命令壳('rm visible.txt')
                    调用('quit')
            进程.wait(timeout=5)
            有效性验证报告['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            有效性验证报告['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if 进程.poll() is None:
                进程.terminate()
                try: 进程.wait(timeout=5)
                except subprocess.TimeoutExpired: 进程.kill(); 进程.wait()
            就绪情况监视器.close(); 进程.stdin.close(); 进程.stdout.close()
            (输出结果/'serial.log').write_bytes(执行记录)
            (输出结果/'report.json').write_text(json.dumps(有效性验证报告,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': 运行()
