#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from executeCommand import projectRoot


def run():
    resultData=projectRoot/'build/verification/remmina';resultData.mkdir(parents=True,exist_ok=True)
    validationReport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as workingPath:
        workingPath=Path(workingPath);runningProcesses=[];selector=selectors.DefaultSelector();serialIo=bytearray()
        logRecords=[]
        try:
            virtualDisplay=shutil.which('Xvfb')
            if virtualDisplay: serverValue=[virtualDisplay]
            else:
                rootfs=projectRoot.parent/'rpi4/build/rootfs'
                serverValue=['qemu-aarch64','-L',str(rootfs),str(rootfs/'usr/bin/Xvfb')]
            def run(argumentArray,environment=None,**namedArgument):
                logRecord=(resultData/('process-%d.log'%len(logRecords))).open('wb');logRecords.append(logRecord)
                dataPosition=subprocess.Popen(argumentArray,env=environment,stdout=logRecord,stderr=subprocess.STDOUT,**namedArgument)
                runningProcesses.append(dataPosition);return dataPosition
            environment=dict(os.environ)
            for name in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):environment.pop(name,None)
            environment.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(workingPath/'config'),XDG_DATA_HOME=str(workingPath/'data'),XDG_CACHE_HOME=str(workingPath/'cache'))
            numericValue=next(itemCount for itemCount in range(80,200) if not Path('/tmp/.X11-unix/X'+str(itemCount)).exists() and not Path('/tmp/.X%d-lock'%itemCount).exists())
            environment['DISPLAY']=':'+str(numericValue)
            displayDevice=run(serverValue+[environment['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],environment=environment)
            deadlineTime=time.monotonic()+30
            while True:
                assert displayDevice.poll() is None and time.monotonic()<deadlineTime,'Xvfb failed; see process-0.log'
                preparationComplete=subprocess.run(['xdotool','getdisplaygeometry'],env=environment,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if preparationComplete.returncode==0:break
                time.sleep(.1)
            guest=subprocess.Popen(['python3',str(projectRoot/'tools/executeCommand.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            runningProcesses.append(guest);selector.register(guest.stdout,selectors.EVENT_READ)
            def await(marker,offsetValue=0):
                deadlineTime=time.monotonic()+45
                while marker not in serialIo[offsetValue:]:
                    assert guest.poll() is None and time.monotonic()<deadlineTime,serialIo[offsetValue:].decode('utf-8','replace')
                    for pressedValue,_ in selector.select(.1):
                        data=pressedValue.fileobj.read(65536)
                        if data:serialIo.extend(data)
            await(b'TERMINAL READY');await(b'jkoros-native> ',serialIo.rfind(b'TERMINAL READY'))
            portNumber=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',serialIo).group(1))
            profile=workingPath/'test.remmina'
            profile.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%portNumber)
            run(['dbus-run-session','--','remmina','-c',str(profile)],environment=environment,start_new_session=True)
            def virtualInputTool(*argumentArray):return subprocess.check_output(['xdotool']+list(argumentArray),env=environment,stderr=subprocess.STDOUT)
            deadlineTime=time.monotonic()+60;window=None
            while time.monotonic()<deadlineTime:
                searchResult=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=environment,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if searchResult.returncode==0:
                    candidate=searchResult.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    focused=subprocess.run(['xdotool','windowfocus','--sync',candidate],env=environment,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if focused.returncode==0:window=candidate;break
                time.sleep(.1)
            assert window,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            virtualInputTool('mousemove','--window',window,'280','240','click','1')
            time.sleep(1)
            def typedCharacter(text):virtualInputTool('type','--clearmodifiers','--delay','50',text)
            def pressedValue(*pressedKeys):virtualInputTool('key','--clearmodifiers',*pressedKeys)
            offsetValue=len(serialIo);typedCharacter('echo ');pressedValue('F9');typedCharacter('dkssudgktpdy gksrmf');pressedValue('F9','Return')
            await('\r\n안녕하세요 hangulText\r\njkoros-native> '.encode(),offsetValue)
            offsetValue=len(serialIo);typedCharacter('echo ');pressedValue('shift+space');typedCharacter('rhk rkqtk');pressedValue('shift+space','Return')
            await('\r\n과 갑사\r\njkoros-native> '.encode(),offsetValue)
            offsetValue=len(serialIo);typedCharacter('help ko');pressedValue('Return')
            await('한/zeroOperand keyValue, Shift+Space 또는 F9'.encode(),offsetValue);await(b'jkoros-native> ',offsetValue)
            offsetValue=len(serialIo);typedCharacter('echo ');pressedValue('F9');typedCharacter('gksrmf dlfr')
            await('읽'.encode(),offsetValue)
            subprocess.check_call(['import','-display',environment['DISPLAY'],'-window',window,str(resultData/'remmina-korean.png')])
            pressedValue('F9','Return')
            await(b'jkoros-native> ',offsetValue)
            # actualData Remmina의 Screen 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            drawingValue=Image.open(str(resultData/'remmina-korean.png')).convert('RGB')
            titleBar=None
            for verticalPosition in range(drawingValue.height):
                horizontalPositions=[horizontalPosition for horizontalPosition in range(drawingValue.width) if drawingValue.getpixel((horizontalPosition,verticalPosition))==(32,80,144)]
                if len(horizontalPositions)>=500:titleBar=(min(horizontalPositions),verticalPosition);break
            assert titleBar,'native terminal title bar not found'
            horizontalPosition,verticalPosition=titleBar[0]+564,titleBar[1]+356
            virtualInputTool('mousemove','--window',window,str(horizontalPosition),str(verticalPosition))
            def waitForBitmap(name,pointsList):
                deadlineValue=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',environment['DISPLAY'],'-window',window,str(resultData/name)])
                    bitmapImage=Image.open(str(resultData/name)).convert('RGB')
                    if all(bitmapImage.getpixel(position)==Colour for position,Colour in pointsList):return
                    assert time.monotonic()<deadlineValue,'Remmina framebuffer did not settle: '+name
                    time.sleep(.1)
            waitForBitmap('remmina-resize-cursor.png',[
                ((horizontalPosition-7,verticalPosition-7),(255,255,255)),((horizontalPosition+7,verticalPosition+7),(255,255,255))])
            virtualInputTool('mousedown','1','mousemove','--window',window,str(horizontalPosition-120),str(verticalPosition-80),'mouseup','1')
            time.sleep(.4)
            offsetValue=len(serialIo);typedCharacter('terminal size');pressedValue('Return')
            await(b'TERMINAL SIZE 53x14\r\n',offsetValue)
            virtualInputTool('mousemove','--window',window,'500','45')
            waitForBitmap('remmina-resized.png',[
                ((titleBar[0]+447,titleBar[1]+279),(39,49,64)),((horizontalPosition,verticalPosition),(24,32,48))])
            if shutil.which('dpkg-query'):
                versionNumber=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versionNumber=subprocess.check_output(['remmina','--version'],env=environment,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validationReport.update(passed=True,display=environment['DISPLAY'],remmina_version=versionNumber,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validationReport['passed'] and 'environment' in locals() and environment.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',environment['DISPLAY'],'-window','root',str(resultData/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for dataPosition in reversed(runningProcesses):
                if dataPosition.poll() is None:
                    if dataPosition.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(dataPosition.pid,signal.SIGTERM)
                    else:dataPosition.terminate()
                    try:dataPosition.wait(timeout=5)
                    except subprocess.TimeoutExpired:dataPosition.kill();dataPosition.wait()
            selector.close()
            for fileEntry in logRecords:fileEntry.close()
            (resultData/'serial.log').write_bytes(serialIo)
            (resultData/'report.json').write_text(json.dumps(validationReport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':run()
