#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Ihele/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "isigaxa.h"
typedef uintptr_t umshini_Amagama;
static int umunxa_inani;
static int 꾸러미사용중, 꾸러미인수이동;
static umshini_Amagama 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, umshini_Amagama 첫째값, umshini_Amagama 둘째값, umshini_Amagama ikhodi_yohlamvu) {
    return 사용자호출(개수, 첫째값, 둘째값, ikhodi_yohlamvu, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (umshini_Amagama)자료위치, 개수); }
static void uhlamvusimo(unsigned ikhodi_yohlamvu) {
    unsigned char imininingwane[4]; unsigned 개수 = 0;
    if (ikhodi_yohlamvu < 128) imininingwane[개수++] = ikhodi_yohlamvu;
    else if (ikhodi_yohlamvu < 2048) { imininingwane[개수++] = 0xc0 | (ikhodi_yohlamvu >> 6); imininingwane[개수++] = 0x80 | (ikhodi_yohlamvu & 63); }
    else if (ikhodi_yohlamvu < 65536) { imininingwane[개수++] = 0xe0 | (ikhodi_yohlamvu >> 12); imininingwane[개수++] = 0x80 | ((ikhodi_yohlamvu >> 6) & 63); imininingwane[개수++] = 0x80 | (ikhodi_yohlamvu & 63); }
    else { imininingwane[개수++] = 0xf0 | (ikhodi_yohlamvu >> 18); imininingwane[개수++] = 0x80 | ((ikhodi_yohlamvu >> 12) & 63); imininingwane[개수++] = 0x80 | ((ikhodi_yohlamvu >> 6) & 63); imininingwane[개수++] = 0x80 | (ikhodi_yohlamvu & 63); }
    바이트들((const char *)imininingwane, 개수);
}
umshini_Amagama ithuluzi_uhlamvusimo(umshini_Amagama inani) {
    unsigned ikhodi_yohlamvu = inani;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (ikhodi_yohlamvu >= 0xdc00 && ikhodi_yohlamvu <= 0xdfff) { uhlamvusimo(0x10000 + ((높은부분 - 0xd800) << 10) + ikhodi_yohlamvu - 0xdc00); return 1; }
        uhlamvusimo(0xfffd);
    }
    if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdbff) 대기중짝글자 = ikhodi_yohlamvu;
    else uhlamvusimo(ikhodi_yohlamvu > 0x10ffff || (ikhodi_yohlamvu >= 0xdc00 && ikhodi_yohlamvu <= 0xdfff) ? 0xfffd : ikhodi_yohlamvu);
    return 1;
}
umshini_Amagama 도구출력(umshini_Amagama inani) {
    const umshini_Amagama *uchunge_imininingwane = (const umshini_Amagama *)inani;
    for (umshini_Amagama 순번 = 0; 순번 < uchunge_imininingwane[0]; 순번++) ithuluzi_uhlamvusimo(uchunge_imininingwane[순번 + 1]);
    return uchunge_imininingwane[0];
}
static int Indlela_2(umshini_Amagama into_Ireferensi, char 결과자료[512]) {
    const umshini_Amagama *첫째값 = (const umshini_Amagama *)into_Ireferensi;
    unsigned 사용량 = 0;
    for (umshini_Amagama 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned ikhodi_yohlamvu = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] indlela_inqubo 경로와 호환한다.
        if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; ikhodi_yohlamvu = 0x10000 + ((ikhodi_yohlamvu - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdfff) return -22;
        unsigned 개수 = ikhodi_yohlamvu < 128 ? 1 : ikhodi_yohlamvu < 2048 ? 2 : ikhodi_yohlamvu < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = ikhodi_yohlamvu;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (ikhodi_yohlamvu >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((ikhodi_yohlamvu >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
umshini_Amagama ithuluzi_vula(umshini_Amagama Igama, umshini_Amagama 설정비트) {
    char 자료위치[512]; int Iphutha = Indlela_2(Igama, 자료위치);
    return (uint32_t)(Iphutha ? Iphutha : 호출(3, (umshini_Amagama)자료위치, 설정비트, 0));
}
umshini_Amagama ithuluzi_vala(umshini_Amagama ifayela_isibambo) { return (uint32_t)호출(4, ifayela_isibambo, 0, 0); }
umshini_Amagama 도구바이트읽기(umshini_Amagama ifayela_isibambo) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, ifayela_isibambo, (umshini_Amagama)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
umshini_Amagama ithuluzi_bhala_ibhayithi(umshini_Amagama ifayela_isibambo, umshini_Amagama inani) {
    unsigned char 둘째값 = inani; return (uint32_t)호출(1, ifayela_isibambo, (umshini_Amagama)&둘째값, 1);
}
umshini_Amagama 도구읽기(umshini_Amagama Igama, umshini_Amagama isikhumulo_imininingwane_ikheli) {
    if (꾸러미사용중) {
        char 자료위치[512]; int Iphutha = Indlela_2(Igama, 자료위치); if (Iphutha) return (uint32_t)Iphutha;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; umshini_Amagama *목적위치 = (umshini_Amagama *)isikhumulo_imininingwane_ikheli;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int ifayela_isibambo = 꾸러미사용중 ? -2 : (int32_t)ithuluzi_vula(Igama, 0);
    if (ifayela_isibambo < 0) {
        char 자료위치[512]; int Iphutha = Indlela_2(Igama, 자료위치); if (Iphutha) return (uint32_t)Iphutha;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Igama; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            umshini_Amagama *목적위치 = (umshini_Amagama *)isikhumulo_imininingwane_ikheli;
            if (목적위치[0] < 자바클래스들[순번].Ubungako) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Ubungako; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].imininingwane[안쪽순번];
            return 자바클래스들[순번].Ubungako;
        }
        return (uint32_t)ifayela_isibambo;
    }
    umshini_Amagama *첫째값 = (umshini_Amagama *)isikhumulo_imininingwane_ikheli;
    intptr_t Ubungako = 호출(9, ifayela_isibambo, 0, 0), 완료량 = 0;
    if (Ubungako < 0 || (umshini_Amagama)Ubungako > 첫째값[0]) { ithuluzi_vala(ifayela_isibambo); return (uint32_t)(Ubungako < 0 ? Ubungako : -27); }
    unsigned char imininingwane_vimbela[256];
    while (완료량 < Ubungako) {
        intptr_t 개수 = 호출(2, ifayela_isibambo, (umshini_Amagama)imininingwane_vimbela, Ubungako - 완료량 < 256 ? Ubungako - 완료량 : 256);
        if (개수 <= 0) { ithuluzi_vala(ifayela_isibambo); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = imininingwane_vimbela[순번];
        완료량 += 개수;
    }
    ithuluzi_vala(ifayela_isibambo); return 완료량;
}
umshini_Amagama ithuluzi_bhala(umshini_Amagama Igama, umshini_Amagama 원본자료, umshini_Amagama 항목수) {
    const umshini_Amagama *첫째값 = (const umshini_Amagama *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int ifayela_isibambo = (int32_t)ithuluzi_vula(Igama, 577); if (ifayela_isibambo < 0) return (uint32_t)ifayela_isibambo;
    unsigned char imininingwane_vimbela[256]; umshini_Amagama 완료량 = 0;
    while (완료량 < 항목수) {
        umshini_Amagama 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (umshini_Amagama 순번 = 0; 순번 < 개수; 순번++) imininingwane_vimbela[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, ifayela_isibambo, (umshini_Amagama)imininingwane_vimbela, 개수);
        if (결과 <= 0) { ithuluzi_vala(ifayela_isibambo); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    ithuluzi_vala(ifayela_isibambo); return 항목수;
}
umshini_Amagama 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
umshini_Amagama ithuluzi_i_agumenti(umshini_Amagama 색인) {
    static const umshini_Amagama okungasho_lutho_inani[1] = {0};
    if (색인 >= 8) return (umshini_Amagama)okungasho_lutho_inani;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (umshini_Amagama)입력결과, sizeof(입력결과));
    if (개수 < 0) return (umshini_Amagama)okungasho_lutho_inani;
    umshini_Amagama *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned ikhodi_yohlamvu = 입력결과[순번++], 더있음 = ikhodi_yohlamvu < 128 ? 0 : ikhodi_yohlamvu >= 0xc2 && ikhodi_yohlamvu < 0xe0 ? 1 : ikhodi_yohlamvu < 0xf0 && ikhodi_yohlamvu >= 0xe0 ? 2 : ikhodi_yohlamvu >= 0xf0 && ikhodi_yohlamvu <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) ikhodi_yohlamvu &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { ikhodi_yohlamvu = (ikhodi_yohlamvu << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || ikhodi_yohlamvu < 최소값 || ikhodi_yohlamvu > 0x10ffff || (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdfff)) ikhodi_yohlamvu = 0xfffd;
        if (ikhodi_yohlamvu >= 65536) { ikhodi_yohlamvu -= 65536; 결과자료[++항목수] = 0xd800 | (ikhodi_yohlamvu >> 10); 결과자료[++항목수] = 0xdc00 | (ikhodi_yohlamvu & 1023); }
        else 결과자료[++항목수] = ikhodi_yohlamvu;
    }
    결과자료[0] = 항목수; return (umshini_Amagama)결과자료;
}
umshini_Amagama 도구분류(void) { return umunxa_inani; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); uhlamvusimo(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int qala_umsebenzisi_i_app(int indlela_inqubo) {
    umunxa_inani = indlela_inqubo;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (umshini_Amagama)첫항목, sizeof(첫항목));
    if (indlela_inqubo == 2 || (indlela_inqubo == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = indlela_inqubo == 2 ? 0 : 1;
        char ifayela_okufakwayo_igama[256]; intptr_t ubude_imininingwane = 호출(15, 꾸러미인수이동, (umshini_Amagama)ifayela_okufakwayo_igama, sizeof(ifayela_okufakwayo_igama));
        if (ubude_imininingwane <= 0 || 꾸러미열기(ifayela_okufakwayo_igama) < 0) {
            static const char Iphutha[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Iphutha, sizeof(Iphutha) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) uhlamvusimo(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Umndeni, 접속번호; uint32_t ikheli; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
umshini_Amagama 도구전문열기(umshini_Amagama 접속번호) {
    intptr_t ifayela_isibambo = 호출(32, 2, 2, 17); if (ifayela_isibambo < 0) return (uint32_t)ifayela_isibambo;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.ikheli = 0;
    intptr_t isimo_inani = 호출(33, ifayela_isibambo, (umshini_Amagama)&첫째값, sizeof(첫째값));
    if (isimo_inani < 0) { ithuluzi_vala(ifayela_isibambo); return (uint32_t)isimo_inani; }
    return ifayela_isibambo;
}
umshini_Amagama 도구전문보내기(umshini_Amagama ifayela_isibambo, umshini_Amagama 접속번호, umshini_Amagama AMALUNGU_AFANAYO_inani, umshini_Amagama ubude_inani) {
    const umshini_Amagama *원본주소 = (const umshini_Amagama *)AMALUNGU_AFANAYO_inani; unsigned char imininingwane[512];
    if (ubude_inani > 512 || ubude_inani > 원본주소[0]) return (uint32_t)-90;
    for (umshini_Amagama 순번 = 0; 순번 < ubude_inani; 순번++) imininingwane[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, ifayela_isibambo, (umshini_Amagama)imininingwane, ubude_inani, 0, (umshini_Amagama)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
umshini_Amagama 도구전문주소보내기(umshini_Amagama ifayela_isibambo, umshini_Amagama ikheli, umshini_Amagama 접속번호, umshini_Amagama AMALUNGU_AFANAYO_inani, umshini_Amagama ubude_inani) {
    const umshini_Amagama *원본주소 = (const umshini_Amagama *)AMALUNGU_AFANAYO_inani; unsigned char imininingwane[512];
    if (ubude_inani > 512 || ubude_inani > 원본주소[0]) return (uint32_t)-90;
    for (umshini_Amagama 순번 = 0; 순번 < ubude_inani; 순번++) imininingwane[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.ikheli = 바이트순서뒤집기(ikheli);
    return (uint32_t)사용자호출(34, ifayela_isibambo, (umshini_Amagama)imininingwane, ubude_inani, 0, (umshini_Amagama)&첫째값, sizeof(첫째값));
}
umshini_Amagama ithuluzi_xhuma(umshini_Amagama ifayela_isibambo, umshini_Amagama ikheli, umshini_Amagama 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.ikheli = 바이트순서뒤집기(ikheli);
    uint32_t Sebenzisa = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, ifayela_isibambo, (umshini_Amagama)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - Sebenzisa) >= 1000) return (uint32_t)-110;
    }
}
umshini_Amagama 도구전문받기(umshini_Amagama ifayela_isibambo, umshini_Amagama AMALUNGU_AFANAYO_inani, umshini_Amagama 수용량) {
    umshini_Amagama *isikhumulo_ikheli = (umshini_Amagama *)AMALUNGU_AFANAYO_inani; unsigned char imininingwane[512];
    if (수용량 > 512 || isikhumulo_ikheli[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned ubude_imininingwane = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, ifayela_isibambo, (umshini_Amagama)imininingwane, 수용량, 0, (umshini_Amagama)&첫째값, (umshini_Amagama)&ubude_imininingwane);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) isikhumulo_ikheli[순번 + 1] = imininingwane[순번]; isikhumulo_ikheli[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; isikhumulo_ikheli[514] = 바이트순서뒤집기(첫째값.ikheli); }
    return (uint32_t)개수;
}
umshini_Amagama 도구전문접속번호(umshini_Amagama ifayela_isibambo) {
    struct 자바주소 첫째값; unsigned ubude_imininingwane = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, ifayela_isibambo, (umshini_Amagama)&첫째값, (umshini_Amagama)&ubude_imininingwane);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
umshini_Amagama 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
umshini_Amagama 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
umshini_Amagama 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
umshini_Amagama 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
umshini_Amagama 도구사각형(umshini_Amagama okuxhumanisa_u_x, umshini_Amagama 세로좌표, umshini_Amagama 너비값, umshini_Amagama 높이값, umshini_Amagama 색상) {
    return (uint32_t)사용자호출(13, okuxhumanisa_u_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

umshini_Amagama ithuluzi_Stream(umshini_Amagama Isenzo,umshini_Amagama ifayela_isibambo,umshini_Amagama inani){
    if(Isenzo==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(inani);
    if(Isenzo==1){첫째값.ikheli=0;intptr_t 반환값=호출(33,ifayela_isibambo,(umshini_Amagama)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,ifayela_isibambo,4,0));}
    if(Isenzo==2)return (uint32_t)호출(37,ifayela_isibambo,(umshini_Amagama)&첫째값,sizeof(첫째값));
    if(Isenzo==3)return (uint32_t)호출(39,ifayela_isibambo,0,0);
    if(Isenzo==4)return 도구전문접속번호(ifayela_isibambo);
    if(Isenzo==5)return (uint32_t)호출(40,ifayela_isibambo,0,0);
    return (uint32_t)-22;
}
umshini_Amagama ithuluzi_i_GUI(umshini_Amagama Isenzo,umshini_Amagama isivezi_inani,umshini_Amagama 첫째값,umshini_Amagama 둘째값,umshini_Amagama ikhodi_yohlamvu,umshini_Amagama isikhumulo_imininingwane){return (uint32_t)사용자호출(20,Isenzo,isivezi_inani,첫째값,둘째값,ikhodi_yohlamvu,isikhumulo_imininingwane);}
umshini_Amagama ithuluzi_i_GUI_I_SMS(umshini_Amagama isivezi_inani,umshini_Amagama AMALUNGU_AFANAYO_inani,umshini_Amagama 개수){
    const umshini_Amagama *원본주소=(const umshini_Amagama *)AMALUNGU_AFANAYO_inani;uint32_t imininingwane[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(umshini_Amagama 순번=0;순번<개수;순번++){unsigned uhlamvusimo_ukubhala_ngokufihla=원본주소[순번+1];if(uhlamvusimo_ukubhala_ngokufihla>=0xd800&&uhlamvusimo_ukubhala_ngokufihla<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;uhlamvusimo_ukubhala_ngokufihla=0x10000+((uhlamvusimo_ukubhala_ngokufihla-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;imininingwane[항목수++]=uhlamvusimo_ukubhala_ngokufihla;}
    return (uint32_t)사용자호출(21,isivezi_inani,(umshini_Amagama)imininingwane,항목수,0,0,0);
}
