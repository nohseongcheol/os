#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_produktoutput(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VÆRDI[16];uint16_t Type_område,maskine_Type;uint32_t versionsnummer;uint64_t indgangspunkt,app_Header_FORSKYDNING,sektionsoverskrift_FORSKYDNING;uint32_t konfiguration_BITS;uint16_t Størrelse,app_Header_tilpasse_størrelse,app_Header_TÆL,sektionsoverskrift_tilpasse_størrelse,sektionsoverskrift_TÆL,sektion_navn_tabel; } Header_VÆRDI;
typedef struct {uint32_t Type_område,konfiguration_BITS;uint64_t FORSKYDNING_VÆRDI,mail,물리주소,파일영역크기,기억영역크기,justere_grænse;} segment_VÆRDI;
static unsigned char Image[16384];
static int udgive_post(const char *Navn){
    size_t vare_TÆL;const unsigned char*원본자료=C_produktoutput(&vare_TÆL);if(vare_TÆL<sizeof(Header_VÆRDI))return -1;
    Header_VÆRDI eksekverbar_fil_Header;memcpy(&eksekverbar_fil_Header,원본자료,sizeof(eksekverbar_fil_Header));
    if(eksekverbar_fil_Header.Type_område!=2||eksekverbar_fil_Header.maskine_Type!=183||eksekverbar_fil_Header.app_Header_tilpasse_størrelse!=sizeof(segment_VÆRDI)||!eksekverbar_fil_Header.app_Header_TÆL||eksekverbar_fil_Header.app_Header_TÆL>16||eksekverbar_fil_Header.app_Header_FORSKYDNING>vare_TÆL||eksekverbar_fil_Header.app_Header_TÆL*sizeof(segment_VÆRDI)>vare_TÆL-eksekverbar_fil_Header.app_Header_FORSKYDNING)return -1;
    eksekverbar_fil_Header.app_Header_FORSKYDNING=sizeof(eksekverbar_fil_Header);eksekverbar_fil_Header.sektionsoverskrift_FORSKYDNING=eksekverbar_fil_Header.sektionsoverskrift_TÆL=eksekverbar_fil_Header.sektionsoverskrift_tilpasse_størrelse=eksekverbar_fil_Header.sektion_navn_tabel=0;memcpy(Image,&eksekverbar_fil_Header,sizeof(eksekverbar_fil_Header));
    size_t 부가정보=sizeof(eksekverbar_fil_Header)+eksekverbar_fil_Header.app_Header_TÆL*sizeof(segment_VÆRDI),Næste_vare=4096;unsigned char side_Liste[3072]={0};int gyldig_indgangspunkt=0;
    for(unsigned 순번=0;순번<eksekverbar_fil_Header.app_Header_TÆL;순번++){
        segment_VÆRDI data_placere;Header_VÆRDI 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_placere,원본자료+원본.app_Header_FORSKYDNING+순번*sizeof(data_placere),sizeof(data_placere));
        if(data_placere.FORSKYDNING_VÆRDI>vare_TÆL||data_placere.파일영역크기>vare_TÆL-data_placere.FORSKYDNING_VÆRDI||data_placere.파일영역크기>data_placere.기억영역크기)return -1;
        if(data_placere.Type_område==1){
            if((data_placere.konfiguration_BITS&~7u)||!(data_placere.konfiguration_BITS&4)||(data_placere.konfiguration_BITS&3)==3||data_placere.mail<0x02000000||data_placere.mail>0x02c00000||data_placere.기억영역크기>0x02c00000-data_placere.mail)return -1;
            if((data_placere.konfiguration_BITS&1)&&eksekverbar_fil_Header.indgangspunkt>=data_placere.mail&&eksekverbar_fil_Header.indgangspunkt-data_placere.mail<data_placere.파일영역크기&&!(eksekverbar_fil_Header.indgangspunkt&3))gyldig_indgangspunkt=1;
            size_t 선행값=data_placere.mail&4095,바이트들=data_placere.파일영역크기?선행값+data_placere.파일영역크기:0;
            if(Næste_vare>sizeof(Image)||바이트들>sizeof(Image)-Næste_vare){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Næste_vare+바이트들),(unsigned)sizeof(Image));return -1;}
            if(바이트들)memcpy(Image+Næste_vare+선행값,원본자료+data_placere.FORSKYDNING_VÆRDI,data_placere.파일영역크기);
            data_placere.mail-=선행값;data_placere.물리주소=data_placere.mail;data_placere.기억영역크기+=선행값;data_placere.파일영역크기=바이트들;data_placere.FORSKYDNING_VÆRDI=Næste_vare;data_placere.justere_grænse=4096;
            for(uint64_t side_VÆRDI=data_placere.mail;side_VÆRDI<data_placere.mail+data_placere.기억영역크기;side_VÆRDI+=4096){unsigned Opslag_INDEKS=(side_VÆRDI-0x02000000)/4096;if(Opslag_INDEKS>=sizeof(side_Liste)||side_Liste[Opslag_INDEKS]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}side_Liste[Opslag_INDEKS]=1;}
            Næste_vare+=(바이트들+4095)&~(size_t)4095;
        }else if(data_placere.Type_område==4){if(data_placere.파일영역크기>4096-부가정보)return -1;memcpy(Image+부가정보,원본자료+data_placere.FORSKYDNING_VÆRDI,data_placere.파일영역크기);data_placere.FORSKYDNING_VÆRDI=부가정보;부가정보+=data_placere.파일영역크기;}
        else if(data_placere.Type_område!=0&&data_placere.Type_område!=6&&data_placere.Type_område!=0x6474e551)return -1;
        memcpy(Image+eksekverbar_fil_Header.app_Header_FORSKYDNING+순번*sizeof(data_placere),&data_placere,sizeof(data_placere));
    }
    if(!gyldig_indgangspunkt)return -1;
    intptr_t fil_handle=사용자호출(3,(uintptr_t)Navn,577,0600,0,0,0);if(fil_handle<0){printf("cc: cannot create output file, error %d\n",(int)fil_handle);return -1;}
    intptr_t 쓴수=사용자호출(1,fil_handle,(uintptr_t)Image,Næste_vare,0,0,0);사용자호출(4,fil_handle,0,0,0,0,0);return 쓴수==(intptr_t)Næste_vare?0:-1;
}
int START_bruger_app(int metode_HYPPIGST){
    char input[256],선택항목[256],produktoutput[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metode_HYPPIGST?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)input,sizeof(input),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(input,"--version")||!strcmp(input,"-version"))){printf(metode_HYPPIGST?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)produktoutput,sizeof(produktoutput),0,0,0)<0)return 2;}
    if(!strcmp(input,produktoutput)){printf("cc: input and output must differ\n");return 2;}
    TCCState*streng_data=tcc_new();if(!streng_data)return 1;
    tcc_undefine_symbol(streng_data,"__linux__");tcc_undefine_symbol(streng_data,"__linux");tcc_undefine_symbol(streng_data,"linux");
    tcc_undefine_symbol(streng_data,"__unix__");tcc_undefine_symbol(streng_data,"__unix");tcc_undefine_symbol(streng_data,"unix");
    tcc_undefine_symbol(streng_data,"__STDC_HOSTED__");tcc_define_symbol(streng_data,"__STDC_HOSTED__","0");tcc_define_symbol(streng_data,"__JKOROS__","1");
    tcc_set_options(streng_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(streng_data,"/sdk/include");
    int 반환값=tcc_set_output_type(streng_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metode_HYPPIGST){const char*원본자료=자바미리번역원문(input);반환값=원본자료?tcc_compile_string(streng_data,원본자료):-1;}else 반환값=tcc_add_file(streng_data,input);}
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/crt.o");
    if(!반환값&&metode_HYPPIGST)반환값=tcc_add_file(streng_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(streng_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(streng_data,"/@cc-output");
    if(!반환값)반환값=udgive_post(produktoutput);
    tcc_delete(streng_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metode_HYPPIGST?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",produktoutput);return 0;
}
