"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def tạoTrìnhBiênDịchC(đườngDẫnGốcCây, đườngDẫnKhoNguồn, TrìnhBiênDịchC, côngCụTrìnhLiênKết, cácBitCấuHình, thựcThiLệnh):
    dữLiệuKếtQuả = đườngDẫnGốcCây / 'build/ccompiler'; dữLiệuKếtQuả.mkdir(exist_ok=True)
    dữLiệuNguyênBản = đườngDẫnGốcCây / 'TrìnhBiênDịchC'
    nguồnGốc = đườngDẫnGốcCây / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    bộCôngCụPhátTriển = đườngDẫnGốcCây / 'vendor/sdk'
    if not (bộCôngCụPhátTriển/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    thànhPhầnDựngSẵn = sorted((bộCôngCụPhátTriển/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not thànhPhầnDựngSẵn: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    cácBitCấuHình = [giáTrịCácThiếtLập for giáTrịCácThiếtLập in cácBitCấuHình if giáTrịCácThiếtLập != '-mgeneral-regs-only']
    cóBaoGồm = ['-I', dữLiệuNguyênBản, '-I', nguồnGốc, '-I', đườngDẫnGốcCây/'NgườiDùng', '-I', dữLiệuKếtQuả, '-isystem', bộCôngCụPhátTriển/'usr/include']
    thựcThiLệnh([TrìnhBiênDịchC]+cácBitCấuHình+['-ffunction-sections','-fdata-sections']+cóBaoGồm+['-c',dữLiệuNguyênBản/'hỗTrợLúcKhởiChạy.c','-o',dữLiệuKếtQuả/'crt.o'])
    thựcThiLệnh([TrìnhBiênDịchC]+cácBitCấuHình+['-I',đườngDẫnKhoNguồn/'posix-kor/arm64-native/TệpĐầuMục']+cóBaoGồm+['-c',dữLiệuNguyênBản/'môiTrườngChạyBiênDịchTrước.c','-o',dữLiệuKếtQuả/'aot-runtime.o'])
    tàiNguyênKèm = [('/sdk/include/'+vịTríDữLiệu.name,vịTríDữLiệu) for vịTríDữLiệu in sorted((đườngDẫnKhoNguồn/'posix-kor/arm64-native/TệpĐầuMục').glob('*.h'))]
    tàiNguyênKèm += [('/sdk/include/'+vịTríDữLiệu.name,vịTríDữLiệu) for vịTríDữLiệu in sorted((nguồnGốc/'include').glob('*.h'))]
    tàiNguyênKèm += [('/sdk/include/'+vịTríDữLiệu.name,vịTríDữLiệu) for vịTríDữLiệu in sorted((dữLiệuNguyênBản/'cácĐầuMụcPhátTriển').glob('*.h'))]
    tàiNguyênKèm += [('/sdk/lib/start.o',đườngDẫnGốcCây/'build/user/start.o'),('/sdk/lib/crt.o',dữLiệuKếtQuả/'crt.o'),('/sdk/lib/aot-runtime.o',dữLiệuKếtQuả/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',đườngDẫnGốcCây/'build/libposix-kor-user.a')]
    giáTrịĐầuMục=['typedef struct { const char *tên; const unsigned char *DữLiệu; unsigned cỡ; } tàiNguyênTrìnhBiênDịch;']
    for chỉSốThứBậc,(_,đườngDẫn) in enumerate(tàiNguyênKèm):
        giáTrịĐầuMục.append('static const unsigned char 탑재자원_%d[] = {%s};'%(chỉSốThứBậc,','.join(str(dữLiệuTạm) for dữLiệuTạm in đườngDẫn.read_bytes())))
    giáTrịĐầuMục.append('static const tàiNguyênTrìnhBiênDịch cácTàiNguyênTrìnhBiênDịch[] = {')
    for chỉSốThứBậc,(tên,đườngDẫn) in enumerate(tàiNguyênKèm): giáTrịĐầuMục.append('{%s, 탑재자원_%d, %d},'%(json.dumps(tên,ensure_ascii=False),chỉSốThứBậc,đườngDẫn.stat().st_size))
    giáTrịĐầuMục.append('};');(dữLiệuKếtQuả/'resources.h').write_text('\n'.join(giáTrịĐầuMục)+'\n',encoding='utf-8')
    cácTệpĐích=[]
    for tên in ('côngCụTrìnhBiênDịch.c','HỗTrợMôiTrườngChạy.c','chạy.c','thờiGianCủaTrước.c','cầuNốiTrảVề.S'):
        tệpĐích=dữLiệuKếtQuả/(Path(tên).stem+'.o');cácTệpĐích.append(tệpĐích)
        thựcThiLệnh([TrìnhBiênDịchC]+cácBitCấuHình+['-ffunction-sections','-fdata-sections']+cóBaoGồm+['-c',dữLiệuNguyênBản/tên,'-o',tệpĐích])
    tệpTệpThựcThi=đườngDẫnGốcCây/'build/user/cc.elf'
    thựcThiLệnh([côngCụTrìnhLiênKết,'--gc-sections','-T',đườngDẫnGốcCây/'NgườiDùng/BốTríLiênKết.ld','-z','max-page-size=4096','-o',tệpTệpThựcThi,
         đườngDẫnGốcCây/'build/user/start.o',đườngDẫnGốcCây/'build/user/runtime.o']+cácTệpĐích+
         [đườngDẫnGốcCây/'build/user'/tên for tên in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[thànhPhầnDựngSẵn[-1]])
