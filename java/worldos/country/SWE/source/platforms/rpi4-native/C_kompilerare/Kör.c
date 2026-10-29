#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_utleverans(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifierare_värde[16];uint16_t Typ_område,dator_Typ;uint32_t versionsnummer;uint64_t startpunkt,app_huvud_FÖRSKJUTNING,avsnittsrubrik_FÖRSKJUTNING;uint32_t konfiguration_BITS;uint16_t Storlek,app_huvud_storlek,app_huvud_ANTAL,avsnittsrubrik_storlek,avsnittsrubrik_ANTAL,avsnitt_namn_tabell; } huvud_värde;
typedef struct {uint32_t Typ_område,konfiguration_BITS;uint64_t FÖRSKJUTNING_värde,Adress,물리주소,파일영역크기,기억영역크기,justera_gräns;} segment_värde_32e9301f;
static unsigned char BILD[16384];
static int publicera_post(const char *Namn){
    size_t objekt_ANTAL;const unsigned char*원본자료=C_utleverans(&objekt_ANTAL);if(objekt_ANTAL<sizeof(huvud_värde))return -1;
    huvud_värde körbar_fil_huvud;memcpy(&körbar_fil_huvud,원본자료,sizeof(körbar_fil_huvud));
    if(körbar_fil_huvud.Typ_område!=2||körbar_fil_huvud.dator_Typ!=183||körbar_fil_huvud.app_huvud_storlek!=sizeof(segment_värde_32e9301f)||!körbar_fil_huvud.app_huvud_ANTAL||körbar_fil_huvud.app_huvud_ANTAL>16||körbar_fil_huvud.app_huvud_FÖRSKJUTNING>objekt_ANTAL||körbar_fil_huvud.app_huvud_ANTAL*sizeof(segment_värde_32e9301f)>objekt_ANTAL-körbar_fil_huvud.app_huvud_FÖRSKJUTNING)return -1;
    körbar_fil_huvud.app_huvud_FÖRSKJUTNING=sizeof(körbar_fil_huvud);körbar_fil_huvud.avsnittsrubrik_FÖRSKJUTNING=körbar_fil_huvud.avsnittsrubrik_ANTAL=körbar_fil_huvud.avsnittsrubrik_storlek=körbar_fil_huvud.avsnitt_namn_tabell=0;memcpy(BILD,&körbar_fil_huvud,sizeof(körbar_fil_huvud));
    size_t 부가정보=sizeof(körbar_fil_huvud)+körbar_fil_huvud.app_huvud_ANTAL*sizeof(segment_värde_32e9301f),Nästa_objekt=4096;unsigned char page_ange[3072]={0};int giltig_startpunkt=0;
    for(unsigned 순번=0;순번<körbar_fil_huvud.app_huvud_ANTAL;순번++){
        segment_värde_32e9301f data_placera;huvud_värde 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_placera,원본자료+원본.app_huvud_FÖRSKJUTNING+순번*sizeof(data_placera),sizeof(data_placera));
        if(data_placera.FÖRSKJUTNING_värde>objekt_ANTAL||data_placera.파일영역크기>objekt_ANTAL-data_placera.FÖRSKJUTNING_värde||data_placera.파일영역크기>data_placera.기억영역크기)return -1;
        if(data_placera.Typ_område==1){
            if((data_placera.konfiguration_BITS&~7u)||!(data_placera.konfiguration_BITS&4)||(data_placera.konfiguration_BITS&3)==3||data_placera.Adress<0x02000000||data_placera.Adress>0x02c00000||data_placera.기억영역크기>0x02c00000-data_placera.Adress)return -1;
            if((data_placera.konfiguration_BITS&1)&&körbar_fil_huvud.startpunkt>=data_placera.Adress&&körbar_fil_huvud.startpunkt-data_placera.Adress<data_placera.파일영역크기&&!(körbar_fil_huvud.startpunkt&3))giltig_startpunkt=1;
            size_t 선행값=data_placera.Adress&4095,바이트들=data_placera.파일영역크기?선행값+data_placera.파일영역크기:0;
            if(Nästa_objekt>sizeof(BILD)||바이트들>sizeof(BILD)-Nästa_objekt){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Nästa_objekt+바이트들),(unsigned)sizeof(BILD));return -1;}
            if(바이트들)memcpy(BILD+Nästa_objekt+선행값,원본자료+data_placera.FÖRSKJUTNING_värde,data_placera.파일영역크기);
            data_placera.Adress-=선행값;data_placera.물리주소=data_placera.Adress;data_placera.기억영역크기+=선행값;data_placera.파일영역크기=바이트들;data_placera.FÖRSKJUTNING_värde=Nästa_objekt;data_placera.justera_gräns=4096;
            for(uint64_t page_värde=data_placera.Adress;page_värde<data_placera.Adress+data_placera.기억영역크기;page_värde+=4096){unsigned LETAUPP_INDEX=(page_värde-0x02000000)/4096;if(LETAUPP_INDEX>=sizeof(page_ange)||page_ange[LETAUPP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}page_ange[LETAUPP_INDEX]=1;}
            Nästa_objekt+=(바이트들+4095)&~(size_t)4095;
        }else if(data_placera.Typ_område==4){if(data_placera.파일영역크기>4096-부가정보)return -1;memcpy(BILD+부가정보,원본자료+data_placera.FÖRSKJUTNING_värde,data_placera.파일영역크기);data_placera.FÖRSKJUTNING_värde=부가정보;부가정보+=data_placera.파일영역크기;}
        else if(data_placera.Typ_område!=0&&data_placera.Typ_område!=6&&data_placera.Typ_område!=0x6474e551)return -1;
        memcpy(BILD+körbar_fil_huvud.app_huvud_FÖRSKJUTNING+순번*sizeof(data_placera),&data_placera,sizeof(data_placera));
    }
    if(!giltig_startpunkt)return -1;
    intptr_t filreferens=사용자호출(3,(uintptr_t)Namn,577,0600,0,0,0);if(filreferens<0){printf("cc: cannot create output file, error %d\n",(int)filreferens);return -1;}
    intptr_t 쓴수=사용자호출(1,filreferens,(uintptr_t)BILD,Nästa_objekt,0,0,0);사용자호출(4,filreferens,0,0,0,0,0);return 쓴수==(intptr_t)Nästa_objekt?0:-1;
}
int START_användare_app(int metod_läge){
    char indata[256],선택항목[256],utleverans[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metod_läge?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)indata,sizeof(indata),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(indata,"--version")||!strcmp(indata,"-version"))){printf(metod_läge?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)utleverans,sizeof(utleverans),0,0,0)<0)return 2;}
    if(!strcmp(indata,utleverans)){printf("cc: input and output must differ\n");return 2;}
    TCCState*sträng_data=tcc_new();if(!sträng_data)return 1;
    tcc_undefine_symbol(sträng_data,"__linux__");tcc_undefine_symbol(sträng_data,"__linux");tcc_undefine_symbol(sträng_data,"linux");
    tcc_undefine_symbol(sträng_data,"__unix__");tcc_undefine_symbol(sträng_data,"__unix");tcc_undefine_symbol(sträng_data,"unix");
    tcc_undefine_symbol(sträng_data,"__STDC_HOSTED__");tcc_define_symbol(sträng_data,"__STDC_HOSTED__","0");tcc_define_symbol(sträng_data,"__JKOROS__","1");
    tcc_set_options(sträng_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(sträng_data,"/sdk/include");
    int 반환값=tcc_set_output_type(sträng_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metod_läge){const char*원본자료=자바미리번역원문(indata);반환값=원본자료?tcc_compile_string(sträng_data,원본자료):-1;}else 반환값=tcc_add_file(sträng_data,indata);}
    if(!반환값)반환값=tcc_add_file(sträng_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(sträng_data,"/sdk/lib/crt.o");
    if(!반환값&&metod_läge)반환값=tcc_add_file(sträng_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(sträng_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(sträng_data,"/@cc-output");
    if(!반환값)반환값=publicera_post(utleverans);
    tcc_delete(sträng_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metod_läge?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",utleverans);return 0;
}
