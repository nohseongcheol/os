#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Idosiye/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "ipaki.h"
typedef uintptr_t imashini_Ijambo;
static int icyiciro_agaciro;
static int 꾸러미사용중, 꾸러미인수이동;
static imashini_Ijambo 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, imashini_Ijambo 첫째값, imashini_Ijambo 둘째값, imashini_Ijambo 문자값) {
    return 사용자호출(개수, 첫째값, 둘째값, 문자값, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (imashini_Ijambo)자료위치, 개수); }
static void inyuguti(unsigned 문자값) {
    unsigned char amakurushingiro[4]; unsigned 개수 = 0;
    if (문자값 < 128) amakurushingiro[개수++] = 문자값;
    else if (문자값 < 2048) { amakurushingiro[개수++] = 0xc0 | (문자값 >> 6); amakurushingiro[개수++] = 0x80 | (문자값 & 63); }
    else if (문자값 < 65536) { amakurushingiro[개수++] = 0xe0 | (문자값 >> 12); amakurushingiro[개수++] = 0x80 | ((문자값 >> 6) & 63); amakurushingiro[개수++] = 0x80 | (문자값 & 63); }
    else { amakurushingiro[개수++] = 0xf0 | (문자값 >> 18); amakurushingiro[개수++] = 0x80 | ((문자값 >> 12) & 63); amakurushingiro[개수++] = 0x80 | ((문자값 >> 6) & 63); amakurushingiro[개수++] = 0x80 | (문자값 & 63); }
    바이트들((const char *)amakurushingiro, 개수);
}
imashini_Ijambo igikoresho_inyuguti(imashini_Ijambo agaciro) {
    unsigned 문자값 = agaciro;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (문자값 >= 0xdc00 && 문자값 <= 0xdfff) { inyuguti(0x10000 + ((높은부분 - 0xd800) << 10) + 문자값 - 0xdc00); return 1; }
        inyuguti(0xfffd);
    }
    if (문자값 >= 0xd800 && 문자값 <= 0xdbff) 대기중짝글자 = 문자값;
    else inyuguti(문자값 > 0x10ffff || (문자값 >= 0xdc00 && 문자값 <= 0xdfff) ? 0xfffd : 문자값);
    return 1;
}
imashini_Ijambo 도구출력(imashini_Ijambo agaciro) {
    const imashini_Ijambo *igicenteruro_amakurushingiro = (const imashini_Ijambo *)agaciro;
    for (imashini_Ijambo 순번 = 0; 순번 < igicenteruro_amakurushingiro[0]; 순번++) igikoresho_inyuguti(igicenteruro_amakurushingiro[순번 + 1]);
    return igicenteruro_amakurushingiro[0];
}
static int Inzira(imashini_Ijambo ikintu_Indanga, char 결과자료[512]) {
    const imashini_Ijambo *첫째값 = (const imashini_Ijambo *)ikintu_Indanga;
    unsigned 사용량 = 0;
    for (imashini_Ijambo 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned 문자값 = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] uburyo_uburyo 경로와 호환한다.
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
imashini_Ijambo igikoresho_kurema(imashini_Ijambo Izina, imashini_Ijambo 설정비트) {
    char 자료위치[512]; int IKOSA = Inzira(Izina, 자료위치);
    return (uint32_t)(IKOSA ? IKOSA : 호출(3, (imashini_Ijambo)자료위치, 설정비트, 0));
}
imashini_Ijambo igikoresho_gufunga(imashini_Ijambo dosiye_umukondo) { return (uint32_t)호출(4, dosiye_umukondo, 0, 0); }
imashini_Ijambo 도구바이트읽기(imashini_Ijambo dosiye_umukondo) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, dosiye_umukondo, (imashini_Ijambo)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
imashini_Ijambo igikoresho_kwandika_bayiti(imashini_Ijambo dosiye_umukondo, imashini_Ijambo agaciro) {
    unsigned char 둘째값 = agaciro; return (uint32_t)호출(1, dosiye_umukondo, (imashini_Ijambo)&둘째값, 1);
}
imashini_Ijambo 도구읽기(imashini_Ijambo Izina, imashini_Ijambo aho_ijya_amakurushingiro_aderesi) {
    if (꾸러미사용중) {
        char 자료위치[512]; int IKOSA = Inzira(Izina, 자료위치); if (IKOSA) return (uint32_t)IKOSA;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; imashini_Ijambo *목적위치 = (imashini_Ijambo *)aho_ijya_amakurushingiro_aderesi;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int dosiye_umukondo = 꾸러미사용중 ? -2 : (int32_t)igikoresho_kurema(Izina, 0);
    if (dosiye_umukondo < 0) {
        char 자료위치[512]; int IKOSA = Inzira(Izina, 자료위치); if (IKOSA) return (uint32_t)IKOSA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Izina; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            imashini_Ijambo *목적위치 = (imashini_Ijambo *)aho_ijya_amakurushingiro_aderesi;
            if (목적위치[0] < 자바클래스들[순번].Ingano) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Ingano; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].amakurushingiro[안쪽순번];
            return 자바클래스들[순번].Ingano;
        }
        return (uint32_t)dosiye_umukondo;
    }
    imashini_Ijambo *첫째값 = (imashini_Ijambo *)aho_ijya_amakurushingiro_aderesi;
    intptr_t Ingano = 호출(9, dosiye_umukondo, 0, 0), 완료량 = 0;
    if (Ingano < 0 || (imashini_Ijambo)Ingano > 첫째값[0]) { igikoresho_gufunga(dosiye_umukondo); return (uint32_t)(Ingano < 0 ? Ingano : -27); }
    unsigned char amakurushingiro_guheza[256];
    while (완료량 < Ingano) {
        intptr_t 개수 = 호출(2, dosiye_umukondo, (imashini_Ijambo)amakurushingiro_guheza, Ingano - 완료량 < 256 ? Ingano - 완료량 : 256);
        if (개수 <= 0) { igikoresho_gufunga(dosiye_umukondo); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = amakurushingiro_guheza[순번];
        완료량 += 개수;
    }
    igikoresho_gufunga(dosiye_umukondo); return 완료량;
}
imashini_Ijambo igikoresho_kwandika(imashini_Ijambo Izina, imashini_Ijambo 원본자료, imashini_Ijambo 항목수) {
    const imashini_Ijambo *첫째값 = (const imashini_Ijambo *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int dosiye_umukondo = (int32_t)igikoresho_kurema(Izina, 577); if (dosiye_umukondo < 0) return (uint32_t)dosiye_umukondo;
    unsigned char amakurushingiro_guheza[256]; imashini_Ijambo 완료량 = 0;
    while (완료량 < 항목수) {
        imashini_Ijambo 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (imashini_Ijambo 순번 = 0; 순번 < 개수; 순번++) amakurushingiro_guheza[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, dosiye_umukondo, (imashini_Ijambo)amakurushingiro_guheza, 개수);
        if (결과 <= 0) { igikoresho_gufunga(dosiye_umukondo); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    igikoresho_gufunga(dosiye_umukondo); return 항목수;
}
imashini_Ijambo 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
imashini_Ijambo igikoresho_ingingo(imashini_Ijambo 색인) {
    static const imashini_Ijambo irimo_ubusa_agaciro[1] = {0};
    if (색인 >= 8) return (imashini_Ijambo)irimo_ubusa_agaciro;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (imashini_Ijambo)입력결과, sizeof(입력결과));
    if (개수 < 0) return (imashini_Ijambo)irimo_ubusa_agaciro;
    imashini_Ijambo *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
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
    결과자료[0] = 항목수; return (imashini_Ijambo)결과자료;
}
imashini_Ijambo 도구분류(void) { return icyiciro_agaciro; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); inyuguti(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Itangira_ukoresha_porogaramu(int uburyo_uburyo) {
    icyiciro_agaciro = uburyo_uburyo;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (imashini_Ijambo)첫항목, sizeof(첫항목));
    if (uburyo_uburyo == 2 || (uburyo_uburyo == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = uburyo_uburyo == 2 ? 0 : 1;
        char dosiye_icyinjizwa_izina[256]; intptr_t uburebure_amakurushingiro = 호출(15, 꾸러미인수이동, (imashini_Ijambo)dosiye_icyinjizwa_izina, sizeof(dosiye_icyinjizwa_izina));
        if (uburebure_amakurushingiro <= 0 || 꾸러미열기(dosiye_icyinjizwa_izina) < 0) {
            static const char IKOSA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(IKOSA, sizeof(IKOSA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) inyuguti(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Umuryango, 접속번호; uint32_t aderesi; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
imashini_Ijambo 도구전문열기(imashini_Ijambo 접속번호) {
    intptr_t dosiye_umukondo = 호출(32, 2, 2, 17); if (dosiye_umukondo < 0) return (uint32_t)dosiye_umukondo;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.aderesi = 0;
    intptr_t imimerere_agaciro = 호출(33, dosiye_umukondo, (imashini_Ijambo)&첫째값, sizeof(첫째값));
    if (imimerere_agaciro < 0) { igikoresho_gufunga(dosiye_umukondo); return (uint32_t)imimerere_agaciro; }
    return dosiye_umukondo;
}
imashini_Ijambo 도구전문보내기(imashini_Ijambo dosiye_umukondo, imashini_Ijambo 접속번호, imashini_Ijambo ARRAY_agaciro, imashini_Ijambo uburebure_agaciro) {
    const imashini_Ijambo *원본주소 = (const imashini_Ijambo *)ARRAY_agaciro; unsigned char amakurushingiro[512];
    if (uburebure_agaciro > 512 || uburebure_agaciro > 원본주소[0]) return (uint32_t)-90;
    for (imashini_Ijambo 순번 = 0; 순번 < uburebure_agaciro; 순번++) amakurushingiro[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, dosiye_umukondo, (imashini_Ijambo)amakurushingiro, uburebure_agaciro, 0, (imashini_Ijambo)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
imashini_Ijambo 도구전문주소보내기(imashini_Ijambo dosiye_umukondo, imashini_Ijambo aderesi, imashini_Ijambo 접속번호, imashini_Ijambo ARRAY_agaciro, imashini_Ijambo uburebure_agaciro) {
    const imashini_Ijambo *원본주소 = (const imashini_Ijambo *)ARRAY_agaciro; unsigned char amakurushingiro[512];
    if (uburebure_agaciro > 512 || uburebure_agaciro > 원본주소[0]) return (uint32_t)-90;
    for (imashini_Ijambo 순번 = 0; 순번 < uburebure_agaciro; 순번++) amakurushingiro[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.aderesi = 바이트순서뒤집기(aderesi);
    return (uint32_t)사용자호출(34, dosiye_umukondo, (imashini_Ijambo)amakurushingiro, uburebure_agaciro, 0, (imashini_Ijambo)&첫째값, sizeof(첫째값));
}
imashini_Ijambo igikoresho_Guhuza(imashini_Ijambo dosiye_umukondo, imashini_Ijambo aderesi, imashini_Ijambo 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.aderesi = 바이트순서뒤집기(aderesi);
    uint32_t ihuriro = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, dosiye_umukondo, (imashini_Ijambo)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - ihuriro) >= 1000) return (uint32_t)-110;
    }
}
imashini_Ijambo 도구전문받기(imashini_Ijambo dosiye_umukondo, imashini_Ijambo ARRAY_agaciro, imashini_Ijambo 수용량) {
    imashini_Ijambo *aho_ijya_aderesi = (imashini_Ijambo *)ARRAY_agaciro; unsigned char amakurushingiro[512];
    if (수용량 > 512 || aho_ijya_aderesi[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned uburebure_amakurushingiro = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, dosiye_umukondo, (imashini_Ijambo)amakurushingiro, 수용량, 0, (imashini_Ijambo)&첫째값, (imashini_Ijambo)&uburebure_amakurushingiro);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) aho_ijya_aderesi[순번 + 1] = amakurushingiro[순번]; aho_ijya_aderesi[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; aho_ijya_aderesi[514] = 바이트순서뒤집기(첫째값.aderesi); }
    return (uint32_t)개수;
}
imashini_Ijambo 도구전문접속번호(imashini_Ijambo dosiye_umukondo) {
    struct 자바주소 첫째값; unsigned uburebure_amakurushingiro = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, dosiye_umukondo, (imashini_Ijambo)&첫째값, (imashini_Ijambo)&uburebure_amakurushingiro);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
imashini_Ijambo 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
imashini_Ijambo 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
imashini_Ijambo 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
imashini_Ijambo 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
imashini_Ijambo 도구사각형(imashini_Ijambo Ihuza_rya_x, imashini_Ijambo 세로좌표, imashini_Ijambo 너비값, imashini_Ijambo 높이값, imashini_Ijambo 색상) {
    return (uint32_t)사용자호출(13, Ihuza_rya_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

imashini_Ijambo igikoresho_Stream(imashini_Ijambo Igikorwa,imashini_Ijambo dosiye_umukondo,imashini_Ijambo agaciro){
    if(Igikorwa==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(agaciro);
    if(Igikorwa==1){첫째값.aderesi=0;intptr_t 반환값=호출(33,dosiye_umukondo,(imashini_Ijambo)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,dosiye_umukondo,4,0));}
    if(Igikorwa==2)return (uint32_t)호출(37,dosiye_umukondo,(imashini_Ijambo)&첫째값,sizeof(첫째값));
    if(Igikorwa==3)return (uint32_t)호출(39,dosiye_umukondo,0,0);
    if(Igikorwa==4)return 도구전문접속번호(dosiye_umukondo);
    if(Igikorwa==5)return (uint32_t)호출(40,dosiye_umukondo,0,0);
    return (uint32_t)-22;
}
imashini_Ijambo igikoresho_GUI(imashini_Ijambo Igikorwa,imashini_Ijambo indanga_agaciro,imashini_Ijambo 첫째값,imashini_Ijambo 둘째값,imashini_Ijambo 문자값,imashini_Ijambo aho_ijya_amakurushingiro){return (uint32_t)사용자호출(20,Igikorwa,indanga_agaciro,첫째값,둘째값,문자값,aho_ijya_amakurushingiro);}
imashini_Ijambo igikoresho_GUI_SMS(imashini_Ijambo indanga_agaciro,imashini_Ijambo ARRAY_agaciro,imashini_Ijambo 개수){
    const imashini_Ijambo *원본주소=(const imashini_Ijambo *)ARRAY_agaciro;uint32_t amakurushingiro[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(imashini_Ijambo 순번=0;순번<개수;순번++){unsigned inyuguti_gusobeka=원본주소[순번+1];if(inyuguti_gusobeka>=0xd800&&inyuguti_gusobeka<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;inyuguti_gusobeka=0x10000+((inyuguti_gusobeka-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;amakurushingiro[항목수++]=inyuguti_gusobeka;}
    return (uint32_t)사용자호출(21,indanga_agaciro,(imashini_Ijambo)amakurushingiro,항목수,0,0,0);
}
