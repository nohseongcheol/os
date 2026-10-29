#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 název_souboru/výstupní_pozice/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "sada.h"
typedef uintptr_t počítač_Word;
static int oblast_HODNOTA;
static int 꾸러미사용중, 꾸러미인수이동;
static počítač_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned zboží_POČET, počítač_Word 첫째값, počítač_Word SEKUNDA_HODNOTA, počítač_Word bod_kódu) {
    return 사용자호출(zboží_POČET, 첫째값, SEKUNDA_HODNOTA, bod_kódu, 0, 0, 0);
}
static void 바이트들(const char *data_pozice, size_t zboží_POČET) { 호출(1, 1, (počítač_Word)data_pozice, zboží_POČET); }
static void znak(unsigned bod_kódu) {
    unsigned char data[4]; unsigned zboží_POČET = 0;
    if (bod_kódu < 128) data[zboží_POČET++] = bod_kódu;
    else if (bod_kódu < 2048) { data[zboží_POČET++] = 0xc0 | (bod_kódu >> 6); data[zboží_POČET++] = 0x80 | (bod_kódu & 63); }
    else if (bod_kódu < 65536) { data[zboží_POČET++] = 0xe0 | (bod_kódu >> 12); data[zboží_POČET++] = 0x80 | ((bod_kódu >> 6) & 63); data[zboží_POČET++] = 0x80 | (bod_kódu & 63); }
    else { data[zboží_POČET++] = 0xf0 | (bod_kódu >> 18); data[zboží_POČET++] = 0x80 | ((bod_kódu >> 12) & 63); data[zboží_POČET++] = 0x80 | ((bod_kódu >> 6) & 63); data[zboží_POČET++] = 0x80 | (bod_kódu & 63); }
    바이트들((const char *)data, zboží_POČET);
}
počítač_Word nástroj_znak(počítač_Word HODNOTA) {
    unsigned bod_kódu = HODNOTA;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (bod_kódu >= 0xdc00 && bod_kódu <= 0xdfff) { znak(0x10000 + ((높은부분 - 0xd800) << 10) + bod_kódu - 0xdc00); return 1; }
        znak(0xfffd);
    }
    if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff) 대기중짝글자 = bod_kódu;
    else znak(bod_kódu > 0x10ffff || (bod_kódu >= 0xdc00 && bod_kódu <= 0xdfff) ? 0xfffd : bod_kódu);
    return 1;
}
počítač_Word 도구출력(počítač_Word HODNOTA) {
    const počítač_Word *řetězec_data = (const počítač_Word *)HODNOTA;
    for (počítač_Word 순번 = 0; 순번 < řetězec_data[0]; 순번++) nástroj_znak(řetězec_data[순번 + 1]);
    return řetězec_data[0];
}
static int cesta_2(počítač_Word objekt_odkaz, char KV_data[512]) {
    const počítač_Word *첫째값 = (const počítač_Word *)objekt_odkaz;
    unsigned 사용량 = 0;
    for (počítač_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned bod_kódu = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metoda_MODE 경로와 호환한다.
        if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) return -22;
        unsigned zboží_POČET = bod_kódu < 128 ? 1 : bod_kódu < 2048 ? 2 : bod_kódu < 65536 ? 3 : 4;
        if (사용량 + zboží_POČET > 511) return -36;
        if (zboží_POČET == 1) KV_data[사용량++] = bod_kódu;
        else {
            KV_data[사용량++] = (zboží_POČET == 2 ? 0xc0 : zboží_POČET == 3 ? 0xe0 : 0xf0) | (bod_kódu >> (6 * (zboží_POČET - 1)));
            for (unsigned 안쪽순번 = zboží_POČET - 1; 안쪽순번; 안쪽순번--) KV_data[사용량++] = 0x80 | ((bod_kódu >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KV_data[사용량] = 0; return 사용량 ? 0 : -22;
}
počítač_Word nástroj_otevřít(počítač_Word Název, počítač_Word konfigurace_BITS) {
    char data_pozice[512]; int chyba = cesta_2(Název, data_pozice);
    return (uint32_t)(chyba ? chyba : 호출(3, (počítač_Word)data_pozice, konfigurace_BITS, 0));
}
počítač_Word nástroj_Zavřít(počítač_Word popisovač_souboru) { return (uint32_t)호출(4, popisovač_souboru, 0, 0); }
počítač_Word 도구바이트읽기(počítač_Word popisovač_souboru) {
    unsigned char SEKUNDA_HODNOTA; intptr_t zboží_POČET = 호출(2, popisovač_souboru, (počítač_Word)&SEKUNDA_HODNOTA, 1);
    return (uint32_t)(zboží_POČET == 1 ? SEKUNDA_HODNOTA : zboží_POČET == 0 ? 256 : zboží_POČET);
}
počítač_Word nástroj_zápis_bajt(počítač_Word popisovač_souboru, počítač_Word HODNOTA) {
    unsigned char SEKUNDA_HODNOTA = HODNOTA; return (uint32_t)호출(1, popisovač_souboru, (počítač_Word)&SEKUNDA_HODNOTA, 1);
}
počítač_Word 도구읽기(počítač_Word Název, počítač_Word cíl_data_ODKAZ) {
    if (꾸러미사용중) {
        char data_pozice[512]; int chyba = cesta_2(Název, data_pozice); if (chyba) return (uint32_t)chyba;
        unsigned zboží_POČET = 0; while (data_pozice[zboží_POČET]) zboží_POČET++;
        if (zboží_POČET >= 6) for (unsigned 순번 = 0; 순번 < zboží_POČET - 6; 순번++) if (data_pozice[순번] == '.') data_pozice[순번] = '/';
        unsigned char 바이트들[16384]; počítač_Word *cíl_HODNOTA_pozice = (počítač_Word *)cíl_data_ODKAZ;
        int RECEIVED_POČET = 꾸러미읽기(data_pozice, 바이트들, cíl_HODNOTA_pozice[0] < sizeof(바이트들) ? cíl_HODNOTA_pozice[0] : sizeof(바이트들));
        if (RECEIVED_POČET >= 0) { for (int 순번 = 0; 순번 < RECEIVED_POČET; 순번++) cíl_HODNOTA_pozice[순번 + 1] = 바이트들[순번]; return RECEIVED_POČET; }
        if (RECEIVED_POČET != -2) return (uint32_t)RECEIVED_POČET;
    }
    int popisovač_souboru = 꾸러미사용중 ? -2 : (int32_t)nástroj_otevřít(Název, 0);
    if (popisovač_souboru < 0) {
        char data_pozice[512]; int chyba = cesta_2(Název, data_pozice); if (chyba) return (uint32_t)chyba;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Další_POSUN = 자바클래스들[순번].Název; unsigned 안쪽순번 = 0;
            while (data_pozice[안쪽순번] && data_pozice[안쪽순번] == Další_POSUN[안쪽순번]) 안쪽순번++;
            if (data_pozice[안쪽순번] || Další_POSUN[안쪽순번]) continue;
            počítač_Word *cíl_HODNOTA_pozice = (počítač_Word *)cíl_data_ODKAZ;
            if (cíl_HODNOTA_pozice[0] < 자바클래스들[순번].Velikost) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Velikost; 안쪽순번++) cíl_HODNOTA_pozice[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Velikost;
        }
        return (uint32_t)popisovač_souboru;
    }
    počítač_Word *첫째값 = (počítač_Word *)cíl_data_ODKAZ;
    intptr_t Velikost = 호출(9, popisovač_souboru, 0, 0), dokončeno_částka = 0;
    if (Velikost < 0 || (počítač_Word)Velikost > 첫째값[0]) { nástroj_Zavřít(popisovač_souboru); return (uint32_t)(Velikost < 0 ? Velikost : -27); }
    unsigned char datový_blok[256];
    while (dokončeno_částka < Velikost) {
        intptr_t zboží_POČET = 호출(2, popisovač_souboru, (počítač_Word)datový_blok, Velikost - dokončeno_částka < 256 ? Velikost - dokončeno_částka : 256);
        if (zboží_POČET <= 0) { nástroj_Zavřít(popisovač_souboru); return (uint32_t)(zboží_POČET ? zboží_POČET : -5); }
        for (intptr_t 순번 = 0; 순번 < zboží_POČET; 순번++) 첫째값[1 + dokončeno_částka + 순번] = datový_blok[순번];
        dokončeno_částka += zboží_POČET;
    }
    nástroj_Zavřít(popisovač_souboru); return dokončeno_částka;
}
počítač_Word nástroj_zápis(počítač_Word Název, počítač_Word 원본자료, počítač_Word položka_POČET) {
    const počítač_Word *첫째값 = (const počítač_Word *)원본자료;
    if (položka_POČET > 첫째값[0] || položka_POČET > 16384) return (uint32_t)-27;
    int popisovač_souboru = (int32_t)nástroj_otevřít(Název, 577); if (popisovač_souboru < 0) return (uint32_t)popisovač_souboru;
    unsigned char datový_blok[256]; počítač_Word dokončeno_částka = 0;
    while (dokončeno_částka < položka_POČET) {
        počítač_Word zboží_POČET = položka_POČET - dokončeno_částka < 256 ? položka_POČET - dokončeno_částka : 256;
        for (počítač_Word 순번 = 0; 순번 < zboží_POČET; 순번++) datový_blok[순번] = 첫째값[1 + dokončeno_částka + 순번];
        intptr_t VÝSLEDEK = 호출(1, popisovač_souboru, (počítač_Word)datový_blok, zboží_POČET);
        if (VÝSLEDEK <= 0) { nástroj_Zavřít(popisovač_souboru); return (uint32_t)(VÝSLEDEK ? VÝSLEDEK : -5); }
        dokončeno_částka += VÝSLEDEK;
    }
    nástroj_Zavřít(popisovač_souboru); return položka_POČET;
}
počítač_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
počítač_Word nástroj_argument(počítač_Word VYHLEDAT_INDEX) {
    static const počítač_Word 빈값[1] = {0};
    if (VYHLEDAT_INDEX >= 8) return (počítač_Word)빈값;
    unsigned char vstup[256]; intptr_t zboží_POČET;
    if (꾸러미사용중 && VYHLEDAT_INDEX == 0) { const char *data_pozice = 꾸러미진입클래스(); zboží_POČET = 0; while (data_pozice[zboží_POČET] && zboží_POČET < 255) { vstup[zboží_POČET] = data_pozice[zboží_POČET]; zboží_POČET++; } }
    else zboží_POČET = 호출(15, VYHLEDAT_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (počítač_Word)vstup, sizeof(vstup));
    if (zboží_POČET < 0) return (počítač_Word)빈값;
    počítač_Word *KV_data = 전달인수[VYHLEDAT_INDEX]; unsigned položka_POČET = 0;
    for (intptr_t 순번 = 0; 순번 < zboží_POČET;) {
        unsigned bod_kódu = vstup[순번++], 더있음 = bod_kódu < 128 ? 0 : bod_kódu >= 0xc2 && bod_kódu < 0xe0 ? 1 : bod_kódu < 0xf0 && bod_kódu >= 0xe0 ? 2 : bod_kódu >= 0xf0 && bod_kódu <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > zboží_POČET) { KV_data[++položka_POČET] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) bod_kódu &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (vstup[순번] & 0xc0) == 0x80) { bod_kódu = (bod_kódu << 6) | (vstup[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || bod_kódu < 최소값 || bod_kódu > 0x10ffff || (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff)) bod_kódu = 0xfffd;
        if (bod_kódu >= 65536) { bod_kódu -= 65536; KV_data[++položka_POČET] = 0xd800 | (bod_kódu >> 10); KV_data[++položka_POČET] = 0xdc00 | (bod_kódu & 1023); }
        else KV_data[++položka_POČET] = bod_kódu;
    }
    KV_data[0] = položka_POČET; return (počítač_Word)KV_data;
}
počítač_Word nástroj_Druh(void) { return oblast_HODNOTA; }
void 커널중단(const char *povinnost_zvěřejnit_SMS) {
    const char *data_pozice = povinnost_zvěřejnit_SMS; while (*data_pozice) data_pozice++;
    바이트들("Java tool runtime error: ", 25); 바이트들(povinnost_zvěřejnit_SMS, data_pozice - povinnost_zvěřejnit_SMS); znak(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_uživatel_program(int metoda_MODE) {
    oblast_HODNOTA = metoda_MODE;
    unsigned char 첫항목[256]; intptr_t zboží_POČET = 호출(15, 0, (počítač_Word)첫항목, sizeof(첫항목));
    if (metoda_MODE == 2 || (metoda_MODE == 1 && zboží_POČET == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metoda_MODE == 2 ? 0 : 1;
        char Soubor_položka_název[256]; intptr_t délka_data = 호출(15, 꾸러미인수이동, (počítač_Word)Soubor_položka_název, sizeof(Soubor_položka_název));
        if (délka_data <= 0 || 꾸러미열기(Soubor_položka_název) < 0) {
            static const char chyba[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(chyba, sizeof(chyba) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int VÝSLEDEK = 자바진입();
    if (대기중짝글자) znak(0xfffd);
    return VÝSLEDEK;
}

// UDP는 vlastní 커널의 SVC를 통과하며 dobrá_zboží 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t řada, číslo_portu; uint32_t Adresa; unsigned char nulová_hodnota[8]; };
static struct 자바주소 protokol_UDP_ODKAZ(unsigned číslo_portu) {
    struct 자바주소 첫째값 = {2, (uint16_t)((číslo_portu << 8) | (číslo_portu >> 8)), 0x0100007f, {0}}; return 첫째값;
}
počítač_Word nástroj_protokol_UDP_otevřít(počítač_Word číslo_portu) {
    intptr_t popisovač_souboru = 호출(32, 2, 2, 17); if (popisovač_souboru < 0) return (uint32_t)popisovač_souboru;
    struct 자바주소 첫째값 = protokol_UDP_ODKAZ(číslo_portu);
    첫째값.Adresa = 0;
    intptr_t Stav_HODNOTA = 호출(33, popisovač_souboru, (počítač_Word)&첫째값, sizeof(첫째값));
    if (Stav_HODNOTA < 0) { nástroj_Zavřít(popisovač_souboru); return (uint32_t)Stav_HODNOTA; }
    return popisovač_souboru;
}
počítač_Word nástroj_protokol_UDP_poslat(počítač_Word popisovač_souboru, počítač_Word číslo_portu, počítač_Word pole_HODNOTA, počítač_Word délka_HODNOTA) {
    const počítač_Word *원본주소 = (const počítač_Word *)pole_HODNOTA; unsigned char data[512];
    if (délka_HODNOTA > 512 || délka_HODNOTA > 원본주소[0]) return (uint32_t)-90;
    for (počítač_Word 순번 = 0; 순번 < délka_HODNOTA; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = protokol_UDP_ODKAZ(číslo_portu);
    return (uint32_t)사용자호출(34, popisovač_souboru, (počítač_Word)data, délka_HODNOTA, 0, (počítač_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t zboží_POČET) { return (zboží_POČET>>24)|((zboží_POČET>>8)&0xff00)|((zboží_POČET<<8)&0xff0000)|(zboží_POČET<<24); }
počítač_Word nástroj_protokol_UDP_poslat_ODKAZ(počítač_Word popisovač_souboru, počítač_Word Adresa, počítač_Word číslo_portu, počítač_Word pole_HODNOTA, počítač_Word délka_HODNOTA) {
    const počítač_Word *원본주소 = (const počítač_Word *)pole_HODNOTA; unsigned char data[512];
    if (délka_HODNOTA > 512 || délka_HODNOTA > 원본주소[0]) return (uint32_t)-90;
    for (počítač_Word 순번 = 0; 순번 < délka_HODNOTA; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = protokol_UDP_ODKAZ(číslo_portu); 첫째값.Adresa = 바이트순서뒤집기(Adresa);
    return (uint32_t)사용자호출(34, popisovač_souboru, (počítač_Word)data, délka_HODNOTA, 0, (počítač_Word)&첫째값, sizeof(첫째값));
}
počítač_Word nástroj_spojit(počítač_Word popisovač_souboru, počítač_Word Adresa, počítač_Word číslo_portu) {
    struct 자바주소 첫째값 = protokol_UDP_ODKAZ(číslo_portu); 첫째값.Adresa = 바이트순서뒤집기(Adresa);
    uint32_t Spustit_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t VÝSLEDEK = 호출(37, popisovač_souboru, (počítač_Word)&첫째값, sizeof(첫째값));
        if (VÝSLEDEK != -115) return (uint32_t)VÝSLEDEK;
        if ((uint32_t)(호출(7, 0, 0, 0) - Spustit_2) >= 1000) return (uint32_t)-110;
    }
}
počítač_Word 도구전문받기(počítač_Word popisovač_souboru, počítač_Word pole_HODNOTA, počítač_Word zásobník_kapacita) {
    počítač_Word *cíl_ODKAZ_08bbd577 = (počítač_Word *)pole_HODNOTA; unsigned char data[512];
    if (zásobník_kapacita > 512 || cíl_ODKAZ_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned délka_data = sizeof(첫째값);
    intptr_t zboží_POČET = 사용자호출(35, popisovač_souboru, (počítač_Word)data, zásobník_kapacita, 0, (počítač_Word)&첫째값, (počítač_Word)&délka_data);
    if (zboží_POČET >= 0) { for (intptr_t 순번 = 0; 순번 < zboží_POČET; 순번++) cíl_ODKAZ_08bbd577[순번 + 1] = data[순번]; cíl_ODKAZ_08bbd577[513] = (첫째값.číslo_portu << 8 | 첫째값.číslo_portu >> 8) & 65535; cíl_ODKAZ_08bbd577[514] = 바이트순서뒤집기(첫째값.Adresa); }
    return (uint32_t)zboží_POČET;
}
počítač_Word nástroj_protokol_UDP_port(počítač_Word popisovač_souboru) {
    struct 자바주소 첫째값; unsigned délka_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, popisovač_souboru, (počítač_Word)&첫째값, (počítač_Word)&délka_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.číslo_portu << 8 | 첫째값.číslo_portu >> 8) & 65535);
}
počítač_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
počítač_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
počítač_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
počítač_Word nástroj_grafika_počkej(void) { return (uint32_t)화면키기다리기(); }
počítač_Word nástroj_obdélník(počítač_Word souřadnice_x, počítač_Word Y_souřadnice, počítač_Word 너비값, počítač_Word vyžádáno_výška_HODNOTA, počítač_Word 색상) {
    return (uint32_t)사용자호출(13, souřadnice_x, Y_souřadnice, 색상, 너비값, vyžádáno_výška_HODNOTA, 0);
}

počítač_Word nástroj_tok(počítač_Word Akce,počítač_Word popisovač_souboru,počítač_Word HODNOTA){
    if(Akce==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=protokol_UDP_ODKAZ(HODNOTA);
    if(Akce==1){첫째값.Adresa=0;intptr_t 반환값=호출(33,popisovač_souboru,(počítač_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,popisovač_souboru,4,0));}
    if(Akce==2)return (uint32_t)호출(37,popisovač_souboru,(počítač_Word)&첫째값,sizeof(첫째값));
    if(Akce==3)return (uint32_t)호출(39,popisovač_souboru,0,0);
    if(Akce==4)return nástroj_protokol_UDP_port(popisovač_souboru);
    if(Akce==5)return (uint32_t)호출(40,popisovač_souboru,0,0);
    return (uint32_t)-22;
}
počítač_Word nástroj_grafické_rozhraní_GUI(počítač_Word Akce,počítač_Word identifikátor_HODNOTA,počítač_Word 첫째값,počítač_Word SEKUNDA_HODNOTA,počítač_Word bod_kódu,počítač_Word cíl_data){return (uint32_t)사용자호출(20,Akce,identifikátor_HODNOTA,첫째값,SEKUNDA_HODNOTA,bod_kódu,cíl_data);}
počítač_Word nástroj_grafické_rozhraní_GUI_SMS(počítač_Word identifikátor_HODNOTA,počítač_Word pole_HODNOTA,počítač_Word zboží_POČET){
    const počítač_Word *원본주소=(const počítač_Word *)pole_HODNOTA;uint32_t data[127];unsigned položka_POČET=0;
    if(zboží_POČET>원본주소[0])return (uint32_t)-22;
    for(počítač_Word 순번=0;순번<zboží_POČET;순번++){unsigned kódování_znaků=원본주소[순번+1];if(kódování_znaků>=0xd800&&kódování_znaků<=0xdbff&&순번+1<zboží_POČET){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;kódování_znaků=0x10000+((kódování_znaků-0xd800)<<10)+낮은값-0xdc00;}if(položka_POČET==127)return (uint32_t)-22;data[položka_POČET++]=kódování_znaků;}
    return (uint32_t)사용자호출(21,identifikátor_HODNOTA,(počítač_Word)data,položka_POČET,0,0,0);
}
