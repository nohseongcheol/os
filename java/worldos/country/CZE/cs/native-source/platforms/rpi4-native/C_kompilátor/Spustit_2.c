#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_výstup(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikátor_HODNOTA[16];uint16_t TYP_oblast,počítač_TYP;uint32_t číslo_verze;uint64_t vstupní_bod,program_Nadpis_POSUN,záhlaví_oddílu_POSUN;uint32_t konfigurace_BITS;uint16_t Velikost,program_Nadpis_změnit_velikost,program_Nadpis_POČET,záhlaví_oddílu_změnit_velikost,záhlaví_oddílu_POČET,oddíl_název_tabulka; } Nadpis_HODNOTA;
typedef struct {uint32_t TYP_oblast,konfigurace_BITS;uint64_t POSUN_HODNOTA,Adresa,물리주소,파일영역크기,기억영역크기,zarovnat_mez;} segment_HODNOTA;
static unsigned char image[16384];
static int publikovat_položka(const char *Název){
    size_t zboží_POČET;const unsigned char*원본자료=C_výstup(&zboží_POČET);if(zboží_POČET<sizeof(Nadpis_HODNOTA))return -1;
    Nadpis_HODNOTA spustitelný_Nadpis;memcpy(&spustitelný_Nadpis,원본자료,sizeof(spustitelný_Nadpis));
    if(spustitelný_Nadpis.TYP_oblast!=2||spustitelný_Nadpis.počítač_TYP!=183||spustitelný_Nadpis.program_Nadpis_změnit_velikost!=sizeof(segment_HODNOTA)||!spustitelný_Nadpis.program_Nadpis_POČET||spustitelný_Nadpis.program_Nadpis_POČET>16||spustitelný_Nadpis.program_Nadpis_POSUN>zboží_POČET||spustitelný_Nadpis.program_Nadpis_POČET*sizeof(segment_HODNOTA)>zboží_POČET-spustitelný_Nadpis.program_Nadpis_POSUN)return -1;
    spustitelný_Nadpis.program_Nadpis_POSUN=sizeof(spustitelný_Nadpis);spustitelný_Nadpis.záhlaví_oddílu_POSUN=spustitelný_Nadpis.záhlaví_oddílu_POČET=spustitelný_Nadpis.záhlaví_oddílu_změnit_velikost=spustitelný_Nadpis.oddíl_název_tabulka=0;memcpy(image,&spustitelný_Nadpis,sizeof(spustitelný_Nadpis));
    size_t 부가정보=sizeof(spustitelný_Nadpis)+spustitelný_Nadpis.program_Nadpis_POČET*sizeof(segment_HODNOTA),Další_zboží=4096;unsigned char stránka_Seznam[3072]={0};int platný_vstupní_bod=0;
    for(unsigned 순번=0;순번<spustitelný_Nadpis.program_Nadpis_POČET;순번++){
        segment_HODNOTA data_pozice;Nadpis_HODNOTA 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_pozice,원본자료+원본.program_Nadpis_POSUN+순번*sizeof(data_pozice),sizeof(data_pozice));
        if(data_pozice.POSUN_HODNOTA>zboží_POČET||data_pozice.파일영역크기>zboží_POČET-data_pozice.POSUN_HODNOTA||data_pozice.파일영역크기>data_pozice.기억영역크기)return -1;
        if(data_pozice.TYP_oblast==1){
            if((data_pozice.konfigurace_BITS&~7u)||!(data_pozice.konfigurace_BITS&4)||(data_pozice.konfigurace_BITS&3)==3||data_pozice.Adresa<0x02000000||data_pozice.Adresa>0x02c00000||data_pozice.기억영역크기>0x02c00000-data_pozice.Adresa)return -1;
            if((data_pozice.konfigurace_BITS&1)&&spustitelný_Nadpis.vstupní_bod>=data_pozice.Adresa&&spustitelný_Nadpis.vstupní_bod-data_pozice.Adresa<data_pozice.파일영역크기&&!(spustitelný_Nadpis.vstupní_bod&3))platný_vstupní_bod=1;
            size_t 선행값=data_pozice.Adresa&4095,바이트들=data_pozice.파일영역크기?선행값+data_pozice.파일영역크기:0;
            if(Další_zboží>sizeof(image)||바이트들>sizeof(image)-Další_zboží){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Další_zboží+바이트들),(unsigned)sizeof(image));return -1;}
            if(바이트들)memcpy(image+Další_zboží+선행값,원본자료+data_pozice.POSUN_HODNOTA,data_pozice.파일영역크기);
            data_pozice.Adresa-=선행값;data_pozice.물리주소=data_pozice.Adresa;data_pozice.기억영역크기+=선행값;data_pozice.파일영역크기=바이트들;data_pozice.POSUN_HODNOTA=Další_zboží;data_pozice.zarovnat_mez=4096;
            for(uint64_t stránka_HODNOTA=data_pozice.Adresa;stránka_HODNOTA<data_pozice.Adresa+data_pozice.기억영역크기;stránka_HODNOTA+=4096){unsigned VYHLEDAT_INDEX=(stránka_HODNOTA-0x02000000)/4096;if(VYHLEDAT_INDEX>=sizeof(stránka_Seznam)||stránka_Seznam[VYHLEDAT_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}stránka_Seznam[VYHLEDAT_INDEX]=1;}
            Další_zboží+=(바이트들+4095)&~(size_t)4095;
        }else if(data_pozice.TYP_oblast==4){if(data_pozice.파일영역크기>4096-부가정보)return -1;memcpy(image+부가정보,원본자료+data_pozice.POSUN_HODNOTA,data_pozice.파일영역크기);data_pozice.POSUN_HODNOTA=부가정보;부가정보+=data_pozice.파일영역크기;}
        else if(data_pozice.TYP_oblast!=0&&data_pozice.TYP_oblast!=6&&data_pozice.TYP_oblast!=0x6474e551)return -1;
        memcpy(image+spustitelný_Nadpis.program_Nadpis_POSUN+순번*sizeof(data_pozice),&data_pozice,sizeof(data_pozice));
    }
    if(!platný_vstupní_bod)return -1;
    intptr_t popisovač_souboru=사용자호출(3,(uintptr_t)Název,577,0600,0,0,0);if(popisovač_souboru<0){printf("cc: cannot create output file, error %d\n",(int)popisovač_souboru);return -1;}
    intptr_t 쓴수=사용자호출(1,popisovač_souboru,(uintptr_t)image,Další_zboží,0,0,0);사용자호출(4,popisovač_souboru,0,0,0,0,0);return 쓴수==(intptr_t)Další_zboží?0:-1;
}
int START_uživatel_program(int metoda_MODE){
    char vstup[256],선택항목[256],výstup[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metoda_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)vstup,sizeof(vstup),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(vstup,"--version")||!strcmp(vstup,"-version"))){printf(metoda_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)výstup,sizeof(výstup),0,0,0)<0)return 2;}
    if(!strcmp(vstup,výstup)){printf("cc: input and output must differ\n");return 2;}
    TCCState*řetězec_data=tcc_new();if(!řetězec_data)return 1;
    tcc_undefine_symbol(řetězec_data,"__linux__");tcc_undefine_symbol(řetězec_data,"__linux");tcc_undefine_symbol(řetězec_data,"linux");
    tcc_undefine_symbol(řetězec_data,"__unix__");tcc_undefine_symbol(řetězec_data,"__unix");tcc_undefine_symbol(řetězec_data,"unix");
    tcc_undefine_symbol(řetězec_data,"__STDC_HOSTED__");tcc_define_symbol(řetězec_data,"__STDC_HOSTED__","0");tcc_define_symbol(řetězec_data,"__JKOROS__","1");
    tcc_set_options(řetězec_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(řetězec_data,"/sdk/include");
    int 반환값=tcc_set_output_type(řetězec_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metoda_MODE){const char*원본자료=자바미리번역원문(vstup);반환값=원본자료?tcc_compile_string(řetězec_data,원본자료):-1;}else 반환값=tcc_add_file(řetězec_data,vstup);}
    if(!반환값)반환값=tcc_add_file(řetězec_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(řetězec_data,"/sdk/lib/crt.o");
    if(!반환값&&metoda_MODE)반환값=tcc_add_file(řetězec_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(řetězec_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(řetězec_data,"/@cc-output");
    if(!반환값)반환값=publikovat_položka(výstup);
    tcc_delete(řetězec_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metoda_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",výstup);return 0;
}
