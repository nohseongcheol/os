#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 nazwa_pliku/pozycja_wyjścia/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "pakiet.h"
typedef uintptr_t maszyna_Word;
static int obszar_WARTOŚĆ;
static int 꾸러미사용중, 꾸러미인수이동;
static maszyna_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned towar_ILE_LICZB, maszyna_Word 첫째값, maszyna_Word SEKUNDA_WARTOŚĆ, maszyna_Word kod_znaku) {
    return 사용자호출(towar_ILE_LICZB, 첫째값, SEKUNDA_WARTOŚĆ, kod_znaku, 0, 0, 0);
}
static void 바이트들(const char *dane_stanowisko, size_t towar_ILE_LICZB) { 호출(1, 1, (maszyna_Word)dane_stanowisko, towar_ILE_LICZB); }
static void znak(unsigned kod_znaku) {
    unsigned char dane[4]; unsigned towar_ILE_LICZB = 0;
    if (kod_znaku < 128) dane[towar_ILE_LICZB++] = kod_znaku;
    else if (kod_znaku < 2048) { dane[towar_ILE_LICZB++] = 0xc0 | (kod_znaku >> 6); dane[towar_ILE_LICZB++] = 0x80 | (kod_znaku & 63); }
    else if (kod_znaku < 65536) { dane[towar_ILE_LICZB++] = 0xe0 | (kod_znaku >> 12); dane[towar_ILE_LICZB++] = 0x80 | ((kod_znaku >> 6) & 63); dane[towar_ILE_LICZB++] = 0x80 | (kod_znaku & 63); }
    else { dane[towar_ILE_LICZB++] = 0xf0 | (kod_znaku >> 18); dane[towar_ILE_LICZB++] = 0x80 | ((kod_znaku >> 12) & 63); dane[towar_ILE_LICZB++] = 0x80 | ((kod_znaku >> 6) & 63); dane[towar_ILE_LICZB++] = 0x80 | (kod_znaku & 63); }
    바이트들((const char *)dane, towar_ILE_LICZB);
}
maszyna_Word narzędzie_znak(maszyna_Word WARTOŚĆ) {
    unsigned kod_znaku = WARTOŚĆ;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kod_znaku >= 0xdc00 && kod_znaku <= 0xdfff) { znak(0x10000 + ((높은부분 - 0xd800) << 10) + kod_znaku - 0xdc00); return 1; }
        znak(0xfffd);
    }
    if (kod_znaku >= 0xd800 && kod_znaku <= 0xdbff) 대기중짝글자 = kod_znaku;
    else znak(kod_znaku > 0x10ffff || (kod_znaku >= 0xdc00 && kod_znaku <= 0xdfff) ? 0xfffd : kod_znaku);
    return 1;
}
maszyna_Word 도구출력(maszyna_Word WARTOŚĆ) {
    const maszyna_Word *ciąg_dane = (const maszyna_Word *)WARTOŚĆ;
    for (maszyna_Word 순번 = 0; 순번 < ciąg_dane[0]; 순번++) narzędzie_znak(ciąg_dane[순번 + 1]);
    return ciąg_dane[0];
}
static int ścieżka_2(maszyna_Word obiekt_odwołanie, char KR_dane[512]) {
    const maszyna_Word *첫째값 = (const maszyna_Word *)obiekt_odwołanie;
    unsigned 사용량 = 0;
    for (maszyna_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kod_znaku = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metoda_tryb 경로와 호환한다.
        if (kod_znaku >= 0xd800 && kod_znaku <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kod_znaku = 0x10000 + ((kod_znaku - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kod_znaku >= 0xd800 && kod_znaku <= 0xdfff) return -22;
        unsigned towar_ILE_LICZB = kod_znaku < 128 ? 1 : kod_znaku < 2048 ? 2 : kod_znaku < 65536 ? 3 : 4;
        if (사용량 + towar_ILE_LICZB > 511) return -36;
        if (towar_ILE_LICZB == 1) KR_dane[사용량++] = kod_znaku;
        else {
            KR_dane[사용량++] = (towar_ILE_LICZB == 2 ? 0xc0 : towar_ILE_LICZB == 3 ? 0xe0 : 0xf0) | (kod_znaku >> (6 * (towar_ILE_LICZB - 1)));
            for (unsigned 안쪽순번 = towar_ILE_LICZB - 1; 안쪽순번; 안쪽순번--) KR_dane[사용량++] = 0x80 | ((kod_znaku >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_dane[사용량] = 0; return 사용량 ? 0 : -22;
}
maszyna_Word narzędzie_otwarty(maszyna_Word Nazwa, maszyna_Word konfiguracja_BITS) {
    char dane_stanowisko[512]; int błąd = ścieżka_2(Nazwa, dane_stanowisko);
    return (uint32_t)(błąd ? błąd : 호출(3, (maszyna_Word)dane_stanowisko, konfiguracja_BITS, 0));
}
maszyna_Word narzędzie_Zamknij(maszyna_Word dojście_do_pliku) { return (uint32_t)호출(4, dojście_do_pliku, 0, 0); }
maszyna_Word 도구바이트읽기(maszyna_Word dojście_do_pliku) {
    unsigned char SEKUNDA_WARTOŚĆ; intptr_t towar_ILE_LICZB = 호출(2, dojście_do_pliku, (maszyna_Word)&SEKUNDA_WARTOŚĆ, 1);
    return (uint32_t)(towar_ILE_LICZB == 1 ? SEKUNDA_WARTOŚĆ : towar_ILE_LICZB == 0 ? 256 : towar_ILE_LICZB);
}
maszyna_Word narzędzie_zapis_bajt(maszyna_Word dojście_do_pliku, maszyna_Word WARTOŚĆ) {
    unsigned char SEKUNDA_WARTOŚĆ = WARTOŚĆ; return (uint32_t)호출(1, dojście_do_pliku, (maszyna_Word)&SEKUNDA_WARTOŚĆ, 1);
}
maszyna_Word 도구읽기(maszyna_Word Nazwa, maszyna_Word cel_dane_ADRES) {
    if (꾸러미사용중) {
        char dane_stanowisko[512]; int błąd = ścieżka_2(Nazwa, dane_stanowisko); if (błąd) return (uint32_t)błąd;
        unsigned towar_ILE_LICZB = 0; while (dane_stanowisko[towar_ILE_LICZB]) towar_ILE_LICZB++;
        if (towar_ILE_LICZB >= 6) for (unsigned 순번 = 0; 순번 < towar_ILE_LICZB - 6; 순번++) if (dane_stanowisko[순번] == '.') dane_stanowisko[순번] = '/';
        unsigned char 바이트들[16384]; maszyna_Word *cel_WARTOŚĆ_stanowisko = (maszyna_Word *)cel_dane_ADRES;
        int KWOTA_WYKUP_ILE_LICZB = 꾸러미읽기(dane_stanowisko, 바이트들, cel_WARTOŚĆ_stanowisko[0] < sizeof(바이트들) ? cel_WARTOŚĆ_stanowisko[0] : sizeof(바이트들));
        if (KWOTA_WYKUP_ILE_LICZB >= 0) { for (int 순번 = 0; 순번 < KWOTA_WYKUP_ILE_LICZB; 순번++) cel_WARTOŚĆ_stanowisko[순번 + 1] = 바이트들[순번]; return KWOTA_WYKUP_ILE_LICZB; }
        if (KWOTA_WYKUP_ILE_LICZB != -2) return (uint32_t)KWOTA_WYKUP_ILE_LICZB;
    }
    int dojście_do_pliku = 꾸러미사용중 ? -2 : (int32_t)narzędzie_otwarty(Nazwa, 0);
    if (dojście_do_pliku < 0) {
        char dane_stanowisko[512]; int błąd = ścieżka_2(Nazwa, dane_stanowisko); if (błąd) return (uint32_t)błąd;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Dalej_przesunąć = 자바클래스들[순번].Nazwa; unsigned 안쪽순번 = 0;
            while (dane_stanowisko[안쪽순번] && dane_stanowisko[안쪽순번] == Dalej_przesunąć[안쪽순번]) 안쪽순번++;
            if (dane_stanowisko[안쪽순번] || Dalej_przesunąć[안쪽순번]) continue;
            maszyna_Word *cel_WARTOŚĆ_stanowisko = (maszyna_Word *)cel_dane_ADRES;
            if (cel_WARTOŚĆ_stanowisko[0] < 자바클래스들[순번].Rozmiar) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Rozmiar; 안쪽순번++) cel_WARTOŚĆ_stanowisko[안쪽순번 + 1] = 자바클래스들[순번].dane[안쪽순번];
            return 자바클래스들[순번].Rozmiar;
        }
        return (uint32_t)dojście_do_pliku;
    }
    maszyna_Word *첫째값 = (maszyna_Word *)cel_dane_ADRES;
    intptr_t Rozmiar = 호출(9, dojście_do_pliku, 0, 0), Wykonane_ilość = 0;
    if (Rozmiar < 0 || (maszyna_Word)Rozmiar > 첫째값[0]) { narzędzie_Zamknij(dojście_do_pliku); return (uint32_t)(Rozmiar < 0 ? Rozmiar : -27); }
    unsigned char blok_danych[256];
    while (Wykonane_ilość < Rozmiar) {
        intptr_t towar_ILE_LICZB = 호출(2, dojście_do_pliku, (maszyna_Word)blok_danych, Rozmiar - Wykonane_ilość < 256 ? Rozmiar - Wykonane_ilość : 256);
        if (towar_ILE_LICZB <= 0) { narzędzie_Zamknij(dojście_do_pliku); return (uint32_t)(towar_ILE_LICZB ? towar_ILE_LICZB : -5); }
        for (intptr_t 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) 첫째값[1 + Wykonane_ilość + 순번] = blok_danych[순번];
        Wykonane_ilość += towar_ILE_LICZB;
    }
    narzędzie_Zamknij(dojście_do_pliku); return Wykonane_ilość;
}
maszyna_Word narzędzie_zapis(maszyna_Word Nazwa, maszyna_Word 원본자료, maszyna_Word wpis_ILE_LICZB) {
    const maszyna_Word *첫째값 = (const maszyna_Word *)원본자료;
    if (wpis_ILE_LICZB > 첫째값[0] || wpis_ILE_LICZB > 16384) return (uint32_t)-27;
    int dojście_do_pliku = (int32_t)narzędzie_otwarty(Nazwa, 577); if (dojście_do_pliku < 0) return (uint32_t)dojście_do_pliku;
    unsigned char blok_danych[256]; maszyna_Word Wykonane_ilość = 0;
    while (Wykonane_ilość < wpis_ILE_LICZB) {
        maszyna_Word towar_ILE_LICZB = wpis_ILE_LICZB - Wykonane_ilość < 256 ? wpis_ILE_LICZB - Wykonane_ilość : 256;
        for (maszyna_Word 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) blok_danych[순번] = 첫째값[1 + Wykonane_ilość + 순번];
        intptr_t WYNIK = 호출(1, dojście_do_pliku, (maszyna_Word)blok_danych, towar_ILE_LICZB);
        if (WYNIK <= 0) { narzędzie_Zamknij(dojście_do_pliku); return (uint32_t)(WYNIK ? WYNIK : -5); }
        Wykonane_ilość += WYNIK;
    }
    narzędzie_Zamknij(dojście_do_pliku); return wpis_ILE_LICZB;
}
maszyna_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
maszyna_Word narzędzie_argument(maszyna_Word WYSZUKAJ_INDEKS) {
    static const maszyna_Word 빈값[1] = {0};
    if (WYSZUKAJ_INDEKS >= 8) return (maszyna_Word)빈값;
    unsigned char wejście[256]; intptr_t towar_ILE_LICZB;
    if (꾸러미사용중 && WYSZUKAJ_INDEKS == 0) { const char *dane_stanowisko = 꾸러미진입클래스(); towar_ILE_LICZB = 0; while (dane_stanowisko[towar_ILE_LICZB] && towar_ILE_LICZB < 255) { wejście[towar_ILE_LICZB] = dane_stanowisko[towar_ILE_LICZB]; towar_ILE_LICZB++; } }
    else towar_ILE_LICZB = 호출(15, WYSZUKAJ_INDEKS + (꾸러미사용중 ? 꾸러미인수이동 : 0), (maszyna_Word)wejście, sizeof(wejście));
    if (towar_ILE_LICZB < 0) return (maszyna_Word)빈값;
    maszyna_Word *KR_dane = 전달인수[WYSZUKAJ_INDEKS]; unsigned wpis_ILE_LICZB = 0;
    for (intptr_t 순번 = 0; 순번 < towar_ILE_LICZB;) {
        unsigned kod_znaku = wejście[순번++], 더있음 = kod_znaku < 128 ? 0 : kod_znaku >= 0xc2 && kod_znaku < 0xe0 ? 1 : kod_znaku < 0xf0 && kod_znaku >= 0xe0 ? 2 : kod_znaku >= 0xf0 && kod_znaku <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > towar_ILE_LICZB) { KR_dane[++wpis_ILE_LICZB] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kod_znaku &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (wejście[순번] & 0xc0) == 0x80) { kod_znaku = (kod_znaku << 6) | (wejście[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kod_znaku < 최소값 || kod_znaku > 0x10ffff || (kod_znaku >= 0xd800 && kod_znaku <= 0xdfff)) kod_znaku = 0xfffd;
        if (kod_znaku >= 65536) { kod_znaku -= 65536; KR_dane[++wpis_ILE_LICZB] = 0xd800 | (kod_znaku >> 10); KR_dane[++wpis_ILE_LICZB] = 0xdc00 | (kod_znaku & 1023); }
        else KR_dane[++wpis_ILE_LICZB] = kod_znaku;
    }
    KR_dane[0] = wpis_ILE_LICZB; return (maszyna_Word)KR_dane;
}
maszyna_Word narzędzie_Rodzaj(void) { return obszar_WARTOŚĆ; }
void 커널중단(const char *powiadomienie_SMS) {
    const char *dane_stanowisko = powiadomienie_SMS; while (*dane_stanowisko) dane_stanowisko++;
    바이트들("Java tool runtime error: ", 25); 바이트들(powiadomienie_SMS, dane_stanowisko - powiadomienie_SMS); znak(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_użytkownik_program(int metoda_tryb) {
    obszar_WARTOŚĆ = metoda_tryb;
    unsigned char 첫항목[256]; intptr_t towar_ILE_LICZB = 호출(15, 0, (maszyna_Word)첫항목, sizeof(첫항목));
    if (metoda_tryb == 2 || (metoda_tryb == 1 && towar_ILE_LICZB == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metoda_tryb == 2 ? 0 : 1;
        char Plik_wpis_nazwa[256]; intptr_t długość_dane = 호출(15, 꾸러미인수이동, (maszyna_Word)Plik_wpis_nazwa, sizeof(Plik_wpis_nazwa));
        if (długość_dane <= 0 || 꾸러미열기(Plik_wpis_nazwa) < 0) {
            static const char błąd[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(błąd, sizeof(błąd) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int WYNIK = 자바진입();
    if (대기중짝글자) znak(0xfffd);
    return WYNIK;
}

// UDP는 własny 커널의 SVC를 통과하며 bieżący_towar 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Rodzina, numer_portu; uint32_t Adres; unsigned char wartość_zerowa[8]; };
static struct 자바주소 UDP_ADRES(unsigned numer_portu) {
    struct 자바주소 첫째값 = {2, (uint16_t)((numer_portu << 8) | (numer_portu >> 8)), 0x0100007f, {0}}; return 첫째값;
}
maszyna_Word narzędzie_UDP_otwarty(maszyna_Word numer_portu) {
    intptr_t dojście_do_pliku = 호출(32, 2, 2, 17); if (dojście_do_pliku < 0) return (uint32_t)dojście_do_pliku;
    struct 자바주소 첫째값 = UDP_ADRES(numer_portu);
    첫째값.Adres = 0;
    intptr_t Stan_WARTOŚĆ = 호출(33, dojście_do_pliku, (maszyna_Word)&첫째값, sizeof(첫째값));
    if (Stan_WARTOŚĆ < 0) { narzędzie_Zamknij(dojście_do_pliku); return (uint32_t)Stan_WARTOŚĆ; }
    return dojście_do_pliku;
}
maszyna_Word narzędzie_UDP_wysłać(maszyna_Word dojście_do_pliku, maszyna_Word numer_portu, maszyna_Word TABLICA_WARTOŚĆ, maszyna_Word długość_WARTOŚĆ) {
    const maszyna_Word *원본주소 = (const maszyna_Word *)TABLICA_WARTOŚĆ; unsigned char dane[512];
    if (długość_WARTOŚĆ > 512 || długość_WARTOŚĆ > 원본주소[0]) return (uint32_t)-90;
    for (maszyna_Word 순번 = 0; 순번 < długość_WARTOŚĆ; 순번++) dane[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRES(numer_portu);
    return (uint32_t)사용자호출(34, dojście_do_pliku, (maszyna_Word)dane, długość_WARTOŚĆ, 0, (maszyna_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t towar_ILE_LICZB) { return (towar_ILE_LICZB>>24)|((towar_ILE_LICZB>>8)&0xff00)|((towar_ILE_LICZB<<8)&0xff0000)|(towar_ILE_LICZB<<24); }
maszyna_Word narzędzie_UDP_wysłać_ADRES(maszyna_Word dojście_do_pliku, maszyna_Word Adres, maszyna_Word numer_portu, maszyna_Word TABLICA_WARTOŚĆ, maszyna_Word długość_WARTOŚĆ) {
    const maszyna_Word *원본주소 = (const maszyna_Word *)TABLICA_WARTOŚĆ; unsigned char dane[512];
    if (długość_WARTOŚĆ > 512 || długość_WARTOŚĆ > 원본주소[0]) return (uint32_t)-90;
    for (maszyna_Word 순번 = 0; 순번 < długość_WARTOŚĆ; 순번++) dane[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRES(numer_portu); 첫째값.Adres = 바이트순서뒤집기(Adres);
    return (uint32_t)사용자호출(34, dojście_do_pliku, (maszyna_Word)dane, długość_WARTOŚĆ, 0, (maszyna_Word)&첫째값, sizeof(첫째값));
}
maszyna_Word narzędzie_POŁĄCZ(maszyna_Word dojście_do_pliku, maszyna_Word Adres, maszyna_Word numer_portu) {
    struct 자바주소 첫째값 = UDP_ADRES(numer_portu); 첫째값.Adres = 바이트순서뒤집기(Adres);
    uint32_t Uruchom_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t WYNIK = 호출(37, dojście_do_pliku, (maszyna_Word)&첫째값, sizeof(첫째값));
        if (WYNIK != -115) return (uint32_t)WYNIK;
        if ((uint32_t)(호출(7, 0, 0, 0) - Uruchom_2) >= 1000) return (uint32_t)-110;
    }
}
maszyna_Word 도구전문받기(maszyna_Word dojście_do_pliku, maszyna_Word TABLICA_WARTOŚĆ, maszyna_Word bufor_pojemność) {
    maszyna_Word *cel_ADRES_08bbd577 = (maszyna_Word *)TABLICA_WARTOŚĆ; unsigned char dane[512];
    if (bufor_pojemność > 512 || cel_ADRES_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned długość_dane = sizeof(첫째값);
    intptr_t towar_ILE_LICZB = 사용자호출(35, dojście_do_pliku, (maszyna_Word)dane, bufor_pojemność, 0, (maszyna_Word)&첫째값, (maszyna_Word)&długość_dane);
    if (towar_ILE_LICZB >= 0) { for (intptr_t 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) cel_ADRES_08bbd577[순번 + 1] = dane[순번]; cel_ADRES_08bbd577[513] = (첫째값.numer_portu << 8 | 첫째값.numer_portu >> 8) & 65535; cel_ADRES_08bbd577[514] = 바이트순서뒤집기(첫째값.Adres); }
    return (uint32_t)towar_ILE_LICZB;
}
maszyna_Word narzędzie_UDP_port(maszyna_Word dojście_do_pliku) {
    struct 자바주소 첫째값; unsigned długość_dane = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, dojście_do_pliku, (maszyna_Word)&첫째값, (maszyna_Word)&długość_dane);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.numer_portu << 8 | 첫째값.numer_portu >> 8) & 65535);
}
maszyna_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
maszyna_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
maszyna_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
maszyna_Word narzędzie_grafika_chwileczkę(void) { return (uint32_t)화면키기다리기(); }
maszyna_Word narzędzie_prostokąt(maszyna_Word współrzędna_X, maszyna_Word Y_współrzędna, maszyna_Word 너비값, maszyna_Word wymagane_wysokość_WARTOŚĆ, maszyna_Word 색상) {
    return (uint32_t)사용자호출(13, współrzędna_X, Y_współrzędna, 색상, 너비값, wymagane_wysokość_WARTOŚĆ, 0);
}

maszyna_Word narzędzie_Stream(maszyna_Word Akcja,maszyna_Word dojście_do_pliku,maszyna_Word WARTOŚĆ){
    if(Akcja==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADRES(WARTOŚĆ);
    if(Akcja==1){첫째값.Adres=0;intptr_t 반환값=호출(33,dojście_do_pliku,(maszyna_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,dojście_do_pliku,4,0));}
    if(Akcja==2)return (uint32_t)호출(37,dojście_do_pliku,(maszyna_Word)&첫째값,sizeof(첫째값));
    if(Akcja==3)return (uint32_t)호출(39,dojście_do_pliku,0,0);
    if(Akcja==4)return narzędzie_UDP_port(dojście_do_pliku);
    if(Akcja==5)return (uint32_t)호출(40,dojście_do_pliku,0,0);
    return (uint32_t)-22;
}
maszyna_Word narzędzie_GUI(maszyna_Word Akcja,maszyna_Word identyfikator_WARTOŚĆ,maszyna_Word 첫째값,maszyna_Word SEKUNDA_WARTOŚĆ,maszyna_Word kod_znaku,maszyna_Word cel_dane){return (uint32_t)사용자호출(20,Akcja,identyfikator_WARTOŚĆ,첫째값,SEKUNDA_WARTOŚĆ,kod_znaku,cel_dane);}
maszyna_Word narzędzie_GUI_SMS(maszyna_Word identyfikator_WARTOŚĆ,maszyna_Word TABLICA_WARTOŚĆ,maszyna_Word towar_ILE_LICZB){
    const maszyna_Word *원본주소=(const maszyna_Word *)TABLICA_WARTOŚĆ;uint32_t dane[127];unsigned wpis_ILE_LICZB=0;
    if(towar_ILE_LICZB>원본주소[0])return (uint32_t)-22;
    for(maszyna_Word 순번=0;순번<towar_ILE_LICZB;순번++){unsigned kodowanie_znaku=원본주소[순번+1];if(kodowanie_znaku>=0xd800&&kodowanie_znaku<=0xdbff&&순번+1<towar_ILE_LICZB){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;kodowanie_znaku=0x10000+((kodowanie_znaku-0xd800)<<10)+낮은값-0xdc00;}if(wpis_ILE_LICZB==127)return (uint32_t)-22;dane[wpis_ILE_LICZB++]=kodowanie_znaku;}
    return (uint32_t)사용자호출(21,identyfikator_WARTOŚĆ,(maszyna_Word)dane,wpis_ILE_LICZB,0,0,0);
}
