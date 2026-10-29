#!/usr/bin/env python3
"""libclang 声明·引用 위치를 수집한다. 外部值 헤더의 멤버는 변환하지 않는다."""
import ctypes as C源代码
import hashlib
import json
from pathlib import Path

项目根 = Path(__file__).resolve().parents[1]
实现 = C源代码.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class 字符串(C源代码.Structure): _fields_ = [('数据',C源代码.c_void_p),('显示值',C源代码.c_uint)]
class 光标值(C源代码.Structure): _fields_ = [('种类值',C源代码.c_uint),('辅助值',C源代码.c_int),('数据',C源代码.c_void_p*3)]
class 位置(C源代码.Structure): _fields_ = [('数据',C源代码.c_void_p*2),('偏移值',C源代码.c_uint)]
def 函数(名称, 发回结果, *实参):
    条目值 = getattr(实现, 名称); 条目值.restype = 发回结果; 条目值.argtypes = list(实参); return 条目值
获取文本 = 函数('clang_getCString',C源代码.c_char_p,字符串)
释放文本 = 函数('clang_disposeString',None,字符串)
def 文本(值):
    结果 = (获取文本(值) or b'').decode('utf-8'); 释放文本(值); return 结果
获取名称 = 函数('clang_getCursorSpelling',字符串,光标值)
获取引用 = 函数('clang_getCursorReferenced',光标值,光标值)
获取位置 = 函数('clang_getCursorLocation',位置,光标值)
文件位置 = 函数('clang_getFileLocation',None,位置,C源代码.POINTER(C源代码.c_void_p),C源代码.POINTER(C源代码.c_uint),C源代码.POINTER(C源代码.c_uint),C源代码.POINTER(C源代码.c_uint))
文件条目名称 = 函数('clang_getFileName',字符串,C源代码.c_void_p)
唯一名称 = 函数('clang_getCursorUSR',字符串,光标值)
连接状态种类 = 函数('clang_getCursorLinkage',C源代码.c_uint,光标值)
已访问类型 = C源代码.CFUNCTYPE(C源代码.c_uint,光标值,光标值,C源代码.c_void_p)
访问值 = 函数('clang_visitChildren',C源代码.c_uint,光标值,已访问类型,C源代码.c_void_p)
生成 = 函数('clang_createIndex',C源代码.c_void_p,C源代码.c_int,C源代码.c_int)
分析值 = 函数('clang_parseTranslationUnit',C源代码.c_void_p,C源代码.c_void_p,C源代码.c_char_p,C源代码.POINTER(C源代码.c_char_p),C源代码.c_int,C源代码.c_void_p,C源代码.c_uint,C源代码.c_uint)
根值 = 函数('clang_getTranslationUnitCursor',光标值,C源代码.c_void_p)
结束程序 = 函数('clang_disposeTranslationUnit',None,C源代码.c_void_p)
诊断个数 = 函数('clang_getNumDiagnostics',C源代码.c_uint,C源代码.c_void_p)
获取诊断 = 函数('clang_getDiagnostic',C源代码.c_void_p,C源代码.c_void_p,C源代码.c_uint)
严重性值 = 函数('clang_getDiagnosticSeverity',C源代码.c_uint,C源代码.c_void_p)
诊断消息 = 函数('clang_getDiagnosticSpelling',字符串,C源代码.c_void_p)
释放诊断 = 函数('clang_disposeDiagnostic',None,C源代码.c_void_p)

def 位置索引(条目值):
    文件 = C源代码.c_void_p(); 行 = C源代码.c_uint(); 槽条目 = C源代码.c_uint(); 偏移值 = C源代码.c_uint()
    文件位置(获取位置(条目值),C源代码.byref(文件),C源代码.byref(行),C源代码.byref(槽条目),C源代码.byref(偏移值))
    return (文本(文件条目名称(文件)) if 文件 else '', 偏移值.value, 行.value)

def 执行命令():
    查找索引 = 生成(0,0); 声明列列表 = {}; 引用列列表 = []; 错误列 = []
    # 编译器工具.c는 内置 声明 없이 TinyCC 外部值 단일 翻译源代码 단위만 포함한다.
    # 外部值 선언을 内置 이름으로 세지 않으며, 实际数据 빌드에서는 继续处理 컴파일한다.
    自有文件 = {str(路径.resolve()) for 路径 in 项目根.rglob('*') if 路径.suffix in ('.c','.h','.cpp','.inc')
              and not set(路径.relative_to(项目根).parts)&{'build','dist','vendor','__pycache__'}
              and 路径.relative_to(项目根).as_posix() != 'C编译器/编译器工具.c'}
    公用值 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(项目根/'用户'),
          '-I'+str(项目根.parents[1]/'posix-kor/arm64-native/头文件'),'-I'+str(项目根/'build'),'-I'+str(项目根/'build/user'),
          '-I'+str(项目根/'build/remote'),'-I'+str(项目根/'vendor/bearssl/inc'),
          '-I'+str(项目根/'vendor/bearssl/src'),'-I'+str(项目根/'vendor/libassh/src'),
          '-I'+str(项目根/'vendor/lwip/src/include'),'-I'+str(项目根/'通信网络'),
          '-I'+str(项目根/'远程值'),'-I'+str(项目根/'C编译器')]
    for 路径 in sorted(Path(名称) for 名称 in 自有文件 if 名称.endswith(('.c','.cpp'))):
        实参 = 公用值 + ['-std=c++11' if 路径.suffix=='.cpp' else '-std=c11']
        if '通信网络' in 路径.parts: 实参 += ['-I'+str(项目根/'通信网络'),'-I'+str(项目根/'vendor/lwip/src/include')]
        if 'C编译器' in 路径.parts:
            实参 += ['-I'+str(项目根/'C编译器'),'-I'+str(项目根/'vendor/tinycc'),'-I'+str(项目根/'build/ccompiler'),
                    '-isystem',str(项目根.parent/'rpi4/build/rootfs/usr/include')]
        if 'Python桥接' in 路径.parts:
            实参 += ['-I'+str(项目根/'Python桥接'),'-I'+str(项目根/'build/micropython-1.24.1'),'-I'+str(项目根/'build/python'),'-isystem','/usr/include/newlib']
        if '远程值' in 路径.parts:
            实参 += ['-isystem', '/usr/include/newlib']
        if '分发值' in 路径.parts: 实参 += ['-D__JKOROS__=1']
        if 路径.name=='软件包.c': 实参 += ['-I'+str(项目根/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        组值 = (C源代码.c_char_p*len(实参))(*[条目值.encode() for 条目值 in 实参])
        翻译单位 = 分析值(查找索引,str(路径).encode(),组值,len(实参),None,0,1)
        for 编号 in range(诊断个数(翻译单位)):
            诊断值 = 获取诊断(翻译单位,编号)
            if 严重性值(诊断值)>=3: 错误列.append((str(路径.relative_to(项目根)),文本(诊断消息(诊断值))))
            释放诊断(诊断值)
        @已访问类型
        def 审查值(条目值,父值,数据):
            文件,偏移值,行 = 位置索引(条目值)
            if 文件 not in 自有文件: return 2 if 条目值.种类值==300 else 1
            词法用机器字 = 文本(获取名称(条目值))
            if not 词法用机器字 or any(ord(字符值)>127 for 字符值 in 词法用机器字): return 2
            if 条目值.种类值 in (2,3,4,5,6,7,8,9,10,20,21,501):
                唯一值 = 文本(唯一名称(条目值)) or 文件+':'+str(偏移值)
                声明列列表[唯一值] = {'文件':文件,'偏移值':偏移值,'行':行,'种类值':条目值.种类值,'名称':词法用机器字,'连接':连接状态种类(条目值)}
                引用列列表.append((文件,偏移值,词法用机器字,唯一值))
            else:
                引用 = 获取引用(条目值)
                引用文件,_,_ = 位置索引(引用)
                if 引用文件 in 自有文件:
                    唯一值 = 文本(唯一名称(引用)); 引用列列表.append((文件,偏移值,文本(获取名称(引用)),唯一值))
            return 2
        访问值(根值(翻译单位),审查值,None)
        结束程序(翻译单位)
    目的地址值 = 项目根/'build/한국어화/시언어분석.json'
    目的地址值.parent.mkdir(parents=True, exist_ok=True)
    散列值列列表 = {文件:hashlib.sha256(Path(文件).read_bytes()).hexdigest() for 文件 in sorted(自有文件)}
    目的地址值.write_text(json.dumps({'声明':声明列列表,'引用':引用列列表,'错误':错误列,'원문해시':散列值列列表},ensure_ascii=False,indent=2)+'\n')
    print('声明',len(声明列列表),'引用',len(引用列列表),'错误',len(错误列))
    for 错误 in 错误列: print(*错误)

if __name__=='__main__': 执行命令()
