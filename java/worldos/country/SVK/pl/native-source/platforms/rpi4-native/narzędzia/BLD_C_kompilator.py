"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Twórca_C_kompilator(korzeń_ścieżka, repozytorium_ścieżka, C_kompilator, konsolidator_narzędzie, konfiguracja_BITS, Wykonaj_polecenie):
    KR_dane = korzeń_ścieżka / 'build/ccompiler'; KR_dane.mkdir(exist_ok=True)
    원본자료 = korzeń_ścieżka / 'C_kompilator'
    nadrzędny_99f91985 = korzeń_ścieżka / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    zestaw_deweloperski = korzeń_ścieżka / 'vendor/sdk'
    if not (zestaw_deweloperski/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((zestaw_deweloperski/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguracja_BITS = [Ustawienia_WARTOŚĆ for Ustawienia_WARTOŚĆ in konfiguracja_BITS if Ustawienia_WARTOŚĆ != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', nadrzędny_99f91985, '-I', korzeń_ścieżka/'przestrzeń_użytkownika', '-I', KR_dane, '-isystem', zestaw_deweloperski/'usr/include']
    Wykonaj_polecenie([C_kompilator]+konfiguracja_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'uruchomienie_wsparcie.c','-o',KR_dane/'crt.o'])
    Wykonaj_polecenie([C_kompilator]+konfiguracja_BITS+['-I',repozytorium_ścieżka/'posix-kor/arm64-native/deklaracje']+포함인수+['-c',원본자료/'drzewo_obiektów_aplikacji_CLR.c','-o',KR_dane/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+dane_stanowisko.name,dane_stanowisko) for dane_stanowisko in sorted((repozytorium_ścieżka/'posix-kor/arm64-native/deklaracje').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dane_stanowisko.name,dane_stanowisko) for dane_stanowisko in sorted((nadrzędny_99f91985/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dane_stanowisko.name,dane_stanowisko) for dane_stanowisko in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',korzeń_ścieżka/'build/user/start.o'),('/sdk/lib/crt.o',KR_dane/'crt.o'),('/sdk/lib/aot-runtime.o',KR_dane/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',korzeń_ścieżka/'build/libposix-kor-user.a')]
    Nagłówek_WARTOŚĆ=['typedef struct { const char *Nazwa; const unsigned char *dane; unsigned Rozmiar; } kompilator_zasób;']
    for 순번,(_,ścieżka_2) in enumerate(탑재자료):
        Nagłówek_WARTOŚĆ.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ścieżka_2.read_bytes())))
    Nagłówek_WARTOŚĆ.append('static const kompilator_zasób kompilator_Zasoby[] = {')
    for 순번,(Nazwa,ścieżka_2) in enumerate(탑재자료): Nagłówek_WARTOŚĆ.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nazwa,ensure_ascii=False),순번,ścieżka_2.stat().st_size))
    Nagłówek_WARTOŚĆ.append('};');(KR_dane/'resources.h').write_text('\n'.join(Nagłówek_WARTOŚĆ)+'\n',encoding='utf-8')
    cel_Files=[]
    for Nazwa in ('kompilator_narzędzie.c','CLR_wsparcie.c','Uruchom_2.c','미리번역.c','Zwrot_mostek.S'):
        plik_docelowy=KR_dane/(Path(Nazwa).stem+'.o');cel_Files.append(plik_docelowy)
        Wykonaj_polecenie([C_kompilator]+konfiguracja_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nazwa,'-o',plik_docelowy])
    plik_wykonywalny=korzeń_ścieżka/'build/user/cc.elf'
    Wykonaj_polecenie([konsolidator_narzędzie,'--gc-sections','-T',korzeń_ścieżka/'przestrzeń_użytkownika/układ_konsolidacji.ld','-z','max-page-size=4096','-o',plik_wykonywalny,
         korzeń_ścieżka/'build/user/start.o',korzeń_ścieżka/'build/user/runtime.o']+cel_Files+
         [korzeń_ścieżka/'build/user'/Nazwa for Nazwa in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
