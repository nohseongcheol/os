#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 ini/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "꾸러미.h"
typedef uintptr_t 기계낱말;
static int Ataqatigiivvik_atuutilik;
static int 꾸러미사용중, 꾸러미인수이동;
static 기계낱말 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, 기계낱말 첫째값, 기계낱말 둘째값, 기계낱말 immikkuuqtumut_nalunaikkut) {
    return 사용자호출(개수, 첫째값, 둘째값, immikkuuqtumut_nalunaikkut, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (기계낱말)자료위치, 개수); }
static void immikkuuqtuq(unsigned immikkuuqtumut_nalunaikkut) {
    unsigned char titiqqat[4]; unsigned 개수 = 0;
    if (immikkuuqtumut_nalunaikkut < 128) titiqqat[개수++] = immikkuuqtumut_nalunaikkut;
    else if (immikkuuqtumut_nalunaikkut < 2048) { titiqqat[개수++] = 0xc0 | (immikkuuqtumut_nalunaikkut >> 6); titiqqat[개수++] = 0x80 | (immikkuuqtumut_nalunaikkut & 63); }
    else if (immikkuuqtumut_nalunaikkut < 65536) { titiqqat[개수++] = 0xe0 | (immikkuuqtumut_nalunaikkut >> 12); titiqqat[개수++] = 0x80 | ((immikkuuqtumut_nalunaikkut >> 6) & 63); titiqqat[개수++] = 0x80 | (immikkuuqtumut_nalunaikkut & 63); }
    else { titiqqat[개수++] = 0xf0 | (immikkuuqtumut_nalunaikkut >> 18); titiqqat[개수++] = 0x80 | ((immikkuuqtumut_nalunaikkut >> 12) & 63); titiqqat[개수++] = 0x80 | ((immikkuuqtumut_nalunaikkut >> 6) & 63); titiqqat[개수++] = 0x80 | (immikkuuqtumut_nalunaikkut & 63); }
    바이트들((const char *)titiqqat, 개수);
}
기계낱말 sanajjut_immikkuuqtuq(기계낱말 atuutilik) {
    unsigned immikkuuqtumut_nalunaikkut = atuutilik;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (immikkuuqtumut_nalunaikkut >= 0xdc00 && immikkuuqtumut_nalunaikkut <= 0xdfff) { immikkuuqtuq(0x10000 + ((높은부분 - 0xd800) << 10) + immikkuuqtumut_nalunaikkut - 0xdc00); return 1; }
        immikkuuqtuq(0xfffd);
    }
    if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdbff) 대기중짝글자 = immikkuuqtumut_nalunaikkut;
    else immikkuuqtuq(immikkuuqtumut_nalunaikkut > 0x10ffff || (immikkuuqtumut_nalunaikkut >= 0xdc00 && immikkuuqtumut_nalunaikkut <= 0xdfff) ? 0xfffd : immikkuuqtumut_nalunaikkut);
    return 1;
}
기계낱말 도구출력(기계낱말 atuutilik) {
    const 기계낱말 *qimiaq_titiqqat = (const 기계낱말 *)atuutilik;
    for (기계낱말 순번 = 0; 순번 < qimiaq_titiqqat[0]; 순번++) sanajjut_immikkuuqtuq(qimiaq_titiqqat[순번 + 1]);
    return qimiaq_titiqqat[0];
}
static int aqqut(기계낱말 객체참조, char 결과자료[512]) {
    const 기계낱말 *첫째값 = (const 기계낱말 *)객체참조;
    unsigned 사용량 = 0;
    for (기계낱말 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned immikkuuqtumut_nalunaikkut = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] 방식 경로와 호환한다.
        if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; immikkuuqtumut_nalunaikkut = 0x10000 + ((immikkuuqtumut_nalunaikkut - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdfff) return -22;
        unsigned 개수 = immikkuuqtumut_nalunaikkut < 128 ? 1 : immikkuuqtumut_nalunaikkut < 2048 ? 2 : immikkuuqtumut_nalunaikkut < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = immikkuuqtumut_nalunaikkut;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (immikkuuqtumut_nalunaikkut >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((immikkuuqtumut_nalunaikkut >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
기계낱말 sanajjut_matuirli(기계낱말 atiq, 기계낱말 설정비트) {
    char 자료위치[512]; int tammarniq = aqqut(atiq, 자료위치);
    return (uint32_t)(tammarniq ? tammarniq : 호출(3, (기계낱말)자료위치, 설정비트, 0));
}
기계낱말 sanajjut_matuli(기계낱말 ini_nuuttarut) { return (uint32_t)호출(4, ini_nuuttarut, 0, 0); }
기계낱말 도구바이트읽기(기계낱말 ini_nuuttarut) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, ini_nuuttarut, (기계낱말)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
기계낱말 sanajjut_titiraq_byte(기계낱말 ini_nuuttarut, 기계낱말 atuutilik) {
    unsigned char 둘째값 = atuutilik; return (uint32_t)호출(1, ini_nuuttarut, (기계낱말)&둘째값, 1);
}
기계낱말 도구읽기(기계낱말 atiq, 기계낱말 namunngarvik_titiqqat_turaarut) {
    if (꾸러미사용중) {
        char 자료위치[512]; int tammarniq = aqqut(atiq, 자료위치); if (tammarniq) return (uint32_t)tammarniq;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; 기계낱말 *목적위치 = (기계낱말 *)namunngarvik_titiqqat_turaarut;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int ini_nuuttarut = 꾸러미사용중 ? -2 : (int32_t)sanajjut_matuirli(atiq, 0);
    if (ini_nuuttarut < 0) {
        char 자료위치[512]; int tammarniq = aqqut(atiq, 자료위치); if (tammarniq) return (uint32_t)tammarniq;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].atiq; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            기계낱말 *목적위치 = (기계낱말 *)namunngarvik_titiqqat_turaarut;
            if (목적위치[0] < 자바클래스들[순번].anininga) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].anininga; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].titiqqat[안쪽순번];
            return 자바클래스들[순번].anininga;
        }
        return (uint32_t)ini_nuuttarut;
    }
    기계낱말 *첫째값 = (기계낱말 *)namunngarvik_titiqqat_turaarut;
    intptr_t anininga = 호출(9, ini_nuuttarut, 0, 0), 완료량 = 0;
    if (anininga < 0 || (기계낱말)anininga > 첫째값[0]) { sanajjut_matuli(ini_nuuttarut); return (uint32_t)(anininga < 0 ? anininga : -27); }
    unsigned char titiqqat_sapummili[256];
    while (완료량 < anininga) {
        intptr_t 개수 = 호출(2, ini_nuuttarut, (기계낱말)titiqqat_sapummili, anininga - 완료량 < 256 ? anininga - 완료량 : 256);
        if (개수 <= 0) { sanajjut_matuli(ini_nuuttarut); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = titiqqat_sapummili[순번];
        완료량 += 개수;
    }
    sanajjut_matuli(ini_nuuttarut); return 완료량;
}
기계낱말 sanajjut_titiraq(기계낱말 atiq, 기계낱말 원본자료, 기계낱말 항목수) {
    const 기계낱말 *첫째값 = (const 기계낱말 *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int ini_nuuttarut = (int32_t)sanajjut_matuirli(atiq, 577); if (ini_nuuttarut < 0) return (uint32_t)ini_nuuttarut;
    unsigned char titiqqat_sapummili[256]; 기계낱말 완료량 = 0;
    while (완료량 < 항목수) {
        기계낱말 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (기계낱말 순번 = 0; 순번 < 개수; 순번++) titiqqat_sapummili[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, ini_nuuttarut, (기계낱말)titiqqat_sapummili, 개수);
        if (결과 <= 0) { sanajjut_matuli(ini_nuuttarut); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    sanajjut_matuli(ini_nuuttarut); return 항목수;
}
기계낱말 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
기계낱말 sanajjut_aturniqarnirainiq(기계낱말 색인) {
    static const 기계낱말 빈값[1] = {0};
    if (색인 >= 8) return (기계낱말)빈값;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (기계낱말)입력결과, sizeof(입력결과));
    if (개수 < 0) return (기계낱말)빈값;
    기계낱말 *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned immikkuuqtumut_nalunaikkut = 입력결과[순번++], 더있음 = immikkuuqtumut_nalunaikkut < 128 ? 0 : immikkuuqtumut_nalunaikkut >= 0xc2 && immikkuuqtumut_nalunaikkut < 0xe0 ? 1 : immikkuuqtumut_nalunaikkut < 0xf0 && immikkuuqtumut_nalunaikkut >= 0xe0 ? 2 : immikkuuqtumut_nalunaikkut >= 0xf0 && immikkuuqtumut_nalunaikkut <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) immikkuuqtumut_nalunaikkut &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { immikkuuqtumut_nalunaikkut = (immikkuuqtumut_nalunaikkut << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || immikkuuqtumut_nalunaikkut < 최소값 || immikkuuqtumut_nalunaikkut > 0x10ffff || (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdfff)) immikkuuqtumut_nalunaikkut = 0xfffd;
        if (immikkuuqtumut_nalunaikkut >= 65536) { immikkuuqtumut_nalunaikkut -= 65536; 결과자료[++항목수] = 0xd800 | (immikkuuqtumut_nalunaikkut >> 10); 결과자료[++항목수] = 0xdc00 | (immikkuuqtumut_nalunaikkut & 1023); }
        else 결과자료[++항목수] = immikkuuqtumut_nalunaikkut;
    }
    결과자료[0] = 항목수; return (기계낱말)결과자료;
}
기계낱말 도구분류(void) { return Ataqatigiivvik_atuutilik; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); immikkuuqtuq(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int pigiarli_atuqtuq_pilirijjut(int 방식) {
    Ataqatigiivvik_atuutilik = 방식;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (기계낱말)첫항목, sizeof(첫항목));
    if (방식 == 2 || (방식 == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = 방식 == 2 ? 0 : 1;
        char ini_Iliniku_atiq[256]; intptr_t takininga_titiqqat = 호출(15, 꾸러미인수이동, (기계낱말)ini_Iliniku_atiq, sizeof(ini_Iliniku_atiq));
        if (takininga_titiqqat <= 0 || 꾸러미열기(ini_Iliniku_atiq) < 0) {
            static const char tammarniq[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(tammarniq, sizeof(tammarniq) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) immikkuuqtuq(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t illumiuqatigiit, 접속번호; uint32_t turaarut; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
기계낱말 도구전문열기(기계낱말 접속번호) {
    intptr_t ini_nuuttarut = 호출(32, 2, 2, 17); if (ini_nuuttarut < 0) return (uint32_t)ini_nuuttarut;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.turaarut = 0;
    intptr_t qanuilinganiq_atuutilik = 호출(33, ini_nuuttarut, (기계낱말)&첫째값, sizeof(첫째값));
    if (qanuilinganiq_atuutilik < 0) { sanajjut_matuli(ini_nuuttarut); return (uint32_t)qanuilinganiq_atuutilik; }
    return ini_nuuttarut;
}
기계낱말 도구전문보내기(기계낱말 ini_nuuttarut, 기계낱말 접속번호, 기계낱말 array_atuutilik, 기계낱말 takininga_atuutilik) {
    const 기계낱말 *원본주소 = (const 기계낱말 *)array_atuutilik; unsigned char titiqqat[512];
    if (takininga_atuutilik > 512 || takininga_atuutilik > 원본주소[0]) return (uint32_t)-90;
    for (기계낱말 순번 = 0; 순번 < takininga_atuutilik; 순번++) titiqqat[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, ini_nuuttarut, (기계낱말)titiqqat, takininga_atuutilik, 0, (기계낱말)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
기계낱말 도구전문주소보내기(기계낱말 ini_nuuttarut, 기계낱말 turaarut, 기계낱말 접속번호, 기계낱말 array_atuutilik, 기계낱말 takininga_atuutilik) {
    const 기계낱말 *원본주소 = (const 기계낱말 *)array_atuutilik; unsigned char titiqqat[512];
    if (takininga_atuutilik > 512 || takininga_atuutilik > 원본주소[0]) return (uint32_t)-90;
    for (기계낱말 순번 = 0; 순번 < takininga_atuutilik; 순번++) titiqqat[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.turaarut = 바이트순서뒤집기(turaarut);
    return (uint32_t)사용자호출(34, ini_nuuttarut, (기계낱말)titiqqat, takininga_atuutilik, 0, (기계낱말)&첫째값, sizeof(첫째값));
}
기계낱말 sanajjut_kasurli(기계낱말 ini_nuuttarut, 기계낱말 turaarut, 기계낱말 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.turaarut = 바이트순서뒤집기(turaarut);
    uint32_t 시작 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, ini_nuuttarut, (기계낱말)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - 시작) >= 1000) return (uint32_t)-110;
    }
}
기계낱말 도구전문받기(기계낱말 ini_nuuttarut, 기계낱말 array_atuutilik, 기계낱말 수용량) {
    기계낱말 *namunngarvik_turaarut = (기계낱말 *)array_atuutilik; unsigned char titiqqat[512];
    if (수용량 > 512 || namunngarvik_turaarut[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned takininga_titiqqat = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, ini_nuuttarut, (기계낱말)titiqqat, 수용량, 0, (기계낱말)&첫째값, (기계낱말)&takininga_titiqqat);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) namunngarvik_turaarut[순번 + 1] = titiqqat[순번]; namunngarvik_turaarut[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; namunngarvik_turaarut[514] = 바이트순서뒤집기(첫째값.turaarut); }
    return (uint32_t)개수;
}
기계낱말 도구전문접속번호(기계낱말 ini_nuuttarut) {
    struct 자바주소 첫째값; unsigned takininga_titiqqat = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, ini_nuuttarut, (기계낱말)&첫째값, (기계낱말)&takininga_titiqqat);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
기계낱말 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
기계낱말 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
기계낱말 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
기계낱말 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
기계낱말 도구사각형(기계낱말 가로좌표, 기계낱말 세로좌표, 기계낱말 너비값, 기계낱말 높이값, 기계낱말 색상) {
    return (uint32_t)사용자호출(13, 가로좌표, 세로좌표, 색상, 너비값, 높이값, 0);
}

기계낱말 sanajjut_ingirrania_aulataup(기계낱말 sugiarut,기계낱말 ini_nuuttarut,기계낱말 atuutilik){
    if(sugiarut==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(atuutilik);
    if(sugiarut==1){첫째값.turaarut=0;intptr_t 반환값=호출(33,ini_nuuttarut,(기계낱말)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,ini_nuuttarut,4,0));}
    if(sugiarut==2)return (uint32_t)호출(37,ini_nuuttarut,(기계낱말)&첫째값,sizeof(첫째값));
    if(sugiarut==3)return (uint32_t)호출(39,ini_nuuttarut,0,0);
    if(sugiarut==4)return 도구전문접속번호(ini_nuuttarut);
    if(sugiarut==5)return (uint32_t)호출(40,ini_nuuttarut,0,0);
    return (uint32_t)-22;
}
기계낱말 sanajjut_GUI(기계낱말 sugiarut,기계낱말 식별자,기계낱말 첫째값,기계낱말 둘째값,기계낱말 immikkuuqtumut_nalunaikkut,기계낱말 namunngarvik_titiqqat){return (uint32_t)사용자호출(20,sugiarut,식별자,첫째값,둘째값,immikkuuqtumut_nalunaikkut,namunngarvik_titiqqat);}
기계낱말 sanajjut_GUI_titiqqaq(기계낱말 식별자,기계낱말 array_atuutilik,기계낱말 개수){
    const 기계낱말 *원본주소=(const 기계낱말 *)array_atuutilik;uint32_t titiqqat[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(기계낱말 순번=0;순번<개수;순번++){unsigned immikkuuqtuq_tukiniktiri=원본주소[순번+1];if(immikkuuqtuq_tukiniktiri>=0xd800&&immikkuuqtuq_tukiniktiri<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;immikkuuqtuq_tukiniktiri=0x10000+((immikkuuqtuq_tukiniktiri-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;titiqqat[항목수++]=immikkuuqtuq_tukiniktiri;}
    return (uint32_t)사용자호출(21,식별자,(기계낱말)titiqqat,항목수,0,0,0);
}
