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
from exekutatu_komando import Project_erro


def Exekutatu_2():
    neurria_datuak=Project_erro/'build/verification/remmina';neurria_datuak.mkdir(parents=True,exist_ok=True)
    balidazio_txosten={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];준비선택기=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            birtual_pantaila=shutil.which('Xvfb')
            if birtual_pantaila: zerbitzari_balio=[birtual_pantaila]
            else:
                뿌리파일계층=Project_erro.parent/'rpi4/build/rootfs'
                zerbitzari_balio=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Exekutatu_2(arg_matrize,환경=None,**이름붙인인수):
                LOG_marka=(neurria_datuak/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_marka)
                datuak_kargu=subprocess.Popen(arg_matrize,env=환경,stdout=LOG_marka,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(datuak_kargu);return datuak_kargu
            환경=dict(os.environ)
            for Izena in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Izena,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(elementu_ZENBATU for elementu_ZENBATU in range(80,200) if not Path('/tmp/.X11-unix/X'+str(elementu_ZENBATU)).exists() and not Path('/tmp/.X%d-lock'%elementu_ZENBATU).exists())
            환경['DISPLAY']=':'+str(수치)
            pantaila=Exekutatu_2(zerbitzari_balio+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert pantaila.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            gonbidatu=subprocess.Popen(['python3',str(Project_erro/'Tresnak/exekutatu_komando.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(gonbidatu);준비선택기.register(gonbidatu.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,Geruzak_balio=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[Geruzak_balio:]:
                    assert gonbidatu.poll() is None and time.monotonic()<마감시각,직렬입출력[Geruzak_balio:].decode('utf-8','replace')
                    for 누름값,_ in 준비선택기.select(.1):
                        datuak=누름값.fileobj.read(65536)
                        if datuak:직렬입출력.extend(datuak)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            ataka_zenbaki=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            profil=작업경로/'test.remmina'
            profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%ataka_zenbaki)
            Exekutatu_2(['dbus-run-session','--','remmina','-c',str(profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*arg_matrize):return subprocess.check_output(['xdotool']+list(arg_matrize),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Leihoa=None
            while time.monotonic()<마감시각:
                BILATU_neurria=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if BILATU_neurria.returncode==0:
                    후보=BILATU_neurria.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Lehentasunezkoak=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Lehentasunezkoak.returncode==0:Leihoa=후보;break
                time.sleep(.1)
            assert Leihoa,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Leihoa,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Testua):가상입력도구('type','--clearmodifiers','--delay','50',Testua)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Geruzak_balio=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Geruzak_balio)
            Geruzak_balio=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Geruzak_balio)
            Geruzak_balio=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 gako_balio, Shift+Space 또는 F9'.encode(),Geruzak_balio);기다리기(b'jkoros-native> ',Geruzak_balio)
            Geruzak_balio=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Geruzak_balio)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Leihoa,str(neurria_datuak/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Geruzak_balio)
            # benetako_datuak Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            그림=Image.open(str(neurria_datuak/'remmina-korean.png')).convert('RGB')
            titulu_barra=None
            for Bertikala_kargu in range(그림.height):
                가로들=[가로 for 가로 in range(그림.width) if 그림.getpixel((가로,Bertikala_kargu))==(32,80,144)]
                if len(가로들)>=500:titulu_barra=(min(가로들),Bertikala_kargu);break
            assert titulu_barra,'native terminal title bar not found'
            가로,Bertikala_kargu=titulu_barra[0]+564,titulu_barra[1]+356
            가상입력도구('mousemove','--window',Leihoa,str(가로),str(Bertikala_kargu))
            def 화상기다리기(Izena,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Leihoa,str(neurria_datuak/Izena)])
                    bit_mapa_irudi=Image.open(str(neurria_datuak/Izena)).convert('RGB')
                    if all(bit_mapa_irudi.getpixel(Posizioa)==빛 for Posizioa,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Izena
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Bertikala_kargu-7),(255,255,255)),((가로+7,Bertikala_kargu+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Leihoa,str(가로-120),str(Bertikala_kargu-80),'mouseup','1')
            time.sleep(.4)
            Geruzak_balio=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Geruzak_balio)
            가상입력도구('mousemove','--window',Leihoa,'500','45')
            화상기다리기('remmina-resized.png',[
                ((titulu_barra[0]+447,titulu_barra[1]+279),(39,49,64)),((가로,Bertikala_kargu),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            balidazio_txosten.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not balidazio_txosten['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(neurria_datuak/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for datuak_kargu in reversed(실행과정들):
                if datuak_kargu.poll() is None:
                    if datuak_kargu.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(datuak_kargu.pid,signal.SIGTERM)
                    else:datuak_kargu.terminate()
                    try:datuak_kargu.wait(timeout=5)
                    except subprocess.TimeoutExpired:datuak_kargu.kill();datuak_kargu.wait()
            준비선택기.close()
            for fitxategi_sarrera in 기록들:fitxategi_sarrera.close()
            (neurria_datuak/'serial.log').write_bytes(직렬입출력)
            (neurria_datuak/'report.json').write_text(json.dumps(balidazio_txosten,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Exekutatu_2()
