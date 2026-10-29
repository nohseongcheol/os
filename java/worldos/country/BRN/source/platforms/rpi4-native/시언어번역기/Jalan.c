#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char 식별자[16];uint16_t TYPE_bidang,mesin_TYPE;uint32_t nombor_versi;uint64_t titik_permulaan,aplikasi_Pengepala_Ofset,seksyen_Pengepala_Ofset;uint32_t konfigurasi_Background_Intelligent_Transfer_Service;uint16_t Saiz,aplikasi_Pengepala_saiz,aplikasi_Pengepala_COUNT,seksyen_Pengepala_saiz,seksyen_Pengepala_COUNT,seksyen_nama_jadual; } Pengepala_VALUE;
typedef struct {uint32_t TYPE_bidang,konfigurasi_Background_Intelligent_Transfer_Service;uint64_t Ofset_VALUE,e_mel,물리주소,파일영역크기,기억영역크기,맞춤;} segmen_VALUE;
static unsigned char imej[16384];
static int terbit_pemasukan(const char *Nama){
    size_t item_COUNT;const unsigned char*원본자료=시언어출력(&item_COUNT);if(item_COUNT<sizeof(Pengepala_VALUE))return -1;
    Pengepala_VALUE fail_boleh_laku_Pengepala;memcpy(&fail_boleh_laku_Pengepala,원본자료,sizeof(fail_boleh_laku_Pengepala));
    if(fail_boleh_laku_Pengepala.TYPE_bidang!=2||fail_boleh_laku_Pengepala.mesin_TYPE!=183||fail_boleh_laku_Pengepala.aplikasi_Pengepala_saiz!=sizeof(segmen_VALUE)||!fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT||fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT>16||fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset>item_COUNT||fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT*sizeof(segmen_VALUE)>item_COUNT-fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset)return -1;
    fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset=sizeof(fail_boleh_laku_Pengepala);fail_boleh_laku_Pengepala.seksyen_Pengepala_Ofset=fail_boleh_laku_Pengepala.seksyen_Pengepala_COUNT=fail_boleh_laku_Pengepala.seksyen_Pengepala_saiz=fail_boleh_laku_Pengepala.seksyen_nama_jadual=0;memcpy(imej,&fail_boleh_laku_Pengepala,sizeof(fail_boleh_laku_Pengepala));
    size_t 부가정보=sizeof(fail_boleh_laku_Pengepala)+fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT*sizeof(segmen_VALUE),Seterusnya_item=4096;unsigned char halaman_Senarai[3072]={0};int sah_titik_permulaan=0;
    for(unsigned 순번=0;순번<fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT;순번++){
        segmen_VALUE data_jawatan;Pengepala_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_jawatan,원본자료+원본.aplikasi_Pengepala_Ofset+순번*sizeof(data_jawatan),sizeof(data_jawatan));
        if(data_jawatan.Ofset_VALUE>item_COUNT||data_jawatan.파일영역크기>item_COUNT-data_jawatan.Ofset_VALUE||data_jawatan.파일영역크기>data_jawatan.기억영역크기)return -1;
        if(data_jawatan.TYPE_bidang==1){
            if((data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service&~7u)||!(data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service&4)||(data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service&3)==3||data_jawatan.e_mel<0x02000000||data_jawatan.e_mel>0x02c00000||data_jawatan.기억영역크기>0x02c00000-data_jawatan.e_mel)return -1;
            if((data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service&1)&&fail_boleh_laku_Pengepala.titik_permulaan>=data_jawatan.e_mel&&fail_boleh_laku_Pengepala.titik_permulaan-data_jawatan.e_mel<data_jawatan.파일영역크기&&!(fail_boleh_laku_Pengepala.titik_permulaan&3))sah_titik_permulaan=1;
            size_t 선행값=data_jawatan.e_mel&4095,바이트들=data_jawatan.파일영역크기?선행값+data_jawatan.파일영역크기:0;
            if(Seterusnya_item>sizeof(imej)||바이트들>sizeof(imej)-Seterusnya_item){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Seterusnya_item+바이트들),(unsigned)sizeof(imej));return -1;}
            if(바이트들)memcpy(imej+Seterusnya_item+선행값,원본자료+data_jawatan.Ofset_VALUE,data_jawatan.파일영역크기);
            data_jawatan.e_mel-=선행값;data_jawatan.물리주소=data_jawatan.e_mel;data_jawatan.기억영역크기+=선행값;data_jawatan.파일영역크기=바이트들;data_jawatan.Ofset_VALUE=Seterusnya_item;data_jawatan.맞춤=4096;
            for(uint64_t halaman_VALUE=data_jawatan.e_mel;halaman_VALUE<data_jawatan.e_mel+data_jawatan.기억영역크기;halaman_VALUE+=4096){unsigned Carian_INDEX=(halaman_VALUE-0x02000000)/4096;if(Carian_INDEX>=sizeof(halaman_Senarai)||halaman_Senarai[Carian_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}halaman_Senarai[Carian_INDEX]=1;}
            Seterusnya_item+=(바이트들+4095)&~(size_t)4095;
        }else if(data_jawatan.TYPE_bidang==4){if(data_jawatan.파일영역크기>4096-부가정보)return -1;memcpy(imej+부가정보,원본자료+data_jawatan.Ofset_VALUE,data_jawatan.파일영역크기);data_jawatan.Ofset_VALUE=부가정보;부가정보+=data_jawatan.파일영역크기;}
        else if(data_jawatan.TYPE_bidang!=0&&data_jawatan.TYPE_bidang!=6&&data_jawatan.TYPE_bidang!=0x6474e551)return -1;
        memcpy(imej+fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset+순번*sizeof(data_jawatan),&data_jawatan,sizeof(data_jawatan));
    }
    if(!sah_titik_permulaan)return -1;
    intptr_t fail_pemegang=사용자호출(3,(uintptr_t)Nama,577,0600,0,0,0);if(fail_pemegang<0){printf("cc: cannot create output file, error %d\n",(int)fail_pemegang);return -1;}
    intptr_t 쓴수=사용자호출(1,fail_pemegang,(uintptr_t)imej,Seterusnya_item,0,0,0);사용자호출(4,fail_pemegang,0,0,0,0,0);return 쓴수==(intptr_t)Seterusnya_item?0:-1;
}
int Mula_pengguna_aplikasi(int kaedah_mod){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(kaedah_mod?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(kaedah_mod?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*rentetan_data=tcc_new();if(!rentetan_data)return 1;
    tcc_undefine_symbol(rentetan_data,"__linux__");tcc_undefine_symbol(rentetan_data,"__linux");tcc_undefine_symbol(rentetan_data,"linux");
    tcc_undefine_symbol(rentetan_data,"__unix__");tcc_undefine_symbol(rentetan_data,"__unix");tcc_undefine_symbol(rentetan_data,"unix");
    tcc_undefine_symbol(rentetan_data,"__STDC_HOSTED__");tcc_define_symbol(rentetan_data,"__STDC_HOSTED__","0");tcc_define_symbol(rentetan_data,"__JKOROS__","1");
    tcc_set_options(rentetan_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(rentetan_data,"/sdk/include");
    int 반환값=tcc_set_output_type(rentetan_data,TCC_OUTPUT_EXE);
    if(!반환값){if(kaedah_mod){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(rentetan_data,원본자료):-1;}else 반환값=tcc_add_file(rentetan_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(rentetan_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(rentetan_data,"/sdk/lib/crt.o");
    if(!반환값&&kaedah_mod)반환값=tcc_add_file(rentetan_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(rentetan_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(rentetan_data,"/@cc-output");
    if(!반환값)반환값=terbit_pemasukan(출력결과);
    tcc_delete(rentetan_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(kaedah_mod?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
