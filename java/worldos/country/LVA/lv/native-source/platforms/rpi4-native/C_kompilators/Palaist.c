#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_ražojums(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikators_VALUE[16];uint16_t TYPE_joma,mašīna_TYPE;uint32_t versijas_numurs;uint64_t ieejas_punkts,programma_galvene_Nobīde,sadaļas_galvene_Nobīde;uint32_t konfigurācija_Background_Intelligent_Transfer_Service;uint16_t Izmērs,programma_galvene_mainīt_izmērus,programma_galvene_COUNT,sadaļas_galvene_mainīt_izmērus,sadaļas_galvene_COUNT,sadaļa_nosaukums_tabula; } galvene_VALUE;
typedef struct {uint32_t TYPE_joma,konfigurācija_Background_Intelligent_Transfer_Service;uint64_t Nobīde_VALUE,adrese,물리주소,파일영역크기,기억영역크기,맞춤;} segments_VALUE;
static unsigned char IMAGE[16384];
static int publicēt_ievade(const char *Nosaukums){
    size_t krājums_COUNT;const unsigned char*원본자료=C_ražojums(&krājums_COUNT);if(krājums_COUNT<sizeof(galvene_VALUE))return -1;
    galvene_VALUE izpildāms_fails_galvene;memcpy(&izpildāms_fails_galvene,원본자료,sizeof(izpildāms_fails_galvene));
    if(izpildāms_fails_galvene.TYPE_joma!=2||izpildāms_fails_galvene.mašīna_TYPE!=183||izpildāms_fails_galvene.programma_galvene_mainīt_izmērus!=sizeof(segments_VALUE)||!izpildāms_fails_galvene.programma_galvene_COUNT||izpildāms_fails_galvene.programma_galvene_COUNT>16||izpildāms_fails_galvene.programma_galvene_Nobīde>krājums_COUNT||izpildāms_fails_galvene.programma_galvene_COUNT*sizeof(segments_VALUE)>krājums_COUNT-izpildāms_fails_galvene.programma_galvene_Nobīde)return -1;
    izpildāms_fails_galvene.programma_galvene_Nobīde=sizeof(izpildāms_fails_galvene);izpildāms_fails_galvene.sadaļas_galvene_Nobīde=izpildāms_fails_galvene.sadaļas_galvene_COUNT=izpildāms_fails_galvene.sadaļas_galvene_mainīt_izmērus=izpildāms_fails_galvene.sadaļa_nosaukums_tabula=0;memcpy(IMAGE,&izpildāms_fails_galvene,sizeof(izpildāms_fails_galvene));
    size_t 부가정보=sizeof(izpildāms_fails_galvene)+izpildāms_fails_galvene.programma_galvene_COUNT*sizeof(segments_VALUE),Tālāk_krājums=4096;unsigned char lapa_Saraksts[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<izpildāms_fails_galvene.programma_galvene_COUNT;순번++){
        segments_VALUE dati_amats;galvene_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&dati_amats,원본자료+원본.programma_galvene_Nobīde+순번*sizeof(dati_amats),sizeof(dati_amats));
        if(dati_amats.Nobīde_VALUE>krājums_COUNT||dati_amats.파일영역크기>krājums_COUNT-dati_amats.Nobīde_VALUE||dati_amats.파일영역크기>dati_amats.기억영역크기)return -1;
        if(dati_amats.TYPE_joma==1){
            if((dati_amats.konfigurācija_Background_Intelligent_Transfer_Service&~7u)||!(dati_amats.konfigurācija_Background_Intelligent_Transfer_Service&4)||(dati_amats.konfigurācija_Background_Intelligent_Transfer_Service&3)==3||dati_amats.adrese<0x02000000||dati_amats.adrese>0x02c00000||dati_amats.기억영역크기>0x02c00000-dati_amats.adrese)return -1;
            if((dati_amats.konfigurācija_Background_Intelligent_Transfer_Service&1)&&izpildāms_fails_galvene.ieejas_punkts>=dati_amats.adrese&&izpildāms_fails_galvene.ieejas_punkts-dati_amats.adrese<dati_amats.파일영역크기&&!(izpildāms_fails_galvene.ieejas_punkts&3))진입점정상=1;
            size_t 선행값=dati_amats.adrese&4095,바이트들=dati_amats.파일영역크기?선행값+dati_amats.파일영역크기:0;
            if(Tālāk_krājums>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Tālāk_krājums){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Tālāk_krājums+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Tālāk_krājums+선행값,원본자료+dati_amats.Nobīde_VALUE,dati_amats.파일영역크기);
            dati_amats.adrese-=선행값;dati_amats.물리주소=dati_amats.adrese;dati_amats.기억영역크기+=선행값;dati_amats.파일영역크기=바이트들;dati_amats.Nobīde_VALUE=Tālāk_krājums;dati_amats.맞춤=4096;
            for(uint64_t lapa_VALUE=dati_amats.adrese;lapa_VALUE<dati_amats.adrese+dati_amats.기억영역크기;lapa_VALUE+=4096){unsigned LOOKUP_INDEX=(lapa_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(lapa_Saraksts)||lapa_Saraksts[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}lapa_Saraksts[LOOKUP_INDEX]=1;}
            Tālāk_krājums+=(바이트들+4095)&~(size_t)4095;
        }else if(dati_amats.TYPE_joma==4){if(dati_amats.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+dati_amats.Nobīde_VALUE,dati_amats.파일영역크기);dati_amats.Nobīde_VALUE=부가정보;부가정보+=dati_amats.파일영역크기;}
        else if(dati_amats.TYPE_joma!=0&&dati_amats.TYPE_joma!=6&&dati_amats.TYPE_joma!=0x6474e551)return -1;
        memcpy(IMAGE+izpildāms_fails_galvene.programma_galvene_Nobīde+순번*sizeof(dati_amats),&dati_amats,sizeof(dati_amats));
    }
    if(!진입점정상)return -1;
    intptr_t Fails_turis=사용자호출(3,(uintptr_t)Nosaukums,577,0600,0,0,0);if(Fails_turis<0){printf("cc: cannot create output file, error %d\n",(int)Fails_turis);return -1;}
    intptr_t 쓴수=사용자호출(1,Fails_turis,(uintptr_t)IMAGE,Tālāk_krājums,0,0,0);사용자호출(4,Fails_turis,0,0,0,0,0);return 쓴수==(intptr_t)Tālāk_krājums?0:-1;
}
int Sākt_lietotājs_programma(int metode_MODE){
    char 입력결과[256],선택항목[256],ražojums[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metode_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metode_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)ražojums,sizeof(ražojums),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,ražojums)){printf("cc: input and output must differ\n");return 2;}
    TCCState*virkne_dati=tcc_new();if(!virkne_dati)return 1;
    tcc_undefine_symbol(virkne_dati,"__linux__");tcc_undefine_symbol(virkne_dati,"__linux");tcc_undefine_symbol(virkne_dati,"linux");
    tcc_undefine_symbol(virkne_dati,"__unix__");tcc_undefine_symbol(virkne_dati,"__unix");tcc_undefine_symbol(virkne_dati,"unix");
    tcc_undefine_symbol(virkne_dati,"__STDC_HOSTED__");tcc_define_symbol(virkne_dati,"__STDC_HOSTED__","0");tcc_define_symbol(virkne_dati,"__JKOROS__","1");
    tcc_set_options(virkne_dati,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(virkne_dati,"/sdk/include");
    int 반환값=tcc_set_output_type(virkne_dati,TCC_OUTPUT_EXE);
    if(!반환값){if(metode_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(virkne_dati,원본자료):-1;}else 반환값=tcc_add_file(virkne_dati,입력결과);}
    if(!반환값)반환값=tcc_add_file(virkne_dati,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(virkne_dati,"/sdk/lib/crt.o");
    if(!반환값&&metode_MODE)반환값=tcc_add_file(virkne_dati,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(virkne_dati,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(virkne_dati,"/@cc-output");
    if(!반환값)반환값=publicēt_ievade(ražojums);
    tcc_delete(virkne_dati);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metode_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",ražojums);return 0;
}
