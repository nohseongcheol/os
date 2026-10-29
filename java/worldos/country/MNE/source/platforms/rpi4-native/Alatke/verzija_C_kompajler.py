"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Create_C_kompajler(koren_putanja, depo_putanja, C_kompajler, 연결편집기, konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini, Izvrši_komanda):
    KR_podaci = koren_putanja / 'build/ccompiler'; KR_podaci.mkdir(exist_ok=True)
    원본자료 = koren_putanja / 'C_kompajler'
    izvorni = koren_putanja / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    komplet_za_razvoj_programa = koren_putanja / 'vendor/sdk'
    if not (komplet_za_razvoj_programa/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((komplet_za_razvoj_programa/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini = [Postavke_VALUE for Postavke_VALUE in konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini if Postavke_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', izvorni, '-I', koren_putanja/'korisnik', '-I', KR_podaci, '-isystem', komplet_za_razvoj_programa/'usr/include']
    Izvrši_komanda([C_kompajler]+konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'시작지원.c','-o',KR_podaci/'crt.o'])
    Izvrši_komanda([C_kompajler]+konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini+['-I',depo_putanja/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',KR_podaci/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+podaci_pozicija.name,podaci_pozicija) for podaci_pozicija in sorted((depo_putanja/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podaci_pozicija.name,podaci_pozicija) for podaci_pozicija in sorted((izvorni/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podaci_pozicija.name,podaci_pozicija) for podaci_pozicija in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',koren_putanja/'build/user/start.o'),('/sdk/lib/crt.o',KR_podaci/'crt.o'),('/sdk/lib/aot-runtime.o',KR_podaci/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',koren_putanja/'build/libposix-kor-user.a')]
    Zaglavlje_VALUE=['typedef struct { const char *ime; const unsigned char *podaci; unsigned promeniti_veličinu; } kompajler_resurs;']
    for 순번,(_,putanja) in enumerate(탑재자료):
        Zaglavlje_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in putanja.read_bytes())))
    Zaglavlje_VALUE.append('static const kompajler_resurs kompajler_Izvori[] = {')
    for 순번,(ime,putanja) in enumerate(탑재자료): Zaglavlje_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ime,ensure_ascii=False),순번,putanja.stat().st_size))
    Zaglavlje_VALUE.append('};');(KR_podaci/'resources.h').write_text('\n'.join(Zaglavlje_VALUE)+'\n',encoding='utf-8')
    odredište_Datoteke=[]
    for ime in ('kompajler_alatka.c','CLR_komponenta_Podrška.c','koristiti.c','미리번역.c','vratiti_most.S'):
        odredišna_datoteka=KR_podaci/(Path(ime).stem+'.o');odredište_Datoteke.append(odredišna_datoteka)
        Izvrši_komanda([C_kompajler]+konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ime,'-o',odredišna_datoteka])
    실행파일=koren_putanja/'build/user/cc.elf'
    Izvrši_komanda([연결편집기,'--gc-sections','-T',koren_putanja/'korisnik/Veza_Raspored.ld','-z','max-page-size=4096','-o',실행파일,
         koren_putanja/'build/user/start.o',koren_putanja/'build/user/runtime.o']+odredište_Datoteke+
         [koren_putanja/'build/user'/ime for ime in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
