#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_išeiga(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikatorius_VALUE[16];uint16_t TYPE_sritis,mašina_TYPE;uint32_t versijos_numeris;uint64_t įrašas_p,programa_Antraštė_OFFSET,sekcijos_antraštė_OFFSET;uint32_t konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba;uint16_t Dydis,programa_Antraštė_dydis,programa_Antraštė_COUNT,sekcijos_antraštė_dydis,sekcijos_antraštė_COUNT,sekcija_pavadinimas_lentelė; } Antraštė_VALUE;
typedef struct {uint32_t TYPE_sritis,konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba;uint64_t OFFSET_VALUE,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} segmentas_VALUE_32e9301f;
static unsigned char IMAGE[16384];
static int publikuoti_įrašas(const char *Pavadinimas_2){
    size_t prekė_COUNT;const unsigned char*원본자료=C_išeiga(&prekė_COUNT);if(prekė_COUNT<sizeof(Antraštė_VALUE))return -1;
    Antraštė_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_sritis!=2||실행머리.mašina_TYPE!=183||실행머리.programa_Antraštė_dydis!=sizeof(segmentas_VALUE_32e9301f)||!실행머리.programa_Antraštė_COUNT||실행머리.programa_Antraštė_COUNT>16||실행머리.programa_Antraštė_OFFSET>prekė_COUNT||실행머리.programa_Antraštė_COUNT*sizeof(segmentas_VALUE_32e9301f)>prekė_COUNT-실행머리.programa_Antraštė_OFFSET)return -1;
    실행머리.programa_Antraštė_OFFSET=sizeof(실행머리);실행머리.sekcijos_antraštė_OFFSET=실행머리.sekcijos_antraštė_COUNT=실행머리.sekcijos_antraštė_dydis=실행머리.sekcija_pavadinimas_lentelė=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.programa_Antraštė_COUNT*sizeof(segmentas_VALUE_32e9301f),toliau_prekė=4096;unsigned char puslapis_Sąrašas[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.programa_Antraštė_COUNT;순번++){
        segmentas_VALUE_32e9301f duomenys_padėtis;Antraštė_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&duomenys_padėtis,원본자료+원본.programa_Antraštė_OFFSET+순번*sizeof(duomenys_padėtis),sizeof(duomenys_padėtis));
        if(duomenys_padėtis.OFFSET_VALUE>prekė_COUNT||duomenys_padėtis.파일영역크기>prekė_COUNT-duomenys_padėtis.OFFSET_VALUE||duomenys_padėtis.파일영역크기>duomenys_padėtis.기억영역크기)return -1;
        if(duomenys_padėtis.TYPE_sritis==1){
            if((duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&~7u)||!(duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&4)||(duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&3)==3||duomenys_padėtis.ADDRESS<0x02000000||duomenys_padėtis.ADDRESS>0x02c00000||duomenys_padėtis.기억영역크기>0x02c00000-duomenys_padėtis.ADDRESS)return -1;
            if((duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&1)&&실행머리.įrašas_p>=duomenys_padėtis.ADDRESS&&실행머리.įrašas_p-duomenys_padėtis.ADDRESS<duomenys_padėtis.파일영역크기&&!(실행머리.įrašas_p&3))진입점정상=1;
            size_t 선행값=duomenys_padėtis.ADDRESS&4095,바이트들=duomenys_padėtis.파일영역크기?선행값+duomenys_padėtis.파일영역크기:0;
            if(toliau_prekė>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-toliau_prekė){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(toliau_prekė+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+toliau_prekė+선행값,원본자료+duomenys_padėtis.OFFSET_VALUE,duomenys_padėtis.파일영역크기);
            duomenys_padėtis.ADDRESS-=선행값;duomenys_padėtis.물리주소=duomenys_padėtis.ADDRESS;duomenys_padėtis.기억영역크기+=선행값;duomenys_padėtis.파일영역크기=바이트들;duomenys_padėtis.OFFSET_VALUE=toliau_prekė;duomenys_padėtis.맞춤=4096;
            for(uint64_t puslapis_VALUE=duomenys_padėtis.ADDRESS;puslapis_VALUE<duomenys_padėtis.ADDRESS+duomenys_padėtis.기억영역크기;puslapis_VALUE+=4096){unsigned LOOKUP_INDEX=(puslapis_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(puslapis_Sąrašas)||puslapis_Sąrašas[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}puslapis_Sąrašas[LOOKUP_INDEX]=1;}
            toliau_prekė+=(바이트들+4095)&~(size_t)4095;
        }else if(duomenys_padėtis.TYPE_sritis==4){if(duomenys_padėtis.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+duomenys_padėtis.OFFSET_VALUE,duomenys_padėtis.파일영역크기);duomenys_padėtis.OFFSET_VALUE=부가정보;부가정보+=duomenys_padėtis.파일영역크기;}
        else if(duomenys_padėtis.TYPE_sritis!=0&&duomenys_padėtis.TYPE_sritis!=6&&duomenys_padėtis.TYPE_sritis!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.programa_Antraštė_OFFSET+순번*sizeof(duomenys_padėtis),&duomenys_padėtis,sizeof(duomenys_padėtis));
    }
    if(!진입점정상)return -1;
    intptr_t Failas_rodyklė=사용자호출(3,(uintptr_t)Pavadinimas_2,577,0600,0,0,0);if(Failas_rodyklė<0){printf("cc: cannot create output file, error %d\n",(int)Failas_rodyklė);return -1;}
    intptr_t 쓴수=사용자호출(1,Failas_rodyklė,(uintptr_t)IMAGE,toliau_prekė,0,0,0);사용자호출(4,Failas_rodyklė,0,0,0,0,0);return 쓴수==(intptr_t)toliau_prekė?0:-1;
}
int Start_naudotojas_programa(int metodas_MODE){
    char 입력결과[256],선택항목[256],išeiga[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metodas_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metodas_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)išeiga,sizeof(išeiga),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,išeiga)){printf("cc: input and output must differ\n");return 2;}
    TCCState*eilutė_duomenys=tcc_new();if(!eilutė_duomenys)return 1;
    tcc_undefine_symbol(eilutė_duomenys,"__linux__");tcc_undefine_symbol(eilutė_duomenys,"__linux");tcc_undefine_symbol(eilutė_duomenys,"linux");
    tcc_undefine_symbol(eilutė_duomenys,"__unix__");tcc_undefine_symbol(eilutė_duomenys,"__unix");tcc_undefine_symbol(eilutė_duomenys,"unix");
    tcc_undefine_symbol(eilutė_duomenys,"__STDC_HOSTED__");tcc_define_symbol(eilutė_duomenys,"__STDC_HOSTED__","0");tcc_define_symbol(eilutė_duomenys,"__JKOROS__","1");
    tcc_set_options(eilutė_duomenys,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(eilutė_duomenys,"/sdk/include");
    int 반환값=tcc_set_output_type(eilutė_duomenys,TCC_OUTPUT_EXE);
    if(!반환값){if(metodas_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(eilutė_duomenys,원본자료):-1;}else 반환값=tcc_add_file(eilutė_duomenys,입력결과);}
    if(!반환값)반환값=tcc_add_file(eilutė_duomenys,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(eilutė_duomenys,"/sdk/lib/crt.o");
    if(!반환값&&metodas_MODE)반환값=tcc_add_file(eilutė_duomenys,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(eilutė_duomenys,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(eilutė_duomenys,"/@cc-output");
    if(!반환값)반환값=publikuoti_įrašas(išeiga);
    tcc_delete(eilutė_duomenys);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metodas_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",išeiga);return 0;
}
