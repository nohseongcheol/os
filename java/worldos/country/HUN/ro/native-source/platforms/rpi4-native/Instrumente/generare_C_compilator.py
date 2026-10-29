"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def crea_C_compilator(rădăcină_cale, depozit_cale, C_compilator, 연결편집기, configurație_Serviciu_de_transfer_inteligent_în_fundal, executa_comandă):
    KR_date = rădăcină_cale / 'build/ccompiler'; KR_date.mkdir(exist_ok=True)
    원본자료 = rădăcină_cale / 'C_compilator'
    în_amonte = rădăcină_cale / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    kit_de_dezvoltare = rădăcină_cale / 'vendor/sdk'
    if not (kit_de_dezvoltare/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((kit_de_dezvoltare/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    configurație_Serviciu_de_transfer_inteligent_în_fundal = [Setări_VALUE for Setări_VALUE in configurație_Serviciu_de_transfer_inteligent_în_fundal if Setări_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', în_amonte, '-I', rădăcină_cale/'utilizator', '-I', KR_date, '-isystem', kit_de_dezvoltare/'usr/include']
    executa_comandă([C_compilator]+configurație_Serviciu_de_transfer_inteligent_în_fundal+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'boot_suport.c','-o',KR_date/'crt.o'])
    executa_comandă([C_compilator]+configurație_Serviciu_de_transfer_inteligent_în_fundal+['-I',depozit_cale/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',KR_date/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+date_poziție.name,date_poziție) for date_poziție in sorted((depozit_cale/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+date_poziție.name,date_poziție) for date_poziție in sorted((în_amonte/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+date_poziție.name,date_poziție) for date_poziție in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rădăcină_cale/'build/user/start.o'),('/sdk/lib/crt.o',KR_date/'crt.o'),('/sdk/lib/aot-runtime.o',KR_date/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rădăcină_cale/'build/libposix-kor-user.a')]
    Antet_VALUE=['typedef struct { const char *Nume; const unsigned char *date; unsigned Mărime; } compilator_resursă;']
    for 순번,(_,Cale) in enumerate(탑재자료):
        Antet_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Cale.read_bytes())))
    Antet_VALUE.append('static const compilator_resursă compilator_Resurse[] = {')
    for 순번,(Nume,Cale) in enumerate(탑재자료): Antet_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nume,ensure_ascii=False),순번,Cale.stat().st_size))
    Antet_VALUE.append('};');(KR_date/'resources.h').write_text('\n'.join(Antet_VALUE)+'\n',encoding='utf-8')
    destinație_Fișiere=[]
    for Nume in ('compilator_instrument.c','CLR_suport.c','Pornește.c','미리번역.c','restitui_punte.S'):
        fișier_destinație=KR_date/(Path(Nume).stem+'.o');destinație_Fișiere.append(fișier_destinație)
        executa_comandă([C_compilator]+configurație_Serviciu_de_transfer_inteligent_în_fundal+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nume,'-o',fișier_destinație])
    실행파일=rădăcină_cale/'build/user/cc.elf'
    executa_comandă([연결편집기,'--gc-sections','-T',rădăcină_cale/'utilizator/Link_Aspect.ld','-z','max-page-size=4096','-o',실행파일,
         rădăcină_cale/'build/user/start.o',rădăcină_cale/'build/user/runtime.o']+destinație_Fișiere+
         [rădăcină_cale/'build/user'/Nume for Nume in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
