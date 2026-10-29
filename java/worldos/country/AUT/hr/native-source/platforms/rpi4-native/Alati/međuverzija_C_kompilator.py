"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Create_C_kompilator(korijen_put, spremište_put, C_kompilator, 연결편집기, konfiguracija_Pozadinski_pametni_servis_za_transfer, Izvrši_naredba):
    KR_podaci = korijen_put / 'build/ccompiler'; KR_podaci.mkdir(exist_ok=True)
    원본자료 = korijen_put / 'C_kompilator'
    koji_ažurira_izvornik = korijen_put / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    set_razvojnih_alata = korijen_put / 'vendor/sdk'
    if not (set_razvojnih_alata/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((set_razvojnih_alata/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguracija_Pozadinski_pametni_servis_za_transfer = [Postavke_VALUE for Postavke_VALUE in konfiguracija_Pozadinski_pametni_servis_za_transfer if Postavke_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', koji_ažurira_izvornik, '-I', korijen_put/'korisnik', '-I', KR_podaci, '-isystem', set_razvojnih_alata/'usr/include']
    Izvrši_naredba([C_kompilator]+konfiguracija_Pozadinski_pametni_servis_za_transfer+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'pokretanje_Podrška.c','-o',KR_podaci/'crt.o'])
    Izvrši_naredba([C_kompilator]+konfiguracija_Pozadinski_pametni_servis_za_transfer+['-I',spremište_put/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',KR_podaci/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+podaci_položaj.name,podaci_položaj) for podaci_položaj in sorted((spremište_put/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podaci_položaj.name,podaci_položaj) for podaci_položaj in sorted((koji_ažurira_izvornik/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podaci_položaj.name,podaci_položaj) for podaci_položaj in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',korijen_put/'build/user/start.o'),('/sdk/lib/crt.o',KR_podaci/'crt.o'),('/sdk/lib/aot-runtime.o',KR_podaci/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',korijen_put/'build/libposix-kor-user.a')]
    Zaglavlje_VALUE=['typedef struct { const char *Ime; const unsigned char *podaci; unsigned Veličina; } kompilator_resurs;']
    for 순번,(_,PUTANJA) in enumerate(탑재자료):
        Zaglavlje_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in PUTANJA.read_bytes())))
    Zaglavlje_VALUE.append('static const kompilator_resurs kompilator_Resursi[] = {')
    for 순번,(Ime,PUTANJA) in enumerate(탑재자료): Zaglavlje_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Ime,ensure_ascii=False),순번,PUTANJA.stat().st_size))
    Zaglavlje_VALUE.append('};');(KR_podaci/'resources.h').write_text('\n'.join(Zaglavlje_VALUE)+'\n',encoding='utf-8')
    odredište_Datoteke=[]
    for Ime in ('kompilator_alat.c','CLR_Podrška.c','Pokreni.c','미리번역.c','vratiti_most.S'):
        odredišna_datoteka=KR_podaci/(Path(Ime).stem+'.o');odredište_Datoteke.append(odredišna_datoteka)
        Izvrši_naredba([C_kompilator]+konfiguracija_Pozadinski_pametni_servis_za_transfer+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Ime,'-o',odredišna_datoteka])
    실행파일=korijen_put/'build/user/cc.elf'
    Izvrši_naredba([연결편집기,'--gc-sections','-T',korijen_put/'korisnik/veza_Raspored.ld','-z','max-page-size=4096','-o',실행파일,
         korijen_put/'build/user/start.o',korijen_put/'build/user/runtime.o']+odredište_Datoteke+
         [korijen_put/'build/user'/Ime for Ime in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
