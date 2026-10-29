#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikatzaile_balio[16];uint16_t MOTA_Kategoria,gailu_MOTA;uint32_t 판번호;uint64_t sarrera_p,aplik_goiburu_Geruzak,atalaren_goiburu_Geruzak;uint32_t konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna;uint16_t Tamaina,프로그램머리크기,aplik_goiburu_ZENBATU,구역머리크기,atalaren_goiburu_ZENBATU,sekzio_izen_taula; } goiburu_balio;
typedef struct {uint32_t MOTA_Kategoria,konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna;uint64_t Geruzak_balio,helbide,물리주소,파일영역크기,기억영역크기,맞춤;} segmentu_balio;
static unsigned char irudi[16384];
static int argitaratu_sarrera(const char *Izena){
    size_t elementu_ZENBATU;const unsigned char*원본자료=시언어출력(&elementu_ZENBATU);if(elementu_ZENBATU<sizeof(goiburu_balio))return -1;
    goiburu_balio 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.MOTA_Kategoria!=2||실행머리.gailu_MOTA!=183||실행머리.프로그램머리크기!=sizeof(segmentu_balio)||!실행머리.aplik_goiburu_ZENBATU||실행머리.aplik_goiburu_ZENBATU>16||실행머리.aplik_goiburu_Geruzak>elementu_ZENBATU||실행머리.aplik_goiburu_ZENBATU*sizeof(segmentu_balio)>elementu_ZENBATU-실행머리.aplik_goiburu_Geruzak)return -1;
    실행머리.aplik_goiburu_Geruzak=sizeof(실행머리);실행머리.atalaren_goiburu_Geruzak=실행머리.atalaren_goiburu_ZENBATU=실행머리.구역머리크기=실행머리.sekzio_izen_taula=0;memcpy(irudi,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.aplik_goiburu_ZENBATU*sizeof(segmentu_balio),Hurrengoa_elementu=4096;unsigned char orri_Zerrenda[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.aplik_goiburu_ZENBATU;순번++){
        segmentu_balio datuak_kargu;goiburu_balio 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&datuak_kargu,원본자료+원본.aplik_goiburu_Geruzak+순번*sizeof(datuak_kargu),sizeof(datuak_kargu));
        if(datuak_kargu.Geruzak_balio>elementu_ZENBATU||datuak_kargu.파일영역크기>elementu_ZENBATU-datuak_kargu.Geruzak_balio||datuak_kargu.파일영역크기>datuak_kargu.기억영역크기)return -1;
        if(datuak_kargu.MOTA_Kategoria==1){
            if((datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&~7u)||!(datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&4)||(datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&3)==3||datuak_kargu.helbide<0x02000000||datuak_kargu.helbide>0x02c00000||datuak_kargu.기억영역크기>0x02c00000-datuak_kargu.helbide)return -1;
            if((datuak_kargu.konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&1)&&실행머리.sarrera_p>=datuak_kargu.helbide&&실행머리.sarrera_p-datuak_kargu.helbide<datuak_kargu.파일영역크기&&!(실행머리.sarrera_p&3))진입점정상=1;
            size_t 선행값=datuak_kargu.helbide&4095,바이트들=datuak_kargu.파일영역크기?선행값+datuak_kargu.파일영역크기:0;
            if(Hurrengoa_elementu>sizeof(irudi)||바이트들>sizeof(irudi)-Hurrengoa_elementu){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Hurrengoa_elementu+바이트들),(unsigned)sizeof(irudi));return -1;}
            if(바이트들)memcpy(irudi+Hurrengoa_elementu+선행값,원본자료+datuak_kargu.Geruzak_balio,datuak_kargu.파일영역크기);
            datuak_kargu.helbide-=선행값;datuak_kargu.물리주소=datuak_kargu.helbide;datuak_kargu.기억영역크기+=선행값;datuak_kargu.파일영역크기=바이트들;datuak_kargu.Geruzak_balio=Hurrengoa_elementu;datuak_kargu.맞춤=4096;
            for(uint64_t orri_balio=datuak_kargu.helbide;orri_balio<datuak_kargu.helbide+datuak_kargu.기억영역크기;orri_balio+=4096){unsigned BEGIRATU_INDIZE=(orri_balio-0x02000000)/4096;if(BEGIRATU_INDIZE>=sizeof(orri_Zerrenda)||orri_Zerrenda[BEGIRATU_INDIZE]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}orri_Zerrenda[BEGIRATU_INDIZE]=1;}
            Hurrengoa_elementu+=(바이트들+4095)&~(size_t)4095;
        }else if(datuak_kargu.MOTA_Kategoria==4){if(datuak_kargu.파일영역크기>4096-부가정보)return -1;memcpy(irudi+부가정보,원본자료+datuak_kargu.Geruzak_balio,datuak_kargu.파일영역크기);datuak_kargu.Geruzak_balio=부가정보;부가정보+=datuak_kargu.파일영역크기;}
        else if(datuak_kargu.MOTA_Kategoria!=0&&datuak_kargu.MOTA_Kategoria!=6&&datuak_kargu.MOTA_Kategoria!=0x6474e551)return -1;
        memcpy(irudi+실행머리.aplik_goiburu_Geruzak+순번*sizeof(datuak_kargu),&datuak_kargu,sizeof(datuak_kargu));
    }
    if(!진입점정상)return -1;
    intptr_t fitxategi_helduleku=사용자호출(3,(uintptr_t)Izena,577,0600,0,0,0);if(fitxategi_helduleku<0){printf("cc: cannot create output file, error %d\n",(int)fitxategi_helduleku);return -1;}
    intptr_t 쓴수=사용자호출(1,fitxategi_helduleku,(uintptr_t)irudi,Hurrengoa_elementu,0,0,0);사용자호출(4,fitxategi_helduleku,0,0,0,0,0);return 쓴수==(intptr_t)Hurrengoa_elementu?0:-1;
}
int HASI_erabiltzaile_aplik(int 방식){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(방식?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(방식?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*kate_datuak=tcc_new();if(!kate_datuak)return 1;
    tcc_undefine_symbol(kate_datuak,"__linux__");tcc_undefine_symbol(kate_datuak,"__linux");tcc_undefine_symbol(kate_datuak,"linux");
    tcc_undefine_symbol(kate_datuak,"__unix__");tcc_undefine_symbol(kate_datuak,"__unix");tcc_undefine_symbol(kate_datuak,"unix");
    tcc_undefine_symbol(kate_datuak,"__STDC_HOSTED__");tcc_define_symbol(kate_datuak,"__STDC_HOSTED__","0");tcc_define_symbol(kate_datuak,"__JKOROS__","1");
    tcc_set_options(kate_datuak,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(kate_datuak,"/sdk/include");
    int 반환값=tcc_set_output_type(kate_datuak,TCC_OUTPUT_EXE);
    if(!반환값){if(방식){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(kate_datuak,원본자료):-1;}else 반환값=tcc_add_file(kate_datuak,입력결과);}
    if(!반환값)반환값=tcc_add_file(kate_datuak,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(kate_datuak,"/sdk/lib/crt.o");
    if(!반환값&&방식)반환값=tcc_add_file(kate_datuak,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(kate_datuak,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(kate_datuak,"/@cc-output");
    if(!반환값)반환값=argitaratu_sarrera(출력결과);
    tcc_delete(kate_datuak);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(방식?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
