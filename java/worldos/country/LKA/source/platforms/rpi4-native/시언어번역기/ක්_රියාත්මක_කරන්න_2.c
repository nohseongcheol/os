#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char හඳුන්වනය_අගය[16];uint16_t ටයිප්_කරන්න_ප්_රවර්ගය,යන්ත්_රය_ටයිප්_කරන්න;uint32_t 판번호;uint64_t පිවිසුම_ලකුණ,යෙදු_ශීර්ෂය_ඕෆ්සෙට්,අංශය_ශීර්ෂය_ඕෆ්සෙට්;uint32_t 설정비트;uint16_t ප්_රමාණය,යෙදු_ශීර්ෂය_ප්_රමාණනය,프로그램머리개수,අංශය_ශීර්ෂය_ප්_රමාණනය,구역머리개수,අංශය_නම_වගුව; } ශීර්ෂය_අගය;
typedef struct {uint32_t ටයිප්_කරන්න_ප්_රවර්ගය,설정비트;uint64_t ඕෆ්සෙට්_අගය,යොමුව,물리주소,파일영역크기,기억영역크기,맞춤;} ඛණ්ඩය_අගය;
static unsigned char අනුරුව[16384];
static int පළ_කරන්න_පිවිසුම(const char *නම){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(ශීර්ෂය_අගය))return -1;
    ශීර්ෂය_අගය 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.ටයිප්_කරන්න_ප්_රවර්ගය!=2||실행머리.යන්ත්_රය_ටයිප්_කරන්න!=183||실행머리.යෙදු_ශීර්ෂය_ප්_රමාණනය!=sizeof(ඛණ්ඩය_අගය)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.යෙදු_ශීර්ෂය_ඕෆ්සෙට්>개수||실행머리.프로그램머리개수*sizeof(ඛණ්ඩය_අගය)>개수-실행머리.යෙදු_ශීර්ෂය_ඕෆ්සෙට්)return -1;
    실행머리.යෙදු_ශීර්ෂය_ඕෆ්සෙට්=sizeof(실행머리);실행머리.අංශය_ශීර්ෂය_ඕෆ්සෙට්=실행머리.구역머리개수=실행머리.අංශය_ශීර්ෂය_ප්_රමාණනය=실행머리.අංශය_නම_වගුව=0;memcpy(අනුරුව,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(ඛණ්ඩය_අගය),다음=4096;unsigned char පිටුව_ලැයිස්තුව[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        ඛණ්ඩය_අගය 자료위치;ශීර්ෂය_අගය 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.යෙදු_ශීර්ෂය_ඕෆ්සෙට්+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.ඕෆ්සෙට්_අගය>개수||자료위치.파일영역크기>개수-자료위치.ඕෆ්සෙට්_අගය||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.ටයිප්_කරන්න_ප්_රවර්ගය==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.යොමුව<0x02000000||자료위치.යොමුව>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.යොමුව)return -1;
            if((자료위치.설정비트&1)&&실행머리.පිවිසුම_ලකුණ>=자료위치.යොමුව&&실행머리.පිවිසුම_ලකුණ-자료위치.යොමුව<자료위치.파일영역크기&&!(실행머리.පිවිසුම_ලකුණ&3))진입점정상=1;
            size_t 선행값=자료위치.යොමුව&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(අනුරුව)||바이트들>sizeof(අනුරුව)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(අනුරුව));return -1;}
            if(바이트들)memcpy(අනුරුව+다음+선행값,원본자료+자료위치.ඕෆ්සෙට්_අගය,자료위치.파일영역크기);
            자료위치.යොමුව-=선행값;자료위치.물리주소=자료위치.යොමුව;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.ඕෆ්සෙට්_අගය=다음;자료위치.맞춤=4096;
            for(uint64_t පිටුව_අගය=자료위치.යොමුව;පිටුව_අගය<자료위치.යොමුව+자료위치.기억영역크기;පිටුව_අගය+=4096){unsigned 색인=(පිටුව_අගය-0x02000000)/4096;if(색인>=sizeof(පිටුව_ලැයිස්තුව)||පිටුව_ලැයිස්තුව[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}පිටුව_ලැයිස්තුව[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.ටයිප්_කරන්න_ප්_රවර්ගය==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(අනුරුව+부가정보,원본자료+자료위치.ඕෆ්සෙට්_අගය,자료위치.파일영역크기);자료위치.ඕෆ්සෙට්_අගය=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.ටයිප්_කරන්න_ප්_රවර්ගය!=0&&자료위치.ටයිප්_කරන්න_ප්_රවර්ගය!=6&&자료위치.ටයිප්_කරන්න_ප්_රවර්ගය!=0x6474e551)return -1;
        memcpy(අනුරුව+실행머리.යෙදු_ශීර්ෂය_ඕෆ්සෙට්+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t ගොනුව_හසුරුව=사용자호출(3,(uintptr_t)නම,577,0600,0,0,0);if(ගොනුව_හසුරුව<0){printf("cc: cannot create output file, error %d\n",(int)ගොනුව_හසුරුව);return -1;}
    intptr_t 쓴수=사용자호출(1,ගොනුව_හසුරුව,(uintptr_t)අනුරුව,다음,0,0,0);사용자호출(4,ගොනුව_හසුරුව,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int ඇරඹුම_පරිශීලක_යෙදු(int ක්_රමය_ප්_රකාරය){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(ක්_රමය_ප්_රකාරය?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(ක්_රමය_ප්_රකාරය?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*අනුලකුණු_වැල_දත්ත=tcc_new();if(!අනුලකුණු_වැල_දත්ත)return 1;
    tcc_undefine_symbol(අනුලකුණු_වැල_දත්ත,"__linux__");tcc_undefine_symbol(අනුලකුණු_වැල_දත්ත,"__linux");tcc_undefine_symbol(අනුලකුණු_වැල_දත්ත,"linux");
    tcc_undefine_symbol(අනුලකුණු_වැල_දත්ත,"__unix__");tcc_undefine_symbol(අනුලකුණු_වැල_දත්ත,"__unix");tcc_undefine_symbol(අනුලකුණු_වැල_දත්ත,"unix");
    tcc_undefine_symbol(අනුලකුණු_වැල_දත්ත,"__STDC_HOSTED__");tcc_define_symbol(අනුලකුණු_වැල_දත්ත,"__STDC_HOSTED__","0");tcc_define_symbol(අනුලකුණු_වැල_දත්ත,"__JKOROS__","1");
    tcc_set_options(අනුලකුණු_වැල_දත්ත,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(අනුලකුණු_වැල_දත්ත,"/sdk/include");
    int 반환값=tcc_set_output_type(අනුලකුණු_වැල_දත්ත,TCC_OUTPUT_EXE);
    if(!반환값){if(ක්_රමය_ප්_රකාරය){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(අනුලකුණු_වැල_දත්ත,원본자료):-1;}else 반환값=tcc_add_file(අනුලකුණු_වැල_දත්ත,입력결과);}
    if(!반환값)반환값=tcc_add_file(අනුලකුණු_වැල_දත්ත,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(අනුලකුණු_වැල_දත්ත,"/sdk/lib/crt.o");
    if(!반환값&&ක්_රමය_ප්_රකාරය)반환값=tcc_add_file(අනුලකුණු_වැල_දත්ත,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(අනුලකුණු_වැල_දත්ත,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(අනුලකුණු_වැල_දත්ත,"/@cc-output");
    if(!반환값)반환값=පළ_කරන්න_පිවිසුම(출력결과);
    tcc_delete(අනුලකුණු_වැල_දත්ත);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(ක්_රමය_ප්_රකාරය?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
