#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char күрсәткеч_VALUE[16];uint16_t TYPE_категория,машина_TYPE;uint32_t 판번호;uint64_t кертү_балл,кушымта_Башлама_OFFSET,өлеш_Башлама_OFFSET;uint32_t 설정비트;uint16_t үлчәмен_үзгәртү,кушымта_Башлама_үлчәмен_үзгәртү,кушымта_Башлама_COUNT,өлеш_Башлама_үлчәмен_үзгәртү,өлеш_Башлама_COUNT,өлеш_исем_таблица; } Башлама_VALUE;
typedef struct {uint32_t TYPE_категория,설정비트;uint64_t OFFSET_VALUE,адрес,물리주소,파일영역크기,기억영역크기,맞춤;} өлеш_VALUE_32e9301f;
static unsigned char IMAGE[16384];
static int нәшер_итү_кертү(const char *исем){
    size_t элемент_COUNT;const unsigned char*원본자료=시언어출력(&элемент_COUNT);if(элемент_COUNT<sizeof(Башлама_VALUE))return -1;
    Башлама_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_категория!=2||실행머리.машина_TYPE!=183||실행머리.кушымта_Башлама_үлчәмен_үзгәртү!=sizeof(өлеш_VALUE_32e9301f)||!실행머리.кушымта_Башлама_COUNT||실행머리.кушымта_Башлама_COUNT>16||실행머리.кушымта_Башлама_OFFSET>элемент_COUNT||실행머리.кушымта_Башлама_COUNT*sizeof(өлеш_VALUE_32e9301f)>элемент_COUNT-실행머리.кушымта_Башлама_OFFSET)return -1;
    실행머리.кушымта_Башлама_OFFSET=sizeof(실행머리);실행머리.өлеш_Башлама_OFFSET=실행머리.өлеш_Башлама_COUNT=실행머리.өлеш_Башлама_үлчәмен_үзгәртү=실행머리.өлеш_исем_таблица=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.кушымта_Башлама_COUNT*sizeof(өлеш_VALUE_32e9301f),Киләсе_элемент=4096;unsigned char бит_Исемлек[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.кушымта_Башлама_COUNT;순번++){
        өлеш_VALUE_32e9301f мәгълүмат_урнаштыру;Башлама_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&мәгълүмат_урнаштыру,원본자료+원본.кушымта_Башлама_OFFSET+순번*sizeof(мәгълүмат_урнаштыру),sizeof(мәгълүмат_урнаштыру));
        if(мәгълүмат_урнаштыру.OFFSET_VALUE>элемент_COUNT||мәгълүмат_урнаштыру.파일영역크기>элемент_COUNT-мәгълүмат_урнаштыру.OFFSET_VALUE||мәгълүмат_урнаштыру.파일영역크기>мәгълүмат_урнаштыру.기억영역크기)return -1;
        if(мәгълүмат_урнаштыру.TYPE_категория==1){
            if((мәгълүмат_урнаштыру.설정비트&~7u)||!(мәгълүмат_урнаштыру.설정비트&4)||(мәгълүмат_урнаштыру.설정비트&3)==3||мәгълүмат_урнаштыру.адрес<0x02000000||мәгълүмат_урнаштыру.адрес>0x02c00000||мәгълүмат_урнаштыру.기억영역크기>0x02c00000-мәгълүмат_урнаштыру.адрес)return -1;
            if((мәгълүмат_урнаштыру.설정비트&1)&&실행머리.кертү_балл>=мәгълүмат_урнаштыру.адрес&&실행머리.кертү_балл-мәгълүмат_урнаштыру.адрес<мәгълүмат_урнаштыру.파일영역크기&&!(실행머리.кертү_балл&3))진입점정상=1;
            size_t 선행값=мәгълүмат_урнаштыру.адрес&4095,바이트들=мәгълүмат_урнаштыру.파일영역크기?선행값+мәгълүмат_урнаштыру.파일영역크기:0;
            if(Киләсе_элемент>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Киләсе_элемент){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Киләсе_элемент+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Киләсе_элемент+선행값,원본자료+мәгълүмат_урнаштыру.OFFSET_VALUE,мәгълүмат_урнаштыру.파일영역크기);
            мәгълүмат_урнаштыру.адрес-=선행값;мәгълүмат_урнаштыру.물리주소=мәгълүмат_урнаштыру.адрес;мәгълүмат_урнаштыру.기억영역크기+=선행값;мәгълүмат_урнаштыру.파일영역크기=바이트들;мәгълүмат_урнаштыру.OFFSET_VALUE=Киләсе_элемент;мәгълүмат_урнаштыру.맞춤=4096;
            for(uint64_t бит_VALUE=мәгълүмат_урнаштыру.адрес;бит_VALUE<мәгълүмат_урнаштыру.адрес+мәгълүмат_урнаштыру.기억영역크기;бит_VALUE+=4096){unsigned Эзләү_INDEX=(бит_VALUE-0x02000000)/4096;if(Эзләү_INDEX>=sizeof(бит_Исемлек)||бит_Исемлек[Эзләү_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}бит_Исемлек[Эзләү_INDEX]=1;}
            Киләсе_элемент+=(바이트들+4095)&~(size_t)4095;
        }else if(мәгълүмат_урнаштыру.TYPE_категория==4){if(мәгълүмат_урнаштыру.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+мәгълүмат_урнаштыру.OFFSET_VALUE,мәгълүмат_урнаштыру.파일영역크기);мәгълүмат_урнаштыру.OFFSET_VALUE=부가정보;부가정보+=мәгълүмат_урнаштыру.파일영역크기;}
        else if(мәгълүмат_урнаштыру.TYPE_категория!=0&&мәгълүмат_урнаштыру.TYPE_категория!=6&&мәгълүмат_урнаштыру.TYPE_категория!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.кушымта_Башлама_OFFSET+순번*sizeof(мәгълүмат_урнаштыру),&мәгълүмат_урнаштыру,sizeof(мәгълүмат_урнаштыру));
    }
    if(!진입점정상)return -1;
    intptr_t файл_дескриптор=사용자호출(3,(uintptr_t)исем,577,0600,0,0,0);if(файл_дескриптор<0){printf("cc: cannot create output file, error %d\n",(int)файл_дескриптор);return -1;}
    intptr_t 쓴수=사용자호출(1,файл_дескриптор,(uintptr_t)IMAGE,Киләсе_элемент,0,0,0);사용자호출(4,файл_дескриптор,0,0,0,0,0);return 쓴수==(intptr_t)Киләсе_элемент?0:-1;
}
int Start_кулланучы_кушымта(int ысул_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(ысул_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(ысул_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*юл_мәгълүмат=tcc_new();if(!юл_мәгълүмат)return 1;
    tcc_undefine_symbol(юл_мәгълүмат,"__linux__");tcc_undefine_symbol(юл_мәгълүмат,"__linux");tcc_undefine_symbol(юл_мәгълүмат,"linux");
    tcc_undefine_symbol(юл_мәгълүмат,"__unix__");tcc_undefine_symbol(юл_мәгълүмат,"__unix");tcc_undefine_symbol(юл_мәгълүмат,"unix");
    tcc_undefine_symbol(юл_мәгълүмат,"__STDC_HOSTED__");tcc_define_symbol(юл_мәгълүмат,"__STDC_HOSTED__","0");tcc_define_symbol(юл_мәгълүмат,"__JKOROS__","1");
    tcc_set_options(юл_мәгълүмат,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(юл_мәгълүмат,"/sdk/include");
    int 반환값=tcc_set_output_type(юл_мәгълүмат,TCC_OUTPUT_EXE);
    if(!반환값){if(ысул_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(юл_мәгълүмат,원본자료):-1;}else 반환값=tcc_add_file(юл_мәгълүмат,입력결과);}
    if(!반환값)반환값=tcc_add_file(юл_мәгълүмат,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(юл_мәгълүмат,"/sdk/lib/crt.o");
    if(!반환값&&ысул_MODE)반환값=tcc_add_file(юл_мәгълүмат,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(юл_мәгълүмат,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(юл_мәгълүмат,"/@cc-output");
    if(!반환값)반환값=нәшер_итү_кертү(출력결과);
    tcc_delete(юл_мәгълүмат);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(ысул_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
