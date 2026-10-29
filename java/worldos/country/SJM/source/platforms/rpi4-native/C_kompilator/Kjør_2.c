#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_produksjon(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VERDI[16];uint16_t Type_område,maskin_Type;uint32_t versjonsnummer;uint64_t inngangspunkt,app_Topptekst_FORSKYVNING,deloverskrift_FORSKYVNING;uint32_t konfigurasjon_BITS;uint16_t Størrelse,app_Topptekst_skalere,app_Topptekst_ANTALL,deloverskrift_skalere,deloverskrift_ANTALL,inndeling_navn_tabell; } Topptekst_VERDI;
typedef struct {uint32_t Type_område,konfigurasjon_BITS;uint64_t FORSKYVNING_VERDI,e_post,물리주소,파일영역크기,기억영역크기,justere_grense;} segment_VERDI;
static unsigned char BILDE[16384];
static int publisere_oppføring(const char *Navn){
    size_t vare_ANTALL;const unsigned char*원본자료=C_produksjon(&vare_ANTALL);if(vare_ANTALL<sizeof(Topptekst_VERDI))return -1;
    Topptekst_VERDI kjørbar_fil_Topptekst;memcpy(&kjørbar_fil_Topptekst,원본자료,sizeof(kjørbar_fil_Topptekst));
    if(kjørbar_fil_Topptekst.Type_område!=2||kjørbar_fil_Topptekst.maskin_Type!=183||kjørbar_fil_Topptekst.app_Topptekst_skalere!=sizeof(segment_VERDI)||!kjørbar_fil_Topptekst.app_Topptekst_ANTALL||kjørbar_fil_Topptekst.app_Topptekst_ANTALL>16||kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING>vare_ANTALL||kjørbar_fil_Topptekst.app_Topptekst_ANTALL*sizeof(segment_VERDI)>vare_ANTALL-kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING)return -1;
    kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING=sizeof(kjørbar_fil_Topptekst);kjørbar_fil_Topptekst.deloverskrift_FORSKYVNING=kjørbar_fil_Topptekst.deloverskrift_ANTALL=kjørbar_fil_Topptekst.deloverskrift_skalere=kjørbar_fil_Topptekst.inndeling_navn_tabell=0;memcpy(BILDE,&kjørbar_fil_Topptekst,sizeof(kjørbar_fil_Topptekst));
    size_t 부가정보=sizeof(kjørbar_fil_Topptekst)+kjørbar_fil_Topptekst.app_Topptekst_ANTALL*sizeof(segment_VERDI),Neste_vare=4096;unsigned char page_Liste[3072]={0};int gyldig_inngangspunkt=0;
    for(unsigned 순번=0;순번<kjørbar_fil_Topptekst.app_Topptekst_ANTALL;순번++){
        segment_VERDI data_plassere;Topptekst_VERDI 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_plassere,원본자료+원본.app_Topptekst_FORSKYVNING+순번*sizeof(data_plassere),sizeof(data_plassere));
        if(data_plassere.FORSKYVNING_VERDI>vare_ANTALL||data_plassere.파일영역크기>vare_ANTALL-data_plassere.FORSKYVNING_VERDI||data_plassere.파일영역크기>data_plassere.기억영역크기)return -1;
        if(data_plassere.Type_område==1){
            if((data_plassere.konfigurasjon_BITS&~7u)||!(data_plassere.konfigurasjon_BITS&4)||(data_plassere.konfigurasjon_BITS&3)==3||data_plassere.e_post<0x02000000||data_plassere.e_post>0x02c00000||data_plassere.기억영역크기>0x02c00000-data_plassere.e_post)return -1;
            if((data_plassere.konfigurasjon_BITS&1)&&kjørbar_fil_Topptekst.inngangspunkt>=data_plassere.e_post&&kjørbar_fil_Topptekst.inngangspunkt-data_plassere.e_post<data_plassere.파일영역크기&&!(kjørbar_fil_Topptekst.inngangspunkt&3))gyldig_inngangspunkt=1;
            size_t 선행값=data_plassere.e_post&4095,바이트들=data_plassere.파일영역크기?선행값+data_plassere.파일영역크기:0;
            if(Neste_vare>sizeof(BILDE)||바이트들>sizeof(BILDE)-Neste_vare){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Neste_vare+바이트들),(unsigned)sizeof(BILDE));return -1;}
            if(바이트들)memcpy(BILDE+Neste_vare+선행값,원본자료+data_plassere.FORSKYVNING_VERDI,data_plassere.파일영역크기);
            data_plassere.e_post-=선행값;data_plassere.물리주소=data_plassere.e_post;data_plassere.기억영역크기+=선행값;data_plassere.파일영역크기=바이트들;data_plassere.FORSKYVNING_VERDI=Neste_vare;data_plassere.justere_grense=4096;
            for(uint64_t page_VERDI=data_plassere.e_post;page_VERDI<data_plassere.e_post+data_plassere.기억영역크기;page_VERDI+=4096){unsigned Oppslag_INDEKS=(page_VERDI-0x02000000)/4096;if(Oppslag_INDEKS>=sizeof(page_Liste)||page_Liste[Oppslag_INDEKS]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}page_Liste[Oppslag_INDEKS]=1;}
            Neste_vare+=(바이트들+4095)&~(size_t)4095;
        }else if(data_plassere.Type_område==4){if(data_plassere.파일영역크기>4096-부가정보)return -1;memcpy(BILDE+부가정보,원본자료+data_plassere.FORSKYVNING_VERDI,data_plassere.파일영역크기);data_plassere.FORSKYVNING_VERDI=부가정보;부가정보+=data_plassere.파일영역크기;}
        else if(data_plassere.Type_område!=0&&data_plassere.Type_område!=6&&data_plassere.Type_område!=0x6474e551)return -1;
        memcpy(BILDE+kjørbar_fil_Topptekst.app_Topptekst_FORSKYVNING+순번*sizeof(data_plassere),&data_plassere,sizeof(data_plassere));
    }
    if(!gyldig_inngangspunkt)return -1;
    intptr_t Fil_håndtak=사용자호출(3,(uintptr_t)Navn,577,0600,0,0,0);if(Fil_håndtak<0){printf("cc: cannot create output file, error %d\n",(int)Fil_håndtak);return -1;}
    intptr_t 쓴수=사용자호출(1,Fil_håndtak,(uintptr_t)BILDE,Neste_vare,0,0,0);사용자호출(4,Fil_håndtak,0,0,0,0,0);return 쓴수==(intptr_t)Neste_vare?0:-1;
}
int START_bruker_app(int metode_MODUS){
    char inndata[256],선택항목[256],produksjon[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metode_MODUS?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)inndata,sizeof(inndata),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(inndata,"--version")||!strcmp(inndata,"-version"))){printf(metode_MODUS?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)produksjon,sizeof(produksjon),0,0,0)<0)return 2;}
    if(!strcmp(inndata,produksjon)){printf("cc: input and output must differ\n");return 2;}
    TCCState*streng_data=tcc_new();if(!streng_data)return 1;
    tcc_undefine_symbol(streng_data,"__linux__");tcc_undefine_symbol(streng_data,"__linux");tcc_undefine_symbol(streng_data,"linux");
    tcc_undefine_symbol(streng_data,"__unix__");tcc_undefine_symbol(streng_data,"__unix");tcc_undefine_symbol(streng_data,"unix");
    tcc_undefine_symbol(streng_data,"__STDC_HOSTED__");tcc_define_symbol(streng_data,"__STDC_HOSTED__","0");tcc_define_symbol(streng_data,"__JKOROS__","1");
    tcc_set_options(streng_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(streng_data,"/sdk/include");
    int 반환값=tcc_set_output_type(streng_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metode_MODUS){const char*원본자료=자바미리번역원문(inndata);반환값=원본자료?tcc_compile_string(streng_data,원본자료):-1;}else 반환값=tcc_add_file(streng_data,inndata);}
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/crt.o");
    if(!반환값&&metode_MODUS)반환값=tcc_add_file(streng_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(streng_data,"/@cc-output");
    if(!반환값)반환값=publisere_oppføring(produksjon);
    tcc_delete(streng_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metode_MODUS?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",produksjon);return 0;
}
