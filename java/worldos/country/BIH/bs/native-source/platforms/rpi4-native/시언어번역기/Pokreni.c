#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VALUE[16];uint16_t TYPE_oblast,mašina_TYPE;uint32_t broj_verzije;uint64_t unos_p,program_Zaglavlje_Pomak,sekcija_Zaglavlje_Pomak;uint32_t 설정비트;uint16_t Veličina,program_Zaglavlje_podesiti_veličinu,program_Zaglavlje_COUNT,sekcija_Zaglavlje_podesiti_veličinu,sekcija_Zaglavlje_COUNT,sekcija_naziv_tabela; } Zaglavlje_VALUE;
typedef struct {uint32_t TYPE_oblast,설정비트;uint64_t Pomak_VALUE,adresa,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int objavi_unos(const char *Naziv){
    size_t stavka_COUNT;const unsigned char*원본자료=시언어출력(&stavka_COUNT);if(stavka_COUNT<sizeof(Zaglavlje_VALUE))return -1;
    Zaglavlje_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_oblast!=2||실행머리.mašina_TYPE!=183||실행머리.program_Zaglavlje_podesiti_veličinu!=sizeof(segment_VALUE)||!실행머리.program_Zaglavlje_COUNT||실행머리.program_Zaglavlje_COUNT>16||실행머리.program_Zaglavlje_Pomak>stavka_COUNT||실행머리.program_Zaglavlje_COUNT*sizeof(segment_VALUE)>stavka_COUNT-실행머리.program_Zaglavlje_Pomak)return -1;
    실행머리.program_Zaglavlje_Pomak=sizeof(실행머리);실행머리.sekcija_Zaglavlje_Pomak=실행머리.sekcija_Zaglavlje_COUNT=실행머리.sekcija_Zaglavlje_podesiti_veličinu=실행머리.sekcija_naziv_tabela=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.program_Zaglavlje_COUNT*sizeof(segment_VALUE),Dalje_stavka=4096;unsigned char stranica_spisak[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.program_Zaglavlje_COUNT;순번++){
        segment_VALUE podaci_položaj;Zaglavlje_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&podaci_položaj,원본자료+원본.program_Zaglavlje_Pomak+순번*sizeof(podaci_položaj),sizeof(podaci_položaj));
        if(podaci_položaj.Pomak_VALUE>stavka_COUNT||podaci_položaj.파일영역크기>stavka_COUNT-podaci_položaj.Pomak_VALUE||podaci_položaj.파일영역크기>podaci_položaj.기억영역크기)return -1;
        if(podaci_položaj.TYPE_oblast==1){
            if((podaci_položaj.설정비트&~7u)||!(podaci_položaj.설정비트&4)||(podaci_položaj.설정비트&3)==3||podaci_položaj.adresa<0x02000000||podaci_položaj.adresa>0x02c00000||podaci_položaj.기억영역크기>0x02c00000-podaci_položaj.adresa)return -1;
            if((podaci_položaj.설정비트&1)&&실행머리.unos_p>=podaci_položaj.adresa&&실행머리.unos_p-podaci_položaj.adresa<podaci_položaj.파일영역크기&&!(실행머리.unos_p&3))진입점정상=1;
            size_t 선행값=podaci_položaj.adresa&4095,바이트들=podaci_položaj.파일영역크기?선행값+podaci_položaj.파일영역크기:0;
            if(Dalje_stavka>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Dalje_stavka){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Dalje_stavka+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Dalje_stavka+선행값,원본자료+podaci_položaj.Pomak_VALUE,podaci_položaj.파일영역크기);
            podaci_položaj.adresa-=선행값;podaci_položaj.물리주소=podaci_položaj.adresa;podaci_položaj.기억영역크기+=선행값;podaci_položaj.파일영역크기=바이트들;podaci_položaj.Pomak_VALUE=Dalje_stavka;podaci_položaj.맞춤=4096;
            for(uint64_t stranica_VALUE=podaci_položaj.adresa;stranica_VALUE<podaci_položaj.adresa+podaci_položaj.기억영역크기;stranica_VALUE+=4096){unsigned LOOKUP_INDEX=(stranica_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(stranica_spisak)||stranica_spisak[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}stranica_spisak[LOOKUP_INDEX]=1;}
            Dalje_stavka+=(바이트들+4095)&~(size_t)4095;
        }else if(podaci_položaj.TYPE_oblast==4){if(podaci_položaj.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+podaci_položaj.Pomak_VALUE,podaci_položaj.파일영역크기);podaci_položaj.Pomak_VALUE=부가정보;부가정보+=podaci_položaj.파일영역크기;}
        else if(podaci_položaj.TYPE_oblast!=0&&podaci_položaj.TYPE_oblast!=6&&podaci_položaj.TYPE_oblast!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.program_Zaglavlje_Pomak+순번*sizeof(podaci_položaj),&podaci_položaj,sizeof(podaci_položaj));
    }
    if(!진입점정상)return -1;
    intptr_t fajl_hvatište=사용자호출(3,(uintptr_t)Naziv,577,0600,0,0,0);if(fajl_hvatište<0){printf("cc: cannot create output file, error %d\n",(int)fajl_hvatište);return -1;}
    intptr_t 쓴수=사용자호출(1,fajl_hvatište,(uintptr_t)IMAGE,Dalje_stavka,0,0,0);사용자호출(4,fajl_hvatište,0,0,0,0,0);return 쓴수==(intptr_t)Dalje_stavka?0:-1;
}
int START_korisnik_program(int metoda_mod){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metoda_mod?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metoda_mod?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*string_podaci=tcc_new();if(!string_podaci)return 1;
    tcc_undefine_symbol(string_podaci,"__linux__");tcc_undefine_symbol(string_podaci,"__linux");tcc_undefine_symbol(string_podaci,"linux");
    tcc_undefine_symbol(string_podaci,"__unix__");tcc_undefine_symbol(string_podaci,"__unix");tcc_undefine_symbol(string_podaci,"unix");
    tcc_undefine_symbol(string_podaci,"__STDC_HOSTED__");tcc_define_symbol(string_podaci,"__STDC_HOSTED__","0");tcc_define_symbol(string_podaci,"__JKOROS__","1");
    tcc_set_options(string_podaci,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(string_podaci,"/sdk/include");
    int 반환값=tcc_set_output_type(string_podaci,TCC_OUTPUT_EXE);
    if(!반환값){if(metoda_mod){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(string_podaci,원본자료):-1;}else 반환값=tcc_add_file(string_podaci,입력결과);}
    if(!반환값)반환값=tcc_add_file(string_podaci,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(string_podaci,"/sdk/lib/crt.o");
    if(!반환값&&metoda_mod)반환값=tcc_add_file(string_podaci,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(string_podaci,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(string_podaci,"/@cc-output");
    if(!반환값)반환값=objavi_unos(출력결과);
    tcc_delete(string_podaci);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metoda_mod?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
