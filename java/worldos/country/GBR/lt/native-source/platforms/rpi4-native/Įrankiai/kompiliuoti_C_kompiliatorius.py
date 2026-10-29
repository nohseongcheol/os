"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def kurti_C_kompiliatorius(šaknis_kelias, saugykla_kelias, C_kompiliatorius, 연결편집기, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, Vykdyti_komanda):
    KR_duomenys = šaknis_kelias / 'build/ccompiler'; KR_duomenys.mkdir(exist_ok=True)
    원본자료 = šaknis_kelias / 'C_kompiliatorius'
    šaltinio = šaknis_kelias / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    programuotojo_rinkinys = šaknis_kelias / 'vendor/sdk'
    if not (programuotojo_rinkinys/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((programuotojo_rinkinys/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba = [Parametrai_VALUE for Parametrai_VALUE in konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba if Parametrai_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', šaltinio, '-I', šaknis_kelias/'naudotojas', '-I', KR_duomenys, '-isystem', programuotojo_rinkinys/'usr/include']
    Vykdyti_komanda([C_kompiliatorius]+konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'perkrovimas_pagalba.c','-o',KR_duomenys/'crt.o'])
    Vykdyti_komanda([C_kompiliatorius]+konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba+['-I',saugykla_kelias/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KR_duomenys/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+duomenys_padėtis.name,duomenys_padėtis) for duomenys_padėtis in sorted((saugykla_kelias/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+duomenys_padėtis.name,duomenys_padėtis) for duomenys_padėtis in sorted((šaltinio/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+duomenys_padėtis.name,duomenys_padėtis) for duomenys_padėtis in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',šaknis_kelias/'build/user/start.o'),('/sdk/lib/crt.o',KR_duomenys/'crt.o'),('/sdk/lib/aot-runtime.o',KR_duomenys/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',šaknis_kelias/'build/libposix-kor-user.a')]
    Antraštė_VALUE=['typedef struct { const char *Pavadinimas_2; const unsigned char *duomenys; unsigned Dydis; } kompiliatorius_ištekliai;']
    for 순번,(_,KELIAS) in enumerate(탑재자료):
        Antraštė_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in KELIAS.read_bytes())))
    Antraštė_VALUE.append('static const kompiliatorius_ištekliai kompiliatorius_Ištekliai[] = {')
    for 순번,(Pavadinimas_2,KELIAS) in enumerate(탑재자료): Antraštė_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Pavadinimas_2,ensure_ascii=False),순번,KELIAS.stat().st_size))
    Antraštė_VALUE.append('};');(KR_duomenys/'resources.h').write_text('\n'.join(Antraštė_VALUE)+'\n',encoding='utf-8')
    vieta_Failai=[]
    for Pavadinimas_2 in ('kompiliatorius_įrankis.c','CLR_pagalba.c','Paleisti.c','미리번역.c','grąžinti_tiltas.S'):
        paskirties_failas=KR_duomenys/(Path(Pavadinimas_2).stem+'.o');vieta_Failai.append(paskirties_failas)
        Vykdyti_komanda([C_kompiliatorius]+konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Pavadinimas_2,'-o',paskirties_failas])
    실행파일=šaknis_kelias/'build/user/cc.elf'
    Vykdyti_komanda([연결편집기,'--gc-sections','-T',šaknis_kelias/'naudotojas/sieti_schema.ld','-z','max-page-size=4096','-o',실행파일,
         šaknis_kelias/'build/user/start.o',šaknis_kelias/'build/user/runtime.o']+vieta_Failai+
         [šaknis_kelias/'build/user'/Pavadinimas_2 for Pavadinimas_2 in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
