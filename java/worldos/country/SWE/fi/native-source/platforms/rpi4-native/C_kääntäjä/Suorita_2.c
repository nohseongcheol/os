#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_tulos(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char tunniste_ARVO[16];uint16_t TYYPPI_alue,kone_TYYPPI;uint32_t versionumero;uint64_t aloituskohta,ohjelma_otsikko_SIIRTYMÄ,osan_otsikko_SIIRTYMÄ;uint32_t määritys_Background_Intelligent_Transfer_Service;uint16_t Koko,ohjelma_otsikko_muuttaa_kokoa,ohjelma_otsikko_LASKE,osan_otsikko_muuttaa_kokoa,osan_otsikko_LASKE,osa_nimi_taulukko; } otsikko_ARVO;
typedef struct {uint32_t TYYPPI_alue,määritys_Background_Intelligent_Transfer_Service;uint64_t SIIRTYMÄ_ARVO,OSOITE,물리주소,파일영역크기,기억영역크기,tasaa_rajattu_alue;} segmentti_ARVO;
static unsigned char KUVA[16384];
static int julkaista_merkintä(const char *Nimi){
    size_t kohde_LASKE;const unsigned char*원본자료=C_tulos(&kohde_LASKE);if(kohde_LASKE<sizeof(otsikko_ARVO))return -1;
    otsikko_ARVO suoritettava_tiedosto_otsikko;memcpy(&suoritettava_tiedosto_otsikko,원본자료,sizeof(suoritettava_tiedosto_otsikko));
    if(suoritettava_tiedosto_otsikko.TYYPPI_alue!=2||suoritettava_tiedosto_otsikko.kone_TYYPPI!=183||suoritettava_tiedosto_otsikko.ohjelma_otsikko_muuttaa_kokoa!=sizeof(segmentti_ARVO)||!suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE||suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE>16||suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ>kohde_LASKE||suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE*sizeof(segmentti_ARVO)>kohde_LASKE-suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ)return -1;
    suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ=sizeof(suoritettava_tiedosto_otsikko);suoritettava_tiedosto_otsikko.osan_otsikko_SIIRTYMÄ=suoritettava_tiedosto_otsikko.osan_otsikko_LASKE=suoritettava_tiedosto_otsikko.osan_otsikko_muuttaa_kokoa=suoritettava_tiedosto_otsikko.osa_nimi_taulukko=0;memcpy(KUVA,&suoritettava_tiedosto_otsikko,sizeof(suoritettava_tiedosto_otsikko));
    size_t 부가정보=sizeof(suoritettava_tiedosto_otsikko)+suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE*sizeof(segmentti_ARVO),Seuraava_kohde=4096;unsigned char page_luettelo[3072]={0};int kelvollinen_aloituskohta=0;
    for(unsigned 순번=0;순번<suoritettava_tiedosto_otsikko.ohjelma_otsikko_LASKE;순번++){
        segmentti_ARVO data_toimi;otsikko_ARVO 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_toimi,원본자료+원본.ohjelma_otsikko_SIIRTYMÄ+순번*sizeof(data_toimi),sizeof(data_toimi));
        if(data_toimi.SIIRTYMÄ_ARVO>kohde_LASKE||data_toimi.파일영역크기>kohde_LASKE-data_toimi.SIIRTYMÄ_ARVO||data_toimi.파일영역크기>data_toimi.기억영역크기)return -1;
        if(data_toimi.TYYPPI_alue==1){
            if((data_toimi.määritys_Background_Intelligent_Transfer_Service&~7u)||!(data_toimi.määritys_Background_Intelligent_Transfer_Service&4)||(data_toimi.määritys_Background_Intelligent_Transfer_Service&3)==3||data_toimi.OSOITE<0x02000000||data_toimi.OSOITE>0x02c00000||data_toimi.기억영역크기>0x02c00000-data_toimi.OSOITE)return -1;
            if((data_toimi.määritys_Background_Intelligent_Transfer_Service&1)&&suoritettava_tiedosto_otsikko.aloituskohta>=data_toimi.OSOITE&&suoritettava_tiedosto_otsikko.aloituskohta-data_toimi.OSOITE<data_toimi.파일영역크기&&!(suoritettava_tiedosto_otsikko.aloituskohta&3))kelvollinen_aloituskohta=1;
            size_t 선행값=data_toimi.OSOITE&4095,바이트들=data_toimi.파일영역크기?선행값+data_toimi.파일영역크기:0;
            if(Seuraava_kohde>sizeof(KUVA)||바이트들>sizeof(KUVA)-Seuraava_kohde){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Seuraava_kohde+바이트들),(unsigned)sizeof(KUVA));return -1;}
            if(바이트들)memcpy(KUVA+Seuraava_kohde+선행값,원본자료+data_toimi.SIIRTYMÄ_ARVO,data_toimi.파일영역크기);
            data_toimi.OSOITE-=선행값;data_toimi.물리주소=data_toimi.OSOITE;data_toimi.기억영역크기+=선행값;data_toimi.파일영역크기=바이트들;data_toimi.SIIRTYMÄ_ARVO=Seuraava_kohde;data_toimi.tasaa_rajattu_alue=4096;
            for(uint64_t page_ARVO=data_toimi.OSOITE;page_ARVO<data_toimi.OSOITE+data_toimi.기억영역크기;page_ARVO+=4096){unsigned HAKU_INDEKSI=(page_ARVO-0x02000000)/4096;if(HAKU_INDEKSI>=sizeof(page_luettelo)||page_luettelo[HAKU_INDEKSI]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}page_luettelo[HAKU_INDEKSI]=1;}
            Seuraava_kohde+=(바이트들+4095)&~(size_t)4095;
        }else if(data_toimi.TYYPPI_alue==4){if(data_toimi.파일영역크기>4096-부가정보)return -1;memcpy(KUVA+부가정보,원본자료+data_toimi.SIIRTYMÄ_ARVO,data_toimi.파일영역크기);data_toimi.SIIRTYMÄ_ARVO=부가정보;부가정보+=data_toimi.파일영역크기;}
        else if(data_toimi.TYYPPI_alue!=0&&data_toimi.TYYPPI_alue!=6&&data_toimi.TYYPPI_alue!=0x6474e551)return -1;
        memcpy(KUVA+suoritettava_tiedosto_otsikko.ohjelma_otsikko_SIIRTYMÄ+순번*sizeof(data_toimi),&data_toimi,sizeof(data_toimi));
    }
    if(!kelvollinen_aloituskohta)return -1;
    intptr_t Tiedosto_kahva=사용자호출(3,(uintptr_t)Nimi,577,0600,0,0,0);if(Tiedosto_kahva<0){printf("cc: cannot create output file, error %d\n",(int)Tiedosto_kahva);return -1;}
    intptr_t 쓴수=사용자호출(1,Tiedosto_kahva,(uintptr_t)KUVA,Seuraava_kohde,0,0,0);사용자호출(4,Tiedosto_kahva,0,0,0,0,0);return 쓴수==(intptr_t)Seuraava_kohde?0:-1;
}
int alku_käyttäjä_ohjelma(int menetelmä_tila){
    char syöte[256],선택항목[256],tulos[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(menetelmä_tila?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)syöte,sizeof(syöte),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(syöte,"--version")||!strcmp(syöte,"-version"))){printf(menetelmä_tila?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)tulos,sizeof(tulos),0,0,0)<0)return 2;}
    if(!strcmp(syöte,tulos)){printf("cc: input and output must differ\n");return 2;}
    TCCState*merkkijono_data=tcc_new();if(!merkkijono_data)return 1;
    tcc_undefine_symbol(merkkijono_data,"__linux__");tcc_undefine_symbol(merkkijono_data,"__linux");tcc_undefine_symbol(merkkijono_data,"linux");
    tcc_undefine_symbol(merkkijono_data,"__unix__");tcc_undefine_symbol(merkkijono_data,"__unix");tcc_undefine_symbol(merkkijono_data,"unix");
    tcc_undefine_symbol(merkkijono_data,"__STDC_HOSTED__");tcc_define_symbol(merkkijono_data,"__STDC_HOSTED__","0");tcc_define_symbol(merkkijono_data,"__JKOROS__","1");
    tcc_set_options(merkkijono_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(merkkijono_data,"/sdk/include");
    int 반환값=tcc_set_output_type(merkkijono_data,TCC_OUTPUT_EXE);
    if(!반환값){if(menetelmä_tila){const char*원본자료=자바미리번역원문(syöte);반환값=원본자료?tcc_compile_string(merkkijono_data,원본자료):-1;}else 반환값=tcc_add_file(merkkijono_data,syöte);}
    if(!반환값)반환값=tcc_add_file(merkkijono_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(merkkijono_data,"/sdk/lib/crt.o");
    if(!반환값&&menetelmä_tila)반환값=tcc_add_file(merkkijono_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(merkkijono_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(merkkijono_data,"/@cc-output");
    if(!반환값)반환값=julkaista_merkintä(tulos);
    tcc_delete(merkkijono_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(menetelmä_tila?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",tulos);return 0;
}
