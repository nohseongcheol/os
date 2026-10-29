#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_uitvoer(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char id_WAARDE[16];uint16_t TYPE_gebied,machine_TYPE;uint32_t versienummer;uint64_t beginpunt,app_header_VERSCHUIVING,sectiekop_VERSCHUIVING;uint32_t configuratie_BITS;uint16_t Grootte,app_header_formaat_wijzigen,app_header_AANTAL,sectiekop_formaat_wijzigen,sectiekop_AANTAL,sectie_naam_tabel; } header_WAARDE;
typedef struct {uint32_t TYPE_gebied,configuratie_BITS;uint64_t VERSCHUIVING_WAARDE,ADRES,물리주소,파일영역크기,기억영역크기,uitlijnen_grens;} segment_WAARDE;
static unsigned char kopie[16384];
static int publiceren_invoer(const char *Naam){
    size_t item_AANTAL;const unsigned char*원본자료=C_uitvoer(&item_AANTAL);if(item_AANTAL<sizeof(header_WAARDE))return -1;
    header_WAARDE uitvoerbaar_header;memcpy(&uitvoerbaar_header,원본자료,sizeof(uitvoerbaar_header));
    if(uitvoerbaar_header.TYPE_gebied!=2||uitvoerbaar_header.machine_TYPE!=183||uitvoerbaar_header.app_header_formaat_wijzigen!=sizeof(segment_WAARDE)||!uitvoerbaar_header.app_header_AANTAL||uitvoerbaar_header.app_header_AANTAL>16||uitvoerbaar_header.app_header_VERSCHUIVING>item_AANTAL||uitvoerbaar_header.app_header_AANTAL*sizeof(segment_WAARDE)>item_AANTAL-uitvoerbaar_header.app_header_VERSCHUIVING)return -1;
    uitvoerbaar_header.app_header_VERSCHUIVING=sizeof(uitvoerbaar_header);uitvoerbaar_header.sectiekop_VERSCHUIVING=uitvoerbaar_header.sectiekop_AANTAL=uitvoerbaar_header.sectiekop_formaat_wijzigen=uitvoerbaar_header.sectie_naam_tabel=0;memcpy(kopie,&uitvoerbaar_header,sizeof(uitvoerbaar_header));
    size_t 부가정보=sizeof(uitvoerbaar_header)+uitvoerbaar_header.app_header_AANTAL*sizeof(segment_WAARDE),Volgende_item=4096;unsigned char page_Lijst[3072]={0};int geldig_beginpunt=0;
    for(unsigned 순번=0;순번<uitvoerbaar_header.app_header_AANTAL;순번++){
        segment_WAARDE gegevens_functie;header_WAARDE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&gegevens_functie,원본자료+원본.app_header_VERSCHUIVING+순번*sizeof(gegevens_functie),sizeof(gegevens_functie));
        if(gegevens_functie.VERSCHUIVING_WAARDE>item_AANTAL||gegevens_functie.파일영역크기>item_AANTAL-gegevens_functie.VERSCHUIVING_WAARDE||gegevens_functie.파일영역크기>gegevens_functie.기억영역크기)return -1;
        if(gegevens_functie.TYPE_gebied==1){
            if((gegevens_functie.configuratie_BITS&~7u)||!(gegevens_functie.configuratie_BITS&4)||(gegevens_functie.configuratie_BITS&3)==3||gegevens_functie.ADRES<0x02000000||gegevens_functie.ADRES>0x02c00000||gegevens_functie.기억영역크기>0x02c00000-gegevens_functie.ADRES)return -1;
            if((gegevens_functie.configuratie_BITS&1)&&uitvoerbaar_header.beginpunt>=gegevens_functie.ADRES&&uitvoerbaar_header.beginpunt-gegevens_functie.ADRES<gegevens_functie.파일영역크기&&!(uitvoerbaar_header.beginpunt&3))geldig_beginpunt=1;
            size_t 선행값=gegevens_functie.ADRES&4095,바이트들=gegevens_functie.파일영역크기?선행값+gegevens_functie.파일영역크기:0;
            if(Volgende_item>sizeof(kopie)||바이트들>sizeof(kopie)-Volgende_item){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Volgende_item+바이트들),(unsigned)sizeof(kopie));return -1;}
            if(바이트들)memcpy(kopie+Volgende_item+선행값,원본자료+gegevens_functie.VERSCHUIVING_WAARDE,gegevens_functie.파일영역크기);
            gegevens_functie.ADRES-=선행값;gegevens_functie.물리주소=gegevens_functie.ADRES;gegevens_functie.기억영역크기+=선행값;gegevens_functie.파일영역크기=바이트들;gegevens_functie.VERSCHUIVING_WAARDE=Volgende_item;gegevens_functie.uitlijnen_grens=4096;
            for(uint64_t page_WAARDE=gegevens_functie.ADRES;page_WAARDE<gegevens_functie.ADRES+gegevens_functie.기억영역크기;page_WAARDE+=4096){unsigned ZOEKEN_INDEX=(page_WAARDE-0x02000000)/4096;if(ZOEKEN_INDEX>=sizeof(page_Lijst)||page_Lijst[ZOEKEN_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}page_Lijst[ZOEKEN_INDEX]=1;}
            Volgende_item+=(바이트들+4095)&~(size_t)4095;
        }else if(gegevens_functie.TYPE_gebied==4){if(gegevens_functie.파일영역크기>4096-부가정보)return -1;memcpy(kopie+부가정보,원본자료+gegevens_functie.VERSCHUIVING_WAARDE,gegevens_functie.파일영역크기);gegevens_functie.VERSCHUIVING_WAARDE=부가정보;부가정보+=gegevens_functie.파일영역크기;}
        else if(gegevens_functie.TYPE_gebied!=0&&gegevens_functie.TYPE_gebied!=6&&gegevens_functie.TYPE_gebied!=0x6474e551)return -1;
        memcpy(kopie+uitvoerbaar_header.app_header_VERSCHUIVING+순번*sizeof(gegevens_functie),&gegevens_functie,sizeof(gegevens_functie));
    }
    if(!geldig_beginpunt)return -1;
    intptr_t bestandsingang=사용자호출(3,(uintptr_t)Naam,577,0600,0,0,0);if(bestandsingang<0){printf("cc: cannot create output file, error %d\n",(int)bestandsingang);return -1;}
    intptr_t 쓴수=사용자호출(1,bestandsingang,(uintptr_t)kopie,Volgende_item,0,0,0);사용자호출(4,bestandsingang,0,0,0,0,0);return 쓴수==(intptr_t)Volgende_item?0:-1;
}
int START_gebruiker_app(int methode_MODUS){
    char invoer[256],선택항목[256],uitvoer[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(methode_MODUS?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)invoer,sizeof(invoer),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(invoer,"--version")||!strcmp(invoer,"-version"))){printf(methode_MODUS?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)uitvoer,sizeof(uitvoer),0,0,0)<0)return 2;}
    if(!strcmp(invoer,uitvoer)){printf("cc: input and output must differ\n");return 2;}
    TCCState*tekenreeks_gegevens=tcc_new();if(!tekenreeks_gegevens)return 1;
    tcc_undefine_symbol(tekenreeks_gegevens,"__linux__");tcc_undefine_symbol(tekenreeks_gegevens,"__linux");tcc_undefine_symbol(tekenreeks_gegevens,"linux");
    tcc_undefine_symbol(tekenreeks_gegevens,"__unix__");tcc_undefine_symbol(tekenreeks_gegevens,"__unix");tcc_undefine_symbol(tekenreeks_gegevens,"unix");
    tcc_undefine_symbol(tekenreeks_gegevens,"__STDC_HOSTED__");tcc_define_symbol(tekenreeks_gegevens,"__STDC_HOSTED__","0");tcc_define_symbol(tekenreeks_gegevens,"__JKOROS__","1");
    tcc_set_options(tekenreeks_gegevens,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(tekenreeks_gegevens,"/sdk/include");
    int 반환값=tcc_set_output_type(tekenreeks_gegevens,TCC_OUTPUT_EXE);
    if(!반환값){if(methode_MODUS){const char*원본자료=자바미리번역원문(invoer);반환값=원본자료?tcc_compile_string(tekenreeks_gegevens,원본자료):-1;}else 반환값=tcc_add_file(tekenreeks_gegevens,invoer);}
    if(!반환값)반환값=tcc_add_file(tekenreeks_gegevens,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(tekenreeks_gegevens,"/sdk/lib/crt.o");
    if(!반환값&&methode_MODUS)반환값=tcc_add_file(tekenreeks_gegevens,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(tekenreeks_gegevens,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(tekenreeks_gegevens,"/@cc-output");
    if(!반환값)반환값=publiceren_invoer(uitvoer);
    tcc_delete(tekenreeks_gegevens);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(methode_MODUS?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",uitvoer);return 0;
}
