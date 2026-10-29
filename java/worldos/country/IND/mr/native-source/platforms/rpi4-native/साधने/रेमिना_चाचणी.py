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
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ


def सुरू_करा():
    मोजमाप_डेटा=प्रोजेक्ट_मूळ/'build/verification/remmina';मोजमाप_डेटा.mkdir(parents=True,exist_ok=True)
    पडताळणी_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as कार्यरत_पथ:
        कार्यरत_पथ=Path(कार्यरत_पथ);धावणे_प्रक्रिया=[];निवडक=selectors.DefaultSelector();अनुक्रमिक_आदानप्रदान=bytearray()
        लॉग_नोंदी=[]
        try:
            व्हर्च्युअल_प्रदर्शन=shutil.which('Xvfb')
            if व्हर्च्युअल_प्रदर्शन: सर्व्हर_मूल्य=[व्हर्च्युअल_प्रदर्शन]
            else:
                मूळसंचिकाव्यवस्था=प्रोजेक्ट_मूळ.parent/'rpi4/build/rootfs'
                सर्व्हर_मूल्य=['qemu-aarch64','-L',str(मूळसंचिकाव्यवस्था),str(मूळसंचिकाव्यवस्था/'usr/bin/Xvfb')]
            def सुरू_करा(वितर्क_ऍरे,पर्यावरण=None,**नामांकित_वितर्क):
                लॉग_नोंद=(मोजमाप_डेटा/('process-%d.log'%len(लॉग_नोंदी))).open('wb');लॉग_नोंदी.append(लॉग_नोंद)
                डेटा_स्थान=subprocess.Popen(वितर्क_ऍरे,env=पर्यावरण,stdout=लॉग_नोंद,stderr=subprocess.STDOUT,**नामांकित_वितर्क)
                धावणे_प्रक्रिया.append(डेटा_स्थान);return डेटा_स्थान
            पर्यावरण=dict(os.environ)
            for नाव in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):पर्यावरण.pop(नाव,None)
            पर्यावरण.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(कार्यरत_पथ/'config'),XDG_DATA_HOME=str(कार्यरत_पथ/'data'),XDG_CACHE_HOME=str(कार्यरत_पथ/'cache'))
            संख्यात्मक_मूल्य=next(आयटम_संख्या for आयटम_संख्या in range(80,200) if not Path('/tmp/.X11-unix/X'+str(आयटम_संख्या)).exists() and not Path('/tmp/.X%d-lock'%आयटम_संख्या).exists())
            पर्यावरण['DISPLAY']=':'+str(संख्यात्मक_मूल्य)
            प्रदर्शन=सुरू_करा(सर्व्हर_मूल्य+[पर्यावरण['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],पर्यावरण=पर्यावरण)
            अंतिमवेळ_वेळ=time.monotonic()+30
            while True:
                assert प्रदर्शन.poll() is None and time.monotonic()<अंतिमवेळ_वेळ,'Xvfb failed; see process-0.log'
                तयारी_पूर्ण=subprocess.run(['xdotool','getdisplaygeometry'],env=पर्यावरण,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if तयारी_पूर्ण.returncode==0:break
                time.sleep(.1)
            अतिथी=subprocess.Popen(['python3',str(प्रोजेक्ट_मूळ/'साधने/आज्ञा_कार्यवाही_करा.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            धावणे_प्रक्रिया.append(अतिथी);निवडक.register(अतिथी.stdout,selectors.EVENT_READ)
            def प्रतीक्षाकरा(खूण,ऑफसेट_मूल्य=0):
                अंतिमवेळ_वेळ=time.monotonic()+45
                while खूण not in अनुक्रमिक_आदानप्रदान[ऑफसेट_मूल्य:]:
                    assert अतिथी.poll() is None and time.monotonic()<अंतिमवेळ_वेळ,अनुक्रमिक_आदानप्रदान[ऑफसेट_मूल्य:].decode('utf-8','replace')
                    for दाबलेले_मूल्य,_ in निवडक.select(.1):
                        डेटा=दाबलेले_मूल्य.fileobj.read(65536)
                        if डेटा:अनुक्रमिक_आदानप्रदान.extend(डेटा)
            प्रतीक्षाकरा(b'TERMINAL READY');प्रतीक्षाकरा(b'jkoros-native> ',अनुक्रमिक_आदानप्रदान.rfind(b'TERMINAL READY'))
            पोर्ट_नंबर=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',अनुक्रमिक_आदानप्रदान).group(1))
            प्रोफाइल=कार्यरत_पथ/'test.remmina'
            प्रोफाइल.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%पोर्ट_नंबर)
            सुरू_करा(['dbus-run-session','--','remmina','-c',str(प्रोफाइल)],पर्यावरण=पर्यावरण,start_new_session=True)
            def व्हर्च्युअल_आदान_साधन(*वितर्क_ऍरे):return subprocess.check_output(['xdotool']+list(वितर्क_ऍरे),env=पर्यावरण,stderr=subprocess.STDOUT)
            अंतिमवेळ_वेळ=time.monotonic()+60;विंडो=None
            while time.monotonic()<अंतिमवेळ_वेळ:
                शोध_मोजमाप=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=पर्यावरण,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if शोध_मोजमाप.returncode==0:
                    उमेदवार=शोध_मोजमाप.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    केंद्रित=subprocess.run(['xdotool','windowfocus','--sync',उमेदवार],env=पर्यावरण,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if केंद्रित.returncode==0:विंडो=उमेदवार;break
                time.sleep(.1)
            assert विंडो,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            व्हर्च्युअल_आदान_साधन('mousemove','--window',विंडो,'280','240','click','1')
            time.sleep(1)
            def टंकित_वर्ण(पाठ्य):व्हर्च्युअल_आदान_साधन('type','--clearmodifiers','--delay','50',पाठ्य)
            def दाबलेले_मूल्य(*दाबलेले_कळा):व्हर्च्युअल_आदान_साधन('key','--clearmodifiers',*दाबलेले_कळा)
            ऑफसेट_मूल्य=len(अनुक्रमिक_आदानप्रदान);टंकित_वर्ण('echo ');दाबलेले_मूल्य('F9');टंकित_वर्ण('dkssudgktpdy gksrmf');दाबलेले_मूल्य('F9','Return')
            प्रतीक्षाकरा('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(अनुक्रमिक_आदानप्रदान);टंकित_वर्ण('echo ');दाबलेले_मूल्य('shift+space');टंकित_वर्ण('rhk rkqtk');दाबलेले_मूल्य('shift+space','Return')
            प्रतीक्षाकरा('\r\n과 갑사\r\njkoros-native> '.encode(),ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(अनुक्रमिक_आदानप्रदान);टंकित_वर्ण('help ko');दाबलेले_मूल्य('Return')
            प्रतीक्षाकरा('한/शून्य_संकार्य कळ_मूल्य, Shift+Space 또는 F9'.encode(),ऑफसेट_मूल्य);प्रतीक्षाकरा(b'jkoros-native> ',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(अनुक्रमिक_आदानप्रदान);टंकित_वर्ण('echo ');दाबलेले_मूल्य('F9');टंकित_वर्ण('gksrmf dlfr')
            प्रतीक्षाकरा('읽'.encode(),ऑफसेट_मूल्य)
            subprocess.check_call(['import','-display',पर्यावरण['DISPLAY'],'-window',विंडो,str(मोजमाप_डेटा/'remmina-korean.png')])
            दाबलेले_मूल्य('F9','Return')
            प्रतीक्षाकरा(b'jkoros-native> ',ऑफसेट_मूल्य)
            # वास्तविक_डेटा Remmina의 पडदा 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            रेखांकन_मूल्य=Image.open(str(मोजमाप_डेटा/'remmina-korean.png')).convert('RGB')
            शीर्षक_पट्_टी=None
            for अनुलंब_स्थान in range(रेखांकन_मूल्य.height):
                आडवे_स्थाने=[आडवे_स्थान for आडवे_स्थान in range(रेखांकन_मूल्य.width) if रेखांकन_मूल्य.getpixel((आडवे_स्थान,अनुलंब_स्थान))==(32,80,144)]
                if len(आडवे_स्थाने)>=500:शीर्षक_पट्_टी=(min(आडवे_स्थाने),अनुलंब_स्थान);break
            assert शीर्षक_पट्_टी,'native terminal title bar not found'
            आडवे_स्थान,अनुलंब_स्थान=शीर्षक_पट्_टी[0]+564,शीर्षक_पट्_टी[1]+356
            व्हर्च्युअल_आदान_साधन('mousemove','--window',विंडो,str(आडवे_स्थान),str(अनुलंब_स्थान))
            def प्रतीक्षा_करा_साठी_बिटमॅप(नाव,बिंदू_यादी):
                अंतिमवेळ_मूल्य=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',पर्यावरण['DISPLAY'],'-window',विंडो,str(मोजमाप_डेटा/नाव)])
                    बिटमॅप_चित्र=Image.open(str(मोजमाप_डेटा/नाव)).convert('RGB')
                    if all(बिटमॅप_चित्र.getpixel(जागा)==रंग for जागा,रंग in बिंदू_यादी):return
                    assert time.monotonic()<अंतिमवेळ_मूल्य,'Remmina framebuffer did not settle: '+नाव
                    time.sleep(.1)
            प्रतीक्षा_करा_साठी_बिटमॅप('remmina-resize-cursor.png',[
                ((आडवे_स्थान-7,अनुलंब_स्थान-7),(255,255,255)),((आडवे_स्थान+7,अनुलंब_स्थान+7),(255,255,255))])
            व्हर्च्युअल_आदान_साधन('mousedown','1','mousemove','--window',विंडो,str(आडवे_स्थान-120),str(अनुलंब_स्थान-80),'mouseup','1')
            time.sleep(.4)
            ऑफसेट_मूल्य=len(अनुक्रमिक_आदानप्रदान);टंकित_वर्ण('terminal size');दाबलेले_मूल्य('Return')
            प्रतीक्षाकरा(b'TERMINAL SIZE 53x14\r\n',ऑफसेट_मूल्य)
            व्हर्च्युअल_आदान_साधन('mousemove','--window',विंडो,'500','45')
            प्रतीक्षा_करा_साठी_बिटमॅप('remmina-resized.png',[
                ((शीर्षक_पट्_टी[0]+447,शीर्षक_पट्_टी[1]+279),(39,49,64)),((आडवे_स्थान,अनुलंब_स्थान),(24,32,48))])
            if shutil.which('dpkg-query'):
                आवृत्ती_संख्या=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                आवृत्ती_संख्या=subprocess.check_output(['remmina','--version'],env=पर्यावरण,stderr=subprocess.STDOUT).decode('utf-8','replace')
            पडताळणी_अहवाल.update(passed=True,display=पर्यावरण['DISPLAY'],remmina_version=आवृत्ती_संख्या,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not पडताळणी_अहवाल['passed'] and 'पर्यावरण' in locals() and पर्यावरण.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',पर्यावरण['DISPLAY'],'-window','root',str(मोजमाप_डेटा/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for डेटा_स्थान in reversed(धावणे_प्रक्रिया):
                if डेटा_स्थान.poll() is None:
                    if डेटा_स्थान.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(डेटा_स्थान.pid,signal.SIGTERM)
                    else:डेटा_स्थान.terminate()
                    try:डेटा_स्थान.wait(timeout=5)
                    except subprocess.TimeoutExpired:डेटा_स्थान.kill();डेटा_स्थान.wait()
            निवडक.close()
            for संचिका_प्रविष्टी in लॉग_नोंदी:संचिका_प्रविष्टी.close()
            (मोजमाप_डेटा/'serial.log').write_bytes(अनुक्रमिक_आदानप्रदान)
            (मोजमाप_डेटा/'report.json').write_text(json.dumps(पडताळणी_अहवाल,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':सुरू_करा()
