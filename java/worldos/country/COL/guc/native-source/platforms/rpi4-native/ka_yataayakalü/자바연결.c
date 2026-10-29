#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 anaajaalaa/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "꾸러미.h"
typedef uintptr_t 기계낱말;
static int akotchiraayanüliee_ajutuu;
static int 꾸러미사용중, 꾸러미인수이동;
static 기계낱말 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, 기계낱말 첫째값, 기계낱말 둘째값, 기계낱말 문자값) {
    return 사용자호출(개수, 첫째값, 둘째값, 문자값, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (기계낱말)자료위치, 개수); }
static void jeerü(unsigned 문자값) {
    unsigned char atijaaya[4]; unsigned 개수 = 0;
    if (문자값 < 128) atijaaya[개수++] = 문자값;
    else if (문자값 < 2048) { atijaaya[개수++] = 0xc0 | (문자값 >> 6); atijaaya[개수++] = 0x80 | (문자값 & 63); }
    else if (문자값 < 65536) { atijaaya[개수++] = 0xe0 | (문자값 >> 12); atijaaya[개수++] = 0x80 | ((문자값 >> 6) & 63); atijaaya[개수++] = 0x80 | (문자값 & 63); }
    else { atijaaya[개수++] = 0xf0 | (문자값 >> 18); atijaaya[개수++] = 0x80 | ((문자값 >> 12) & 63); atijaaya[개수++] = 0x80 | ((문자값 >> 6) & 63); atijaaya[개수++] = 0x80 | (문자값 & 63); }
    바이트들((const char *)atijaaya, 개수);
}
기계낱말 a_yataaya_jeerü(기계낱말 ajutuu) {
    unsigned 문자값 = ajutuu;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (문자값 >= 0xdc00 && 문자값 <= 0xdfff) { jeerü(0x10000 + ((높은부분 - 0xd800) << 10) + 문자값 - 0xdc00); return 1; }
        jeerü(0xfffd);
    }
    if (문자값 >= 0xd800 && 문자값 <= 0xdbff) 대기중짝글자 = 문자값;
    else jeerü(문자값 > 0x10ffff || (문자값 >= 0xdc00 && 문자값 <= 0xdfff) ? 0xfffd : 문자값);
    return 1;
}
기계낱말 도구출력(기계낱말 ajutuu) {
    const 기계낱말 *kaleena_atijaaya = (const 기계낱말 *)ajutuu;
    for (기계낱말 순번 = 0; 순번 < kaleena_atijaaya[0]; 순번++) a_yataaya_jeerü(kaleena_atijaaya[순번 + 1]);
    return kaleena_atijaaya[0];
}
static int wopu_a_ttaaleemüin(기계낱말 객체참조, char 결과자료[512]) {
    const 기계낱말 *첫째값 = (const 기계낱말 *)객체참조;
    unsigned 사용량 = 0;
    for (기계낱말 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned 문자값 = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] 방식 경로와 호환한다.
        if (문자값 >= 0xd800 && 문자값 <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (문자값 >= 0xd800 && 문자값 <= 0xdfff) return -22;
        unsigned 개수 = 문자값 < 128 ? 1 : 문자값 < 2048 ? 2 : 문자값 < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = 문자값;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (문자값 >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((문자값 >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
기계낱말 도구열기(기계낱말 이름, 기계낱말 설정비트) {
    char 자료위치[512]; int ajachitia = wopu_a_ttaaleemüin(이름, 자료위치);
    return (uint32_t)(ajachitia ? ajachitia : 호출(3, (기계낱말)자료위치, 설정비트, 0));
}
기계낱말 a_yataaya_asürülaa(기계낱말 anaajaalaa_aapaaya) { return (uint32_t)호출(4, anaajaalaa_aapaaya, 0, 0); }
기계낱말 도구바이트읽기(기계낱말 anaajaalaa_aapaaya) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, anaajaalaa_aapaaya, (기계낱말)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
기계낱말 a_yataaya_ashajaa_waai(기계낱말 anaajaalaa_aapaaya, 기계낱말 ajutuu) {
    unsigned char 둘째값 = ajutuu; return (uint32_t)호출(1, anaajaalaa_aapaaya, (기계낱말)&둘째값, 1);
}
기계낱말 도구읽기(기계낱말 이름, 기계낱말 jalamüinjatü_atijaaya_ejepüsee) {
    if (꾸러미사용중) {
        char 자료위치[512]; int ajachitia = wopu_a_ttaaleemüin(이름, 자료위치); if (ajachitia) return (uint32_t)ajachitia;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; 기계낱말 *목적위치 = (기계낱말 *)jalamüinjatü_atijaaya_ejepüsee;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int anaajaalaa_aapaaya = 꾸러미사용중 ? -2 : (int32_t)도구열기(이름, 0);
    if (anaajaalaa_aapaaya < 0) {
        char 자료위치[512]; int ajachitia = wopu_a_ttaaleemüin(이름, 자료위치); if (ajachitia) return (uint32_t)ajachitia;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].이름; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            기계낱말 *목적위치 = (기계낱말 *)jalamüinjatü_atijaaya_ejepüsee;
            if (목적위치[0] < 자바클래스들[순번].크기) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].크기; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].atijaaya[안쪽순번];
            return 자바클래스들[순번].크기;
        }
        return (uint32_t)anaajaalaa_aapaaya;
    }
    기계낱말 *첫째값 = (기계낱말 *)jalamüinjatü_atijaaya_ejepüsee;
    intptr_t 크기 = 호출(9, anaajaalaa_aapaaya, 0, 0), 완료량 = 0;
    if (크기 < 0 || (기계낱말)크기 > 첫째값[0]) { a_yataaya_asürülaa(anaajaalaa_aapaaya); return (uint32_t)(크기 < 0 ? 크기 : -27); }
    unsigned char 자료덩이[256];
    while (완료량 < 크기) {
        intptr_t 개수 = 호출(2, anaajaalaa_aapaaya, (기계낱말)자료덩이, 크기 - 완료량 < 256 ? 크기 - 완료량 : 256);
        if (개수 <= 0) { a_yataaya_asürülaa(anaajaalaa_aapaaya); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = 자료덩이[순번];
        완료량 += 개수;
    }
    a_yataaya_asürülaa(anaajaalaa_aapaaya); return 완료량;
}
기계낱말 a_yataaya_ashajaa(기계낱말 이름, 기계낱말 원본자료, 기계낱말 항목수) {
    const 기계낱말 *첫째값 = (const 기계낱말 *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int anaajaalaa_aapaaya = (int32_t)도구열기(이름, 577); if (anaajaalaa_aapaaya < 0) return (uint32_t)anaajaalaa_aapaaya;
    unsigned char 자료덩이[256]; 기계낱말 완료량 = 0;
    while (완료량 < 항목수) {
        기계낱말 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (기계낱말 순번 = 0; 순번 < 개수; 순번++) 자료덩이[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, anaajaalaa_aapaaya, (기계낱말)자료덩이, 개수);
        if (결과 <= 0) { a_yataaya_asürülaa(anaajaalaa_aapaaya); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    a_yataaya_asürülaa(anaajaalaa_aapaaya); return 항목수;
}
기계낱말 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
기계낱말 a_yataaya_ajutuu(기계낱말 색인) {
    static const 기계낱말 빈값[1] = {0};
    if (색인 >= 8) return (기계낱말)빈값;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (기계낱말)입력결과, sizeof(입력결과));
    if (개수 < 0) return (기계낱말)빈값;
    기계낱말 *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned 문자값 = 입력결과[순번++], 더있음 = 문자값 < 128 ? 0 : 문자값 >= 0xc2 && 문자값 < 0xe0 ? 1 : 문자값 < 0xf0 && 문자값 >= 0xe0 ? 2 : 문자값 >= 0xf0 && 문자값 <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) 문자값 &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { 문자값 = (문자값 << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || 문자값 < 최소값 || 문자값 > 0x10ffff || (문자값 >= 0xd800 && 문자값 <= 0xdfff)) 문자값 = 0xfffd;
        if (문자값 >= 65536) { 문자값 -= 65536; 결과자료[++항목수] = 0xd800 | (문자값 >> 10); 결과자료[++항목수] = 0xdc00 | (문자값 & 1023); }
        else 결과자료[++항목수] = 문자값;
    }
    결과자료[0] = 항목수; return (기계낱말)결과자료;
}
기계낱말 도구분류(void) { return akotchiraayanüliee_ajutuu; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); jeerü(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int achuwalaa_ka_yataayakalü_akumajiaa(int 방식) {
    akotchiraayanüliee_ajutuu = 방식;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (기계낱말)첫항목, sizeof(첫항목));
    if (방식 == 2 || (방식 == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = 방식 == 2 ? 0 : 1;
        char 파일이름[256]; intptr_t akaliaa_atijaaya = 호출(15, 꾸러미인수이동, (기계낱말)파일이름, sizeof(파일이름));
        if (akaliaa_atijaaya <= 0 || 꾸러미열기(파일이름) < 0) {
            static const char ajachitia[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(ajachitia, sizeof(ajachitia) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) jeerü(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t 주소계열, 접속번호; uint32_t ejepüsee; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
기계낱말 도구전문열기(기계낱말 접속번호) {
    intptr_t anaajaalaa_aapaaya = 호출(32, 2, 2, 17); if (anaajaalaa_aapaaya < 0) return (uint32_t)anaajaalaa_aapaaya;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.ejepüsee = 0;
    intptr_t jamakua_iparülein_ajutuu = 호출(33, anaajaalaa_aapaaya, (기계낱말)&첫째값, sizeof(첫째값));
    if (jamakua_iparülein_ajutuu < 0) { a_yataaya_asürülaa(anaajaalaa_aapaaya); return (uint32_t)jamakua_iparülein_ajutuu; }
    return anaajaalaa_aapaaya;
}
기계낱말 도구전문보내기(기계낱말 anaajaalaa_aapaaya, 기계낱말 접속번호, 기계낱말 matüriisü_ajutuu, 기계낱말 akaliaa_ajutuu) {
    const 기계낱말 *원본주소 = (const 기계낱말 *)matüriisü_ajutuu; unsigned char atijaaya[512];
    if (akaliaa_ajutuu > 512 || akaliaa_ajutuu > 원본주소[0]) return (uint32_t)-90;
    for (기계낱말 순번 = 0; 순번 < akaliaa_ajutuu; 순번++) atijaaya[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, anaajaalaa_aapaaya, (기계낱말)atijaaya, akaliaa_ajutuu, 0, (기계낱말)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
기계낱말 도구전문주소보내기(기계낱말 anaajaalaa_aapaaya, 기계낱말 ejepüsee, 기계낱말 접속번호, 기계낱말 matüriisü_ajutuu, 기계낱말 akaliaa_ajutuu) {
    const 기계낱말 *원본주소 = (const 기계낱말 *)matüriisü_ajutuu; unsigned char atijaaya[512];
    if (akaliaa_ajutuu > 512 || akaliaa_ajutuu > 원본주소[0]) return (uint32_t)-90;
    for (기계낱말 순번 = 0; 순번 < akaliaa_ajutuu; 순번++) atijaaya[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.ejepüsee = 바이트순서뒤집기(ejepüsee);
    return (uint32_t)사용자호출(34, anaajaalaa_aapaaya, (기계낱말)atijaaya, akaliaa_ajutuu, 0, (기계낱말)&첫째값, sizeof(첫째값));
}
기계낱말 a_yataaya_a_ataa(기계낱말 anaajaalaa_aapaaya, 기계낱말 ejepüsee, 기계낱말 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.ejepüsee = 바이트순서뒤집기(ejepüsee);
    uint32_t 시작 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, anaajaalaa_aapaaya, (기계낱말)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - 시작) >= 1000) return (uint32_t)-110;
    }
}
기계낱말 도구전문받기(기계낱말 anaajaalaa_aapaaya, 기계낱말 matüriisü_ajutuu, 기계낱말 수용량) {
    기계낱말 *jalamüinjatü_ejepüsee = (기계낱말 *)matüriisü_ajutuu; unsigned char atijaaya[512];
    if (수용량 > 512 || jalamüinjatü_ejepüsee[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned akaliaa_atijaaya = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, anaajaalaa_aapaaya, (기계낱말)atijaaya, 수용량, 0, (기계낱말)&첫째값, (기계낱말)&akaliaa_atijaaya);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) jalamüinjatü_ejepüsee[순번 + 1] = atijaaya[순번]; jalamüinjatü_ejepüsee[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; jalamüinjatü_ejepüsee[514] = 바이트순서뒤집기(첫째값.ejepüsee); }
    return (uint32_t)개수;
}
기계낱말 도구전문접속번호(기계낱말 anaajaalaa_aapaaya) {
    struct 자바주소 첫째값; unsigned akaliaa_atijaaya = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, anaajaalaa_aapaaya, (기계낱말)&첫째값, (기계낱말)&akaliaa_atijaaya);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
기계낱말 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
기계낱말 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
기계낱말 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
기계낱말 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
기계낱말 도구사각형(기계낱말 가로좌표, 기계낱말 세로좌표, 기계낱말 너비값, 기계낱말 높이값, 기계낱말 색상) {
    return (uint32_t)사용자호출(13, 가로좌표, 세로좌표, 색상, 너비값, 높이값, 0);
}

기계낱말 a_yataaya_palantüsü(기계낱말 aa_inra_awai,기계낱말 anaajaalaa_aapaaya,기계낱말 ajutuu){
    if(aa_inra_awai==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(ajutuu);
    if(aa_inra_awai==1){첫째값.ejepüsee=0;intptr_t 반환값=호출(33,anaajaalaa_aapaaya,(기계낱말)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,anaajaalaa_aapaaya,4,0));}
    if(aa_inra_awai==2)return (uint32_t)호출(37,anaajaalaa_aapaaya,(기계낱말)&첫째값,sizeof(첫째값));
    if(aa_inra_awai==3)return (uint32_t)호출(39,anaajaalaa_aapaaya,0,0);
    if(aa_inra_awai==4)return 도구전문접속번호(anaajaalaa_aapaaya);
    if(aa_inra_awai==5)return (uint32_t)호출(40,anaajaalaa_aapaaya,0,0);
    return (uint32_t)-22;
}
기계낱말 a_yataaya_po_upünawaa_e_ruushi(기계낱말 aa_inra_awai,기계낱말 식별자,기계낱말 첫째값,기계낱말 둘째값,기계낱말 문자값,기계낱말 jalamüinjatü_atijaaya){return (uint32_t)사용자호출(20,aa_inra_awai,식별자,첫째값,둘째값,문자값,jalamüinjatü_atijaaya);}
기계낱말 도구화면글(기계낱말 식별자,기계낱말 matüriisü_ajutuu,기계낱말 개수){
    const 기계낱말 *원본주소=(const 기계낱말 *)matüriisü_ajutuu;uint32_t atijaaya[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(기계낱말 순번=0;순번<개수;순번++){unsigned jeerü_atijitaalüjiaa=원본주소[순번+1];if(jeerü_atijitaalüjiaa>=0xd800&&jeerü_atijitaalüjiaa<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;jeerü_atijitaalüjiaa=0x10000+((jeerü_atijitaalüjiaa-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;atijaaya[항목수++]=jeerü_atijitaalüjiaa;}
    return (uint32_t)사용자호출(21,식별자,(기계낱말)atijaaya,항목수,0,0,0);
}
