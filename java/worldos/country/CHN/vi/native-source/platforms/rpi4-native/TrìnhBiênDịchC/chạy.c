#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "gọiThựcHiện.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *đầuRaC(size_t *);
extern const char *nguồnBiênDịchTrướcJava(const char *);
typedef struct { unsigned char giáTrịĐịnhDanh[16];uint16_t loạiMụcKiểu,kiểuMáy;uint32_t sốPhiênBản;uint64_t điểmMục,độLệchĐầuMụcChươngTrình,độLệchĐầuMụcMụcĐoạn;uint32_t cácBitCấuHình;uint16_t cỡ,cỡĐầuMụcChươngTrình,sốLượngĐầuMụcChươngTrình,cỡĐầuMụcMụcĐoạn,sốLượngĐầuMụcMụcĐoạn,bảngTraTênMụcĐoạn; } giáTrịĐầuMục;
typedef struct {uint32_t loạiMụcKiểu,cácBitCấuHình;uint64_t giáTrịĐộLệch,địaChỉ,địaChỉVậtLý,cỡVùngTệp,cỡVùngBộNhớ,ranhGiớiCănChỉnh;} giáTrịĐoạnVùng;
static unsigned char ảnh[16384];
static int mụcCôngBố(const char *tên){
    size_t sốLượngPhầnMục;const unsigned char*dữLiệuNguyênBản=đầuRaC(&sốLượngPhầnMục);if(sốLượngPhầnMục<sizeof(giáTrịĐầuMục))return -1;
    giáTrịĐầuMục đầuMụcTệpThựcThi;memcpy(&đầuMụcTệpThựcThi,dữLiệuNguyênBản,sizeof(đầuMụcTệpThựcThi));
    if(đầuMụcTệpThựcThi.loạiMụcKiểu!=2||đầuMụcTệpThựcThi.kiểuMáy!=183||đầuMụcTệpThựcThi.cỡĐầuMụcChươngTrình!=sizeof(giáTrịĐoạnVùng)||!đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình||đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình>16||đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình>sốLượngPhầnMục||đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình*sizeof(giáTrịĐoạnVùng)>sốLượngPhầnMục-đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình)return -1;
    đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình=sizeof(đầuMụcTệpThựcThi);đầuMụcTệpThựcThi.độLệchĐầuMụcMụcĐoạn=đầuMụcTệpThựcThi.sốLượngĐầuMụcMụcĐoạn=đầuMụcTệpThựcThi.cỡĐầuMụcMụcĐoạn=đầuMụcTệpThựcThi.bảngTraTênMụcĐoạn=0;memcpy(ảnh,&đầuMụcTệpThựcThi,sizeof(đầuMụcTệpThựcThi));
    size_t thôngTinPhụTrợ=sizeof(đầuMụcTệpThựcThi)+đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình*sizeof(giáTrịĐoạnVùng),phầnMụcKếTiếp=4096;unsigned char danhSáchTrang[3072]={0};int điểmMụcHợpLệ=0;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<đầuMụcTệpThựcThi.sốLượngĐầuMụcChươngTrình;chỉSốThứBậc++){
        giáTrịĐoạnVùng vịTríDữLiệu;giáTrịĐầuMục nguyênBản;memcpy(&nguyênBản,dữLiệuNguyênBản,sizeof(nguyênBản));memcpy(&vịTríDữLiệu,dữLiệuNguyênBản+nguyênBản.độLệchĐầuMụcChươngTrình+chỉSốThứBậc*sizeof(vịTríDữLiệu),sizeof(vịTríDữLiệu));
        if(vịTríDữLiệu.giáTrịĐộLệch>sốLượngPhầnMục||vịTríDữLiệu.cỡVùngTệp>sốLượngPhầnMục-vịTríDữLiệu.giáTrịĐộLệch||vịTríDữLiệu.cỡVùngTệp>vịTríDữLiệu.cỡVùngBộNhớ)return -1;
        if(vịTríDữLiệu.loạiMụcKiểu==1){
            if((vịTríDữLiệu.cácBitCấuHình&~7u)||!(vịTríDữLiệu.cácBitCấuHình&4)||(vịTríDữLiệu.cácBitCấuHình&3)==3||vịTríDữLiệu.địaChỉ<0x02000000||vịTríDữLiệu.địaChỉ>0x02c00000||vịTríDữLiệu.cỡVùngBộNhớ>0x02c00000-vịTríDữLiệu.địaChỉ)return -1;
            if((vịTríDữLiệu.cácBitCấuHình&1)&&đầuMụcTệpThựcThi.điểmMục>=vịTríDữLiệu.địaChỉ&&đầuMụcTệpThựcThi.điểmMục-vịTríDữLiệu.địaChỉ<vịTríDữLiệu.cỡVùngTệp&&!(đầuMụcTệpThựcThi.điểmMục&3))điểmMụcHợpLệ=1;
            size_t giáTrịLiềnTrước=vịTríDữLiệu.địaChỉ&4095,cácGiáTrịByte=vịTríDữLiệu.cỡVùngTệp?giáTrịLiềnTrước+vịTríDữLiệu.cỡVùngTệp:0;
            if(phầnMụcKếTiếp>sizeof(ảnh)||cácGiáTrịByte>sizeof(ảnh)-phầnMụcKếTiếp){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(phầnMụcKếTiếp+cácGiáTrịByte),(unsigned)sizeof(ảnh));return -1;}
            if(cácGiáTrịByte)memcpy(ảnh+phầnMụcKếTiếp+giáTrịLiềnTrước,dữLiệuNguyênBản+vịTríDữLiệu.giáTrịĐộLệch,vịTríDữLiệu.cỡVùngTệp);
            vịTríDữLiệu.địaChỉ-=giáTrịLiềnTrước;vịTríDữLiệu.địaChỉVậtLý=vịTríDữLiệu.địaChỉ;vịTríDữLiệu.cỡVùngBộNhớ+=giáTrịLiềnTrước;vịTríDữLiệu.cỡVùngTệp=cácGiáTrịByte;vịTríDữLiệu.giáTrịĐộLệch=phầnMụcKếTiếp;vịTríDữLiệu.ranhGiớiCănChỉnh=4096;
            for(uint64_t giáTrịTrang=vịTríDữLiệu.địaChỉ;giáTrịTrang<vịTríDữLiệu.địaChỉ+vịTríDữLiệu.cỡVùngBộNhớ;giáTrịTrang+=4096){unsigned chỉSốTraCứu=(giáTrịTrang-0x02000000)/4096;if(chỉSốTraCứu>=sizeof(danhSáchTrang)||danhSáchTrang[chỉSốTraCứu]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}danhSáchTrang[chỉSốTraCứu]=1;}
            phầnMụcKếTiếp+=(cácGiáTrịByte+4095)&~(size_t)4095;
        }else if(vịTríDữLiệu.loạiMụcKiểu==4){if(vịTríDữLiệu.cỡVùngTệp>4096-thôngTinPhụTrợ)return -1;memcpy(ảnh+thôngTinPhụTrợ,dữLiệuNguyênBản+vịTríDữLiệu.giáTrịĐộLệch,vịTríDữLiệu.cỡVùngTệp);vịTríDữLiệu.giáTrịĐộLệch=thôngTinPhụTrợ;thôngTinPhụTrợ+=vịTríDữLiệu.cỡVùngTệp;}
        else if(vịTríDữLiệu.loạiMụcKiểu!=0&&vịTríDữLiệu.loạiMụcKiểu!=6&&vịTríDữLiệu.loạiMụcKiểu!=0x6474e551)return -1;
        memcpy(ảnh+đầuMụcTệpThựcThi.độLệchĐầuMụcChươngTrình+chỉSốThứBậc*sizeof(vịTríDữLiệu),&vịTríDữLiệu,sizeof(vịTríDữLiệu));
    }
    if(!điểmMụcHợpLệ)return -1;
    intptr_t thẻXửLýTệp=gọiThựcHiệnNgườiDùng(3,(uintptr_t)tên,577,0600,0,0,0);if(thẻXửLýTệp<0){printf("cc: cannot create output file, error %d\n",(int)thẻXửLýTệp);return -1;}
    intptr_t đãGhiXong=gọiThựcHiệnNgườiDùng(1,thẻXửLýTệp,(uintptr_t)ảnh,phầnMụcKếTiếp,0,0,0);gọiThựcHiệnNgườiDùng(4,thẻXửLýTệp,0,0,0,0,0);return đãGhiXong==(intptr_t)phầnMụcKếTiếp?0:-1;
}
int bắtChạyChươngTrìnhNgườiDùng(int chếĐộPhươngThức){
    char đầuVào[256],mụcĐãChọn[256],đầuRa[256]="a.elf";
    int sốLượngCácĐốiSố=gọiThựcHiệnNgườiDùng(15,UINTPTR_MAX,0,0,0,0,0);
    if(sốLượngCácĐốiSố!=1&&sốLượngCácĐốiSố!=3){printf(chếĐộPhươngThức?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(gọiThựcHiệnNgườiDùng(15,0,(uintptr_t)đầuVào,sizeof(đầuVào),0,0,0)<0)return 2;
    if(sốLượngCácĐốiSố==1&&(!strcmp(đầuVào,"--version")||!strcmp(đầuVào,"-version"))){printf(chếĐộPhươngThức?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(sốLượngCácĐốiSố==3){gọiThựcHiệnNgườiDùng(15,1,(uintptr_t)mụcĐãChọn,sizeof(mụcĐãChọn),0,0,0);if(strcmp(mụcĐãChọn,"-o")||gọiThựcHiệnNgườiDùng(15,2,(uintptr_t)đầuRa,sizeof(đầuRa),0,0,0)<0)return 2;}
    if(!strcmp(đầuVào,đầuRa)){printf("cc: input and output must differ\n");return 2;}
    TCCState*dữLiệuChuỗi=tcc_new();if(!dữLiệuChuỗi)return 1;
    tcc_undefine_symbol(dữLiệuChuỗi,"__linux__");tcc_undefine_symbol(dữLiệuChuỗi,"__linux");tcc_undefine_symbol(dữLiệuChuỗi,"linux");
    tcc_undefine_symbol(dữLiệuChuỗi,"__unix__");tcc_undefine_symbol(dữLiệuChuỗi,"__unix");tcc_undefine_symbol(dữLiệuChuỗi,"unix");
    tcc_undefine_symbol(dữLiệuChuỗi,"__STDC_HOSTED__");tcc_define_symbol(dữLiệuChuỗi,"__STDC_HOSTED__","0");tcc_define_symbol(dữLiệuChuỗi,"__JKOROS__","1");
    tcc_set_options(dữLiệuChuỗi,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(dữLiệuChuỗi,"/sdk/include");
    int giáTrịĐãTrảVề=tcc_set_output_type(dữLiệuChuỗi,TCC_OUTPUT_EXE);
    if(!giáTrịĐãTrảVề){if(chếĐộPhươngThức){const char*dữLiệuNguyênBản=nguồnBiênDịchTrướcJava(đầuVào);giáTrịĐãTrảVề=dữLiệuNguyênBản?tcc_compile_string(dữLiệuChuỗi,dữLiệuNguyênBản):-1;}else giáTrịĐãTrảVề=tcc_add_file(dữLiệuChuỗi,đầuVào);}
    if(!giáTrịĐãTrảVề)giáTrịĐãTrảVề=tcc_add_file(dữLiệuChuỗi,"/sdk/lib/start.o");
    if(!giáTrịĐãTrảVề)giáTrịĐãTrảVề=tcc_add_file(dữLiệuChuỗi,"/sdk/lib/crt.o");
    if(!giáTrịĐãTrảVề&&chếĐộPhươngThức)giáTrịĐãTrảVề=tcc_add_file(dữLiệuChuỗi,"/sdk/lib/aot-runtime.o");
    if(!giáTrịĐãTrảVề)giáTrịĐãTrảVề=tcc_add_file(dữLiệuChuỗi,"/sdk/lib/libposix-kor-user.a");
    if(!giáTrịĐãTrảVề)giáTrịĐãTrảVề=tcc_output_file(dữLiệuChuỗi,"/@cc-output");
    if(!giáTrịĐãTrảVề)giáTrịĐãTrảVề=mụcCôngBố(đầuRa);
    tcc_delete(dữLiệuChuỗi);
    if(giáTrịĐãTrảVề){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(chếĐộPhươngThức?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",đầuRa);return 0;
}
