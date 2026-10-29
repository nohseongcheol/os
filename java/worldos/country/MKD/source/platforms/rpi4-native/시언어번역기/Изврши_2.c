#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char идентификатор_VALUE[16];uint16_t TYPE_област,машина_TYPE;uint32_t број_на_верзија;uint64_t внес_поен,програма_Заглавие_OFFSET,секција_Заглавие_OFFSET;uint32_t конфигурација_Услуга_за_интелигентен_пренос_во_заднина;uint16_t Големина,програма_Заглавие_големина,програма_Заглавие_COUNT,секција_Заглавие_големина,секција_Заглавие_COUNT,секција_име_табела; } Заглавие_VALUE;
typedef struct {uint32_t TYPE_област,конфигурација_Услуга_за_интелигентен_пренос_во_заднина;uint64_t OFFSET_VALUE,адреса,물리주소,파일영역크기,기억영역크기,맞춤;} сегмент_VALUE;
static unsigned char IMAGE[16384];
static int објави_внес(const char *Име){
    size_t ставка_COUNT;const unsigned char*원본자료=시언어출력(&ставка_COUNT);if(ставка_COUNT<sizeof(Заглавие_VALUE))return -1;
    Заглавие_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_област!=2||실행머리.машина_TYPE!=183||실행머리.програма_Заглавие_големина!=sizeof(сегмент_VALUE)||!실행머리.програма_Заглавие_COUNT||실행머리.програма_Заглавие_COUNT>16||실행머리.програма_Заглавие_OFFSET>ставка_COUNT||실행머리.програма_Заглавие_COUNT*sizeof(сегмент_VALUE)>ставка_COUNT-실행머리.програма_Заглавие_OFFSET)return -1;
    실행머리.програма_Заглавие_OFFSET=sizeof(실행머리);실행머리.секција_Заглавие_OFFSET=실행머리.секција_Заглавие_COUNT=실행머리.секција_Заглавие_големина=실행머리.секција_име_табела=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.програма_Заглавие_COUNT*sizeof(сегмент_VALUE),Следно_ставка=4096;unsigned char страница_Список[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.програма_Заглавие_COUNT;순번++){
        сегмент_VALUE податоци_позиционирање;Заглавие_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&податоци_позиционирање,원본자료+원본.програма_Заглавие_OFFSET+순번*sizeof(податоци_позиционирање),sizeof(податоци_позиционирање));
        if(податоци_позиционирање.OFFSET_VALUE>ставка_COUNT||податоци_позиционирање.파일영역크기>ставка_COUNT-податоци_позиционирање.OFFSET_VALUE||податоци_позиционирање.파일영역크기>податоци_позиционирање.기억영역크기)return -1;
        if(податоци_позиционирање.TYPE_област==1){
            if((податоци_позиционирање.конфигурација_Услуга_за_интелигентен_пренос_во_заднина&~7u)||!(податоци_позиционирање.конфигурација_Услуга_за_интелигентен_пренос_во_заднина&4)||(податоци_позиционирање.конфигурација_Услуга_за_интелигентен_пренос_во_заднина&3)==3||податоци_позиционирање.адреса<0x02000000||податоци_позиционирање.адреса>0x02c00000||податоци_позиционирање.기억영역크기>0x02c00000-податоци_позиционирање.адреса)return -1;
            if((податоци_позиционирање.конфигурација_Услуга_за_интелигентен_пренос_во_заднина&1)&&실행머리.внес_поен>=податоци_позиционирање.адреса&&실행머리.внес_поен-податоци_позиционирање.адреса<податоци_позиционирање.파일영역크기&&!(실행머리.внес_поен&3))진입점정상=1;
            size_t 선행값=податоци_позиционирање.адреса&4095,바이트들=податоци_позиционирање.파일영역크기?선행값+податоци_позиционирање.파일영역크기:0;
            if(Следно_ставка>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Следно_ставка){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Следно_ставка+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Следно_ставка+선행값,원본자료+податоци_позиционирање.OFFSET_VALUE,податоци_позиционирање.파일영역크기);
            податоци_позиционирање.адреса-=선행값;податоци_позиционирање.물리주소=податоци_позиционирање.адреса;податоци_позиционирање.기억영역크기+=선행값;податоци_позиционирање.파일영역크기=바이트들;податоци_позиционирање.OFFSET_VALUE=Следно_ставка;податоци_позиционирање.맞춤=4096;
            for(uint64_t страница_VALUE=податоци_позиционирање.адреса;страница_VALUE<податоци_позиционирање.адреса+податоци_позиционирање.기억영역크기;страница_VALUE+=4096){unsigned LOOKUP_INDEX=(страница_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(страница_Список)||страница_Список[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}страница_Список[LOOKUP_INDEX]=1;}
            Следно_ставка+=(바이트들+4095)&~(size_t)4095;
        }else if(податоци_позиционирање.TYPE_област==4){if(податоци_позиционирање.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+податоци_позиционирање.OFFSET_VALUE,податоци_позиционирање.파일영역크기);податоци_позиционирање.OFFSET_VALUE=부가정보;부가정보+=податоци_позиционирање.파일영역크기;}
        else if(податоци_позиционирање.TYPE_област!=0&&податоци_позиционирање.TYPE_област!=6&&податоци_позиционирање.TYPE_област!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.програма_Заглавие_OFFSET+순번*sizeof(податоци_позиционирање),&податоци_позиционирање,sizeof(податоци_позиционирање));
    }
    if(!진입점정상)return -1;
    intptr_t датотека_рачка=사용자호출(3,(uintptr_t)Име,577,0600,0,0,0);if(датотека_рачка<0){printf("cc: cannot create output file, error %d\n",(int)датотека_рачка);return -1;}
    intptr_t 쓴수=사용자호출(1,датотека_рачка,(uintptr_t)IMAGE,Следно_ставка,0,0,0);사용자호출(4,датотека_рачка,0,0,0,0,0);return 쓴수==(intptr_t)Следно_ставка?0:-1;
}
int Start_корисник_програма(int метод_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(метод_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(метод_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*низа_податоци=tcc_new();if(!низа_податоци)return 1;
    tcc_undefine_symbol(низа_податоци,"__linux__");tcc_undefine_symbol(низа_податоци,"__linux");tcc_undefine_symbol(низа_податоци,"linux");
    tcc_undefine_symbol(низа_податоци,"__unix__");tcc_undefine_symbol(низа_податоци,"__unix");tcc_undefine_symbol(низа_податоци,"unix");
    tcc_undefine_symbol(низа_податоци,"__STDC_HOSTED__");tcc_define_symbol(низа_податоци,"__STDC_HOSTED__","0");tcc_define_symbol(низа_податоци,"__JKOROS__","1");
    tcc_set_options(низа_податоци,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(низа_податоци,"/sdk/include");
    int 반환값=tcc_set_output_type(низа_податоци,TCC_OUTPUT_EXE);
    if(!반환값){if(метод_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(низа_податоци,원본자료):-1;}else 반환값=tcc_add_file(низа_податоци,입력결과);}
    if(!반환값)반환값=tcc_add_file(низа_податоци,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(низа_податоци,"/sdk/lib/crt.o");
    if(!반환값&&метод_MODE)반환값=tcc_add_file(низа_податоци,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(низа_податоци,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(низа_податоци,"/@cc-output");
    if(!반환값)반환값=објави_внес(출력결과);
    tcc_delete(низа_податоци);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(метод_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
