#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char tagakilala_VALUE[16];uint16_t TYPE_kategorya,machine_TYPE;uint32_t 판번호;uint64_t pagpasok_point,app_Header_OFFSET,seksiyon_Header_OFFSET;uint32_t kompigurasyon_Background_Intelligent_Transfer_Service;uint16_t sukat_82232621,app_Header_sukat,app_Header_COUNT,seksiyon_Header_sukat,seksiyon_Header_COUNT,seksiyon_pangalan_talahanayan; } Header_VALUE;
typedef struct {uint32_t TYPE_kategorya,kompigurasyon_Background_Intelligent_Transfer_Service;uint64_t OFFSET_VALUE,email,물리주소,파일영역크기,기억영역크기,맞춤;} bahagi_VALUE;
static unsigned char IMAGE[16384];
static int ilathala_pagpasok(const char *pangalan){
    size_t item_COUNT;const unsigned char*원본자료=시언어출력(&item_COUNT);if(item_COUNT<sizeof(Header_VALUE))return -1;
    Header_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_kategorya!=2||실행머리.machine_TYPE!=183||실행머리.app_Header_sukat!=sizeof(bahagi_VALUE)||!실행머리.app_Header_COUNT||실행머리.app_Header_COUNT>16||실행머리.app_Header_OFFSET>item_COUNT||실행머리.app_Header_COUNT*sizeof(bahagi_VALUE)>item_COUNT-실행머리.app_Header_OFFSET)return -1;
    실행머리.app_Header_OFFSET=sizeof(실행머리);실행머리.seksiyon_Header_OFFSET=실행머리.seksiyon_Header_COUNT=실행머리.seksiyon_Header_sukat=실행머리.seksiyon_pangalan_talahanayan=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.app_Header_COUNT*sizeof(bahagi_VALUE),Susunod_item=4096;unsigned char page_list[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.app_Header_COUNT;순번++){
        bahagi_VALUE data_posisyon;Header_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_posisyon,원본자료+원본.app_Header_OFFSET+순번*sizeof(data_posisyon),sizeof(data_posisyon));
        if(data_posisyon.OFFSET_VALUE>item_COUNT||data_posisyon.파일영역크기>item_COUNT-data_posisyon.OFFSET_VALUE||data_posisyon.파일영역크기>data_posisyon.기억영역크기)return -1;
        if(data_posisyon.TYPE_kategorya==1){
            if((data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service&~7u)||!(data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service&4)||(data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service&3)==3||data_posisyon.email<0x02000000||data_posisyon.email>0x02c00000||data_posisyon.기억영역크기>0x02c00000-data_posisyon.email)return -1;
            if((data_posisyon.kompigurasyon_Background_Intelligent_Transfer_Service&1)&&실행머리.pagpasok_point>=data_posisyon.email&&실행머리.pagpasok_point-data_posisyon.email<data_posisyon.파일영역크기&&!(실행머리.pagpasok_point&3))진입점정상=1;
            size_t 선행값=data_posisyon.email&4095,바이트들=data_posisyon.파일영역크기?선행값+data_posisyon.파일영역크기:0;
            if(Susunod_item>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Susunod_item){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Susunod_item+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Susunod_item+선행값,원본자료+data_posisyon.OFFSET_VALUE,data_posisyon.파일영역크기);
            data_posisyon.email-=선행값;data_posisyon.물리주소=data_posisyon.email;data_posisyon.기억영역크기+=선행값;data_posisyon.파일영역크기=바이트들;data_posisyon.OFFSET_VALUE=Susunod_item;data_posisyon.맞춤=4096;
            for(uint64_t page_VALUE=data_posisyon.email;page_VALUE<data_posisyon.email+data_posisyon.기억영역크기;page_VALUE+=4096){unsigned LOOKUP_INDEX=(page_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(page_list)||page_list[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}page_list[LOOKUP_INDEX]=1;}
            Susunod_item+=(바이트들+4095)&~(size_t)4095;
        }else if(data_posisyon.TYPE_kategorya==4){if(data_posisyon.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+data_posisyon.OFFSET_VALUE,data_posisyon.파일영역크기);data_posisyon.OFFSET_VALUE=부가정보;부가정보+=data_posisyon.파일영역크기;}
        else if(data_posisyon.TYPE_kategorya!=0&&data_posisyon.TYPE_kategorya!=6&&data_posisyon.TYPE_kategorya!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.app_Header_OFFSET+순번*sizeof(data_posisyon),&data_posisyon,sizeof(data_posisyon));
    }
    if(!진입점정상)return -1;
    intptr_t file_hawakán=사용자호출(3,(uintptr_t)pangalan,577,0600,0,0,0);if(file_hawakán<0){printf("cc: cannot create output file, error %d\n",(int)file_hawakán);return -1;}
    intptr_t 쓴수=사용자호출(1,file_hawakán,(uintptr_t)IMAGE,Susunod_item,0,0,0);사용자호출(4,file_hawakán,0,0,0,0,0);return 쓴수==(intptr_t)Susunod_item?0:-1;
}
int Start_gumagamit_app(int pamamaraan_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(pamamaraan_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(pamamaraan_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*string_data=tcc_new();if(!string_data)return 1;
    tcc_undefine_symbol(string_data,"__linux__");tcc_undefine_symbol(string_data,"__linux");tcc_undefine_symbol(string_data,"linux");
    tcc_undefine_symbol(string_data,"__unix__");tcc_undefine_symbol(string_data,"__unix");tcc_undefine_symbol(string_data,"unix");
    tcc_undefine_symbol(string_data,"__STDC_HOSTED__");tcc_define_symbol(string_data,"__STDC_HOSTED__","0");tcc_define_symbol(string_data,"__JKOROS__","1");
    tcc_set_options(string_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(string_data,"/sdk/include");
    int 반환값=tcc_set_output_type(string_data,TCC_OUTPUT_EXE);
    if(!반환값){if(pamamaraan_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(string_data,원본자료):-1;}else 반환값=tcc_add_file(string_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/crt.o");
    if(!반환값&&pamamaraan_MODE)반환값=tcc_add_file(string_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(string_data,"/@cc-output");
    if(!반환값)반환값=ilathala_pagpasok(출력결과);
    tcc_delete(string_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(pamamaraan_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
