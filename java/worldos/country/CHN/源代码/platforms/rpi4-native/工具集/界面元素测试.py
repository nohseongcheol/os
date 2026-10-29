#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 执行命令 import 项目根,命令

def 运行():
    目的地址值位置=项目根/'build/verification/swing';目的地址值位置.mkdir(parents=True,exist_ok=True)
    类路径=项目根/'build/verification/new-java';类路径.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(项目根/'dist/jkoros-native-korean.jar'),'-d',str(类路径),str(项目根/'测试/Java/Swing测试.java'),str(项目根/'测试/Java/测试韩文字母窗口.java')])
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
            数据=(项目根/'build/verification/new-java/Swing测试.class').read_bytes()
            发送('load Swing测试.class\n'.encode(),b'hex> ')
            for 序数索引 in range(0,len(数据),64):发送(数据[序数索引:序数索引+64].hex().encode()+b'\n',b'hex> ')
            发送(b'.\n')
            发送('java Swing测试\n'.encode(),b'SWING READY')
            结束偏移=time.monotonic()+3
            while time.monotonic()<结束偏移:句柄事件(.1)
            # JFrame centered at (120,100), content at y=130.
            发送(单击按钮(200,210),b'',)  # focus JTextField
            数据位置.stdin.write('누리'.encode());数据位置.stdin.flush()
            结束偏移=time.monotonic()+.3
            while time.monotonic()<结束偏移:句柄事件(.05)
            结果=发送(单击按钮(200,255),'SWING CLICK 이름누리'.encode())
            等待(b'true',len(日志记录)-len(结果))
            发送(快捷操作值(1),b'TERMINAL FOCUS 2')
            结果=命令壳('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 结果
            发送(单击按钮(180,12),b'TERMINAL FOCUS 1')
            结束偏移=time.monotonic()+.3
            while time.monotonic()<结束偏移:句柄事件(.05)
            with socket.socket(socket.AF_UNIX) as 字符代码:
                字符代码.settimeout(10);字符代码.connect(str(测试替身控制连接状态))
                with 字符代码.makefile('rwb') as 文件条目:
                    json.loads(文件条目.readline())
                    for 申请值 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(目的地址值位置/'native-swing.png'),'format':'png'}}):
                        文件条目.write((json.dumps(申请值)+'\n').encode());文件条目.flush()
                        while True:
                            已返回值=json.loads(文件条目.readline())
                            if 'error' in 已返回值:raise AssertionError(已返回值)
                            if 'return' in 已返回值:break
            发送(单击按钮(505,115))
            命令壳('echo SWING_CLOSED_OK')
            数据=(类路径/'测试韩文字母窗口.class').read_bytes()
            发送('load 测试韩文字母窗口.class\n'.encode(),b'hex> ')
            for 序数索引 in range(0,len(数据),64):发送(数据[序数索引:序数索引+64].hex().encode()+b'\n',b'hex> ')
            发送(b'.\n')
            发送('java 测试韩文字母窗口\n'.encode(),b'KOREAN SWING READY')
            发送(单击按钮(200,255),'KOREAN SWING CLICK 名称'.encode())
            发送(单击按钮(505,115))
            命令壳('echo KOREAN_SWING_CLOSED_OK')
            有效性验证报告.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','中文 窗口/按钮/动作通知/事件排队 directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 数据位置.poll() is None:数据位置.terminate()
            try:数据位置.wait(timeout=5)
            except subprocess.TimeoutExpired:数据位置.kill();数据位置.wait()
            选择器.close();数据位置.stdin.close();数据位置.stdout.close();(目的地址值位置/'serial.log').write_bytes(日志记录);(目的地址值位置/'report.json').write_text(json.dumps(有效性验证报告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':运行()
