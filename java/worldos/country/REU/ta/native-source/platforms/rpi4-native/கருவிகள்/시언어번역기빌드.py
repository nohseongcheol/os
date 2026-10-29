"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(மூலம்_பாதை, தொகுபதிவகம்_பாதை, 시언어번역기, 연결편집기, உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை, இயக்கு_கட்டளை):
    அளவிடக்கூடியது_தரவு = மூலம்_பாதை / 'build/ccompiler'; அளவிடக்கூடியது_தரவு.mkdir(exist_ok=True)
    원본자료 = மூலம்_பாதை / '시언어번역기'
    அப்ஸ்ட்ரீம் = மூலம்_பாதை / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = மூலம்_பாதை / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை = [அமைப்புகள்_மதிப்பு for அமைப்புகள்_மதிப்பு in உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை if அமைப்புகள்_மதிப்பு != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', அப்ஸ்ட்ரீம், '-I', மூலம்_பாதை/'பயனர்', '-I', அளவிடக்கூடியது_தரவு, '-isystem', 개발꾸러미/'usr/include']
    இயக்கு_கட்டளை([시언어번역기]+உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'இயக்கம்_ஆதரவு.c','-o',அளவிடக்கூடியது_தரவு/'crt.o'])
    இயக்கு_கட்டளை([시언어번역기]+உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை+['-I',தொகுபதிவகம்_பாதை/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',அளவிடக்கூடியது_தரவு/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+தரவு_நிலை.name,தரவு_நிலை) for தரவு_நிலை in sorted((தொகுபதிவகம்_பாதை/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+தரவு_நிலை.name,தரவு_நிலை) for தரவு_நிலை in sorted((அப்ஸ்ட்ரீம்/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+தரவு_நிலை.name,தரவு_நிலை) for தரவு_நிலை in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',மூலம்_பாதை/'build/user/start.o'),('/sdk/lib/crt.o',அளவிடக்கூடியது_தரவு/'crt.o'),('/sdk/lib/aot-runtime.o',அளவிடக்கூடியது_தரவு/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',மூலம்_பாதை/'build/libposix-kor-user.a')]
    மேற்குறிப்பு_மதிப்பு=['typedef struct { const char *பெயர்; const unsigned char *தரவு; unsigned அளவு; } 번역기자원;']
    for 순번,(_,பாதை_2) in enumerate(탑재자료):
        மேற்குறிப்பு_மதிப்பு.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in பாதை_2.read_bytes())))
    மேற்குறிப்பு_மதிப்பு.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(பெயர்,பாதை_2) in enumerate(탑재자료): மேற்குறிப்பு_மதிப்பு.append('{%s, 탑재자원_%d, %d},'%(json.dumps(பெயர்,ensure_ascii=False),순번,பாதை_2.stat().st_size))
    மேற்குறிப்பு_மதிப்பு.append('};');(அளவிடக்கூடியது_தரவு/'resources.h').write_text('\n'.join(மேற்குறிப்பு_மதிப்பு)+'\n',encoding='utf-8')
    இலக்கு_கோப்புகள்=[]
    for பெயர் in ('번역기.c','பொது_மொழி_இயக்க_நேரம்_ஆதரவு.c','செயல்படுத்துக.c','미리번역.c','되돌림.S'):
        இலக்குக்_கோப்பு=அளவிடக்கூடியது_தரவு/(Path(பெயர்).stem+'.o');இலக்கு_கோப்புகள்.append(இலக்குக்_கோப்பு)
        இயக்கு_கட்டளை([시언어번역기]+உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/பெயர்,'-o',இலக்குக்_கோப்பு])
    செயல்படுத்தக்கூடிய_கோப்பு=மூலம்_பாதை/'build/user/cc.elf'
    இயக்கு_கட்டளை([연결편집기,'--gc-sections','-T',மூலம்_பாதை/'பயனர்/இணை_லேஅவுட்.ld','-z','max-page-size=4096','-o',செயல்படுத்தக்கூடிய_கோப்பு,
         மூலம்_பாதை/'build/user/start.o',மூலம்_பாதை/'build/user/runtime.o']+இலக்கு_கோப்புகள்+
         [மூலம்_பாதை/'build/user'/பெயர் for பெயர் in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
