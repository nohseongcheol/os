"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(Racinn_Wee, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ausféieren_Befeel):
    Mooss_Daten = Racinn_Wee / 'build/ccompiler'; Mooss_Daten.mkdir(exist_ok=True)
    원본자료 = Racinn_Wee / '시언어번역기'
    외부원문 = Racinn_Wee / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = Racinn_Wee / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Astellungen_VALUE for Astellungen_VALUE in 설정비트 if Astellungen_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', Racinn_Wee/'Benotzer', '-I', Mooss_Daten, '-isystem', 개발꾸러미/'usr/include']
    ausféieren_Befeel([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'Start_Support.c','-o',Mooss_Daten/'crt.o'])
    ausféieren_Befeel([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',Mooss_Daten/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+Daten_positionéieren.name,Daten_positionéieren) for Daten_positionéieren in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+Daten_positionéieren.name,Daten_positionéieren) for Daten_positionéieren in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+Daten_positionéieren.name,Daten_positionéieren) for Daten_positionéieren in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',Racinn_Wee/'build/user/start.o'),('/sdk/lib/crt.o',Mooss_Daten/'crt.o'),('/sdk/lib/aot-runtime.o',Mooss_Daten/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',Racinn_Wee/'build/libposix-kor-user.a')]
    En_tête_VALUE=['typedef struct { const char *Numm; const unsigned char *Daten; unsigned d_Gréisst_veränneren; } 번역기자원;']
    for 순번,(_,Wee) in enumerate(탑재자료):
        En_tête_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Wee.read_bytes())))
    En_tête_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Numm,Wee) in enumerate(탑재자료): En_tête_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Numm,ensure_ascii=False),순번,Wee.stat().st_size))
    En_tête_VALUE.append('};');(Mooss_Daten/'resources.h').write_text('\n'.join(En_tête_VALUE)+'\n',encoding='utf-8')
    Zil_Fichieren=[]
    for Numm in ('번역기.c','Common_Language_Runtime_Support.c','Laf.c','미리번역.c','되돌림.S'):
        Zilfichier=Mooss_Daten/(Path(Numm).stem+'.o');Zil_Fichieren.append(Zilfichier)
        ausféieren_Befeel([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Numm,'-o',Zilfichier])
    실행파일=Racinn_Wee/'build/user/cc.elf'
    ausféieren_Befeel([연결편집기,'--gc-sections','-T',Racinn_Wee/'Benotzer/Link_Layout.ld','-z','max-page-size=4096','-o',실행파일,
         Racinn_Wee/'build/user/start.o',Racinn_Wee/'build/user/runtime.o']+Zil_Fichieren+
         [Racinn_Wee/'build/user'/Numm for Numm in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
