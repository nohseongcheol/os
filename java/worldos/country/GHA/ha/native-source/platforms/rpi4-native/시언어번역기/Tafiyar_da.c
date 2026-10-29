#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char mai_ganewa_Daraja[16];uint16_t rubuta_ɓangare,na_ura_mai_kwakwalwa_rubuta;uint32_t 판번호;uint64_t Mashigar_bayanai_maki,Shiri_Kai_Sassautawa,Sashi_Kai_Sassautawa;uint32_t saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango;uint16_t Girma,Shiri_Kai_girma,프로그램머리개수,Sashi_Kai_girma,구역머리개수,Sashi_Suna_tebur; } Kai_Daraja;
typedef struct {uint32_t rubuta_ɓangare,saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango;uint64_t Sassautawa_Daraja,imel,물리주소,파일영역크기,기억영역크기,맞춤;} yanki_Daraja;
static unsigned char Hoto[16384];
static int wallafa_Mashigar_bayanai(const char *Suna){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(Kai_Daraja))return -1;
    Kai_Daraja 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.rubuta_ɓangare!=2||실행머리.na_ura_mai_kwakwalwa_rubuta!=183||실행머리.Shiri_Kai_girma!=sizeof(yanki_Daraja)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.Shiri_Kai_Sassautawa>개수||실행머리.프로그램머리개수*sizeof(yanki_Daraja)>개수-실행머리.Shiri_Kai_Sassautawa)return -1;
    실행머리.Shiri_Kai_Sassautawa=sizeof(실행머리);실행머리.Sashi_Kai_Sassautawa=실행머리.구역머리개수=실행머리.Sashi_Kai_girma=실행머리.Sashi_Suna_tebur=0;memcpy(Hoto,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(yanki_Daraja),다음=4096;unsigned char shafi_Jeri[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        yanki_Daraja 자료위치;Kai_Daraja 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.Shiri_Kai_Sassautawa+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Sassautawa_Daraja>개수||자료위치.파일영역크기>개수-자료위치.Sassautawa_Daraja||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.rubuta_ɓangare==1){
            if((자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&~7u)||!(자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&4)||(자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&3)==3||자료위치.imel<0x02000000||자료위치.imel>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.imel)return -1;
            if((자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&1)&&실행머리.Mashigar_bayanai_maki>=자료위치.imel&&실행머리.Mashigar_bayanai_maki-자료위치.imel<자료위치.파일영역크기&&!(실행머리.Mashigar_bayanai_maki&3))진입점정상=1;
            size_t 선행값=자료위치.imel&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(Hoto)||바이트들>sizeof(Hoto)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(Hoto));return -1;}
            if(바이트들)memcpy(Hoto+다음+선행값,원본자료+자료위치.Sassautawa_Daraja,자료위치.파일영역크기);
            자료위치.imel-=선행값;자료위치.물리주소=자료위치.imel;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Sassautawa_Daraja=다음;자료위치.맞춤=4096;
            for(uint64_t shafi_Daraja=자료위치.imel;shafi_Daraja<자료위치.imel+자료위치.기억영역크기;shafi_Daraja+=4096){unsigned 색인=(shafi_Daraja-0x02000000)/4096;if(색인>=sizeof(shafi_Jeri)||shafi_Jeri[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}shafi_Jeri[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.rubuta_ɓangare==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(Hoto+부가정보,원본자료+자료위치.Sassautawa_Daraja,자료위치.파일영역크기);자료위치.Sassautawa_Daraja=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.rubuta_ɓangare!=0&&자료위치.rubuta_ɓangare!=6&&자료위치.rubuta_ɓangare!=0x6474e551)return -1;
        memcpy(Hoto+실행머리.Shiri_Kai_Sassautawa+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t Fayil_Mariki=사용자호출(3,(uintptr_t)Suna,577,0600,0,0,0);if(Fayil_Mariki<0){printf("cc: cannot create output file, error %d\n",(int)Fayil_Mariki);return -1;}
    intptr_t 쓴수=사용자호출(1,Fayil_Mariki,(uintptr_t)Hoto,다음,0,0,0);사용자호출(4,Fayil_Mariki,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Fara_Mai_anfani_da_kwamfuta_Shiri(int tsari_yanayin_aiki){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(tsari_yanayin_aiki?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(tsari_yanayin_aiki?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*Zare_Tarin_bayani=tcc_new();if(!Zare_Tarin_bayani)return 1;
    tcc_undefine_symbol(Zare_Tarin_bayani,"__linux__");tcc_undefine_symbol(Zare_Tarin_bayani,"__linux");tcc_undefine_symbol(Zare_Tarin_bayani,"linux");
    tcc_undefine_symbol(Zare_Tarin_bayani,"__unix__");tcc_undefine_symbol(Zare_Tarin_bayani,"__unix");tcc_undefine_symbol(Zare_Tarin_bayani,"unix");
    tcc_undefine_symbol(Zare_Tarin_bayani,"__STDC_HOSTED__");tcc_define_symbol(Zare_Tarin_bayani,"__STDC_HOSTED__","0");tcc_define_symbol(Zare_Tarin_bayani,"__JKOROS__","1");
    tcc_set_options(Zare_Tarin_bayani,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(Zare_Tarin_bayani,"/sdk/include");
    int 반환값=tcc_set_output_type(Zare_Tarin_bayani,TCC_OUTPUT_EXE);
    if(!반환값){if(tsari_yanayin_aiki){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(Zare_Tarin_bayani,원본자료):-1;}else 반환값=tcc_add_file(Zare_Tarin_bayani,입력결과);}
    if(!반환값)반환값=tcc_add_file(Zare_Tarin_bayani,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(Zare_Tarin_bayani,"/sdk/lib/crt.o");
    if(!반환값&&tsari_yanayin_aiki)반환값=tcc_add_file(Zare_Tarin_bayani,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(Zare_Tarin_bayani,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(Zare_Tarin_bayani,"/@cc-output");
    if(!반환값)반환값=wallafa_Mashigar_bayanai(출력결과);
    tcc_delete(Zare_Tarin_bayani);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(tsari_yanayin_aiki?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
