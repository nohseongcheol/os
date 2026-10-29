#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char 식별자[16];uint16_t 유형,기계유형;uint32_t 판번호;uint64_t ننوت_ټکى,프로그램머리변위,구역머리변위;uint32_t 설정비트;uint16_t کچ,프로그램머리크기,프로그램머리개수,구역머리크기,구역머리개수,구역이름표; } سرۍ_ارزښت;
typedef struct {uint32_t 유형,설정비트;uint64_t 변위,پته,물리주소,파일영역크기,기억영역크기,맞춤;} 구획;
static unsigned char انځور[16384];
static int خپرېدا_ننوت(const char *نوم){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(سرۍ_ارزښت))return -1;
    سرۍ_ارزښت 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.유형!=2||실행머리.기계유형!=183||실행머리.프로그램머리크기!=sizeof(구획)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.프로그램머리변위>개수||실행머리.프로그램머리개수*sizeof(구획)>개수-실행머리.프로그램머리변위)return -1;
    실행머리.프로그램머리변위=sizeof(실행머리);실행머리.구역머리변위=실행머리.구역머리개수=실행머리.구역머리크기=실행머리.구역이름표=0;memcpy(انځور,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(구획),다음=4096;unsigned char 쪽목록[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        구획 자료위치;سرۍ_ارزښت 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.프로그램머리변위+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.변위>개수||자료위치.파일영역크기>개수-자료위치.변위||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.유형==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.پته<0x02000000||자료위치.پته>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.پته)return -1;
            if((자료위치.설정비트&1)&&실행머리.ننوت_ټکى>=자료위치.پته&&실행머리.ننوت_ټکى-자료위치.پته<자료위치.파일영역크기&&!(실행머리.ننوت_ټکى&3))진입점정상=1;
            size_t 선행값=자료위치.پته&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(انځور)||바이트들>sizeof(انځور)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(انځور));return -1;}
            if(바이트들)memcpy(انځور+다음+선행값,원본자료+자료위치.변위,자료위치.파일영역크기);
            자료위치.پته-=선행값;자료위치.물리주소=자료위치.پته;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.변위=다음;자료위치.맞춤=4096;
            for(uint64_t مخ_ارزښت=자료위치.پته;مخ_ارزښت<자료위치.پته+자료위치.기억영역크기;مخ_ارزښت+=4096){unsigned 색인=(مخ_ارزښت-0x02000000)/4096;if(색인>=sizeof(쪽목록)||쪽목록[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}쪽목록[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.유형==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(انځور+부가정보,원본자료+자료위치.변위,자료위치.파일영역크기);자료위치.변위=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.유형!=0&&자료위치.유형!=6&&자료위치.유형!=0x6474e551)return -1;
        memcpy(انځور+실행머리.프로그램머리변위+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t دوتنه_لاستى=사용자호출(3,(uintptr_t)نوم,577,0600,0,0,0);if(دوتنه_لاستى<0){printf("cc: cannot create output file, error %d\n",(int)دوتنه_لاستى);return -1;}
    intptr_t 쓴수=사용자호출(1,دوتنه_لاستى,(uintptr_t)انځور,다음,0,0,0);사용자호출(4,دوتنه_لاستى,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int پيل_کارن_کاريال(int 방식){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(방식?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(방식?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*مزى_اومتوک=tcc_new();if(!مزى_اومتوک)return 1;
    tcc_undefine_symbol(مزى_اومتوک,"__linux__");tcc_undefine_symbol(مزى_اومتوک,"__linux");tcc_undefine_symbol(مزى_اومتوک,"linux");
    tcc_undefine_symbol(مزى_اومتوک,"__unix__");tcc_undefine_symbol(مزى_اومتوک,"__unix");tcc_undefine_symbol(مزى_اومتوک,"unix");
    tcc_undefine_symbol(مزى_اومتوک,"__STDC_HOSTED__");tcc_define_symbol(مزى_اومتوک,"__STDC_HOSTED__","0");tcc_define_symbol(مزى_اومتوک,"__JKOROS__","1");
    tcc_set_options(مزى_اومتوک,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(مزى_اومتوک,"/sdk/include");
    int 반환값=tcc_set_output_type(مزى_اومتوک,TCC_OUTPUT_EXE);
    if(!반환값){if(방식){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(مزى_اومتوک,원본자료):-1;}else 반환값=tcc_add_file(مزى_اومتوک,입력결과);}
    if(!반환값)반환값=tcc_add_file(مزى_اومتوک,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(مزى_اومتوک,"/sdk/lib/crt.o");
    if(!반환값&&방식)반환값=tcc_add_file(مزى_اومتوک,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(مزى_اومتوک,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(مزى_اومتوک,"/@cc-output");
    if(!반환값)반환값=خپرېدا_ننوت(출력결과);
    tcc_delete(مزى_اومتوک);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(방식?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
