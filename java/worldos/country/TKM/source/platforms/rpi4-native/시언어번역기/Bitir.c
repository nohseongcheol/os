#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char tanaýjy_baha[16];uint16_t ýaz_kategoriýa,kompýuter_ýaz;uint32_t 판번호;uint64_t girizmeklik_utuk,programma_At_Süýşüriş,bölüm_At_Süýşüriş;uint32_t 설정비트;uint16_t Ululyk,programma_At_ölçegi_üýtget,프로그램머리개수,bölüm_At_ölçegi_üýtget,구역머리개수,bölüm_at_tablisa; } At_baha;
typedef struct {uint32_t ýaz_kategoriýa,설정비트;uint64_t Süýşüriş_baha,salgy,물리주소,파일영역크기,기억영역크기,맞춤;} bölek_baha;
static unsigned char surat[16384];
static int neşir_et_girizmeklik(const char *Ad){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(At_baha))return -1;
    At_baha 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.ýaz_kategoriýa!=2||실행머리.kompýuter_ýaz!=183||실행머리.programma_At_ölçegi_üýtget!=sizeof(bölek_baha)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.programma_At_Süýşüriş>개수||실행머리.프로그램머리개수*sizeof(bölek_baha)>개수-실행머리.programma_At_Süýşüriş)return -1;
    실행머리.programma_At_Süýşüriş=sizeof(실행머리);실행머리.bölüm_At_Süýşüriş=실행머리.구역머리개수=실행머리.bölüm_At_ölçegi_üýtget=실행머리.bölüm_at_tablisa=0;memcpy(surat,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(bölek_baha),다음=4096;unsigned char sahypa_Sanaw[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        bölek_baha 자료위치;At_baha 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.programma_At_Süýşüriş+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Süýşüriş_baha>개수||자료위치.파일영역크기>개수-자료위치.Süýşüriş_baha||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.ýaz_kategoriýa==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.salgy<0x02000000||자료위치.salgy>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.salgy)return -1;
            if((자료위치.설정비트&1)&&실행머리.girizmeklik_utuk>=자료위치.salgy&&실행머리.girizmeklik_utuk-자료위치.salgy<자료위치.파일영역크기&&!(실행머리.girizmeklik_utuk&3))진입점정상=1;
            size_t 선행값=자료위치.salgy&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(surat)||바이트들>sizeof(surat)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(surat));return -1;}
            if(바이트들)memcpy(surat+다음+선행값,원본자료+자료위치.Süýşüriş_baha,자료위치.파일영역크기);
            자료위치.salgy-=선행값;자료위치.물리주소=자료위치.salgy;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Süýşüriş_baha=다음;자료위치.맞춤=4096;
            for(uint64_t sahypa_baha=자료위치.salgy;sahypa_baha<자료위치.salgy+자료위치.기억영역크기;sahypa_baha+=4096){unsigned 색인=(sahypa_baha-0x02000000)/4096;if(색인>=sizeof(sahypa_Sanaw)||sahypa_Sanaw[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}sahypa_Sanaw[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.ýaz_kategoriýa==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(surat+부가정보,원본자료+자료위치.Süýşüriş_baha,자료위치.파일영역크기);자료위치.Süýşüriş_baha=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.ýaz_kategoriýa!=0&&자료위치.ýaz_kategoriýa!=6&&자료위치.ýaz_kategoriýa!=0x6474e551)return -1;
        memcpy(surat+실행머리.programma_At_Süýşüriş+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t faýl_ryçag=사용자호출(3,(uintptr_t)Ad,577,0600,0,0,0);if(faýl_ryçag<0){printf("cc: cannot create output file, error %d\n",(int)faýl_ryçag);return -1;}
    intptr_t 쓴수=사용자호출(1,faýl_ryçag,(uintptr_t)surat,다음,0,0,0);사용자호출(4,faýl_ryçag,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int başlat_ulanyjy_programma(int usul_reje){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(usul_reje?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(usul_reje?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*setir_maglumat=tcc_new();if(!setir_maglumat)return 1;
    tcc_undefine_symbol(setir_maglumat,"__linux__");tcc_undefine_symbol(setir_maglumat,"__linux");tcc_undefine_symbol(setir_maglumat,"linux");
    tcc_undefine_symbol(setir_maglumat,"__unix__");tcc_undefine_symbol(setir_maglumat,"__unix");tcc_undefine_symbol(setir_maglumat,"unix");
    tcc_undefine_symbol(setir_maglumat,"__STDC_HOSTED__");tcc_define_symbol(setir_maglumat,"__STDC_HOSTED__","0");tcc_define_symbol(setir_maglumat,"__JKOROS__","1");
    tcc_set_options(setir_maglumat,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(setir_maglumat,"/sdk/include");
    int 반환값=tcc_set_output_type(setir_maglumat,TCC_OUTPUT_EXE);
    if(!반환값){if(usul_reje){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(setir_maglumat,원본자료):-1;}else 반환값=tcc_add_file(setir_maglumat,입력결과);}
    if(!반환값)반환값=tcc_add_file(setir_maglumat,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(setir_maglumat,"/sdk/lib/crt.o");
    if(!반환값&&usul_reje)반환값=tcc_add_file(setir_maglumat,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(setir_maglumat,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(setir_maglumat,"/@cc-output");
    if(!반환값)반환값=neşir_et_girizmeklik(출력결과);
    tcc_delete(setir_maglumat);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(usul_reje?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
