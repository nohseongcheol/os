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
from Izpildīt_komanda import Project_sakne


def Palaist():
    mērs_dati=Project_sakne/'build/verification/remmina';mērs_dati.mkdir(parents=True,exist_ok=True)
    validācija_ziņot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];atlasītājs=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: serveris_VALUE=[가상표시장치]
            else:
                뿌리파일계층=Project_sakne.parent/'rpi4/build/rootfs'
                serveris_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Palaist(arg_ARRAY,환경=None,**nosaukts_arguments):
                LOG_RECORD=(mērs_dati/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                dati_amats=subprocess.Popen(arg_ARRAY,env=환경,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**nosaukts_arguments)
                실행과정들.append(dati_amats);return dati_amats
            환경=dict(os.environ)
            for Nosaukums in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Nosaukums,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(krājums_COUNT for krājums_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(krājums_COUNT)).exists() and not Path('/tmp/.X%d-lock'%krājums_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            displejs=Palaist(serveris_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            izpildes_termiņš_TIME=time.monotonic()+30
            while True:
                assert displejs.poll() is None and time.monotonic()<izpildes_termiņš_TIME,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            viesis=subprocess.Popen(['python3',str(Project_sakne/'Rīki/Izpildīt_komanda.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(viesis);atlasītājs.register(viesis.stdout,selectors.EVENT_READ)
            def 기다리기(marķieris,Nobīde_VALUE=0):
                izpildes_termiņš_TIME=time.monotonic()+45
                while marķieris not in 직렬입출력[Nobīde_VALUE:]:
                    assert viesis.poll() is None and time.monotonic()<izpildes_termiņš_TIME,직렬입출력[Nobīde_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in atlasītājs.select(.1):
                        dati=누름값.fileobj.read(65536)
                        if dati:직렬입출력.extend(dati)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            porta_numurs=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profils=작업경로/'test.remmina'
            Profils.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%porta_numurs)
            Palaist(['dbus-run-session','--','remmina','-c',str(Profils)],환경=환경,start_new_session=True)
            def 가상입력도구(*arg_ARRAY):return subprocess.check_output(['xdotool']+list(arg_ARRAY),env=환경,stderr=subprocess.STDOUT)
            izpildes_termiņš_TIME=time.monotonic()+60;Logs=None
            while time.monotonic()<izpildes_termiņš_TIME:
                Meklēt_mērs=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Meklēt_mērs.returncode==0:
                    후보=Meklēt_mērs.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Svarīgie=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Svarīgie.returncode==0:Logs=후보;break
                time.sleep(.1)
            assert Logs,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Logs,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Teksts):가상입력도구('type','--clearmodifiers','--delay','50',Teksts)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Nobīde_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Nobīde_VALUE)
            Nobīde_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Nobīde_VALUE)
            Nobīde_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nulle_operands Atslēga_VALUE, Shift+Space 또는 F9'.encode(),Nobīde_VALUE);기다리기(b'jkoros-native> ',Nobīde_VALUE)
            Nobīde_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Nobīde_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Logs,str(mērs_dati/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Nobīde_VALUE)
            # faktisks_dati Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            zīmējums_VALUE=Image.open(str(mērs_dati/'remmina-korean.png')).convert('RGB')
            virsrakstjosla=None
            for vertikāle_amats in range(zīmējums_VALUE.height):
                가로들=[가로 for 가로 in range(zīmējums_VALUE.width) if zīmējums_VALUE.getpixel((가로,vertikāle_amats))==(32,80,144)]
                if len(가로들)>=500:virsrakstjosla=(min(가로들),vertikāle_amats);break
            assert virsrakstjosla,'native terminal title bar not found'
            가로,vertikāle_amats=virsrakstjosla[0]+564,virsrakstjosla[1]+356
            가상입력도구('mousemove','--window',Logs,str(가로),str(vertikāle_amats))
            def 화상기다리기(Nosaukums,점들):
                izpildes_termiņš_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Logs,str(mērs_dati/Nosaukums)])
                    bitkarte_IMAGE=Image.open(str(mērs_dati/Nosaukums)).convert('RGB')
                    if all(bitkarte_IMAGE.getpixel(Novietojums)==빛 for Novietojums,빛 in 점들):return
                    assert time.monotonic()<izpildes_termiņš_VALUE,'Remmina framebuffer did not settle: '+Nosaukums
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,vertikāle_amats-7),(255,255,255)),((가로+7,vertikāle_amats+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Logs,str(가로-120),str(vertikāle_amats-80),'mouseup','1')
            time.sleep(.4)
            Nobīde_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Nobīde_VALUE)
            가상입력도구('mousemove','--window',Logs,'500','45')
            화상기다리기('remmina-resized.png',[
                ((virsrakstjosla[0]+447,virsrakstjosla[1]+279),(39,49,64)),((가로,vertikāle_amats),(24,32,48))])
            if shutil.which('dpkg-query'):
                versijas_numurs=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versijas_numurs=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validācija_ziņot.update(passed=True,display=환경['DISPLAY'],remmina_version=versijas_numurs,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validācija_ziņot['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(mērs_dati/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for dati_amats in reversed(실행과정들):
                if dati_amats.poll() is None:
                    if dati_amats.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(dati_amats.pid,signal.SIGTERM)
                    else:dati_amats.terminate()
                    try:dati_amats.wait(timeout=5)
                    except subprocess.TimeoutExpired:dati_amats.kill();dati_amats.wait()
            atlasītājs.close()
            for Fails_ievade in 기록들:Fails_ievade.close()
            (mērs_dati/'serial.log').write_bytes(직렬입출력)
            (mērs_dati/'report.json').write_text(json.dumps(validācija_ziņot,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Palaist()
