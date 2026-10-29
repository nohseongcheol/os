#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char kitambulishi_thamani[16];uint16_t aina_kategoria,mashine_aina;uint32_t 판번호;uint64_t ingizo_pointi,programu_kichwa_Chipua,sehemu_kichwa_Chipua;uint32_t usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma;uint16_t panga_ukubwa,programu_kichwa_panga_ukubwa,프로그램머리개수,sehemu_kichwa_panga_ukubwa,구역머리개수,sehemu_jina_jedwali; } kichwa_thamani;
typedef struct {uint32_t aina_kategoria,usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma;uint64_t Chipua_thamani,anwani,물리주소,파일영역크기,기억영역크기,맞춤;} sehemu_thamani_32e9301f;
static unsigned char picha[16384];
static int chapisha_ingizo(const char *Jina){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(kichwa_thamani))return -1;
    kichwa_thamani 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.aina_kategoria!=2||실행머리.mashine_aina!=183||실행머리.programu_kichwa_panga_ukubwa!=sizeof(sehemu_thamani_32e9301f)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.programu_kichwa_Chipua>개수||실행머리.프로그램머리개수*sizeof(sehemu_thamani_32e9301f)>개수-실행머리.programu_kichwa_Chipua)return -1;
    실행머리.programu_kichwa_Chipua=sizeof(실행머리);실행머리.sehemu_kichwa_Chipua=실행머리.구역머리개수=실행머리.sehemu_kichwa_panga_ukubwa=실행머리.sehemu_jina_jedwali=0;memcpy(picha,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(sehemu_thamani_32e9301f),다음=4096;unsigned char ukurasa_Orodha[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        sehemu_thamani_32e9301f 자료위치;kichwa_thamani 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.programu_kichwa_Chipua+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Chipua_thamani>개수||자료위치.파일영역크기>개수-자료위치.Chipua_thamani||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.aina_kategoria==1){
            if((자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&~7u)||!(자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&4)||(자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&3)==3||자료위치.anwani<0x02000000||자료위치.anwani>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.anwani)return -1;
            if((자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&1)&&실행머리.ingizo_pointi>=자료위치.anwani&&실행머리.ingizo_pointi-자료위치.anwani<자료위치.파일영역크기&&!(실행머리.ingizo_pointi&3))진입점정상=1;
            size_t 선행값=자료위치.anwani&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(picha)||바이트들>sizeof(picha)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(picha));return -1;}
            if(바이트들)memcpy(picha+다음+선행값,원본자료+자료위치.Chipua_thamani,자료위치.파일영역크기);
            자료위치.anwani-=선행값;자료위치.물리주소=자료위치.anwani;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Chipua_thamani=다음;자료위치.맞춤=4096;
            for(uint64_t ukurasa_thamani=자료위치.anwani;ukurasa_thamani<자료위치.anwani+자료위치.기억영역크기;ukurasa_thamani+=4096){unsigned 색인=(ukurasa_thamani-0x02000000)/4096;if(색인>=sizeof(ukurasa_Orodha)||ukurasa_Orodha[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ukurasa_Orodha[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.aina_kategoria==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(picha+부가정보,원본자료+자료위치.Chipua_thamani,자료위치.파일영역크기);자료위치.Chipua_thamani=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.aina_kategoria!=0&&자료위치.aina_kategoria!=6&&자료위치.aina_kategoria!=0x6474e551)return -1;
        memcpy(picha+실행머리.programu_kichwa_Chipua+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t faili_kishiko=사용자호출(3,(uintptr_t)Jina,577,0600,0,0,0);if(faili_kishiko<0){printf("cc: cannot create output file, error %d\n",(int)faili_kishiko);return -1;}
    intptr_t 쓴수=사용자호출(1,faili_kishiko,(uintptr_t)picha,다음,0,0,0);사용자호출(4,faili_kishiko,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Anza_mtumiaji_programu(int mbinu_hali_tumizi){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(mbinu_hali_tumizi?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(mbinu_hali_tumizi?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*tungo_data=tcc_new();if(!tungo_data)return 1;
    tcc_undefine_symbol(tungo_data,"__linux__");tcc_undefine_symbol(tungo_data,"__linux");tcc_undefine_symbol(tungo_data,"linux");
    tcc_undefine_symbol(tungo_data,"__unix__");tcc_undefine_symbol(tungo_data,"__unix");tcc_undefine_symbol(tungo_data,"unix");
    tcc_undefine_symbol(tungo_data,"__STDC_HOSTED__");tcc_define_symbol(tungo_data,"__STDC_HOSTED__","0");tcc_define_symbol(tungo_data,"__JKOROS__","1");
    tcc_set_options(tungo_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(tungo_data,"/sdk/include");
    int 반환값=tcc_set_output_type(tungo_data,TCC_OUTPUT_EXE);
    if(!반환값){if(mbinu_hali_tumizi){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(tungo_data,원본자료):-1;}else 반환값=tcc_add_file(tungo_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(tungo_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(tungo_data,"/sdk/lib/crt.o");
    if(!반환값&&mbinu_hali_tumizi)반환값=tcc_add_file(tungo_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(tungo_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(tungo_data,"/@cc-output");
    if(!반환값)반환값=chapisha_ingizo(출력결과);
    tcc_delete(tungo_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(mbinu_hali_tumizi?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
