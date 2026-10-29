#!/usr/bin/env python3
"""Self-contained edition builder and launcher. Copied into every edition."""
import argparse
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from archive import cpio, directory_entries
from ip_config import read_config, qemu_network

def build(root):
    info=json.loads((root/'edition.json').read_text(encoding='utf-8'))
    output=root/'build';output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='classes-',dir=str(output)) as temporary:
        classes=Path(temporary)
        subprocess.run(['javac','--release','11','-encoding','UTF-8','-d',str(classes)]+[str(root/x) for x in info['sources']],check=True)
        shutil.copy2(str(root/info['messages']),str(classes/'messages.properties'))
        subprocess.run(['jar','cfe',str(output/'edition.jar.next'),info['main'],'-C',str(classes),'.'],check=True)
        (output/'edition.jar.next').replace(output/'edition.jar')
    return output/'edition.jar'

def runtime_path(root, explicit=None):
    choices=[Path(explicit)] if explicit else [root/'runtime']+[x/'build/runtime' for x in root.parents]
    for candidate in choices:
        if (candidate/'manifest.json').exists():return candidate.resolve()
    raise SystemExit('Runtime missing: run make runtime at java/worldos, or specify --runtime')

def prepare(root,runtime,tests=None):
    info=json.loads((root/'edition.json').read_text(encoding='utf-8'))
    jar=root/'build/edition.jar'
    if not jar.exists() or any((root/p).stat().st_mtime > jar.stat().st_mtime for p in info['sources']+[info['messages']]):jar=build(root)
    stage=Path(tempfile.mkdtemp(prefix='overlay-',dir=str(root/'build')))
    network = read_config(root)
    # Also refresh an existing runtime's old fixed-address init script.
    init = (runtime/'worldos-init').read_text(encoding='utf-8')
    init = init.replace("ip address add 10.0.2.15/24 dev eth0\nip route add default via 10.0.2.2\nprintf 'nameserver 10.0.2.3\\n' > /etc/resolv.conf",
                        '. /opt/worldos/ip.conf\nip address add "$IP/$PREFIX" dev eth0\nif [ "$GATEWAY" != 0.0.0.0 ]; then ip route add default via "$GATEWAY"; fi\nprintf \'nameserver %s\\n\' "$DNS" > /etc/resolv.conf')
    (stage/'worldos-init').write_text(init, encoding='utf-8')
    (stage/'ip.conf').write_text(''.join(key+'='+network[key]+'\n' for key in ('IP','NETMASK','GATEWAY','DNS'))+'PREFIX='+str(network['prefix'])+'\n')
    (stage/'worldos-init').chmod(0o755)
    shutil.copy2(str(runtime/'input-session.sh'),str(stage/'input-session.sh'))
    shutil.copy2(str(jar),str(stage/'edition.jar'))
    for example in (root/info['examples']).rglob('*'):
        if example.is_file():
            destination=stage/'examples'/example.relative_to(root/info['examples'])
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(str(example),str(destination))
    shutil.copy2(str(root/info['posix']),str(stage/'posix.h'))
    (stage/'identity').write_text(info['country']+'/'+info['language']+'\n',encoding='utf-8')
    if 'identifiers' in info:
        names=info['identifiers']
        local_c='#include <errno.h>\n#include <string.h>\n#include <stdio.h>\n#include "/opt/worldos/posix.h"\nint main(void) { int fd='+names['open']+'("/home/user/workspace/local-posix.txt",O_CREAT|O_RDWR|O_TRUNC,0600); char data[4]={0}; if(fd<0 || '+names['write']+'(fd,"ok",2)!=2 || '+names['sync']+'(fd) || '+names['seek']+'(fd,0,SEEK_SET)<0 || '+names['read']+'(fd,data,2)!=2 || strcmp(data,"ok") || '+names['close']+'(fd)) return 1; puts("PASS localized-posix-names"); return 0; }\n'
        (stage/'posix-local-test.c').write_text(local_c,encoding='utf-8')
    engine=info.get('input_method',{}).get('engine','keyboard-us')
    profile='[Groups/0]\nName=Default\nDefault Layout=us\nDefaultIM='+engine+'\n\n[Groups/0/Items/0]\nName=keyboard-us\nLayout=\n'
    if engine!='keyboard-us':profile+='\n[Groups/0/Items/1]\nName='+engine+'\nLayout=\n'
    profile+='\n[GroupOrder]\n0=Default\n'
    (stage/'fcitx-profile').write_text(profile)
    session='#!/bin/sh\nexport JAVA_HOME=/usr/lib/jvm/java-25-openjdk\nexport PATH=$JAVA_HOME/bin:/usr/bin:/bin:/usr/sbin:/sbin\n. /opt/worldos/input-session.sh\nopenbox >/tmp/openbox.log 2>&1 &\nexec java -Dworldos.locale='+info['language'].replace('_','-')+' -jar /opt/worldos/edition.jar\n'
    (stage/'session.sh').write_text(session);(stage/'session.sh').chmod(0o755)
    if tests:
        for source in Path(tests).iterdir():
            if source.is_file():shutil.copy2(str(source),str(stage/source.name))
    entries=[('edition',stat.S_IFDIR|0o755,b'',0,0)]
    entries += [('edition/'+n,m,d,a,b) for n,m,d,a,b in directory_entries(stage)]
    overlay=root/'build/edition.cpio';cpio(entries,overlay)
    shutil.rmtree(str(stage))
    initrd=root/'build/initrd.img'
    with initrd.open('wb') as target:
        with (runtime/'base.cpio.gz').open('rb') as source:shutil.copyfileobj(source,target)
        with gzip.GzipFile(fileobj=target,mode='wb',mtime=0) as compressed:
            with overlay.open('rb') as source:shutil.copyfileobj(source,compressed)
    return initrd

def run(root,args):
    runtime=runtime_path(root,args.runtime);initrd=prepare(root,runtime,args.tests)
    disk=Path(args.disk).resolve() if args.disk else root/'build/data.ext4'
    disk.parent.mkdir(parents=True,exist_ok=True)
    with (Path(str(disk)+'.lock')).open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('This edition data disk is already in use')
        if not disk.exists():
            with disk.open('wb') as stream:stream.truncate(2*1024**3)
            subprocess.run(['mke2fs','-q','-F','-t','ext4',str(disk)],check=True)
        acceleration=args.accel
        if acceleration=='auto':acceleration='kvm' if os.access('/dev/kvm',os.R_OK|os.W_OK) else 'tcg'
        command=['qemu-system-x86_64','-machine','q35,accel='+acceleration,'-m',str(args.memory),'-smp','2','-kernel',str(runtime/'vmlinuz'),'-initrd',str(initrd),
          '-append','console=tty0 console=ttyS0 rdinit=/init quiet'+(' worldos.test='+args.test_mode if args.tests else ''),
          '-drive','file='+str(runtime/'rootfs.squashfs')+',format=raw,if=virtio,readonly=on',
          '-drive','file='+str(disk)+',format=raw,if=virtio','-netdev','user,id=network,'+qemu_network(read_config(root)),'-device','virtio-net-pci,netdev=network',
          '-device','virtio-vga','-device','virtio-rng-pci','-no-reboot','-serial',('file:'+str(root/'build/serial.log') if args.tests else 'mon:stdio')]
        if args.headless:command+=['-display','none']
        if args.qmp:command+=['-qmp','unix:'+str(Path(args.qmp).resolve())+',server,nowait']
        print('WorldOS '+str(root)+'; serial log: '+str(root/'build/serial.log'),flush=True)
        try:return subprocess.call(command,timeout=args.timeout)
        except subprocess.TimeoutExpired:raise SystemExit('Guest exceeded timeout; inspect build/serial.log')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['build','run'])
    parser.add_argument('--root',default=str(Path(__file__).resolve().parent))
    parser.add_argument('--runtime');parser.add_argument('--disk');parser.add_argument('--headless',action='store_true')
    parser.add_argument('--tests');parser.add_argument('--test-mode',default='full');parser.add_argument('--qmp')
    parser.add_argument('--timeout',type=int,default=None);parser.add_argument('--memory',type=int,default=2048)
    parser.add_argument('--accel',choices=['auto','kvm','tcg'],default='auto')
    args=parser.parse_args();root=Path(args.root).resolve()
    if args.command=='build':build(root)
    else:sys.exit(run(root,args))
if __name__=='__main__':main()
