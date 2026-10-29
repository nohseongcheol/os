#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Datoteka/Izpis/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "sveženj.h"
typedef uintptr_t računalnik_Word;
static int območje_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static računalnik_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned element_COUNT, računalnik_Word 첫째값, računalnik_Word SECOND_VALUE, računalnik_Word koda_znaka) {
    return 사용자호출(element_COUNT, 첫째값, SECOND_VALUE, koda_znaka, 0, 0, 0);
}
static void 바이트들(const char *podatki_položaj, size_t element_COUNT) { 호출(1, 1, (računalnik_Word)podatki_položaj, element_COUNT); }
static void znak(unsigned koda_znaka) {
    unsigned char podatki[4]; unsigned element_COUNT = 0;
    if (koda_znaka < 128) podatki[element_COUNT++] = koda_znaka;
    else if (koda_znaka < 2048) { podatki[element_COUNT++] = 0xc0 | (koda_znaka >> 6); podatki[element_COUNT++] = 0x80 | (koda_znaka & 63); }
    else if (koda_znaka < 65536) { podatki[element_COUNT++] = 0xe0 | (koda_znaka >> 12); podatki[element_COUNT++] = 0x80 | ((koda_znaka >> 6) & 63); podatki[element_COUNT++] = 0x80 | (koda_znaka & 63); }
    else { podatki[element_COUNT++] = 0xf0 | (koda_znaka >> 18); podatki[element_COUNT++] = 0x80 | ((koda_znaka >> 12) & 63); podatki[element_COUNT++] = 0x80 | ((koda_znaka >> 6) & 63); podatki[element_COUNT++] = 0x80 | (koda_znaka & 63); }
    바이트들((const char *)podatki, element_COUNT);
}
računalnik_Word orodje_znak(računalnik_Word VALUE) {
    unsigned koda_znaka = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (koda_znaka >= 0xdc00 && koda_znaka <= 0xdfff) { znak(0x10000 + ((높은부분 - 0xd800) << 10) + koda_znaka - 0xdc00); return 1; }
        znak(0xfffd);
    }
    if (koda_znaka >= 0xd800 && koda_znaka <= 0xdbff) 대기중짝글자 = koda_znaka;
    else znak(koda_znaka > 0x10ffff || (koda_znaka >= 0xdc00 && koda_znaka <= 0xdfff) ? 0xfffd : koda_znaka);
    return 1;
}
računalnik_Word 도구출력(računalnik_Word VALUE) {
    const računalnik_Word *niz_podatki = (const računalnik_Word *)VALUE;
    for (računalnik_Word 순번 = 0; 순번 < niz_podatki[0]; 순번++) orodje_znak(niz_podatki[순번 + 1]);
    return niz_podatki[0];
}
static int POT(računalnik_Word predmet_Gradiva, char KR_podatki[512]) {
    const računalnik_Word *첫째값 = (const računalnik_Word *)predmet_Gradiva;
    unsigned 사용량 = 0;
    for (računalnik_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned koda_znaka = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metoda_MODE 경로와 호환한다.
        if (koda_znaka >= 0xd800 && koda_znaka <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; koda_znaka = 0x10000 + ((koda_znaka - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (koda_znaka >= 0xd800 && koda_znaka <= 0xdfff) return -22;
        unsigned element_COUNT = koda_znaka < 128 ? 1 : koda_znaka < 2048 ? 2 : koda_znaka < 65536 ? 3 : 4;
        if (사용량 + element_COUNT > 511) return -36;
        if (element_COUNT == 1) KR_podatki[사용량++] = koda_znaka;
        else {
            KR_podatki[사용량++] = (element_COUNT == 2 ? 0xc0 : element_COUNT == 3 ? 0xe0 : 0xf0) | (koda_znaka >> (6 * (element_COUNT - 1)));
            for (unsigned 안쪽순번 = element_COUNT - 1; 안쪽순번; 안쪽순번--) KR_podatki[사용량++] = 0x80 | ((koda_znaka >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_podatki[사용량] = 0; return 사용량 ? 0 : -22;
}
računalnik_Word orodje_odprto(računalnik_Word Ime, računalnik_Word konfiguracija_storitev_Background_Intelligent_Transfer_Service) {
    char podatki_položaj[512]; int NAPAKA = POT(Ime, podatki_položaj);
    return (uint32_t)(NAPAKA ? NAPAKA : 호출(3, (računalnik_Word)podatki_položaj, konfiguracija_storitev_Background_Intelligent_Transfer_Service, 0));
}
računalnik_Word orodje_Zapri(računalnik_Word Datoteka_ročica) { return (uint32_t)호출(4, Datoteka_ročica, 0, 0); }
računalnik_Word 도구바이트읽기(računalnik_Word Datoteka_ročica) {
    unsigned char SECOND_VALUE; intptr_t element_COUNT = 호출(2, Datoteka_ročica, (računalnik_Word)&SECOND_VALUE, 1);
    return (uint32_t)(element_COUNT == 1 ? SECOND_VALUE : element_COUNT == 0 ? 256 : element_COUNT);
}
računalnik_Word orodje_pisati_bajt(računalnik_Word Datoteka_ročica, računalnik_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Datoteka_ročica, (računalnik_Word)&SECOND_VALUE, 1);
}
računalnik_Word 도구읽기(računalnik_Word Ime, računalnik_Word cilj_podatki_naslov) {
    if (꾸러미사용중) {
        char podatki_položaj[512]; int NAPAKA = POT(Ime, podatki_položaj); if (NAPAKA) return (uint32_t)NAPAKA;
        unsigned element_COUNT = 0; while (podatki_položaj[element_COUNT]) element_COUNT++;
        if (element_COUNT >= 6) for (unsigned 순번 = 0; 순번 < element_COUNT - 6; 순번++) if (podatki_položaj[순번] == '.') podatki_položaj[순번] = '/';
        unsigned char 바이트들[16384]; računalnik_Word *cilj_VALUE_položaj = (računalnik_Word *)cilj_podatki_naslov;
        int RECEIVED_COUNT = 꾸러미읽기(podatki_položaj, 바이트들, cilj_VALUE_položaj[0] < sizeof(바이트들) ? cilj_VALUE_položaj[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) cilj_VALUE_položaj[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Datoteka_ročica = 꾸러미사용중 ? -2 : (int32_t)orodje_odprto(Ime, 0);
    if (Datoteka_ročica < 0) {
        char podatki_položaj[512]; int NAPAKA = POT(Ime, podatki_položaj); if (NAPAKA) return (uint32_t)NAPAKA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Naprej_odmik = 자바클래스들[순번].Ime; unsigned 안쪽순번 = 0;
            while (podatki_položaj[안쪽순번] && podatki_položaj[안쪽순번] == Naprej_odmik[안쪽순번]) 안쪽순번++;
            if (podatki_položaj[안쪽순번] || Naprej_odmik[안쪽순번]) continue;
            računalnik_Word *cilj_VALUE_položaj = (računalnik_Word *)cilj_podatki_naslov;
            if (cilj_VALUE_položaj[0] < 자바클래스들[순번].Velikost) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Velikost; 안쪽순번++) cilj_VALUE_položaj[안쪽순번 + 1] = 자바클래스들[순번].podatki[안쪽순번];
            return 자바클래스들[순번].Velikost;
        }
        return (uint32_t)Datoteka_ročica;
    }
    računalnik_Word *첫째값 = (računalnik_Word *)cilj_podatki_naslov;
    intptr_t Velikost = 호출(9, Datoteka_ročica, 0, 0), Dokončano_znesek = 0;
    if (Velikost < 0 || (računalnik_Word)Velikost > 첫째값[0]) { orodje_Zapri(Datoteka_ročica); return (uint32_t)(Velikost < 0 ? Velikost : -27); }
    unsigned char blok_podatkov[256];
    while (Dokončano_znesek < Velikost) {
        intptr_t element_COUNT = 호출(2, Datoteka_ročica, (računalnik_Word)blok_podatkov, Velikost - Dokončano_znesek < 256 ? Velikost - Dokončano_znesek : 256);
        if (element_COUNT <= 0) { orodje_Zapri(Datoteka_ročica); return (uint32_t)(element_COUNT ? element_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) 첫째값[1 + Dokončano_znesek + 순번] = blok_podatkov[순번];
        Dokončano_znesek += element_COUNT;
    }
    orodje_Zapri(Datoteka_ročica); return Dokončano_znesek;
}
računalnik_Word orodje_pisati(računalnik_Word Ime, računalnik_Word 원본자료, računalnik_Word vnos_COUNT) {
    const računalnik_Word *첫째값 = (const računalnik_Word *)원본자료;
    if (vnos_COUNT > 첫째값[0] || vnos_COUNT > 16384) return (uint32_t)-27;
    int Datoteka_ročica = (int32_t)orodje_odprto(Ime, 577); if (Datoteka_ročica < 0) return (uint32_t)Datoteka_ročica;
    unsigned char blok_podatkov[256]; računalnik_Word Dokončano_znesek = 0;
    while (Dokončano_znesek < vnos_COUNT) {
        računalnik_Word element_COUNT = vnos_COUNT - Dokončano_znesek < 256 ? vnos_COUNT - Dokončano_znesek : 256;
        for (računalnik_Word 순번 = 0; 순번 < element_COUNT; 순번++) blok_podatkov[순번] = 첫째값[1 + Dokončano_znesek + 순번];
        intptr_t REZULTAT = 호출(1, Datoteka_ročica, (računalnik_Word)blok_podatkov, element_COUNT);
        if (REZULTAT <= 0) { orodje_Zapri(Datoteka_ročica); return (uint32_t)(REZULTAT ? REZULTAT : -5); }
        Dokončano_znesek += REZULTAT;
    }
    orodje_Zapri(Datoteka_ročica); return vnos_COUNT;
}
računalnik_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
računalnik_Word orodje_argument(računalnik_Word LOOKUP_INDEX) {
    static const računalnik_Word prazen_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (računalnik_Word)prazen_VALUE;
    unsigned char 입력결과[256]; intptr_t element_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *podatki_položaj = 꾸러미진입클래스(); element_COUNT = 0; while (podatki_položaj[element_COUNT] && element_COUNT < 255) { 입력결과[element_COUNT] = podatki_položaj[element_COUNT]; element_COUNT++; } }
    else element_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (računalnik_Word)입력결과, sizeof(입력결과));
    if (element_COUNT < 0) return (računalnik_Word)prazen_VALUE;
    računalnik_Word *KR_podatki = 전달인수[LOOKUP_INDEX]; unsigned vnos_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < element_COUNT;) {
        unsigned koda_znaka = 입력결과[순번++], 더있음 = koda_znaka < 128 ? 0 : koda_znaka >= 0xc2 && koda_znaka < 0xe0 ? 1 : koda_znaka < 0xf0 && koda_znaka >= 0xe0 ? 2 : koda_znaka >= 0xf0 && koda_znaka <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > element_COUNT) { KR_podatki[++vnos_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) koda_znaka &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { koda_znaka = (koda_znaka << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || koda_znaka < 최소값 || koda_znaka > 0x10ffff || (koda_znaka >= 0xd800 && koda_znaka <= 0xdfff)) koda_znaka = 0xfffd;
        if (koda_znaka >= 65536) { koda_znaka -= 65536; KR_podatki[++vnos_COUNT] = 0xd800 | (koda_znaka >> 10); KR_podatki[++vnos_COUNT] = 0xdc00 | (koda_znaka & 1023); }
        else KR_podatki[++vnos_COUNT] = koda_znaka;
    }
    KR_podatki[0] = vnos_COUNT; return (računalnik_Word)KR_podatki;
}
računalnik_Word 도구분류(void) { return območje_VALUE; }
void 커널중단(const char *obvestilo_SMS) {
    const char *podatki_položaj = obvestilo_SMS; while (*podatki_položaj) podatki_položaj++;
    바이트들("Java tool runtime error: ", 25); 바이트들(obvestilo_SMS, podatki_položaj - obvestilo_SMS); znak(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_uporabnik_aplikacija(int metoda_MODE) {
    območje_VALUE = metoda_MODE;
    unsigned char 첫항목[256]; intptr_t element_COUNT = 호출(15, 0, (računalnik_Word)첫항목, sizeof(첫항목));
    if (metoda_MODE == 2 || (metoda_MODE == 1 && element_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metoda_MODE == 2 ? 0 : 1;
        char Datoteka_vnos_ime[256]; intptr_t 길이값 = 호출(15, 꾸러미인수이동, (računalnik_Word)Datoteka_vnos_ime, sizeof(Datoteka_vnos_ime));
        if (길이값 <= 0 || 꾸러미열기(Datoteka_vnos_ime) < 0) {
            static const char NAPAKA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(NAPAKA, sizeof(NAPAKA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int REZULTAT = 자바진입();
    if (대기중짝글자) znak(0xfffd);
    return REZULTAT;
}

// UDP는 lastno 커널의 SVC를 통과하며 sprotno_element 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Družina, številka_vrat; uint32_t naslov; unsigned char ničelna_vrednost[8]; };
static struct 자바주소 UDP_naslov(unsigned številka_vrat) {
    struct 자바주소 첫째값 = {2, (uint16_t)((številka_vrat << 8) | (številka_vrat >> 8)), 0x0100007f, {0}}; return 첫째값;
}
računalnik_Word orodje_UDP_odprto(računalnik_Word številka_vrat) {
    intptr_t Datoteka_ročica = 호출(32, 2, 2, 17); if (Datoteka_ročica < 0) return (uint32_t)Datoteka_ročica;
    struct 자바주소 첫째값 = UDP_naslov(številka_vrat);
    첫째값.naslov = 0;
    intptr_t stanje_VALUE = 호출(33, Datoteka_ročica, (računalnik_Word)&첫째값, sizeof(첫째값));
    if (stanje_VALUE < 0) { orodje_Zapri(Datoteka_ročica); return (uint32_t)stanje_VALUE; }
    return Datoteka_ročica;
}
računalnik_Word orodje_UDP_poslati(računalnik_Word Datoteka_ročica, računalnik_Word številka_vrat, računalnik_Word ARRAY_VALUE, računalnik_Word 길이) {
    const računalnik_Word *원본주소 = (const računalnik_Word *)ARRAY_VALUE; unsigned char podatki[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (računalnik_Word 순번 = 0; 순번 < 길이; 순번++) podatki[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_naslov(številka_vrat);
    return (uint32_t)사용자호출(34, Datoteka_ročica, (računalnik_Word)podatki, 길이, 0, (računalnik_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t element_COUNT) { return (element_COUNT>>24)|((element_COUNT>>8)&0xff00)|((element_COUNT<<8)&0xff0000)|(element_COUNT<<24); }
računalnik_Word orodje_UDP_poslati_naslov(računalnik_Word Datoteka_ročica, računalnik_Word naslov, računalnik_Word številka_vrat, računalnik_Word ARRAY_VALUE, računalnik_Word 길이) {
    const računalnik_Word *원본주소 = (const računalnik_Word *)ARRAY_VALUE; unsigned char podatki[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (računalnik_Word 순번 = 0; 순번 < 길이; 순번++) podatki[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_naslov(številka_vrat); 첫째값.naslov = 바이트순서뒤집기(naslov);
    return (uint32_t)사용자호출(34, Datoteka_ročica, (računalnik_Word)podatki, 길이, 0, (računalnik_Word)&첫째값, sizeof(첫째값));
}
računalnik_Word orodje_POVEŽI(računalnik_Word Datoteka_ročica, računalnik_Word naslov, računalnik_Word številka_vrat) {
    struct 자바주소 첫째값 = UDP_naslov(številka_vrat); 첫째값.naslov = 바이트순서뒤집기(naslov);
    uint32_t Zaženi = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t REZULTAT = 호출(37, Datoteka_ročica, (računalnik_Word)&첫째값, sizeof(첫째값));
        if (REZULTAT != -115) return (uint32_t)REZULTAT;
        if ((uint32_t)(호출(7, 0, 0, 0) - Zaženi) >= 1000) return (uint32_t)-110;
    }
}
računalnik_Word 도구전문받기(računalnik_Word Datoteka_ročica, računalnik_Word ARRAY_VALUE, računalnik_Word medpomnilnik_zmogljivost) {
    računalnik_Word *cilj_naslov_08bbd577 = (računalnik_Word *)ARRAY_VALUE; unsigned char podatki[512];
    if (medpomnilnik_zmogljivost > 512 || cilj_naslov_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t element_COUNT = 사용자호출(35, Datoteka_ročica, (računalnik_Word)podatki, medpomnilnik_zmogljivost, 0, (računalnik_Word)&첫째값, (računalnik_Word)&길이값);
    if (element_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) cilj_naslov_08bbd577[순번 + 1] = podatki[순번]; cilj_naslov_08bbd577[513] = (첫째값.številka_vrat << 8 | 첫째값.številka_vrat >> 8) & 65535; cilj_naslov_08bbd577[514] = 바이트순서뒤집기(첫째값.naslov); }
    return (uint32_t)element_COUNT;
}
računalnik_Word orodje_UDP_vrata(računalnik_Word Datoteka_ročica) {
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Datoteka_ročica, (računalnik_Word)&첫째값, (računalnik_Word)&길이값);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.številka_vrat << 8 | 첫째값.številka_vrat >> 8) & 65535);
}
računalnik_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
računalnik_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
računalnik_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
računalnik_Word orodje_grafični_elementi_počakaj(void) { return (uint32_t)화면키기다리기(); }
računalnik_Word orodje_pravokotnik(računalnik_Word koordinata_x, računalnik_Word 세로좌표, računalnik_Word 너비값, računalnik_Word 높이값, računalnik_Word 색상) {
    return (uint32_t)사용자호출(13, koordinata_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

računalnik_Word orodje_tok(računalnik_Word Dejanje,računalnik_Word Datoteka_ročica,računalnik_Word VALUE){
    if(Dejanje==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_naslov(VALUE);
    if(Dejanje==1){첫째값.naslov=0;intptr_t 반환값=호출(33,Datoteka_ročica,(računalnik_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Datoteka_ročica,4,0));}
    if(Dejanje==2)return (uint32_t)호출(37,Datoteka_ročica,(računalnik_Word)&첫째값,sizeof(첫째값));
    if(Dejanje==3)return (uint32_t)호출(39,Datoteka_ročica,0,0);
    if(Dejanje==4)return orodje_UDP_vrata(Datoteka_ročica);
    if(Dejanje==5)return (uint32_t)호출(40,Datoteka_ročica,0,0);
    return (uint32_t)-22;
}
računalnik_Word orodje_grafični_uporabniški_vmesnik(računalnik_Word Dejanje,računalnik_Word identifikator_VALUE,računalnik_Word 첫째값,računalnik_Word SECOND_VALUE,računalnik_Word koda_znaka,računalnik_Word cilj_podatki){return (uint32_t)사용자호출(20,Dejanje,identifikator_VALUE,첫째값,SECOND_VALUE,koda_znaka,cilj_podatki);}
računalnik_Word orodje_grafični_uporabniški_vmesnik_SMS(računalnik_Word identifikator_VALUE,računalnik_Word ARRAY_VALUE,računalnik_Word element_COUNT){
    const računalnik_Word *원본주소=(const računalnik_Word *)ARRAY_VALUE;uint32_t podatki[127];unsigned vnos_COUNT=0;
    if(element_COUNT>원본주소[0])return (uint32_t)-22;
    for(računalnik_Word 순번=0;순번<element_COUNT;순번++){unsigned kodiranje_znakov=원본주소[순번+1];if(kodiranje_znakov>=0xd800&&kodiranje_znakov<=0xdbff&&순번+1<element_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;kodiranje_znakov=0x10000+((kodiranje_znakov-0xd800)<<10)+낮은값-0xdc00;}if(vnos_COUNT==127)return (uint32_t)-22;podatki[vnos_COUNT++]=kodiranje_znakov;}
    return (uint32_t)사용자호출(21,identifikator_VALUE,(računalnik_Word)podatki,vnos_COUNT,0,0,0);
}
