"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(pūtake_ara, 저장소경로, 시언어번역기, 연결편집기, 설정비트, kawe_tono):
    mēhua_raraunga = pūtake_ara / 'build/ccompiler'; mēhua_raraunga.mkdir(exist_ok=True)
    원본자료 = pūtake_ara / '시언어번역기'
    외부원문 = pūtake_ara / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = pūtake_ara / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Ngā_Tautuhinga_uara for Ngā_Tautuhinga_uara in 설정비트 if Ngā_Tautuhinga_uara != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', pūtake_ara/'kaiwhakamahi', '-I', mēhua_raraunga, '-isystem', 개발꾸러미/'usr/include']
    kawe_tono([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'whakaara_Tautoko.c','-o',mēhua_raraunga/'crt.o'])
    kawe_tono([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',mēhua_raraunga/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+raraunga_tūranga.name,raraunga_tūranga) for raraunga_tūranga in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+raraunga_tūranga.name,raraunga_tūranga) for raraunga_tūranga in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+raraunga_tūranga.name,raraunga_tūranga) for raraunga_tūranga in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',pūtake_ara/'build/user/start.o'),('/sdk/lib/crt.o',mēhua_raraunga/'crt.o'),('/sdk/lib/aot-runtime.o',mēhua_raraunga/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',pūtake_ara/'build/libposix-kor-user.a')]
    Pane_uara=['typedef struct { const char *Ingoa; const unsigned char *raraunga; unsigned rahi; } 번역기자원;']
    for 순번,(_,ara) in enumerate(탑재자료):
        Pane_uara.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ara.read_bytes())))
    Pane_uara.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Ingoa,ara) in enumerate(탑재자료): Pane_uara.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Ingoa,ensure_ascii=False),순번,ara.stat().st_size))
    Pane_uara.append('};');(mēhua_raraunga/'resources.h').write_text('\n'.join(Pane_uara)+'\n',encoding='utf-8')
    ūnga_Ngā_Kōnae=[]
    for Ingoa in ('번역기.c','wāhaere_reo_noa_Tautoko.c','whakahaere.c','미리번역.c','되돌림.S'):
        kōnae_ūnga_ffac9b48=mēhua_raraunga/(Path(Ingoa).stem+'.o');ūnga_Ngā_Kōnae.append(kōnae_ūnga_ffac9b48)
        kawe_tono([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Ingoa,'-o',kōnae_ūnga_ffac9b48])
    실행파일=pūtake_ara/'build/user/cc.elf'
    kawe_tono([연결편집기,'--gc-sections','-T',pūtake_ara/'kaiwhakamahi/Hono_Tahora.ld','-z','max-page-size=4096','-o',실행파일,
         pūtake_ara/'build/user/start.o',pūtake_ara/'build/user/runtime.o']+ūnga_Ngā_Kōnae+
         [pūtake_ara/'build/user'/Ingoa for Ingoa in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
