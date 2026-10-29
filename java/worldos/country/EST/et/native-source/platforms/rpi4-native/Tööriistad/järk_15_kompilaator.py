"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def avama_15_kompilaator(juur_tee, hoidla_tee, _15_kompilaator, 연결편집기, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, Täida_käsk):
    näitaja_andmed = juur_tee / 'build/ccompiler'; näitaja_andmed.mkdir(exist_ok=True)
    원본자료 = juur_tee / '_15_kompilaator'
    ülesvoolu = juur_tee / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    arenduskomplekt = juur_tee / 'vendor/sdk'
    if not (arenduskomplekt/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((arenduskomplekt/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus = [Sätted_VALUE for Sätted_VALUE in konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus if Sätted_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', ülesvoolu, '-I', juur_tee/'kasutaja', '-I', näitaja_andmed, '-isystem', arenduskomplekt/'usr/include']
    Täida_käsk([_15_kompilaator]+konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'käivitus_tugi.c','-o',näitaja_andmed/'crt.o'])
    Täida_käsk([_15_kompilaator]+konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus+['-I',hoidla_tee/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',näitaja_andmed/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+andmed_ametikoht.name,andmed_ametikoht) for andmed_ametikoht in sorted((hoidla_tee/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+andmed_ametikoht.name,andmed_ametikoht) for andmed_ametikoht in sorted((ülesvoolu/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+andmed_ametikoht.name,andmed_ametikoht) for andmed_ametikoht in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',juur_tee/'build/user/start.o'),('/sdk/lib/crt.o',näitaja_andmed/'crt.o'),('/sdk/lib/aot-runtime.o',näitaja_andmed/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',juur_tee/'build/libposix-kor-user.a')]
    Päis_VALUE=['typedef struct { const char *Nimi_2; const unsigned char *andmed; unsigned Suurus; } kompilaator_ressurss;']
    for 순번,(_,RADA) in enumerate(탑재자료):
        Päis_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in RADA.read_bytes())))
    Päis_VALUE.append('static const kompilaator_ressurss kompilaator_Ressursid[] = {')
    for 순번,(Nimi_2,RADA) in enumerate(탑재자료): Päis_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nimi_2,ensure_ascii=False),순번,RADA.stat().st_size))
    Päis_VALUE.append('};');(näitaja_andmed/'resources.h').write_text('\n'.join(Päis_VALUE)+'\n',encoding='utf-8')
    sihtkoht_Failid=[]
    for Nimi_2 in ('kompilaator_tööriist.c','CLR_tugi.c','Käivita_2.c','미리번역.c','tagasi_saatma_sild.S'):
        sihtfail=näitaja_andmed/(Path(Nimi_2).stem+'.o');sihtkoht_Failid.append(sihtfail)
        Täida_käsk([_15_kompilaator]+konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nimi_2,'-o',sihtfail])
    실행파일=juur_tee/'build/user/cc.elf'
    Täida_käsk([연결편집기,'--gc-sections','-T',juur_tee/'kasutaja/Link_küljend.ld','-z','max-page-size=4096','-o',실행파일,
         juur_tee/'build/user/start.o',juur_tee/'build/user/runtime.o']+sihtkoht_Failid+
         [juur_tee/'build/user'/Nimi_2 for Nimi_2 in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
