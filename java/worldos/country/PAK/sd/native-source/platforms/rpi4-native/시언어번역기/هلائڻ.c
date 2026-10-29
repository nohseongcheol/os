#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char سڃاڻپ_ڪندڙ_قدر[16];uint16_t قسم_قسم,مشين_قسم;uint32_t 판번호;uint64_t داخلا_هنڌ,ائپ_هيڊر_آف_سيٽ,سيڪشن_هيڊر_آف_سيٽ;uint32_t 설정비트;uint16_t سائيز,ائپ_هيڊر_سائيز,프로그램머리개수,سيڪشن_هيڊر_سائيز,구역머리개수,سيڪشن_نالو_جدول; } هيڊر_قدر;
typedef struct {uint32_t قسم_قسم,설정비트;uint64_t آف_سيٽ_قدر,پتو,물리주소,파일영역크기,기억영역크기,맞춤;} حصو_قدر;
static unsigned char نقش[16384];
static int چاپيو_داخلا(const char *نالو){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(هيڊر_قدر))return -1;
    هيڊر_قدر 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.قسم_قسم!=2||실행머리.مشين_قسم!=183||실행머리.ائپ_هيڊر_سائيز!=sizeof(حصو_قدر)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.ائپ_هيڊر_آف_سيٽ>개수||실행머리.프로그램머리개수*sizeof(حصو_قدر)>개수-실행머리.ائپ_هيڊر_آف_سيٽ)return -1;
    실행머리.ائپ_هيڊر_آف_سيٽ=sizeof(실행머리);실행머리.سيڪشن_هيڊر_آف_سيٽ=실행머리.구역머리개수=실행머리.سيڪشن_هيڊر_سائيز=실행머리.سيڪشن_نالو_جدول=0;memcpy(نقش,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(حصو_قدر),다음=4096;unsigned char صفحو_فهرست[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        حصو_قدر 자료위치;هيڊر_قدر 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.ائپ_هيڊر_آف_سيٽ+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.آف_سيٽ_قدر>개수||자료위치.파일영역크기>개수-자료위치.آف_سيٽ_قدر||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.قسم_قسم==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.پتو<0x02000000||자료위치.پتو>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.پتو)return -1;
            if((자료위치.설정비트&1)&&실행머리.داخلا_هنڌ>=자료위치.پتو&&실행머리.داخلا_هنڌ-자료위치.پتو<자료위치.파일영역크기&&!(실행머리.داخلا_هنڌ&3))진입점정상=1;
            size_t 선행값=자료위치.پتو&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(نقش)||바이트들>sizeof(نقش)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(نقش));return -1;}
            if(바이트들)memcpy(نقش+다음+선행값,원본자료+자료위치.آف_سيٽ_قدر,자료위치.파일영역크기);
            자료위치.پتو-=선행값;자료위치.물리주소=자료위치.پتو;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.آف_سيٽ_قدر=다음;자료위치.맞춤=4096;
            for(uint64_t صفحو_قدر=자료위치.پتو;صفحو_قدر<자료위치.پتو+자료위치.기억영역크기;صفحو_قدر+=4096){unsigned 색인=(صفحو_قدر-0x02000000)/4096;if(색인>=sizeof(صفحو_فهرست)||صفحو_فهرست[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}صفحو_فهرست[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.قسم_قسم==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(نقش+부가정보,원본자료+자료위치.آف_سيٽ_قدر,자료위치.파일영역크기);자료위치.آف_سيٽ_قدر=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.قسم_قسم!=0&&자료위치.قسم_قسم!=6&&자료위치.قسم_قسم!=0x6474e551)return -1;
        memcpy(نقش+실행머리.ائپ_هيڊر_آف_سيٽ+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t فائل_منهن_ڏيڻ=사용자호출(3,(uintptr_t)نالو,577,0600,0,0,0);if(فائل_منهن_ڏيڻ<0){printf("cc: cannot create output file, error %d\n",(int)فائل_منهن_ڏيڻ);return -1;}
    intptr_t 쓴수=사용자호출(1,فائل_منهن_ڏيڻ,(uintptr_t)نقش,다음,0,0,0);사용자호출(4,فائل_منهن_ڏيڻ,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int شروع_صارف_ائپ(int طريقو_موڊ){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(طريقو_موڊ?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(طريقو_موڊ?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*اسٽرنگ_ڪوائف=tcc_new();if(!اسٽرنگ_ڪوائف)return 1;
    tcc_undefine_symbol(اسٽرنگ_ڪوائف,"__linux__");tcc_undefine_symbol(اسٽرنگ_ڪوائف,"__linux");tcc_undefine_symbol(اسٽرنگ_ڪوائف,"linux");
    tcc_undefine_symbol(اسٽرنگ_ڪوائف,"__unix__");tcc_undefine_symbol(اسٽرنگ_ڪوائف,"__unix");tcc_undefine_symbol(اسٽرنگ_ڪوائف,"unix");
    tcc_undefine_symbol(اسٽرنگ_ڪوائف,"__STDC_HOSTED__");tcc_define_symbol(اسٽرنگ_ڪوائف,"__STDC_HOSTED__","0");tcc_define_symbol(اسٽرنگ_ڪوائف,"__JKOROS__","1");
    tcc_set_options(اسٽرنگ_ڪوائف,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(اسٽرنگ_ڪوائف,"/sdk/include");
    int 반환값=tcc_set_output_type(اسٽرنگ_ڪوائف,TCC_OUTPUT_EXE);
    if(!반환값){if(طريقو_موڊ){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(اسٽرنگ_ڪوائف,원본자료):-1;}else 반환값=tcc_add_file(اسٽرنگ_ڪوائف,입력결과);}
    if(!반환값)반환값=tcc_add_file(اسٽرنگ_ڪوائف,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(اسٽرنگ_ڪوائف,"/sdk/lib/crt.o");
    if(!반환값&&طريقو_موڊ)반환값=tcc_add_file(اسٽرنگ_ڪوائف,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(اسٽرنگ_ڪوائف,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(اسٽرنگ_ڪوائف,"/@cc-output");
    if(!반환값)반환값=چاپيو_داخلا(출력결과);
    tcc_delete(اسٽرنگ_ڪوائف);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(طريقو_موڊ?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
