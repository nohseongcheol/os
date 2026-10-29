#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char ناسێنەر_نرخ[16];uint16_t چاپکردن_پۆل,مەکینه_چاپکردن;uint32_t 판번호;uint64_t تێنووسین_خاڵ,بەرنامە_سەرپەڕ_ئۆفسێت,بەش_سەرپەڕ_ئۆفسێت;uint32_t 설정비트;uint16_t گۆڕینی_ئەندازە,بەرنامە_سەرپەڕ_گۆڕینی_ئەندازە,프로그램머리개수,بەش_سەرپەڕ_گۆڕینی_ئەندازە,구역머리개수,بەش_ناو_خشتە; } سەرپەڕ_نرخ;
typedef struct {uint32_t چاپکردن_پۆل,설정비트;uint64_t ئۆفسێت_نرخ,ناونیشان,물리주소,파일영역크기,기억영역크기,맞춤;} بەش_نرخ_32e9301f;
static unsigned char وێنە[16384];
static int بڵاو_کردن_تێنووسین(const char *ناو){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(سەرپەڕ_نرخ))return -1;
    سەرپەڕ_نرخ 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.چاپکردن_پۆل!=2||실행머리.مەکینه_چاپکردن!=183||실행머리.بەرنامە_سەرپەڕ_گۆڕینی_ئەندازە!=sizeof(بەش_نرخ_32e9301f)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.بەرنامە_سەرپەڕ_ئۆفسێت>개수||실행머리.프로그램머리개수*sizeof(بەش_نرخ_32e9301f)>개수-실행머리.بەرنامە_سەرپەڕ_ئۆفسێت)return -1;
    실행머리.بەرنامە_سەرپەڕ_ئۆفسێت=sizeof(실행머리);실행머리.بەش_سەرپەڕ_ئۆفسێت=실행머리.구역머리개수=실행머리.بەش_سەرپەڕ_گۆڕینی_ئەندازە=실행머리.بەش_ناو_خشتە=0;memcpy(وێنە,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(بەش_نرخ_32e9301f),다음=4096;unsigned char لاپەڕە_لیست[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        بەش_نرخ_32e9301f 자료위치;سەرپەڕ_نرخ 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.بەرنامە_سەرپەڕ_ئۆفسێت+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.ئۆفسێت_نرخ>개수||자료위치.파일영역크기>개수-자료위치.ئۆفسێت_نرخ||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.چاپکردن_پۆل==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.ناونیشان<0x02000000||자료위치.ناونیشان>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.ناونیشان)return -1;
            if((자료위치.설정비트&1)&&실행머리.تێنووسین_خاڵ>=자료위치.ناونیشان&&실행머리.تێنووسین_خاڵ-자료위치.ناونیشان<자료위치.파일영역크기&&!(실행머리.تێنووسین_خاڵ&3))진입점정상=1;
            size_t 선행값=자료위치.ناونیشان&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(وێنە)||바이트들>sizeof(وێنە)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(وێنە));return -1;}
            if(바이트들)memcpy(وێنە+다음+선행값,원본자료+자료위치.ئۆفسێت_نرخ,자료위치.파일영역크기);
            자료위치.ناونیشان-=선행값;자료위치.물리주소=자료위치.ناونیشان;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.ئۆفسێت_نرخ=다음;자료위치.맞춤=4096;
            for(uint64_t لاپەڕە_نرخ=자료위치.ناونیشان;لاپەڕە_نرخ<자료위치.ناونیشان+자료위치.기억영역크기;لاپەڕە_نرخ+=4096){unsigned 색인=(لاپەڕە_نرخ-0x02000000)/4096;if(색인>=sizeof(لاپەڕە_لیست)||لاپەڕە_لیست[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}لاپەڕە_لیست[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.چاپکردن_پۆل==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(وێنە+부가정보,원본자료+자료위치.ئۆفسێت_نرخ,자료위치.파일영역크기);자료위치.ئۆفسێت_نرخ=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.چاپکردن_پۆل!=0&&자료위치.چاپکردن_پۆل!=6&&자료위치.چاپکردن_پۆل!=0x6474e551)return -1;
        memcpy(وێنە+실행머리.بەرنامە_سەرپەڕ_ئۆفسێت+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t فایل_دەسک=사용자호출(3,(uintptr_t)ناو,577,0600,0,0,0);if(فایل_دەسک<0){printf("cc: cannot create output file, error %d\n",(int)فایل_دەسک);return -1;}
    intptr_t 쓴수=사용자호출(1,فایل_دەسک,(uintptr_t)وێنە,다음,0,0,0);사용자호출(4,فایل_دەسک,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int دەستپێك_بەکارهێنەر_بەرنامە(int ڕێگا_دۆخ){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(ڕێگا_دۆخ?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(ڕێگا_دۆخ?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*رست_دەیتا=tcc_new();if(!رست_دەیتا)return 1;
    tcc_undefine_symbol(رست_دەیتا,"__linux__");tcc_undefine_symbol(رست_دەیتا,"__linux");tcc_undefine_symbol(رست_دەیتا,"linux");
    tcc_undefine_symbol(رست_دەیتا,"__unix__");tcc_undefine_symbol(رست_دەیتا,"__unix");tcc_undefine_symbol(رست_دەیتا,"unix");
    tcc_undefine_symbol(رست_دەیتا,"__STDC_HOSTED__");tcc_define_symbol(رست_دەیتا,"__STDC_HOSTED__","0");tcc_define_symbol(رست_دەیتا,"__JKOROS__","1");
    tcc_set_options(رست_دەیتا,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(رست_دەیتا,"/sdk/include");
    int 반환값=tcc_set_output_type(رست_دەیتا,TCC_OUTPUT_EXE);
    if(!반환값){if(ڕێگا_دۆخ){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(رست_دەیتا,원본자료):-1;}else 반환값=tcc_add_file(رست_دەیتا,입력결과);}
    if(!반환값)반환값=tcc_add_file(رست_دەیتا,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(رست_دەیتا,"/sdk/lib/crt.o");
    if(!반환값&&ڕێگا_دۆخ)반환값=tcc_add_file(رست_دەیتا,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(رست_دەیتا,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(رست_دەیتا,"/@cc-output");
    if(!반환값)반환값=بڵاو_کردن_تێنووسین(출력결과);
    tcc_delete(رست_دەیتا);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(ڕێگا_دۆخ?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
