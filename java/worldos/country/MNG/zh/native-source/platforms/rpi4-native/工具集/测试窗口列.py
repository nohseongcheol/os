#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 执行命令 import 项目根,命令

def 运行():
    目的地址值位置=项目根/'build/verification/windows';目的地址值位置.mkdir(parents=True,exist_ok=True)
    有效性验证报告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest()};日志记录=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 工作中路径:
        测试替身控制连接状态=Path(工作中路径)/'qmp.sock'
        数据位置=subprocess.Popen(命令()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(测试替身控制连接状态)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        选择器=selectors.DefaultSelector();选择器.register(数据位置.stdout,selectors.EVENT_READ)
        def 句柄事件(秒数单位=.1):
            for 已按下值,_ in 选择器.select(秒数单位):
                第二值=已按下值.fileobj.read(65536)
                if 第二值:日志记录.extend(第二值)
            assert b'PANIC:' not in 日志记录 and b'HALTED' not in 日志记录,日志记录[-2048:]
        def 等待(标记,当前位置,秒数单位=50):
            结束偏移=time.monotonic()+秒数单位
            while 标记 not in 日志记录[当前位置:]:
                if time.monotonic()>结束偏移 or 数据位置.poll() is not None:raise AssertionError(日志记录[当前位置:].decode('utf-8','replace'))
                句柄事件()
            return bytes(日志记录[当前位置:])
        def 发送(第二值,标记=b'jkoros-native> '):
            当前位置=len(日志记录);数据位置.stdin.write(第二值);数据位置.stdin.flush();return 等待(标记,当前位置)
        def 命令壳(字符串数据):return 发送((字符串数据+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def 快捷操作值(第三索引):return bytes([30,2,第三索引,0,0,0,0])
        def 单击按钮(横坐标坐标,Y_按钮坐标):return bytes([30,1,1,横坐标坐标&255,横坐标坐标>>8,Y_按钮坐标&255,Y_按钮坐标>>8,30,1,0,横坐标坐标&255,横坐标坐标>>8,Y_按钮坐标&255,Y_按钮坐标>>8])
        def 命令模式():
            数据位置.stdin.write(b'\x1b');数据位置.stdin.flush();结束偏移=time.monotonic()+.2
            while time.monotonic()<结束偏移:句柄事件(.03)
        try:
            等待(b'jkoros-native> ',0)
            命令壳('terminal');句柄事件(.3)
            命令壳('mkdir first; cd first; export NAME=one')
            发送('vi 首位序数.py\n'.encode(),b'NORMAL')
            发送('i값 = 21\nprint(值 * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            结束偏移=time.monotonic()+3
            while time.monotonic()<结束偏移:句柄事件(.1)
            发送(快捷操作值(1),b'TERMINAL FOCUS 2');句柄事件(.2)
            assert b'/\r\n' in 命令壳('pwd')
            命令壳('export NAME=two')
            发送('vi 第二序数.txt\n'.encode(),b'NORMAL')
            发送('i두 번째 窗口\n'.encode(),b'INSERT')
            发送(单击按钮(180,12),b'TERMINAL FOCUS 1');句柄事件(.2)
            命令模式();发送(b':wq\r')
            assert b'one:/first' in 命令壳('echo "$NAME:$PWD"')
            assert '值 = 21\r\nprint(值 * 2)'.encode() in 命令壳('cat 首位序数.py')
            结果=命令壳('python 首位序数.py');assert b'42\r\n' in 结果,结果
            # Close the first shell with its actual title-bar X; second editor resumes.
            发送(单击按钮(560,63),b'TERMINAL FOCUS 2');句柄事件(.2)
            命令模式();发送(b':wq\r')
            assert b'two:/' in 命令壳('echo "$NAME:$PWD"')
            assert '두 번째 窗口'.encode() in 命令壳('cat 第二序数.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            发送('vi 第二序数.txt\n'.encode(),b'NORMAL');发送(b'xu',b'NORMAL')
            发送(b'iX',b'INSERT');命令模式();发送(b':q\r',b'Unsaved')
            发送(b':q!\r');assert '두 번째 窗口'.encode() in 命令壳('cat 第二序数.txt')
            发送(快捷操作值(1),b'TERMINAL FOCUS 1');句柄事件(.2)
            发送(快捷操作值(1),b'TERMINAL FOCUS 3');句柄事件(.2)
            发送(快捷操作值(1),b'TERMINAL FOCUS 4');句柄事件(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            数据位置.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));数据位置.stdin.flush()
            命令壳('echo DRAGGED_OK')
            发送('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            发送('i저장하지 않은 数据'.encode(),b'INSERT')
            发送(单击按钮(578,97),b'TERMINAL FOCUS 3');句柄事件(.2)
            assert '버릴문서.txt'.encode() not in 命令壳('ls')
            发送(快捷操作值(1),b'TERMINAL FOCUS 4');句柄事件(.2)
            命令壳('echo REUSED_WINDOW_OK')
            已完成总量=日志记录.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            等待(b'jkoros-native> ',已完成总量)
            # UART completion precedes the next QEMU display refresh.
            结束偏移=time.monotonic()+.3
            while time.monotonic()<结束偏移:句柄事件(.05)
            with socket.socket(socket.AF_UNIX) as 字符代码:
                字符代码.settimeout(10);字符代码.connect(str(测试替身控制连接状态))
                with 字符代码.makefile('rwb') as 文件条目:
                    json.loads(文件条目.readline())
                    for 申请值 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(目的地址值位置/'four-terminals.png'),'format':'png'}}):
                        文件条目.write((json.dumps(申请值)+'\n').encode());文件条目.flush()
                        while True:
                            已返回值=json.loads(文件条目.readline())
                            if 'error' in 已返回值:raise AssertionError(已返回值)
                            if 'return' in 已返回值:break
            from PIL import Image
            像素列列表=Image.open(str(目的地址值位置/'four-terminals.png')).convert('RGB')
            for 坐标一对,像素颜色 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 像素列列表.getpixel(坐标一对)==像素颜色,(坐标一对,像素列列表.getpixel(坐标一对))
            命令壳('echo FOUR_WINDOWS_OK')
            有效性验证报告.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 数据位置.poll() is None:数据位置.terminate()
            try:数据位置.wait(timeout=5)
            except subprocess.TimeoutExpired:数据位置.kill();数据位置.wait()
            选择器.close();数据位置.stdin.close();数据位置.stdout.close();(目的地址值位置/'serial.log').write_bytes(日志记录);(目的地址值位置/'report.json').write_text(json.dumps(有效性验证报告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':运行()
