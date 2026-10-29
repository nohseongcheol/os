#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Faýl/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "toplum.h"
typedef uintptr_t kompýuter_Söz;
static int kategoriýa_baha;
static int 꾸러미사용중, 꾸러미인수이동;
static kompýuter_Söz 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, kompýuter_Söz 첫째값, kompýuter_Söz 둘째값, kompýuter_Söz nyşanyň_kody) {
    return 사용자호출(개수, 첫째값, 둘째값, nyşanyň_kody, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (kompýuter_Söz)자료위치, 개수); }
static void nyşan_a5317f02(unsigned nyşanyň_kody) {
    unsigned char maglumat[4]; unsigned 개수 = 0;
    if (nyşanyň_kody < 128) maglumat[개수++] = nyşanyň_kody;
    else if (nyşanyň_kody < 2048) { maglumat[개수++] = 0xc0 | (nyşanyň_kody >> 6); maglumat[개수++] = 0x80 | (nyşanyň_kody & 63); }
    else if (nyşanyň_kody < 65536) { maglumat[개수++] = 0xe0 | (nyşanyň_kody >> 12); maglumat[개수++] = 0x80 | ((nyşanyň_kody >> 6) & 63); maglumat[개수++] = 0x80 | (nyşanyň_kody & 63); }
    else { maglumat[개수++] = 0xf0 | (nyşanyň_kody >> 18); maglumat[개수++] = 0x80 | ((nyşanyň_kody >> 12) & 63); maglumat[개수++] = 0x80 | ((nyşanyň_kody >> 6) & 63); maglumat[개수++] = 0x80 | (nyşanyň_kody & 63); }
    바이트들((const char *)maglumat, 개수);
}
kompýuter_Söz gural_nyşan(kompýuter_Söz baha) {
    unsigned nyşanyň_kody = baha;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (nyşanyň_kody >= 0xdc00 && nyşanyň_kody <= 0xdfff) { nyşan_a5317f02(0x10000 + ((높은부분 - 0xd800) << 10) + nyşanyň_kody - 0xdc00); return 1; }
        nyşan_a5317f02(0xfffd);
    }
    if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdbff) 대기중짝글자 = nyşanyň_kody;
    else nyşan_a5317f02(nyşanyň_kody > 0x10ffff || (nyşanyň_kody >= 0xdc00 && nyşanyň_kody <= 0xdfff) ? 0xfffd : nyşanyň_kody);
    return 1;
}
kompýuter_Söz 도구출력(kompýuter_Söz baha) {
    const kompýuter_Söz *setir_maglumat = (const kompýuter_Söz *)baha;
    for (kompýuter_Söz 순번 = 0; 순번 < setir_maglumat[0]; 순번++) gural_nyşan(setir_maglumat[순번 + 1]);
    return setir_maglumat[0];
}
static int Ýol(kompýuter_Söz obýekt_Salgylanma, char 결과자료[512]) {
    const kompýuter_Söz *첫째값 = (const kompýuter_Söz *)obýekt_Salgylanma;
    unsigned 사용량 = 0;
    for (kompýuter_Söz 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned nyşanyň_kody = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] usul_reje 경로와 호환한다.
        if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; nyşanyň_kody = 0x10000 + ((nyşanyň_kody - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdfff) return -22;
        unsigned 개수 = nyşanyň_kody < 128 ? 1 : nyşanyň_kody < 2048 ? 2 : nyşanyň_kody < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = nyşanyň_kody;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (nyşanyň_kody >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((nyşanyň_kody >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
kompýuter_Söz gural_aç(kompýuter_Söz Ad, kompýuter_Söz 설정비트) {
    char 자료위치[512]; int Hata = Ýol(Ad, 자료위치);
    return (uint32_t)(Hata ? Hata : 호출(3, (kompýuter_Söz)자료위치, 설정비트, 0));
}
kompýuter_Söz gural_ýap(kompýuter_Söz faýl_ryçag) { return (uint32_t)호출(4, faýl_ryçag, 0, 0); }
kompýuter_Söz 도구바이트읽기(kompýuter_Söz faýl_ryçag) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, faýl_ryçag, (kompýuter_Söz)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
kompýuter_Söz gural_ýaz_baýt(kompýuter_Söz faýl_ryçag, kompýuter_Söz baha) {
    unsigned char 둘째값 = baha; return (uint32_t)호출(1, faýl_ryçag, (kompýuter_Söz)&둘째값, 1);
}
kompýuter_Söz 도구읽기(kompýuter_Söz Ad, kompýuter_Söz barylmaly_ýer_maglumat_salgy) {
    if (꾸러미사용중) {
        char 자료위치[512]; int Hata = Ýol(Ad, 자료위치); if (Hata) return (uint32_t)Hata;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; kompýuter_Söz *목적위치 = (kompýuter_Söz *)barylmaly_ýer_maglumat_salgy;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int faýl_ryçag = 꾸러미사용중 ? -2 : (int32_t)gural_aç(Ad, 0);
    if (faýl_ryçag < 0) {
        char 자료위치[512]; int Hata = Ýol(Ad, 자료위치); if (Hata) return (uint32_t)Hata;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Ad; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            kompýuter_Söz *목적위치 = (kompýuter_Söz *)barylmaly_ýer_maglumat_salgy;
            if (목적위치[0] < 자바클래스들[순번].Ululyk) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Ululyk; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].maglumat[안쪽순번];
            return 자바클래스들[순번].Ululyk;
        }
        return (uint32_t)faýl_ryçag;
    }
    kompýuter_Söz *첫째값 = (kompýuter_Söz *)barylmaly_ýer_maglumat_salgy;
    intptr_t Ululyk = 호출(9, faýl_ryçag, 0, 0), 완료량 = 0;
    if (Ululyk < 0 || (kompýuter_Söz)Ululyk > 첫째값[0]) { gural_ýap(faýl_ryçag); return (uint32_t)(Ululyk < 0 ? Ululyk : -27); }
    unsigned char maglumat_bökde[256];
    while (완료량 < Ululyk) {
        intptr_t 개수 = 호출(2, faýl_ryçag, (kompýuter_Söz)maglumat_bökde, Ululyk - 완료량 < 256 ? Ululyk - 완료량 : 256);
        if (개수 <= 0) { gural_ýap(faýl_ryçag); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = maglumat_bökde[순번];
        완료량 += 개수;
    }
    gural_ýap(faýl_ryçag); return 완료량;
}
kompýuter_Söz gural_ýaz(kompýuter_Söz Ad, kompýuter_Söz 원본자료, kompýuter_Söz 항목수) {
    const kompýuter_Söz *첫째값 = (const kompýuter_Söz *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int faýl_ryçag = (int32_t)gural_aç(Ad, 577); if (faýl_ryçag < 0) return (uint32_t)faýl_ryçag;
    unsigned char maglumat_bökde[256]; kompýuter_Söz 완료량 = 0;
    while (완료량 < 항목수) {
        kompýuter_Söz 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (kompýuter_Söz 순번 = 0; 순번 < 개수; 순번++) maglumat_bökde[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, faýl_ryçag, (kompýuter_Söz)maglumat_bökde, 개수);
        if (결과 <= 0) { gural_ýap(faýl_ryçag); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    gural_ýap(faýl_ryçag); return 항목수;
}
kompýuter_Söz 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
kompýuter_Söz gural_argument(kompýuter_Söz 색인) {
    static const kompýuter_Söz boş_baha[1] = {0};
    if (색인 >= 8) return (kompýuter_Söz)boş_baha;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (kompýuter_Söz)입력결과, sizeof(입력결과));
    if (개수 < 0) return (kompýuter_Söz)boş_baha;
    kompýuter_Söz *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned nyşanyň_kody = 입력결과[순번++], 더있음 = nyşanyň_kody < 128 ? 0 : nyşanyň_kody >= 0xc2 && nyşanyň_kody < 0xe0 ? 1 : nyşanyň_kody < 0xf0 && nyşanyň_kody >= 0xe0 ? 2 : nyşanyň_kody >= 0xf0 && nyşanyň_kody <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) nyşanyň_kody &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { nyşanyň_kody = (nyşanyň_kody << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || nyşanyň_kody < 최소값 || nyşanyň_kody > 0x10ffff || (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdfff)) nyşanyň_kody = 0xfffd;
        if (nyşanyň_kody >= 65536) { nyşanyň_kody -= 65536; 결과자료[++항목수] = 0xd800 | (nyşanyň_kody >> 10); 결과자료[++항목수] = 0xdc00 | (nyşanyň_kody & 1023); }
        else 결과자료[++항목수] = nyşanyň_kody;
    }
    결과자료[0] = 항목수; return (kompýuter_Söz)결과자료;
}
kompýuter_Söz 도구분류(void) { return kategoriýa_baha; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); nyşan_a5317f02(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int başlat_ulanyjy_programma(int usul_reje) {
    kategoriýa_baha = usul_reje;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (kompýuter_Söz)첫항목, sizeof(첫항목));
    if (usul_reje == 2 || (usul_reje == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = usul_reje == 2 ? 0 : 1;
        char faýl_girizmeklik_at[256]; intptr_t dowamlylyk_maglumat = 호출(15, 꾸러미인수이동, (kompýuter_Söz)faýl_girizmeklik_at, sizeof(faýl_girizmeklik_at));
        if (dowamlylyk_maglumat <= 0 || 꾸러미열기(faýl_girizmeklik_at) < 0) {
            static const char Hata[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Hata, sizeof(Hata) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) nyşan_a5317f02(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Maşgala, 접속번호; uint32_t salgy; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
kompýuter_Söz 도구전문열기(kompýuter_Söz 접속번호) {
    intptr_t faýl_ryçag = 호출(32, 2, 2, 17); if (faýl_ryçag < 0) return (uint32_t)faýl_ryçag;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.salgy = 0;
    intptr_t ýagdaý_baha = 호출(33, faýl_ryçag, (kompýuter_Söz)&첫째값, sizeof(첫째값));
    if (ýagdaý_baha < 0) { gural_ýap(faýl_ryçag); return (uint32_t)ýagdaý_baha; }
    return faýl_ryçag;
}
kompýuter_Söz 도구전문보내기(kompýuter_Söz faýl_ryçag, kompýuter_Söz 접속번호, kompýuter_Söz ARRAY_baha, kompýuter_Söz dowamlylyk_baha) {
    const kompýuter_Söz *원본주소 = (const kompýuter_Söz *)ARRAY_baha; unsigned char maglumat[512];
    if (dowamlylyk_baha > 512 || dowamlylyk_baha > 원본주소[0]) return (uint32_t)-90;
    for (kompýuter_Söz 순번 = 0; 순번 < dowamlylyk_baha; 순번++) maglumat[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, faýl_ryçag, (kompýuter_Söz)maglumat, dowamlylyk_baha, 0, (kompýuter_Söz)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
kompýuter_Söz 도구전문주소보내기(kompýuter_Söz faýl_ryçag, kompýuter_Söz salgy, kompýuter_Söz 접속번호, kompýuter_Söz ARRAY_baha, kompýuter_Söz dowamlylyk_baha) {
    const kompýuter_Söz *원본주소 = (const kompýuter_Söz *)ARRAY_baha; unsigned char maglumat[512];
    if (dowamlylyk_baha > 512 || dowamlylyk_baha > 원본주소[0]) return (uint32_t)-90;
    for (kompýuter_Söz 순번 = 0; 순번 < dowamlylyk_baha; 순번++) maglumat[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.salgy = 바이트순서뒤집기(salgy);
    return (uint32_t)사용자호출(34, faýl_ryçag, (kompýuter_Söz)maglumat, dowamlylyk_baha, 0, (kompýuter_Söz)&첫째값, sizeof(첫째값));
}
kompýuter_Söz gural_Birikme(kompýuter_Söz faýl_ryçag, kompýuter_Söz salgy, kompýuter_Söz 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.salgy = 바이트순서뒤집기(salgy);
    uint32_t Bitir = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, faýl_ryçag, (kompýuter_Söz)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - Bitir) >= 1000) return (uint32_t)-110;
    }
}
kompýuter_Söz 도구전문받기(kompýuter_Söz faýl_ryçag, kompýuter_Söz ARRAY_baha, kompýuter_Söz 수용량) {
    kompýuter_Söz *barylmaly_ýer_salgy = (kompýuter_Söz *)ARRAY_baha; unsigned char maglumat[512];
    if (수용량 > 512 || barylmaly_ýer_salgy[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned dowamlylyk_maglumat = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, faýl_ryçag, (kompýuter_Söz)maglumat, 수용량, 0, (kompýuter_Söz)&첫째값, (kompýuter_Söz)&dowamlylyk_maglumat);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) barylmaly_ýer_salgy[순번 + 1] = maglumat[순번]; barylmaly_ýer_salgy[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; barylmaly_ýer_salgy[514] = 바이트순서뒤집기(첫째값.salgy); }
    return (uint32_t)개수;
}
kompýuter_Söz 도구전문접속번호(kompýuter_Söz faýl_ryçag) {
    struct 자바주소 첫째값; unsigned dowamlylyk_maglumat = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, faýl_ryçag, (kompýuter_Söz)&첫째값, (kompýuter_Söz)&dowamlylyk_maglumat);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
kompýuter_Söz 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
kompýuter_Söz 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
kompýuter_Söz 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
kompýuter_Söz 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
kompýuter_Söz 도구사각형(kompýuter_Söz x_koordinatasy, kompýuter_Söz 세로좌표, kompýuter_Söz 너비값, kompýuter_Söz 높이값, kompýuter_Söz 색상) {
    return (uint32_t)사용자호출(13, x_koordinatasy, 세로좌표, 색상, 너비값, 높이값, 0);
}

kompýuter_Söz gural_Stream(kompýuter_Söz iş,kompýuter_Söz faýl_ryçag,kompýuter_Söz baha){
    if(iş==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(baha);
    if(iş==1){첫째값.salgy=0;intptr_t 반환값=호출(33,faýl_ryçag,(kompýuter_Söz)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,faýl_ryçag,4,0));}
    if(iş==2)return (uint32_t)호출(37,faýl_ryçag,(kompýuter_Söz)&첫째값,sizeof(첫째값));
    if(iş==3)return (uint32_t)호출(39,faýl_ryçag,0,0);
    if(iş==4)return 도구전문접속번호(faýl_ryçag);
    if(iş==5)return (uint32_t)호출(40,faýl_ryçag,0,0);
    return (uint32_t)-22;
}
kompýuter_Söz gural_GUI(kompýuter_Söz iş,kompýuter_Söz tanaýjy_baha,kompýuter_Söz 첫째값,kompýuter_Söz 둘째값,kompýuter_Söz nyşanyň_kody,kompýuter_Söz barylmaly_ýer_maglumat){return (uint32_t)사용자호출(20,iş,tanaýjy_baha,첫째값,둘째값,nyşanyň_kody,barylmaly_ýer_maglumat);}
kompýuter_Söz gural_GUI_SMS(kompýuter_Söz tanaýjy_baha,kompýuter_Söz ARRAY_baha,kompýuter_Söz 개수){
    const kompýuter_Söz *원본주소=(const kompýuter_Söz *)ARRAY_baha;uint32_t maglumat[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(kompýuter_Söz 순번=0;순번<개수;순번++){unsigned nyşan_kodlaşdyrma=원본주소[순번+1];if(nyşan_kodlaşdyrma>=0xd800&&nyşan_kodlaşdyrma<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;nyşan_kodlaşdyrma=0x10000+((nyşan_kodlaşdyrma-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;maglumat[항목수++]=nyşan_kodlaşdyrma;}
    return (uint32_t)사용자호출(21,tanaýjy_baha,(kompýuter_Söz)maglumat,항목수,0,0,0);
}
