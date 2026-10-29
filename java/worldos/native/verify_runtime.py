#!/usr/bin/env python3
"""Exercise the country's actual kernel through VNC, its shell, and vi."""
import argparse
import ftplib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import selectors
import signal
import socket
import socketserver
import struct
import subprocess
import time
import threading
import zipfile
from PIL import Image
from source_names import make_renamer
from verify_country_boots import source_digest, launcher_digest

ROOT=Path(__file__).resolve().parents[1]


def exact(sock,count):
    result=bytearray()
    while len(result)<count:
        part=sock.recv(count-len(result))
        if not part:raise EOFError()
        result.extend(part)
    return bytes(result)


def verify(folder,network=False,label=None,network_host='127.0.0.1'):
    folder=folder.resolve(); config=json.loads((folder/'native.json').read_text())
    source_hash=source_digest(folder, config)
    launch_hash=launcher_digest(folder, config)
    local_log=make_renamer(config['identifiers'])
    native=folder/config['source']/config['native']
    output=ROOT/'build/native/verification'/(label or config['country']);output.mkdir(parents=True,exist_ok=True)
    servers=[];ftp=None;packets=[];extra=[]
    if network:
        class Stream(socketserver.BaseRequestHandler):
            def handle(self):
                data=bytearray();self.request.settimeout(10)
                while b'\n' not in data and len(data)<4096:
                    part=self.request.recv(4096)
                    if not part:return
                    data.extend(part)
                packets.append(('tcp',bytes(data)));self.request.sendall(data)
        class Datagram(socketserver.BaseRequestHandler):
            def handle(self):
                data,sock=self.request;packets.append(('udp',data));sock.sendto(data,self.client_address)
        for kind,handler in [(socketserver.ThreadingTCPServer,Stream),(socketserver.ThreadingUDPServer,Datagram)]:
            while True:
                server=kind(('127.0.0.1',0),handler)
                if not 50000<=server.server_address[1]<=50007:break
                server.server_close()
            server.daemon_threads=True
            threading.Thread(target=server.serve_forever,kwargs={'poll_interval':.1},daemon=True).start();servers.append(server)
        tcp_port,udp_port=[server.server_address[1] for server in servers]
        while True:
            with socket.socket() as probe:
                probe.bind(('127.0.0.1',0));ftp_port=probe.getsockname()[1]
            if not 50000<=ftp_port<=50007:break
        extra=['--network','--ftp-port',str(ftp_port),'--network-host',network_host]
    process=subprocess.Popen(['sh',str(folder/'native-launch.sh'),'desktop','--port','0','--resolution','960x540']+extra,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
    selector=selectors.DefaultSelector();selector.register(process.stdout,selectors.EVENT_READ)
    transcript=bytearray(); client=None
    report={'passed':False,'country':config['country'],'language':config['language'],'linux_loaded':False,
            'source_sha256':source_hash,'launcher_sha256':launch_hash,'complete_localization_certified':False}
    if network:report['host_ports']={'tcp':tcp_port,'udp':udp_port,'ftp':ftp_port}
    def until(marker,offset=0,timeout=90):
        deadline=time.monotonic()+timeout
        while marker not in transcript[offset:]:
            if time.monotonic()>deadline or process.poll() is not None:
                raise AssertionError('Missing '+repr(marker)+'\n'+transcript[max(0,offset-100):].decode('utf-8','replace'))
            for key,_ in selector.select(.1):
                part=key.fileobj.read(65536)
                if part:transcript.extend(part)
        return transcript[offset:].decode('utf-8','replace')
    def key(symbol,down=True):client.sendall(struct.pack('>BBHI',4,int(down),0,symbol))
    def tap(symbol):key(symbol);key(symbol,False)
    def type_text(text):
        for char in text:tap(0xff0d if char=='\n' else ord(char) if ord(char)<256 else 0x1000000|ord(char))
    sequence=[0]
    def shell(command):
        sequence[0]+=1;marker='__WORLDOS_DONE_'+str(sequence[0])+'__'
        print(config['country'],command,flush=True)
        offset=len(transcript);type_text(command+'; echo; echo '+marker+'\n')
        return until(('\r\n'+marker+'\r\njkoros-native> ').encode(),offset)
    def pixels(name):
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,960,540));rgb=bytearray(960*540*3)
        while True:
            kind=exact(client,1)[0]
            if kind==2:continue
            if kind==3:exact(client,struct.unpack('>I',exact(client,7)[3:])[0]);continue
            assert kind==0,kind
            count=struct.unpack('>H',exact(client,3)[1:])[0]
            for _ in range(count):
                x,y,width,height,encoding=struct.unpack('>HHHHi',exact(client,12));assert encoding==0
                data=exact(client,width*height*4)
                image=Image.frombytes('RGB',(width,height),data,'raw','BGRX')
                for row in range(height):
                    at=((y+row)*960+x)*3
                    rgb[at:at+width*3]=image.crop((0,row,width,row+1)).tobytes()
            if count:break
        Image.frombytes('RGB',(960,540),bytes(rgb)).save(str(output/name))
    try:
        # A relocated, source-only edition builds all guest runtimes first.
        until(b'TERMINAL READY',timeout=600);until(b'jkoros-native> ',transcript.rfind(b'TERMINAL READY'))
        # native-edition may rebuild before boot. Bind evidence to that image,
        # not an older artifact sampled immediately after starting the runner.
        report['kernel_sha256']=hashlib.sha256((native/'build/kernel8.img').read_bytes()).hexdigest()
        assert source_digest(folder, config)==source_hash, 'Source changed during build'
        port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcript).group(1))
        client=socket.create_connection(('127.0.0.1',port),timeout=20)
        assert exact(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        count=exact(client,1)[0];assert 1 in exact(client,count);client.sendall(b'\x01');assert exact(client,4)==b'\0'*4
        client.sendall(b'\x01');init=exact(client,24);exact(client,struct.unpack('>I',init[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        help_output=shell('help input');assert config['help'] in help_output,help_output
        p=config['input']
        for shift in (False,True):
            offset=len(transcript);type_text('echo ')
            if shift:key(0xffe1);tap(32);key(0xffe1,False)
            else:tap(0xffc6)
            type_text(p['sample_keys']);tap(0xffc6);type_text('\n')
            until(('\r\n'+p['sample']+'\r\n').encode(),offset);until(b'jkoros-native> ',offset)
        report['f9_and_shift_space']=True
        offset=len(transcript);type_text('vi native-input.txt\n');until(b'NORMAL',offset)
        type_text('i');tap(0xffc6);type_text(p['sample_keys']);tap(0xffc6)
        # Wait for the inserted text before asking QEMU for its real framebuffer.
        until(p['sample'].encode(),offset);pixels('vi-input.png')
        tap(0xff1b);type_text(':wq\n');until(b'jkoros-native> ',offset)
        saved=shell('cat native-input.txt');assert p['sample'] in saved,saved
        report['vi_utf8_saved']=True
        shell('example java');shell('cd /example/java')
        name=config['examples']['출력예제']
        compiled=shell('javac '+name+'.java');assert 'exit 0' in compiled,compiled
        ran=shell('java '+name);assert '42' in ran and 'exit 0' in ran,ran
        report['guest_javac_java']=True
        file_name=config['examples']['파일예제'];net_name=config['examples']['네트워크예제']
        ran=shell('java '+file_name);assert 'exit 0' in ran,ran
        if network:
            ran=shell('java '+net_name+' '+str(tcp_port)+' '+str(udp_port));assert 'exit 0' in ran,ran
        offset=len(transcript);type_text('vi '+name+'.java\n');until(b'NORMAL',offset)
        pixels('vi-source.png');tap(0xff1b);type_text(':q\n');until(b'jkoros-native> ',offset)
        report['localized_source_in_vi']=name+'.java'
        offset=len(transcript);type_text('java '+config['examples']['창예제']+'\n')
        until((local_log('GUI 예제 준비: ')+config['examples']['창예제']).encode(),offset)
        def click(x,y):
            client.sendall(struct.pack('>BBHH',5,1,x,y));client.sendall(struct.pack('>BBHH',5,0,x,y))
        offset=len(transcript);click(300,270);until(local_log('GUI 인사:').encode(),offset)
        pixels('window-example.png');offset=len(transcript);click(690,133);until(b'jkoros-native> ',offset)
        report['localized_gui_callback']=True
        shell('cd /');shell('example python');shell('cd /example/python')
        ran=shell('python '+name+'.py');assert '42' in ran and 'exit 0' in ran,ran
        report['guest_python']=True
        ran=shell('python '+file_name+'.py');assert 'exit 0' in ran,ran
        if network:
            ran=shell('python '+net_name+'.py '+str(udp_port));assert 'exit 0' in ran,ran
        shell('cd /');shell('example c');shell('cd /example/c')
        compiled=shell('cc '+name+'.c -o demo');assert 'exit 0' in compiled,compiled
        ran=shell('./demo');assert 'exit 0' in ran,ran
        report['guest_c']=True
        compiled=shell('cc '+file_name+'.c -o file-demo');assert 'exit 0' in compiled,compiled
        ran=shell('./file-demo');assert 'exit 0' in ran,ran
        report['java_c_python_file_io']=True
        if network:
            compiled=shell('cc '+net_name+'.c -o network-demo');assert 'exit 0' in compiled,compiled
            ran=shell('./network-demo '+str(udp_port));assert 'exit 0' in ran,ran
            assert any(kind=='tcp' and b'JAVA' in data for kind,data in packets),packets
            for language in (b'JAVA',b'PYTHON',b'C '):
                assert any(kind=='udp' and data.startswith(language) for kind,data in packets),packets
            report['java_tcp_udp_python_c_udp']=True
            shell('cd /');started=shell('ftpd start');assert 'FTP listening' in started,started
            ftp=ftplib.FTP();ftp.encoding='utf-8';ftp.connect(network_host,ftp_port,timeout=20);ftp.login()
            jar=io.BytesIO()
            # The current FTP service deliberately exposes flat root names.
            # Copy the current guest compiler output there before downloading.
            copied=shell('cp /example/java/'+name+'.class /'+name+'.class')
            assert 'error' not in copied.lower(), copied
            guest_class=bytearray()
            ftp.retrbinary('RETR '+name+'.class',guest_class.extend)
            assert guest_class.startswith(b'\xca\xfe\xba\xbe'), 'Missing guest-compiled class'
            report['ftp_jar_uses_guest_compiled_class']=True
            with zipfile.ZipFile(jar,'w',compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr('META-INF/MANIFEST.MF','Manifest-Version: 1.0\r\nMain-Class: '+name+'\r\n\r\n')
                archive.writestr(name+'.class',bytes(guest_class))
            jar_name=name+'.jar';jar.seek(0);ftp.storbinary('STOR '+jar_name,jar)
            received=bytearray();ftp.retrbinary('RETR '+jar_name,received.extend);assert received==jar.getvalue()
            for command in ('java -jar '+jar_name,'./'+jar_name):
                ran=shell(command);assert 'exit 0' in ran and '42' in ran,ran
            ftp.delete(jar_name);ftp.delete(name+'.class');report['ftp_localized_jar_upload_execute']=True
            report['network_packets']=[{'protocol':kind,'text':data.decode('utf-8')} for kind,data in packets]
        assert source_digest(folder, config)==source_hash, 'Source changed during guest probes'
        assert launcher_digest(folder, config)==launch_hash, 'Launcher changed during guest probes'
        report['passed']=True
    except Exception as error:
        report['error']=str(error)
        raise
    finally:
        report['network_packets']=[{'protocol':kind,'text':data.decode('utf-8','replace')} for kind,data in packets]
        if ftp:ftp.close()
        if client:client.close()
        if process.poll() is None:os.killpg(process.pid,signal.SIGTERM)
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
        selector.close()
        for server in servers:server.shutdown();server.server_close()
        (output/'serial.log').write_bytes(transcript)
        (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('countries',nargs='+');parser.add_argument('--network',action='store_true');parser.add_argument('--label');parser.add_argument('--network-host',default='127.0.0.1');args=parser.parse_args()
    if args.label and len(args.countries)!=1:parser.error('--label requires one country')
    for value in args.countries:
        verify(Path(value) if '/' in value else ROOT/'country'/value,args.network,args.label,args.network_host)
