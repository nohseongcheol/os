#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VALUE[16];uint16_t TYPE_kategori,maskin_TYPE;uint32_t 판번호;uint64_t oppføring_p,app_hode_OFFSET,del_hode_OFFSET;uint32_t 설정비트;uint16_t Storleik,app_hode_endre_storleik,app_hode_COUNT,del_hode_endre_storleik,del_hode_COUNT,del_namn_tabell; } hode_VALUE;
typedef struct {uint32_t TYPE_kategori,설정비트;uint64_t OFFSET_VALUE,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int publiser_oppføring(const char *Namn){
    size_t vare_COUNT;const unsigned char*원본자료=시언어출력(&vare_COUNT);if(vare_COUNT<sizeof(hode_VALUE))return -1;
    hode_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_kategori!=2||실행머리.maskin_TYPE!=183||실행머리.app_hode_endre_storleik!=sizeof(segment_VALUE)||!실행머리.app_hode_COUNT||실행머리.app_hode_COUNT>16||실행머리.app_hode_OFFSET>vare_COUNT||실행머리.app_hode_COUNT*sizeof(segment_VALUE)>vare_COUNT-실행머리.app_hode_OFFSET)return -1;
    실행머리.app_hode_OFFSET=sizeof(실행머리);실행머리.del_hode_OFFSET=실행머리.del_hode_COUNT=실행머리.del_hode_endre_storleik=실행머리.del_namn_tabell=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.app_hode_COUNT*sizeof(segment_VALUE),Neste_vare=4096;unsigned char side_Liste[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.app_hode_COUNT;순번++){
        segment_VALUE data_plassere;hode_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_plassere,원본자료+원본.app_hode_OFFSET+순번*sizeof(data_plassere),sizeof(data_plassere));
        if(data_plassere.OFFSET_VALUE>vare_COUNT||data_plassere.파일영역크기>vare_COUNT-data_plassere.OFFSET_VALUE||data_plassere.파일영역크기>data_plassere.기억영역크기)return -1;
        if(data_plassere.TYPE_kategori==1){
            if((data_plassere.설정비트&~7u)||!(data_plassere.설정비트&4)||(data_plassere.설정비트&3)==3||data_plassere.ADDRESS<0x02000000||data_plassere.ADDRESS>0x02c00000||data_plassere.기억영역크기>0x02c00000-data_plassere.ADDRESS)return -1;
            if((data_plassere.설정비트&1)&&실행머리.oppføring_p>=data_plassere.ADDRESS&&실행머리.oppføring_p-data_plassere.ADDRESS<data_plassere.파일영역크기&&!(실행머리.oppføring_p&3))진입점정상=1;
            size_t 선행값=data_plassere.ADDRESS&4095,바이트들=data_plassere.파일영역크기?선행값+data_plassere.파일영역크기:0;
            if(Neste_vare>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Neste_vare){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Neste_vare+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Neste_vare+선행값,원본자료+data_plassere.OFFSET_VALUE,data_plassere.파일영역크기);
            data_plassere.ADDRESS-=선행값;data_plassere.물리주소=data_plassere.ADDRESS;data_plassere.기억영역크기+=선행값;data_plassere.파일영역크기=바이트들;data_plassere.OFFSET_VALUE=Neste_vare;data_plassere.맞춤=4096;
            for(uint64_t side_VALUE=data_plassere.ADDRESS;side_VALUE<data_plassere.ADDRESS+data_plassere.기억영역크기;side_VALUE+=4096){unsigned LOOKUP_INDEX=(side_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(side_Liste)||side_Liste[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}side_Liste[LOOKUP_INDEX]=1;}
            Neste_vare+=(바이트들+4095)&~(size_t)4095;
        }else if(data_plassere.TYPE_kategori==4){if(data_plassere.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+data_plassere.OFFSET_VALUE,data_plassere.파일영역크기);data_plassere.OFFSET_VALUE=부가정보;부가정보+=data_plassere.파일영역크기;}
        else if(data_plassere.TYPE_kategori!=0&&data_plassere.TYPE_kategori!=6&&data_plassere.TYPE_kategori!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.app_hode_OFFSET+순번*sizeof(data_plassere),&data_plassere,sizeof(data_plassere));
    }
    if(!진입점정상)return -1;
    intptr_t fil_handtak=사용자호출(3,(uintptr_t)Namn,577,0600,0,0,0);if(fil_handtak<0){printf("cc: cannot create output file, error %d\n",(int)fil_handtak);return -1;}
    intptr_t 쓴수=사용자호출(1,fil_handtak,(uintptr_t)IMAGE,Neste_vare,0,0,0);사용자호출(4,fil_handtak,0,0,0,0,0);return 쓴수==(intptr_t)Neste_vare?0:-1;
}
int START_brukar_app(int metode_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metode_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metode_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*streng_data=tcc_new();if(!streng_data)return 1;
    tcc_undefine_symbol(streng_data,"__linux__");tcc_undefine_symbol(streng_data,"__linux");tcc_undefine_symbol(streng_data,"linux");
    tcc_undefine_symbol(streng_data,"__unix__");tcc_undefine_symbol(streng_data,"__unix");tcc_undefine_symbol(streng_data,"unix");
    tcc_undefine_symbol(streng_data,"__STDC_HOSTED__");tcc_define_symbol(streng_data,"__STDC_HOSTED__","0");tcc_define_symbol(streng_data,"__JKOROS__","1");
    tcc_set_options(streng_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(streng_data,"/sdk/include");
    int 반환값=tcc_set_output_type(streng_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metode_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(streng_data,원본자료):-1;}else 반환값=tcc_add_file(streng_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/crt.o");
    if(!반환값&&metode_MODE)반환값=tcc_add_file(streng_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(streng_data,"/@cc-output");
    if(!반환값)반환값=publiser_oppføring(출력결과);
    tcc_delete(streng_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metode_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
