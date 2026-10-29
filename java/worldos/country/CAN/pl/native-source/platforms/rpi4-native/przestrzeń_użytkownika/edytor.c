/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "Plik_ABI.h"
#define edytor_pojemność 16384
static unsigned char tekst[edytor_pojemność],cofnąć_dane[edytor_pojemność],복사자료[edytor_pojemność],KR_dane[1024];
static int długość_WARTOŚĆ,INDEKS_WARTOŚĆ,맨위,왼쪽,변경됨,Wstawianie,cofnąć_długość,위쪽,cofnąć_Zmiany,되돌림있음,kopiować_długość,사용량,LICZBA_KOLUMN=68,WIERSZ_ILE_LICZB=19;
static char Plik_wpis_nazwa[64],polecenie[128],ZNAJDŹ_wpis[128];
static const char *powiadomienie_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned oczekujący_Klucz;
static int pomoc_obszar,Stan_OBRAZ,Stan_kolejka;
static void opróżnić(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_dane,사용량,0,0,0);사용량=0;}}
static void bajt_dane(unsigned kod_znaku){if(Stan_OBRAZ){if((kod_znaku&192)!=128){Stan_kolejka+=kod_znaku>=196?2:1;}if(Stan_kolejka>=LICZBA_KOLUMN)return;}if(사용량==(int)sizeof(KR_dane))opróżnić();KR_dane[사용량++]=kod_znaku;}
static void 글내보내기(const char *ciąg_dane){while(*ciąg_dane)bajt_dane((unsigned char)*ciąg_dane++);}
static void 수치(unsigned towar_ILE_LICZB){char SEKUNDA_WARTOŚĆ[12];int 순번=0;do{SEKUNDA_WARTOŚĆ[순번++]='0'+towar_ILE_LICZB%10;towar_ILE_LICZB/=10;}while(towar_ILE_LICZB);while(순번)bajt_dane(SEKUNDA_WARTOŚĆ[--순번]);}
static void przenosić_WARTOŚĆ(int WIERSZ_stanowisko,int kolumna_stanowisko){글내보내기("\033[");수치(WIERSZ_stanowisko);bajt_dane(';');수치(kolumna_stanowisko);bajt_dane('H');}
static int Wstecz(int dane_stanowisko){if(dane_stanowisko){dane_stanowisko--;while(dane_stanowisko>0&&(tekst[dane_stanowisko]&192)==128)dane_stanowisko--;}return dane_stanowisko;}
static int Dalej_towar(int dane_stanowisko){if(dane_stanowisko<długość_WARTOŚĆ){dane_stanowisko++;while(dane_stanowisko<długość_WARTOŚĆ&&(tekst[dane_stanowisko]&192)==128)dane_stanowisko++;}return dane_stanowisko;}
static int Uruchom_2(int dane_stanowisko){while(dane_stanowisko>0&&tekst[dane_stanowisko-1]!='\n')dane_stanowisko--;return dane_stanowisko;}
static int Koniec_przesunąć(int dane_stanowisko){while(dane_stanowisko<długość_WARTOŚĆ&&tekst[dane_stanowisko]!='\n')dane_stanowisko++;return dane_stanowisko;}
static int 너비(unsigned kod_znaku){return kod_znaku>=196?2:1;}
static int kolumna(int dane_stanowisko){int kod_znaku=0;for(int 순번=Uruchom_2(dane_stanowisko);순번<dane_stanowisko;순번=Dalej_towar(순번))kod_znaku+=tekst[순번]=='\t'?4-kod_znaku%4:너비(tekst[순번]);return kod_znaku;}
static void punkt_kontrolny(void){for(int 순번=0;순번<długość_WARTOŚĆ;순번++)cofnąć_dane[순번]=tekst[순번];cofnąć_długość=długość_WARTOŚĆ;위쪽=INDEKS_WARTOŚĆ;cofnąć_Zmiany=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){punkt_kontrolny();for(int 순번=도착위치;순번<długość_WARTOŚĆ;순번++)tekst[출발위치+순번-도착위치]=tekst[순번];długość_WARTOŚĆ-=도착위치-출발위치;INDEKS_WARTOŚĆ=출발위치;변경됨=1;}
static int dołączać_WARTOŚĆ(const unsigned char *ciąg_dane,int towar_ILE_LICZB){if(towar_ILE_LICZB>edytor_pojemność-długość_WARTOŚĆ){powiadomienie_SMS="File full (16384 bytes)";return 0;}punkt_kontrolny();for(int 순번=długość_WARTOŚĆ-1;순번>=INDEKS_WARTOŚĆ;순번--)tekst[순번+towar_ILE_LICZB]=tekst[순번];for(int 순번=0;순번<towar_ILE_LICZB;순번++)tekst[INDEKS_WARTOŚĆ+순번]=ciąg_dane[순번];długość_WARTOŚĆ+=towar_ILE_LICZB;INDEKS_WARTOŚĆ+=towar_ILE_LICZB;변경됨=1;return 1;}
static void gałąź(int 차이){int kolumna_stanowisko=kolumna(INDEKS_WARTOŚĆ),dane_stanowisko=Uruchom_2(INDEKS_WARTOŚĆ);if(차이<0){if(!dane_stanowisko)return;dane_stanowisko=Uruchom_2(dane_stanowisko-1);}else{dane_stanowisko=Koniec_przesunąć(dane_stanowisko);if(dane_stanowisko==długość_WARTOŚĆ)return;dane_stanowisko++;}int kod_znaku=0;while(dane_stanowisko<długość_WARTOŚĆ&&tekst[dane_stanowisko]!='\n'&&kod_znaku<kolumna_stanowisko){kod_znaku+=tekst[dane_stanowisko]=='\t'?4-kod_znaku%4:너비(tekst[dane_stanowisko]);dane_stanowisko=Dalej_towar(dane_stanowisko);}INDEKS_WARTOŚĆ=dane_stanowisko;}
static void 화면그리기(void){
    if(INDEKS_WARTOŚĆ>długość_WARTOŚĆ)INDEKS_WARTOŚĆ=długość_WARTOŚĆ;if(맨위>INDEKS_WARTOŚĆ)맨위=Uruchom_2(INDEKS_WARTOŚĆ);맨위=Uruchom_2(맨위);
    int WIERSZ_stanowisko=0;for(int 순번=맨위;순번<INDEKS_WARTOŚĆ;순번++)if(tekst[순번]=='\n')WIERSZ_stanowisko++;
    while(WIERSZ_stanowisko>=WIERSZ_ILE_LICZB-1){맨위=Koniec_przesunąć(맨위);if(맨위<długość_WARTOŚĆ)맨위++;WIERSZ_stanowisko--;}
    int kolumna_stanowisko=kolumna(INDEKS_WARTOŚĆ);if(kolumna_stanowisko<왼쪽)왼쪽=kolumna_stanowisko;if(kolumna_stanowisko-왼쪽>=LICZBA_KOLUMN-1)왼쪽=kolumna_stanowisko-LICZBA_KOLUMN+2;
    글내보내기("\033[?25l");int dane_stanowisko=맨위;
    for(int 반환값=0;반환값<WIERSZ_ILE_LICZB-1;반환값++){
        przenosić_WARTOŚĆ(반환값+1,1);글내보내기("\033[0m\033[2K");int kod_znaku=0,그려진상태=0;
        if(dane_stanowisko>=długość_WARTOŚĆ&&반환값>WIERSZ_stanowisko){글내보내기("\033[90m~\033[0m");continue;}
        while(dane_stanowisko<długość_WARTOŚĆ&&tekst[dane_stanowisko]!='\n'){
            int Dalej_przesunąć=Dalej_towar(dane_stanowisko),너비값=tekst[dane_stanowisko]=='\t'?4-kod_znaku%4:너비(tekst[dane_stanowisko]);
            if(kod_znaku>=왼쪽&&kod_znaku-왼쪽+너비값<LICZBA_KOLUMN){
                if(tekst[dane_stanowisko]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bajt_dane(' ');}else if(tekst[dane_stanowisko]<32||tekst[dane_stanowisko]==127){bajt_dane('?');}else for(int 안쪽순번=dane_stanowisko;안쪽순번<Dalej_przesunąć;안쪽순번++)bajt_dane(tekst[안쪽순번]);그려진상태+=너비값;
            }kod_znaku+=너비값;dane_stanowisko=Dalej_przesunąć;
        }
        (void)그려진상태;if(dane_stanowisko<długość_WARTOŚĆ)dane_stanowisko++;
    }
    przenosić_WARTOŚĆ(WIERSZ_ILE_LICZB,1);글내보내기("\033[7m\033[2K");Stan_OBRAZ=1;Stan_kolejka=0;글내보내기(Wstawianie?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Plik_wpis_nazwa[이름바이트수]&&이름바이트수<30)bajt_dane(Plik_wpis_nazwa[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int wiersz_wejścia=1;for(int 순번=0;순번<INDEKS_WARTOŚĆ;순번++)if(tekst[순번]=='\n')wiersz_wejścia++;수치(wiersz_wejścia);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(powiadomienie_SMS){int towar_ILE_LICZB=0;글내보내기(" | ");while(powiadomienie_SMS[towar_ILE_LICZB]&&towar_ILE_LICZB<20)bajt_dane(powiadomienie_SMS[towar_ILE_LICZB++]);}
    Stan_OBRAZ=0;글내보내기("\033[0m");przenosić_WARTOŚĆ(WIERSZ_stanowisko+1,kolumna_stanowisko-왼쪽+1);글내보내기("\033[?25h");opróżnić();
}
static int 누름값(void){
    if(oczekujący_Klucz){int 셋째순번=oczekujący_Klucz;oczekujący_Klucz=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Rozmiar=사용자호출(16,3,0,0,0,0,0);
        if(LICZBA_KOLUMN!=(int)(Rozmiar&65535)||WIERSZ_ILE_LICZB!=(int)(Rozmiar>>16)){
            LICZBA_KOLUMN=Rozmiar&65535;WIERSZ_ILE_LICZB=Rozmiar>>16;화면그리기();
            if(pomoc_obszar){przenosić_WARTOŚĆ(WIERSZ_ILE_LICZB,1);글내보내기("\033[0m\033[2K");bajt_dane(pomoc_obszar);글내보내기(polecenie);opróżnić();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned bieżący_stanowisko=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-bieżący_stanowisko<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){oczekujący_Klucz=셋째순번;return 27;}
    int towar_ILE_LICZB=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){towar_ILE_LICZB=towar_ILE_LICZB*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return towar_ILE_LICZB==3?1007:towar_ILE_LICZB==5?1008:towar_ILE_LICZB==6?1009:towar_ILE_LICZB==1?1005:towar_ILE_LICZB==4?1006:27;return 27;}return 27;
}
static int Store_WARTOŚĆ(void){
    int dojście_do_pliku=otwarty_Plik(Plik_wpis_nazwa,R_W|없으면만들기|obcinać_Spis_treści,0600);if(dojście_do_pliku<0){powiadomienie_SMS="Cannot open for save";return 0;}
    intptr_t towar_ILE_LICZB=zapis_Plik_dane(dojście_do_pliku,tekst,długość_WARTOŚĆ);Zamknij_Plik(dojście_do_pliku);if(towar_ILE_LICZB!=długość_WARTOŚĆ){powiadomienie_SMS="Write failed";return 0;}변경됨=0;powiadomienie_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEKUNDA_WARTOŚĆ){while(*첫째값&&*첫째값==*SEKUNDA_WARTOŚĆ){첫째값++;SEKUNDA_WARTOŚĆ++;}return *첫째값==*SEKUNDA_WARTOŚĆ;}
static void ZNAJDŹ_Dalej(void){int towar_ILE_LICZB=0;while(ZNAJDŹ_wpis[towar_ILE_LICZB])towar_ILE_LICZB++;if(!towar_ILE_LICZB){powiadomienie_SMS="No search pattern";return;}for(int 순번=1;순번<=długość_WARTOŚĆ;순번++){int dane_stanowisko=(INDEKS_WARTOŚĆ+순번)%(długość_WARTOŚĆ?długość_WARTOŚĆ:1),안쪽순번=0;while(안쪽순번<towar_ILE_LICZB&&dane_stanowisko+안쪽순번<długość_WARTOŚĆ&&tekst[dane_stanowisko+안쪽순번]==(unsigned char)ZNAJDŹ_wpis[안쪽순번])안쪽순번++;if(안쪽순번==towar_ILE_LICZB){INDEKS_WARTOŚĆ=dane_stanowisko;powiadomienie_SMS="Match";return;}}powiadomienie_SMS="Pattern not found";}
static int monit(int obszar_WARTOŚĆ){
    int towar_ILE_LICZB=0;polecenie[0]=0;
    for(;;){przenosić_WARTOŚĆ(WIERSZ_ILE_LICZB,1);글내보내기("\033[0m\033[2K");bajt_dane(obszar_WARTOŚĆ);글내보내기(polecenie);opróżnić();pomoc_obszar=obszar_WARTOŚĆ;int 셋째순번=누름값();pomoc_obszar=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(towar_ILE_LICZB){towar_ILE_LICZB--;while(towar_ILE_LICZB>0&&((unsigned char)polecenie[towar_ILE_LICZB]&192)==128)towar_ILE_LICZB--;polecenie[towar_ILE_LICZB]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&towar_ILE_LICZB<120){polecenie[towar_ILE_LICZB++]=셋째순번;polecenie[towar_ILE_LICZB]=0;}
    }
    if(obszar_WARTOŚĆ=='/'){for(int 순번=0;순번<=towar_ILE_LICZB;순번++)ZNAJDŹ_wpis[순번]=polecenie[순번];ZNAJDŹ_Dalej();return 0;}
    if(같은지(polecenie,"q!"))return 1;
    if(같은지(polecenie,"q")){if(!변경됨)return 1;powiadomienie_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(polecenie,"wq")||같은지(polecenie,"x"))return Store_WARTOŚĆ();
    if(같은지(polecenie,"w")){Store_WARTOŚĆ();return 0;}
    if(polecenie[0]=='w'&&polecenie[1]==' '){int 순번=2;while(polecenie[순번]==' ')순번++;int Rozmiar=towar_ILE_LICZB-순번;if(Rozmiar<1||Rozmiar>63){powiadomienie_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Rozmiar;안쪽순번++)Plik_wpis_nazwa[안쪽순번]=polecenie[순번+안쪽순번];Plik_wpis_nazwa[Rozmiar]=0;Store_WARTOŚĆ();return 0;}
    int wiersz_wejścia=0;for(int 순번=0;순번<towar_ILE_LICZB;순번++){if(polecenie[순번]<'0'||polecenie[순번]>'9'){wiersz_wejścia=0;break;}wiersz_wejścia=wiersz_wejścia*10+polecenie[순번]-'0';if(wiersz_wejścia>16384){wiersz_wejścia=0;break;}}
    if(wiersz_wejścia){INDEKS_WARTOŚĆ=0;while(--wiersz_wejścia&&INDEKS_WARTOŚĆ<długość_WARTOŚĆ){INDEKS_WARTOŚĆ=Koniec_przesunąć(INDEKS_WARTOŚĆ);if(INDEKS_WARTOŚĆ<długość_WARTOŚĆ)INDEKS_WARTOŚĆ++;}return 0;}
    powiadomienie_SMS="Unknown vi command";return 0;
}
int START_użytkownik_program(int 무시값){
    (void)무시값;if(użytkownik_argument_ILE_LICZB()!=1||użytkownik_argument(0,Plik_wpis_nazwa,sizeof(Plik_wpis_nazwa))<0){글내보내기("Usage: vi FILE\n");opróżnić();return 2;}
    int dojście_do_pliku=otwarty_Plik(Plik_wpis_nazwa,tylko_do_odczytu_WARTOŚĆ,0);
    if(dojście_do_pliku>=0){int towar_ILE_LICZB=rozmiar_pliku(dojście_do_pliku);if(towar_ILE_LICZB<0||towar_ILE_LICZB>edytor_pojemność){Zamknij_Plik(dojście_do_pliku);return 1;}długość_WARTOŚĆ=파일자료읽기(dojście_do_pliku,tekst,towar_ILE_LICZB);Zamknij_Plik(dojście_do_pliku);if(długość_WARTOŚĆ!=towar_ILE_LICZB)return 1;for(int 순번=0;순번<długość_WARTOŚĆ;순번++)if(!tekst[순번]){글내보내기("vi: NUL byte in text file\n");opróżnić();return 1;}}
    else if(numer_błędu!=2){글내보내기("vi: cannot read file\n");opróżnić();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");opróżnić();return 1;}LICZBA_KOLUMN=흐린색&65535;WIERSZ_ILE_LICZB=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");opróżnić();
    int interlinia_część=0,zakończ_program=0;
    while(!zakończ_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();powiadomienie_SMS=0;
        if(셋째순번==1001){gałąź(-1);continue;}if(셋째순번==1002){gałąź(1);continue;}if(셋째순번==1003){INDEKS_WARTOŚĆ=Dalej_towar(INDEKS_WARTOŚĆ);continue;}if(셋째순번==1004){INDEKS_WARTOŚĆ=Wstecz(INDEKS_WARTOŚĆ);continue;}
        if(셋째순번==1005){INDEKS_WARTOŚĆ=Uruchom_2(INDEKS_WARTOŚĆ);continue;}if(셋째순번==1006){INDEKS_WARTOŚĆ=Koniec_przesunąć(INDEKS_WARTOŚĆ);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<WIERSZ_ILE_LICZB-2;순번++)gałąź(셋째순번==1008?-1:1);continue;}
        if(Wstawianie){
            if(셋째순번==27||셋째순번==3){Wstawianie=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEKS_WARTOŚĆ)바이트지우기(Wstecz(INDEKS_WARTOŚĆ),INDEKS_WARTOŚĆ);continue;}
            if(셋째순번==1007){if(INDEKS_WARTOŚĆ<długość_WARTOŚĆ)바이트지우기(INDEKS_WARTOŚĆ,Dalej_towar(INDEKS_WARTOŚĆ));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEKUNDA_WARTOŚĆ[4];SEKUNDA_WARTOŚĆ[0]=셋째순번;int towar_ILE_LICZB=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!towar_ILE_LICZB){powiadomienie_SMS="Invalid UTF-8";continue;}int prawidłowy=1;for(int 순번=1;순번<towar_ILE_LICZB;순번++){int kod_znaku=누름값();if(kod_znaku<128||kod_znaku>191){oczekujący_Klucz=kod_znaku;prawidłowy=0;break;}SEKUNDA_WARTOŚĆ[순번]=kod_znaku;}
                if(prawidłowy)dołączać_WARTOŚĆ(SEKUNDA_WARTOŚĆ,towar_ILE_LICZB);
            }continue;
        }
        if(interlinia_część){int dane_stanowisko=interlinia_część;interlinia_część=0;if(dane_stanowisko=='g'&&셋째순번=='g'){INDEKS_WARTOŚĆ=0;continue;}if(dane_stanowisko=='Z'&&셋째순번=='Z'){zakończ_program=Store_WARTOŚĆ();continue;}if((dane_stanowisko=='d'&&셋째순번=='d')||(dane_stanowisko=='y'&&셋째순번=='y')){int 첫째값=Uruchom_2(INDEKS_WARTOŚĆ),SEKUNDA_WARTOŚĆ=Koniec_przesunąć(INDEKS_WARTOŚĆ);if(SEKUNDA_WARTOŚĆ<długość_WARTOŚĆ)SEKUNDA_WARTOŚĆ++;kopiować_długość=SEKUNDA_WARTOŚĆ-첫째값;for(int 순번=0;순번<kopiować_długość;순번++)복사자료[순번]=tekst[첫째값+순번];if(dane_stanowisko=='d')바이트지우기(첫째값,SEKUNDA_WARTOŚĆ);continue;}}
        if(셋째순번=='i'){Wstawianie=1;continue;}if(셋째순번=='a'){if(INDEKS_WARTOŚĆ<Koniec_przesunąć(INDEKS_WARTOŚĆ))INDEKS_WARTOŚĆ=Dalej_towar(INDEKS_WARTOŚĆ);Wstawianie=1;continue;}
        if(셋째순번=='I'){INDEKS_WARTOŚĆ=Uruchom_2(INDEKS_WARTOŚĆ);Wstawianie=1;continue;}if(셋째순번=='A'){INDEKS_WARTOŚĆ=Koniec_przesunąć(INDEKS_WARTOŚĆ);Wstawianie=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linia_Koniec='\n';INDEKS_WARTOŚĆ=셋째순번=='o'?Koniec_przesunąć(INDEKS_WARTOŚĆ):Uruchom_2(INDEKS_WARTOŚĆ);if(dołączać_WARTOŚĆ(&linia_Koniec,1)){if(셋째순번=='O')INDEKS_WARTOŚĆ--;Wstawianie=1;}continue;}
        if(셋째순번=='h'){INDEKS_WARTOŚĆ=Wstecz(INDEKS_WARTOŚĆ);continue;}if(셋째순번=='l'){INDEKS_WARTOŚĆ=Dalej_towar(INDEKS_WARTOŚĆ);continue;}if(셋째순번=='j'){gałąź(1);continue;}if(셋째순번=='k'){gałąź(-1);continue;}
        if(셋째순번=='0'){INDEKS_WARTOŚĆ=Uruchom_2(INDEKS_WARTOŚĆ);continue;}if(셋째순번=='$'){INDEKS_WARTOŚĆ=Koniec_przesunąć(INDEKS_WARTOŚĆ);continue;}if(셋째순번=='G'){INDEKS_WARTOŚĆ=Uruchom_2(długość_WARTOŚĆ);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){interlinia_część=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEKS_WARTOŚĆ<długość_WARTOŚĆ)바이트지우기(INDEKS_WARTOŚĆ,Dalej_towar(INDEKS_WARTOŚĆ));continue;}
        if(셋째순번=='p'&&kopiować_długość){INDEKS_WARTOŚĆ=Koniec_przesunąć(INDEKS_WARTOŚĆ);if(INDEKS_WARTOŚĆ<długość_WARTOŚĆ)INDEKS_WARTOŚĆ++;dołączać_WARTOŚĆ(복사자료,kopiować_długość);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<edytor_pojemność;순번++){unsigned char SEKUNDA_WARTOŚĆ=tekst[순번];tekst[순번]=cofnąć_dane[순번];cofnąć_dane[순번]=SEKUNDA_WARTOŚĆ;}int towar_ILE_LICZB=długość_WARTOŚĆ;długość_WARTOŚĆ=cofnąć_długość;cofnąć_długość=towar_ILE_LICZB;towar_ILE_LICZB=INDEKS_WARTOŚĆ;INDEKS_WARTOŚĆ=위쪽;위쪽=towar_ILE_LICZB;towar_ILE_LICZB=변경됨;변경됨=cofnąć_Zmiany;cofnąć_Zmiany=towar_ILE_LICZB;continue;}
        if(셋째순번==':'||셋째순번=='/'){zakończ_program=monit(셋째순번);continue;}if(셋째순번=='n'){ZNAJDŹ_Dalej();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");opróżnić();사용자호출(16,2,0,0,0,0,0);return 0;
}
