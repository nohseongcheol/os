#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char ઓળખકર્તા_મૂલ્ય[16];uint16_t લખો_શ્રેણી,મશીન_લખો;uint32_t 판번호;uint64_t પ્રવેશ_બિંદુ,એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ,અનુભાગ_શીર્ષલેખ_ઑફસેટ;uint32_t 설정비트;uint16_t માપ,એપ્લિકેશન_શીર્ષલેખ_આકાર,프로그램머리개수,અનુભાગ_શીર્ષલેખ_આકાર,구역머리개수,અનુભાગ_નામ_કોષ્ટક; } શીર્ષલેખ_મૂલ્ય;
typedef struct {uint32_t લખો_શ્રેણી,설정비트;uint64_t ઑફસેટ_મૂલ્ય,સરનામું,물리주소,파일영역크기,기억영역크기,맞춤;} ભાગ_મૂલ્ય;
static unsigned char છબી[16384];
static int પ્રકાશિત_કરો_પ્રવેશ(const char *નામ){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(શીર્ષલેખ_મૂલ્ય))return -1;
    શીર્ષલેખ_મૂલ્ય 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.લખો_શ્રેણી!=2||실행머리.મશીન_લખો!=183||실행머리.એપ્લિકેશન_શીર્ષલેખ_આકાર!=sizeof(ભાગ_મૂલ્ય)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ>개수||실행머리.프로그램머리개수*sizeof(ભાગ_મૂલ્ય)>개수-실행머리.એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ)return -1;
    실행머리.એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ=sizeof(실행머리);실행머리.અનુભાગ_શીર્ષલેખ_ઑફસેટ=실행머리.구역머리개수=실행머리.અનુભાગ_શીર્ષલેખ_આકાર=실행머리.અનુભાગ_નામ_કોષ્ટક=0;memcpy(છબી,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(ભાગ_મૂલ્ય),આગલું_આઇટમ=4096;unsigned char પેજ_સૂચી[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        ભાગ_મૂલ્ય ડેટા_સ્થિતિ;શીર્ષલેખ_મૂલ્ય 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&ડેટા_સ્થિતિ,원본자료+원본.એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ+순번*sizeof(ડેટા_સ્થિતિ),sizeof(ડેટા_સ્થિતિ));
        if(ડેટા_સ્થિતિ.ઑફસેટ_મૂલ્ય>개수||ડેટા_સ્થિતિ.파일영역크기>개수-ડેટા_સ્થિતિ.ઑફસેટ_મૂલ્ય||ડેટા_સ્થિતિ.파일영역크기>ડેટા_સ્થિતિ.기억영역크기)return -1;
        if(ડેટા_સ્થિતિ.લખો_શ્રેણી==1){
            if((ડેટા_સ્થિતિ.설정비트&~7u)||!(ડેટા_સ્થિતિ.설정비트&4)||(ડેટા_સ્થિતિ.설정비트&3)==3||ડેટા_સ્થિતિ.સરનામું<0x02000000||ડેટા_સ્થિતિ.સરનામું>0x02c00000||ડેટા_સ્થિતિ.기억영역크기>0x02c00000-ડેટા_સ્થિતિ.સરનામું)return -1;
            if((ડેટા_સ્થિતિ.설정비트&1)&&실행머리.પ્રવેશ_બિંદુ>=ડેટા_સ્થિતિ.સરનામું&&실행머리.પ્રવેશ_બિંદુ-ડેટા_સ્થિતિ.સરનામું<ડેટા_સ્થિતિ.파일영역크기&&!(실행머리.પ્રવેશ_બિંદુ&3))진입점정상=1;
            size_t 선행값=ડેટા_સ્થિતિ.સરનામું&4095,바이트들=ડેટા_સ્થિતિ.파일영역크기?선행값+ડેટા_સ્થિતિ.파일영역크기:0;
            if(આગલું_આઇટમ>sizeof(છબી)||바이트들>sizeof(છબી)-આગલું_આઇટમ){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(આગલું_આઇટમ+바이트들),(unsigned)sizeof(છબી));return -1;}
            if(바이트들)memcpy(છબી+આગલું_આઇટમ+선행값,원본자료+ડેટા_સ્થિતિ.ઑફસેટ_મૂલ્ય,ડેટા_સ્થિતિ.파일영역크기);
            ડેટા_સ્થિતિ.સરનામું-=선행값;ડેટા_સ્થિતિ.물리주소=ડેટા_સ્થિતિ.સરનામું;ડેટા_સ્થિતિ.기억영역크기+=선행값;ડેટા_સ્થિતિ.파일영역크기=바이트들;ડેટા_સ્થિતિ.ઑફસેટ_મૂલ્ય=આગલું_આઇટમ;ડેટા_સ્થિતિ.맞춤=4096;
            for(uint64_t પેજ_મૂલ્ય=ડેટા_સ્થિતિ.સરનામું;પેજ_મૂલ્ય<ડેટા_સ્થિતિ.સરનામું+ડેટા_સ્થિતિ.기억영역크기;પેજ_મૂલ્ય+=4096){unsigned લુકઅપ_અનુક્રમણિકા=(પેજ_મૂલ્ય-0x02000000)/4096;if(લુકઅપ_અનુક્રમણિકા>=sizeof(પેજ_સૂચી)||પેજ_સૂચી[લુકઅપ_અનુક્રમણિકા]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}પેજ_સૂચી[લુકઅપ_અનુક્રમણિકા]=1;}
            આગલું_આઇટમ+=(바이트들+4095)&~(size_t)4095;
        }else if(ડેટા_સ્થિતિ.લખો_શ્રેણી==4){if(ડેટા_સ્થિતિ.파일영역크기>4096-부가정보)return -1;memcpy(છબી+부가정보,원본자료+ડેટા_સ્થિતિ.ઑફસેટ_મૂલ્ય,ડેટા_સ્થિતિ.파일영역크기);ડેટા_સ્થિતિ.ઑફસેટ_મૂલ્ય=부가정보;부가정보+=ડેટા_સ્થિતિ.파일영역크기;}
        else if(ડેટા_સ્થિતિ.લખો_શ્રેણી!=0&&ડેટા_સ્થિતિ.લખો_શ્રેણી!=6&&ડેટા_સ્થિતિ.લખો_શ્રેણી!=0x6474e551)return -1;
        memcpy(છબી+실행머리.એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ+순번*sizeof(ડેટા_સ્થિતિ),&ડેટા_સ્થિતિ,sizeof(ડેટા_સ્થિતિ));
    }
    if(!진입점정상)return -1;
    intptr_t ફાઇલ_હેન્ડલ=사용자호출(3,(uintptr_t)નામ,577,0600,0,0,0);if(ફાઇલ_હેન્ડલ<0){printf("cc: cannot create output file, error %d\n",(int)ફાઇલ_હેન્ડલ);return -1;}
    intptr_t 쓴수=사용자호출(1,ફાઇલ_હેન્ડલ,(uintptr_t)છબી,આગલું_આઇટમ,0,0,0);사용자호출(4,ફાઇલ_હેન્ડલ,0,0,0,0,0);return 쓴수==(intptr_t)આગલું_આઇટમ?0:-1;
}
int પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન(int પદ્ધતિ_મોડ){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(પદ્ધતિ_મોડ?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(પદ્ધતિ_મોડ?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*સ્ટ્રિંગ_ડેટા=tcc_new();if(!સ્ટ્રિંગ_ડેટા)return 1;
    tcc_undefine_symbol(સ્ટ્રિંગ_ડેટા,"__linux__");tcc_undefine_symbol(સ્ટ્રિંગ_ડેટા,"__linux");tcc_undefine_symbol(સ્ટ્રિંગ_ડેટા,"linux");
    tcc_undefine_symbol(સ્ટ્રિંગ_ડેટા,"__unix__");tcc_undefine_symbol(સ્ટ્રિંગ_ડેટા,"__unix");tcc_undefine_symbol(સ્ટ્રિંગ_ડેટા,"unix");
    tcc_undefine_symbol(સ્ટ્રિંગ_ડેટા,"__STDC_HOSTED__");tcc_define_symbol(સ્ટ્રિંગ_ડેટા,"__STDC_HOSTED__","0");tcc_define_symbol(સ્ટ્રિંગ_ડેટા,"__JKOROS__","1");
    tcc_set_options(સ્ટ્રિંગ_ડેટા,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(સ્ટ્રિંગ_ડેટા,"/sdk/include");
    int 반환값=tcc_set_output_type(સ્ટ્રિંગ_ડેટા,TCC_OUTPUT_EXE);
    if(!반환값){if(પદ્ધતિ_મોડ){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(સ્ટ્રિંગ_ડેટા,원본자료):-1;}else 반환값=tcc_add_file(સ્ટ્રિંગ_ડેટા,입력결과);}
    if(!반환값)반환값=tcc_add_file(સ્ટ્રિંગ_ડેટા,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(સ્ટ્રિંગ_ડેટા,"/sdk/lib/crt.o");
    if(!반환값&&પદ્ધતિ_મોડ)반환값=tcc_add_file(સ્ટ્રિંગ_ડેટા,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(સ્ટ્રિંગ_ડેટા,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(સ્ટ્રિંગ_ડેટા,"/@cc-output");
    if(!반환값)반환값=પ્રકાશિત_કરો_પ્રવેશ(출력결과);
    tcc_delete(સ્ટ્રિંગ_ડેટા);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(પદ્ધતિ_મોડ?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
