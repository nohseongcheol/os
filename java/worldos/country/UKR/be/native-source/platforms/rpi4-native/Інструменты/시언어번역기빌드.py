"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(기준경로, рэпазіторый_шлях, 시언어번역기, 연결편집기, канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў, выканаць_каманда):
    결과자료 = 기준경로 / 'build/ccompiler'; 결과자료.mkdir(exist_ok=True)
    원본자료 = 기준경로 / '시언어번역기'
    вышэйстаячы = 기준경로 / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = 기준경로 / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў = [Налады_значэнне for Налады_значэнне in канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў if Налады_значэнне != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', вышэйстаячы, '-I', 기준경로/'карыстальнік', '-I', 결과자료, '-isystem', 개발꾸러미/'usr/include']
    выканаць_каманда([시언어번역기]+канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'запуск_апора.c','-o',결과자료/'crt.o'])
    выканаць_каманда([시언어번역기]+канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў+['-I',рэпазіторый_шлях/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',결과자료/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((рэпазіторый_шлях/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((вышэйстаячы/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',기준경로/'build/user/start.o'),('/sdk/lib/crt.o',결과자료/'crt.o'),('/sdk/lib/aot-runtime.o',결과자료/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',기준경로/'build/libposix-kor-user.a')]
    Загаловак_значэнне=['typedef struct { const char *Назва; const unsigned char *дадзеныя; unsigned Памер; } 번역기자원;']
    for 순번,(_,ШЛЯХ) in enumerate(탑재자료):
        Загаловак_значэнне.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ШЛЯХ.read_bytes())))
    Загаловак_значэнне.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Назва,ШЛЯХ) in enumerate(탑재자료): Загаловак_значэнне.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Назва,ensure_ascii=False),순번,ШЛЯХ.stat().st_size))
    Загаловак_значэнне.append('};');(결과자료/'resources.h').write_text('\n'.join(Загаловак_значэнне)+'\n',encoding='utf-8')
    прызначэнне_Файлы=[]
    for Назва in ('번역기.c','агульнамоўная_серада_выканання_апора.c','Выканаць.c','미리번역.c','되돌림.S'):
        канчатковы_файл=결과자료/(Path(Назва).stem+'.o');прызначэнне_Файлы.append(канчатковы_файл)
        выканаць_каманда([시언어번역기]+канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Назва,'-o',канчатковы_файл])
    실행파일=기준경로/'build/user/cc.elf'
    выканаць_каманда([연결편집기,'--gc-sections','-T',기준경로/'карыстальнік/сувязь_Макет.ld','-z','max-page-size=4096','-o',실행파일,
         기준경로/'build/user/start.o',기준경로/'build/user/runtime.o']+прызначэнне_Файлы+
         [기준경로/'build/user'/Назва for Назва in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
