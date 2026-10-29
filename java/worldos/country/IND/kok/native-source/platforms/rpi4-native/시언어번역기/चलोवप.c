#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char वळखुपी_मोल[16];uint16_t TYPE_वर्ग,यंत्र_TYPE;uint32_t 판번호;uint64_t प्रवेश_पॉयंट,एप्लिकेशन_माथाळो_ऑफसॅट,विभाग_माथाळो_ऑफसॅट;uint32_t 설정비트;uint16_t आवाठ,एप्लिकेशन_माथाळो_आवाठ,एप्लिकेशन_माथाळो_COUNT,विभाग_माथाळो_आवाठ,विभाग_माथाळो_COUNT,विभाग_नांव_तकटो; } माथाळो_मोल;
typedef struct {uint32_t TYPE_वर्ग,설정비트;uint64_t ऑफसॅट_मोल,नामो,물리주소,파일영역크기,기억영역크기,맞춤;} सेगमेंट_मोल;
static unsigned char IMAGE[16384];
static int उजवाडावचें_प्रवेश(const char *नांव){
    size_t आयटम_COUNT;const unsigned char*원본자료=시언어출력(&आयटम_COUNT);if(आयटम_COUNT<sizeof(माथाळो_मोल))return -1;
    माथाळो_मोल 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_वर्ग!=2||실행머리.यंत्र_TYPE!=183||실행머리.एप्लिकेशन_माथाळो_आवाठ!=sizeof(सेगमेंट_मोल)||!실행머리.एप्लिकेशन_माथाळो_COUNT||실행머리.एप्लिकेशन_माथाळो_COUNT>16||실행머리.एप्लिकेशन_माथाळो_ऑफसॅट>आयटम_COUNT||실행머리.एप्लिकेशन_माथाळो_COUNT*sizeof(सेगमेंट_मोल)>आयटम_COUNT-실행머리.एप्लिकेशन_माथाळो_ऑफसॅट)return -1;
    실행머리.एप्लिकेशन_माथाळो_ऑफसॅट=sizeof(실행머리);실행머리.विभाग_माथाळो_ऑफसॅट=실행머리.विभाग_माथाळो_COUNT=실행머리.विभाग_माथाळो_आवाठ=실행머리.विभाग_नांव_तकटो=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.एप्लिकेशन_माथाळो_COUNT*sizeof(सेगमेंट_मोल),फुडलें_आयटम=4096;unsigned char पान_सुची[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.एप्लिकेशन_माथाळो_COUNT;순번++){
        सेगमेंट_मोल डेटा_स्थिती;माथाळो_मोल 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&डेटा_स्थिती,원본자료+원본.एप्लिकेशन_माथाळो_ऑफसॅट+순번*sizeof(डेटा_स्थिती),sizeof(डेटा_स्थिती));
        if(डेटा_स्थिती.ऑफसॅट_मोल>आयटम_COUNT||डेटा_स्थिती.파일영역크기>आयटम_COUNT-डेटा_स्थिती.ऑफसॅट_मोल||डेटा_स्थिती.파일영역크기>डेटा_स्थिती.기억영역크기)return -1;
        if(डेटा_स्थिती.TYPE_वर्ग==1){
            if((डेटा_स्थिती.설정비트&~7u)||!(डेटा_स्थिती.설정비트&4)||(डेटा_स्थिती.설정비트&3)==3||डेटा_स्थिती.नामो<0x02000000||डेटा_स्थिती.नामो>0x02c00000||डेटा_स्थिती.기억영역크기>0x02c00000-डेटा_स्थिती.नामो)return -1;
            if((डेटा_स्थिती.설정비트&1)&&실행머리.प्रवेश_पॉयंट>=डेटा_स्थिती.नामो&&실행머리.प्रवेश_पॉयंट-डेटा_स्थिती.नामो<डेटा_स्थिती.파일영역크기&&!(실행머리.प्रवेश_पॉयंट&3))진입점정상=1;
            size_t 선행값=डेटा_स्थिती.नामो&4095,바이트들=डेटा_स्थिती.파일영역크기?선행값+डेटा_स्थिती.파일영역크기:0;
            if(फुडलें_आयटम>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-फुडलें_आयटम){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(फुडलें_आयटम+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+फुडलें_आयटम+선행값,원본자료+डेटा_स्थिती.ऑफसॅट_मोल,डेटा_स्थिती.파일영역크기);
            डेटा_स्थिती.नामो-=선행값;डेटा_स्थिती.물리주소=डेटा_स्थिती.नामो;डेटा_स्थिती.기억영역크기+=선행값;डेटा_स्थिती.파일영역크기=바이트들;डेटा_स्थिती.ऑफसॅट_मोल=फुडलें_आयटम;डेटा_स्थिती.맞춤=4096;
            for(uint64_t पान_मोल=डेटा_स्थिती.नामो;पान_मोल<डेटा_स्थिती.नामो+डेटा_स्थिती.기억영역크기;पान_मोल+=4096){unsigned लूकअप_INDEX=(पान_मोल-0x02000000)/4096;if(लूकअप_INDEX>=sizeof(पान_सुची)||पान_सुची[लूकअप_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}पान_सुची[लूकअप_INDEX]=1;}
            फुडलें_आयटम+=(바이트들+4095)&~(size_t)4095;
        }else if(डेटा_स्थिती.TYPE_वर्ग==4){if(डेटा_स्थिती.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+डेटा_स्थिती.ऑफसॅट_मोल,डेटा_स्थिती.파일영역크기);डेटा_स्थिती.ऑफसॅट_मोल=부가정보;부가정보+=डेटा_स्थिती.파일영역크기;}
        else if(डेटा_स्थिती.TYPE_वर्ग!=0&&डेटा_स्थिती.TYPE_वर्ग!=6&&डेटा_स्थिती.TYPE_वर्ग!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.एप्लिकेशन_माथाळो_ऑफसॅट+순번*sizeof(डेटा_स्थिती),&डेटा_स्थिती,sizeof(डेटा_स्थिती));
    }
    if(!진입점정상)return -1;
    intptr_t फायल_हँडल=사용자호출(3,(uintptr_t)नांव,577,0600,0,0,0);if(फायल_हँडल<0){printf("cc: cannot create output file, error %d\n",(int)फायल_हँडल);return -1;}
    intptr_t 쓴수=사용자호출(1,फायल_हँडल,(uintptr_t)IMAGE,फुडलें_आयटम,0,0,0);사용자호출(4,फायल_हँडल,0,0,0,0,0);return 쓴수==(intptr_t)फुडलें_आयटम?0:-1;
}
int Start_उपेगकर्तो_एप्लिकेशन(int पद्दत_मोड){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(पद्दत_मोड?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(पद्दत_मोड?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*स्ट्रिंग_डेटा=tcc_new();if(!स्ट्रिंग_डेटा)return 1;
    tcc_undefine_symbol(स्ट्रिंग_डेटा,"__linux__");tcc_undefine_symbol(स्ट्रिंग_डेटा,"__linux");tcc_undefine_symbol(स्ट्रिंग_डेटा,"linux");
    tcc_undefine_symbol(स्ट्रिंग_डेटा,"__unix__");tcc_undefine_symbol(स्ट्रिंग_डेटा,"__unix");tcc_undefine_symbol(स्ट्रिंग_डेटा,"unix");
    tcc_undefine_symbol(स्ट्रिंग_डेटा,"__STDC_HOSTED__");tcc_define_symbol(स्ट्रिंग_डेटा,"__STDC_HOSTED__","0");tcc_define_symbol(स्ट्रिंग_डेटा,"__JKOROS__","1");
    tcc_set_options(स्ट्रिंग_डेटा,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(स्ट्रिंग_डेटा,"/sdk/include");
    int 반환값=tcc_set_output_type(स्ट्रिंग_डेटा,TCC_OUTPUT_EXE);
    if(!반환값){if(पद्दत_मोड){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(स्ट्रिंग_डेटा,원본자료):-1;}else 반환값=tcc_add_file(स्ट्रिंग_डेटा,입력결과);}
    if(!반환값)반환값=tcc_add_file(स्ट्रिंग_डेटा,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(स्ट्रिंग_डेटा,"/sdk/lib/crt.o");
    if(!반환값&&पद्दत_मोड)반환값=tcc_add_file(स्ट्रिंग_डेटा,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(स्ट्रिंग_डेटा,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(स्ट्रिंग_डेटा,"/@cc-output");
    if(!반환값)반환값=उजवाडावचें_प्रवेश(출력결과);
    tcc_delete(स्ट्रिंग_डेटा);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(पद्दत_मोड?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
