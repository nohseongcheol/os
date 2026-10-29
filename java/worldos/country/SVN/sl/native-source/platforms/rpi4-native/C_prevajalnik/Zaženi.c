#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VALUE[16];uint16_t Tip_območje,računalnik_Tip;uint32_t številka_različice;uint64_t vnos_p,aplikacija_Glava_odmik,glava_odseka_odmik;uint32_t konfiguracija_storitev_Background_Intelligent_Transfer_Service;uint16_t Velikost,aplikacija_Glava_spremeniti_velikost,aplikacija_Glava_COUNT,glava_odseka_spremeniti_velikost,glava_odseka_COUNT,odsek_ime_tabela; } Glava_VALUE;
typedef struct {uint32_t Tip_območje,konfiguracija_storitev_Background_Intelligent_Transfer_Service;uint64_t odmik_VALUE,naslov,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int objaviti_vnos(const char *Ime){
    size_t element_COUNT;const unsigned char*원본자료=시언어출력(&element_COUNT);if(element_COUNT<sizeof(Glava_VALUE))return -1;
    Glava_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.Tip_območje!=2||실행머리.računalnik_Tip!=183||실행머리.aplikacija_Glava_spremeniti_velikost!=sizeof(segment_VALUE)||!실행머리.aplikacija_Glava_COUNT||실행머리.aplikacija_Glava_COUNT>16||실행머리.aplikacija_Glava_odmik>element_COUNT||실행머리.aplikacija_Glava_COUNT*sizeof(segment_VALUE)>element_COUNT-실행머리.aplikacija_Glava_odmik)return -1;
    실행머리.aplikacija_Glava_odmik=sizeof(실행머리);실행머리.glava_odseka_odmik=실행머리.glava_odseka_COUNT=실행머리.glava_odseka_spremeniti_velikost=실행머리.odsek_ime_tabela=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.aplikacija_Glava_COUNT*sizeof(segment_VALUE),Naprej_element=4096;unsigned char stran_Seznam[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.aplikacija_Glava_COUNT;순번++){
        segment_VALUE podatki_položaj;Glava_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&podatki_položaj,원본자료+원본.aplikacija_Glava_odmik+순번*sizeof(podatki_položaj),sizeof(podatki_položaj));
        if(podatki_položaj.odmik_VALUE>element_COUNT||podatki_položaj.파일영역크기>element_COUNT-podatki_položaj.odmik_VALUE||podatki_položaj.파일영역크기>podatki_položaj.기억영역크기)return -1;
        if(podatki_položaj.Tip_območje==1){
            if((podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service&~7u)||!(podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service&4)||(podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service&3)==3||podatki_položaj.naslov<0x02000000||podatki_položaj.naslov>0x02c00000||podatki_položaj.기억영역크기>0x02c00000-podatki_položaj.naslov)return -1;
            if((podatki_položaj.konfiguracija_storitev_Background_Intelligent_Transfer_Service&1)&&실행머리.vnos_p>=podatki_položaj.naslov&&실행머리.vnos_p-podatki_položaj.naslov<podatki_položaj.파일영역크기&&!(실행머리.vnos_p&3))진입점정상=1;
            size_t 선행값=podatki_položaj.naslov&4095,바이트들=podatki_položaj.파일영역크기?선행값+podatki_položaj.파일영역크기:0;
            if(Naprej_element>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Naprej_element){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Naprej_element+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Naprej_element+선행값,원본자료+podatki_položaj.odmik_VALUE,podatki_položaj.파일영역크기);
            podatki_položaj.naslov-=선행값;podatki_položaj.물리주소=podatki_položaj.naslov;podatki_položaj.기억영역크기+=선행값;podatki_položaj.파일영역크기=바이트들;podatki_položaj.odmik_VALUE=Naprej_element;podatki_položaj.맞춤=4096;
            for(uint64_t stran_VALUE=podatki_položaj.naslov;stran_VALUE<podatki_položaj.naslov+podatki_položaj.기억영역크기;stran_VALUE+=4096){unsigned LOOKUP_INDEX=(stran_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(stran_Seznam)||stran_Seznam[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}stran_Seznam[LOOKUP_INDEX]=1;}
            Naprej_element+=(바이트들+4095)&~(size_t)4095;
        }else if(podatki_položaj.Tip_območje==4){if(podatki_položaj.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+podatki_položaj.odmik_VALUE,podatki_položaj.파일영역크기);podatki_položaj.odmik_VALUE=부가정보;부가정보+=podatki_položaj.파일영역크기;}
        else if(podatki_položaj.Tip_območje!=0&&podatki_položaj.Tip_območje!=6&&podatki_položaj.Tip_območje!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.aplikacija_Glava_odmik+순번*sizeof(podatki_položaj),&podatki_položaj,sizeof(podatki_položaj));
    }
    if(!진입점정상)return -1;
    intptr_t Datoteka_ročica=사용자호출(3,(uintptr_t)Ime,577,0600,0,0,0);if(Datoteka_ročica<0){printf("cc: cannot create output file, error %d\n",(int)Datoteka_ročica);return -1;}
    intptr_t 쓴수=사용자호출(1,Datoteka_ročica,(uintptr_t)IMAGE,Naprej_element,0,0,0);사용자호출(4,Datoteka_ročica,0,0,0,0,0);return 쓴수==(intptr_t)Naprej_element?0:-1;
}
int Start_uporabnik_aplikacija(int metoda_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metoda_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metoda_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*niz_podatki=tcc_new();if(!niz_podatki)return 1;
    tcc_undefine_symbol(niz_podatki,"__linux__");tcc_undefine_symbol(niz_podatki,"__linux");tcc_undefine_symbol(niz_podatki,"linux");
    tcc_undefine_symbol(niz_podatki,"__unix__");tcc_undefine_symbol(niz_podatki,"__unix");tcc_undefine_symbol(niz_podatki,"unix");
    tcc_undefine_symbol(niz_podatki,"__STDC_HOSTED__");tcc_define_symbol(niz_podatki,"__STDC_HOSTED__","0");tcc_define_symbol(niz_podatki,"__JKOROS__","1");
    tcc_set_options(niz_podatki,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(niz_podatki,"/sdk/include");
    int 반환값=tcc_set_output_type(niz_podatki,TCC_OUTPUT_EXE);
    if(!반환값){if(metoda_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(niz_podatki,원본자료):-1;}else 반환값=tcc_add_file(niz_podatki,입력결과);}
    if(!반환값)반환값=tcc_add_file(niz_podatki,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(niz_podatki,"/sdk/lib/crt.o");
    if(!반환값&&metoda_MODE)반환값=tcc_add_file(niz_podatki,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(niz_podatki,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(niz_podatki,"/@cc-output");
    if(!반환값)반환값=objaviti_vnos(출력결과);
    tcc_delete(niz_podatki);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metoda_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
