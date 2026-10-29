"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(kök_yol, anbar_yol, 시언어번역기, 연결편집기, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, icra_etmək_əmr):
    ölçü_verilənlər = kök_yol / 'build/ccompiler'; ölçü_verilənlər.mkdir(exist_ok=True)
    원본자료 = kök_yol / '시언어번역기'
    mənbə_istiqaməti = kök_yol / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = kök_yol / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti = [Parametrlər_VALUE for Parametrlər_VALUE in konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti if Parametrlər_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', mənbə_istiqaməti, '-I', kök_yol/'istifadəçi', '-I', ölçü_verilənlər, '-isystem', 개발꾸러미/'usr/include']
    icra_etmək_əmr([시언어번역기]+konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'yükləmə_Dəstək.c','-o',ölçü_verilənlər/'crt.o'])
    icra_etmək_əmr([시언어번역기]+konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti+['-I',anbar_yol/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ölçü_verilənlər/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+verilənlər_yerinə_qoymaq.name,verilənlər_yerinə_qoymaq) for verilənlər_yerinə_qoymaq in sorted((anbar_yol/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+verilənlər_yerinə_qoymaq.name,verilənlər_yerinə_qoymaq) for verilənlər_yerinə_qoymaq in sorted((mənbə_istiqaməti/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+verilənlər_yerinə_qoymaq.name,verilənlər_yerinə_qoymaq) for verilənlər_yerinə_qoymaq in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',kök_yol/'build/user/start.o'),('/sdk/lib/crt.o',ölçü_verilənlər/'crt.o'),('/sdk/lib/aot-runtime.o',ölçü_verilənlər/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',kök_yol/'build/libposix-kor-user.a')]
    Başlıq_VALUE=['typedef struct { const char *Ad; const unsigned char *verilənlər; unsigned Böyüklük; } 번역기자원;']
    for 순번,(_,Cığır) in enumerate(탑재자료):
        Başlıq_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Cığır.read_bytes())))
    Başlıq_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Ad,Cığır) in enumerate(탑재자료): Başlıq_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Ad,ensure_ascii=False),순번,Cığır.stat().st_size))
    Başlıq_VALUE.append('};');(ölçü_verilənlər/'resources.h').write_text('\n'.join(Başlıq_VALUE)+'\n',encoding='utf-8')
    təyinat_Fayllar=[]
    for Ad in ('번역기.c','ümumi_dil_icrası_Dəstək.c','İcra_Et.c','미리번역.c','geri_qaytarmaq_körpü.S'):
        təyinat_faylı=ölçü_verilənlər/(Path(Ad).stem+'.o');təyinat_Fayllar.append(təyinat_faylı)
        icra_etmək_əmr([시언어번역기]+konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Ad,'-o',təyinat_faylı])
    실행파일=kök_yol/'build/user/cc.elf'
    icra_etmək_əmr([연결편집기,'--gc-sections','-T',kök_yol/'istifadəçi/keçid_Düzüm.ld','-z','max-page-size=4096','-o',실행파일,
         kök_yol/'build/user/start.o',kök_yol/'build/user/runtime.o']+təyinat_Fayllar+
         [kök_yol/'build/user'/Ad for Ad in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
