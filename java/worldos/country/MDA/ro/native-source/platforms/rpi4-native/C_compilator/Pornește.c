#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identificator_VALUE[16];uint16_t Tip_zonă,mașină_Tip;uint32_t număr_de_versiune;uint64_t intrare_p,program_Antet_OFFSET,antet_secțiune_OFFSET;uint32_t configurație_Serviciu_de_transfer_inteligent_în_fundal;uint16_t Mărime,program_Antet_dimensiona,program_Antet_COUNT,antet_secțiune_dimensiona,antet_secțiune_COUNT,secțiune_nume_tabel; } Antet_VALUE;
typedef struct {uint32_t Tip_zonă,configurație_Serviciu_de_transfer_inteligent_în_fundal;uint64_t OFFSET_VALUE,adresa,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int publica_intrare(const char *Nume){
    size_t element_COUNT;const unsigned char*원본자료=시언어출력(&element_COUNT);if(element_COUNT<sizeof(Antet_VALUE))return -1;
    Antet_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.Tip_zonă!=2||실행머리.mașină_Tip!=183||실행머리.program_Antet_dimensiona!=sizeof(segment_VALUE)||!실행머리.program_Antet_COUNT||실행머리.program_Antet_COUNT>16||실행머리.program_Antet_OFFSET>element_COUNT||실행머리.program_Antet_COUNT*sizeof(segment_VALUE)>element_COUNT-실행머리.program_Antet_OFFSET)return -1;
    실행머리.program_Antet_OFFSET=sizeof(실행머리);실행머리.antet_secțiune_OFFSET=실행머리.antet_secțiune_COUNT=실행머리.antet_secțiune_dimensiona=실행머리.secțiune_nume_tabel=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.program_Antet_COUNT*sizeof(segment_VALUE),Următorul_element=4096;unsigned char pagina_Listă[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.program_Antet_COUNT;순번++){
        segment_VALUE date_poziție;Antet_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&date_poziție,원본자료+원본.program_Antet_OFFSET+순번*sizeof(date_poziție),sizeof(date_poziție));
        if(date_poziție.OFFSET_VALUE>element_COUNT||date_poziție.파일영역크기>element_COUNT-date_poziție.OFFSET_VALUE||date_poziție.파일영역크기>date_poziție.기억영역크기)return -1;
        if(date_poziție.Tip_zonă==1){
            if((date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal&~7u)||!(date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal&4)||(date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal&3)==3||date_poziție.adresa<0x02000000||date_poziție.adresa>0x02c00000||date_poziție.기억영역크기>0x02c00000-date_poziție.adresa)return -1;
            if((date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal&1)&&실행머리.intrare_p>=date_poziție.adresa&&실행머리.intrare_p-date_poziție.adresa<date_poziție.파일영역크기&&!(실행머리.intrare_p&3))진입점정상=1;
            size_t 선행값=date_poziție.adresa&4095,바이트들=date_poziție.파일영역크기?선행값+date_poziție.파일영역크기:0;
            if(Următorul_element>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Următorul_element){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Următorul_element+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Următorul_element+선행값,원본자료+date_poziție.OFFSET_VALUE,date_poziție.파일영역크기);
            date_poziție.adresa-=선행값;date_poziție.물리주소=date_poziție.adresa;date_poziție.기억영역크기+=선행값;date_poziție.파일영역크기=바이트들;date_poziție.OFFSET_VALUE=Următorul_element;date_poziție.맞춤=4096;
            for(uint64_t pagina_VALUE=date_poziție.adresa;pagina_VALUE<date_poziție.adresa+date_poziție.기억영역크기;pagina_VALUE+=4096){unsigned LOOKUP_INDEX=(pagina_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(pagina_Listă)||pagina_Listă[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}pagina_Listă[LOOKUP_INDEX]=1;}
            Următorul_element+=(바이트들+4095)&~(size_t)4095;
        }else if(date_poziție.Tip_zonă==4){if(date_poziție.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+date_poziție.OFFSET_VALUE,date_poziție.파일영역크기);date_poziție.OFFSET_VALUE=부가정보;부가정보+=date_poziție.파일영역크기;}
        else if(date_poziție.Tip_zonă!=0&&date_poziție.Tip_zonă!=6&&date_poziție.Tip_zonă!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.program_Antet_OFFSET+순번*sizeof(date_poziție),&date_poziție,sizeof(date_poziție));
    }
    if(!진입점정상)return -1;
    intptr_t Fișier_handle=사용자호출(3,(uintptr_t)Nume,577,0600,0,0,0);if(Fișier_handle<0){printf("cc: cannot create output file, error %d\n",(int)Fișier_handle);return -1;}
    intptr_t 쓴수=사용자호출(1,Fișier_handle,(uintptr_t)IMAGE,Următorul_element,0,0,0);사용자호출(4,Fișier_handle,0,0,0,0,0);return 쓴수==(intptr_t)Următorul_element?0:-1;
}
int buta_utilizator_program(int metodă_mod){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metodă_mod?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metodă_mod?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*șir_date=tcc_new();if(!șir_date)return 1;
    tcc_undefine_symbol(șir_date,"__linux__");tcc_undefine_symbol(șir_date,"__linux");tcc_undefine_symbol(șir_date,"linux");
    tcc_undefine_symbol(șir_date,"__unix__");tcc_undefine_symbol(șir_date,"__unix");tcc_undefine_symbol(șir_date,"unix");
    tcc_undefine_symbol(șir_date,"__STDC_HOSTED__");tcc_define_symbol(șir_date,"__STDC_HOSTED__","0");tcc_define_symbol(șir_date,"__JKOROS__","1");
    tcc_set_options(șir_date,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(șir_date,"/sdk/include");
    int 반환값=tcc_set_output_type(șir_date,TCC_OUTPUT_EXE);
    if(!반환값){if(metodă_mod){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(șir_date,원본자료):-1;}else 반환값=tcc_add_file(șir_date,입력결과);}
    if(!반환값)반환값=tcc_add_file(șir_date,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(șir_date,"/sdk/lib/crt.o");
    if(!반환값&&metodă_mod)반환값=tcc_add_file(șir_date,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(șir_date,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(șir_date,"/@cc-output");
    if(!반환값)반환값=publica_intrare(출력결과);
    tcc_delete(șir_date);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metodă_mod?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
