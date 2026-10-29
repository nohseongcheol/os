"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(rel_camí, dipòsit_camí, 시언어번역기, 연결편집기, configuració_Servei_de_transferència_intel_ligent_en_segon_terme, Executa_ordre):
    mesura_dades = rel_camí / 'build/ccompiler'; mesura_dades.mkdir(exist_ok=True)
    원본자료 = rel_camí / '시언어번역기'
    superior = rel_camí / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = rel_camí / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    configuració_Servei_de_transferència_intel_ligent_en_segon_terme = [Configuració_VALOR for Configuració_VALOR in configuració_Servei_de_transferència_intel_ligent_en_segon_terme if Configuració_VALOR != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', superior, '-I', rel_camí/'usuari', '-I', mesura_dades, '-isystem', 개발꾸러미/'usr/include']
    Executa_ordre([시언어번역기]+configuració_Servei_de_transferència_intel_ligent_en_segon_terme+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'inici_suport.c','-o',mesura_dades/'crt.o'])
    Executa_ordre([시언어번역기]+configuració_Servei_de_transferència_intel_ligent_en_segon_terme+['-I',dipòsit_camí/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',mesura_dades/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+dades_càrrec.name,dades_càrrec) for dades_càrrec in sorted((dipòsit_camí/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dades_càrrec.name,dades_càrrec) for dades_càrrec in sorted((superior/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dades_càrrec.name,dades_càrrec) for dades_càrrec in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rel_camí/'build/user/start.o'),('/sdk/lib/crt.o',mesura_dades/'crt.o'),('/sdk/lib/aot-runtime.o',mesura_dades/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rel_camí/'build/libposix-kor-user.a')]
    Capçalera_VALOR=['typedef struct { const char *Nom; const unsigned char *dades; unsigned Mida; } 번역기자원;']
    for 순번,(_,Camí) in enumerate(탑재자료):
        Capçalera_VALOR.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Camí.read_bytes())))
    Capçalera_VALOR.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Nom,Camí) in enumerate(탑재자료): Capçalera_VALOR.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nom,ensure_ascii=False),순번,Camí.stat().st_size))
    Capçalera_VALOR.append('};');(mesura_dades/'resources.h').write_text('\n'.join(Capçalera_VALOR)+'\n',encoding='utf-8')
    destinació_Fitxers=[]
    for Nom in ('번역기.c','실행지원.c','Executa_2.c','미리번역.c','tornar_les_tasques_pont.S'):
        fitxer_de_destinació=mesura_dades/(Path(Nom).stem+'.o');destinació_Fitxers.append(fitxer_de_destinació)
        Executa_ordre([시언어번역기]+configuració_Servei_de_transferència_intel_ligent_en_segon_terme+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nom,'-o',fitxer_de_destinació])
    실행파일=rel_camí/'build/user/cc.elf'
    Executa_ordre([연결편집기,'--gc-sections','-T',rel_camí/'usuari/enllaç_disseny.ld','-z','max-page-size=4096','-o',실행파일,
         rel_camí/'build/user/start.o',rel_camí/'build/user/runtime.o']+destinació_Fitxers+
         [rel_camí/'build/user'/Nom for Nom in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
