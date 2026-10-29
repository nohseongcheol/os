#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Kartelë/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "grupoj.h"
typedef uintptr_t makinë_Word;
static int kategori_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static makinë_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned njësi_COUNT, makinë_Word 첫째값, makinë_Word SECOND_VALUE, makinë_Word kodi_i_karakterit) {
    return 사용자호출(njësi_COUNT, 첫째값, SECOND_VALUE, kodi_i_karakterit, 0, 0, 0);
}
static void 바이트들(const char *të_dhëna_pozicioni, size_t njësi_COUNT) { 호출(1, 1, (makinë_Word)të_dhëna_pozicioni, njësi_COUNT); }
static void karakter(unsigned kodi_i_karakterit) {
    unsigned char të_dhëna[4]; unsigned njësi_COUNT = 0;
    if (kodi_i_karakterit < 128) të_dhëna[njësi_COUNT++] = kodi_i_karakterit;
    else if (kodi_i_karakterit < 2048) { të_dhëna[njësi_COUNT++] = 0xc0 | (kodi_i_karakterit >> 6); të_dhëna[njësi_COUNT++] = 0x80 | (kodi_i_karakterit & 63); }
    else if (kodi_i_karakterit < 65536) { të_dhëna[njësi_COUNT++] = 0xe0 | (kodi_i_karakterit >> 12); të_dhëna[njësi_COUNT++] = 0x80 | ((kodi_i_karakterit >> 6) & 63); të_dhëna[njësi_COUNT++] = 0x80 | (kodi_i_karakterit & 63); }
    else { të_dhëna[njësi_COUNT++] = 0xf0 | (kodi_i_karakterit >> 18); të_dhëna[njësi_COUNT++] = 0x80 | ((kodi_i_karakterit >> 12) & 63); të_dhëna[njësi_COUNT++] = 0x80 | ((kodi_i_karakterit >> 6) & 63); të_dhëna[njësi_COUNT++] = 0x80 | (kodi_i_karakterit & 63); }
    바이트들((const char *)të_dhëna, njësi_COUNT);
}
makinë_Word vegël_karakter(makinë_Word VALUE) {
    unsigned kodi_i_karakterit = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kodi_i_karakterit >= 0xdc00 && kodi_i_karakterit <= 0xdfff) { karakter(0x10000 + ((높은부분 - 0xd800) << 10) + kodi_i_karakterit - 0xdc00); return 1; }
        karakter(0xfffd);
    }
    if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdbff) 대기중짝글자 = kodi_i_karakterit;
    else karakter(kodi_i_karakterit > 0x10ffff || (kodi_i_karakterit >= 0xdc00 && kodi_i_karakterit <= 0xdfff) ? 0xfffd : kodi_i_karakterit);
    return 1;
}
makinë_Word 도구출력(makinë_Word VALUE) {
    const makinë_Word *varg_të_dhëna = (const makinë_Word *)VALUE;
    for (makinë_Word 순번 = 0; 순번 < varg_të_dhëna[0]; 순번++) vegël_karakter(varg_të_dhëna[순번 + 1]);
    return varg_të_dhëna[0];
}
static int POZICIONI(makinë_Word objekt_Referencë, char llogaritje_të_dhëna[512]) {
    const makinë_Word *첫째값 = (const makinë_Word *)objekt_Referencë;
    unsigned 사용량 = 0;
    for (makinë_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kodi_i_karakterit = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metoda_MODE 경로와 호환한다.
        if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kodi_i_karakterit = 0x10000 + ((kodi_i_karakterit - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdfff) return -22;
        unsigned njësi_COUNT = kodi_i_karakterit < 128 ? 1 : kodi_i_karakterit < 2048 ? 2 : kodi_i_karakterit < 65536 ? 3 : 4;
        if (사용량 + njësi_COUNT > 511) return -36;
        if (njësi_COUNT == 1) llogaritje_të_dhëna[사용량++] = kodi_i_karakterit;
        else {
            llogaritje_të_dhëna[사용량++] = (njësi_COUNT == 2 ? 0xc0 : njësi_COUNT == 3 ? 0xe0 : 0xf0) | (kodi_i_karakterit >> (6 * (njësi_COUNT - 1)));
            for (unsigned 안쪽순번 = njësi_COUNT - 1; 안쪽순번; 안쪽순번--) llogaritje_të_dhëna[사용량++] = 0x80 | ((kodi_i_karakterit >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    llogaritje_të_dhëna[사용량] = 0; return 사용량 ? 0 : -22;
}
makinë_Word vegël_hap(makinë_Word Emër, makinë_Word konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond) {
    char të_dhëna_pozicioni[512]; int GABIM = POZICIONI(Emër, të_dhëna_pozicioni);
    return (uint32_t)(GABIM ? GABIM : 호출(3, (makinë_Word)të_dhëna_pozicioni, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, 0));
}
makinë_Word vegël_mbyll(makinë_Word skedar_dorezë) { return (uint32_t)호출(4, skedar_dorezë, 0, 0); }
makinë_Word 도구바이트읽기(makinë_Word skedar_dorezë) {
    unsigned char SECOND_VALUE; intptr_t njësi_COUNT = 호출(2, skedar_dorezë, (makinë_Word)&SECOND_VALUE, 1);
    return (uint32_t)(njësi_COUNT == 1 ? SECOND_VALUE : njësi_COUNT == 0 ? 256 : njësi_COUNT);
}
makinë_Word vegël_shkruaj_bajt(makinë_Word skedar_dorezë, makinë_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, skedar_dorezë, (makinë_Word)&SECOND_VALUE, 1);
}
makinë_Word 도구읽기(makinë_Word Emër, makinë_Word vendmbërritje_të_dhëna_email) {
    if (꾸러미사용중) {
        char të_dhëna_pozicioni[512]; int GABIM = POZICIONI(Emër, të_dhëna_pozicioni); if (GABIM) return (uint32_t)GABIM;
        unsigned njësi_COUNT = 0; while (të_dhëna_pozicioni[njësi_COUNT]) njësi_COUNT++;
        if (njësi_COUNT >= 6) for (unsigned 순번 = 0; 순번 < njësi_COUNT - 6; 순번++) if (të_dhëna_pozicioni[순번] == '.') të_dhëna_pozicioni[순번] = '/';
        unsigned char 바이트들[16384]; makinë_Word *vendmbërritje_VALUE_pozicioni = (makinë_Word *)vendmbërritje_të_dhëna_email;
        int RECEIVED_COUNT = 꾸러미읽기(të_dhëna_pozicioni, 바이트들, vendmbërritje_VALUE_pozicioni[0] < sizeof(바이트들) ? vendmbërritje_VALUE_pozicioni[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) vendmbërritje_VALUE_pozicioni[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int skedar_dorezë = 꾸러미사용중 ? -2 : (int32_t)vegël_hap(Emër, 0);
    if (skedar_dorezë < 0) {
        char të_dhëna_pozicioni[512]; int GABIM = POZICIONI(Emër, të_dhëna_pozicioni); if (GABIM) return (uint32_t)GABIM;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Tjetër_OFFSET = 자바클래스들[순번].Emër; unsigned 안쪽순번 = 0;
            while (të_dhëna_pozicioni[안쪽순번] && të_dhëna_pozicioni[안쪽순번] == Tjetër_OFFSET[안쪽순번]) 안쪽순번++;
            if (të_dhëna_pozicioni[안쪽순번] || Tjetër_OFFSET[안쪽순번]) continue;
            makinë_Word *vendmbërritje_VALUE_pozicioni = (makinë_Word *)vendmbërritje_të_dhëna_email;
            if (vendmbërritje_VALUE_pozicioni[0] < 자바클래스들[순번].Madhësi) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Madhësi; 안쪽순번++) vendmbërritje_VALUE_pozicioni[안쪽순번 + 1] = 자바클래스들[순번].të_dhëna[안쪽순번];
            return 자바클래스들[순번].Madhësi;
        }
        return (uint32_t)skedar_dorezë;
    }
    makinë_Word *첫째값 = (makinë_Word *)vendmbërritje_të_dhëna_email;
    intptr_t Madhësi = 호출(9, skedar_dorezë, 0, 0), 완료량 = 0;
    if (Madhësi < 0 || (makinë_Word)Madhësi > 첫째값[0]) { vegël_mbyll(skedar_dorezë); return (uint32_t)(Madhësi < 0 ? Madhësi : -27); }
    unsigned char të_dhëna_bllokoj[256];
    while (완료량 < Madhësi) {
        intptr_t njësi_COUNT = 호출(2, skedar_dorezë, (makinë_Word)të_dhëna_bllokoj, Madhësi - 완료량 < 256 ? Madhësi - 완료량 : 256);
        if (njësi_COUNT <= 0) { vegël_mbyll(skedar_dorezë); return (uint32_t)(njësi_COUNT ? njësi_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < njësi_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = të_dhëna_bllokoj[순번];
        완료량 += njësi_COUNT;
    }
    vegël_mbyll(skedar_dorezë); return 완료량;
}
makinë_Word vegël_shkruaj(makinë_Word Emër, makinë_Word 원본자료, makinë_Word futje_COUNT) {
    const makinë_Word *첫째값 = (const makinë_Word *)원본자료;
    if (futje_COUNT > 첫째값[0] || futje_COUNT > 16384) return (uint32_t)-27;
    int skedar_dorezë = (int32_t)vegël_hap(Emër, 577); if (skedar_dorezë < 0) return (uint32_t)skedar_dorezë;
    unsigned char të_dhëna_bllokoj[256]; makinë_Word 완료량 = 0;
    while (완료량 < futje_COUNT) {
        makinë_Word njësi_COUNT = futje_COUNT - 완료량 < 256 ? futje_COUNT - 완료량 : 256;
        for (makinë_Word 순번 = 0; 순번 < njësi_COUNT; 순번++) të_dhëna_bllokoj[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t llogaritje = 호출(1, skedar_dorezë, (makinë_Word)të_dhëna_bllokoj, njësi_COUNT);
        if (llogaritje <= 0) { vegël_mbyll(skedar_dorezë); return (uint32_t)(llogaritje ? llogaritje : -5); }
        완료량 += llogaritje;
    }
    vegël_mbyll(skedar_dorezë); return futje_COUNT;
}
makinë_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
makinë_Word vegël_argument(makinë_Word LOOKUP_INDEX) {
    static const makinë_Word bosh_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (makinë_Word)bosh_VALUE;
    unsigned char 입력결과[256]; intptr_t njësi_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *të_dhëna_pozicioni = 꾸러미진입클래스(); njësi_COUNT = 0; while (të_dhëna_pozicioni[njësi_COUNT] && njësi_COUNT < 255) { 입력결과[njësi_COUNT] = të_dhëna_pozicioni[njësi_COUNT]; njësi_COUNT++; } }
    else njësi_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (makinë_Word)입력결과, sizeof(입력결과));
    if (njësi_COUNT < 0) return (makinë_Word)bosh_VALUE;
    makinë_Word *llogaritje_të_dhëna = 전달인수[LOOKUP_INDEX]; unsigned futje_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < njësi_COUNT;) {
        unsigned kodi_i_karakterit = 입력결과[순번++], 더있음 = kodi_i_karakterit < 128 ? 0 : kodi_i_karakterit >= 0xc2 && kodi_i_karakterit < 0xe0 ? 1 : kodi_i_karakterit < 0xf0 && kodi_i_karakterit >= 0xe0 ? 2 : kodi_i_karakterit >= 0xf0 && kodi_i_karakterit <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > njësi_COUNT) { llogaritje_të_dhëna[++futje_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kodi_i_karakterit &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kodi_i_karakterit = (kodi_i_karakterit << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kodi_i_karakterit < 최소값 || kodi_i_karakterit > 0x10ffff || (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdfff)) kodi_i_karakterit = 0xfffd;
        if (kodi_i_karakterit >= 65536) { kodi_i_karakterit -= 65536; llogaritje_të_dhëna[++futje_COUNT] = 0xd800 | (kodi_i_karakterit >> 10); llogaritje_të_dhëna[++futje_COUNT] = 0xdc00 | (kodi_i_karakterit & 1023); }
        else llogaritje_të_dhëna[++futje_COUNT] = kodi_i_karakterit;
    }
    llogaritje_të_dhëna[0] = futje_COUNT; return (makinë_Word)llogaritje_të_dhëna;
}
makinë_Word 도구분류(void) { return kategori_VALUE; }
void 커널중단(const char *알림문) {
    const char *të_dhëna_pozicioni = 알림문; while (*të_dhëna_pozicioni) të_dhëna_pozicioni++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, të_dhëna_pozicioni - 알림문); karakter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int nis_përdorues_program(int metoda_MODE) {
    kategori_VALUE = metoda_MODE;
    unsigned char 첫항목[256]; intptr_t njësi_COUNT = 호출(15, 0, (makinë_Word)첫항목, sizeof(첫항목));
    if (metoda_MODE == 2 || (metoda_MODE == 1 && njësi_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metoda_MODE == 2 ? 0 : 1;
        char skedar_futje_emër[256]; intptr_t gjatësi_të_dhëna = 호출(15, 꾸러미인수이동, (makinë_Word)skedar_futje_emër, sizeof(skedar_futje_emër));
        if (gjatësi_të_dhëna <= 0 || 꾸러미열기(skedar_futje_emër) < 0) {
            static const char GABIM[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(GABIM, sizeof(GABIM) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int llogaritje = 자바진입();
    if (대기중짝글자) karakter(0xfffd);
    return llogaritje;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Familja, numri_i_portës; uint32_t email; unsigned char 영값[8]; };
static struct 자바주소 UDP_email(unsigned numri_i_portës) {
    struct 자바주소 첫째값 = {2, (uint16_t)((numri_i_portës << 8) | (numri_i_portës >> 8)), 0x0100007f, {0}}; return 첫째값;
}
makinë_Word vegël_UDP_hap(makinë_Word numri_i_portës) {
    intptr_t skedar_dorezë = 호출(32, 2, 2, 17); if (skedar_dorezë < 0) return (uint32_t)skedar_dorezë;
    struct 자바주소 첫째값 = UDP_email(numri_i_portës);
    첫째값.email = 0;
    intptr_t status_VALUE = 호출(33, skedar_dorezë, (makinë_Word)&첫째값, sizeof(첫째값));
    if (status_VALUE < 0) { vegël_mbyll(skedar_dorezë); return (uint32_t)status_VALUE; }
    return skedar_dorezë;
}
makinë_Word vegël_UDP_dërgoj(makinë_Word skedar_dorezë, makinë_Word numri_i_portës, makinë_Word ARRAY_VALUE, makinë_Word gjatësi_VALUE) {
    const makinë_Word *원본주소 = (const makinë_Word *)ARRAY_VALUE; unsigned char të_dhëna[512];
    if (gjatësi_VALUE > 512 || gjatësi_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (makinë_Word 순번 = 0; 순번 < gjatësi_VALUE; 순번++) të_dhëna[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_email(numri_i_portës);
    return (uint32_t)사용자호출(34, skedar_dorezë, (makinë_Word)të_dhëna, gjatësi_VALUE, 0, (makinë_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t njësi_COUNT) { return (njësi_COUNT>>24)|((njësi_COUNT>>8)&0xff00)|((njësi_COUNT<<8)&0xff0000)|(njësi_COUNT<<24); }
makinë_Word vegël_UDP_dërgoj_email(makinë_Word skedar_dorezë, makinë_Word email, makinë_Word numri_i_portës, makinë_Word ARRAY_VALUE, makinë_Word gjatësi_VALUE) {
    const makinë_Word *원본주소 = (const makinë_Word *)ARRAY_VALUE; unsigned char të_dhëna[512];
    if (gjatësi_VALUE > 512 || gjatësi_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (makinë_Word 순번 = 0; 순번 < gjatësi_VALUE; 순번++) të_dhëna[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_email(numri_i_portës); 첫째값.email = 바이트순서뒤집기(email);
    return (uint32_t)사용자호출(34, skedar_dorezë, (makinë_Word)të_dhëna, gjatësi_VALUE, 0, (makinë_Word)&첫째값, sizeof(첫째값));
}
makinë_Word vegël_Lidh(makinë_Word skedar_dorezë, makinë_Word email, makinë_Word numri_i_portës) {
    struct 자바주소 첫째값 = UDP_email(numri_i_portës); 첫째값.email = 바이트순서뒤집기(email);
    uint32_t Ekzekuto = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t llogaritje = 호출(37, skedar_dorezë, (makinë_Word)&첫째값, sizeof(첫째값));
        if (llogaritje != -115) return (uint32_t)llogaritje;
        if ((uint32_t)(호출(7, 0, 0, 0) - Ekzekuto) >= 1000) return (uint32_t)-110;
    }
}
makinë_Word 도구전문받기(makinë_Word skedar_dorezë, makinë_Word ARRAY_VALUE, makinë_Word 수용량) {
    makinë_Word *vendmbërritje_email = (makinë_Word *)ARRAY_VALUE; unsigned char të_dhëna[512];
    if (수용량 > 512 || vendmbërritje_email[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned gjatësi_të_dhëna = sizeof(첫째값);
    intptr_t njësi_COUNT = 사용자호출(35, skedar_dorezë, (makinë_Word)të_dhëna, 수용량, 0, (makinë_Word)&첫째값, (makinë_Word)&gjatësi_të_dhëna);
    if (njësi_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < njësi_COUNT; 순번++) vendmbërritje_email[순번 + 1] = të_dhëna[순번]; vendmbërritje_email[513] = (첫째값.numri_i_portës << 8 | 첫째값.numri_i_portës >> 8) & 65535; vendmbërritje_email[514] = 바이트순서뒤집기(첫째값.email); }
    return (uint32_t)njësi_COUNT;
}
makinë_Word vegël_UDP_portë(makinë_Word skedar_dorezë) {
    struct 자바주소 첫째값; unsigned gjatësi_të_dhëna = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, skedar_dorezë, (makinë_Word)&첫째값, (makinë_Word)&gjatësi_të_dhëna);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.numri_i_portës << 8 | 첫째값.numri_i_portës >> 8) & 65535);
}
makinë_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
makinë_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
makinë_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
makinë_Word vegël_figura_Prit(void) { return (uint32_t)화면키기다리기(); }
makinë_Word 도구사각형(makinë_Word koordinata_x, makinë_Word Y_koordinatë, makinë_Word 너비값, makinë_Word 높이값, makinë_Word 색상) {
    return (uint32_t)사용자호출(13, koordinata_x, Y_koordinatë, 색상, 너비값, 높이값, 0);
}

makinë_Word vegël_Stream(makinë_Word Veprim,makinë_Word skedar_dorezë,makinë_Word VALUE){
    if(Veprim==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_email(VALUE);
    if(Veprim==1){첫째값.email=0;intptr_t 반환값=호출(33,skedar_dorezë,(makinë_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,skedar_dorezë,4,0));}
    if(Veprim==2)return (uint32_t)호출(37,skedar_dorezë,(makinë_Word)&첫째값,sizeof(첫째값));
    if(Veprim==3)return (uint32_t)호출(39,skedar_dorezë,0,0);
    if(Veprim==4)return vegël_UDP_portë(skedar_dorezë);
    if(Veprim==5)return (uint32_t)호출(40,skedar_dorezë,0,0);
    return (uint32_t)-22;
}
makinë_Word vegël_GUI(makinë_Word Veprim,makinë_Word identifikues_VALUE,makinë_Word 첫째값,makinë_Word SECOND_VALUE,makinë_Word kodi_i_karakterit,makinë_Word vendmbërritje_të_dhëna){return (uint32_t)사용자호출(20,Veprim,identifikues_VALUE,첫째값,SECOND_VALUE,kodi_i_karakterit,vendmbërritje_të_dhëna);}
makinë_Word vegël_GUI_SMS(makinë_Word identifikues_VALUE,makinë_Word ARRAY_VALUE,makinë_Word njësi_COUNT){
    const makinë_Word *원본주소=(const makinë_Word *)ARRAY_VALUE;uint32_t të_dhëna[127];unsigned futje_COUNT=0;
    if(njësi_COUNT>원본주소[0])return (uint32_t)-22;
    for(makinë_Word 순번=0;순번<njësi_COUNT;순번++){unsigned karakter_enkodim=원본주소[순번+1];if(karakter_enkodim>=0xd800&&karakter_enkodim<=0xdbff&&순번+1<njësi_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;karakter_enkodim=0x10000+((karakter_enkodim-0xd800)<<10)+낮은값-0xdc00;}if(futje_COUNT==127)return (uint32_t)-22;të_dhëna[futje_COUNT++]=karakter_enkodim;}
    return (uint32_t)사용자호출(21,identifikues_VALUE,(makinë_Word)të_dhëna,futje_COUNT,0,0,0);
}
