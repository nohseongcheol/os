#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *الرمز_البريدي_الناتج(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char معرف_قيمة[16];uint16_t نوع_فئة,جهاز_نوع;uint32_t رقم_الإصدار;uint64_t نقطة_الإدخال,تطبيق_عنوان_إزاحة,عنوان_المقطع_إزاحة;uint32_t تكوين_خدمة_النقل_الذكي_في_الخلفية;uint16_t حجم,تطبيق_عنوان_يغير_الحجم,프로그램머리개수,عنوان_المقطع_يغير_الحجم,구역머리개수,قسم_اسم_جدول; } عنوان_قيمة_4a42eba5;
typedef struct {uint32_t نوع_فئة,تكوين_خدمة_النقل_الذكي_في_الخلفية;uint64_t إزاحة_قيمة,عنوان,물리주소,파일영역크기,기억영역크기,맞춤;} قطاع_قيمة;
static unsigned char صورة[16384];
static int نشر_إدخال(const char *اسم){
    size_t 개수;const unsigned char*원본자료=الرمز_البريدي_الناتج(&개수);if(개수<sizeof(عنوان_قيمة_4a42eba5))return -1;
    عنوان_قيمة_4a42eba5 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.نوع_فئة!=2||실행머리.جهاز_نوع!=183||실행머리.تطبيق_عنوان_يغير_الحجم!=sizeof(قطاع_قيمة)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.تطبيق_عنوان_إزاحة>개수||실행머리.프로그램머리개수*sizeof(قطاع_قيمة)>개수-실행머리.تطبيق_عنوان_إزاحة)return -1;
    실행머리.تطبيق_عنوان_إزاحة=sizeof(실행머리);실행머리.عنوان_المقطع_إزاحة=실행머리.구역머리개수=실행머리.عنوان_المقطع_يغير_الحجم=실행머리.قسم_اسم_جدول=0;memcpy(صورة,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(قطاع_قيمة),التالي_عنصر=4096;unsigned char صفحة_قائمة[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        قطاع_قيمة بيانات_منصب;عنوان_قيمة_4a42eba5 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&بيانات_منصب,원본자료+원본.تطبيق_عنوان_إزاحة+순번*sizeof(بيانات_منصب),sizeof(بيانات_منصب));
        if(بيانات_منصب.إزاحة_قيمة>개수||بيانات_منصب.파일영역크기>개수-بيانات_منصب.إزاحة_قيمة||بيانات_منصب.파일영역크기>بيانات_منصب.기억영역크기)return -1;
        if(بيانات_منصب.نوع_فئة==1){
            if((بيانات_منصب.تكوين_خدمة_النقل_الذكي_في_الخلفية&~7u)||!(بيانات_منصب.تكوين_خدمة_النقل_الذكي_في_الخلفية&4)||(بيانات_منصب.تكوين_خدمة_النقل_الذكي_في_الخلفية&3)==3||بيانات_منصب.عنوان<0x02000000||بيانات_منصب.عنوان>0x02c00000||بيانات_منصب.기억영역크기>0x02c00000-بيانات_منصب.عنوان)return -1;
            if((بيانات_منصب.تكوين_خدمة_النقل_الذكي_في_الخلفية&1)&&실행머리.نقطة_الإدخال>=بيانات_منصب.عنوان&&실행머리.نقطة_الإدخال-بيانات_منصب.عنوان<بيانات_منصب.파일영역크기&&!(실행머리.نقطة_الإدخال&3))진입점정상=1;
            size_t 선행값=بيانات_منصب.عنوان&4095,바이트들=بيانات_منصب.파일영역크기?선행값+بيانات_منصب.파일영역크기:0;
            if(التالي_عنصر>sizeof(صورة)||바이트들>sizeof(صورة)-التالي_عنصر){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(التالي_عنصر+바이트들),(unsigned)sizeof(صورة));return -1;}
            if(바이트들)memcpy(صورة+التالي_عنصر+선행값,원본자료+بيانات_منصب.إزاحة_قيمة,بيانات_منصب.파일영역크기);
            بيانات_منصب.عنوان-=선행값;بيانات_منصب.물리주소=بيانات_منصب.عنوان;بيانات_منصب.기억영역크기+=선행값;بيانات_منصب.파일영역크기=바이트들;بيانات_منصب.إزاحة_قيمة=التالي_عنصر;بيانات_منصب.맞춤=4096;
            for(uint64_t صفحة_قيمة=بيانات_منصب.عنوان;صفحة_قيمة<بيانات_منصب.عنوان+بيانات_منصب.기억영역크기;صفحة_قيمة+=4096){unsigned البحث_فهرس=(صفحة_قيمة-0x02000000)/4096;if(البحث_فهرس>=sizeof(صفحة_قائمة)||صفحة_قائمة[البحث_فهرس]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}صفحة_قائمة[البحث_فهرس]=1;}
            التالي_عنصر+=(바이트들+4095)&~(size_t)4095;
        }else if(بيانات_منصب.نوع_فئة==4){if(بيانات_منصب.파일영역크기>4096-부가정보)return -1;memcpy(صورة+부가정보,원본자료+بيانات_منصب.إزاحة_قيمة,بيانات_منصب.파일영역크기);بيانات_منصب.إزاحة_قيمة=부가정보;부가정보+=بيانات_منصب.파일영역크기;}
        else if(بيانات_منصب.نوع_فئة!=0&&بيانات_منصب.نوع_فئة!=6&&بيانات_منصب.نوع_فئة!=0x6474e551)return -1;
        memcpy(صورة+실행머리.تطبيق_عنوان_إزاحة+순번*sizeof(بيانات_منصب),&بيانات_منصب,sizeof(بيانات_منصب));
    }
    if(!진입점정상)return -1;
    intptr_t ملف_مؤشر=사용자호출(3,(uintptr_t)اسم,577,0600,0,0,0);if(ملف_مؤشر<0){printf("cc: cannot create output file, error %d\n",(int)ملف_مؤشر);return -1;}
    intptr_t 쓴수=사용자호출(1,ملف_مؤشر,(uintptr_t)صورة,التالي_عنصر,0,0,0);사용자호출(4,ملف_مؤشر,0,0,0,0,0);return 쓴수==(intptr_t)التالي_عنصر?0:-1;
}
int بدء_مستخدم_تطبيق(int أسلوب_الوضع){
    char إدخال[256],선택항목[256],الناتج[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(أسلوب_الوضع?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)إدخال,sizeof(إدخال),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(إدخال,"--version")||!strcmp(إدخال,"-version"))){printf(أسلوب_الوضع?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)الناتج,sizeof(الناتج),0,0,0)<0)return 2;}
    if(!strcmp(إدخال,الناتج)){printf("cc: input and output must differ\n");return 2;}
    TCCState*سلسلة_بيانات=tcc_new();if(!سلسلة_بيانات)return 1;
    tcc_undefine_symbol(سلسلة_بيانات,"__linux__");tcc_undefine_symbol(سلسلة_بيانات,"__linux");tcc_undefine_symbol(سلسلة_بيانات,"linux");
    tcc_undefine_symbol(سلسلة_بيانات,"__unix__");tcc_undefine_symbol(سلسلة_بيانات,"__unix");tcc_undefine_symbol(سلسلة_بيانات,"unix");
    tcc_undefine_symbol(سلسلة_بيانات,"__STDC_HOSTED__");tcc_define_symbol(سلسلة_بيانات,"__STDC_HOSTED__","0");tcc_define_symbol(سلسلة_بيانات,"__JKOROS__","1");
    tcc_set_options(سلسلة_بيانات,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(سلسلة_بيانات,"/sdk/include");
    int 반환값=tcc_set_output_type(سلسلة_بيانات,TCC_OUTPUT_EXE);
    if(!반환값){if(أسلوب_الوضع){const char*원본자료=자바미리번역원문(إدخال);반환값=원본자료?tcc_compile_string(سلسلة_بيانات,원본자료):-1;}else 반환값=tcc_add_file(سلسلة_بيانات,إدخال);}
    if(!반환값)반환값=tcc_add_file(سلسلة_بيانات,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(سلسلة_بيانات,"/sdk/lib/crt.o");
    if(!반환값&&أسلوب_الوضع)반환값=tcc_add_file(سلسلة_بيانات,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(سلسلة_بيانات,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(سلسلة_بيانات,"/@cc-output");
    if(!반환값)반환값=نشر_إدخال(الناتج);
    tcc_delete(سلسلة_بيانات);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(أسلوب_الوضع?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",الناتج);return 0;
}
