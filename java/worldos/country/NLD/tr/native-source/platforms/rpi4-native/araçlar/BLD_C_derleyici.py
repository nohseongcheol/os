"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def açmak_C_derleyici(kök_yol, depo_yol, C_derleyici, bağlayıcı_araç, Yapılandırma_BITS, yürütmek_komut):
    KR_veri = kök_yol / 'build/ccompiler'; KR_veri.mkdir(exist_ok=True)
    원본자료 = kök_yol / 'C_derleyici'
    yukarı_akış = kök_yol / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    geliştirme_seti = kök_yol / 'vendor/sdk'
    if not (geliştirme_seti/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((geliştirme_seti/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    Yapılandırma_BITS = [Ayarlar_değer for Ayarlar_değer in Yapılandırma_BITS if Ayarlar_değer != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', yukarı_akış, '-I', kök_yol/'kullanıcı_alanı', '-I', KR_veri, '-isystem', geliştirme_seti/'usr/include']
    yürütmek_komut([C_derleyici]+Yapılandırma_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'IPL_Destek.c','-o',KR_veri/'crt.o'])
    yürütmek_komut([C_derleyici]+Yapılandırma_BITS+['-I',depo_yol/'posix-kor/arm64-native/bildirimler']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KR_veri/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+veri_konum.name,veri_konum) for veri_konum in sorted((depo_yol/'posix-kor/arm64-native/bildirimler').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+veri_konum.name,veri_konum) for veri_konum in sorted((yukarı_akış/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+veri_konum.name,veri_konum) for veri_konum in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',kök_yol/'build/user/start.o'),('/sdk/lib/crt.o',KR_veri/'crt.o'),('/sdk/lib/aot-runtime.o',KR_veri/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',kök_yol/'build/libposix-kor-user.a')]
    Başlık_değer=['typedef struct { const char *İsim; const unsigned char *veri; unsigned Boyut; } derleyici_kaynak;']
    for 순번,(_,yol) in enumerate(탑재자료):
        Başlık_değer.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in yol.read_bytes())))
    Başlık_değer.append('static const derleyici_kaynak derleyici_Kaynaklar[] = {')
    for 순번,(İsim,yol) in enumerate(탑재자료): Başlık_değer.append('{%s, 탑재자원_%d, %d},'%(json.dumps(İsim,ensure_ascii=False),순번,yol.stat().st_size))
    Başlık_değer.append('};');(KR_veri/'resources.h').write_text('\n'.join(Başlık_değer)+'\n',encoding='utf-8')
    hedef_Dosyalar=[]
    for İsim in ('derleyici_araç.c','CLR_Destek.c','çalıştır.c','미리번역.c','İade_köprü.S'):
        hedef_dosya=KR_veri/(Path(İsim).stem+'.o');hedef_Dosyalar.append(hedef_dosya)
        yürütmek_komut([C_derleyici]+Yapılandırma_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/İsim,'-o',hedef_dosya])
    çalıştırılabilir=kök_yol/'build/user/cc.elf'
    yürütmek_komut([bağlayıcı_araç,'--gc-sections','-T',kök_yol/'kullanıcı_alanı/bağlama_düzeni.ld','-z','max-page-size=4096','-o',çalıştırılabilir,
         kök_yol/'build/user/start.o',kök_yol/'build/user/runtime.o']+hedef_Dosyalar+
         [kök_yol/'build/user'/İsim for İsim in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
