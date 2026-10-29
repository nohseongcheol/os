#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_produkt_wyjściowy(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identyfikator_WARTOŚĆ[16];uint16_t TYP_obszar,maszyna_TYP;uint32_t numer_wersji;uint64_t punkt_wejścia,program_Nagłówek_przesunąć,nagłówek_sekcji_przesunąć;uint32_t konfiguracja_BITS;uint16_t Rozmiar,program_Nagłówek_zmienić_rozmiar,program_Nagłówek_ILE_LICZB,nagłówek_sekcji_zmienić_rozmiar,nagłówek_sekcji_ILE_LICZB,obszar_nazwa_tabela; } Nagłówek_WARTOŚĆ;
typedef struct {uint32_t TYP_obszar,konfiguracja_BITS;uint64_t przesunąć_WARTOŚĆ_450fc799,Adres,물리주소,파일영역크기,기억영역크기,wyrównać_granica;} odcinek_WARTOŚĆ;
static unsigned char OBRAZ[16384];
static int publikować_wpis(const char *Nazwa){
    size_t towar_ILE_LICZB;const unsigned char*원본자료=C_produkt_wyjściowy(&towar_ILE_LICZB);if(towar_ILE_LICZB<sizeof(Nagłówek_WARTOŚĆ))return -1;
    Nagłówek_WARTOŚĆ wykonywalny_Nagłówek;memcpy(&wykonywalny_Nagłówek,원본자료,sizeof(wykonywalny_Nagłówek));
    if(wykonywalny_Nagłówek.TYP_obszar!=2||wykonywalny_Nagłówek.maszyna_TYP!=183||wykonywalny_Nagłówek.program_Nagłówek_zmienić_rozmiar!=sizeof(odcinek_WARTOŚĆ)||!wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB||wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB>16||wykonywalny_Nagłówek.program_Nagłówek_przesunąć>towar_ILE_LICZB||wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB*sizeof(odcinek_WARTOŚĆ)>towar_ILE_LICZB-wykonywalny_Nagłówek.program_Nagłówek_przesunąć)return -1;
    wykonywalny_Nagłówek.program_Nagłówek_przesunąć=sizeof(wykonywalny_Nagłówek);wykonywalny_Nagłówek.nagłówek_sekcji_przesunąć=wykonywalny_Nagłówek.nagłówek_sekcji_ILE_LICZB=wykonywalny_Nagłówek.nagłówek_sekcji_zmienić_rozmiar=wykonywalny_Nagłówek.obszar_nazwa_tabela=0;memcpy(OBRAZ,&wykonywalny_Nagłówek,sizeof(wykonywalny_Nagłówek));
    size_t 부가정보=sizeof(wykonywalny_Nagłówek)+wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB*sizeof(odcinek_WARTOŚĆ),Dalej_towar=4096;unsigned char strona_Lista[3072]={0};int prawidłowy_punkt_wejścia=0;
    for(unsigned 순번=0;순번<wykonywalny_Nagłówek.program_Nagłówek_ILE_LICZB;순번++){
        odcinek_WARTOŚĆ dane_stanowisko;Nagłówek_WARTOŚĆ 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&dane_stanowisko,원본자료+원본.program_Nagłówek_przesunąć+순번*sizeof(dane_stanowisko),sizeof(dane_stanowisko));
        if(dane_stanowisko.przesunąć_WARTOŚĆ_450fc799>towar_ILE_LICZB||dane_stanowisko.파일영역크기>towar_ILE_LICZB-dane_stanowisko.przesunąć_WARTOŚĆ_450fc799||dane_stanowisko.파일영역크기>dane_stanowisko.기억영역크기)return -1;
        if(dane_stanowisko.TYP_obszar==1){
            if((dane_stanowisko.konfiguracja_BITS&~7u)||!(dane_stanowisko.konfiguracja_BITS&4)||(dane_stanowisko.konfiguracja_BITS&3)==3||dane_stanowisko.Adres<0x02000000||dane_stanowisko.Adres>0x02c00000||dane_stanowisko.기억영역크기>0x02c00000-dane_stanowisko.Adres)return -1;
            if((dane_stanowisko.konfiguracja_BITS&1)&&wykonywalny_Nagłówek.punkt_wejścia>=dane_stanowisko.Adres&&wykonywalny_Nagłówek.punkt_wejścia-dane_stanowisko.Adres<dane_stanowisko.파일영역크기&&!(wykonywalny_Nagłówek.punkt_wejścia&3))prawidłowy_punkt_wejścia=1;
            size_t 선행값=dane_stanowisko.Adres&4095,바이트들=dane_stanowisko.파일영역크기?선행값+dane_stanowisko.파일영역크기:0;
            if(Dalej_towar>sizeof(OBRAZ)||바이트들>sizeof(OBRAZ)-Dalej_towar){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Dalej_towar+바이트들),(unsigned)sizeof(OBRAZ));return -1;}
            if(바이트들)memcpy(OBRAZ+Dalej_towar+선행값,원본자료+dane_stanowisko.przesunąć_WARTOŚĆ_450fc799,dane_stanowisko.파일영역크기);
            dane_stanowisko.Adres-=선행값;dane_stanowisko.물리주소=dane_stanowisko.Adres;dane_stanowisko.기억영역크기+=선행값;dane_stanowisko.파일영역크기=바이트들;dane_stanowisko.przesunąć_WARTOŚĆ_450fc799=Dalej_towar;dane_stanowisko.wyrównać_granica=4096;
            for(uint64_t strona_WARTOŚĆ=dane_stanowisko.Adres;strona_WARTOŚĆ<dane_stanowisko.Adres+dane_stanowisko.기억영역크기;strona_WARTOŚĆ+=4096){unsigned WYSZUKAJ_INDEKS=(strona_WARTOŚĆ-0x02000000)/4096;if(WYSZUKAJ_INDEKS>=sizeof(strona_Lista)||strona_Lista[WYSZUKAJ_INDEKS]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}strona_Lista[WYSZUKAJ_INDEKS]=1;}
            Dalej_towar+=(바이트들+4095)&~(size_t)4095;
        }else if(dane_stanowisko.TYP_obszar==4){if(dane_stanowisko.파일영역크기>4096-부가정보)return -1;memcpy(OBRAZ+부가정보,원본자료+dane_stanowisko.przesunąć_WARTOŚĆ_450fc799,dane_stanowisko.파일영역크기);dane_stanowisko.przesunąć_WARTOŚĆ_450fc799=부가정보;부가정보+=dane_stanowisko.파일영역크기;}
        else if(dane_stanowisko.TYP_obszar!=0&&dane_stanowisko.TYP_obszar!=6&&dane_stanowisko.TYP_obszar!=0x6474e551)return -1;
        memcpy(OBRAZ+wykonywalny_Nagłówek.program_Nagłówek_przesunąć+순번*sizeof(dane_stanowisko),&dane_stanowisko,sizeof(dane_stanowisko));
    }
    if(!prawidłowy_punkt_wejścia)return -1;
    intptr_t dojście_do_pliku=사용자호출(3,(uintptr_t)Nazwa,577,0600,0,0,0);if(dojście_do_pliku<0){printf("cc: cannot create output file, error %d\n",(int)dojście_do_pliku);return -1;}
    intptr_t 쓴수=사용자호출(1,dojście_do_pliku,(uintptr_t)OBRAZ,Dalej_towar,0,0,0);사용자호출(4,dojście_do_pliku,0,0,0,0,0);return 쓴수==(intptr_t)Dalej_towar?0:-1;
}
int START_użytkownik_program(int metoda_tryb){
    char wejście[256],선택항목[256],produkt_wyjściowy[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metoda_tryb?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)wejście,sizeof(wejście),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(wejście,"--version")||!strcmp(wejście,"-version"))){printf(metoda_tryb?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)produkt_wyjściowy,sizeof(produkt_wyjściowy),0,0,0)<0)return 2;}
    if(!strcmp(wejście,produkt_wyjściowy)){printf("cc: input and output must differ\n");return 2;}
    TCCState*ciąg_dane=tcc_new();if(!ciąg_dane)return 1;
    tcc_undefine_symbol(ciąg_dane,"__linux__");tcc_undefine_symbol(ciąg_dane,"__linux");tcc_undefine_symbol(ciąg_dane,"linux");
    tcc_undefine_symbol(ciąg_dane,"__unix__");tcc_undefine_symbol(ciąg_dane,"__unix");tcc_undefine_symbol(ciąg_dane,"unix");
    tcc_undefine_symbol(ciąg_dane,"__STDC_HOSTED__");tcc_define_symbol(ciąg_dane,"__STDC_HOSTED__","0");tcc_define_symbol(ciąg_dane,"__JKOROS__","1");
    tcc_set_options(ciąg_dane,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(ciąg_dane,"/sdk/include");
    int 반환값=tcc_set_output_type(ciąg_dane,TCC_OUTPUT_EXE);
    if(!반환값){if(metoda_tryb){const char*원본자료=자바미리번역원문(wejście);반환값=원본자료?tcc_compile_string(ciąg_dane,원본자료):-1;}else 반환값=tcc_add_file(ciąg_dane,wejście);}
    if(!반환값)반환값=tcc_add_file(ciąg_dane,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(ciąg_dane,"/sdk/lib/crt.o");
    if(!반환값&&metoda_tryb)반환값=tcc_add_file(ciąg_dane,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(ciąg_dane,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(ciąg_dane,"/@cc-output");
    if(!반환값)반환값=publikować_wpis(produkt_wyjściowy);
    tcc_delete(ciąg_dane);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metoda_tryb?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",produkt_wyjściowy);return 0;
}
