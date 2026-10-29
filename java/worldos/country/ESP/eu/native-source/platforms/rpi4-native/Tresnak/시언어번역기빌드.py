"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(erro_bide_izen, biltegi_bide_izen, 시언어번역기, 연결편집기, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, exekutatu_komando):
    neurria_datuak = erro_bide_izen / 'build/ccompiler'; neurria_datuak.mkdir(exist_ok=True)
    원본자료 = erro_bide_izen / '시언어번역기'
    goranzko = erro_bide_izen / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = erro_bide_izen / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna = [Ezarpenak_balio for Ezarpenak_balio in konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna if Ezarpenak_balio != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', goranzko, '-I', erro_bide_izen/'erabiltzaile', '-I', neurria_datuak, '-isystem', 개발꾸러미/'usr/include']
    exekutatu_komando([시언어번역기]+konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'abio_Laguntza.c','-o',neurria_datuak/'crt.o'])
    exekutatu_komando([시언어번역기]+konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna+['-I',biltegi_bide_izen/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',neurria_datuak/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+datuak_kargu.name,datuak_kargu) for datuak_kargu in sorted((biltegi_bide_izen/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+datuak_kargu.name,datuak_kargu) for datuak_kargu in sorted((goranzko/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+datuak_kargu.name,datuak_kargu) for datuak_kargu in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',erro_bide_izen/'build/user/start.o'),('/sdk/lib/crt.o',neurria_datuak/'crt.o'),('/sdk/lib/aot-runtime.o',neurria_datuak/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',erro_bide_izen/'build/libposix-kor-user.a')]
    goiburu_balio=['typedef struct { const char *Izena; const unsigned char *datuak; unsigned Tamaina; } 번역기자원;']
    for 순번,(_,Bide_izena) in enumerate(탑재자료):
        goiburu_balio.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Bide_izena.read_bytes())))
    goiburu_balio.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Izena,Bide_izena) in enumerate(탑재자료): goiburu_balio.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Izena,ensure_ascii=False),순번,Bide_izena.stat().st_size))
    goiburu_balio.append('};');(neurria_datuak/'resources.h').write_text('\n'.join(goiburu_balio)+'\n',encoding='utf-8')
    helburu_Fitxategiak=[]
    for Izena in ('번역기.c','실행지원.c','Exekutatu_2.c','미리번역.c','itzuli_zubi.S'):
        helburuko_fitxategi=neurria_datuak/(Path(Izena).stem+'.o');helburu_Fitxategiak.append(helburuko_fitxategi)
        exekutatu_komando([시언어번역기]+konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Izena,'-o',helburuko_fitxategi])
    실행파일=erro_bide_izen/'build/user/cc.elf'
    exekutatu_komando([연결편집기,'--gc-sections','-T',erro_bide_izen/'erabiltzaile/lotu_diseinu.ld','-z','max-page-size=4096','-o',실행파일,
         erro_bide_izen/'build/user/start.o',erro_bide_izen/'build/user/runtime.o']+helburu_Fitxategiak+
         [erro_bide_izen/'build/user'/Izena for Izena in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
