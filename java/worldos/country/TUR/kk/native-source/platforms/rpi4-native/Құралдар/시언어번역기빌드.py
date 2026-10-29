"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(түбір_жол, репозиторий_жол, 시언어번역기, 연결편집기, конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі, орындау_пәрмен):
    өлшем_деректер = түбір_жол / 'build/ccompiler'; өлшем_деректер.mkdir(exist_ok=True)
    원본자료 = түбір_жол / '시언어번역기'
    жоғарғы = түбір_жол / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = түбір_жол / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі = [Параметрлер_мән for Параметрлер_мән in конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі if Параметрлер_мән != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', жоғарғы, '-I', түбір_жол/'пайдаланушы', '-I', өлшем_деректер, '-isystem', 개발꾸러미/'usr/include']
    орындау_пәрмен([시언어번역기]+конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'іске_қосу_тіреу.c','-o',өлшем_деректер/'crt.o'])
    орындау_пәрмен([시언어번역기]+конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі+['-I',репозиторий_жол/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',өлшем_деректер/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+деректер_лауазым.name,деректер_лауазым) for деректер_лауазым in sorted((репозиторий_жол/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+деректер_лауазым.name,деректер_лауазым) for деректер_лауазым in sorted((жоғарғы/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+деректер_лауазым.name,деректер_лауазым) for деректер_лауазым in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',түбір_жол/'build/user/start.o'),('/sdk/lib/crt.o',өлшем_деректер/'crt.o'),('/sdk/lib/aot-runtime.o',өлшем_деректер/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',түбір_жол/'build/libposix-kor-user.a')]
    Тақырып_мән=['typedef struct { const char *Аты; const unsigned char *деректер; unsigned Өлшемі; } 번역기자원;']
    for 순번,(_,Жол_2) in enumerate(탑재자료):
        Тақырып_мән.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Жол_2.read_bytes())))
    Тақырып_мән.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Аты,Жол_2) in enumerate(탑재자료): Тақырып_мән.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Аты,ensure_ascii=False),순번,Жол_2.stat().st_size))
    Тақырып_мән.append('};');(өлшем_деректер/'resources.h').write_text('\n'.join(Тақырып_мән)+'\n',encoding='utf-8')
    тағайындау_Файлдар=[]
    for Аты in ('번역기.c','CLR_ортасы_тіреу.c','Орындау_2.c','미리번역.c','қайтару_көпір.S'):
        тағайындалған_файл=өлшем_деректер/(Path(Аты).stem+'.o');тағайындау_Файлдар.append(тағайындалған_файл)
        орындау_пәрмен([시언어번역기]+конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Аты,'-o',тағайындалған_файл])
    실행파일=түбір_жол/'build/user/cc.elf'
    орындау_пәрмен([연결편집기,'--gc-sections','-T',түбір_жол/'пайдаланушы/Cілтеме_макет.ld','-z','max-page-size=4096','-o',실행파일,
         түбір_жол/'build/user/start.o',түбір_жол/'build/user/runtime.o']+тағайындау_Файлдар+
         [түбір_жол/'build/user'/Аты for Аты in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
