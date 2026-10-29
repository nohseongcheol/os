#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VALUE[16];uint16_t TYPE_područje,stroj_TYPE;uint32_t broj_verzije;uint64_t unos_p,program_Zaglavlje_pomak,zaglavlje_sekcije_pomak;uint32_t konfiguracija_Pozadinski_pametni_servis_za_transfer;uint16_t Veličina,program_Zaglavlje_promijeniti_veličinu,program_Zaglavlje_COUNT,zaglavlje_sekcije_promijeniti_veličinu,zaglavlje_sekcije_COUNT,sekcija_naziv_tablica; } Zaglavlje_VALUE;
typedef struct {uint32_t TYPE_područje,konfiguracija_Pozadinski_pametni_servis_za_transfer;uint64_t pomak_VALUE,adresa,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int objavi_unos(const char *Ime){
    size_t artikl_COUNT;const unsigned char*원본자료=시언어출력(&artikl_COUNT);if(artikl_COUNT<sizeof(Zaglavlje_VALUE))return -1;
    Zaglavlje_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_područje!=2||실행머리.stroj_TYPE!=183||실행머리.program_Zaglavlje_promijeniti_veličinu!=sizeof(segment_VALUE)||!실행머리.program_Zaglavlje_COUNT||실행머리.program_Zaglavlje_COUNT>16||실행머리.program_Zaglavlje_pomak>artikl_COUNT||실행머리.program_Zaglavlje_COUNT*sizeof(segment_VALUE)>artikl_COUNT-실행머리.program_Zaglavlje_pomak)return -1;
    실행머리.program_Zaglavlje_pomak=sizeof(실행머리);실행머리.zaglavlje_sekcije_pomak=실행머리.zaglavlje_sekcije_COUNT=실행머리.zaglavlje_sekcije_promijeniti_veličinu=실행머리.sekcija_naziv_tablica=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.program_Zaglavlje_COUNT*sizeof(segment_VALUE),Dalje_artikl=4096;unsigned char dojaviti_Popis[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.program_Zaglavlje_COUNT;순번++){
        segment_VALUE podaci_položaj;Zaglavlje_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&podaci_položaj,원본자료+원본.program_Zaglavlje_pomak+순번*sizeof(podaci_položaj),sizeof(podaci_položaj));
        if(podaci_položaj.pomak_VALUE>artikl_COUNT||podaci_položaj.파일영역크기>artikl_COUNT-podaci_položaj.pomak_VALUE||podaci_položaj.파일영역크기>podaci_položaj.기억영역크기)return -1;
        if(podaci_položaj.TYPE_područje==1){
            if((podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer&~7u)||!(podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer&4)||(podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer&3)==3||podaci_položaj.adresa<0x02000000||podaci_položaj.adresa>0x02c00000||podaci_položaj.기억영역크기>0x02c00000-podaci_položaj.adresa)return -1;
            if((podaci_položaj.konfiguracija_Pozadinski_pametni_servis_za_transfer&1)&&실행머리.unos_p>=podaci_položaj.adresa&&실행머리.unos_p-podaci_položaj.adresa<podaci_položaj.파일영역크기&&!(실행머리.unos_p&3))진입점정상=1;
            size_t 선행값=podaci_položaj.adresa&4095,바이트들=podaci_položaj.파일영역크기?선행값+podaci_položaj.파일영역크기:0;
            if(Dalje_artikl>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Dalje_artikl){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Dalje_artikl+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Dalje_artikl+선행값,원본자료+podaci_položaj.pomak_VALUE,podaci_položaj.파일영역크기);
            podaci_položaj.adresa-=선행값;podaci_položaj.물리주소=podaci_položaj.adresa;podaci_položaj.기억영역크기+=선행값;podaci_položaj.파일영역크기=바이트들;podaci_položaj.pomak_VALUE=Dalje_artikl;podaci_položaj.맞춤=4096;
            for(uint64_t dojaviti_VALUE=podaci_položaj.adresa;dojaviti_VALUE<podaci_položaj.adresa+podaci_položaj.기억영역크기;dojaviti_VALUE+=4096){unsigned LOOKUP_INDEX=(dojaviti_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(dojaviti_Popis)||dojaviti_Popis[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}dojaviti_Popis[LOOKUP_INDEX]=1;}
            Dalje_artikl+=(바이트들+4095)&~(size_t)4095;
        }else if(podaci_položaj.TYPE_područje==4){if(podaci_položaj.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+podaci_položaj.pomak_VALUE,podaci_položaj.파일영역크기);podaci_položaj.pomak_VALUE=부가정보;부가정보+=podaci_položaj.파일영역크기;}
        else if(podaci_položaj.TYPE_područje!=0&&podaci_položaj.TYPE_područje!=6&&podaci_položaj.TYPE_područje!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.program_Zaglavlje_pomak+순번*sizeof(podaci_položaj),&podaci_položaj,sizeof(podaci_položaj));
    }
    if(!진입점정상)return -1;
    intptr_t Datoteka_ustroj=사용자호출(3,(uintptr_t)Ime,577,0600,0,0,0);if(Datoteka_ustroj<0){printf("cc: cannot create output file, error %d\n",(int)Datoteka_ustroj);return -1;}
    intptr_t 쓴수=사용자호출(1,Datoteka_ustroj,(uintptr_t)IMAGE,Dalje_artikl,0,0,0);사용자호출(4,Datoteka_ustroj,0,0,0,0,0);return 쓴수==(intptr_t)Dalje_artikl?0:-1;
}
int START_korisnik_program(int postupak_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(postupak_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(postupak_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*niz_podaci=tcc_new();if(!niz_podaci)return 1;
    tcc_undefine_symbol(niz_podaci,"__linux__");tcc_undefine_symbol(niz_podaci,"__linux");tcc_undefine_symbol(niz_podaci,"linux");
    tcc_undefine_symbol(niz_podaci,"__unix__");tcc_undefine_symbol(niz_podaci,"__unix");tcc_undefine_symbol(niz_podaci,"unix");
    tcc_undefine_symbol(niz_podaci,"__STDC_HOSTED__");tcc_define_symbol(niz_podaci,"__STDC_HOSTED__","0");tcc_define_symbol(niz_podaci,"__JKOROS__","1");
    tcc_set_options(niz_podaci,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(niz_podaci,"/sdk/include");
    int 반환값=tcc_set_output_type(niz_podaci,TCC_OUTPUT_EXE);
    if(!반환값){if(postupak_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(niz_podaci,원본자료):-1;}else 반환값=tcc_add_file(niz_podaci,입력결과);}
    if(!반환값)반환값=tcc_add_file(niz_podaci,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(niz_podaci,"/sdk/lib/crt.o");
    if(!반환값&&postupak_MODE)반환값=tcc_add_file(niz_podaci,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(niz_podaci,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(niz_podaci,"/@cc-output");
    if(!반환값)반환값=objavi_unos(출력결과);
    tcc_delete(niz_podaci);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(postupak_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
