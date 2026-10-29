#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Faele/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "sehlopha.h"
typedef uintptr_t motšhene_Thalokontšu;
static int legoro_boleng;
static int 꾸러미사용중, 꾸러미인수이동;
static motšhene_Thalokontšu 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, motšhene_Thalokontšu 첫째값, motšhene_Thalokontšu 둘째값, motšhene_Thalokontšu khouto_ya_tlhaka) {
    return 사용자호출(개수, 첫째값, 둘째값, khouto_ya_tlhaka, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (motšhene_Thalokontšu)자료위치, 개수); }
static void tlhaka(unsigned khouto_ya_tlhaka) {
    unsigned char data[4]; unsigned 개수 = 0;
    if (khouto_ya_tlhaka < 128) data[개수++] = khouto_ya_tlhaka;
    else if (khouto_ya_tlhaka < 2048) { data[개수++] = 0xc0 | (khouto_ya_tlhaka >> 6); data[개수++] = 0x80 | (khouto_ya_tlhaka & 63); }
    else if (khouto_ya_tlhaka < 65536) { data[개수++] = 0xe0 | (khouto_ya_tlhaka >> 12); data[개수++] = 0x80 | ((khouto_ya_tlhaka >> 6) & 63); data[개수++] = 0x80 | (khouto_ya_tlhaka & 63); }
    else { data[개수++] = 0xf0 | (khouto_ya_tlhaka >> 18); data[개수++] = 0x80 | ((khouto_ya_tlhaka >> 12) & 63); data[개수++] = 0x80 | ((khouto_ya_tlhaka >> 6) & 63); data[개수++] = 0x80 | (khouto_ya_tlhaka & 63); }
    바이트들((const char *)data, 개수);
}
motšhene_Thalokontšu tholosi_tlhaka(motšhene_Thalokontšu boleng) {
    unsigned khouto_ya_tlhaka = boleng;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (khouto_ya_tlhaka >= 0xdc00 && khouto_ya_tlhaka <= 0xdfff) { tlhaka(0x10000 + ((높은부분 - 0xd800) << 10) + khouto_ya_tlhaka - 0xdc00); return 1; }
        tlhaka(0xfffd);
    }
    if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdbff) 대기중짝글자 = khouto_ya_tlhaka;
    else tlhaka(khouto_ya_tlhaka > 0x10ffff || (khouto_ya_tlhaka >= 0xdc00 && khouto_ya_tlhaka <= 0xdfff) ? 0xfffd : khouto_ya_tlhaka);
    return 1;
}
motšhene_Thalokontšu tholosi_gatiša(motšhene_Thalokontšu boleng) {
    const motšhene_Thalokontšu *molokoloko_data = (const motšhene_Thalokontšu *)boleng;
    for (motšhene_Thalokontšu 순번 = 0; 순번 < molokoloko_data[0]; 순번++) tholosi_tlhaka(molokoloko_data[순번 + 1]);
    return molokoloko_data[0];
}
static int Tsejana(motšhene_Thalokontšu selo_Dipadišo, char 결과자료[512]) {
    const motšhene_Thalokontšu *첫째값 = (const motšhene_Thalokontšu *)selo_Dipadišo;
    unsigned 사용량 = 0;
    for (motšhene_Thalokontšu 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned khouto_ya_tlhaka = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] mokgwa_mokgwa 경로와 호환한다.
        if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; khouto_ya_tlhaka = 0x10000 + ((khouto_ya_tlhaka - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdfff) return -22;
        unsigned 개수 = khouto_ya_tlhaka < 128 ? 1 : khouto_ya_tlhaka < 2048 ? 2 : khouto_ya_tlhaka < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = khouto_ya_tlhaka;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (khouto_ya_tlhaka >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((khouto_ya_tlhaka >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
motšhene_Thalokontšu tholosi_bula(motšhene_Thalokontšu Leina, motšhene_Thalokontšu 설정비트) {
    char 자료위치[512]; int Phošo = Tsejana(Leina, 자료위치);
    return (uint32_t)(Phošo ? Phošo : 호출(3, (motšhene_Thalokontšu)자료위치, 설정비트, 0));
}
motšhene_Thalokontšu tholosi_tswalela(motšhene_Thalokontšu faele_tshwaro) { return (uint32_t)호출(4, faele_tshwaro, 0, 0); }
motšhene_Thalokontšu 도구바이트읽기(motšhene_Thalokontšu faele_tshwaro) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, faele_tshwaro, (motšhene_Thalokontšu)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
motšhene_Thalokontšu tholosi_ngwala_paete(motšhene_Thalokontšu faele_tshwaro, motšhene_Thalokontšu boleng) {
    unsigned char 둘째값 = boleng; return (uint32_t)호출(1, faele_tshwaro, (motšhene_Thalokontšu)&둘째값, 1);
}
motšhene_Thalokontšu 도구읽기(motšhene_Thalokontšu Leina, motšhene_Thalokontšu boyo_data_atrese) {
    if (꾸러미사용중) {
        char 자료위치[512]; int Phošo = Tsejana(Leina, 자료위치); if (Phošo) return (uint32_t)Phošo;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; motšhene_Thalokontšu *목적위치 = (motšhene_Thalokontšu *)boyo_data_atrese;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int faele_tshwaro = 꾸러미사용중 ? -2 : (int32_t)tholosi_bula(Leina, 0);
    if (faele_tshwaro < 0) {
        char 자료위치[512]; int Phošo = Tsejana(Leina, 자료위치); if (Phošo) return (uint32_t)Phošo;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Leina; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            motšhene_Thalokontšu *목적위치 = (motšhene_Thalokontšu *)boyo_data_atrese;
            if (목적위치[0] < 자바클래스들[순번].Bogolo) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Bogolo; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Bogolo;
        }
        return (uint32_t)faele_tshwaro;
    }
    motšhene_Thalokontšu *첫째값 = (motšhene_Thalokontšu *)boyo_data_atrese;
    intptr_t Bogolo = 호출(9, faele_tshwaro, 0, 0), 완료량 = 0;
    if (Bogolo < 0 || (motšhene_Thalokontšu)Bogolo > 첫째값[0]) { tholosi_tswalela(faele_tshwaro); return (uint32_t)(Bogolo < 0 ? Bogolo : -27); }
    unsigned char data_thibela[256];
    while (완료량 < Bogolo) {
        intptr_t 개수 = 호출(2, faele_tshwaro, (motšhene_Thalokontšu)data_thibela, Bogolo - 완료량 < 256 ? Bogolo - 완료량 : 256);
        if (개수 <= 0) { tholosi_tswalela(faele_tshwaro); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = data_thibela[순번];
        완료량 += 개수;
    }
    tholosi_tswalela(faele_tshwaro); return 완료량;
}
motšhene_Thalokontšu tholosi_ngwala(motšhene_Thalokontšu Leina, motšhene_Thalokontšu 원본자료, motšhene_Thalokontšu 항목수) {
    const motšhene_Thalokontšu *첫째값 = (const motšhene_Thalokontšu *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int faele_tshwaro = (int32_t)tholosi_bula(Leina, 577); if (faele_tshwaro < 0) return (uint32_t)faele_tshwaro;
    unsigned char data_thibela[256]; motšhene_Thalokontšu 완료량 = 0;
    while (완료량 < 항목수) {
        motšhene_Thalokontšu 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (motšhene_Thalokontšu 순번 = 0; 순번 < 개수; 순번++) data_thibela[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, faele_tshwaro, (motšhene_Thalokontšu)data_thibela, 개수);
        if (결과 <= 0) { tholosi_tswalela(faele_tshwaro); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    tholosi_tswalela(faele_tshwaro); return 항목수;
}
motšhene_Thalokontšu 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
motšhene_Thalokontšu tholosi_akumente(motšhene_Thalokontšu 색인) {
    static const motšhene_Thalokontšu hloka_selo_boleng[1] = {0};
    if (색인 >= 8) return (motšhene_Thalokontšu)hloka_selo_boleng;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (motšhene_Thalokontšu)입력결과, sizeof(입력결과));
    if (개수 < 0) return (motšhene_Thalokontšu)hloka_selo_boleng;
    motšhene_Thalokontšu *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned khouto_ya_tlhaka = 입력결과[순번++], 더있음 = khouto_ya_tlhaka < 128 ? 0 : khouto_ya_tlhaka >= 0xc2 && khouto_ya_tlhaka < 0xe0 ? 1 : khouto_ya_tlhaka < 0xf0 && khouto_ya_tlhaka >= 0xe0 ? 2 : khouto_ya_tlhaka >= 0xf0 && khouto_ya_tlhaka <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) khouto_ya_tlhaka &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { khouto_ya_tlhaka = (khouto_ya_tlhaka << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || khouto_ya_tlhaka < 최소값 || khouto_ya_tlhaka > 0x10ffff || (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdfff)) khouto_ya_tlhaka = 0xfffd;
        if (khouto_ya_tlhaka >= 65536) { khouto_ya_tlhaka -= 65536; 결과자료[++항목수] = 0xd800 | (khouto_ya_tlhaka >> 10); 결과자료[++항목수] = 0xdc00 | (khouto_ya_tlhaka & 1023); }
        else 결과자료[++항목수] = khouto_ya_tlhaka;
    }
    결과자료[0] = 항목수; return (motšhene_Thalokontšu)결과자료;
}
motšhene_Thalokontšu 도구분류(void) { return legoro_boleng; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); tlhaka(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Thomišo_mošomiši_tirišo(int mokgwa_mokgwa) {
    legoro_boleng = mokgwa_mokgwa;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (motšhene_Thalokontšu)첫항목, sizeof(첫항목));
    if (mokgwa_mokgwa == 2 || (mokgwa_mokgwa == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = mokgwa_mokgwa == 2 ? 0 : 1;
        char faele_go_tsenya_tshedimošo_leina[256]; intptr_t botelele_data = 호출(15, 꾸러미인수이동, (motšhene_Thalokontšu)faele_go_tsenya_tshedimošo_leina, sizeof(faele_go_tsenya_tshedimošo_leina));
        if (botelele_data <= 0 || 꾸러미열기(faele_go_tsenya_tshedimošo_leina) < 0) {
            static const char Phošo[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Phošo, sizeof(Phošo) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) tlhaka(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Lapa, 접속번호; uint32_t atrese; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
motšhene_Thalokontšu 도구전문열기(motšhene_Thalokontšu 접속번호) {
    intptr_t faele_tshwaro = 호출(32, 2, 2, 17); if (faele_tshwaro < 0) return (uint32_t)faele_tshwaro;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.atrese = 0;
    intptr_t boemo_boleng = 호출(33, faele_tshwaro, (motšhene_Thalokontšu)&첫째값, sizeof(첫째값));
    if (boemo_boleng < 0) { tholosi_tswalela(faele_tshwaro); return (uint32_t)boemo_boleng; }
    return faele_tshwaro;
}
motšhene_Thalokontšu 도구전문보내기(motšhene_Thalokontšu faele_tshwaro, motšhene_Thalokontšu 접속번호, motšhene_Thalokontšu arei_boleng, motšhene_Thalokontšu botelele_boleng) {
    const motšhene_Thalokontšu *원본주소 = (const motšhene_Thalokontšu *)arei_boleng; unsigned char data[512];
    if (botelele_boleng > 512 || botelele_boleng > 원본주소[0]) return (uint32_t)-90;
    for (motšhene_Thalokontšu 순번 = 0; 순번 < botelele_boleng; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, faele_tshwaro, (motšhene_Thalokontšu)data, botelele_boleng, 0, (motšhene_Thalokontšu)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
motšhene_Thalokontšu 도구전문주소보내기(motšhene_Thalokontšu faele_tshwaro, motšhene_Thalokontšu atrese, motšhene_Thalokontšu 접속번호, motšhene_Thalokontšu arei_boleng, motšhene_Thalokontšu botelele_boleng) {
    const motšhene_Thalokontšu *원본주소 = (const motšhene_Thalokontšu *)arei_boleng; unsigned char data[512];
    if (botelele_boleng > 512 || botelele_boleng > 원본주소[0]) return (uint32_t)-90;
    for (motšhene_Thalokontšu 순번 = 0; 순번 < botelele_boleng; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.atrese = 바이트순서뒤집기(atrese);
    return (uint32_t)사용자호출(34, faele_tshwaro, (motšhene_Thalokontšu)data, botelele_boleng, 0, (motšhene_Thalokontšu)&첫째값, sizeof(첫째값));
}
motšhene_Thalokontšu tholosi_KGOKAGANYA(motšhene_Thalokontšu faele_tshwaro, motšhene_Thalokontšu atrese, motšhene_Thalokontšu 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.atrese = 바이트순서뒤집기(atrese);
    uint32_t Diriša = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, faele_tshwaro, (motšhene_Thalokontšu)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - Diriša) >= 1000) return (uint32_t)-110;
    }
}
motšhene_Thalokontšu 도구전문받기(motšhene_Thalokontšu faele_tshwaro, motšhene_Thalokontšu arei_boleng, motšhene_Thalokontšu 수용량) {
    motšhene_Thalokontšu *boyo_atrese = (motšhene_Thalokontšu *)arei_boleng; unsigned char data[512];
    if (수용량 > 512 || boyo_atrese[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned botelele_data = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, faele_tshwaro, (motšhene_Thalokontšu)data, 수용량, 0, (motšhene_Thalokontšu)&첫째값, (motšhene_Thalokontšu)&botelele_data);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) boyo_atrese[순번 + 1] = data[순번]; boyo_atrese[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; boyo_atrese[514] = 바이트순서뒤집기(첫째값.atrese); }
    return (uint32_t)개수;
}
motšhene_Thalokontšu 도구전문접속번호(motšhene_Thalokontšu faele_tshwaro) {
    struct 자바주소 첫째값; unsigned botelele_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, faele_tshwaro, (motšhene_Thalokontšu)&첫째값, (motšhene_Thalokontšu)&botelele_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
motšhene_Thalokontšu 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
motšhene_Thalokontšu 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
motšhene_Thalokontšu 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
motšhene_Thalokontšu 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
motšhene_Thalokontšu 도구사각형(motšhene_Thalokontšu kamano_ya_x, motšhene_Thalokontšu 세로좌표, motšhene_Thalokontšu 너비값, motšhene_Thalokontšu 높이값, motšhene_Thalokontšu 색상) {
    return (uint32_t)사용자호출(13, kamano_ya_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

motšhene_Thalokontšu tholosi_Stream(motšhene_Thalokontšu Mogato,motšhene_Thalokontšu faele_tshwaro,motšhene_Thalokontšu boleng){
    if(Mogato==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(boleng);
    if(Mogato==1){첫째값.atrese=0;intptr_t 반환값=호출(33,faele_tshwaro,(motšhene_Thalokontšu)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,faele_tshwaro,4,0));}
    if(Mogato==2)return (uint32_t)호출(37,faele_tshwaro,(motšhene_Thalokontšu)&첫째값,sizeof(첫째값));
    if(Mogato==3)return (uint32_t)호출(39,faele_tshwaro,0,0);
    if(Mogato==4)return 도구전문접속번호(faele_tshwaro);
    if(Mogato==5)return (uint32_t)호출(40,faele_tshwaro,0,0);
    return (uint32_t)-22;
}
motšhene_Thalokontšu tholosi_GUI(motšhene_Thalokontšu Mogato,motšhene_Thalokontšu sešupi_boleng,motšhene_Thalokontšu 첫째값,motšhene_Thalokontšu 둘째값,motšhene_Thalokontšu khouto_ya_tlhaka,motšhene_Thalokontšu boyo_data){return (uint32_t)사용자호출(20,Mogato,sešupi_boleng,첫째값,둘째값,khouto_ya_tlhaka,boyo_data);}
motšhene_Thalokontšu tholosi_GUI_SMS(motšhene_Thalokontšu sešupi_boleng,motšhene_Thalokontšu arei_boleng,motšhene_Thalokontšu 개수){
    const motšhene_Thalokontšu *원본주소=(const motšhene_Thalokontšu *)arei_boleng;uint32_t data[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(motšhene_Thalokontšu 순번=0;순번<개수;순번++){unsigned tlhaka_go_enkhouta=원본주소[순번+1];if(tlhaka_go_enkhouta>=0xd800&&tlhaka_go_enkhouta<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;tlhaka_go_enkhouta=0x10000+((tlhaka_go_enkhouta-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;data[항목수++]=tlhaka_go_enkhouta;}
    return (uint32_t)사용자호출(21,sešupi_boleng,(motšhene_Thalokontšu)data,항목수,0,0,0);
}
