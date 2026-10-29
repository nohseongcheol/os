"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(rrënjë_shteg, depo_shteg, 시언어번역기, 연결편집기, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, zbatoj_komandë):
    llogaritje_të_dhëna = rrënjë_shteg / 'build/ccompiler'; llogaritje_të_dhëna.mkdir(exist_ok=True)
    원본자료 = rrënjë_shteg / '시언어번역기'
    upstream = rrënjë_shteg / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = rrënjë_shteg / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond = [cilësimet_VALUE for cilësimet_VALUE in konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond if cilësimet_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstream, '-I', rrënjë_shteg/'përdorues', '-I', llogaritje_të_dhëna, '-isystem', 개발꾸러미/'usr/include']
    zbatoj_komandë([시언어번역기]+konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'nisje_Mbështetje.c','-o',llogaritje_të_dhëna/'crt.o'])
    zbatoj_komandë([시언어번역기]+konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond+['-I',depo_shteg/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',llogaritje_të_dhëna/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+të_dhëna_pozicioni.name,të_dhëna_pozicioni) for të_dhëna_pozicioni in sorted((depo_shteg/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+të_dhëna_pozicioni.name,të_dhëna_pozicioni) for të_dhëna_pozicioni in sorted((upstream/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+të_dhëna_pozicioni.name,të_dhëna_pozicioni) for të_dhëna_pozicioni in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rrënjë_shteg/'build/user/start.o'),('/sdk/lib/crt.o',llogaritje_të_dhëna/'crt.o'),('/sdk/lib/aot-runtime.o',llogaritje_të_dhëna/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rrënjë_shteg/'build/libposix-kor-user.a')]
    Kreu_VALUE=['typedef struct { const char *Emër; const unsigned char *të_dhëna; unsigned Madhësi; } 번역기자원;']
    for 순번,(_,POZICIONI) in enumerate(탑재자료):
        Kreu_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in POZICIONI.read_bytes())))
    Kreu_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Emër,POZICIONI) in enumerate(탑재자료): Kreu_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Emër,ensure_ascii=False),순번,POZICIONI.stat().st_size))
    Kreu_VALUE.append('};');(llogaritje_të_dhëna/'resources.h').write_text('\n'.join(Kreu_VALUE)+'\n',encoding='utf-8')
    vendmbërritje_Skedarët=[]
    for Emër in ('번역기.c','koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje.c','Ekzekuto.c','미리번역.c','Kthe_urë.S'):
        skedari_i_vendmbërritjes=llogaritje_të_dhëna/(Path(Emër).stem+'.o');vendmbërritje_Skedarët.append(skedari_i_vendmbërritjes)
        zbatoj_komandë([시언어번역기]+konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Emër,'-o',skedari_i_vendmbërritjes])
    실행파일=rrënjë_shteg/'build/user/cc.elf'
    zbatoj_komandë([연결편집기,'--gc-sections','-T',rrënjë_shteg/'përdorues/lidh_Navigimi.ld','-z','max-page-size=4096','-o',실행파일,
         rrënjë_shteg/'build/user/start.o',rrënjë_shteg/'build/user/runtime.o']+vendmbërritje_Skedarët+
         [rrënjë_shteg/'build/user'/Emër for Emër in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
