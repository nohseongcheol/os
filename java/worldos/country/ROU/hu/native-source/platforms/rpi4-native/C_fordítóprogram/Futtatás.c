#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_kimenet(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char azonosító_ÉRTÉK[16];uint16_t beír_terület,gép_beír;uint32_t verziószám;uint64_t belépési_pont,app_fejléc_Ofszet,szakaszfejléc_Ofszet;uint32_t konfiguráció_BITS;uint16_t Méret,app_fejléc_méretez,app_fejléc_DARAB,szakaszfejléc_méretez,szakaszfejléc_DARAB,szakasz_név_tábla; } fejléc_ÉRTÉK;
typedef struct {uint32_t beír_terület,konfiguráció_BITS;uint64_t Ofszet_ÉRTÉK,CÍM,물리주소,파일영역크기,기억영역크기,igazít_határ;} szegmens_ÉRTÉK;
static unsigned char KÉP[16384];
static int közzétesz_bejegyzés(const char *Név){
    size_t cikk_DARAB;const unsigned char*원본자료=C_kimenet(&cikk_DARAB);if(cikk_DARAB<sizeof(fejléc_ÉRTÉK))return -1;
    fejléc_ÉRTÉK végrehajtható_fejléc;memcpy(&végrehajtható_fejléc,원본자료,sizeof(végrehajtható_fejléc));
    if(végrehajtható_fejléc.beír_terület!=2||végrehajtható_fejléc.gép_beír!=183||végrehajtható_fejléc.app_fejléc_méretez!=sizeof(szegmens_ÉRTÉK)||!végrehajtható_fejléc.app_fejléc_DARAB||végrehajtható_fejléc.app_fejléc_DARAB>16||végrehajtható_fejléc.app_fejléc_Ofszet>cikk_DARAB||végrehajtható_fejléc.app_fejléc_DARAB*sizeof(szegmens_ÉRTÉK)>cikk_DARAB-végrehajtható_fejléc.app_fejléc_Ofszet)return -1;
    végrehajtható_fejléc.app_fejléc_Ofszet=sizeof(végrehajtható_fejléc);végrehajtható_fejléc.szakaszfejléc_Ofszet=végrehajtható_fejléc.szakaszfejléc_DARAB=végrehajtható_fejléc.szakaszfejléc_méretez=végrehajtható_fejléc.szakasz_név_tábla=0;memcpy(KÉP,&végrehajtható_fejléc,sizeof(végrehajtható_fejléc));
    size_t 부가정보=sizeof(végrehajtható_fejléc)+végrehajtható_fejléc.app_fejléc_DARAB*sizeof(szegmens_ÉRTÉK),Tovább_cikk=4096;unsigned char lap_Lista[3072]={0};int érvényes_belépési_pont=0;
    for(unsigned 순번=0;순번<végrehajtható_fejléc.app_fejléc_DARAB;순번++){
        szegmens_ÉRTÉK adat_pozíció;fejléc_ÉRTÉK 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&adat_pozíció,원본자료+원본.app_fejléc_Ofszet+순번*sizeof(adat_pozíció),sizeof(adat_pozíció));
        if(adat_pozíció.Ofszet_ÉRTÉK>cikk_DARAB||adat_pozíció.파일영역크기>cikk_DARAB-adat_pozíció.Ofszet_ÉRTÉK||adat_pozíció.파일영역크기>adat_pozíció.기억영역크기)return -1;
        if(adat_pozíció.beír_terület==1){
            if((adat_pozíció.konfiguráció_BITS&~7u)||!(adat_pozíció.konfiguráció_BITS&4)||(adat_pozíció.konfiguráció_BITS&3)==3||adat_pozíció.CÍM<0x02000000||adat_pozíció.CÍM>0x02c00000||adat_pozíció.기억영역크기>0x02c00000-adat_pozíció.CÍM)return -1;
            if((adat_pozíció.konfiguráció_BITS&1)&&végrehajtható_fejléc.belépési_pont>=adat_pozíció.CÍM&&végrehajtható_fejléc.belépési_pont-adat_pozíció.CÍM<adat_pozíció.파일영역크기&&!(végrehajtható_fejléc.belépési_pont&3))érvényes_belépési_pont=1;
            size_t 선행값=adat_pozíció.CÍM&4095,바이트들=adat_pozíció.파일영역크기?선행값+adat_pozíció.파일영역크기:0;
            if(Tovább_cikk>sizeof(KÉP)||바이트들>sizeof(KÉP)-Tovább_cikk){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Tovább_cikk+바이트들),(unsigned)sizeof(KÉP));return -1;}
            if(바이트들)memcpy(KÉP+Tovább_cikk+선행값,원본자료+adat_pozíció.Ofszet_ÉRTÉK,adat_pozíció.파일영역크기);
            adat_pozíció.CÍM-=선행값;adat_pozíció.물리주소=adat_pozíció.CÍM;adat_pozíció.기억영역크기+=선행값;adat_pozíció.파일영역크기=바이트들;adat_pozíció.Ofszet_ÉRTÉK=Tovább_cikk;adat_pozíció.igazít_határ=4096;
            for(uint64_t lap_ÉRTÉK=adat_pozíció.CÍM;lap_ÉRTÉK<adat_pozíció.CÍM+adat_pozíció.기억영역크기;lap_ÉRTÉK+=4096){unsigned KERES_INDEX=(lap_ÉRTÉK-0x02000000)/4096;if(KERES_INDEX>=sizeof(lap_Lista)||lap_Lista[KERES_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}lap_Lista[KERES_INDEX]=1;}
            Tovább_cikk+=(바이트들+4095)&~(size_t)4095;
        }else if(adat_pozíció.beír_terület==4){if(adat_pozíció.파일영역크기>4096-부가정보)return -1;memcpy(KÉP+부가정보,원본자료+adat_pozíció.Ofszet_ÉRTÉK,adat_pozíció.파일영역크기);adat_pozíció.Ofszet_ÉRTÉK=부가정보;부가정보+=adat_pozíció.파일영역크기;}
        else if(adat_pozíció.beír_terület!=0&&adat_pozíció.beír_terület!=6&&adat_pozíció.beír_terület!=0x6474e551)return -1;
        memcpy(KÉP+végrehajtható_fejléc.app_fejléc_Ofszet+순번*sizeof(adat_pozíció),&adat_pozíció,sizeof(adat_pozíció));
    }
    if(!érvényes_belépési_pont)return -1;
    intptr_t fájlleíró=사용자호출(3,(uintptr_t)Név,577,0600,0,0,0);if(fájlleíró<0){printf("cc: cannot create output file, error %d\n",(int)fájlleíró);return -1;}
    intptr_t 쓴수=사용자호출(1,fájlleíró,(uintptr_t)KÉP,Tovább_cikk,0,0,0);사용자호출(4,fájlleíró,0,0,0,0,0);return 쓴수==(intptr_t)Tovább_cikk?0:-1;
}
int START_felhasználó_app(int metódus_mód){
    char bevitel[256],선택항목[256],kimenet[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metódus_mód?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)bevitel,sizeof(bevitel),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(bevitel,"--version")||!strcmp(bevitel,"-version"))){printf(metódus_mód?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)kimenet,sizeof(kimenet),0,0,0)<0)return 2;}
    if(!strcmp(bevitel,kimenet)){printf("cc: input and output must differ\n");return 2;}
    TCCState*sztring_adat=tcc_new();if(!sztring_adat)return 1;
    tcc_undefine_symbol(sztring_adat,"__linux__");tcc_undefine_symbol(sztring_adat,"__linux");tcc_undefine_symbol(sztring_adat,"linux");
    tcc_undefine_symbol(sztring_adat,"__unix__");tcc_undefine_symbol(sztring_adat,"__unix");tcc_undefine_symbol(sztring_adat,"unix");
    tcc_undefine_symbol(sztring_adat,"__STDC_HOSTED__");tcc_define_symbol(sztring_adat,"__STDC_HOSTED__","0");tcc_define_symbol(sztring_adat,"__JKOROS__","1");
    tcc_set_options(sztring_adat,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(sztring_adat,"/sdk/include");
    int 반환값=tcc_set_output_type(sztring_adat,TCC_OUTPUT_EXE);
    if(!반환값){if(metódus_mód){const char*원본자료=자바미리번역원문(bevitel);반환값=원본자료?tcc_compile_string(sztring_adat,원본자료):-1;}else 반환값=tcc_add_file(sztring_adat,bevitel);}
    if(!반환값)반환값=tcc_add_file(sztring_adat,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(sztring_adat,"/sdk/lib/crt.o");
    if(!반환값&&metódus_mód)반환값=tcc_add_file(sztring_adat,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(sztring_adat,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(sztring_adat,"/@cc-output");
    if(!반환값)반환값=közzétesz_bejegyzés(kimenet);
    tcc_delete(sztring_adat);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metódus_mód?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",kimenet);return 0;
}
