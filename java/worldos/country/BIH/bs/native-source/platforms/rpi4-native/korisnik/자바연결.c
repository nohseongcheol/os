#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fajl/Ispis/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "paket.h"
typedef uintptr_t mašina_Word;
static int oblast_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static mašina_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned stavka_COUNT, mašina_Word 첫째값, mašina_Word SECOND_VALUE, mašina_Word kôd_znaka) {
    return 사용자호출(stavka_COUNT, 첫째값, SECOND_VALUE, kôd_znaka, 0, 0, 0);
}
static void 바이트들(const char *podaci_položaj, size_t stavka_COUNT) { 호출(1, 1, (mašina_Word)podaci_položaj, stavka_COUNT); }
static void znak(unsigned kôd_znaka) {
    unsigned char podaci[4]; unsigned stavka_COUNT = 0;
    if (kôd_znaka < 128) podaci[stavka_COUNT++] = kôd_znaka;
    else if (kôd_znaka < 2048) { podaci[stavka_COUNT++] = 0xc0 | (kôd_znaka >> 6); podaci[stavka_COUNT++] = 0x80 | (kôd_znaka & 63); }
    else if (kôd_znaka < 65536) { podaci[stavka_COUNT++] = 0xe0 | (kôd_znaka >> 12); podaci[stavka_COUNT++] = 0x80 | ((kôd_znaka >> 6) & 63); podaci[stavka_COUNT++] = 0x80 | (kôd_znaka & 63); }
    else { podaci[stavka_COUNT++] = 0xf0 | (kôd_znaka >> 18); podaci[stavka_COUNT++] = 0x80 | ((kôd_znaka >> 12) & 63); podaci[stavka_COUNT++] = 0x80 | ((kôd_znaka >> 6) & 63); podaci[stavka_COUNT++] = 0x80 | (kôd_znaka & 63); }
    바이트들((const char *)podaci, stavka_COUNT);
}
mašina_Word alatka_znak(mašina_Word VALUE) {
    unsigned kôd_znaka = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kôd_znaka >= 0xdc00 && kôd_znaka <= 0xdfff) { znak(0x10000 + ((높은부분 - 0xd800) << 10) + kôd_znaka - 0xdc00); return 1; }
        znak(0xfffd);
    }
    if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff) 대기중짝글자 = kôd_znaka;
    else znak(kôd_znaka > 0x10ffff || (kôd_znaka >= 0xdc00 && kôd_znaka <= 0xdfff) ? 0xfffd : kôd_znaka);
    return 1;
}
mašina_Word 도구출력(mašina_Word VALUE) {
    const mašina_Word *string_podaci = (const mašina_Word *)VALUE;
    for (mašina_Word 순번 = 0; 순번 < string_podaci[0]; 순번++) alatka_znak(string_podaci[순번 + 1]);
    return string_podaci[0];
}
static int Putanja(mašina_Word objekt_Reference, char mjera_podaci[512]) {
    const mašina_Word *첫째값 = (const mašina_Word *)objekt_Reference;
    unsigned 사용량 = 0;
    for (mašina_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kôd_znaka = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metoda_mod 경로와 호환한다.
        if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) return -22;
        unsigned stavka_COUNT = kôd_znaka < 128 ? 1 : kôd_znaka < 2048 ? 2 : kôd_znaka < 65536 ? 3 : 4;
        if (사용량 + stavka_COUNT > 511) return -36;
        if (stavka_COUNT == 1) mjera_podaci[사용량++] = kôd_znaka;
        else {
            mjera_podaci[사용량++] = (stavka_COUNT == 2 ? 0xc0 : stavka_COUNT == 3 ? 0xe0 : 0xf0) | (kôd_znaka >> (6 * (stavka_COUNT - 1)));
            for (unsigned 안쪽순번 = stavka_COUNT - 1; 안쪽순번; 안쪽순번--) mjera_podaci[사용량++] = 0x80 | ((kôd_znaka >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    mjera_podaci[사용량] = 0; return 사용량 ? 0 : -22;
}
mašina_Word alatka_kreirati(mašina_Word Naziv, mašina_Word 설정비트) {
    char podaci_položaj[512]; int GRESKA = Putanja(Naziv, podaci_položaj);
    return (uint32_t)(GRESKA ? GRESKA : 호출(3, (mašina_Word)podaci_položaj, 설정비트, 0));
}
mašina_Word alatka_zatvoriti(mašina_Word fajl_hvatište) { return (uint32_t)호출(4, fajl_hvatište, 0, 0); }
mašina_Word 도구바이트읽기(mašina_Word fajl_hvatište) {
    unsigned char SECOND_VALUE; intptr_t stavka_COUNT = 호출(2, fajl_hvatište, (mašina_Word)&SECOND_VALUE, 1);
    return (uint32_t)(stavka_COUNT == 1 ? SECOND_VALUE : stavka_COUNT == 0 ? 256 : stavka_COUNT);
}
mašina_Word alatka_pisati_bajt(mašina_Word fajl_hvatište, mašina_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, fajl_hvatište, (mašina_Word)&SECOND_VALUE, 1);
}
mašina_Word 도구읽기(mašina_Word Naziv, mašina_Word odredište_podaci_adresa) {
    if (꾸러미사용중) {
        char podaci_položaj[512]; int GRESKA = Putanja(Naziv, podaci_položaj); if (GRESKA) return (uint32_t)GRESKA;
        unsigned stavka_COUNT = 0; while (podaci_položaj[stavka_COUNT]) stavka_COUNT++;
        if (stavka_COUNT >= 6) for (unsigned 순번 = 0; 순번 < stavka_COUNT - 6; 순번++) if (podaci_položaj[순번] == '.') podaci_položaj[순번] = '/';
        unsigned char 바이트들[16384]; mašina_Word *odredište_VALUE_položaj = (mašina_Word *)odredište_podaci_adresa;
        int RECEIVED_COUNT = 꾸러미읽기(podaci_položaj, 바이트들, odredište_VALUE_položaj[0] < sizeof(바이트들) ? odredište_VALUE_položaj[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) odredište_VALUE_položaj[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int fajl_hvatište = 꾸러미사용중 ? -2 : (int32_t)alatka_kreirati(Naziv, 0);
    if (fajl_hvatište < 0) {
        char podaci_položaj[512]; int GRESKA = Putanja(Naziv, podaci_položaj); if (GRESKA) return (uint32_t)GRESKA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Dalje_Pomak = 자바클래스들[순번].Naziv; unsigned 안쪽순번 = 0;
            while (podaci_položaj[안쪽순번] && podaci_položaj[안쪽순번] == Dalje_Pomak[안쪽순번]) 안쪽순번++;
            if (podaci_položaj[안쪽순번] || Dalje_Pomak[안쪽순번]) continue;
            mašina_Word *odredište_VALUE_položaj = (mašina_Word *)odredište_podaci_adresa;
            if (odredište_VALUE_položaj[0] < 자바클래스들[순번].Veličina) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Veličina; 안쪽순번++) odredište_VALUE_položaj[안쪽순번 + 1] = 자바클래스들[순번].podaci[안쪽순번];
            return 자바클래스들[순번].Veličina;
        }
        return (uint32_t)fajl_hvatište;
    }
    mašina_Word *첫째값 = (mašina_Word *)odredište_podaci_adresa;
    intptr_t Veličina = 호출(9, fajl_hvatište, 0, 0), 완료량 = 0;
    if (Veličina < 0 || (mašina_Word)Veličina > 첫째값[0]) { alatka_zatvoriti(fajl_hvatište); return (uint32_t)(Veličina < 0 ? Veličina : -27); }
    unsigned char podaci_blokirati[256];
    while (완료량 < Veličina) {
        intptr_t stavka_COUNT = 호출(2, fajl_hvatište, (mašina_Word)podaci_blokirati, Veličina - 완료량 < 256 ? Veličina - 완료량 : 256);
        if (stavka_COUNT <= 0) { alatka_zatvoriti(fajl_hvatište); return (uint32_t)(stavka_COUNT ? stavka_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < stavka_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = podaci_blokirati[순번];
        완료량 += stavka_COUNT;
    }
    alatka_zatvoriti(fajl_hvatište); return 완료량;
}
mašina_Word alatka_pisati(mašina_Word Naziv, mašina_Word 원본자료, mašina_Word unos_COUNT) {
    const mašina_Word *첫째값 = (const mašina_Word *)원본자료;
    if (unos_COUNT > 첫째값[0] || unos_COUNT > 16384) return (uint32_t)-27;
    int fajl_hvatište = (int32_t)alatka_kreirati(Naziv, 577); if (fajl_hvatište < 0) return (uint32_t)fajl_hvatište;
    unsigned char podaci_blokirati[256]; mašina_Word 완료량 = 0;
    while (완료량 < unos_COUNT) {
        mašina_Word stavka_COUNT = unos_COUNT - 완료량 < 256 ? unos_COUNT - 완료량 : 256;
        for (mašina_Word 순번 = 0; 순번 < stavka_COUNT; 순번++) podaci_blokirati[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t mjera = 호출(1, fajl_hvatište, (mašina_Word)podaci_blokirati, stavka_COUNT);
        if (mjera <= 0) { alatka_zatvoriti(fajl_hvatište); return (uint32_t)(mjera ? mjera : -5); }
        완료량 += mjera;
    }
    alatka_zatvoriti(fajl_hvatište); return unos_COUNT;
}
mašina_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mašina_Word alatka_argument(mašina_Word LOOKUP_INDEX) {
    static const mašina_Word prazno_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (mašina_Word)prazno_VALUE;
    unsigned char 입력결과[256]; intptr_t stavka_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *podaci_položaj = 꾸러미진입클래스(); stavka_COUNT = 0; while (podaci_položaj[stavka_COUNT] && stavka_COUNT < 255) { 입력결과[stavka_COUNT] = podaci_položaj[stavka_COUNT]; stavka_COUNT++; } }
    else stavka_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mašina_Word)입력결과, sizeof(입력결과));
    if (stavka_COUNT < 0) return (mašina_Word)prazno_VALUE;
    mašina_Word *mjera_podaci = 전달인수[LOOKUP_INDEX]; unsigned unos_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < stavka_COUNT;) {
        unsigned kôd_znaka = 입력결과[순번++], 더있음 = kôd_znaka < 128 ? 0 : kôd_znaka >= 0xc2 && kôd_znaka < 0xe0 ? 1 : kôd_znaka < 0xf0 && kôd_znaka >= 0xe0 ? 2 : kôd_znaka >= 0xf0 && kôd_znaka <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > stavka_COUNT) { mjera_podaci[++unos_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kôd_znaka &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kôd_znaka = (kôd_znaka << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kôd_znaka < 최소값 || kôd_znaka > 0x10ffff || (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff)) kôd_znaka = 0xfffd;
        if (kôd_znaka >= 65536) { kôd_znaka -= 65536; mjera_podaci[++unos_COUNT] = 0xd800 | (kôd_znaka >> 10); mjera_podaci[++unos_COUNT] = 0xdc00 | (kôd_znaka & 1023); }
        else mjera_podaci[++unos_COUNT] = kôd_znaka;
    }
    mjera_podaci[0] = unos_COUNT; return (mašina_Word)mjera_podaci;
}
mašina_Word 도구분류(void) { return oblast_VALUE; }
void 커널중단(const char *알림문) {
    const char *podaci_položaj = 알림문; while (*podaci_položaj) podaci_položaj++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, podaci_položaj - 알림문); znak(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_korisnik_program(int metoda_mod) {
    oblast_VALUE = metoda_mod;
    unsigned char 첫항목[256]; intptr_t stavka_COUNT = 호출(15, 0, (mašina_Word)첫항목, sizeof(첫항목));
    if (metoda_mod == 2 || (metoda_mod == 1 && stavka_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metoda_mod == 2 ? 0 : 1;
        char fajl_unos_naziv[256]; intptr_t dužina_podaci = 호출(15, 꾸러미인수이동, (mašina_Word)fajl_unos_naziv, sizeof(fajl_unos_naziv));
        if (dužina_podaci <= 0 || 꾸러미열기(fajl_unos_naziv) < 0) {
            static const char GRESKA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(GRESKA, sizeof(GRESKA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int mjera = 자바진입();
    if (대기중짝글자) znak(0xfffd);
    return mjera;
}

// UDP는 자체 커널의 SVC를 통과하며 trenutno_stavka 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Porodica, broj_priključka; uint32_t adresa; unsigned char 영값[8]; };
static struct 자바주소 UDP_adresa(unsigned broj_priključka) {
    struct 자바주소 첫째값 = {2, (uint16_t)((broj_priključka << 8) | (broj_priključka >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mašina_Word alatka_UDP_kreirati(mašina_Word broj_priključka) {
    intptr_t fajl_hvatište = 호출(32, 2, 2, 17); if (fajl_hvatište < 0) return (uint32_t)fajl_hvatište;
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka);
    첫째값.adresa = 0;
    intptr_t stanje_VALUE = 호출(33, fajl_hvatište, (mašina_Word)&첫째값, sizeof(첫째값));
    if (stanje_VALUE < 0) { alatka_zatvoriti(fajl_hvatište); return (uint32_t)stanje_VALUE; }
    return fajl_hvatište;
}
mašina_Word alatka_UDP_poslati(mašina_Word fajl_hvatište, mašina_Word broj_priključka, mašina_Word niz_VALUE, mašina_Word dužina_VALUE) {
    const mašina_Word *원본주소 = (const mašina_Word *)niz_VALUE; unsigned char podaci[512];
    if (dužina_VALUE > 512 || dužina_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mašina_Word 순번 = 0; 순번 < dužina_VALUE; 순번++) podaci[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka);
    return (uint32_t)사용자호출(34, fajl_hvatište, (mašina_Word)podaci, dužina_VALUE, 0, (mašina_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t stavka_COUNT) { return (stavka_COUNT>>24)|((stavka_COUNT>>8)&0xff00)|((stavka_COUNT<<8)&0xff0000)|(stavka_COUNT<<24); }
mašina_Word alatka_UDP_poslati_adresa(mašina_Word fajl_hvatište, mašina_Word adresa, mašina_Word broj_priključka, mašina_Word niz_VALUE, mašina_Word dužina_VALUE) {
    const mašina_Word *원본주소 = (const mašina_Word *)niz_VALUE; unsigned char podaci[512];
    if (dužina_VALUE > 512 || dužina_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mašina_Word 순번 = 0; 순번 < dužina_VALUE; 순번++) podaci[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka); 첫째값.adresa = 바이트순서뒤집기(adresa);
    return (uint32_t)사용자호출(34, fajl_hvatište, (mašina_Word)podaci, dužina_VALUE, 0, (mašina_Word)&첫째값, sizeof(첫째값));
}
mašina_Word alatka_povezati(mašina_Word fajl_hvatište, mašina_Word adresa, mašina_Word broj_priključka) {
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka); 첫째값.adresa = 바이트순서뒤집기(adresa);
    uint32_t Pokreni = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t mjera = 호출(37, fajl_hvatište, (mašina_Word)&첫째값, sizeof(첫째값));
        if (mjera != -115) return (uint32_t)mjera;
        if ((uint32_t)(호출(7, 0, 0, 0) - Pokreni) >= 1000) return (uint32_t)-110;
    }
}
mašina_Word 도구전문받기(mašina_Word fajl_hvatište, mašina_Word niz_VALUE, mašina_Word 수용량) {
    mašina_Word *odredište_adresa = (mašina_Word *)niz_VALUE; unsigned char podaci[512];
    if (수용량 > 512 || odredište_adresa[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned dužina_podaci = sizeof(첫째값);
    intptr_t stavka_COUNT = 사용자호출(35, fajl_hvatište, (mašina_Word)podaci, 수용량, 0, (mašina_Word)&첫째값, (mašina_Word)&dužina_podaci);
    if (stavka_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < stavka_COUNT; 순번++) odredište_adresa[순번 + 1] = podaci[순번]; odredište_adresa[513] = (첫째값.broj_priključka << 8 | 첫째값.broj_priključka >> 8) & 65535; odredište_adresa[514] = 바이트순서뒤집기(첫째값.adresa); }
    return (uint32_t)stavka_COUNT;
}
mašina_Word alatka_UDP_port(mašina_Word fajl_hvatište) {
    struct 자바주소 첫째값; unsigned dužina_podaci = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fajl_hvatište, (mašina_Word)&첫째값, (mašina_Word)&dužina_podaci);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.broj_priključka << 8 | 첫째값.broj_priključka >> 8) & 65535);
}
mašina_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mašina_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mašina_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mašina_Word alatka_grafika_čekaj(void) { return (uint32_t)화면키기다리기(); }
mašina_Word 도구사각형(mašina_Word koordinata_x, mašina_Word Y_koordinata, mašina_Word 너비값, mašina_Word 높이값, mašina_Word 색상) {
    return (uint32_t)사용자호출(13, koordinata_x, Y_koordinata, 색상, 너비값, 높이값, 0);
}

mašina_Word alatka_tok(mašina_Word radnja,mašina_Word fajl_hvatište,mašina_Word VALUE){
    if(radnja==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_adresa(VALUE);
    if(radnja==1){첫째값.adresa=0;intptr_t 반환값=호출(33,fajl_hvatište,(mašina_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fajl_hvatište,4,0));}
    if(radnja==2)return (uint32_t)호출(37,fajl_hvatište,(mašina_Word)&첫째값,sizeof(첫째값));
    if(radnja==3)return (uint32_t)호출(39,fajl_hvatište,0,0);
    if(radnja==4)return alatka_UDP_port(fajl_hvatište);
    if(radnja==5)return (uint32_t)호출(40,fajl_hvatište,0,0);
    return (uint32_t)-22;
}
mašina_Word alatka_GUI(mašina_Word radnja,mašina_Word identifikator_VALUE,mašina_Word 첫째값,mašina_Word SECOND_VALUE,mašina_Word kôd_znaka,mašina_Word odredište_podaci){return (uint32_t)사용자호출(20,radnja,identifikator_VALUE,첫째값,SECOND_VALUE,kôd_znaka,odredište_podaci);}
mašina_Word alatka_GUI_SMS(mašina_Word identifikator_VALUE,mašina_Word niz_VALUE,mašina_Word stavka_COUNT){
    const mašina_Word *원본주소=(const mašina_Word *)niz_VALUE;uint32_t podaci[127];unsigned unos_COUNT=0;
    if(stavka_COUNT>원본주소[0])return (uint32_t)-22;
    for(mašina_Word 순번=0;순번<stavka_COUNT;순번++){unsigned znak_kodiranje=원본주소[순번+1];if(znak_kodiranje>=0xd800&&znak_kodiranje<=0xdbff&&순번+1<stavka_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;znak_kodiranje=0x10000+((znak_kodiranje-0xd800)<<10)+낮은값-0xdc00;}if(unos_COUNT==127)return (uint32_t)-22;podaci[unos_COUNT++]=znak_kodiranje;}
    return (uint32_t)사용자호출(21,identifikator_VALUE,(mašina_Word)podaci,unos_COUNT,0,0,0);
}
