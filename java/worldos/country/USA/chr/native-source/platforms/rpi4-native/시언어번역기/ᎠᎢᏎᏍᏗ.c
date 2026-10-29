#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ[16];uint16_t 유형,기계유형;uint32_t 판번호;uint64_t Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ,프로그램머리변위,구역머리변위;uint32_t 설정비트;uint16_t ᎢᎩᏓ,ᎬᏙᏗ_ᎦᎸᎳᏗ_ᎪᏪᎵ_ᎢᎩᏓ,프로그램머리개수,ᎤᏓᎯᏢᎢ_ᎦᎸᎳᏗ_ᎪᏪᎵ_ᎢᎩᏓ,구역머리개수,ᎤᏓᎯᏢᎢ_ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ; } ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ;
typedef struct {uint32_t 유형,설정비트;uint64_t 변위,ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,물리주소,파일영역크기,기억영역크기,맞춤;} ᎢᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;
static unsigned char ᎤᏓᏴᎳᏛ[16384];
static int ᏘᎴᏴᏓ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(const char *ᏚᏙᎥᎢ){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ))return -1;
    ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.유형!=2||실행머리.기계유형!=183||실행머리.ᎬᏙᏗ_ᎦᎸᎳᏗ_ᎪᏪᎵ_ᎢᎩᏓ!=sizeof(ᎢᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.프로그램머리변위>개수||실행머리.프로그램머리개수*sizeof(ᎢᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ)>개수-실행머리.프로그램머리변위)return -1;
    실행머리.프로그램머리변위=sizeof(실행머리);실행머리.구역머리변위=실행머리.구역머리개수=실행머리.ᎤᏓᎯᏢᎢ_ᎦᎸᎳᏗ_ᎪᏪᎵ_ᎢᎩᏓ=실행머리.ᎤᏓᎯᏢᎢ_ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ=0;memcpy(ᎤᏓᏴᎳᏛ,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(ᎢᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ),다음=4096;unsigned char ᎤᎦᏅᏓᏛᎢ_ᏕᎦᏅᏅᏛ[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        ᎢᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ 자료위치;ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏧᎬᏩᎶᏗᏯ 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.프로그램머리변위+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.변위>개수||자료위치.파일영역크기>개수-자료위치.변위||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.유형==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ<0x02000000||자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)return -1;
            if((자료위치.설정비트&1)&&실행머리.Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ>=자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ&&실행머리.Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ-자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ<자료위치.파일영역크기&&!(실행머리.Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ&3))진입점정상=1;
            size_t 선행값=자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(ᎤᏓᏴᎳᏛ)||바이트들>sizeof(ᎤᏓᏴᎳᏛ)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(ᎤᏓᏴᎳᏛ));return -1;}
            if(바이트들)memcpy(ᎤᏓᏴᎳᏛ+다음+선행값,원본자료+자료위치.변위,자료위치.파일영역크기);
            자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ-=선행값;자료위치.물리주소=자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.변위=다음;자료위치.맞춤=4096;
            for(uint64_t ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ=자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ<자료위치.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ+자료위치.기억영역크기;ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ+=4096){unsigned 색인=(ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ-0x02000000)/4096;if(색인>=sizeof(ᎤᎦᏅᏓᏛᎢ_ᏕᎦᏅᏅᏛ)||ᎤᎦᏅᏓᏛᎢ_ᏕᎦᏅᏅᏛ[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ᎤᎦᏅᏓᏛᎢ_ᏕᎦᏅᏅᏛ[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.유형==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(ᎤᏓᏴᎳᏛ+부가정보,원본자료+자료위치.변위,자료위치.파일영역크기);자료위치.변위=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.유형!=0&&자료위치.유형!=6&&자료위치.유형!=0x6474e551)return -1;
        memcpy(ᎤᏓᏴᎳᏛ+실행머리.프로그램머리변위+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ=사용자호출(3,(uintptr_t)ᏚᏙᎥᎢ,577,0600,0,0,0);if(ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ<0){printf("cc: cannot create output file, error %d\n",(int)ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ);return -1;}
    intptr_t 쓴수=사용자호출(1,ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ,(uintptr_t)ᎤᏓᏴᎳᏛ,다음,0,0,0);사용자호출(4,ᎠᏍᏆᏂᎪᏙᏗ_ᎫᎭᏢ,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ(int method_ᎬᏙᏗ){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(method_ᎬᏙᏗ?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(method_ᎬᏙᏗ?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*ᎠᏍᏘ_ᎦᏟᏌᏅᎯ=tcc_new();if(!ᎠᏍᏘ_ᎦᏟᏌᏅᎯ)return 1;
    tcc_undefine_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"__linux__");tcc_undefine_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"__linux");tcc_undefine_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"linux");
    tcc_undefine_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"__unix__");tcc_undefine_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"__unix");tcc_undefine_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"unix");
    tcc_undefine_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"__STDC_HOSTED__");tcc_define_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"__STDC_HOSTED__","0");tcc_define_symbol(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"__JKOROS__","1");
    tcc_set_options(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"/sdk/include");
    int 반환값=tcc_set_output_type(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,TCC_OUTPUT_EXE);
    if(!반환값){if(method_ᎬᏙᏗ){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,원본자료):-1;}else 반환값=tcc_add_file(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,입력결과);}
    if(!반환값)반환값=tcc_add_file(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"/sdk/lib/crt.o");
    if(!반환값&&method_ᎬᏙᏗ)반환값=tcc_add_file(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ,"/@cc-output");
    if(!반환값)반환값=ᏘᎴᏴᏓ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(출력결과);
    tcc_delete(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(method_ᎬᏙᏗ?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
