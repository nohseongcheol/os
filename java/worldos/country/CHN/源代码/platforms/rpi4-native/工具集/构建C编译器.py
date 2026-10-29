"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 创建C编译器(根路径, 代码库路径, C编译器, 链接器工具, 配置项位列, 执行命令):
    结果数据 = 根路径 / 'build/ccompiler'; 结果数据.mkdir(exist_ok=True)
    原始数据 = 根路径 / 'C编译器'
    上游 = 根路径 / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    开发工具套件 = 根路径 / 'vendor/sdk'
    if not (开发工具套件/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    内建项集 = sorted((开发工具套件/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 内建项集: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    配置项位列 = [设置值 for 设置值 in 配置项位列 if 设置值 != '-mgeneral-regs-only']
    包含项 = ['-I', 原始数据, '-I', 上游, '-I', 根路径/'用户', '-I', 结果数据, '-isystem', 开发工具套件/'usr/include']
    执行命令([C编译器]+配置项位列+['-ffunction-sections','-fdata-sections']+包含项+['-c',原始数据/'启动支持.c','-o',结果数据/'crt.o'])
    执行命令([C编译器]+配置项位列+['-I',代码库路径/'posix-kor/arm64-native/头文件']+包含项+['-c',原始数据/'提前编译运行时.c','-o',结果数据/'aot-runtime.o'])
    资源素材 = [('/sdk/include/'+数据位置.name,数据位置) for 数据位置 in sorted((代码库路径/'posix-kor/arm64-native/头文件').glob('*.h'))]
    资源素材 += [('/sdk/include/'+数据位置.name,数据位置) for 数据位置 in sorted((上游/'include').glob('*.h'))]
    资源素材 += [('/sdk/include/'+数据位置.name,数据位置) for 数据位置 in sorted((原始数据/'开发头文件集').glob('*.h'))]
    资源素材 += [('/sdk/lib/start.o',根路径/'build/user/start.o'),('/sdk/lib/crt.o',结果数据/'crt.o'),('/sdk/lib/aot-runtime.o',结果数据/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',根路径/'build/libposix-kor-user.a')]
    头部值=['typedef struct { const char *名称; const unsigned char *数据; unsigned 大小; } 编译器资源;']
    for 序数索引,(_,路径) in enumerate(资源素材):
        头部值.append('static const unsigned char 탑재자원_%d[] = {%s};'%(序数索引,','.join(str(临时数据) for 临时数据 in 路径.read_bytes())))
    头部值.append('static const 编译器资源 编译器资源集[] = {')
    for 序数索引,(名称,路径) in enumerate(资源素材): 头部值.append('{%s, 탑재자원_%d, %d},'%(json.dumps(名称,ensure_ascii=False),序数索引,路径.stat().st_size))
    头部值.append('};');(结果数据/'resources.h').write_text('\n'.join(头部值)+'\n',encoding='utf-8')
    目的地址文件集=[]
    for 名称 in ('编译器工具.c','运行时支持.c','运行.c','提前所属时间.c','发回桥接.S'):
        目的地址文件=结果数据/(Path(名称).stem+'.o');目的地址文件集.append(目的地址文件)
        执行命令([C编译器]+配置项位列+['-ffunction-sections','-fdata-sections']+包含项+['-c',原始数据/名称,'-o',目的地址文件])
    可执行文件文件=根路径/'build/user/cc.elf'
    执行命令([链接器工具,'--gc-sections','-T',根路径/'用户/链接布局.ld','-z','max-page-size=4096','-o',可执行文件文件,
         根路径/'build/user/start.o',根路径/'build/user/runtime.o']+目的地址文件集+
         [根路径/'build/user'/名称 for 名称 in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[内建项集[-1]])
