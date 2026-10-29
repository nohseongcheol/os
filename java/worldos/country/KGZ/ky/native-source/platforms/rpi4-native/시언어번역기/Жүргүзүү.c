#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char аныктагыч_маани[16];uint16_t түрү_категория,машина_түрү;uint32_t 판번호;uint64_t киргизме_жазуу_упай,програм_баш_аты_Жылбышуу,бөлүк_баш_аты_Жылбышуу;uint32_t 설정비트;uint16_t Өлчөмү,програм_баш_аты_көлөм,프로그램머리개수,бөлүк_баш_аты_көлөм,구역머리개수,бөлүк_аты_жадыбал; } баш_аты_маани;
typedef struct {uint32_t түрү_категория,설정비트;uint64_t Жылбышуу_маани,дарек,물리주소,파일영역크기,기억영역크기,맞춤;} сегмент_маани;
static unsigned char сүрөт[16384];
static int жарыялоо_киргизме_жазуу(const char *Аты){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(баш_аты_маани))return -1;
    баш_аты_маани 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.түрү_категория!=2||실행머리.машина_түрү!=183||실행머리.програм_баш_аты_көлөм!=sizeof(сегмент_маани)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.програм_баш_аты_Жылбышуу>개수||실행머리.프로그램머리개수*sizeof(сегмент_маани)>개수-실행머리.програм_баш_аты_Жылбышуу)return -1;
    실행머리.програм_баш_аты_Жылбышуу=sizeof(실행머리);실행머리.бөлүк_баш_аты_Жылбышуу=실행머리.구역머리개수=실행머리.бөлүк_баш_аты_көлөм=실행머리.бөлүк_аты_жадыбал=0;memcpy(сүрөт,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(сегмент_маани),다음=4096;unsigned char бет_Тизме[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        сегмент_маани 자료위치;баш_аты_маани 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.програм_баш_аты_Жылбышуу+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Жылбышуу_маани>개수||자료위치.파일영역크기>개수-자료위치.Жылбышуу_маани||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.түрү_категория==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.дарек<0x02000000||자료위치.дарек>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.дарек)return -1;
            if((자료위치.설정비트&1)&&실행머리.киргизме_жазуу_упай>=자료위치.дарек&&실행머리.киргизме_жазуу_упай-자료위치.дарек<자료위치.파일영역크기&&!(실행머리.киргизме_жазуу_упай&3))진입점정상=1;
            size_t 선행값=자료위치.дарек&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(сүрөт)||바이트들>sizeof(сүрөт)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(сүрөт));return -1;}
            if(바이트들)memcpy(сүрөт+다음+선행값,원본자료+자료위치.Жылбышуу_маани,자료위치.파일영역크기);
            자료위치.дарек-=선행값;자료위치.물리주소=자료위치.дарек;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Жылбышуу_маани=다음;자료위치.맞춤=4096;
            for(uint64_t бет_маани=자료위치.дарек;бет_маани<자료위치.дарек+자료위치.기억영역크기;бет_маани+=4096){unsigned 색인=(бет_маани-0x02000000)/4096;if(색인>=sizeof(бет_Тизме)||бет_Тизме[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}бет_Тизме[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.түрү_категория==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(сүрөт+부가정보,원본자료+자료위치.Жылбышуу_маани,자료위치.파일영역크기);자료위치.Жылбышуу_маани=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.түрү_категория!=0&&자료위치.түрү_категория!=6&&자료위치.түрү_категория!=0x6474e551)return -1;
        memcpy(сүрөт+실행머리.програм_баш_аты_Жылбышуу+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t файл_тутка=사용자호출(3,(uintptr_t)Аты,577,0600,0,0,0);if(файл_тутка<0){printf("cc: cannot create output file, error %d\n",(int)файл_тутка);return -1;}
    intptr_t 쓴수=사용자호출(1,файл_тутка,(uintptr_t)сүрөт,다음,0,0,0);사용자호출(4,файл_тутка,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Баштоо_колдонуучу_програм(int ыкма_режим){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(ыкма_режим?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(ыкма_режим?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*сап_берилмелер=tcc_new();if(!сап_берилмелер)return 1;
    tcc_undefine_symbol(сап_берилмелер,"__linux__");tcc_undefine_symbol(сап_берилмелер,"__linux");tcc_undefine_symbol(сап_берилмелер,"linux");
    tcc_undefine_symbol(сап_берилмелер,"__unix__");tcc_undefine_symbol(сап_берилмелер,"__unix");tcc_undefine_symbol(сап_берилмелер,"unix");
    tcc_undefine_symbol(сап_берилмелер,"__STDC_HOSTED__");tcc_define_symbol(сап_берилмелер,"__STDC_HOSTED__","0");tcc_define_symbol(сап_берилмелер,"__JKOROS__","1");
    tcc_set_options(сап_берилмелер,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(сап_берилмелер,"/sdk/include");
    int 반환값=tcc_set_output_type(сап_берилмелер,TCC_OUTPUT_EXE);
    if(!반환값){if(ыкма_режим){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(сап_берилмелер,원본자료):-1;}else 반환값=tcc_add_file(сап_берилмелер,입력결과);}
    if(!반환값)반환값=tcc_add_file(сап_берилмелер,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(сап_берилмелер,"/sdk/lib/crt.o");
    if(!반환값&&ыкма_режим)반환값=tcc_add_file(сап_берилмелер,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(сап_берилмелер,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(сап_берилмелер,"/@cc-output");
    if(!반환값)반환값=жарыялоо_киргизме_жазуу(출력결과);
    tcc_delete(сап_берилмелер);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(ыкма_режим?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
