"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ildiz_yo_l, repozitoriy_yo_l, 시언어번역기, 연결편집기, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, bajarmoq_buyruq):
    o_lchov_ma_lumotlar = ildiz_yo_l / 'build/ccompiler'; o_lchov_ma_lumotlar.mkdir(exist_ok=True)
    원본자료 = ildiz_yo_l / '시언어번역기'
    yuqorida_turuvchi = ildiz_yo_l / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ildiz_yo_l / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati = [Sozlamalar_VALUE for Sozlamalar_VALUE in tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati if Sozlamalar_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', yuqorida_turuvchi, '-I', ildiz_yo_l/'foydalanuvchi', '-I', o_lchov_ma_lumotlar, '-isystem', 개발꾸러미/'usr/include']
    bajarmoq_buyruq([시언어번역기]+tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'yuklash_madad.c','-o',o_lchov_ma_lumotlar/'crt.o'])
    bajarmoq_buyruq([시언어번역기]+tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati+['-I',repozitoriy_yo_l/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',o_lchov_ma_lumotlar/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ma_lumotlar_holat.name,ma_lumotlar_holat) for ma_lumotlar_holat in sorted((repozitoriy_yo_l/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ma_lumotlar_holat.name,ma_lumotlar_holat) for ma_lumotlar_holat in sorted((yuqorida_turuvchi/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ma_lumotlar_holat.name,ma_lumotlar_holat) for ma_lumotlar_holat in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ildiz_yo_l/'build/user/start.o'),('/sdk/lib/crt.o',o_lchov_ma_lumotlar/'crt.o'),('/sdk/lib/aot-runtime.o',o_lchov_ma_lumotlar/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ildiz_yo_l/'build/libposix-kor-user.a')]
    Sarlavha_VALUE=['typedef struct { const char *Nomi; const unsigned char *ma_lumotlar; unsigned Hajmi; } 번역기자원;']
    for 순번,(_,yo_l) in enumerate(탑재자료):
        Sarlavha_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in yo_l.read_bytes())))
    Sarlavha_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Nomi,yo_l) in enumerate(탑재자료): Sarlavha_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nomi,ensure_ascii=False),순번,yo_l.stat().st_size))
    Sarlavha_VALUE.append('};');(o_lchov_ma_lumotlar/'resources.h').write_text('\n'.join(Sarlavha_VALUE)+'\n',encoding='utf-8')
    ko_chirish_joyi_Fayllar=[]
    for Nomi in ('번역기.c','umumiy_til_ish_jarayoni_madad.c','Bajarish.c','미리번역.c','되돌림.S'):
        natijalar_fayli=o_lchov_ma_lumotlar/(Path(Nomi).stem+'.o');ko_chirish_joyi_Fayllar.append(natijalar_fayli)
        bajarmoq_buyruq([시언어번역기]+tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nomi,'-o',natijalar_fayli])
    실행파일=ildiz_yo_l/'build/user/cc.elf'
    bajarmoq_buyruq([연결편집기,'--gc-sections','-T',ildiz_yo_l/'foydalanuvchi/ulash_Maket.ld','-z','max-page-size=4096','-o',실행파일,
         ildiz_yo_l/'build/user/start.o',ildiz_yo_l/'build/user/runtime.o']+ko_chirish_joyi_Fayllar+
         [ildiz_yo_l/'build/user'/Nomi for Nomi in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
