#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fitxategia/Irteera/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "multzo.h"
typedef uintptr_t gailu_Word;
static int Kategoria_balio;
static int 꾸러미사용중, 꾸러미인수이동;
static gailu_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned elementu_ZENBATU, gailu_Word 첫째값, gailu_Word SEGUNDOA_balio, gailu_Word karaktere_kode) {
    return 사용자호출(elementu_ZENBATU, 첫째값, SEGUNDOA_balio, karaktere_kode, 0, 0, 0);
}
static void 바이트들(const char *datuak_kargu, size_t elementu_ZENBATU) { 호출(1, 1, (gailu_Word)datuak_kargu, elementu_ZENBATU); }
static void karaktere(unsigned karaktere_kode) {
    unsigned char datuak[4]; unsigned elementu_ZENBATU = 0;
    if (karaktere_kode < 128) datuak[elementu_ZENBATU++] = karaktere_kode;
    else if (karaktere_kode < 2048) { datuak[elementu_ZENBATU++] = 0xc0 | (karaktere_kode >> 6); datuak[elementu_ZENBATU++] = 0x80 | (karaktere_kode & 63); }
    else if (karaktere_kode < 65536) { datuak[elementu_ZENBATU++] = 0xe0 | (karaktere_kode >> 12); datuak[elementu_ZENBATU++] = 0x80 | ((karaktere_kode >> 6) & 63); datuak[elementu_ZENBATU++] = 0x80 | (karaktere_kode & 63); }
    else { datuak[elementu_ZENBATU++] = 0xf0 | (karaktere_kode >> 18); datuak[elementu_ZENBATU++] = 0x80 | ((karaktere_kode >> 12) & 63); datuak[elementu_ZENBATU++] = 0x80 | ((karaktere_kode >> 6) & 63); datuak[elementu_ZENBATU++] = 0x80 | (karaktere_kode & 63); }
    바이트들((const char *)datuak, elementu_ZENBATU);
}
gailu_Word tresna_karaktere(gailu_Word balio) {
    unsigned karaktere_kode = balio;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (karaktere_kode >= 0xdc00 && karaktere_kode <= 0xdfff) { karaktere(0x10000 + ((높은부분 - 0xd800) << 10) + karaktere_kode - 0xdc00); return 1; }
        karaktere(0xfffd);
    }
    if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdbff) 대기중짝글자 = karaktere_kode;
    else karaktere(karaktere_kode > 0x10ffff || (karaktere_kode >= 0xdc00 && karaktere_kode <= 0xdfff) ? 0xfffd : karaktere_kode);
    return 1;
}
gailu_Word tresna_inprimatu(gailu_Word balio) {
    const gailu_Word *kate_datuak = (const gailu_Word *)balio;
    for (gailu_Word 순번 = 0; 순번 < kate_datuak[0]; 순번++) tresna_karaktere(kate_datuak[순번 + 1]);
    return kate_datuak[0];
}
static int Bide_izena(gailu_Word objektu_Erreferentzia_materiala, char neurria_datuak[512]) {
    const gailu_Word *첫째값 = (const gailu_Word *)objektu_Erreferentzia_materiala;
    unsigned 사용량 = 0;
    for (gailu_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned karaktere_kode = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] 방식 경로와 호환한다.
        if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; karaktere_kode = 0x10000 + ((karaktere_kode - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdfff) return -22;
        unsigned elementu_ZENBATU = karaktere_kode < 128 ? 1 : karaktere_kode < 2048 ? 2 : karaktere_kode < 65536 ? 3 : 4;
        if (사용량 + elementu_ZENBATU > 511) return -36;
        if (elementu_ZENBATU == 1) neurria_datuak[사용량++] = karaktere_kode;
        else {
            neurria_datuak[사용량++] = (elementu_ZENBATU == 2 ? 0xc0 : elementu_ZENBATU == 3 ? 0xe0 : 0xf0) | (karaktere_kode >> (6 * (elementu_ZENBATU - 1)));
            for (unsigned 안쪽순번 = elementu_ZENBATU - 1; 안쪽순번; 안쪽순번--) neurria_datuak[사용량++] = 0x80 | ((karaktere_kode >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    neurria_datuak[사용량] = 0; return 사용량 ? 0 : -22;
}
gailu_Word tresna_ireki(gailu_Word Izena, gailu_Word konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna) {
    char datuak_kargu[512]; int errorea = Bide_izena(Izena, datuak_kargu);
    return (uint32_t)(errorea ? errorea : 호출(3, (gailu_Word)datuak_kargu, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, 0));
}
gailu_Word tresna_itxi(gailu_Word fitxategi_helduleku) { return (uint32_t)호출(4, fitxategi_helduleku, 0, 0); }
gailu_Word 도구바이트읽기(gailu_Word fitxategi_helduleku) {
    unsigned char SEGUNDOA_balio; intptr_t elementu_ZENBATU = 호출(2, fitxategi_helduleku, (gailu_Word)&SEGUNDOA_balio, 1);
    return (uint32_t)(elementu_ZENBATU == 1 ? SEGUNDOA_balio : elementu_ZENBATU == 0 ? 256 : elementu_ZENBATU);
}
gailu_Word tresna_idatzi_byte(gailu_Word fitxategi_helduleku, gailu_Word balio) {
    unsigned char SEGUNDOA_balio = balio; return (uint32_t)호출(1, fitxategi_helduleku, (gailu_Word)&SEGUNDOA_balio, 1);
}
gailu_Word 도구읽기(gailu_Word Izena, gailu_Word helburu_datuak_helbide) {
    if (꾸러미사용중) {
        char datuak_kargu[512]; int errorea = Bide_izena(Izena, datuak_kargu); if (errorea) return (uint32_t)errorea;
        unsigned elementu_ZENBATU = 0; while (datuak_kargu[elementu_ZENBATU]) elementu_ZENBATU++;
        if (elementu_ZENBATU >= 6) for (unsigned 순번 = 0; 순번 < elementu_ZENBATU - 6; 순번++) if (datuak_kargu[순번] == '.') datuak_kargu[순번] = '/';
        unsigned char 바이트들[16384]; gailu_Word *helburu_balio_kargu = (gailu_Word *)helburu_datuak_helbide;
        int RECEIVED_ZENBATU = 꾸러미읽기(datuak_kargu, 바이트들, helburu_balio_kargu[0] < sizeof(바이트들) ? helburu_balio_kargu[0] : sizeof(바이트들));
        if (RECEIVED_ZENBATU >= 0) { for (int 순번 = 0; 순번 < RECEIVED_ZENBATU; 순번++) helburu_balio_kargu[순번 + 1] = 바이트들[순번]; return RECEIVED_ZENBATU; }
        if (RECEIVED_ZENBATU != -2) return (uint32_t)RECEIVED_ZENBATU;
    }
    int fitxategi_helduleku = 꾸러미사용중 ? -2 : (int32_t)tresna_ireki(Izena, 0);
    if (fitxategi_helduleku < 0) {
        char datuak_kargu[512]; int errorea = Bide_izena(Izena, datuak_kargu); if (errorea) return (uint32_t)errorea;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Hurrengoa_Geruzak = 자바클래스들[순번].Izena; unsigned 안쪽순번 = 0;
            while (datuak_kargu[안쪽순번] && datuak_kargu[안쪽순번] == Hurrengoa_Geruzak[안쪽순번]) 안쪽순번++;
            if (datuak_kargu[안쪽순번] || Hurrengoa_Geruzak[안쪽순번]) continue;
            gailu_Word *helburu_balio_kargu = (gailu_Word *)helburu_datuak_helbide;
            if (helburu_balio_kargu[0] < 자바클래스들[순번].Tamaina) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Tamaina; 안쪽순번++) helburu_balio_kargu[안쪽순번 + 1] = 자바클래스들[순번].datuak[안쪽순번];
            return 자바클래스들[순번].Tamaina;
        }
        return (uint32_t)fitxategi_helduleku;
    }
    gailu_Word *첫째값 = (gailu_Word *)helburu_datuak_helbide;
    intptr_t Tamaina = 호출(9, fitxategi_helduleku, 0, 0), Osatutakoak_kopuru = 0;
    if (Tamaina < 0 || (gailu_Word)Tamaina > 첫째값[0]) { tresna_itxi(fitxategi_helduleku); return (uint32_t)(Tamaina < 0 ? Tamaina : -27); }
    unsigned char datuak_blokeatu[256];
    while (Osatutakoak_kopuru < Tamaina) {
        intptr_t elementu_ZENBATU = 호출(2, fitxategi_helduleku, (gailu_Word)datuak_blokeatu, Tamaina - Osatutakoak_kopuru < 256 ? Tamaina - Osatutakoak_kopuru : 256);
        if (elementu_ZENBATU <= 0) { tresna_itxi(fitxategi_helduleku); return (uint32_t)(elementu_ZENBATU ? elementu_ZENBATU : -5); }
        for (intptr_t 순번 = 0; 순번 < elementu_ZENBATU; 순번++) 첫째값[1 + Osatutakoak_kopuru + 순번] = datuak_blokeatu[순번];
        Osatutakoak_kopuru += elementu_ZENBATU;
    }
    tresna_itxi(fitxategi_helduleku); return Osatutakoak_kopuru;
}
gailu_Word tresna_idatzi(gailu_Word Izena, gailu_Word 원본자료, gailu_Word sarrera_ZENBATU) {
    const gailu_Word *첫째값 = (const gailu_Word *)원본자료;
    if (sarrera_ZENBATU > 첫째값[0] || sarrera_ZENBATU > 16384) return (uint32_t)-27;
    int fitxategi_helduleku = (int32_t)tresna_ireki(Izena, 577); if (fitxategi_helduleku < 0) return (uint32_t)fitxategi_helduleku;
    unsigned char datuak_blokeatu[256]; gailu_Word Osatutakoak_kopuru = 0;
    while (Osatutakoak_kopuru < sarrera_ZENBATU) {
        gailu_Word elementu_ZENBATU = sarrera_ZENBATU - Osatutakoak_kopuru < 256 ? sarrera_ZENBATU - Osatutakoak_kopuru : 256;
        for (gailu_Word 순번 = 0; 순번 < elementu_ZENBATU; 순번++) datuak_blokeatu[순번] = 첫째값[1 + Osatutakoak_kopuru + 순번];
        intptr_t EMAITZA = 호출(1, fitxategi_helduleku, (gailu_Word)datuak_blokeatu, elementu_ZENBATU);
        if (EMAITZA <= 0) { tresna_itxi(fitxategi_helduleku); return (uint32_t)(EMAITZA ? EMAITZA : -5); }
        Osatutakoak_kopuru += EMAITZA;
    }
    tresna_itxi(fitxategi_helduleku); return sarrera_ZENBATU;
}
gailu_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
gailu_Word tresna_arg(gailu_Word BEGIRATU_INDIZE) {
    static const gailu_Word 빈값[1] = {0};
    if (BEGIRATU_INDIZE >= 8) return (gailu_Word)빈값;
    unsigned char 입력결과[256]; intptr_t elementu_ZENBATU;
    if (꾸러미사용중 && BEGIRATU_INDIZE == 0) { const char *datuak_kargu = 꾸러미진입클래스(); elementu_ZENBATU = 0; while (datuak_kargu[elementu_ZENBATU] && elementu_ZENBATU < 255) { 입력결과[elementu_ZENBATU] = datuak_kargu[elementu_ZENBATU]; elementu_ZENBATU++; } }
    else elementu_ZENBATU = 호출(15, BEGIRATU_INDIZE + (꾸러미사용중 ? 꾸러미인수이동 : 0), (gailu_Word)입력결과, sizeof(입력결과));
    if (elementu_ZENBATU < 0) return (gailu_Word)빈값;
    gailu_Word *neurria_datuak = 전달인수[BEGIRATU_INDIZE]; unsigned sarrera_ZENBATU = 0;
    for (intptr_t 순번 = 0; 순번 < elementu_ZENBATU;) {
        unsigned karaktere_kode = 입력결과[순번++], 더있음 = karaktere_kode < 128 ? 0 : karaktere_kode >= 0xc2 && karaktere_kode < 0xe0 ? 1 : karaktere_kode < 0xf0 && karaktere_kode >= 0xe0 ? 2 : karaktere_kode >= 0xf0 && karaktere_kode <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > elementu_ZENBATU) { neurria_datuak[++sarrera_ZENBATU] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) karaktere_kode &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { karaktere_kode = (karaktere_kode << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || karaktere_kode < 최소값 || karaktere_kode > 0x10ffff || (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdfff)) karaktere_kode = 0xfffd;
        if (karaktere_kode >= 65536) { karaktere_kode -= 65536; neurria_datuak[++sarrera_ZENBATU] = 0xd800 | (karaktere_kode >> 10); neurria_datuak[++sarrera_ZENBATU] = 0xdc00 | (karaktere_kode & 1023); }
        else neurria_datuak[++sarrera_ZENBATU] = karaktere_kode;
    }
    neurria_datuak[0] = sarrera_ZENBATU; return (gailu_Word)neurria_datuak;
}
gailu_Word 도구분류(void) { return Kategoria_balio; }
void 커널중단(const char *알림문) {
    const char *datuak_kargu = 알림문; while (*datuak_kargu) datuak_kargu++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, datuak_kargu - 알림문); karaktere(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int HASI_erabiltzaile_aplik(int 방식) {
    Kategoria_balio = 방식;
    unsigned char 첫항목[256]; intptr_t elementu_ZENBATU = 호출(15, 0, (gailu_Word)첫항목, sizeof(첫항목));
    if (방식 == 2 || (방식 == 1 && elementu_ZENBATU == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = 방식 == 2 ? 0 : 1;
        char fitxategi_sarrera_izen[256]; intptr_t luzera_datuak = 호출(15, 꾸러미인수이동, (gailu_Word)fitxategi_sarrera_izen, sizeof(fitxategi_sarrera_izen));
        if (luzera_datuak <= 0 || 꾸러미열기(fitxategi_sarrera_izen) < 0) {
            static const char errorea[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(errorea, sizeof(errorea) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int EMAITZA = 자바진입();
    if (대기중짝글자) karaktere(0xfffd);
    return EMAITZA;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t sorta, ataka_zenbaki; uint32_t helbide; unsigned char 영값[8]; };
static struct 자바주소 UDP_helbide(unsigned ataka_zenbaki) {
    struct 자바주소 첫째값 = {2, (uint16_t)((ataka_zenbaki << 8) | (ataka_zenbaki >> 8)), 0x0100007f, {0}}; return 첫째값;
}
gailu_Word tresna_UDP_ireki(gailu_Word ataka_zenbaki) {
    intptr_t fitxategi_helduleku = 호출(32, 2, 2, 17); if (fitxategi_helduleku < 0) return (uint32_t)fitxategi_helduleku;
    struct 자바주소 첫째값 = UDP_helbide(ataka_zenbaki);
    첫째값.helbide = 0;
    intptr_t Egoera_balio = 호출(33, fitxategi_helduleku, (gailu_Word)&첫째값, sizeof(첫째값));
    if (Egoera_balio < 0) { tresna_itxi(fitxategi_helduleku); return (uint32_t)Egoera_balio; }
    return fitxategi_helduleku;
}
gailu_Word tresna_UDP_bidali(gailu_Word fitxategi_helduleku, gailu_Word ataka_zenbaki, gailu_Word matrize_balio, gailu_Word luzera_balio) {
    const gailu_Word *원본주소 = (const gailu_Word *)matrize_balio; unsigned char datuak[512];
    if (luzera_balio > 512 || luzera_balio > 원본주소[0]) return (uint32_t)-90;
    for (gailu_Word 순번 = 0; 순번 < luzera_balio; 순번++) datuak[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_helbide(ataka_zenbaki);
    return (uint32_t)사용자호출(34, fitxategi_helduleku, (gailu_Word)datuak, luzera_balio, 0, (gailu_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t elementu_ZENBATU) { return (elementu_ZENBATU>>24)|((elementu_ZENBATU>>8)&0xff00)|((elementu_ZENBATU<<8)&0xff0000)|(elementu_ZENBATU<<24); }
gailu_Word tresna_UDP_bidali_helbide(gailu_Word fitxategi_helduleku, gailu_Word helbide, gailu_Word ataka_zenbaki, gailu_Word matrize_balio, gailu_Word luzera_balio) {
    const gailu_Word *원본주소 = (const gailu_Word *)matrize_balio; unsigned char datuak[512];
    if (luzera_balio > 512 || luzera_balio > 원본주소[0]) return (uint32_t)-90;
    for (gailu_Word 순번 = 0; 순번 < luzera_balio; 순번++) datuak[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_helbide(ataka_zenbaki); 첫째값.helbide = 바이트순서뒤집기(helbide);
    return (uint32_t)사용자호출(34, fitxategi_helduleku, (gailu_Word)datuak, luzera_balio, 0, (gailu_Word)&첫째값, sizeof(첫째값));
}
gailu_Word tresna_KONEKTATU(gailu_Word fitxategi_helduleku, gailu_Word helbide, gailu_Word ataka_zenbaki) {
    struct 자바주소 첫째값 = UDP_helbide(ataka_zenbaki); 첫째값.helbide = 바이트순서뒤집기(helbide);
    uint32_t Exekutatu_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t EMAITZA = 호출(37, fitxategi_helduleku, (gailu_Word)&첫째값, sizeof(첫째값));
        if (EMAITZA != -115) return (uint32_t)EMAITZA;
        if ((uint32_t)(호출(7, 0, 0, 0) - Exekutatu_2) >= 1000) return (uint32_t)-110;
    }
}
gailu_Word 도구전문받기(gailu_Word fitxategi_helduleku, gailu_Word matrize_balio, gailu_Word buffer_ahalmen) {
    gailu_Word *helburu_helbide_08bbd577 = (gailu_Word *)matrize_balio; unsigned char datuak[512];
    if (buffer_ahalmen > 512 || helburu_helbide_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned luzera_datuak = sizeof(첫째값);
    intptr_t elementu_ZENBATU = 사용자호출(35, fitxategi_helduleku, (gailu_Word)datuak, buffer_ahalmen, 0, (gailu_Word)&첫째값, (gailu_Word)&luzera_datuak);
    if (elementu_ZENBATU >= 0) { for (intptr_t 순번 = 0; 순번 < elementu_ZENBATU; 순번++) helburu_helbide_08bbd577[순번 + 1] = datuak[순번]; helburu_helbide_08bbd577[513] = (첫째값.ataka_zenbaki << 8 | 첫째값.ataka_zenbaki >> 8) & 65535; helburu_helbide_08bbd577[514] = 바이트순서뒤집기(첫째값.helbide); }
    return (uint32_t)elementu_ZENBATU;
}
gailu_Word tresna_UDP_ataka(gailu_Word fitxategi_helduleku) {
    struct 자바주소 첫째값; unsigned luzera_datuak = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fitxategi_helduleku, (gailu_Word)&첫째값, (gailu_Word)&luzera_datuak);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.ataka_zenbaki << 8 | 첫째값.ataka_zenbaki >> 8) & 65535);
}
gailu_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
gailu_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
gailu_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
gailu_Word tresna_grafikoak_itxaron(void) { return (uint32_t)화면키기다리기(); }
gailu_Word 도구사각형(gailu_Word X_koordenatu, gailu_Word Y_koordenatu, gailu_Word 너비값, gailu_Word 높이값, gailu_Word 색상) {
    return (uint32_t)사용자호출(13, X_koordenatu, Y_koordenatu, 색상, 너비값, 높이값, 0);
}

gailu_Word tresna_Stream(gailu_Word Ekintza,gailu_Word fitxategi_helduleku,gailu_Word balio){
    if(Ekintza==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_helbide(balio);
    if(Ekintza==1){첫째값.helbide=0;intptr_t 반환값=호출(33,fitxategi_helduleku,(gailu_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fitxategi_helduleku,4,0));}
    if(Ekintza==2)return (uint32_t)호출(37,fitxategi_helduleku,(gailu_Word)&첫째값,sizeof(첫째값));
    if(Ekintza==3)return (uint32_t)호출(39,fitxategi_helduleku,0,0);
    if(Ekintza==4)return tresna_UDP_ataka(fitxategi_helduleku);
    if(Ekintza==5)return (uint32_t)호출(40,fitxategi_helduleku,0,0);
    return (uint32_t)-22;
}
gailu_Word tresna_GUI(gailu_Word Ekintza,gailu_Word identifikatzaile_balio,gailu_Word 첫째값,gailu_Word SEGUNDOA_balio,gailu_Word karaktere_kode,gailu_Word helburu_datuak){return (uint32_t)사용자호출(20,Ekintza,identifikatzaile_balio,첫째값,SEGUNDOA_balio,karaktere_kode,helburu_datuak);}
gailu_Word tresna_GUI_SMS(gailu_Word identifikatzaile_balio,gailu_Word matrize_balio,gailu_Word elementu_ZENBATU){
    const gailu_Word *원본주소=(const gailu_Word *)matrize_balio;uint32_t datuak[127];unsigned sarrera_ZENBATU=0;
    if(elementu_ZENBATU>원본주소[0])return (uint32_t)-22;
    for(gailu_Word 순번=0;순번<elementu_ZENBATU;순번++){unsigned karaktere_kodeketa=원본주소[순번+1];if(karaktere_kodeketa>=0xd800&&karaktere_kodeketa<=0xdbff&&순번+1<elementu_ZENBATU){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;karaktere_kodeketa=0x10000+((karaktere_kodeketa-0xd800)<<10)+낮은값-0xdc00;}if(sarrera_ZENBATU==127)return (uint32_t)-22;datuak[sarrera_ZENBATU++]=karaktere_kodeketa;}
    return (uint32_t)사용자호출(21,identifikatzaile_balio,(gailu_Word)datuak,sarrera_ZENBATU,0,0,0);
}
