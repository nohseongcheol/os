#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 faele/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "ngatanngwe.h"
typedef uintptr_t motšhine_Lefoko;
static int setlhopha_Boleng_4b6d6445;
static int 꾸러미사용중, 꾸러미인수이동;
static motšhine_Lefoko 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, motšhine_Lefoko 첫째값, motšhine_Lefoko 둘째값, motšhine_Lefoko khoutuletshwao) {
    return 사용자호출(개수, 첫째값, 둘째값, khoutuletshwao, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (motšhine_Lefoko)자료위치, 개수); }
static void Letshwao(unsigned khoutuletshwao) {
    unsigned char tshedimosetso[4]; unsigned 개수 = 0;
    if (khoutuletshwao < 128) tshedimosetso[개수++] = khoutuletshwao;
    else if (khoutuletshwao < 2048) { tshedimosetso[개수++] = 0xc0 | (khoutuletshwao >> 6); tshedimosetso[개수++] = 0x80 | (khoutuletshwao & 63); }
    else if (khoutuletshwao < 65536) { tshedimosetso[개수++] = 0xe0 | (khoutuletshwao >> 12); tshedimosetso[개수++] = 0x80 | ((khoutuletshwao >> 6) & 63); tshedimosetso[개수++] = 0x80 | (khoutuletshwao & 63); }
    else { tshedimosetso[개수++] = 0xf0 | (khoutuletshwao >> 18); tshedimosetso[개수++] = 0x80 | ((khoutuletshwao >> 12) & 63); tshedimosetso[개수++] = 0x80 | ((khoutuletshwao >> 6) & 63); tshedimosetso[개수++] = 0x80 | (khoutuletshwao & 63); }
    바이트들((const char *)tshedimosetso, 개수);
}
motšhine_Lefoko sediriswa_Letshwao(motšhine_Lefoko Boleng) {
    unsigned khoutuletshwao = Boleng;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (khoutuletshwao >= 0xdc00 && khoutuletshwao <= 0xdfff) { Letshwao(0x10000 + ((높은부분 - 0xd800) << 10) + khoutuletshwao - 0xdc00); return 1; }
        Letshwao(0xfffd);
    }
    if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdbff) 대기중짝글자 = khoutuletshwao;
    else Letshwao(khoutuletshwao > 0x10ffff || (khoutuletshwao >= 0xdc00 && khoutuletshwao <= 0xdfff) ? 0xfffd : khoutuletshwao);
    return 1;
}
motšhine_Lefoko 도구출력(motšhine_Lefoko Boleng) {
    const motšhine_Lefoko *dikwalwa_tshedimosetso = (const motšhine_Lefoko *)Boleng;
    for (motšhine_Lefoko 순번 = 0; 순번 < dikwalwa_tshedimosetso[0]; 순번++) sediriswa_Letshwao(dikwalwa_tshedimosetso[순번 + 1]);
    return dikwalwa_tshedimosetso[0];
}
static int tsela(motšhine_Lefoko selwana_Tshupiso, char 결과자료[512]) {
    const motšhine_Lefoko *첫째값 = (const motšhine_Lefoko *)selwana_Tshupiso;
    unsigned 사용량 = 0;
    for (motšhine_Lefoko 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned khoutuletshwao = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] mokgwa_mokgwa 경로와 호환한다.
        if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; khoutuletshwao = 0x10000 + ((khoutuletshwao - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdfff) return -22;
        unsigned 개수 = khoutuletshwao < 128 ? 1 : khoutuletshwao < 2048 ? 2 : khoutuletshwao < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = khoutuletshwao;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (khoutuletshwao >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((khoutuletshwao >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
motšhine_Lefoko sediriswa_bula(motšhine_Lefoko leina, motšhine_Lefoko 설정비트) {
    char 자료위치[512]; int phoso = tsela(leina, 자료위치);
    return (uint32_t)(phoso ? phoso : 호출(3, (motšhine_Lefoko)자료위치, 설정비트, 0));
}
motšhine_Lefoko sediriswa_tswala(motšhine_Lefoko faele_mokgwakamogelo) { return (uint32_t)호출(4, faele_mokgwakamogelo, 0, 0); }
motšhine_Lefoko 도구바이트읽기(motšhine_Lefoko faele_mokgwakamogelo) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, faele_mokgwakamogelo, (motšhine_Lefoko)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
motšhine_Lefoko sediriswa_kwala_baete(motšhine_Lefoko faele_mokgwakamogelo, motšhine_Lefoko Boleng) {
    unsigned char 둘째값 = Boleng; return (uint32_t)호출(1, faele_mokgwakamogelo, (motšhine_Lefoko)&둘째값, 1);
}
motšhine_Lefoko 도구읽기(motšhine_Lefoko leina, motšhine_Lefoko bogorogelo_tshedimosetso_aterese) {
    if (꾸러미사용중) {
        char 자료위치[512]; int phoso = tsela(leina, 자료위치); if (phoso) return (uint32_t)phoso;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; motšhine_Lefoko *목적위치 = (motšhine_Lefoko *)bogorogelo_tshedimosetso_aterese;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int faele_mokgwakamogelo = 꾸러미사용중 ? -2 : (int32_t)sediriswa_bula(leina, 0);
    if (faele_mokgwakamogelo < 0) {
        char 자료위치[512]; int phoso = tsela(leina, 자료위치); if (phoso) return (uint32_t)phoso;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].leina; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            motšhine_Lefoko *목적위치 = (motšhine_Lefoko *)bogorogelo_tshedimosetso_aterese;
            if (목적위치[0] < 자바클래스들[순번].lekanya) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].lekanya; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].tshedimosetso[안쪽순번];
            return 자바클래스들[순번].lekanya;
        }
        return (uint32_t)faele_mokgwakamogelo;
    }
    motšhine_Lefoko *첫째값 = (motšhine_Lefoko *)bogorogelo_tshedimosetso_aterese;
    intptr_t lekanya = 호출(9, faele_mokgwakamogelo, 0, 0), 완료량 = 0;
    if (lekanya < 0 || (motšhine_Lefoko)lekanya > 첫째값[0]) { sediriswa_tswala(faele_mokgwakamogelo); return (uint32_t)(lekanya < 0 ? lekanya : -27); }
    unsigned char tshedimosetso_thibela[256];
    while (완료량 < lekanya) {
        intptr_t 개수 = 호출(2, faele_mokgwakamogelo, (motšhine_Lefoko)tshedimosetso_thibela, lekanya - 완료량 < 256 ? lekanya - 완료량 : 256);
        if (개수 <= 0) { sediriswa_tswala(faele_mokgwakamogelo); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = tshedimosetso_thibela[순번];
        완료량 += 개수;
    }
    sediriswa_tswala(faele_mokgwakamogelo); return 완료량;
}
motšhine_Lefoko sediriswa_kwala(motšhine_Lefoko leina, motšhine_Lefoko 원본자료, motšhine_Lefoko 항목수) {
    const motšhine_Lefoko *첫째값 = (const motšhine_Lefoko *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int faele_mokgwakamogelo = (int32_t)sediriswa_bula(leina, 577); if (faele_mokgwakamogelo < 0) return (uint32_t)faele_mokgwakamogelo;
    unsigned char tshedimosetso_thibela[256]; motšhine_Lefoko 완료량 = 0;
    while (완료량 < 항목수) {
        motšhine_Lefoko 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (motšhine_Lefoko 순번 = 0; 순번 < 개수; 순번++) tshedimosetso_thibela[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, faele_mokgwakamogelo, (motšhine_Lefoko)tshedimosetso_thibela, 개수);
        if (결과 <= 0) { sediriswa_tswala(faele_mokgwakamogelo); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    sediriswa_tswala(faele_mokgwakamogelo); return 항목수;
}
motšhine_Lefoko 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
motšhine_Lefoko sediriswa_Thulaganyo(motšhine_Lefoko 색인) {
    static const motšhine_Lefoko lolea_Boleng[1] = {0};
    if (색인 >= 8) return (motšhine_Lefoko)lolea_Boleng;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (motšhine_Lefoko)입력결과, sizeof(입력결과));
    if (개수 < 0) return (motšhine_Lefoko)lolea_Boleng;
    motšhine_Lefoko *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned khoutuletshwao = 입력결과[순번++], 더있음 = khoutuletshwao < 128 ? 0 : khoutuletshwao >= 0xc2 && khoutuletshwao < 0xe0 ? 1 : khoutuletshwao < 0xf0 && khoutuletshwao >= 0xe0 ? 2 : khoutuletshwao >= 0xf0 && khoutuletshwao <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) khoutuletshwao &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { khoutuletshwao = (khoutuletshwao << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || khoutuletshwao < 최소값 || khoutuletshwao > 0x10ffff || (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdfff)) khoutuletshwao = 0xfffd;
        if (khoutuletshwao >= 65536) { khoutuletshwao -= 65536; 결과자료[++항목수] = 0xd800 | (khoutuletshwao >> 10); 결과자료[++항목수] = 0xdc00 | (khoutuletshwao & 1023); }
        else 결과자료[++항목수] = khoutuletshwao;
    }
    결과자료[0] = 항목수; return (motšhine_Lefoko)결과자료;
}
motšhine_Lefoko 도구분류(void) { return setlhopha_Boleng_4b6d6445; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); Letshwao(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int simolola_modirisi_Tiriso(int mokgwa_mokgwa) {
    setlhopha_Boleng_4b6d6445 = mokgwa_mokgwa;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (motšhine_Lefoko)첫항목, sizeof(첫항목));
    if (mokgwa_mokgwa == 2 || (mokgwa_mokgwa == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = mokgwa_mokgwa == 2 ? 0 : 1;
        char faele_tsenyo_leina[256]; intptr_t boleele_tshedimosetso = 호출(15, 꾸러미인수이동, (motšhine_Lefoko)faele_tsenyo_leina, sizeof(faele_tsenyo_leina));
        if (boleele_tshedimosetso <= 0 || 꾸러미열기(faele_tsenyo_leina) < 0) {
            static const char phoso[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(phoso, sizeof(phoso) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) Letshwao(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 ga_jaana_selwana 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Lelapa, 접속번호; uint32_t aterese; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
motšhine_Lefoko 도구전문열기(motšhine_Lefoko 접속번호) {
    intptr_t faele_mokgwakamogelo = 호출(32, 2, 2, 17); if (faele_mokgwakamogelo < 0) return (uint32_t)faele_mokgwakamogelo;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.aterese = 0;
    intptr_t kemo_Boleng = 호출(33, faele_mokgwakamogelo, (motšhine_Lefoko)&첫째값, sizeof(첫째값));
    if (kemo_Boleng < 0) { sediriswa_tswala(faele_mokgwakamogelo); return (uint32_t)kemo_Boleng; }
    return faele_mokgwakamogelo;
}
motšhine_Lefoko 도구전문보내기(motšhine_Lefoko faele_mokgwakamogelo, motšhine_Lefoko 접속번호, motšhine_Lefoko setlhopha_Boleng_ed437109, motšhine_Lefoko boleele_Boleng) {
    const motšhine_Lefoko *원본주소 = (const motšhine_Lefoko *)setlhopha_Boleng_ed437109; unsigned char tshedimosetso[512];
    if (boleele_Boleng > 512 || boleele_Boleng > 원본주소[0]) return (uint32_t)-90;
    for (motšhine_Lefoko 순번 = 0; 순번 < boleele_Boleng; 순번++) tshedimosetso[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, faele_mokgwakamogelo, (motšhine_Lefoko)tshedimosetso, boleele_Boleng, 0, (motšhine_Lefoko)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
motšhine_Lefoko 도구전문주소보내기(motšhine_Lefoko faele_mokgwakamogelo, motšhine_Lefoko aterese, motšhine_Lefoko 접속번호, motšhine_Lefoko setlhopha_Boleng_ed437109, motšhine_Lefoko boleele_Boleng) {
    const motšhine_Lefoko *원본주소 = (const motšhine_Lefoko *)setlhopha_Boleng_ed437109; unsigned char tshedimosetso[512];
    if (boleele_Boleng > 512 || boleele_Boleng > 원본주소[0]) return (uint32_t)-90;
    for (motšhine_Lefoko 순번 = 0; 순번 < boleele_Boleng; 순번++) tshedimosetso[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.aterese = 바이트순서뒤집기(aterese);
    return (uint32_t)사용자호출(34, faele_mokgwakamogelo, (motšhine_Lefoko)tshedimosetso, boleele_Boleng, 0, (motšhine_Lefoko)&첫째값, sizeof(첫째값));
}
motšhine_Lefoko sediriswa_Golaganya(motšhine_Lefoko faele_mokgwakamogelo, motšhine_Lefoko aterese, motšhine_Lefoko 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.aterese = 바이트순서뒤집기(aterese);
    uint32_t dirisa = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, faele_mokgwakamogelo, (motšhine_Lefoko)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - dirisa) >= 1000) return (uint32_t)-110;
    }
}
motšhine_Lefoko 도구전문받기(motšhine_Lefoko faele_mokgwakamogelo, motšhine_Lefoko setlhopha_Boleng_ed437109, motšhine_Lefoko 수용량) {
    motšhine_Lefoko *bogorogelo_aterese = (motšhine_Lefoko *)setlhopha_Boleng_ed437109; unsigned char tshedimosetso[512];
    if (수용량 > 512 || bogorogelo_aterese[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned boleele_tshedimosetso = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, faele_mokgwakamogelo, (motšhine_Lefoko)tshedimosetso, 수용량, 0, (motšhine_Lefoko)&첫째값, (motšhine_Lefoko)&boleele_tshedimosetso);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) bogorogelo_aterese[순번 + 1] = tshedimosetso[순번]; bogorogelo_aterese[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; bogorogelo_aterese[514] = 바이트순서뒤집기(첫째값.aterese); }
    return (uint32_t)개수;
}
motšhine_Lefoko 도구전문접속번호(motšhine_Lefoko faele_mokgwakamogelo) {
    struct 자바주소 첫째값; unsigned boleele_tshedimosetso = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, faele_mokgwakamogelo, (motšhine_Lefoko)&첫째값, (motšhine_Lefoko)&boleele_tshedimosetso);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
motšhine_Lefoko 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
motšhine_Lefoko 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
motšhine_Lefoko 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
motšhine_Lefoko 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
motšhine_Lefoko 도구사각형(motšhine_Lefoko kgokagano_ya_x, motšhine_Lefoko 세로좌표, motšhine_Lefoko 너비값, motšhine_Lefoko 높이값, motšhine_Lefoko 색상) {
    return (uint32_t)사용자호출(13, kgokagano_ya_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

motšhine_Lefoko sediriswa_moela(motšhine_Lefoko tiro,motšhine_Lefoko faele_mokgwakamogelo,motšhine_Lefoko Boleng){
    if(tiro==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(Boleng);
    if(tiro==1){첫째값.aterese=0;intptr_t 반환값=호출(33,faele_mokgwakamogelo,(motšhine_Lefoko)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,faele_mokgwakamogelo,4,0));}
    if(tiro==2)return (uint32_t)호출(37,faele_mokgwakamogelo,(motšhine_Lefoko)&첫째값,sizeof(첫째값));
    if(tiro==3)return (uint32_t)호출(39,faele_mokgwakamogelo,0,0);
    if(tiro==4)return 도구전문접속번호(faele_mokgwakamogelo);
    if(tiro==5)return (uint32_t)호출(40,faele_mokgwakamogelo,0,0);
    return (uint32_t)-22;
}
motšhine_Lefoko sediriswa_GUI(motšhine_Lefoko tiro,motšhine_Lefoko setlhaodi_Boleng,motšhine_Lefoko 첫째값,motšhine_Lefoko 둘째값,motšhine_Lefoko khoutuletshwao,motšhine_Lefoko bogorogelo_tshedimosetso){return (uint32_t)사용자호출(20,tiro,setlhaodi_Boleng,첫째값,둘째값,khoutuletshwao,bogorogelo_tshedimosetso);}
motšhine_Lefoko sediriswa_GUI_SMS(motšhine_Lefoko setlhaodi_Boleng,motšhine_Lefoko setlhopha_Boleng_ed437109,motšhine_Lefoko 개수){
    const motšhine_Lefoko *원본주소=(const motšhine_Lefoko *)setlhopha_Boleng_ed437109;uint32_t tshedimosetso[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(motšhine_Lefoko 순번=0;순번<개수;순번++){unsigned Letshwao_khoutufatso=원본주소[순번+1];if(Letshwao_khoutufatso>=0xd800&&Letshwao_khoutufatso<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;Letshwao_khoutufatso=0x10000+((Letshwao_khoutufatso-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;tshedimosetso[항목수++]=Letshwao_khoutufatso;}
    return (uint32_t)사용자호출(21,setlhaodi_Boleng,(motšhine_Lefoko)tshedimosetso,항목수,0,0,0);
}
