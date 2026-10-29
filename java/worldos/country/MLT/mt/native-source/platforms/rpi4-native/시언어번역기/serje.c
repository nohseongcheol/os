#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikatur_VALUE[16];uint16_t TYPE_kategorija,kompjuter_TYPE;uint32_t 판번호;uint64_t entrata_punt,programm_Intestazzjoni_OFFSET,taqsima_Intestazzjoni_OFFSET;uint32_t 설정비트;uint16_t daqqas,programm_Intestazzjoni_daqqas,programm_Intestazzjoni_COUNT,taqsima_Intestazzjoni_daqqas,taqsima_Intestazzjoni_COUNT,taqsima_isem_tabella; } Intestazzjoni_VALUE;
typedef struct {uint32_t TYPE_kategorija,설정비트;uint64_t OFFSET_VALUE,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int ppubblika_entrata(const char *isem){
    size_t element_COUNT;const unsigned char*원본자료=시언어출력(&element_COUNT);if(element_COUNT<sizeof(Intestazzjoni_VALUE))return -1;
    Intestazzjoni_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_kategorija!=2||실행머리.kompjuter_TYPE!=183||실행머리.programm_Intestazzjoni_daqqas!=sizeof(segment_VALUE)||!실행머리.programm_Intestazzjoni_COUNT||실행머리.programm_Intestazzjoni_COUNT>16||실행머리.programm_Intestazzjoni_OFFSET>element_COUNT||실행머리.programm_Intestazzjoni_COUNT*sizeof(segment_VALUE)>element_COUNT-실행머리.programm_Intestazzjoni_OFFSET)return -1;
    실행머리.programm_Intestazzjoni_OFFSET=sizeof(실행머리);실행머리.taqsima_Intestazzjoni_OFFSET=실행머리.taqsima_Intestazzjoni_COUNT=실행머리.taqsima_Intestazzjoni_daqqas=실행머리.taqsima_isem_tabella=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.programm_Intestazzjoni_COUNT*sizeof(segment_VALUE),Li_Jmiss_element=4096;unsigned char paġna_Lista[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.programm_Intestazzjoni_COUNT;순번++){
        segment_VALUE data_pożizzjoni;Intestazzjoni_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_pożizzjoni,원본자료+원본.programm_Intestazzjoni_OFFSET+순번*sizeof(data_pożizzjoni),sizeof(data_pożizzjoni));
        if(data_pożizzjoni.OFFSET_VALUE>element_COUNT||data_pożizzjoni.파일영역크기>element_COUNT-data_pożizzjoni.OFFSET_VALUE||data_pożizzjoni.파일영역크기>data_pożizzjoni.기억영역크기)return -1;
        if(data_pożizzjoni.TYPE_kategorija==1){
            if((data_pożizzjoni.설정비트&~7u)||!(data_pożizzjoni.설정비트&4)||(data_pożizzjoni.설정비트&3)==3||data_pożizzjoni.ADDRESS<0x02000000||data_pożizzjoni.ADDRESS>0x02c00000||data_pożizzjoni.기억영역크기>0x02c00000-data_pożizzjoni.ADDRESS)return -1;
            if((data_pożizzjoni.설정비트&1)&&실행머리.entrata_punt>=data_pożizzjoni.ADDRESS&&실행머리.entrata_punt-data_pożizzjoni.ADDRESS<data_pożizzjoni.파일영역크기&&!(실행머리.entrata_punt&3))진입점정상=1;
            size_t 선행값=data_pożizzjoni.ADDRESS&4095,바이트들=data_pożizzjoni.파일영역크기?선행값+data_pożizzjoni.파일영역크기:0;
            if(Li_Jmiss_element>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Li_Jmiss_element){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Li_Jmiss_element+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Li_Jmiss_element+선행값,원본자료+data_pożizzjoni.OFFSET_VALUE,data_pożizzjoni.파일영역크기);
            data_pożizzjoni.ADDRESS-=선행값;data_pożizzjoni.물리주소=data_pożizzjoni.ADDRESS;data_pożizzjoni.기억영역크기+=선행값;data_pożizzjoni.파일영역크기=바이트들;data_pożizzjoni.OFFSET_VALUE=Li_Jmiss_element;data_pożizzjoni.맞춤=4096;
            for(uint64_t paġna_VALUE=data_pożizzjoni.ADDRESS;paġna_VALUE<data_pożizzjoni.ADDRESS+data_pożizzjoni.기억영역크기;paġna_VALUE+=4096){unsigned LOOKUP_INDEX=(paġna_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(paġna_Lista)||paġna_Lista[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}paġna_Lista[LOOKUP_INDEX]=1;}
            Li_Jmiss_element+=(바이트들+4095)&~(size_t)4095;
        }else if(data_pożizzjoni.TYPE_kategorija==4){if(data_pożizzjoni.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+data_pożizzjoni.OFFSET_VALUE,data_pożizzjoni.파일영역크기);data_pożizzjoni.OFFSET_VALUE=부가정보;부가정보+=data_pożizzjoni.파일영역크기;}
        else if(data_pożizzjoni.TYPE_kategorija!=0&&data_pożizzjoni.TYPE_kategorija!=6&&data_pożizzjoni.TYPE_kategorija!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.programm_Intestazzjoni_OFFSET+순번*sizeof(data_pożizzjoni),&data_pożizzjoni,sizeof(data_pożizzjoni));
    }
    if(!진입점정상)return -1;
    intptr_t fajl_handle=사용자호출(3,(uintptr_t)isem,577,0600,0,0,0);if(fajl_handle<0){printf("cc: cannot create output file, error %d\n",(int)fajl_handle);return -1;}
    intptr_t 쓴수=사용자호출(1,fajl_handle,(uintptr_t)IMAGE,Li_Jmiss_element,0,0,0);사용자호출(4,fajl_handle,0,0,0,0,0);return 쓴수==(intptr_t)Li_Jmiss_element?0:-1;
}
int Bidu_utent_programm(int metodu_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metodu_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metodu_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*string_data=tcc_new();if(!string_data)return 1;
    tcc_undefine_symbol(string_data,"__linux__");tcc_undefine_symbol(string_data,"__linux");tcc_undefine_symbol(string_data,"linux");
    tcc_undefine_symbol(string_data,"__unix__");tcc_undefine_symbol(string_data,"__unix");tcc_undefine_symbol(string_data,"unix");
    tcc_undefine_symbol(string_data,"__STDC_HOSTED__");tcc_define_symbol(string_data,"__STDC_HOSTED__","0");tcc_define_symbol(string_data,"__JKOROS__","1");
    tcc_set_options(string_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(string_data,"/sdk/include");
    int 반환값=tcc_set_output_type(string_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metodu_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(string_data,원본자료):-1;}else 반환값=tcc_add_file(string_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/crt.o");
    if(!반환값&&metodu_MODE)반환값=tcc_add_file(string_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(string_data,"/@cc-output");
    if(!반환값)반환값=ppubblika_entrata(출력결과);
    tcc_delete(string_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metodu_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
