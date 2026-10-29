#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikátor_VALUE[16];uint16_t Typ_oblasť,počítač_Typ;uint32_t číslo_verzie;uint64_t položka_bod,program_Nadpis_Posun,hlavička_sekcie_Posun;uint32_t konfigurácia_Background_Intelligent_Transfer_Service;uint16_t Veľkosť,program_Nadpis_zmeniť_veľkosť,program_Nadpis_COUNT,hlavička_sekcie_zmeniť_veľkosť,hlavička_sekcie_COUNT,sekcia_názov_tabuľka; } Nadpis_VALUE;
typedef struct {uint32_t Typ_oblasť,konfigurácia_Background_Intelligent_Transfer_Service;uint64_t Posun_VALUE,adresa,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int publikovať_položka(const char *Názov){
    size_t položka_COUNT;const unsigned char*원본자료=시언어출력(&položka_COUNT);if(položka_COUNT<sizeof(Nadpis_VALUE))return -1;
    Nadpis_VALUE spustiteľný_súbor_Nadpis;memcpy(&spustiteľný_súbor_Nadpis,원본자료,sizeof(spustiteľný_súbor_Nadpis));
    if(spustiteľný_súbor_Nadpis.Typ_oblasť!=2||spustiteľný_súbor_Nadpis.počítač_Typ!=183||spustiteľný_súbor_Nadpis.program_Nadpis_zmeniť_veľkosť!=sizeof(segment_VALUE)||!spustiteľný_súbor_Nadpis.program_Nadpis_COUNT||spustiteľný_súbor_Nadpis.program_Nadpis_COUNT>16||spustiteľný_súbor_Nadpis.program_Nadpis_Posun>položka_COUNT||spustiteľný_súbor_Nadpis.program_Nadpis_COUNT*sizeof(segment_VALUE)>položka_COUNT-spustiteľný_súbor_Nadpis.program_Nadpis_Posun)return -1;
    spustiteľný_súbor_Nadpis.program_Nadpis_Posun=sizeof(spustiteľný_súbor_Nadpis);spustiteľný_súbor_Nadpis.hlavička_sekcie_Posun=spustiteľný_súbor_Nadpis.hlavička_sekcie_COUNT=spustiteľný_súbor_Nadpis.hlavička_sekcie_zmeniť_veľkosť=spustiteľný_súbor_Nadpis.sekcia_názov_tabuľka=0;memcpy(IMAGE,&spustiteľný_súbor_Nadpis,sizeof(spustiteľný_súbor_Nadpis));
    size_t 부가정보=sizeof(spustiteľný_súbor_Nadpis)+spustiteľný_súbor_Nadpis.program_Nadpis_COUNT*sizeof(segment_VALUE),Ďalej_položka=4096;unsigned char strana_Zoznam[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<spustiteľný_súbor_Nadpis.program_Nadpis_COUNT;순번++){
        segment_VALUE údaje_pozícia;Nadpis_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&údaje_pozícia,원본자료+원본.program_Nadpis_Posun+순번*sizeof(údaje_pozícia),sizeof(údaje_pozícia));
        if(údaje_pozícia.Posun_VALUE>položka_COUNT||údaje_pozícia.파일영역크기>položka_COUNT-údaje_pozícia.Posun_VALUE||údaje_pozícia.파일영역크기>údaje_pozícia.기억영역크기)return -1;
        if(údaje_pozícia.Typ_oblasť==1){
            if((údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service&~7u)||!(údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service&4)||(údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service&3)==3||údaje_pozícia.adresa<0x02000000||údaje_pozícia.adresa>0x02c00000||údaje_pozícia.기억영역크기>0x02c00000-údaje_pozícia.adresa)return -1;
            if((údaje_pozícia.konfigurácia_Background_Intelligent_Transfer_Service&1)&&spustiteľný_súbor_Nadpis.položka_bod>=údaje_pozícia.adresa&&spustiteľný_súbor_Nadpis.položka_bod-údaje_pozícia.adresa<údaje_pozícia.파일영역크기&&!(spustiteľný_súbor_Nadpis.položka_bod&3))진입점정상=1;
            size_t 선행값=údaje_pozícia.adresa&4095,바이트들=údaje_pozícia.파일영역크기?선행값+údaje_pozícia.파일영역크기:0;
            if(Ďalej_položka>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Ďalej_položka){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Ďalej_položka+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Ďalej_položka+선행값,원본자료+údaje_pozícia.Posun_VALUE,údaje_pozícia.파일영역크기);
            údaje_pozícia.adresa-=선행값;údaje_pozícia.물리주소=údaje_pozícia.adresa;údaje_pozícia.기억영역크기+=선행값;údaje_pozícia.파일영역크기=바이트들;údaje_pozícia.Posun_VALUE=Ďalej_položka;údaje_pozícia.맞춤=4096;
            for(uint64_t strana_VALUE=údaje_pozícia.adresa;strana_VALUE<údaje_pozícia.adresa+údaje_pozícia.기억영역크기;strana_VALUE+=4096){unsigned LOOKUP_INDEX=(strana_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(strana_Zoznam)||strana_Zoznam[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}strana_Zoznam[LOOKUP_INDEX]=1;}
            Ďalej_položka+=(바이트들+4095)&~(size_t)4095;
        }else if(údaje_pozícia.Typ_oblasť==4){if(údaje_pozícia.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+údaje_pozícia.Posun_VALUE,údaje_pozícia.파일영역크기);údaje_pozícia.Posun_VALUE=부가정보;부가정보+=údaje_pozícia.파일영역크기;}
        else if(údaje_pozícia.Typ_oblasť!=0&&údaje_pozícia.Typ_oblasť!=6&&údaje_pozícia.Typ_oblasť!=0x6474e551)return -1;
        memcpy(IMAGE+spustiteľný_súbor_Nadpis.program_Nadpis_Posun+순번*sizeof(údaje_pozícia),&údaje_pozícia,sizeof(údaje_pozícia));
    }
    if(!진입점정상)return -1;
    intptr_t Súbor_rukoväť=사용자호출(3,(uintptr_t)Názov,577,0600,0,0,0);if(Súbor_rukoväť<0){printf("cc: cannot create output file, error %d\n",(int)Súbor_rukoväť);return -1;}
    intptr_t 쓴수=사용자호출(1,Súbor_rukoväť,(uintptr_t)IMAGE,Ďalej_položka,0,0,0);사용자호출(4,Súbor_rukoväť,0,0,0,0,0);return 쓴수==(intptr_t)Ďalej_položka?0:-1;
}
int START_používateľ_program(int metóda_MODE){
    char vstup[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metóda_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)vstup,sizeof(vstup),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(vstup,"--version")||!strcmp(vstup,"-version"))){printf(metóda_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(vstup,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*reťazec_údaje=tcc_new();if(!reťazec_údaje)return 1;
    tcc_undefine_symbol(reťazec_údaje,"__linux__");tcc_undefine_symbol(reťazec_údaje,"__linux");tcc_undefine_symbol(reťazec_údaje,"linux");
    tcc_undefine_symbol(reťazec_údaje,"__unix__");tcc_undefine_symbol(reťazec_údaje,"__unix");tcc_undefine_symbol(reťazec_údaje,"unix");
    tcc_undefine_symbol(reťazec_údaje,"__STDC_HOSTED__");tcc_define_symbol(reťazec_údaje,"__STDC_HOSTED__","0");tcc_define_symbol(reťazec_údaje,"__JKOROS__","1");
    tcc_set_options(reťazec_údaje,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(reťazec_údaje,"/sdk/include");
    int 반환값=tcc_set_output_type(reťazec_údaje,TCC_OUTPUT_EXE);
    if(!반환값){if(metóda_MODE){const char*원본자료=자바미리번역원문(vstup);반환값=원본자료?tcc_compile_string(reťazec_údaje,원본자료):-1;}else 반환값=tcc_add_file(reťazec_údaje,vstup);}
    if(!반환값)반환값=tcc_add_file(reťazec_údaje,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(reťazec_údaje,"/sdk/lib/crt.o");
    if(!반환값&&metóda_MODE)반환값=tcc_add_file(reťazec_údaje,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(reťazec_údaje,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(reťazec_údaje,"/@cc-output");
    if(!반환값)반환값=publikovať_položka(출력결과);
    tcc_delete(reťazec_údaje);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metóda_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
