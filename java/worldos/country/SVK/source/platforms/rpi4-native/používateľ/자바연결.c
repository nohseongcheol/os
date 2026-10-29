#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Súbor/Výstup/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "zväzok.h"
typedef uintptr_t počítač_Word;
static int oblasť_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static počítač_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned položka_COUNT, počítač_Word 첫째값, počítač_Word SECOND_VALUE, počítač_Word bod_kódu) {
    return 사용자호출(položka_COUNT, 첫째값, SECOND_VALUE, bod_kódu, 0, 0, 0);
}
static void 바이트들(const char *údaje_pozícia, size_t položka_COUNT) { 호출(1, 1, (počítač_Word)údaje_pozícia, položka_COUNT); }
static void znak(unsigned bod_kódu) {
    unsigned char údaje[4]; unsigned položka_COUNT = 0;
    if (bod_kódu < 128) údaje[položka_COUNT++] = bod_kódu;
    else if (bod_kódu < 2048) { údaje[položka_COUNT++] = 0xc0 | (bod_kódu >> 6); údaje[položka_COUNT++] = 0x80 | (bod_kódu & 63); }
    else if (bod_kódu < 65536) { údaje[položka_COUNT++] = 0xe0 | (bod_kódu >> 12); údaje[položka_COUNT++] = 0x80 | ((bod_kódu >> 6) & 63); údaje[položka_COUNT++] = 0x80 | (bod_kódu & 63); }
    else { údaje[položka_COUNT++] = 0xf0 | (bod_kódu >> 18); údaje[položka_COUNT++] = 0x80 | ((bod_kódu >> 12) & 63); údaje[položka_COUNT++] = 0x80 | ((bod_kódu >> 6) & 63); údaje[položka_COUNT++] = 0x80 | (bod_kódu & 63); }
    바이트들((const char *)údaje, položka_COUNT);
}
počítač_Word nástroj_znak(počítač_Word VALUE) {
    unsigned bod_kódu = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (bod_kódu >= 0xdc00 && bod_kódu <= 0xdfff) { znak(0x10000 + ((높은부분 - 0xd800) << 10) + bod_kódu - 0xdc00); return 1; }
        znak(0xfffd);
    }
    if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff) 대기중짝글자 = bod_kódu;
    else znak(bod_kódu > 0x10ffff || (bod_kódu >= 0xdc00 && bod_kódu <= 0xdfff) ? 0xfffd : bod_kódu);
    return 1;
}
počítač_Word 도구출력(počítač_Word VALUE) {
    const počítač_Word *reťazec_údaje = (const počítač_Word *)VALUE;
    for (počítač_Word 순번 = 0; 순번 < reťazec_údaje[0]; 순번++) nástroj_znak(reťazec_údaje[순번 + 1]);
    return reťazec_údaje[0];
}
static int Cesta(počítač_Word objekt_zdroj, char KR_údaje[512]) {
    const počítač_Word *첫째값 = (const počítač_Word *)objekt_zdroj;
    unsigned 사용량 = 0;
    for (počítač_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned bod_kódu = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metóda_MODE 경로와 호환한다.
        if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) return -22;
        unsigned položka_COUNT = bod_kódu < 128 ? 1 : bod_kódu < 2048 ? 2 : bod_kódu < 65536 ? 3 : 4;
        if (사용량 + položka_COUNT > 511) return -36;
        if (položka_COUNT == 1) KR_údaje[사용량++] = bod_kódu;
        else {
            KR_údaje[사용량++] = (položka_COUNT == 2 ? 0xc0 : položka_COUNT == 3 ? 0xe0 : 0xf0) | (bod_kódu >> (6 * (položka_COUNT - 1)));
            for (unsigned 안쪽순번 = položka_COUNT - 1; 안쪽순번; 안쪽순번--) KR_údaje[사용량++] = 0x80 | ((bod_kódu >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_údaje[사용량] = 0; return 사용량 ? 0 : -22;
}
počítač_Word nástroj_otvoriť(počítač_Word Názov, počítač_Word konfigurácia_Background_Intelligent_Transfer_Service) {
    char údaje_pozícia[512]; int chyba = Cesta(Názov, údaje_pozícia);
    return (uint32_t)(chyba ? chyba : 호출(3, (počítač_Word)údaje_pozícia, konfigurácia_Background_Intelligent_Transfer_Service, 0));
}
počítač_Word nástroj_Zavrieť(počítač_Word Súbor_rukoväť) { return (uint32_t)호출(4, Súbor_rukoväť, 0, 0); }
počítač_Word 도구바이트읽기(počítač_Word Súbor_rukoväť) {
    unsigned char SECOND_VALUE; intptr_t položka_COUNT = 호출(2, Súbor_rukoväť, (počítač_Word)&SECOND_VALUE, 1);
    return (uint32_t)(položka_COUNT == 1 ? SECOND_VALUE : položka_COUNT == 0 ? 256 : položka_COUNT);
}
počítač_Word nástroj_zapísať_Byte(počítač_Word Súbor_rukoväť, počítač_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Súbor_rukoväť, (počítač_Word)&SECOND_VALUE, 1);
}
počítač_Word 도구읽기(počítač_Word Názov, počítač_Word cieľ_údaje_adresa) {
    if (꾸러미사용중) {
        char údaje_pozícia[512]; int chyba = Cesta(Názov, údaje_pozícia); if (chyba) return (uint32_t)chyba;
        unsigned položka_COUNT = 0; while (údaje_pozícia[položka_COUNT]) položka_COUNT++;
        if (položka_COUNT >= 6) for (unsigned 순번 = 0; 순번 < položka_COUNT - 6; 순번++) if (údaje_pozícia[순번] == '.') údaje_pozícia[순번] = '/';
        unsigned char 바이트들[16384]; počítač_Word *cieľ_VALUE_pozícia = (počítač_Word *)cieľ_údaje_adresa;
        int RECEIVED_COUNT = 꾸러미읽기(údaje_pozícia, 바이트들, cieľ_VALUE_pozícia[0] < sizeof(바이트들) ? cieľ_VALUE_pozícia[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) cieľ_VALUE_pozícia[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Súbor_rukoväť = 꾸러미사용중 ? -2 : (int32_t)nástroj_otvoriť(Názov, 0);
    if (Súbor_rukoväť < 0) {
        char údaje_pozícia[512]; int chyba = Cesta(Názov, údaje_pozícia); if (chyba) return (uint32_t)chyba;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Ďalej_Posun = 자바클래스들[순번].Názov; unsigned 안쪽순번 = 0;
            while (údaje_pozícia[안쪽순번] && údaje_pozícia[안쪽순번] == Ďalej_Posun[안쪽순번]) 안쪽순번++;
            if (údaje_pozícia[안쪽순번] || Ďalej_Posun[안쪽순번]) continue;
            počítač_Word *cieľ_VALUE_pozícia = (počítač_Word *)cieľ_údaje_adresa;
            if (cieľ_VALUE_pozícia[0] < 자바클래스들[순번].Veľkosť) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Veľkosť; 안쪽순번++) cieľ_VALUE_pozícia[안쪽순번 + 1] = 자바클래스들[순번].údaje[안쪽순번];
            return 자바클래스들[순번].Veľkosť;
        }
        return (uint32_t)Súbor_rukoväť;
    }
    počítač_Word *첫째값 = (počítač_Word *)cieľ_údaje_adresa;
    intptr_t Veľkosť = 호출(9, Súbor_rukoväť, 0, 0), Dokončené_úlohy_suma = 0;
    if (Veľkosť < 0 || (počítač_Word)Veľkosť > 첫째값[0]) { nástroj_Zavrieť(Súbor_rukoväť); return (uint32_t)(Veľkosť < 0 ? Veľkosť : -27); }
    unsigned char blok_údajov[256];
    while (Dokončené_úlohy_suma < Veľkosť) {
        intptr_t položka_COUNT = 호출(2, Súbor_rukoväť, (počítač_Word)blok_údajov, Veľkosť - Dokončené_úlohy_suma < 256 ? Veľkosť - Dokončené_úlohy_suma : 256);
        if (položka_COUNT <= 0) { nástroj_Zavrieť(Súbor_rukoväť); return (uint32_t)(položka_COUNT ? položka_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < položka_COUNT; 순번++) 첫째값[1 + Dokončené_úlohy_suma + 순번] = blok_údajov[순번];
        Dokončené_úlohy_suma += položka_COUNT;
    }
    nástroj_Zavrieť(Súbor_rukoväť); return Dokončené_úlohy_suma;
}
počítač_Word nástroj_zapísať(počítač_Word Názov, počítač_Word 원본자료, počítač_Word položka_COUNT_8f7753a1) {
    const počítač_Word *첫째값 = (const počítač_Word *)원본자료;
    if (položka_COUNT_8f7753a1 > 첫째값[0] || položka_COUNT_8f7753a1 > 16384) return (uint32_t)-27;
    int Súbor_rukoväť = (int32_t)nástroj_otvoriť(Názov, 577); if (Súbor_rukoväť < 0) return (uint32_t)Súbor_rukoväť;
    unsigned char blok_údajov[256]; počítač_Word Dokončené_úlohy_suma = 0;
    while (Dokončené_úlohy_suma < položka_COUNT_8f7753a1) {
        počítač_Word položka_COUNT = položka_COUNT_8f7753a1 - Dokončené_úlohy_suma < 256 ? položka_COUNT_8f7753a1 - Dokončené_úlohy_suma : 256;
        for (počítač_Word 순번 = 0; 순번 < položka_COUNT; 순번++) blok_údajov[순번] = 첫째값[1 + Dokončené_úlohy_suma + 순번];
        intptr_t KR = 호출(1, Súbor_rukoväť, (počítač_Word)blok_údajov, položka_COUNT);
        if (KR <= 0) { nástroj_Zavrieť(Súbor_rukoväť); return (uint32_t)(KR ? KR : -5); }
        Dokončené_úlohy_suma += KR;
    }
    nástroj_Zavrieť(Súbor_rukoväť); return položka_COUNT_8f7753a1;
}
počítač_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
počítač_Word nástroj_argument(počítač_Word LOOKUP_INDEX) {
    static const počítač_Word prázdny_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (počítač_Word)prázdny_VALUE;
    unsigned char vstup[256]; intptr_t položka_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *údaje_pozícia = 꾸러미진입클래스(); položka_COUNT = 0; while (údaje_pozícia[položka_COUNT] && položka_COUNT < 255) { vstup[položka_COUNT] = údaje_pozícia[položka_COUNT]; položka_COUNT++; } }
    else položka_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (počítač_Word)vstup, sizeof(vstup));
    if (položka_COUNT < 0) return (počítač_Word)prázdny_VALUE;
    počítač_Word *KR_údaje = 전달인수[LOOKUP_INDEX]; unsigned položka_COUNT_8f7753a1 = 0;
    for (intptr_t 순번 = 0; 순번 < položka_COUNT;) {
        unsigned bod_kódu = vstup[순번++], 더있음 = bod_kódu < 128 ? 0 : bod_kódu >= 0xc2 && bod_kódu < 0xe0 ? 1 : bod_kódu < 0xf0 && bod_kódu >= 0xe0 ? 2 : bod_kódu >= 0xf0 && bod_kódu <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > položka_COUNT) { KR_údaje[++položka_COUNT_8f7753a1] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) bod_kódu &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (vstup[순번] & 0xc0) == 0x80) { bod_kódu = (bod_kódu << 6) | (vstup[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || bod_kódu < 최소값 || bod_kódu > 0x10ffff || (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff)) bod_kódu = 0xfffd;
        if (bod_kódu >= 65536) { bod_kódu -= 65536; KR_údaje[++položka_COUNT_8f7753a1] = 0xd800 | (bod_kódu >> 10); KR_údaje[++položka_COUNT_8f7753a1] = 0xdc00 | (bod_kódu & 1023); }
        else KR_údaje[++položka_COUNT_8f7753a1] = bod_kódu;
    }
    KR_údaje[0] = položka_COUNT_8f7753a1; return (počítač_Word)KR_údaje;
}
počítač_Word 도구분류(void) { return oblasť_VALUE; }
void 커널중단(const char *upozornenie_SMS) {
    const char *údaje_pozícia = upozornenie_SMS; while (*údaje_pozícia) údaje_pozícia++;
    바이트들("Java tool runtime error: ", 25); 바이트들(upozornenie_SMS, údaje_pozícia - upozornenie_SMS); znak(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_používateľ_program(int metóda_MODE) {
    oblasť_VALUE = metóda_MODE;
    unsigned char 첫항목[256]; intptr_t položka_COUNT = 호출(15, 0, (počítač_Word)첫항목, sizeof(첫항목));
    if (metóda_MODE == 2 || (metóda_MODE == 1 && položka_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metóda_MODE == 2 ? 0 : 1;
        char Súbor_položka_názov[256]; intptr_t dĺžka_údaje = 호출(15, 꾸러미인수이동, (počítač_Word)Súbor_položka_názov, sizeof(Súbor_položka_názov));
        if (dĺžka_údaje <= 0 || 꾸러미열기(Súbor_položka_názov) < 0) {
            static const char chyba[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(chyba, sizeof(chyba) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int KR = 자바진입();
    if (대기중짝글자) znak(0xfffd);
    return KR;
}

// UDP는 vlastné 커널의 SVC를 통과하며 v_termíne_splatnosti_položka 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t séria, číslo_portu; uint32_t adresa; unsigned char 영값[8]; };
static struct 자바주소 UDP_adresa(unsigned číslo_portu) {
    struct 자바주소 첫째값 = {2, (uint16_t)((číslo_portu << 8) | (číslo_portu >> 8)), 0x0100007f, {0}}; return 첫째값;
}
počítač_Word nástroj_UDP_otvoriť(počítač_Word číslo_portu) {
    intptr_t Súbor_rukoväť = 호출(32, 2, 2, 17); if (Súbor_rukoväť < 0) return (uint32_t)Súbor_rukoväť;
    struct 자바주소 첫째값 = UDP_adresa(číslo_portu);
    첫째값.adresa = 0;
    intptr_t Stav_VALUE = 호출(33, Súbor_rukoväť, (počítač_Word)&첫째값, sizeof(첫째값));
    if (Stav_VALUE < 0) { nástroj_Zavrieť(Súbor_rukoväť); return (uint32_t)Stav_VALUE; }
    return Súbor_rukoväť;
}
počítač_Word nástroj_UDP_odoslať(počítač_Word Súbor_rukoväť, počítač_Word číslo_portu, počítač_Word pole_VALUE, počítač_Word dĺžka_VALUE) {
    const počítač_Word *원본주소 = (const počítač_Word *)pole_VALUE; unsigned char údaje[512];
    if (dĺžka_VALUE > 512 || dĺžka_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (počítač_Word 순번 = 0; 순번 < dĺžka_VALUE; 순번++) údaje[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(číslo_portu);
    return (uint32_t)사용자호출(34, Súbor_rukoväť, (počítač_Word)údaje, dĺžka_VALUE, 0, (počítač_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t položka_COUNT) { return (položka_COUNT>>24)|((položka_COUNT>>8)&0xff00)|((položka_COUNT<<8)&0xff0000)|(položka_COUNT<<24); }
počítač_Word nástroj_UDP_odoslať_adresa(počítač_Word Súbor_rukoväť, počítač_Word adresa, počítač_Word číslo_portu, počítač_Word pole_VALUE, počítač_Word dĺžka_VALUE) {
    const počítač_Word *원본주소 = (const počítač_Word *)pole_VALUE; unsigned char údaje[512];
    if (dĺžka_VALUE > 512 || dĺžka_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (počítač_Word 순번 = 0; 순번 < dĺžka_VALUE; 순번++) údaje[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adresa(číslo_portu); 첫째값.adresa = 바이트순서뒤집기(adresa);
    return (uint32_t)사용자호출(34, Súbor_rukoväť, (počítač_Word)údaje, dĺžka_VALUE, 0, (počítač_Word)&첫째값, sizeof(첫째값));
}
počítač_Word nástroj_spojiť(počítač_Word Súbor_rukoväť, počítač_Word adresa, počítač_Word číslo_portu) {
    struct 자바주소 첫째값 = UDP_adresa(číslo_portu); 첫째값.adresa = 바이트순서뒤집기(adresa);
    uint32_t Spustiť_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t KR = 호출(37, Súbor_rukoväť, (počítač_Word)&첫째값, sizeof(첫째값));
        if (KR != -115) return (uint32_t)KR;
        if ((uint32_t)(호출(7, 0, 0, 0) - Spustiť_2) >= 1000) return (uint32_t)-110;
    }
}
počítač_Word 도구전문받기(počítač_Word Súbor_rukoväť, počítač_Word pole_VALUE, počítač_Word medzipamäť_kapacita) {
    počítač_Word *cieľ_adresa_08bbd577 = (počítač_Word *)pole_VALUE; unsigned char údaje[512];
    if (medzipamäť_kapacita > 512 || cieľ_adresa_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned dĺžka_údaje = sizeof(첫째값);
    intptr_t položka_COUNT = 사용자호출(35, Súbor_rukoväť, (počítač_Word)údaje, medzipamäť_kapacita, 0, (počítač_Word)&첫째값, (počítač_Word)&dĺžka_údaje);
    if (položka_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < položka_COUNT; 순번++) cieľ_adresa_08bbd577[순번 + 1] = údaje[순번]; cieľ_adresa_08bbd577[513] = (첫째값.číslo_portu << 8 | 첫째값.číslo_portu >> 8) & 65535; cieľ_adresa_08bbd577[514] = 바이트순서뒤집기(첫째값.adresa); }
    return (uint32_t)položka_COUNT;
}
počítač_Word nástroj_UDP_port(počítač_Word Súbor_rukoväť) {
    struct 자바주소 첫째값; unsigned dĺžka_údaje = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Súbor_rukoväť, (počítač_Word)&첫째값, (počítač_Word)&dĺžka_údaje);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.číslo_portu << 8 | 첫째값.číslo_portu >> 8) & 65535);
}
počítač_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
počítač_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
počítač_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
počítač_Word nástroj_grafické_prvky_počkaj(void) { return (uint32_t)화면키기다리기(); }
počítač_Word nástroj_obdĺžnik(počítač_Word X_súradnica, počítač_Word Y_súradnica, počítač_Word 너비값, počítač_Word 높이값, počítač_Word 색상) {
    return (uint32_t)사용자호출(13, X_súradnica, Y_súradnica, 색상, 너비값, 높이값, 0);
}

počítač_Word nástroj_Stream(počítač_Word Akcia,počítač_Word Súbor_rukoväť,počítač_Word VALUE){
    if(Akcia==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_adresa(VALUE);
    if(Akcia==1){첫째값.adresa=0;intptr_t 반환값=호출(33,Súbor_rukoväť,(počítač_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Súbor_rukoväť,4,0));}
    if(Akcia==2)return (uint32_t)호출(37,Súbor_rukoväť,(počítač_Word)&첫째값,sizeof(첫째값));
    if(Akcia==3)return (uint32_t)호출(39,Súbor_rukoväť,0,0);
    if(Akcia==4)return nástroj_UDP_port(Súbor_rukoväť);
    if(Akcia==5)return (uint32_t)호출(40,Súbor_rukoväť,0,0);
    return (uint32_t)-22;
}
počítač_Word nástroj_grafické_používateľské_rozhranie(počítač_Word Akcia,počítač_Word identifikátor_VALUE,počítač_Word 첫째값,počítač_Word SECOND_VALUE,počítač_Word bod_kódu,počítač_Word cieľ_údaje){return (uint32_t)사용자호출(20,Akcia,identifikátor_VALUE,첫째값,SECOND_VALUE,bod_kódu,cieľ_údaje);}
počítač_Word nástroj_grafické_používateľské_rozhranie_SMS(počítač_Word identifikátor_VALUE,počítač_Word pole_VALUE,počítač_Word položka_COUNT){
    const počítač_Word *원본주소=(const počítač_Word *)pole_VALUE;uint32_t údaje[127];unsigned položka_COUNT_8f7753a1=0;
    if(položka_COUNT>원본주소[0])return (uint32_t)-22;
    for(počítač_Word 순번=0;순번<položka_COUNT;순번++){unsigned kódovanie_znakov=원본주소[순번+1];if(kódovanie_znakov>=0xd800&&kódovanie_znakov<=0xdbff&&순번+1<položka_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;kódovanie_znakov=0x10000+((kódovanie_znakov-0xd800)<<10)+낮은값-0xdc00;}if(položka_COUNT_8f7753a1==127)return (uint32_t)-22;údaje[položka_COUNT_8f7753a1++]=kódovanie_znakov;}
    return (uint32_t)사용자호출(21,identifikátor_VALUE,(počítač_Word)údaje,položka_COUNT_8f7753a1,0,0,0);
}
