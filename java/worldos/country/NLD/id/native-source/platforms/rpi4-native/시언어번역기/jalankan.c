#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char pengidentifikasi_VALUE[16];uint16_t TYPE_area,mesin_TYPE;uint32_t nomor_versi;uint64_t entri_p,apl_judul_OFFSET,header_bagian_OFFSET;uint32_t konfigurasi_Background_Intelligent_Transfer_Service;uint16_t Ukuran,apl_judul_ukuran,apl_judul_COUNT,header_bagian_ukuran,header_bagian_COUNT,seksi_nama_tabel; } judul_VALUE;
typedef struct {uint32_t TYPE_area,konfigurasi_Background_Intelligent_Transfer_Service;uint64_t OFFSET_VALUE,surel,물리주소,파일영역크기,기억영역크기,맞춤;} segmen_VALUE;
static unsigned char foto[16384];
static int terbitkan_entri(const char *Nama_2){
    size_t item_COUNT;const unsigned char*원본자료=시언어출력(&item_COUNT);if(item_COUNT<sizeof(judul_VALUE))return -1;
    judul_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_area!=2||실행머리.mesin_TYPE!=183||실행머리.apl_judul_ukuran!=sizeof(segmen_VALUE)||!실행머리.apl_judul_COUNT||실행머리.apl_judul_COUNT>16||실행머리.apl_judul_OFFSET>item_COUNT||실행머리.apl_judul_COUNT*sizeof(segmen_VALUE)>item_COUNT-실행머리.apl_judul_OFFSET)return -1;
    실행머리.apl_judul_OFFSET=sizeof(실행머리);실행머리.header_bagian_OFFSET=실행머리.header_bagian_COUNT=실행머리.header_bagian_ukuran=실행머리.seksi_nama_tabel=0;memcpy(foto,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.apl_judul_COUNT*sizeof(segmen_VALUE),Berikutnya_item=4096;unsigned char halaman_Daftar[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.apl_judul_COUNT;순번++){
        segmen_VALUE data_posisi;judul_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_posisi,원본자료+원본.apl_judul_OFFSET+순번*sizeof(data_posisi),sizeof(data_posisi));
        if(data_posisi.OFFSET_VALUE>item_COUNT||data_posisi.파일영역크기>item_COUNT-data_posisi.OFFSET_VALUE||data_posisi.파일영역크기>data_posisi.기억영역크기)return -1;
        if(data_posisi.TYPE_area==1){
            if((data_posisi.konfigurasi_Background_Intelligent_Transfer_Service&~7u)||!(data_posisi.konfigurasi_Background_Intelligent_Transfer_Service&4)||(data_posisi.konfigurasi_Background_Intelligent_Transfer_Service&3)==3||data_posisi.surel<0x02000000||data_posisi.surel>0x02c00000||data_posisi.기억영역크기>0x02c00000-data_posisi.surel)return -1;
            if((data_posisi.konfigurasi_Background_Intelligent_Transfer_Service&1)&&실행머리.entri_p>=data_posisi.surel&&실행머리.entri_p-data_posisi.surel<data_posisi.파일영역크기&&!(실행머리.entri_p&3))진입점정상=1;
            size_t 선행값=data_posisi.surel&4095,바이트들=data_posisi.파일영역크기?선행값+data_posisi.파일영역크기:0;
            if(Berikutnya_item>sizeof(foto)||바이트들>sizeof(foto)-Berikutnya_item){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Berikutnya_item+바이트들),(unsigned)sizeof(foto));return -1;}
            if(바이트들)memcpy(foto+Berikutnya_item+선행값,원본자료+data_posisi.OFFSET_VALUE,data_posisi.파일영역크기);
            data_posisi.surel-=선행값;data_posisi.물리주소=data_posisi.surel;data_posisi.기억영역크기+=선행값;data_posisi.파일영역크기=바이트들;data_posisi.OFFSET_VALUE=Berikutnya_item;data_posisi.맞춤=4096;
            for(uint64_t halaman_VALUE=data_posisi.surel;halaman_VALUE<data_posisi.surel+data_posisi.기억영역크기;halaman_VALUE+=4096){unsigned LOOKUP_INDEX=(halaman_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(halaman_Daftar)||halaman_Daftar[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}halaman_Daftar[LOOKUP_INDEX]=1;}
            Berikutnya_item+=(바이트들+4095)&~(size_t)4095;
        }else if(data_posisi.TYPE_area==4){if(data_posisi.파일영역크기>4096-부가정보)return -1;memcpy(foto+부가정보,원본자료+data_posisi.OFFSET_VALUE,data_posisi.파일영역크기);data_posisi.OFFSET_VALUE=부가정보;부가정보+=data_posisi.파일영역크기;}
        else if(data_posisi.TYPE_area!=0&&data_posisi.TYPE_area!=6&&data_posisi.TYPE_area!=0x6474e551)return -1;
        memcpy(foto+실행머리.apl_judul_OFFSET+순번*sizeof(data_posisi),&data_posisi,sizeof(data_posisi));
    }
    if(!진입점정상)return -1;
    intptr_t file_handel=사용자호출(3,(uintptr_t)Nama_2,577,0600,0,0,0);if(file_handel<0){printf("cc: cannot create output file, error %d\n",(int)file_handel);return -1;}
    intptr_t 쓴수=사용자호출(1,file_handel,(uintptr_t)foto,Berikutnya_item,0,0,0);사용자호출(4,file_handel,0,0,0,0,0);return 쓴수==(intptr_t)Berikutnya_item?0:-1;
}
int Mulai_pengguna_apl(int metode_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metode_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metode_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*string_data=tcc_new();if(!string_data)return 1;
    tcc_undefine_symbol(string_data,"__linux__");tcc_undefine_symbol(string_data,"__linux");tcc_undefine_symbol(string_data,"linux");
    tcc_undefine_symbol(string_data,"__unix__");tcc_undefine_symbol(string_data,"__unix");tcc_undefine_symbol(string_data,"unix");
    tcc_undefine_symbol(string_data,"__STDC_HOSTED__");tcc_define_symbol(string_data,"__STDC_HOSTED__","0");tcc_define_symbol(string_data,"__JKOROS__","1");
    tcc_set_options(string_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(string_data,"/sdk/include");
    int 반환값=tcc_set_output_type(string_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metode_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(string_data,원본자료):-1;}else 반환값=tcc_add_file(string_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/crt.o");
    if(!반환값&&metode_MODE)반환값=tcc_add_file(string_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(string_data,"/@cc-output");
    if(!반환값)반환값=terbitkan_entri(출력결과);
    tcc_delete(string_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metode_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
