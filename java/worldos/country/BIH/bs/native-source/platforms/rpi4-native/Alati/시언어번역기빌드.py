"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(koijen_put, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Izvrši_komanda):
    mjera_podaci = koijen_put / 'build/ccompiler'; mjera_podaci.mkdir(exist_ok=True)
    원본자료 = koijen_put / '시언어번역기'
    외부원문 = koijen_put / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = koijen_put / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Postavke_VALUE for Postavke_VALUE in 설정비트 if Postavke_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', koijen_put/'korisnik', '-I', mjera_podaci, '-isystem', 개발꾸러미/'usr/include']
    Izvrši_komanda([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'pokretanje_Podrška.c','-o',mjera_podaci/'crt.o'])
    Izvrši_komanda([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',mjera_podaci/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+podaci_položaj.name,podaci_položaj) for podaci_položaj in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podaci_položaj.name,podaci_položaj) for podaci_položaj in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podaci_položaj.name,podaci_položaj) for podaci_položaj in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',koijen_put/'build/user/start.o'),('/sdk/lib/crt.o',mjera_podaci/'crt.o'),('/sdk/lib/aot-runtime.o',mjera_podaci/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',koijen_put/'build/libposix-kor-user.a')]
    Zaglavlje_VALUE=['typedef struct { const char *Naziv; const unsigned char *podaci; unsigned Veličina; } 번역기자원;']
    for 순번,(_,Putanja) in enumerate(탑재자료):
        Zaglavlje_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Putanja.read_bytes())))
    Zaglavlje_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Naziv,Putanja) in enumerate(탑재자료): Zaglavlje_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Naziv,ensure_ascii=False),순번,Putanja.stat().st_size))
    Zaglavlje_VALUE.append('};');(mjera_podaci/'resources.h').write_text('\n'.join(Zaglavlje_VALUE)+'\n',encoding='utf-8')
    odredište_Fajlovi=[]
    for Naziv in ('번역기.c','zajednička_jezička_biblioteka_Podrška.c','Pokreni.c','미리번역.c','vratiti_most.S'):
        odredišni_fajl=mjera_podaci/(Path(Naziv).stem+'.o');odredište_Fajlovi.append(odredišni_fajl)
        Izvrši_komanda([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Naziv,'-o',odredišni_fajl])
    실행파일=koijen_put/'build/user/cc.elf'
    Izvrši_komanda([연결편집기,'--gc-sections','-T',koijen_put/'korisnik/Veza_izgled.ld','-z','max-page-size=4096','-o',실행파일,
         koijen_put/'build/user/start.o',koijen_put/'build/user/runtime.o']+odredište_Fajlovi+
         [koijen_put/'build/user'/Naziv for Naziv in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
