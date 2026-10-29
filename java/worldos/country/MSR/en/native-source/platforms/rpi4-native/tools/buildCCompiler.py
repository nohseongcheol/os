"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def createCCompiler(rootPath, repositoryPath, CCompiler, linkerTool, configurationBits, executeCommand):
    resultData = rootPath / 'build/ccompiler'; resultData.mkdir(exist_ok=True)
    originalData = rootPath / 'CCompiler'
    upstream = rootPath / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    developmentKit = rootPath / 'vendor/sdk'
    if not (developmentKit/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    builtins = sorted((developmentKit/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not builtins: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    configurationBits = [settingsValue for settingsValue in configurationBits if settingsValue != '-mgeneral-regs-only']
    includes = ['-I', originalData, '-I', upstream, '-I', rootPath/'User', '-I', resultData, '-isystem', developmentKit/'usr/include']
    executeCommand([CCompiler]+configurationBits+['-ffunction-sections','-fdata-sections']+includes+['-c',originalData/'startupSupport.c','-o',resultData/'crt.o'])
    executeCommand([CCompiler]+configurationBits+['-I',repositoryPath/'posix-kor/arm64-native/headers']+includes+['-c',originalData/'aotRuntime.c','-o',resultData/'aot-runtime.o'])
    assets = [('/sdk/include/'+dataPosition.name,dataPosition) for dataPosition in sorted((repositoryPath/'posix-kor/arm64-native/headers').glob('*.h'))]
    assets += [('/sdk/include/'+dataPosition.name,dataPosition) for dataPosition in sorted((upstream/'include').glob('*.h'))]
    assets += [('/sdk/include/'+dataPosition.name,dataPosition) for dataPosition in sorted((originalData/'developmentHeaders').glob('*.h'))]
    assets += [('/sdk/lib/start.o',rootPath/'build/user/start.o'),('/sdk/lib/crt.o',resultData/'crt.o'),('/sdk/lib/aot-runtime.o',resultData/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rootPath/'build/libposix-kor-user.a')]
    headerValue=['typedef struct { const char *name; const unsigned char *data; unsigned size; } compilerResource;']
    for ordinalIndex,(_,path) in enumerate(assets):
        headerValue.append('static const unsigned char 탑재자원_%d[] = {%s};'%(ordinalIndex,','.join(str(temporaryData) for temporaryData in path.read_bytes())))
    headerValue.append('static const compilerResource compilerResources[] = {')
    for ordinalIndex,(name,path) in enumerate(assets): headerValue.append('{%s, 탑재자원_%d, %d},'%(json.dumps(name,ensure_ascii=False),ordinalIndex,path.stat().st_size))
    headerValue.append('};');(resultData/'resources.h').write_text('\n'.join(headerValue)+'\n',encoding='utf-8')
    destinationFiles=[]
    for name in ('compilerTool.c','RuntimeSupport.c','run.c','aheadOfTime.c','returnBridge.S'):
        destinationFile=resultData/(Path(name).stem+'.o');destinationFiles.append(destinationFile)
        executeCommand([CCompiler]+configurationBits+['-ffunction-sections','-fdata-sections']+includes+['-c',originalData/name,'-o',destinationFile])
    executableFile=rootPath/'build/user/cc.elf'
    executeCommand([linkerTool,'--gc-sections','-T',rootPath/'User/link_layout.ld','-z','max-page-size=4096','-o',executableFile,
         rootPath/'build/user/start.o',rootPath/'build/user/runtime.o']+destinationFiles+
         [rootPath/'build/user'/name for name in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[builtins[-1]])
