#!/usr/bin/env python3
import argparse
import http.server
import json
import os
import signal
from pathlib import Path
import shutil
import ssl
import subprocess
import threading
import time
import uuid
ROOT=Path(__file__).resolve().parents[1]
from ip_config import read_config
class Handler(http.server.BaseHTTPRequestHandler):
    token=b''
    def do_GET(self):
        self.send_response(200);self.send_header('Content-Length',str(len(self.token)));self.end_headers();self.wfile.write(self.token)
    def log_message(self,*args):pass

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--edition',default='KOR/ko');parser.add_argument('--reboots',type=int,default=2);parser.add_argument('--gui',action='store_true');parser.add_argument('--timeout',type=int,default=600)
    parser.add_argument('--focus',choices=['all','input','desktop','workbench'],default='all')
    args=parser.parse_args();root=ROOT/'country'/args.edition
    gateway=read_config(root)['GATEWAY']
    output=ROOT/'build/verification'/(args.edition.replace('/','-')+'-'+time.strftime('%Y%m%d-%H%M%S'));output.mkdir(parents=True)
    tests=output/'payload';shutil.copytree(str(ROOT/'tests'),str(tests))
    if args.focus=='workbench':
        (tests/'run-user-tests.sh').write_text('#!/bin/sh\nset -eu\n. /opt/worldos/input-session.sh\nopenbox >/home/user/workspace/openbox-test.log 2>&1 &\nsleep 2\njavac -encoding UTF-8 -d /home/user/workspace/test-classes /opt/worldos/WorkbenchFeatures.java\njava -cp /home/user/workspace/test-classes WorkbenchFeatures\necho WORLDOS_FEATURE_TESTS_OK\n')
        (tests/'run-user-tests.sh').chmod(0o755)
    if args.focus=='input':
        (tests/'run-user-tests.sh').write_text('#!/bin/sh\nset -eu\ntrap \'cp /tmp/fcitx.log /home/user/workspace/fcitx-test.log\' 0\n. /opt/worldos/input-session.sh\ncp /tmp/fcitx.log /home/user/workspace/fcitx-test.log\nopenbox >/home/user/workspace/openbox-test.log 2>&1 &\nsleep 5\ngdbus call --session --dest org.fcitx.Fcitx5 --object-path /controller --method org.fcitx.Fcitx.Controller1.AvailableInputMethods > /home/user/workspace/input-methods.txt\njavac -encoding UTF-8 -d /home/user/workspace/test-classes /opt/worldos/InputFeatures.java\njava -cp /home/user/workspace/test-classes InputFeatures\necho WORLDOS_FEATURE_TESTS_OK\n')
        (tests/'run-user-tests.sh').chmod(0o755)
    if args.focus=='desktop':
        script=(tests/'run-user-tests.sh').read_text()
        script='\n'.join(line for line in script.splitlines() if not any(name in line for name in ['JavaFeatures','NativeBridge','native_bridge.c','libworldos_jni.so']))+'\n'
        (tests/'run-user-tests.sh').write_text(script)
    # Only the public certificate enters the guest. HTTPS hostname verification remains enabled.
    key=output/'server.key';cert=tests/'server.crt';configuration=output/'openssl.cnf'
    configuration.write_text(('[req]\ndistinguished_name=dn\nx509_extensions=extensions\nprompt=no\n[dn]\nCN=10.0.2.2\n[extensions]\nsubjectAltName=IP:10.0.2.2\nbasicConstraints=CA:TRUE\nkeyUsage=digitalSignature,keyEncipherment,keyCertSign\n').replace('10.0.2.2',gateway))
    subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-days','2','-keyout',str(key),'-out',str(cert),'-config',str(configuration)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    token=uuid.uuid4().hex;Handler.token=token.encode();servers=[]
    for secure in [False,True]:
        server=http.server.HTTPServer(('127.0.0.1',0),Handler)
        if secure:
            context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);context.load_cert_chain(str(cert),str(key));server.socket=context.wrap_socket(server.socket,server_side=True)
        thread=threading.Thread(target=server.serve_forever);thread.daemon=True;thread.start();servers.append(server)
    (tests/'network.properties').write_text('http=http://'+gateway+':'+str(servers[0].server_port)+'/\nhttps=https://'+gateway+':'+str(servers[1].server_port)+'/\ntoken='+token+'\n')
    report={'edition':args.edition,'display':'Xorg' if args.gui else 'Xvfb','focus':args.focus,'boots':[]}
    try:
        for boot in range(args.reboots):
            command=['python3',str(root/'edition.py'),'run','--headless','--tests',str(tests),'--test-mode','gui' if args.gui else 'full','--disk',str(output/'data.ext4'),'--timeout',str(args.timeout)]
            serial=root/'build/serial.log'
            serial.write_text('')
            process=subprocess.Popen(command,start_new_session=True)
            deadline=time.monotonic()+args.timeout+30
            try:
                while process.poll() is None:
                    live=serial.read_text(errors='replace')
                    if 'Kernel panic' in live or "sh: can't access tty; job control turned off" in live or 'setsid: not found' in live or time.monotonic()>deadline:
                        os.killpg(process.pid,signal.SIGTERM)
                        break
                    time.sleep(0.5)
                process.wait(timeout=10)
            finally:
                if process.poll() is None:
                    os.killpg(process.pid,signal.SIGKILL)
                    process.wait()
            log=(root/'build/serial.log').read_text(errors='replace');(output/('boot-'+str(boot)+'.log')).write_text(log)
            with (output/('filesystem-'+str(boot)+'.log')).open('wb') as diagnostics:
                filesystem=subprocess.run(['e2fsck','-fn',str(output/'data.ext4')],stdout=diagnostics,stderr=subprocess.STDOUT)
            fslog=(output/('filesystem-'+str(boot)+'.log')).read_text(errors='replace')
            clean=filesystem.returncode==0 and 'skipping journal recovery' not in fslog and 'Fix? no' not in fslog
            passed=process.returncode==0 and clean and 'WORLDOS_FEATURE_TESTS_OK' in log and 'WORLDOS_TEST_EXIT=0' in log and 'WORLDOS_SHUTDOWN_CLEAN' in log
            if boot>0:passed=passed and 'PASS persistence-after-reboot' in log
            report['boots'].append({'index':boot,'passed':passed,'filesystem_clean':clean,'checks':[line.strip() for line in log.splitlines() if line.startswith('PASS ')]})
            print(json.dumps(report['boots'][-1],ensure_ascii=False),flush=True)
            if not passed:raise RuntimeError('Guest validation failed. See '+str(output/('boot-'+str(boot)+'.log')))
        for name in ['swing.png','workbench.png','input.png','input-methods.txt']:
            subprocess.run(['debugfs','-R','dump /root/home/user/workspace/'+name+' '+str(output/name),str(output/'data.ext4')],check=True,stdout=subprocess.DEVNULL)
    finally:
        for server in servers:server.shutdown();server.server_close()
        for guest,name in [('var/log/xorg.log','xorg.log'),('home/user/workspace/fcitx-test.log','fcitx.log'),('home/user/workspace/openbox-test.log','openbox.log'),('home/user/workspace/input.png','input.png'),('home/user/workspace/input-methods.txt','input-methods.txt')]:
            if (output/'data.ext4').exists():
                subprocess.run(['debugfs','-R','dump /root/'+guest+' '+str(output/name),str(output/'data.ext4')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print('Validation artifacts: '+str(output),flush=True)
if __name__=='__main__':main()
