#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Faịlụ/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "ngwungwu.h"
typedef uintptr_t ngwa_komputa_Mkpụrụokwu;
static int otu_valuu_4b6d6445;
static int 꾸러미사용중, 꾸러미인수이동;
static ngwa_komputa_Mkpụrụokwu 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, ngwa_komputa_Mkpụrụokwu 첫째값, ngwa_komputa_Mkpụrụokwu 둘째값, ngwa_komputa_Mkpụrụokwu koòdù_nkeakàrà) {
    return 사용자호출(개수, 첫째값, 둘째값, koòdù_nkeakàrà, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (ngwa_komputa_Mkpụrụokwu)자료위치, 개수); }
static void mkpụrụedemede(unsigned koòdù_nkeakàrà) {
    unsigned char datà[4]; unsigned 개수 = 0;
    if (koòdù_nkeakàrà < 128) datà[개수++] = koòdù_nkeakàrà;
    else if (koòdù_nkeakàrà < 2048) { datà[개수++] = 0xc0 | (koòdù_nkeakàrà >> 6); datà[개수++] = 0x80 | (koòdù_nkeakàrà & 63); }
    else if (koòdù_nkeakàrà < 65536) { datà[개수++] = 0xe0 | (koòdù_nkeakàrà >> 12); datà[개수++] = 0x80 | ((koòdù_nkeakàrà >> 6) & 63); datà[개수++] = 0x80 | (koòdù_nkeakàrà & 63); }
    else { datà[개수++] = 0xf0 | (koòdù_nkeakàrà >> 18); datà[개수++] = 0x80 | ((koòdù_nkeakàrà >> 12) & 63); datà[개수++] = 0x80 | ((koòdù_nkeakàrà >> 6) & 63); datà[개수++] = 0x80 | (koòdù_nkeakàrà & 63); }
    바이트들((const char *)datà, 개수);
}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_mkpụrụedemede(ngwa_komputa_Mkpụrụokwu valuu) {
    unsigned koòdù_nkeakàrà = valuu;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (koòdù_nkeakàrà >= 0xdc00 && koòdù_nkeakàrà <= 0xdfff) { mkpụrụedemede(0x10000 + ((높은부분 - 0xd800) << 10) + koòdù_nkeakàrà - 0xdc00); return 1; }
        mkpụrụedemede(0xfffd);
    }
    if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdbff) 대기중짝글자 = koòdù_nkeakàrà;
    else mkpụrụedemede(koòdù_nkeakàrà > 0x10ffff || (koòdù_nkeakàrà >= 0xdc00 && koòdù_nkeakàrà <= 0xdfff) ? 0xfffd : koòdù_nkeakàrà);
    return 1;
}
ngwa_komputa_Mkpụrụokwu 도구출력(ngwa_komputa_Mkpụrụokwu valuu) {
    const ngwa_komputa_Mkpụrụokwu *ùsòròokwū_datà = (const ngwa_komputa_Mkpụrụokwu *)valuu;
    for (ngwa_komputa_Mkpụrụokwu 순번 = 0; 순번 < ùsòròokwū_datà[0]; 순번++) ngwaọrụ_mkpụrụedemede(ùsòròokwū_datà[순번 + 1]);
    return ùsòròokwū_datà[0];
}
static int ụzọ_ozi(ngwa_komputa_Mkpụrụokwu ihe_Nrụtụ_aka, char 결과자료[512]) {
    const ngwa_komputa_Mkpụrụokwu *첫째값 = (const ngwa_komputa_Mkpụrụokwu *)ihe_Nrụtụ_aka;
    unsigned 사용량 = 0;
    for (ngwa_komputa_Mkpụrụokwu 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned koòdù_nkeakàrà = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] usoro_moòdù 경로와 호환한다.
        if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; koòdù_nkeakàrà = 0x10000 + ((koòdù_nkeakàrà - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdfff) return -22;
        unsigned 개수 = koòdù_nkeakàrà < 128 ? 1 : koòdù_nkeakàrà < 2048 ? 2 : koòdù_nkeakàrà < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = koòdù_nkeakàrà;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (koòdù_nkeakàrà >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((koòdù_nkeakàrà >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_mepee(ngwa_komputa_Mkpụrụokwu Aha, ngwa_komputa_Mkpụrụokwu 설정비트) {
    char 자료위치[512]; int mmejọ = ụzọ_ozi(Aha, 자료위치);
    return (uint32_t)(mmejọ ? mmejọ : 호출(3, (ngwa_komputa_Mkpụrụokwu)자료위치, 설정비트, 0));
}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_mmechi(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka) { return (uint32_t)호출(4, ọbọakwụkwọ_ebenjìaka, 0, 0); }
ngwa_komputa_Mkpụrụokwu 도구바이트읽기(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_dee_baịtị(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka, ngwa_komputa_Mkpụrụokwu valuu) {
    unsigned char 둘째값 = valuu; return (uint32_t)호출(1, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)&둘째값, 1);
}
ngwa_komputa_Mkpụrụokwu 도구읽기(ngwa_komputa_Mkpụrụokwu Aha, ngwa_komputa_Mkpụrụokwu ebemwèga_datà_àdreèsì) {
    if (꾸러미사용중) {
        char 자료위치[512]; int mmejọ = ụzọ_ozi(Aha, 자료위치); if (mmejọ) return (uint32_t)mmejọ;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; ngwa_komputa_Mkpụrụokwu *목적위치 = (ngwa_komputa_Mkpụrụokwu *)ebemwèga_datà_àdreèsì;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int ọbọakwụkwọ_ebenjìaka = 꾸러미사용중 ? -2 : (int32_t)ngwaọrụ_mepee(Aha, 0);
    if (ọbọakwụkwọ_ebenjìaka < 0) {
        char 자료위치[512]; int mmejọ = ụzọ_ozi(Aha, 자료위치); if (mmejọ) return (uint32_t)mmejọ;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Aha; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            ngwa_komputa_Mkpụrụokwu *목적위치 = (ngwa_komputa_Mkpụrụokwu *)ebemwèga_datà_àdreèsì;
            if (목적위치[0] < 자바클래스들[순번].Ụhara) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Ụhara; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].datà[안쪽순번];
            return 자바클래스들[순번].Ụhara;
        }
        return (uint32_t)ọbọakwụkwọ_ebenjìaka;
    }
    ngwa_komputa_Mkpụrụokwu *첫째값 = (ngwa_komputa_Mkpụrụokwu *)ebemwèga_datà_àdreèsì;
    intptr_t Ụhara = 호출(9, ọbọakwụkwọ_ebenjìaka, 0, 0), 완료량 = 0;
    if (Ụhara < 0 || (ngwa_komputa_Mkpụrụokwu)Ụhara > 첫째값[0]) { ngwaọrụ_mmechi(ọbọakwụkwọ_ebenjìaka); return (uint32_t)(Ụhara < 0 ? Ụhara : -27); }
    unsigned char datà_gbochie[256];
    while (완료량 < Ụhara) {
        intptr_t 개수 = 호출(2, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)datà_gbochie, Ụhara - 완료량 < 256 ? Ụhara - 완료량 : 256);
        if (개수 <= 0) { ngwaọrụ_mmechi(ọbọakwụkwọ_ebenjìaka); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = datà_gbochie[순번];
        완료량 += 개수;
    }
    ngwaọrụ_mmechi(ọbọakwụkwọ_ebenjìaka); return 완료량;
}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_dee(ngwa_komputa_Mkpụrụokwu Aha, ngwa_komputa_Mkpụrụokwu 원본자료, ngwa_komputa_Mkpụrụokwu 항목수) {
    const ngwa_komputa_Mkpụrụokwu *첫째값 = (const ngwa_komputa_Mkpụrụokwu *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int ọbọakwụkwọ_ebenjìaka = (int32_t)ngwaọrụ_mepee(Aha, 577); if (ọbọakwụkwọ_ebenjìaka < 0) return (uint32_t)ọbọakwụkwọ_ebenjìaka;
    unsigned char datà_gbochie[256]; ngwa_komputa_Mkpụrụokwu 완료량 = 0;
    while (완료량 < 항목수) {
        ngwa_komputa_Mkpụrụokwu 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (ngwa_komputa_Mkpụrụokwu 순번 = 0; 순번 < 개수; 순번++) datà_gbochie[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)datà_gbochie, 개수);
        if (결과 <= 0) { ngwaọrụ_mmechi(ọbọakwụkwọ_ebenjìaka); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    ngwaọrụ_mmechi(ọbọakwụkwọ_ebenjìaka); return 항목수;
}
ngwa_komputa_Mkpụrụokwu 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
ngwa_komputa_Mkpụrụokwu ngwaọrụ_agụment(ngwa_komputa_Mkpụrụokwu 색인) {
    static const ngwa_komputa_Mkpụrụokwu oghere_valuu_202e823e[1] = {0};
    if (색인 >= 8) return (ngwa_komputa_Mkpụrụokwu)oghere_valuu_202e823e;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (ngwa_komputa_Mkpụrụokwu)입력결과, sizeof(입력결과));
    if (개수 < 0) return (ngwa_komputa_Mkpụrụokwu)oghere_valuu_202e823e;
    ngwa_komputa_Mkpụrụokwu *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned koòdù_nkeakàrà = 입력결과[순번++], 더있음 = koòdù_nkeakàrà < 128 ? 0 : koòdù_nkeakàrà >= 0xc2 && koòdù_nkeakàrà < 0xe0 ? 1 : koòdù_nkeakàrà < 0xf0 && koòdù_nkeakàrà >= 0xe0 ? 2 : koòdù_nkeakàrà >= 0xf0 && koòdù_nkeakàrà <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) koòdù_nkeakàrà &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { koòdù_nkeakàrà = (koòdù_nkeakàrà << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || koòdù_nkeakàrà < 최소값 || koòdù_nkeakàrà > 0x10ffff || (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdfff)) koòdù_nkeakàrà = 0xfffd;
        if (koòdù_nkeakàrà >= 65536) { koòdù_nkeakàrà -= 65536; 결과자료[++항목수] = 0xd800 | (koòdù_nkeakàrà >> 10); 결과자료[++항목수] = 0xdc00 | (koòdù_nkeakàrà & 1023); }
        else 결과자료[++항목수] = koòdù_nkeakàrà;
    }
    결과자료[0] = 항목수; return (ngwa_komputa_Mkpụrụokwu)결과자료;
}
ngwa_komputa_Mkpụrụokwu 도구분류(void) { return otu_valuu_4b6d6445; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); mkpụrụedemede(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Mbido_òjìàrụ_app(int usoro_moòdù) {
    otu_valuu_4b6d6445 = usoro_moòdù;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (ngwa_komputa_Mkpụrụokwu)첫항목, sizeof(첫항목));
    if (usoro_moòdù == 2 || (usoro_moòdù == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = usoro_moòdù == 2 ? 0 : 1;
        char ọbọakwụkwọ_ndebà_akara_ahà[256]; intptr_t ogologo_datà = 호출(15, 꾸러미인수이동, (ngwa_komputa_Mkpụrụokwu)ọbọakwụkwọ_ndebà_akara_ahà, sizeof(ọbọakwụkwọ_ndebà_akara_ahà));
        if (ogologo_datà <= 0 || 꾸러미열기(ọbọakwụkwọ_ndebà_akara_ahà) < 0) {
            static const char mmejọ[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(mmejọ, sizeof(mmejọ) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) mkpụrụedemede(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Ezinụlọ, 접속번호; uint32_t àdreèsì; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
ngwa_komputa_Mkpụrụokwu 도구전문열기(ngwa_komputa_Mkpụrụokwu 접속번호) {
    intptr_t ọbọakwụkwọ_ebenjìaka = 호출(32, 2, 2, 17); if (ọbọakwụkwọ_ebenjìaka < 0) return (uint32_t)ọbọakwụkwọ_ebenjìaka;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.àdreèsì = 0;
    intptr_t ọnọdụ_valuu = 호출(33, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)&첫째값, sizeof(첫째값));
    if (ọnọdụ_valuu < 0) { ngwaọrụ_mmechi(ọbọakwụkwọ_ebenjìaka); return (uint32_t)ọnọdụ_valuu; }
    return ọbọakwụkwọ_ebenjìaka;
}
ngwa_komputa_Mkpụrụokwu 도구전문보내기(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka, ngwa_komputa_Mkpụrụokwu 접속번호, ngwa_komputa_Mkpụrụokwu MKPOKỌTA_valuu, ngwa_komputa_Mkpụrụokwu ogologo_valuu) {
    const ngwa_komputa_Mkpụrụokwu *원본주소 = (const ngwa_komputa_Mkpụrụokwu *)MKPOKỌTA_valuu; unsigned char datà[512];
    if (ogologo_valuu > 512 || ogologo_valuu > 원본주소[0]) return (uint32_t)-90;
    for (ngwa_komputa_Mkpụrụokwu 순번 = 0; 순번 < ogologo_valuu; 순번++) datà[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)datà, ogologo_valuu, 0, (ngwa_komputa_Mkpụrụokwu)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
ngwa_komputa_Mkpụrụokwu 도구전문주소보내기(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka, ngwa_komputa_Mkpụrụokwu àdreèsì, ngwa_komputa_Mkpụrụokwu 접속번호, ngwa_komputa_Mkpụrụokwu MKPOKỌTA_valuu, ngwa_komputa_Mkpụrụokwu ogologo_valuu) {
    const ngwa_komputa_Mkpụrụokwu *원본주소 = (const ngwa_komputa_Mkpụrụokwu *)MKPOKỌTA_valuu; unsigned char datà[512];
    if (ogologo_valuu > 512 || ogologo_valuu > 원본주소[0]) return (uint32_t)-90;
    for (ngwa_komputa_Mkpụrụokwu 순번 = 0; 순번 < ogologo_valuu; 순번++) datà[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.àdreèsì = 바이트순서뒤집기(àdreèsì);
    return (uint32_t)사용자호출(34, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)datà, ogologo_valuu, 0, (ngwa_komputa_Mkpụrụokwu)&첫째값, sizeof(첫째값));
}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_JIKỌ(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka, ngwa_komputa_Mkpụrụokwu àdreèsì, ngwa_komputa_Mkpụrụokwu 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.àdreèsì = 바이트순서뒤집기(àdreèsì);
    uint32_t Bido = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - Bido) >= 1000) return (uint32_t)-110;
    }
}
ngwa_komputa_Mkpụrụokwu 도구전문받기(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka, ngwa_komputa_Mkpụrụokwu MKPOKỌTA_valuu, ngwa_komputa_Mkpụrụokwu 수용량) {
    ngwa_komputa_Mkpụrụokwu *ebemwèga_àdreèsì = (ngwa_komputa_Mkpụrụokwu *)MKPOKỌTA_valuu; unsigned char datà[512];
    if (수용량 > 512 || ebemwèga_àdreèsì[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned ogologo_datà = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)datà, 수용량, 0, (ngwa_komputa_Mkpụrụokwu)&첫째값, (ngwa_komputa_Mkpụrụokwu)&ogologo_datà);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) ebemwèga_àdreèsì[순번 + 1] = datà[순번]; ebemwèga_àdreèsì[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; ebemwèga_àdreèsì[514] = 바이트순서뒤집기(첫째값.àdreèsì); }
    return (uint32_t)개수;
}
ngwa_komputa_Mkpụrụokwu 도구전문접속번호(ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka) {
    struct 자바주소 첫째값; unsigned ogologo_datà = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, ọbọakwụkwọ_ebenjìaka, (ngwa_komputa_Mkpụrụokwu)&첫째값, (ngwa_komputa_Mkpụrụokwu)&ogologo_datà);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
ngwa_komputa_Mkpụrụokwu 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
ngwa_komputa_Mkpụrụokwu 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
ngwa_komputa_Mkpụrụokwu 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
ngwa_komputa_Mkpụrụokwu 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
ngwa_komputa_Mkpụrụokwu 도구사각형(ngwa_komputa_Mkpụrụokwu ngakọrịta_x, ngwa_komputa_Mkpụrụokwu 세로좌표, ngwa_komputa_Mkpụrụokwu 너비값, ngwa_komputa_Mkpụrụokwu 높이값, ngwa_komputa_Mkpụrụokwu 색상) {
    return (uint32_t)사용자호출(13, ngakọrịta_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

ngwa_komputa_Mkpụrụokwu ngwaọrụ_agịrị(ngwa_komputa_Mkpụrụokwu mmèm,ngwa_komputa_Mkpụrụokwu ọbọakwụkwọ_ebenjìaka,ngwa_komputa_Mkpụrụokwu valuu){
    if(mmèm==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(valuu);
    if(mmèm==1){첫째값.àdreèsì=0;intptr_t 반환값=호출(33,ọbọakwụkwọ_ebenjìaka,(ngwa_komputa_Mkpụrụokwu)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,ọbọakwụkwọ_ebenjìaka,4,0));}
    if(mmèm==2)return (uint32_t)호출(37,ọbọakwụkwọ_ebenjìaka,(ngwa_komputa_Mkpụrụokwu)&첫째값,sizeof(첫째값));
    if(mmèm==3)return (uint32_t)호출(39,ọbọakwụkwọ_ebenjìaka,0,0);
    if(mmèm==4)return 도구전문접속번호(ọbọakwụkwọ_ebenjìaka);
    if(mmèm==5)return (uint32_t)호출(40,ọbọakwụkwọ_ebenjìaka,0,0);
    return (uint32_t)-22;
}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_GUI(ngwa_komputa_Mkpụrụokwu mmèm,ngwa_komputa_Mkpụrụokwu ihe_nkọwapụta_valuu,ngwa_komputa_Mkpụrụokwu 첫째값,ngwa_komputa_Mkpụrụokwu 둘째값,ngwa_komputa_Mkpụrụokwu koòdù_nkeakàrà,ngwa_komputa_Mkpụrụokwu ebemwèga_datà){return (uint32_t)사용자호출(20,mmèm,ihe_nkọwapụta_valuu,첫째값,둘째값,koòdù_nkeakàrà,ebemwèga_datà);}
ngwa_komputa_Mkpụrụokwu ngwaọrụ_GUI_SMS(ngwa_komputa_Mkpụrụokwu ihe_nkọwapụta_valuu,ngwa_komputa_Mkpụrụokwu MKPOKỌTA_valuu,ngwa_komputa_Mkpụrụokwu 개수){
    const ngwa_komputa_Mkpụrụokwu *원본주소=(const ngwa_komputa_Mkpụrụokwu *)MKPOKỌTA_valuu;uint32_t datà[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(ngwa_komputa_Mkpụrụokwu 순번=0;순번<개수;순번++){unsigned mkpụrụedemede_ntinye_koòdù=원본주소[순번+1];if(mkpụrụedemede_ntinye_koòdù>=0xd800&&mkpụrụedemede_ntinye_koòdù<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;mkpụrụedemede_ntinye_koòdù=0x10000+((mkpụrụedemede_ntinye_koòdù-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;datà[항목수++]=mkpụrụedemede_ntinye_koòdù;}
    return (uint32_t)사용자호출(21,ihe_nkọwapụta_valuu,(ngwa_komputa_Mkpụrụokwu)datà,항목수,0,0,0);
}
