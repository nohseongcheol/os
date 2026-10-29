#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Datoteka/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "komplet.h"
typedef uintptr_t računar_Word;
static int oblast_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static računar_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned stavka_COUNT, računar_Word 첫째값, računar_Word SECOND_VALUE, računar_Word kôd_znaka) {
    return 사용자호출(stavka_COUNT, 첫째값, SECOND_VALUE, kôd_znaka, 0, 0, 0);
}
static void 바이트들(const char *podaci_pozicija, size_t stavka_COUNT) { 호출(1, 1, (računar_Word)podaci_pozicija, stavka_COUNT); }
static void znak(unsigned kôd_znaka) {
    unsigned char podaci[4]; unsigned stavka_COUNT = 0;
    if (kôd_znaka < 128) podaci[stavka_COUNT++] = kôd_znaka;
    else if (kôd_znaka < 2048) { podaci[stavka_COUNT++] = 0xc0 | (kôd_znaka >> 6); podaci[stavka_COUNT++] = 0x80 | (kôd_znaka & 63); }
    else if (kôd_znaka < 65536) { podaci[stavka_COUNT++] = 0xe0 | (kôd_znaka >> 12); podaci[stavka_COUNT++] = 0x80 | ((kôd_znaka >> 6) & 63); podaci[stavka_COUNT++] = 0x80 | (kôd_znaka & 63); }
    else { podaci[stavka_COUNT++] = 0xf0 | (kôd_znaka >> 18); podaci[stavka_COUNT++] = 0x80 | ((kôd_znaka >> 12) & 63); podaci[stavka_COUNT++] = 0x80 | ((kôd_znaka >> 6) & 63); podaci[stavka_COUNT++] = 0x80 | (kôd_znaka & 63); }
    바이트들((const char *)podaci, stavka_COUNT);
}
računar_Word alatka_znak(računar_Word VALUE) {
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
računar_Word 도구출력(računar_Word VALUE) {
    const računar_Word *niska_podaci = (const računar_Word *)VALUE;
    for (računar_Word 순번 = 0; 순번 < niska_podaci[0]; 순번++) alatka_znak(niska_podaci[순번 + 1]);
    return niska_podaci[0];
}
static int putanja(računar_Word objekat_referenca, char KR_podaci[512]) {
    const računar_Word *첫째값 = (const računar_Word *)objekat_referenca;
    unsigned 사용량 = 0;
    for (računar_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kôd_znaka = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metod_MODE 경로와 호환한다.
        if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) return -22;
        unsigned stavka_COUNT = kôd_znaka < 128 ? 1 : kôd_znaka < 2048 ? 2 : kôd_znaka < 65536 ? 3 : 4;
        if (사용량 + stavka_COUNT > 511) return -36;
        if (stavka_COUNT == 1) KR_podaci[사용량++] = kôd_znaka;
        else {
            KR_podaci[사용량++] = (stavka_COUNT == 2 ? 0xc0 : stavka_COUNT == 3 ? 0xe0 : 0xf0) | (kôd_znaka >> (6 * (stavka_COUNT - 1)));
            for (unsigned 안쪽순번 = stavka_COUNT - 1; 안쪽순번; 안쪽순번--) KR_podaci[사용량++] = 0x80 | ((kôd_znaka >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_podaci[사용량] = 0; return 사용량 ? 0 : -22;
}
računar_Word alatka_otvoren(računar_Word ime, računar_Word konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini) {
    char podaci_pozicija[512]; int greška = putanja(ime, podaci_pozicija);
    return (uint32_t)(greška ? greška : 호출(3, (računar_Word)podaci_pozicija, konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini, 0));
}
računar_Word alatka_Zatvori(računar_Word Datoteka_pokazivač) { return (uint32_t)호출(4, Datoteka_pokazivač, 0, 0); }
računar_Word 도구바이트읽기(računar_Word Datoteka_pokazivač) {
    unsigned char SECOND_VALUE; intptr_t stavka_COUNT = 호출(2, Datoteka_pokazivač, (računar_Word)&SECOND_VALUE, 1);
    return (uint32_t)(stavka_COUNT == 1 ? SECOND_VALUE : stavka_COUNT == 0 ? 256 : stavka_COUNT);
}
računar_Word 도구바이트쓰기(računar_Word Datoteka_pokazivač, računar_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Datoteka_pokazivač, (računar_Word)&SECOND_VALUE, 1);
}
računar_Word 도구읽기(računar_Word ime, računar_Word odredište_podaci_adresa) {
    if (꾸러미사용중) {
        char podaci_pozicija[512]; int greška = putanja(ime, podaci_pozicija); if (greška) return (uint32_t)greška;
        unsigned stavka_COUNT = 0; while (podaci_pozicija[stavka_COUNT]) stavka_COUNT++;
        if (stavka_COUNT >= 6) for (unsigned 순번 = 0; 순번 < stavka_COUNT - 6; 순번++) if (podaci_pozicija[순번] == '.') podaci_pozicija[순번] = '/';
        unsigned char 바이트들[16384]; računar_Word *odredište_VALUE_pozicija = (računar_Word *)odredište_podaci_adresa;
        int RECEIVED_COUNT = 꾸러미읽기(podaci_pozicija, 바이트들, odredište_VALUE_pozicija[0] < sizeof(바이트들) ? odredište_VALUE_pozicija[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) odredište_VALUE_pozicija[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Datoteka_pokazivač = 꾸러미사용중 ? -2 : (int32_t)alatka_otvoren(ime, 0);
    if (Datoteka_pokazivač < 0) {
        char podaci_pozicija[512]; int greška = putanja(ime, podaci_pozicija); if (greška) return (uint32_t)greška;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Dalje_Pomak = 자바클래스들[순번].ime; unsigned 안쪽순번 = 0;
            while (podaci_pozicija[안쪽순번] && podaci_pozicija[안쪽순번] == Dalje_Pomak[안쪽순번]) 안쪽순번++;
            if (podaci_pozicija[안쪽순번] || Dalje_Pomak[안쪽순번]) continue;
            računar_Word *odredište_VALUE_pozicija = (računar_Word *)odredište_podaci_adresa;
            if (odredište_VALUE_pozicija[0] < 자바클래스들[순번].promeniti_veličinu) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].promeniti_veličinu; 안쪽순번++) odredište_VALUE_pozicija[안쪽순번 + 1] = 자바클래스들[순번].podaci[안쪽순번];
            return 자바클래스들[순번].promeniti_veličinu;
        }
        return (uint32_t)Datoteka_pokazivač;
    }
    računar_Word *첫째값 = (računar_Word *)odredište_podaci_adresa;
    intptr_t promeniti_veličinu = 호출(9, Datoteka_pokazivač, 0, 0), Dovršeno_iznos = 0;
    if (promeniti_veličinu < 0 || (računar_Word)promeniti_veličinu > 첫째값[0]) { alatka_Zatvori(Datoteka_pokazivač); return (uint32_t)(promeniti_veličinu < 0 ? promeniti_veličinu : -27); }
    unsigned char blok_podataka[256];
    while (Dovršeno_iznos < promeniti_veličinu) {
        intptr_t stavka_COUNT = 호출(2, Datoteka_pokazivač, (računar_Word)blok_podataka, promeniti_veličinu - Dovršeno_iznos < 256 ? promeniti_veličinu - Dovršeno_iznos : 256);
        if (stavka_COUNT <= 0) { alatka_Zatvori(Datoteka_pokazivač); return (uint32_t)(stavka_COUNT ? stavka_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < stavka_COUNT; 순번++) 첫째값[1 + Dovršeno_iznos + 순번] = blok_podataka[순번];
        Dovršeno_iznos += stavka_COUNT;
    }
    alatka_Zatvori(Datoteka_pokazivač); return Dovršeno_iznos;
}
računar_Word 도구쓰기(računar_Word ime, računar_Word 원본자료, računar_Word stavka_COUNT_8f7753a1) {
    const računar_Word *첫째값 = (const računar_Word *)원본자료;
    if (stavka_COUNT_8f7753a1 > 첫째값[0] || stavka_COUNT_8f7753a1 > 16384) return (uint32_t)-27;
    int Datoteka_pokazivač = (int32_t)alatka_otvoren(ime, 577); if (Datoteka_pokazivač < 0) return (uint32_t)Datoteka_pokazivač;
    unsigned char blok_podataka[256]; računar_Word Dovršeno_iznos = 0;
    while (Dovršeno_iznos < stavka_COUNT_8f7753a1) {
        računar_Word stavka_COUNT = stavka_COUNT_8f7753a1 - Dovršeno_iznos < 256 ? stavka_COUNT_8f7753a1 - Dovršeno_iznos : 256;
        for (računar_Word 순번 = 0; 순번 < stavka_COUNT; 순번++) blok_podataka[순번] = 첫째값[1 + Dovršeno_iznos + 순번];
        intptr_t KR = 호출(1, Datoteka_pokazivač, (računar_Word)blok_podataka, stavka_COUNT);
        if (KR <= 0) { alatka_Zatvori(Datoteka_pokazivač); return (uint32_t)(KR ? KR : -5); }
        Dovršeno_iznos += KR;
    }
    alatka_Zatvori(Datoteka_pokazivač); return stavka_COUNT_8f7753a1;
}
računar_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
računar_Word alatka_argument(računar_Word LOOKUP_INDEX) {
    static const računar_Word 빈값[1] = {0};
    if (LOOKUP_INDEX >= 8) return (računar_Word)빈값;
    unsigned char 입력결과[256]; intptr_t stavka_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *podaci_pozicija = 꾸러미진입클래스(); stavka_COUNT = 0; while (podaci_pozicija[stavka_COUNT] && stavka_COUNT < 255) { 입력결과[stavka_COUNT] = podaci_pozicija[stavka_COUNT]; stavka_COUNT++; } }
    else stavka_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (računar_Word)입력결과, sizeof(입력결과));
    if (stavka_COUNT < 0) return (računar_Word)빈값;
    računar_Word *KR_podaci = 전달인수[LOOKUP_INDEX]; unsigned stavka_COUNT_8f7753a1 = 0;
    for (intptr_t 순번 = 0; 순번 < stavka_COUNT;) {
        unsigned kôd_znaka = 입력결과[순번++], 더있음 = kôd_znaka < 128 ? 0 : kôd_znaka >= 0xc2 && kôd_znaka < 0xe0 ? 1 : kôd_znaka < 0xf0 && kôd_znaka >= 0xe0 ? 2 : kôd_znaka >= 0xf0 && kôd_znaka <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > stavka_COUNT) { KR_podaci[++stavka_COUNT_8f7753a1] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kôd_znaka &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kôd_znaka = (kôd_znaka << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kôd_znaka < 최소값 || kôd_znaka > 0x10ffff || (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff)) kôd_znaka = 0xfffd;
        if (kôd_znaka >= 65536) { kôd_znaka -= 65536; KR_podaci[++stavka_COUNT_8f7753a1] = 0xd800 | (kôd_znaka >> 10); KR_podaci[++stavka_COUNT_8f7753a1] = 0xdc00 | (kôd_znaka & 1023); }
        else KR_podaci[++stavka_COUNT_8f7753a1] = kôd_znaka;
    }
    KR_podaci[0] = stavka_COUNT_8f7753a1; return (računar_Word)KR_podaci;
}
računar_Word 도구분류(void) { return oblast_VALUE; }
void 커널중단(const char *obaveštavanje_SMS) {
    const char *podaci_pozicija = obaveštavanje_SMS; while (*podaci_pozicija) podaci_pozicija++;
    바이트들("Java tool runtime error: ", 25); 바이트들(obaveštavanje_SMS, podaci_pozicija - obaveštavanje_SMS); znak(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_korisnik_program(int metod_MODE) {
    oblast_VALUE = metod_MODE;
    unsigned char 첫항목[256]; intptr_t stavka_COUNT = 호출(15, 0, (računar_Word)첫항목, sizeof(첫항목));
    if (metod_MODE == 2 || (metod_MODE == 1 && stavka_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metod_MODE == 2 ? 0 : 1;
        char Datoteka_stavka_ime[256]; intptr_t 길이값 = 호출(15, 꾸러미인수이동, (računar_Word)Datoteka_stavka_ime, sizeof(Datoteka_stavka_ime));
        if (길이값 <= 0 || 꾸러미열기(Datoteka_stavka_ime) < 0) {
            static const char greška[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(greška, sizeof(greška) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int KR = 자바진입();
    if (대기중짝글자) znak(0xfffd);
    return KR;
}

// UDP는 자체 커널의 SVC를 통과하며 aktuelno_stavka 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Porodica, broj_porta; uint32_t adresa; unsigned char nula_VALUE[8]; };
static struct 자바주소 UDP_adresa(unsigned broj_porta) {
    struct 자바주소 첫째값 = {2, (uint16_t)((broj_porta << 8) | (broj_porta >> 8)), 0x0100007f, {0}}; return 첫째값;
}
računar_Word alatka_UDP_otvoren(računar_Word broj_porta) {
    intptr_t Datoteka_pokazivač = 호출(32, 2, 2, 17); if (Datoteka_pokazivač < 0) return (uint32_t)Datoteka_pokazivač;
    struct 자바주소 첫째값 = UDP_adresa(broj_porta);
    첫째값.adresa = 0;
    intptr_t Status_VALUE = 호출(33, Datoteka_pokazivač, (računar_Word)&첫째값, sizeof(첫째값));
    if (Status_VALUE < 0) { alatka_Zatvori(Datoteka_pokazivač); return (uint32_t)Status_VALUE; }
    return Datoteka_pokazivač;
}
računar_Word alatka_UDP_poslati(računar_Word Datoteka_pokazivač, računar_Word broj_porta, računar_Word niz_VALUE, računar_Word 길이) {
    const računar_Word *원본주소 = (const računar_Word *)niz_VALUE; unsigned char podaci[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (računar_Word 순번 = 0; 순번 < 길이; 순번++) podaci[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(broj_porta);
    return (uint32_t)사용자호출(34, Datoteka_pokazivač, (računar_Word)podaci, 길이, 0, (računar_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t stavka_COUNT) { return (stavka_COUNT>>24)|((stavka_COUNT>>8)&0xff00)|((stavka_COUNT<<8)&0xff0000)|(stavka_COUNT<<24); }
računar_Word alatka_UDP_poslati_adresa(računar_Word Datoteka_pokazivač, računar_Word adresa, računar_Word broj_porta, računar_Word niz_VALUE, računar_Word 길이) {
    const računar_Word *원본주소 = (const računar_Word *)niz_VALUE; unsigned char podaci[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (računar_Word 순번 = 0; 순번 < 길이; 순번++) podaci[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(broj_porta); 첫째값.adresa = 바이트순서뒤집기(adresa);
    return (uint32_t)사용자호출(34, Datoteka_pokazivač, (računar_Word)podaci, 길이, 0, (računar_Word)&첫째값, sizeof(첫째값));
}
računar_Word alatka_veze(računar_Word Datoteka_pokazivač, računar_Word adresa, računar_Word broj_porta) {
    struct 자바주소 첫째값 = UDP_adresa(broj_porta); 첫째값.adresa = 바이트순서뒤집기(adresa);
    uint32_t koristiti = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t KR = 호출(37, Datoteka_pokazivač, (računar_Word)&첫째값, sizeof(첫째값));
        if (KR != -115) return (uint32_t)KR;
        if ((uint32_t)(호출(7, 0, 0, 0) - koristiti) >= 1000) return (uint32_t)-110;
    }
}
računar_Word 도구전문받기(računar_Word Datoteka_pokazivač, računar_Word niz_VALUE, računar_Word bafer_kapacitet) {
    računar_Word *odredište_adresa = (računar_Word *)niz_VALUE; unsigned char podaci[512];
    if (bafer_kapacitet > 512 || odredište_adresa[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t stavka_COUNT = 사용자호출(35, Datoteka_pokazivač, (računar_Word)podaci, bafer_kapacitet, 0, (računar_Word)&첫째값, (računar_Word)&길이값);
    if (stavka_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < stavka_COUNT; 순번++) odredište_adresa[순번 + 1] = podaci[순번]; odredište_adresa[513] = (첫째값.broj_porta << 8 | 첫째값.broj_porta >> 8) & 65535; odredište_adresa[514] = 바이트순서뒤집기(첫째값.adresa); }
    return (uint32_t)stavka_COUNT;
}
računar_Word alatka_UDP_port(računar_Word Datoteka_pokazivač) {
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Datoteka_pokazivač, (računar_Word)&첫째값, (računar_Word)&길이값);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.broj_porta << 8 | 첫째값.broj_porta >> 8) & 65535);
}
računar_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
računar_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
računar_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
računar_Word alatka_grafika_čekaj(void) { return (uint32_t)화면키기다리기(); }
računar_Word 도구사각형(računar_Word x_koordinata, računar_Word 세로좌표, računar_Word 너비값, računar_Word 높이값, računar_Word 색상) {
    return (uint32_t)사용자호출(13, x_koordinata, 세로좌표, 색상, 너비값, 높이값, 0);
}

računar_Word alatka_tok(računar_Word radnja,računar_Word Datoteka_pokazivač,računar_Word VALUE){
    if(radnja==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_adresa(VALUE);
    if(radnja==1){첫째값.adresa=0;intptr_t 반환값=호출(33,Datoteka_pokazivač,(računar_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Datoteka_pokazivač,4,0));}
    if(radnja==2)return (uint32_t)호출(37,Datoteka_pokazivač,(računar_Word)&첫째값,sizeof(첫째값));
    if(radnja==3)return (uint32_t)호출(39,Datoteka_pokazivač,0,0);
    if(radnja==4)return alatka_UDP_port(Datoteka_pokazivač);
    if(radnja==5)return (uint32_t)호출(40,Datoteka_pokazivač,0,0);
    return (uint32_t)-22;
}
računar_Word alatka_GUI(računar_Word radnja,računar_Word identifikator_VALUE,računar_Word 첫째값,računar_Word SECOND_VALUE,računar_Word kôd_znaka,računar_Word odredište_podaci){return (uint32_t)사용자호출(20,radnja,identifikator_VALUE,첫째값,SECOND_VALUE,kôd_znaka,odredište_podaci);}
računar_Word alatka_GUI_SMS(računar_Word identifikator_VALUE,računar_Word niz_VALUE,računar_Word stavka_COUNT){
    const računar_Word *원본주소=(const računar_Word *)niz_VALUE;uint32_t podaci[127];unsigned stavka_COUNT_8f7753a1=0;
    if(stavka_COUNT>원본주소[0])return (uint32_t)-22;
    for(računar_Word 순번=0;순번<stavka_COUNT;순번++){unsigned kodiranje_znakova=원본주소[순번+1];if(kodiranje_znakova>=0xd800&&kodiranje_znakova<=0xdbff&&순번+1<stavka_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;kodiranje_znakova=0x10000+((kodiranje_znakova-0xd800)<<10)+낮은값-0xdc00;}if(stavka_COUNT_8f7753a1==127)return (uint32_t)-22;podaci[stavka_COUNT_8f7753a1++]=kodiranje_znakova;}
    return (uint32_t)사용자호출(21,identifikator_VALUE,(računar_Word)podaci,stavka_COUNT_8f7753a1,0,0,0);
}
