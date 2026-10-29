#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char شناخت_کرنڑ_آلا_قدر[16];uint16_t ٹائپ_کرو_زمرہ,مشین_ٹائپ_کرو;uint32_t 판번호;uint64_t داخلہ_مقام,ایپ_سرتحریر_آف_سیٹ,سیکشن_سرتحریر_آف_سیٹ;uint32_t 설정비트;uint16_t سائز,ایپ_سرتحریر_سائز,프로그램머리개수,سیکشن_سرتحریر_سائز,구역머리개수,سیکشن_ناں_جدول; } سرتحریر_قدر;
typedef struct {uint32_t ٹائپ_کرو_زمرہ,설정비트;uint64_t آف_سیٹ_قدر,پتا,물리주소,파일영역크기,기억영역크기,맞춤;} حصہ_قدر;
static unsigned char نقش[16384];
static int چھاپو_داخلہ(const char *ناں){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(سرتحریر_قدر))return -1;
    سرتحریر_قدر 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.ٹائپ_کرو_زمرہ!=2||실행머리.مشین_ٹائپ_کرو!=183||실행머리.ایپ_سرتحریر_سائز!=sizeof(حصہ_قدر)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.ایپ_سرتحریر_آف_سیٹ>개수||실행머리.프로그램머리개수*sizeof(حصہ_قدر)>개수-실행머리.ایپ_سرتحریر_آف_سیٹ)return -1;
    실행머리.ایپ_سرتحریر_آف_سیٹ=sizeof(실행머리);실행머리.سیکشن_سرتحریر_آف_سیٹ=실행머리.구역머리개수=실행머리.سیکشن_سرتحریر_سائز=실행머리.سیکشن_ناں_جدول=0;memcpy(نقش,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(حصہ_قدر),다음=4096;unsigned char صفحہ_فرست[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        حصہ_قدر 자료위치;سرتحریر_قدر 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.ایپ_سرتحریر_آف_سیٹ+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.آف_سیٹ_قدر>개수||자료위치.파일영역크기>개수-자료위치.آف_سیٹ_قدر||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.ٹائپ_کرو_زمرہ==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.پتا<0x02000000||자료위치.پتا>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.پتا)return -1;
            if((자료위치.설정비트&1)&&실행머리.داخلہ_مقام>=자료위치.پتا&&실행머리.داخلہ_مقام-자료위치.پتا<자료위치.파일영역크기&&!(실행머리.داخلہ_مقام&3))진입점정상=1;
            size_t 선행값=자료위치.پتا&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(نقش)||바이트들>sizeof(نقش)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(نقش));return -1;}
            if(바이트들)memcpy(نقش+다음+선행값,원본자료+자료위치.آف_سیٹ_قدر,자료위치.파일영역크기);
            자료위치.پتا-=선행값;자료위치.물리주소=자료위치.پتا;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.آف_سیٹ_قدر=다음;자료위치.맞춤=4096;
            for(uint64_t صفحہ_قدر=자료위치.پتا;صفحہ_قدر<자료위치.پتا+자료위치.기억영역크기;صفحہ_قدر+=4096){unsigned 색인=(صفحہ_قدر-0x02000000)/4096;if(색인>=sizeof(صفحہ_فرست)||صفحہ_فرست[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}صفحہ_فرست[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.ٹائپ_کرو_زمرہ==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(نقش+부가정보,원본자료+자료위치.آف_سیٹ_قدر,자료위치.파일영역크기);자료위치.آف_سیٹ_قدر=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.ٹائپ_کرو_زمرہ!=0&&자료위치.ٹائپ_کرو_زمرہ!=6&&자료위치.ٹائپ_کرو_زمرہ!=0x6474e551)return -1;
        memcpy(نقش+실행머리.ایپ_سرتحریر_آف_سیٹ+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t فائل_نبٹنا=사용자호출(3,(uintptr_t)ناں,577,0600,0,0,0);if(فائل_نبٹنا<0){printf("cc: cannot create output file, error %d\n",(int)فائل_نبٹنا);return -1;}
    intptr_t 쓴수=사용자호출(1,فائل_نبٹنا,(uintptr_t)نقش,다음,0,0,0);사용자호출(4,فائل_نبٹنا,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int مکھ_صارف_ایپ(int طریقہ_موڈ){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(طریقہ_موڈ?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(طریقہ_موڈ?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*سٹرنگ_کوائف=tcc_new();if(!سٹرنگ_کوائف)return 1;
    tcc_undefine_symbol(سٹرنگ_کوائف,"__linux__");tcc_undefine_symbol(سٹرنگ_کوائف,"__linux");tcc_undefine_symbol(سٹرنگ_کوائف,"linux");
    tcc_undefine_symbol(سٹرنگ_کوائف,"__unix__");tcc_undefine_symbol(سٹرنگ_کوائف,"__unix");tcc_undefine_symbol(سٹرنگ_کوائف,"unix");
    tcc_undefine_symbol(سٹرنگ_کوائف,"__STDC_HOSTED__");tcc_define_symbol(سٹرنگ_کوائف,"__STDC_HOSTED__","0");tcc_define_symbol(سٹرنگ_کوائف,"__JKOROS__","1");
    tcc_set_options(سٹرنگ_کوائف,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(سٹرنگ_کوائف,"/sdk/include");
    int 반환값=tcc_set_output_type(سٹرنگ_کوائف,TCC_OUTPUT_EXE);
    if(!반환값){if(طریقہ_موڈ){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(سٹرنگ_کوائف,원본자료):-1;}else 반환값=tcc_add_file(سٹرنگ_کوائف,입력결과);}
    if(!반환값)반환값=tcc_add_file(سٹرنگ_کوائف,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(سٹرنگ_کوائف,"/sdk/lib/crt.o");
    if(!반환값&&طریقہ_موڈ)반환값=tcc_add_file(سٹرنگ_کوائف,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(سٹرنگ_کوائف,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(سٹرنگ_کوائف,"/@cc-output");
    if(!반환값)반환값=چھاپو_داخلہ(출력결과);
    tcc_delete(سٹرنگ_کوائف);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(طریقہ_موڈ?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
