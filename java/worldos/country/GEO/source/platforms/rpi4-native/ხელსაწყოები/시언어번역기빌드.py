"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ფესვი_მდებარეობა, 저장소경로, 시언어번역기, 연결편집기, 설정비트, შესრულება_ბრძანება):
    გაზომვა_მონაცემები = ფესვი_მდებარეობა / 'build/ccompiler'; გაზომვა_მონაცემები.mkdir(exist_ok=True)
    원본자료 = ფესვი_მდებარეობა / '시언어번역기'
    외부원문 = ფესვი_მდებარეობა / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ფესვი_მდებარეობა / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [პარამეტრები_მნიშვნელობა for პარამეტრები_მნიშვნელობა in 설정비트 if პარამეტრები_მნიშვნელობა != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', ფესვი_მდებარეობა/'მომხმარებელი', '-I', გაზომვა_მონაცემები, '-isystem', 개발꾸러미/'usr/include']
    შესრულება_ბრძანება([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ჩატვირთვა_მხარდაჭერა.c','-o',გაზომვა_მონაცემები/'crt.o'])
    შესრულება_ბრძანება([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',გაზომვა_მონაცემები/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+მონაცემები_პოზიცია.name,მონაცემები_პოზიცია) for მონაცემები_პოზიცია in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+მონაცემები_პოზიცია.name,მონაცემები_პოზიცია) for მონაცემები_პოზიცია in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+მონაცემები_პოზიცია.name,მონაცემები_პოზიცია) for მონაცემები_პოზიცია in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ფესვი_მდებარეობა/'build/user/start.o'),('/sdk/lib/crt.o',გაზომვა_მონაცემები/'crt.o'),('/sdk/lib/aot-runtime.o',გაზომვა_მონაცემები/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ფესვი_მდებარეობა/'build/libposix-kor-user.a')]
    ზედა_კოლონტიტული_მნიშვნელობა=['typedef struct { const char *სახელი; const unsigned char *მონაცემები; unsigned ზომა; } 번역기자원;']
    for 순번,(_,გეზი) in enumerate(탑재자료):
        ზედა_კოლონტიტული_მნიშვნელობა.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in გეზი.read_bytes())))
    ზედა_კოლონტიტული_მნიშვნელობა.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(სახელი,გეზი) in enumerate(탑재자료): ზედა_კოლონტიტული_მნიშვნელობა.append('{%s, 탑재자원_%d, %d},'%(json.dumps(სახელი,ensure_ascii=False),순번,გეზი.stat().st_size))
    ზედა_კოლონტიტული_მნიშვნელობა.append('};');(გაზომვა_მონაცემები/'resources.h').write_text('\n'.join(ზედა_კოლონტიტული_მნიშვნელობა)+'\n',encoding='utf-8')
    მიმართულება_ფაილები=[]
    for სახელი in ('번역기.c','საერთო_ენობრივი_გარემო_მხარდაჭერა.c','გაშვება.c','미리번역.c','დაბრუნება_ხიდი.S'):
        დანიშნულების_ფაილი=გაზომვა_მონაცემები/(Path(სახელი).stem+'.o');მიმართულება_ფაილები.append(დანიშნულების_ფაილი)
        შესრულება_ბრძანება([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/სახელი,'-o',დანიშნულების_ფაილი])
    실행파일=ფესვი_მდებარეობა/'build/user/cc.elf'
    შესრულება_ბრძანება([연결편집기,'--gc-sections','-T',ფესვი_მდებარეობა/'მომხმარებელი/ბმული_განლაგება.ld','-z','max-page-size=4096','-o',실행파일,
         ფესვი_მდებარეობა/'build/user/start.o',ფესვი_მდებარეობა/'build/user/runtime.o']+მიმართულება_ფაილები+
         [ფესვი_მდებარეობა/'build/user'/სახელი for სახელი in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
