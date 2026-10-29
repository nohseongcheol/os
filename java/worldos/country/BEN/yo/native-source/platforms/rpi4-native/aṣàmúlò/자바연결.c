#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fáìlì/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "àkópọ̀.h"
typedef uintptr_t maṣíìnì_Ọ̀rọ̀;
static int ìsọ̀rí_iye;
static int 꾸러미사용중, 꾸러미인수이동;
static maṣíìnì_Ọ̀rọ̀ 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, maṣíìnì_Ọ̀rọ̀ 첫째값, maṣíìnì_Ọ̀rọ̀ 둘째값, maṣíìnì_Ọ̀rọ̀ kóòdù_ẹyọ_ọ̀rọ̀) {
    return 사용자호출(개수, 첫째값, 둘째값, kóòdù_ẹyọ_ọ̀rọ̀, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (maṣíìnì_Ọ̀rọ̀)자료위치, 개수); }
static void ẹyọ_ọ̀rọ̀(unsigned kóòdù_ẹyọ_ọ̀rọ̀) {
    unsigned char détà[4]; unsigned 개수 = 0;
    if (kóòdù_ẹyọ_ọ̀rọ̀ < 128) détà[개수++] = kóòdù_ẹyọ_ọ̀rọ̀;
    else if (kóòdù_ẹyọ_ọ̀rọ̀ < 2048) { détà[개수++] = 0xc0 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 6); détà[개수++] = 0x80 | (kóòdù_ẹyọ_ọ̀rọ̀ & 63); }
    else if (kóòdù_ẹyọ_ọ̀rọ̀ < 65536) { détà[개수++] = 0xe0 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 12); détà[개수++] = 0x80 | ((kóòdù_ẹyọ_ọ̀rọ̀ >> 6) & 63); détà[개수++] = 0x80 | (kóòdù_ẹyọ_ọ̀rọ̀ & 63); }
    else { détà[개수++] = 0xf0 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 18); détà[개수++] = 0x80 | ((kóòdù_ẹyọ_ọ̀rọ̀ >> 12) & 63); détà[개수++] = 0x80 | ((kóòdù_ẹyọ_ọ̀rọ̀ >> 6) & 63); détà[개수++] = 0x80 | (kóòdù_ẹyọ_ọ̀rọ̀ & 63); }
    바이트들((const char *)détà, 개수);
}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_ẹyọ_ọ̀rọ̀(maṣíìnì_Ọ̀rọ̀ iye) {
    unsigned kóòdù_ẹyọ_ọ̀rọ̀ = iye;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xdc00 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff) { ẹyọ_ọ̀rọ̀(0x10000 + ((높은부분 - 0xd800) << 10) + kóòdù_ẹyọ_ọ̀rọ̀ - 0xdc00); return 1; }
        ẹyọ_ọ̀rọ̀(0xfffd);
    }
    if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdbff) 대기중짝글자 = kóòdù_ẹyọ_ọ̀rọ̀;
    else ẹyọ_ọ̀rọ̀(kóòdù_ẹyọ_ọ̀rọ̀ > 0x10ffff || (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xdc00 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff) ? 0xfffd : kóòdù_ẹyọ_ọ̀rọ̀);
    return 1;
}
maṣíìnì_Ọ̀rọ̀ 도구출력(maṣíìnì_Ọ̀rọ̀ iye) {
    const maṣíìnì_Ọ̀rọ̀ *fọ́nrán_détà = (const maṣíìnì_Ọ̀rọ̀ *)iye;
    for (maṣíìnì_Ọ̀rọ̀ 순번 = 0; 순번 < fọ́nrán_détà[0]; 순번++) irinṣẹ́_ẹyọ_ọ̀rọ̀(fọ́nrán_détà[순번 + 1]);
    return fọ́nrán_détà[0];
}
static int ọ̀nà(maṣíìnì_Ọ̀rọ̀ nǹkan_Ìtọ́ka, char 결과자료[512]) {
    const maṣíìnì_Ọ̀rọ̀ *첫째값 = (const maṣíìnì_Ọ̀rọ̀ *)nǹkan_Ìtọ́ka;
    unsigned 사용량 = 0;
    for (maṣíìnì_Ọ̀rọ̀ 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kóòdù_ẹyọ_ọ̀rọ̀ = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] ìlànà_móòdù 경로와 호환한다.
        if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kóòdù_ẹyọ_ọ̀rọ̀ = 0x10000 + ((kóòdù_ẹyọ_ọ̀rọ̀ - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff) return -22;
        unsigned 개수 = kóòdù_ẹyọ_ọ̀rọ̀ < 128 ? 1 : kóòdù_ẹyọ_ọ̀rọ̀ < 2048 ? 2 : kóòdù_ẹyọ_ọ̀rọ̀ < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = kóòdù_ẹyọ_ọ̀rọ̀;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (kóòdù_ẹyọ_ọ̀rọ̀ >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((kóòdù_ẹyọ_ọ̀rọ̀ >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_ṣí(maṣíìnì_Ọ̀rọ̀ Orúkọ, maṣíìnì_Ọ̀rọ̀ 설정비트) {
    char 자료위치[512]; int àṣìṣe = ọ̀nà(Orúkọ, 자료위치);
    return (uint32_t)(àṣìṣe ? àṣìṣe : 호출(3, (maṣíìnì_Ọ̀rọ̀)자료위치, 설정비트, 0));
}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_pa_dé(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù) { return (uint32_t)호출(4, fáìlì_èkù, 0, 0); }
maṣíìnì_Ọ̀rọ̀ 도구바이트읽기(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_kọ_báìtì(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù, maṣíìnì_Ọ̀rọ̀ iye) {
    unsigned char 둘째값 = iye; return (uint32_t)호출(1, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)&둘째값, 1);
}
maṣíìnì_Ọ̀rọ̀ 도구읽기(maṣíìnì_Ọ̀rọ̀ Orúkọ, maṣíìnì_Ọ̀rọ̀ èbúté_détà_àdírẹ́ẹ̀sì) {
    if (꾸러미사용중) {
        char 자료위치[512]; int àṣìṣe = ọ̀nà(Orúkọ, 자료위치); if (àṣìṣe) return (uint32_t)àṣìṣe;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; maṣíìnì_Ọ̀rọ̀ *목적위치 = (maṣíìnì_Ọ̀rọ̀ *)èbúté_détà_àdírẹ́ẹ̀sì;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int fáìlì_èkù = 꾸러미사용중 ? -2 : (int32_t)irinṣẹ́_ṣí(Orúkọ, 0);
    if (fáìlì_èkù < 0) {
        char 자료위치[512]; int àṣìṣe = ọ̀nà(Orúkọ, 자료위치); if (àṣìṣe) return (uint32_t)àṣìṣe;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Orúkọ; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            maṣíìnì_Ọ̀rọ̀ *목적위치 = (maṣíìnì_Ọ̀rọ̀ *)èbúté_détà_àdírẹ́ẹ̀sì;
            if (목적위치[0] < 자바클래스들[순번].Ìwọ̀n) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Ìwọ̀n; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].détà[안쪽순번];
            return 자바클래스들[순번].Ìwọ̀n;
        }
        return (uint32_t)fáìlì_èkù;
    }
    maṣíìnì_Ọ̀rọ̀ *첫째값 = (maṣíìnì_Ọ̀rọ̀ *)èbúté_détà_àdírẹ́ẹ̀sì;
    intptr_t Ìwọ̀n = 호출(9, fáìlì_èkù, 0, 0), 완료량 = 0;
    if (Ìwọ̀n < 0 || (maṣíìnì_Ọ̀rọ̀)Ìwọ̀n > 첫째값[0]) { irinṣẹ́_pa_dé(fáìlì_èkù); return (uint32_t)(Ìwọ̀n < 0 ? Ìwọ̀n : -27); }
    unsigned char détà_sèdíwọ[256];
    while (완료량 < Ìwọ̀n) {
        intptr_t 개수 = 호출(2, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)détà_sèdíwọ, Ìwọ̀n - 완료량 < 256 ? Ìwọ̀n - 완료량 : 256);
        if (개수 <= 0) { irinṣẹ́_pa_dé(fáìlì_èkù); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = détà_sèdíwọ[순번];
        완료량 += 개수;
    }
    irinṣẹ́_pa_dé(fáìlì_èkù); return 완료량;
}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_kọ(maṣíìnì_Ọ̀rọ̀ Orúkọ, maṣíìnì_Ọ̀rọ̀ 원본자료, maṣíìnì_Ọ̀rọ̀ 항목수) {
    const maṣíìnì_Ọ̀rọ̀ *첫째값 = (const maṣíìnì_Ọ̀rọ̀ *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int fáìlì_èkù = (int32_t)irinṣẹ́_ṣí(Orúkọ, 577); if (fáìlì_èkù < 0) return (uint32_t)fáìlì_èkù;
    unsigned char détà_sèdíwọ[256]; maṣíìnì_Ọ̀rọ̀ 완료량 = 0;
    while (완료량 < 항목수) {
        maṣíìnì_Ọ̀rọ̀ 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (maṣíìnì_Ọ̀rọ̀ 순번 = 0; 순번 < 개수; 순번++) détà_sèdíwọ[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)détà_sèdíwọ, 개수);
        if (결과 <= 0) { irinṣẹ́_pa_dé(fáìlì_èkù); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    irinṣẹ́_pa_dé(fáìlì_èkù); return 항목수;
}
maṣíìnì_Ọ̀rọ̀ 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_ágúmẹ́ntì(maṣíìnì_Ọ̀rọ̀ 색인) {
    static const maṣíìnì_Ọ̀rọ̀ òfìfo_iye[1] = {0};
    if (색인 >= 8) return (maṣíìnì_Ọ̀rọ̀)òfìfo_iye;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (maṣíìnì_Ọ̀rọ̀)입력결과, sizeof(입력결과));
    if (개수 < 0) return (maṣíìnì_Ọ̀rọ̀)òfìfo_iye;
    maṣíìnì_Ọ̀rọ̀ *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned kóòdù_ẹyọ_ọ̀rọ̀ = 입력결과[순번++], 더있음 = kóòdù_ẹyọ_ọ̀rọ̀ < 128 ? 0 : kóòdù_ẹyọ_ọ̀rọ̀ >= 0xc2 && kóòdù_ẹyọ_ọ̀rọ̀ < 0xe0 ? 1 : kóòdù_ẹyọ_ọ̀rọ̀ < 0xf0 && kóòdù_ẹyọ_ọ̀rọ̀ >= 0xe0 ? 2 : kóòdù_ẹyọ_ọ̀rọ̀ >= 0xf0 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kóòdù_ẹyọ_ọ̀rọ̀ &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kóòdù_ẹyọ_ọ̀rọ̀ = (kóòdù_ẹyọ_ọ̀rọ̀ << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kóòdù_ẹyọ_ọ̀rọ̀ < 최소값 || kóòdù_ẹyọ_ọ̀rọ̀ > 0x10ffff || (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff)) kóòdù_ẹyọ_ọ̀rọ̀ = 0xfffd;
        if (kóòdù_ẹyọ_ọ̀rọ̀ >= 65536) { kóòdù_ẹyọ_ọ̀rọ̀ -= 65536; 결과자료[++항목수] = 0xd800 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 10); 결과자료[++항목수] = 0xdc00 | (kóòdù_ẹyọ_ọ̀rọ̀ & 1023); }
        else 결과자료[++항목수] = kóòdù_ẹyọ_ọ̀rọ̀;
    }
    결과자료[0] = 항목수; return (maṣíìnì_Ọ̀rọ̀)결과자료;
}
maṣíìnì_Ọ̀rọ̀ 도구분류(void) { return ìsọ̀rí_iye; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); ẹyọ_ọ̀rọ̀(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int ìlànà_móòdù) {
    ìsọ̀rí_iye = ìlànà_móòdù;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (maṣíìnì_Ọ̀rọ̀)첫항목, sizeof(첫항목));
    if (ìlànà_móòdù == 2 || (ìlànà_móòdù == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = ìlànà_móòdù == 2 ? 0 : 1;
        char fáìlì_ìgbéwọlé_orúkọ[256]; intptr_t gígùn_détà = 호출(15, 꾸러미인수이동, (maṣíìnì_Ọ̀rọ̀)fáìlì_ìgbéwọlé_orúkọ, sizeof(fáìlì_ìgbéwọlé_orúkọ));
        if (gígùn_détà <= 0 || 꾸러미열기(fáìlì_ìgbéwọlé_orúkọ) < 0) {
            static const char àṣìṣe[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(àṣìṣe, sizeof(àṣìṣe) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) ẹyọ_ọ̀rọ̀(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Ẹbí, 접속번호; uint32_t àdírẹ́ẹ̀sì; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
maṣíìnì_Ọ̀rọ̀ 도구전문열기(maṣíìnì_Ọ̀rọ̀ 접속번호) {
    intptr_t fáìlì_èkù = 호출(32, 2, 2, 17); if (fáìlì_èkù < 0) return (uint32_t)fáìlì_èkù;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.àdírẹ́ẹ̀sì = 0;
    intptr_t ipò_iye = 호출(33, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)&첫째값, sizeof(첫째값));
    if (ipò_iye < 0) { irinṣẹ́_pa_dé(fáìlì_èkù); return (uint32_t)ipò_iye; }
    return fáìlì_èkù;
}
maṣíìnì_Ọ̀rọ̀ 도구전문보내기(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù, maṣíìnì_Ọ̀rọ̀ 접속번호, maṣíìnì_Ọ̀rọ̀ ÀRÉÈ_iye, maṣíìnì_Ọ̀rọ̀ gígùn_iye) {
    const maṣíìnì_Ọ̀rọ̀ *원본주소 = (const maṣíìnì_Ọ̀rọ̀ *)ÀRÉÈ_iye; unsigned char détà[512];
    if (gígùn_iye > 512 || gígùn_iye > 원본주소[0]) return (uint32_t)-90;
    for (maṣíìnì_Ọ̀rọ̀ 순번 = 0; 순번 < gígùn_iye; 순번++) détà[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)détà, gígùn_iye, 0, (maṣíìnì_Ọ̀rọ̀)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
maṣíìnì_Ọ̀rọ̀ 도구전문주소보내기(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù, maṣíìnì_Ọ̀rọ̀ àdírẹ́ẹ̀sì, maṣíìnì_Ọ̀rọ̀ 접속번호, maṣíìnì_Ọ̀rọ̀ ÀRÉÈ_iye, maṣíìnì_Ọ̀rọ̀ gígùn_iye) {
    const maṣíìnì_Ọ̀rọ̀ *원본주소 = (const maṣíìnì_Ọ̀rọ̀ *)ÀRÉÈ_iye; unsigned char détà[512];
    if (gígùn_iye > 512 || gígùn_iye > 원본주소[0]) return (uint32_t)-90;
    for (maṣíìnì_Ọ̀rọ̀ 순번 = 0; 순번 < gígùn_iye; 순번++) détà[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.àdírẹ́ẹ̀sì = 바이트순서뒤집기(àdírẹ́ẹ̀sì);
    return (uint32_t)사용자호출(34, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)détà, gígùn_iye, 0, (maṣíìnì_Ọ̀rọ̀)&첫째값, sizeof(첫째값));
}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_SOMỌ́(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù, maṣíìnì_Ọ̀rọ̀ àdírẹ́ẹ̀sì, maṣíìnì_Ọ̀rọ̀ 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.àdírẹ́ẹ̀sì = 바이트순서뒤집기(àdírẹ́ẹ̀sì);
    uint32_t Rọ́ọ̀nù = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - Rọ́ọ̀nù) >= 1000) return (uint32_t)-110;
    }
}
maṣíìnì_Ọ̀rọ̀ 도구전문받기(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù, maṣíìnì_Ọ̀rọ̀ ÀRÉÈ_iye, maṣíìnì_Ọ̀rọ̀ 수용량) {
    maṣíìnì_Ọ̀rọ̀ *èbúté_àdírẹ́ẹ̀sì = (maṣíìnì_Ọ̀rọ̀ *)ÀRÉÈ_iye; unsigned char détà[512];
    if (수용량 > 512 || èbúté_àdírẹ́ẹ̀sì[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned gígùn_détà = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)détà, 수용량, 0, (maṣíìnì_Ọ̀rọ̀)&첫째값, (maṣíìnì_Ọ̀rọ̀)&gígùn_détà);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) èbúté_àdírẹ́ẹ̀sì[순번 + 1] = détà[순번]; èbúté_àdírẹ́ẹ̀sì[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; èbúté_àdírẹ́ẹ̀sì[514] = 바이트순서뒤집기(첫째값.àdírẹ́ẹ̀sì); }
    return (uint32_t)개수;
}
maṣíìnì_Ọ̀rọ̀ 도구전문접속번호(maṣíìnì_Ọ̀rọ̀ fáìlì_èkù) {
    struct 자바주소 첫째값; unsigned gígùn_détà = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fáìlì_èkù, (maṣíìnì_Ọ̀rọ̀)&첫째값, (maṣíìnì_Ọ̀rọ̀)&gígùn_détà);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
maṣíìnì_Ọ̀rọ̀ 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
maṣíìnì_Ọ̀rọ̀ 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
maṣíìnì_Ọ̀rọ̀ 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
maṣíìnì_Ọ̀rọ̀ 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
maṣíìnì_Ọ̀rọ̀ 도구사각형(maṣíìnì_Ọ̀rọ̀ ibi_ìtọ́kasí_x, maṣíìnì_Ọ̀rọ̀ 세로좌표, maṣíìnì_Ọ̀rọ̀ 너비값, maṣíìnì_Ọ̀rọ̀ 높이값, maṣíìnì_Ọ̀rọ̀ 색상) {
    return (uint32_t)사용자호출(13, ibi_ìtọ́kasí_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

maṣíìnì_Ọ̀rọ̀ irinṣẹ́_Stream(maṣíìnì_Ọ̀rọ̀ ìṣe,maṣíìnì_Ọ̀rọ̀ fáìlì_èkù,maṣíìnì_Ọ̀rọ̀ iye){
    if(ìṣe==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(iye);
    if(ìṣe==1){첫째값.àdírẹ́ẹ̀sì=0;intptr_t 반환값=호출(33,fáìlì_èkù,(maṣíìnì_Ọ̀rọ̀)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fáìlì_èkù,4,0));}
    if(ìṣe==2)return (uint32_t)호출(37,fáìlì_èkù,(maṣíìnì_Ọ̀rọ̀)&첫째값,sizeof(첫째값));
    if(ìṣe==3)return (uint32_t)호출(39,fáìlì_èkù,0,0);
    if(ìṣe==4)return 도구전문접속번호(fáìlì_èkù);
    if(ìṣe==5)return (uint32_t)호출(40,fáìlì_èkù,0,0);
    return (uint32_t)-22;
}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_GUI(maṣíìnì_Ọ̀rọ̀ ìṣe,maṣíìnì_Ọ̀rọ̀ Àfidámọ̀_iye,maṣíìnì_Ọ̀rọ̀ 첫째값,maṣíìnì_Ọ̀rọ̀ 둘째값,maṣíìnì_Ọ̀rọ̀ kóòdù_ẹyọ_ọ̀rọ̀,maṣíìnì_Ọ̀rọ̀ èbúté_détà){return (uint32_t)사용자호출(20,ìṣe,Àfidámọ̀_iye,첫째값,둘째값,kóòdù_ẹyọ_ọ̀rọ̀,èbúté_détà);}
maṣíìnì_Ọ̀rọ̀ irinṣẹ́_GUI_SMS(maṣíìnì_Ọ̀rọ̀ Àfidámọ̀_iye,maṣíìnì_Ọ̀rọ̀ ÀRÉÈ_iye,maṣíìnì_Ọ̀rọ̀ 개수){
    const maṣíìnì_Ọ̀rọ̀ *원본주소=(const maṣíìnì_Ọ̀rọ̀ *)ÀRÉÈ_iye;uint32_t détà[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(maṣíìnì_Ọ̀rọ̀ 순번=0;순번<개수;순번++){unsigned ẹyọ_ọ̀rọ̀_pípàrokò=원본주소[순번+1];if(ẹyọ_ọ̀rọ̀_pípàrokò>=0xd800&&ẹyọ_ọ̀rọ̀_pípàrokò<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;ẹyọ_ọ̀rọ̀_pípàrokò=0x10000+((ẹyọ_ọ̀rọ̀_pípàrokò-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;détà[항목수++]=ẹyọ_ọ̀rọ̀_pípàrokò;}
    return (uint32_t)사용자호출(21,Àfidámọ̀_iye,(maṣíìnì_Ọ̀rọ̀)détà,항목수,0,0,0);
}
