#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Datoteka/Izlaz/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "komplet.h"
typedef uintptr_t stroj_Word;
static int područje_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static stroj_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned artikl_COUNT, stroj_Word 첫째값, stroj_Word SECOND_VALUE, stroj_Word kodna_točka) {
    return 사용자호출(artikl_COUNT, 첫째값, SECOND_VALUE, kodna_točka, 0, 0, 0);
}
static void 바이트들(const char *podaci_položaj, size_t artikl_COUNT) { 호출(1, 1, (stroj_Word)podaci_položaj, artikl_COUNT); }
static void znak(unsigned kodna_točka) {
    unsigned char podaci[4]; unsigned artikl_COUNT = 0;
    if (kodna_točka < 128) podaci[artikl_COUNT++] = kodna_točka;
    else if (kodna_točka < 2048) { podaci[artikl_COUNT++] = 0xc0 | (kodna_točka >> 6); podaci[artikl_COUNT++] = 0x80 | (kodna_točka & 63); }
    else if (kodna_točka < 65536) { podaci[artikl_COUNT++] = 0xe0 | (kodna_točka >> 12); podaci[artikl_COUNT++] = 0x80 | ((kodna_točka >> 6) & 63); podaci[artikl_COUNT++] = 0x80 | (kodna_točka & 63); }
    else { podaci[artikl_COUNT++] = 0xf0 | (kodna_točka >> 18); podaci[artikl_COUNT++] = 0x80 | ((kodna_točka >> 12) & 63); podaci[artikl_COUNT++] = 0x80 | ((kodna_točka >> 6) & 63); podaci[artikl_COUNT++] = 0x80 | (kodna_točka & 63); }
    바이트들((const char *)podaci, artikl_COUNT);
}
stroj_Word alat_znak(stroj_Word VALUE) {
    unsigned kodna_točka = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kodna_točka >= 0xdc00 && kodna_točka <= 0xdfff) { znak(0x10000 + ((높은부분 - 0xd800) << 10) + kodna_točka - 0xdc00); return 1; }
        znak(0xfffd);
    }
    if (kodna_točka >= 0xd800 && kodna_točka <= 0xdbff) 대기중짝글자 = kodna_točka;
    else znak(kodna_točka > 0x10ffff || (kodna_točka >= 0xdc00 && kodna_točka <= 0xdfff) ? 0xfffd : kodna_točka);
    return 1;
}
stroj_Word 도구출력(stroj_Word VALUE) {
    const stroj_Word *niz_podaci = (const stroj_Word *)VALUE;
    for (stroj_Word 순번 = 0; 순번 < niz_podaci[0]; 순번++) alat_znak(niz_podaci[순번 + 1]);
    return niz_podaci[0];
}
static int PUTANJA(stroj_Word objekt_Reference, char KR_podaci[512]) {
    const stroj_Word *첫째값 = (const stroj_Word *)objekt_Reference;
    unsigned 사용량 = 0;
    for (stroj_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kodna_točka = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] postupak_MODE 경로와 호환한다.
        if (kodna_točka >= 0xd800 && kodna_točka <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kodna_točka = 0x10000 + ((kodna_točka - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kodna_točka >= 0xd800 && kodna_točka <= 0xdfff) return -22;
        unsigned artikl_COUNT = kodna_točka < 128 ? 1 : kodna_točka < 2048 ? 2 : kodna_točka < 65536 ? 3 : 4;
        if (사용량 + artikl_COUNT > 511) return -36;
        if (artikl_COUNT == 1) KR_podaci[사용량++] = kodna_točka;
        else {
            KR_podaci[사용량++] = (artikl_COUNT == 2 ? 0xc0 : artikl_COUNT == 3 ? 0xe0 : 0xf0) | (kodna_točka >> (6 * (artikl_COUNT - 1)));
            for (unsigned 안쪽순번 = artikl_COUNT - 1; 안쪽순번; 안쪽순번--) KR_podaci[사용량++] = 0x80 | ((kodna_točka >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_podaci[사용량] = 0; return 사용량 ? 0 : -22;
}
stroj_Word alat_otvoreno(stroj_Word Ime, stroj_Word konfiguracija_Pozadinski_pametni_servis_za_transfer) {
    char podaci_položaj[512]; int GREŠKA = PUTANJA(Ime, podaci_položaj);
    return (uint32_t)(GREŠKA ? GREŠKA : 호출(3, (stroj_Word)podaci_položaj, konfiguracija_Pozadinski_pametni_servis_za_transfer, 0));
}
stroj_Word alat_Zatvori(stroj_Word Datoteka_ustroj) { return (uint32_t)호출(4, Datoteka_ustroj, 0, 0); }
stroj_Word 도구바이트읽기(stroj_Word Datoteka_ustroj) {
    unsigned char SECOND_VALUE; intptr_t artikl_COUNT = 호출(2, Datoteka_ustroj, (stroj_Word)&SECOND_VALUE, 1);
    return (uint32_t)(artikl_COUNT == 1 ? SECOND_VALUE : artikl_COUNT == 0 ? 256 : artikl_COUNT);
}
stroj_Word alat_zapisivanje_bajt(stroj_Word Datoteka_ustroj, stroj_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Datoteka_ustroj, (stroj_Word)&SECOND_VALUE, 1);
}
stroj_Word 도구읽기(stroj_Word Ime, stroj_Word odredište_podaci_adresa) {
    if (꾸러미사용중) {
        char podaci_položaj[512]; int GREŠKA = PUTANJA(Ime, podaci_položaj); if (GREŠKA) return (uint32_t)GREŠKA;
        unsigned artikl_COUNT = 0; while (podaci_položaj[artikl_COUNT]) artikl_COUNT++;
        if (artikl_COUNT >= 6) for (unsigned 순번 = 0; 순번 < artikl_COUNT - 6; 순번++) if (podaci_položaj[순번] == '.') podaci_položaj[순번] = '/';
        unsigned char 바이트들[16384]; stroj_Word *odredište_VALUE_položaj = (stroj_Word *)odredište_podaci_adresa;
        int RECEIVED_COUNT = 꾸러미읽기(podaci_položaj, 바이트들, odredište_VALUE_položaj[0] < sizeof(바이트들) ? odredište_VALUE_položaj[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) odredište_VALUE_položaj[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Datoteka_ustroj = 꾸러미사용중 ? -2 : (int32_t)alat_otvoreno(Ime, 0);
    if (Datoteka_ustroj < 0) {
        char podaci_položaj[512]; int GREŠKA = PUTANJA(Ime, podaci_položaj); if (GREŠKA) return (uint32_t)GREŠKA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Dalje_pomak = 자바클래스들[순번].Ime; unsigned 안쪽순번 = 0;
            while (podaci_položaj[안쪽순번] && podaci_položaj[안쪽순번] == Dalje_pomak[안쪽순번]) 안쪽순번++;
            if (podaci_položaj[안쪽순번] || Dalje_pomak[안쪽순번]) continue;
            stroj_Word *odredište_VALUE_položaj = (stroj_Word *)odredište_podaci_adresa;
            if (odredište_VALUE_položaj[0] < 자바클래스들[순번].Veličina) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Veličina; 안쪽순번++) odredište_VALUE_položaj[안쪽순번 + 1] = 자바클래스들[순번].podaci[안쪽순번];
            return 자바클래스들[순번].Veličina;
        }
        return (uint32_t)Datoteka_ustroj;
    }
    stroj_Word *첫째값 = (stroj_Word *)odredište_podaci_adresa;
    intptr_t Veličina = 호출(9, Datoteka_ustroj, 0, 0), Dovršeno_iznos = 0;
    if (Veličina < 0 || (stroj_Word)Veličina > 첫째값[0]) { alat_Zatvori(Datoteka_ustroj); return (uint32_t)(Veličina < 0 ? Veličina : -27); }
    unsigned char podatkovni_blok[256];
    while (Dovršeno_iznos < Veličina) {
        intptr_t artikl_COUNT = 호출(2, Datoteka_ustroj, (stroj_Word)podatkovni_blok, Veličina - Dovršeno_iznos < 256 ? Veličina - Dovršeno_iznos : 256);
        if (artikl_COUNT <= 0) { alat_Zatvori(Datoteka_ustroj); return (uint32_t)(artikl_COUNT ? artikl_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < artikl_COUNT; 순번++) 첫째값[1 + Dovršeno_iznos + 순번] = podatkovni_blok[순번];
        Dovršeno_iznos += artikl_COUNT;
    }
    alat_Zatvori(Datoteka_ustroj); return Dovršeno_iznos;
}
stroj_Word alat_zapisivanje(stroj_Word Ime, stroj_Word 원본자료, stroj_Word unos_COUNT) {
    const stroj_Word *첫째값 = (const stroj_Word *)원본자료;
    if (unos_COUNT > 첫째값[0] || unos_COUNT > 16384) return (uint32_t)-27;
    int Datoteka_ustroj = (int32_t)alat_otvoreno(Ime, 577); if (Datoteka_ustroj < 0) return (uint32_t)Datoteka_ustroj;
    unsigned char podatkovni_blok[256]; stroj_Word Dovršeno_iznos = 0;
    while (Dovršeno_iznos < unos_COUNT) {
        stroj_Word artikl_COUNT = unos_COUNT - Dovršeno_iznos < 256 ? unos_COUNT - Dovršeno_iznos : 256;
        for (stroj_Word 순번 = 0; 순번 < artikl_COUNT; 순번++) podatkovni_blok[순번] = 첫째값[1 + Dovršeno_iznos + 순번];
        intptr_t REZULTAT = 호출(1, Datoteka_ustroj, (stroj_Word)podatkovni_blok, artikl_COUNT);
        if (REZULTAT <= 0) { alat_Zatvori(Datoteka_ustroj); return (uint32_t)(REZULTAT ? REZULTAT : -5); }
        Dovršeno_iznos += REZULTAT;
    }
    alat_Zatvori(Datoteka_ustroj); return unos_COUNT;
}
stroj_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
stroj_Word alat_argument(stroj_Word LOOKUP_INDEX) {
    static const stroj_Word 빈값[1] = {0};
    if (LOOKUP_INDEX >= 8) return (stroj_Word)빈값;
    unsigned char 입력결과[256]; intptr_t artikl_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *podaci_položaj = 꾸러미진입클래스(); artikl_COUNT = 0; while (podaci_položaj[artikl_COUNT] && artikl_COUNT < 255) { 입력결과[artikl_COUNT] = podaci_položaj[artikl_COUNT]; artikl_COUNT++; } }
    else artikl_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (stroj_Word)입력결과, sizeof(입력결과));
    if (artikl_COUNT < 0) return (stroj_Word)빈값;
    stroj_Word *KR_podaci = 전달인수[LOOKUP_INDEX]; unsigned unos_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < artikl_COUNT;) {
        unsigned kodna_točka = 입력결과[순번++], 더있음 = kodna_točka < 128 ? 0 : kodna_točka >= 0xc2 && kodna_točka < 0xe0 ? 1 : kodna_točka < 0xf0 && kodna_točka >= 0xe0 ? 2 : kodna_točka >= 0xf0 && kodna_točka <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > artikl_COUNT) { KR_podaci[++unos_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kodna_točka &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kodna_točka = (kodna_točka << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kodna_točka < 최소값 || kodna_točka > 0x10ffff || (kodna_točka >= 0xd800 && kodna_točka <= 0xdfff)) kodna_točka = 0xfffd;
        if (kodna_točka >= 65536) { kodna_točka -= 65536; KR_podaci[++unos_COUNT] = 0xd800 | (kodna_točka >> 10); KR_podaci[++unos_COUNT] = 0xdc00 | (kodna_točka & 1023); }
        else KR_podaci[++unos_COUNT] = kodna_točka;
    }
    KR_podaci[0] = unos_COUNT; return (stroj_Word)KR_podaci;
}
stroj_Word 도구분류(void) { return područje_VALUE; }
void 커널중단(const char *obavijest_SMS) {
    const char *podaci_položaj = obavijest_SMS; while (*podaci_položaj) podaci_položaj++;
    바이트들("Java tool runtime error: ", 25); 바이트들(obavijest_SMS, podaci_položaj - obavijest_SMS); znak(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_korisnik_program(int postupak_MODE) {
    područje_VALUE = postupak_MODE;
    unsigned char 첫항목[256]; intptr_t artikl_COUNT = 호출(15, 0, (stroj_Word)첫항목, sizeof(첫항목));
    if (postupak_MODE == 2 || (postupak_MODE == 1 && artikl_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = postupak_MODE == 2 ? 0 : 1;
        char Datoteka_unos_naziv[256]; intptr_t 길이값 = 호출(15, 꾸러미인수이동, (stroj_Word)Datoteka_unos_naziv, sizeof(Datoteka_unos_naziv));
        if (길이값 <= 0 || 꾸러미열기(Datoteka_unos_naziv) < 0) {
            static const char GREŠKA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(GREŠKA, sizeof(GREŠKA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int REZULTAT = 자바진입();
    if (대기중짝글자) znak(0xfffd);
    return REZULTAT;
}

// UDP는 vlastiti 커널의 SVC를 통과하며 redovno_artikl 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t linija, broj_priključka; uint32_t adresa; unsigned char nula_VALUE[8]; };
static struct 자바주소 UDP_adresa(unsigned broj_priključka) {
    struct 자바주소 첫째값 = {2, (uint16_t)((broj_priključka << 8) | (broj_priključka >> 8)), 0x0100007f, {0}}; return 첫째값;
}
stroj_Word alat_UDP_otvoreno(stroj_Word broj_priključka) {
    intptr_t Datoteka_ustroj = 호출(32, 2, 2, 17); if (Datoteka_ustroj < 0) return (uint32_t)Datoteka_ustroj;
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka);
    첫째값.adresa = 0;
    intptr_t Stanje_VALUE = 호출(33, Datoteka_ustroj, (stroj_Word)&첫째값, sizeof(첫째값));
    if (Stanje_VALUE < 0) { alat_Zatvori(Datoteka_ustroj); return (uint32_t)Stanje_VALUE; }
    return Datoteka_ustroj;
}
stroj_Word alat_UDP_slati(stroj_Word Datoteka_ustroj, stroj_Word broj_priključka, stroj_Word ARRAY_VALUE, stroj_Word 길이) {
    const stroj_Word *원본주소 = (const stroj_Word *)ARRAY_VALUE; unsigned char podaci[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (stroj_Word 순번 = 0; 순번 < 길이; 순번++) podaci[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka);
    return (uint32_t)사용자호출(34, Datoteka_ustroj, (stroj_Word)podaci, 길이, 0, (stroj_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t artikl_COUNT) { return (artikl_COUNT>>24)|((artikl_COUNT>>8)&0xff00)|((artikl_COUNT<<8)&0xff0000)|(artikl_COUNT<<24); }
stroj_Word alat_UDP_slati_adresa(stroj_Word Datoteka_ustroj, stroj_Word adresa, stroj_Word broj_priključka, stroj_Word ARRAY_VALUE, stroj_Word 길이) {
    const stroj_Word *원본주소 = (const stroj_Word *)ARRAY_VALUE; unsigned char podaci[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (stroj_Word 순번 = 0; 순번 < 길이; 순번++) podaci[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka); 첫째값.adresa = 바이트순서뒤집기(adresa);
    return (uint32_t)사용자호출(34, Datoteka_ustroj, (stroj_Word)podaci, 길이, 0, (stroj_Word)&첫째값, sizeof(첫째값));
}
stroj_Word alat_CONNECT(stroj_Word Datoteka_ustroj, stroj_Word adresa, stroj_Word broj_priključka) {
    struct 자바주소 첫째값 = UDP_adresa(broj_priključka); 첫째값.adresa = 바이트순서뒤집기(adresa);
    uint32_t Pokreni = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t REZULTAT = 호출(37, Datoteka_ustroj, (stroj_Word)&첫째값, sizeof(첫째값));
        if (REZULTAT != -115) return (uint32_t)REZULTAT;
        if ((uint32_t)(호출(7, 0, 0, 0) - Pokreni) >= 1000) return (uint32_t)-110;
    }
}
stroj_Word 도구전문받기(stroj_Word Datoteka_ustroj, stroj_Word ARRAY_VALUE, stroj_Word međuspremnik_kapacitet) {
    stroj_Word *odredište_adresa = (stroj_Word *)ARRAY_VALUE; unsigned char podaci[512];
    if (međuspremnik_kapacitet > 512 || odredište_adresa[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t artikl_COUNT = 사용자호출(35, Datoteka_ustroj, (stroj_Word)podaci, međuspremnik_kapacitet, 0, (stroj_Word)&첫째값, (stroj_Word)&길이값);
    if (artikl_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < artikl_COUNT; 순번++) odredište_adresa[순번 + 1] = podaci[순번]; odredište_adresa[513] = (첫째값.broj_priključka << 8 | 첫째값.broj_priključka >> 8) & 65535; odredište_adresa[514] = 바이트순서뒤집기(첫째값.adresa); }
    return (uint32_t)artikl_COUNT;
}
stroj_Word alat_UDP_prebaciti(stroj_Word Datoteka_ustroj) {
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Datoteka_ustroj, (stroj_Word)&첫째값, (stroj_Word)&길이값);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.broj_priključka << 8 | 첫째값.broj_priključka >> 8) & 65535);
}
stroj_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
stroj_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
stroj_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
stroj_Word alat_grafika_čekaj(void) { return (uint32_t)화면키기다리기(); }
stroj_Word alat_pravokutnik(stroj_Word koordinata_x, stroj_Word 세로좌표, stroj_Word 너비값, stroj_Word 높이값, stroj_Word 색상) {
    return (uint32_t)사용자호출(13, koordinata_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

stroj_Word alat_tok(stroj_Word Aktivnost,stroj_Word Datoteka_ustroj,stroj_Word VALUE){
    if(Aktivnost==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_adresa(VALUE);
    if(Aktivnost==1){첫째값.adresa=0;intptr_t 반환값=호출(33,Datoteka_ustroj,(stroj_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Datoteka_ustroj,4,0));}
    if(Aktivnost==2)return (uint32_t)호출(37,Datoteka_ustroj,(stroj_Word)&첫째값,sizeof(첫째값));
    if(Aktivnost==3)return (uint32_t)호출(39,Datoteka_ustroj,0,0);
    if(Aktivnost==4)return alat_UDP_prebaciti(Datoteka_ustroj);
    if(Aktivnost==5)return (uint32_t)호출(40,Datoteka_ustroj,0,0);
    return (uint32_t)-22;
}
stroj_Word alat_GUI(stroj_Word Aktivnost,stroj_Word identifikator_VALUE,stroj_Word 첫째값,stroj_Word SECOND_VALUE,stroj_Word kodna_točka,stroj_Word odredište_podaci){return (uint32_t)사용자호출(20,Aktivnost,identifikator_VALUE,첫째값,SECOND_VALUE,kodna_točka,odredište_podaci);}
stroj_Word alat_GUI_SMS(stroj_Word identifikator_VALUE,stroj_Word ARRAY_VALUE,stroj_Word artikl_COUNT){
    const stroj_Word *원본주소=(const stroj_Word *)ARRAY_VALUE;uint32_t podaci[127];unsigned unos_COUNT=0;
    if(artikl_COUNT>원본주소[0])return (uint32_t)-22;
    for(stroj_Word 순번=0;순번<artikl_COUNT;순번++){unsigned kodiranje_znakova=원본주소[순번+1];if(kodiranje_znakova>=0xd800&&kodiranje_znakova<=0xdbff&&순번+1<artikl_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;kodiranje_znakova=0x10000+((kodiranje_znakova-0xd800)<<10)+낮은값-0xdc00;}if(unos_COUNT==127)return (uint32_t)-22;podaci[unos_COUNT++]=kodiranje_znakova;}
    return (uint32_t)사용자호출(21,identifikator_VALUE,(stroj_Word)podaci,unos_COUNT,0,0,0);
}
