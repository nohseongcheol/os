#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fayil/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "dami.h"
typedef uintptr_t na_ura_mai_kwakwalwa_Microsoft_Word;
static int ɓangare_Daraja;
static int 꾸러미사용중, 꾸러미인수이동;
static na_ura_mai_kwakwalwa_Microsoft_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, na_ura_mai_kwakwalwa_Microsoft_Word 첫째값, na_ura_mai_kwakwalwa_Microsoft_Word 둘째값, na_ura_mai_kwakwalwa_Microsoft_Word Lambar_sirrin_harafi) {
    return 사용자호출(개수, 첫째값, 둘째값, Lambar_sirrin_harafi, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (na_ura_mai_kwakwalwa_Microsoft_Word)자료위치, 개수); }
static void Harafi(unsigned Lambar_sirrin_harafi) {
    unsigned char Tarin_bayani[4]; unsigned 개수 = 0;
    if (Lambar_sirrin_harafi < 128) Tarin_bayani[개수++] = Lambar_sirrin_harafi;
    else if (Lambar_sirrin_harafi < 2048) { Tarin_bayani[개수++] = 0xc0 | (Lambar_sirrin_harafi >> 6); Tarin_bayani[개수++] = 0x80 | (Lambar_sirrin_harafi & 63); }
    else if (Lambar_sirrin_harafi < 65536) { Tarin_bayani[개수++] = 0xe0 | (Lambar_sirrin_harafi >> 12); Tarin_bayani[개수++] = 0x80 | ((Lambar_sirrin_harafi >> 6) & 63); Tarin_bayani[개수++] = 0x80 | (Lambar_sirrin_harafi & 63); }
    else { Tarin_bayani[개수++] = 0xf0 | (Lambar_sirrin_harafi >> 18); Tarin_bayani[개수++] = 0x80 | ((Lambar_sirrin_harafi >> 12) & 63); Tarin_bayani[개수++] = 0x80 | ((Lambar_sirrin_harafi >> 6) & 63); Tarin_bayani[개수++] = 0x80 | (Lambar_sirrin_harafi & 63); }
    바이트들((const char *)Tarin_bayani, 개수);
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_Harafi(na_ura_mai_kwakwalwa_Microsoft_Word Daraja) {
    unsigned Lambar_sirrin_harafi = Daraja;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (Lambar_sirrin_harafi >= 0xdc00 && Lambar_sirrin_harafi <= 0xdfff) { Harafi(0x10000 + ((높은부분 - 0xd800) << 10) + Lambar_sirrin_harafi - 0xdc00); return 1; }
        Harafi(0xfffd);
    }
    if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdbff) 대기중짝글자 = Lambar_sirrin_harafi;
    else Harafi(Lambar_sirrin_harafi > 0x10ffff || (Lambar_sirrin_harafi >= 0xdc00 && Lambar_sirrin_harafi <= 0xdfff) ? 0xfffd : Lambar_sirrin_harafi);
    return 1;
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_yi_ɗab_i(na_ura_mai_kwakwalwa_Microsoft_Word Daraja) {
    const na_ura_mai_kwakwalwa_Microsoft_Word *Zare_Tarin_bayani = (const na_ura_mai_kwakwalwa_Microsoft_Word *)Daraja;
    for (na_ura_mai_kwakwalwa_Microsoft_Word 순번 = 0; 순번 < Zare_Tarin_bayani[0]; 순번++) kayan_aiki_Harafi(Zare_Tarin_bayani[순번 + 1]);
    return Zare_Tarin_bayani[0];
}
static int Hanyar_shiga(na_ura_mai_kwakwalwa_Microsoft_Word abu_Manazarta, char 결과자료[512]) {
    const na_ura_mai_kwakwalwa_Microsoft_Word *첫째값 = (const na_ura_mai_kwakwalwa_Microsoft_Word *)abu_Manazarta;
    unsigned 사용량 = 0;
    for (na_ura_mai_kwakwalwa_Microsoft_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned Lambar_sirrin_harafi = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] tsari_yanayin_aiki 경로와 호환한다.
        if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; Lambar_sirrin_harafi = 0x10000 + ((Lambar_sirrin_harafi - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdfff) return -22;
        unsigned 개수 = Lambar_sirrin_harafi < 128 ? 1 : Lambar_sirrin_harafi < 2048 ? 2 : Lambar_sirrin_harafi < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = Lambar_sirrin_harafi;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (Lambar_sirrin_harafi >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((Lambar_sirrin_harafi >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_buɗe(na_ura_mai_kwakwalwa_Microsoft_Word Suna, na_ura_mai_kwakwalwa_Microsoft_Word saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango) {
    char 자료위치[512]; int Kuskure = Hanyar_shiga(Suna, 자료위치);
    return (uint32_t)(Kuskure ? Kuskure : 호출(3, (na_ura_mai_kwakwalwa_Microsoft_Word)자료위치, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, 0));
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_Rufe(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki) { return (uint32_t)호출(4, Fayil_Mariki, 0, 0); }
na_ura_mai_kwakwalwa_Microsoft_Word 도구바이트읽기(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_Rubuta_bayit(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki, na_ura_mai_kwakwalwa_Microsoft_Word Daraja) {
    unsigned char 둘째값 = Daraja; return (uint32_t)호출(1, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)&둘째값, 1);
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구읽기(na_ura_mai_kwakwalwa_Microsoft_Word Suna, na_ura_mai_kwakwalwa_Microsoft_Word Zangon_ƙarshe_Tarin_bayani_imel) {
    if (꾸러미사용중) {
        char 자료위치[512]; int Kuskure = Hanyar_shiga(Suna, 자료위치); if (Kuskure) return (uint32_t)Kuskure;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; na_ura_mai_kwakwalwa_Microsoft_Word *목적위치 = (na_ura_mai_kwakwalwa_Microsoft_Word *)Zangon_ƙarshe_Tarin_bayani_imel;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int Fayil_Mariki = 꾸러미사용중 ? -2 : (int32_t)kayan_aiki_buɗe(Suna, 0);
    if (Fayil_Mariki < 0) {
        char 자료위치[512]; int Kuskure = Hanyar_shiga(Suna, 자료위치); if (Kuskure) return (uint32_t)Kuskure;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Suna; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            na_ura_mai_kwakwalwa_Microsoft_Word *목적위치 = (na_ura_mai_kwakwalwa_Microsoft_Word *)Zangon_ƙarshe_Tarin_bayani_imel;
            if (목적위치[0] < 자바클래스들[순번].Girma) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Girma; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].Tarin_bayani[안쪽순번];
            return 자바클래스들[순번].Girma;
        }
        return (uint32_t)Fayil_Mariki;
    }
    na_ura_mai_kwakwalwa_Microsoft_Word *첫째값 = (na_ura_mai_kwakwalwa_Microsoft_Word *)Zangon_ƙarshe_Tarin_bayani_imel;
    intptr_t Girma = 호출(9, Fayil_Mariki, 0, 0), 완료량 = 0;
    if (Girma < 0 || (na_ura_mai_kwakwalwa_Microsoft_Word)Girma > 첫째값[0]) { kayan_aiki_Rufe(Fayil_Mariki); return (uint32_t)(Girma < 0 ? Girma : -27); }
    unsigned char Tarin_bayani_bulo[256];
    while (완료량 < Girma) {
        intptr_t 개수 = 호출(2, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)Tarin_bayani_bulo, Girma - 완료량 < 256 ? Girma - 완료량 : 256);
        if (개수 <= 0) { kayan_aiki_Rufe(Fayil_Mariki); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = Tarin_bayani_bulo[순번];
        완료량 += 개수;
    }
    kayan_aiki_Rufe(Fayil_Mariki); return 완료량;
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_Rubuta(na_ura_mai_kwakwalwa_Microsoft_Word Suna, na_ura_mai_kwakwalwa_Microsoft_Word 원본자료, na_ura_mai_kwakwalwa_Microsoft_Word 항목수) {
    const na_ura_mai_kwakwalwa_Microsoft_Word *첫째값 = (const na_ura_mai_kwakwalwa_Microsoft_Word *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int Fayil_Mariki = (int32_t)kayan_aiki_buɗe(Suna, 577); if (Fayil_Mariki < 0) return (uint32_t)Fayil_Mariki;
    unsigned char Tarin_bayani_bulo[256]; na_ura_mai_kwakwalwa_Microsoft_Word 완료량 = 0;
    while (완료량 < 항목수) {
        na_ura_mai_kwakwalwa_Microsoft_Word 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (na_ura_mai_kwakwalwa_Microsoft_Word 순번 = 0; 순번 < 개수; 순번++) Tarin_bayani_bulo[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)Tarin_bayani_bulo, 개수);
        if (결과 <= 0) { kayan_aiki_Rufe(Fayil_Mariki); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    kayan_aiki_Rufe(Fayil_Mariki); return 항목수;
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_Tubalin_aiki(na_ura_mai_kwakwalwa_Microsoft_Word 색인) {
    static const na_ura_mai_kwakwalwa_Microsoft_Word holoko_Daraja[1] = {0};
    if (색인 >= 8) return (na_ura_mai_kwakwalwa_Microsoft_Word)holoko_Daraja;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (na_ura_mai_kwakwalwa_Microsoft_Word)입력결과, sizeof(입력결과));
    if (개수 < 0) return (na_ura_mai_kwakwalwa_Microsoft_Word)holoko_Daraja;
    na_ura_mai_kwakwalwa_Microsoft_Word *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned Lambar_sirrin_harafi = 입력결과[순번++], 더있음 = Lambar_sirrin_harafi < 128 ? 0 : Lambar_sirrin_harafi >= 0xc2 && Lambar_sirrin_harafi < 0xe0 ? 1 : Lambar_sirrin_harafi < 0xf0 && Lambar_sirrin_harafi >= 0xe0 ? 2 : Lambar_sirrin_harafi >= 0xf0 && Lambar_sirrin_harafi <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) Lambar_sirrin_harafi &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { Lambar_sirrin_harafi = (Lambar_sirrin_harafi << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || Lambar_sirrin_harafi < 최소값 || Lambar_sirrin_harafi > 0x10ffff || (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdfff)) Lambar_sirrin_harafi = 0xfffd;
        if (Lambar_sirrin_harafi >= 65536) { Lambar_sirrin_harafi -= 65536; 결과자료[++항목수] = 0xd800 | (Lambar_sirrin_harafi >> 10); 결과자료[++항목수] = 0xdc00 | (Lambar_sirrin_harafi & 1023); }
        else 결과자료[++항목수] = Lambar_sirrin_harafi;
    }
    결과자료[0] = 항목수; return (na_ura_mai_kwakwalwa_Microsoft_Word)결과자료;
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구분류(void) { return ɓangare_Daraja; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); Harafi(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Fara_Mai_anfani_da_kwamfuta_Shiri(int tsari_yanayin_aiki) {
    ɓangare_Daraja = tsari_yanayin_aiki;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (na_ura_mai_kwakwalwa_Microsoft_Word)첫항목, sizeof(첫항목));
    if (tsari_yanayin_aiki == 2 || (tsari_yanayin_aiki == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = tsari_yanayin_aiki == 2 ? 0 : 1;
        char Fayil_Mashigar_bayanai_Suna[256]; intptr_t Tsawo_Tarin_bayani = 호출(15, 꾸러미인수이동, (na_ura_mai_kwakwalwa_Microsoft_Word)Fayil_Mashigar_bayanai_Suna, sizeof(Fayil_Mashigar_bayanai_Suna));
        if (Tsawo_Tarin_bayani <= 0 || 꾸러미열기(Fayil_Mashigar_bayanai_Suna) < 0) {
            static const char Kuskure[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Kuskure, sizeof(Kuskure) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) Harafi(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Iyali, lambar_kafa; uint32_t imel; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned lambar_kafa) {
    struct 자바주소 첫째값 = {2, (uint16_t)((lambar_kafa << 8) | (lambar_kafa >> 8)), 0x0100007f, {0}}; return 첫째값;
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구전문열기(na_ura_mai_kwakwalwa_Microsoft_Word lambar_kafa) {
    intptr_t Fayil_Mariki = 호출(32, 2, 2, 17); if (Fayil_Mariki < 0) return (uint32_t)Fayil_Mariki;
    struct 자바주소 첫째값 = 전문주소(lambar_kafa);
    첫째값.imel = 0;
    intptr_t Matsayi_Daraja = 호출(33, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값, sizeof(첫째값));
    if (Matsayi_Daraja < 0) { kayan_aiki_Rufe(Fayil_Mariki); return (uint32_t)Matsayi_Daraja; }
    return Fayil_Mariki;
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구전문보내기(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki, na_ura_mai_kwakwalwa_Microsoft_Word lambar_kafa, na_ura_mai_kwakwalwa_Microsoft_Word TSARI_Daraja, na_ura_mai_kwakwalwa_Microsoft_Word Tsawo_Daraja) {
    const na_ura_mai_kwakwalwa_Microsoft_Word *원본주소 = (const na_ura_mai_kwakwalwa_Microsoft_Word *)TSARI_Daraja; unsigned char Tarin_bayani[512];
    if (Tsawo_Daraja > 512 || Tsawo_Daraja > 원본주소[0]) return (uint32_t)-90;
    for (na_ura_mai_kwakwalwa_Microsoft_Word 순번 = 0; 순번 < Tsawo_Daraja; 순번++) Tarin_bayani[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(lambar_kafa);
    return (uint32_t)사용자호출(34, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)Tarin_bayani, Tsawo_Daraja, 0, (na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
na_ura_mai_kwakwalwa_Microsoft_Word 도구전문주소보내기(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki, na_ura_mai_kwakwalwa_Microsoft_Word imel, na_ura_mai_kwakwalwa_Microsoft_Word lambar_kafa, na_ura_mai_kwakwalwa_Microsoft_Word TSARI_Daraja, na_ura_mai_kwakwalwa_Microsoft_Word Tsawo_Daraja) {
    const na_ura_mai_kwakwalwa_Microsoft_Word *원본주소 = (const na_ura_mai_kwakwalwa_Microsoft_Word *)TSARI_Daraja; unsigned char Tarin_bayani[512];
    if (Tsawo_Daraja > 512 || Tsawo_Daraja > 원본주소[0]) return (uint32_t)-90;
    for (na_ura_mai_kwakwalwa_Microsoft_Word 순번 = 0; 순번 < Tsawo_Daraja; 순번++) Tarin_bayani[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(lambar_kafa); 첫째값.imel = 바이트순서뒤집기(imel);
    return (uint32_t)사용자호출(34, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)Tarin_bayani, Tsawo_Daraja, 0, (na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값, sizeof(첫째값));
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_HAƊI(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki, na_ura_mai_kwakwalwa_Microsoft_Word imel, na_ura_mai_kwakwalwa_Microsoft_Word lambar_kafa) {
    struct 자바주소 첫째값 = 전문주소(lambar_kafa); 첫째값.imel = 바이트순서뒤집기(imel);
    uint32_t Tafiyar_da = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - Tafiyar_da) >= 1000) return (uint32_t)-110;
    }
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구전문받기(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki, na_ura_mai_kwakwalwa_Microsoft_Word TSARI_Daraja, na_ura_mai_kwakwalwa_Microsoft_Word 수용량) {
    na_ura_mai_kwakwalwa_Microsoft_Word *Zangon_ƙarshe_imel = (na_ura_mai_kwakwalwa_Microsoft_Word *)TSARI_Daraja; unsigned char Tarin_bayani[512];
    if (수용량 > 512 || Zangon_ƙarshe_imel[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned Tsawo_Tarin_bayani = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)Tarin_bayani, 수용량, 0, (na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값, (na_ura_mai_kwakwalwa_Microsoft_Word)&Tsawo_Tarin_bayani);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) Zangon_ƙarshe_imel[순번 + 1] = Tarin_bayani[순번]; Zangon_ƙarshe_imel[513] = (첫째값.lambar_kafa << 8 | 첫째값.lambar_kafa >> 8) & 65535; Zangon_ƙarshe_imel[514] = 바이트순서뒤집기(첫째값.imel); }
    return (uint32_t)개수;
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구전문접속번호(na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki) {
    struct 자바주소 첫째값; unsigned Tsawo_Tarin_bayani = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Fayil_Mariki, (na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값, (na_ura_mai_kwakwalwa_Microsoft_Word)&Tsawo_Tarin_bayani);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.lambar_kafa << 8 | 첫째값.lambar_kafa >> 8) & 65535);
}
na_ura_mai_kwakwalwa_Microsoft_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
na_ura_mai_kwakwalwa_Microsoft_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
na_ura_mai_kwakwalwa_Microsoft_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
na_ura_mai_kwakwalwa_Microsoft_Word 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
na_ura_mai_kwakwalwa_Microsoft_Word 도구사각형(na_ura_mai_kwakwalwa_Microsoft_Word gamayyar_x, na_ura_mai_kwakwalwa_Microsoft_Word Maɓallin_Y_Mai_tsarawa, na_ura_mai_kwakwalwa_Microsoft_Word 너비값, na_ura_mai_kwakwalwa_Microsoft_Word 높이값, na_ura_mai_kwakwalwa_Microsoft_Word 색상) {
    return (uint32_t)사용자호출(13, gamayyar_x, Maɓallin_Y_Mai_tsarawa, 색상, 너비값, 높이값, 0);
}

na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_watsuwa(na_ura_mai_kwakwalwa_Microsoft_Word Aiki,na_ura_mai_kwakwalwa_Microsoft_Word Fayil_Mariki,na_ura_mai_kwakwalwa_Microsoft_Word Daraja){
    if(Aiki==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(Daraja);
    if(Aiki==1){첫째값.imel=0;intptr_t 반환값=호출(33,Fayil_Mariki,(na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Fayil_Mariki,4,0));}
    if(Aiki==2)return (uint32_t)호출(37,Fayil_Mariki,(na_ura_mai_kwakwalwa_Microsoft_Word)&첫째값,sizeof(첫째값));
    if(Aiki==3)return (uint32_t)호출(39,Fayil_Mariki,0,0);
    if(Aiki==4)return 도구전문접속번호(Fayil_Mariki);
    if(Aiki==5)return (uint32_t)호출(40,Fayil_Mariki,0,0);
    return (uint32_t)-22;
}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_GUI(na_ura_mai_kwakwalwa_Microsoft_Word Aiki,na_ura_mai_kwakwalwa_Microsoft_Word mai_ganewa_Daraja,na_ura_mai_kwakwalwa_Microsoft_Word 첫째값,na_ura_mai_kwakwalwa_Microsoft_Word 둘째값,na_ura_mai_kwakwalwa_Microsoft_Word Lambar_sirrin_harafi,na_ura_mai_kwakwalwa_Microsoft_Word Zangon_ƙarshe_Tarin_bayani){return (uint32_t)사용자호출(20,Aiki,mai_ganewa_Daraja,첫째값,둘째값,Lambar_sirrin_harafi,Zangon_ƙarshe_Tarin_bayani);}
na_ura_mai_kwakwalwa_Microsoft_Word kayan_aiki_GUI_SMS(na_ura_mai_kwakwalwa_Microsoft_Word mai_ganewa_Daraja,na_ura_mai_kwakwalwa_Microsoft_Word TSARI_Daraja,na_ura_mai_kwakwalwa_Microsoft_Word 개수){
    const na_ura_mai_kwakwalwa_Microsoft_Word *원본주소=(const na_ura_mai_kwakwalwa_Microsoft_Word *)TSARI_Daraja;uint32_t Tarin_bayani[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(na_ura_mai_kwakwalwa_Microsoft_Word 순번=0;순번<개수;순번++){unsigned Harafi_Juyar_da_bayanai_zuwa_lamba=원본주소[순번+1];if(Harafi_Juyar_da_bayanai_zuwa_lamba>=0xd800&&Harafi_Juyar_da_bayanai_zuwa_lamba<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;Harafi_Juyar_da_bayanai_zuwa_lamba=0x10000+((Harafi_Juyar_da_bayanai_zuwa_lamba-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;Tarin_bayani[항목수++]=Harafi_Juyar_da_bayanai_zuwa_lamba;}
    return (uint32_t)사용자호출(21,mai_ganewa_Daraja,(na_ura_mai_kwakwalwa_Microsoft_Word)Tarin_bayani,항목수,0,0,0);
}
