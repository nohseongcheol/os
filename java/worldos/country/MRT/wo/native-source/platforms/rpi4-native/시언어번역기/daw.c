#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char raññeekaay_xëyma[16];uint16_t xeet_ngiir,masin_xeet;uint32_t 판번호;uint64_t dugal_xabaar_Tomb,jëfekaay_Tur_Randal,dog_Tur_Randal;uint32_t 설정비트;uint16_t tolluwaay,jëfekaay_Tur_tolluwaay,프로그램머리개수,dog_Tur_tolluwaay,구역머리개수,dog_tur_àlluwa; } Tur_xëyma;
typedef struct {uint32_t xeet_ngiir,설정비트;uint64_t Randal_xëyma,dëkkuwaay,물리주소,파일영역크기,기억영역크기,맞춤;} dog_xëyma_32e9301f;
static unsigned char nataal[16384];
static int Siiwal_dugal_xabaar(const char *tur_253d1510){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(Tur_xëyma))return -1;
    Tur_xëyma 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.xeet_ngiir!=2||실행머리.masin_xeet!=183||실행머리.jëfekaay_Tur_tolluwaay!=sizeof(dog_xëyma_32e9301f)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.jëfekaay_Tur_Randal>개수||실행머리.프로그램머리개수*sizeof(dog_xëyma_32e9301f)>개수-실행머리.jëfekaay_Tur_Randal)return -1;
    실행머리.jëfekaay_Tur_Randal=sizeof(실행머리);실행머리.dog_Tur_Randal=실행머리.구역머리개수=실행머리.dog_Tur_tolluwaay=실행머리.dog_tur_àlluwa=0;memcpy(nataal,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(dog_xëyma_32e9301f),다음=4096;unsigned char xët_lim[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        dog_xëyma_32e9301f 자료위치;Tur_xëyma 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.jëfekaay_Tur_Randal+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Randal_xëyma>개수||자료위치.파일영역크기>개수-자료위치.Randal_xëyma||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.xeet_ngiir==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.dëkkuwaay<0x02000000||자료위치.dëkkuwaay>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.dëkkuwaay)return -1;
            if((자료위치.설정비트&1)&&실행머리.dugal_xabaar_Tomb>=자료위치.dëkkuwaay&&실행머리.dugal_xabaar_Tomb-자료위치.dëkkuwaay<자료위치.파일영역크기&&!(실행머리.dugal_xabaar_Tomb&3))진입점정상=1;
            size_t 선행값=자료위치.dëkkuwaay&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(nataal)||바이트들>sizeof(nataal)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(nataal));return -1;}
            if(바이트들)memcpy(nataal+다음+선행값,원본자료+자료위치.Randal_xëyma,자료위치.파일영역크기);
            자료위치.dëkkuwaay-=선행값;자료위치.물리주소=자료위치.dëkkuwaay;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Randal_xëyma=다음;자료위치.맞춤=4096;
            for(uint64_t xët_xëyma=자료위치.dëkkuwaay;xët_xëyma<자료위치.dëkkuwaay+자료위치.기억영역크기;xët_xëyma+=4096){unsigned 색인=(xët_xëyma-0x02000000)/4096;if(색인>=sizeof(xët_lim)||xët_lim[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}xët_lim[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.xeet_ngiir==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(nataal+부가정보,원본자료+자료위치.Randal_xëyma,자료위치.파일영역크기);자료위치.Randal_xëyma=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.xeet_ngiir!=0&&자료위치.xeet_ngiir!=6&&자료위치.xeet_ngiir!=0x6474e551)return -1;
        memcpy(nataal+실행머리.jëfekaay_Tur_Randal+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t bara_denc_yombal=사용자호출(3,(uintptr_t)tur_253d1510,577,0600,0,0,0);if(bara_denc_yombal<0){printf("cc: cannot create output file, error %d\n",(int)bara_denc_yombal);return -1;}
    intptr_t 쓴수=사용자호출(1,bara_denc_yombal,(uintptr_t)nataal,다음,0,0,0);사용자호출(4,bara_denc_yombal,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Door_kiy_jariñoo_internet_jëfekaay(int doxalin_anam){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(doxalin_anam?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(doxalin_anam?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*araf_yu_bennoo_mbir=tcc_new();if(!araf_yu_bennoo_mbir)return 1;
    tcc_undefine_symbol(araf_yu_bennoo_mbir,"__linux__");tcc_undefine_symbol(araf_yu_bennoo_mbir,"__linux");tcc_undefine_symbol(araf_yu_bennoo_mbir,"linux");
    tcc_undefine_symbol(araf_yu_bennoo_mbir,"__unix__");tcc_undefine_symbol(araf_yu_bennoo_mbir,"__unix");tcc_undefine_symbol(araf_yu_bennoo_mbir,"unix");
    tcc_undefine_symbol(araf_yu_bennoo_mbir,"__STDC_HOSTED__");tcc_define_symbol(araf_yu_bennoo_mbir,"__STDC_HOSTED__","0");tcc_define_symbol(araf_yu_bennoo_mbir,"__JKOROS__","1");
    tcc_set_options(araf_yu_bennoo_mbir,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(araf_yu_bennoo_mbir,"/sdk/include");
    int 반환값=tcc_set_output_type(araf_yu_bennoo_mbir,TCC_OUTPUT_EXE);
    if(!반환값){if(doxalin_anam){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(araf_yu_bennoo_mbir,원본자료):-1;}else 반환값=tcc_add_file(araf_yu_bennoo_mbir,입력결과);}
    if(!반환값)반환값=tcc_add_file(araf_yu_bennoo_mbir,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(araf_yu_bennoo_mbir,"/sdk/lib/crt.o");
    if(!반환값&&doxalin_anam)반환값=tcc_add_file(araf_yu_bennoo_mbir,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(araf_yu_bennoo_mbir,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(araf_yu_bennoo_mbir,"/@cc-output");
    if(!반환값)반환값=Siiwal_dugal_xabaar(출력결과);
    tcc_delete(araf_yu_bennoo_mbir);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(doxalin_anam?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
