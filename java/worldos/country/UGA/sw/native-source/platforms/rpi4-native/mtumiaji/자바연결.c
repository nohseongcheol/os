#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 faili/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "fungasha.h"
typedef uintptr_t mashine_Neno;
static int kategoria_thamani;
static int 꾸러미사용중, 꾸러미인수이동;
static mashine_Neno 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, mashine_Neno 첫째값, mashine_Neno 둘째값, mashine_Neno msimbo_wa_kibambo) {
    return 사용자호출(개수, 첫째값, 둘째값, msimbo_wa_kibambo, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (mashine_Neno)자료위치, 개수); }
static void kibambo(unsigned msimbo_wa_kibambo) {
    unsigned char data[4]; unsigned 개수 = 0;
    if (msimbo_wa_kibambo < 128) data[개수++] = msimbo_wa_kibambo;
    else if (msimbo_wa_kibambo < 2048) { data[개수++] = 0xc0 | (msimbo_wa_kibambo >> 6); data[개수++] = 0x80 | (msimbo_wa_kibambo & 63); }
    else if (msimbo_wa_kibambo < 65536) { data[개수++] = 0xe0 | (msimbo_wa_kibambo >> 12); data[개수++] = 0x80 | ((msimbo_wa_kibambo >> 6) & 63); data[개수++] = 0x80 | (msimbo_wa_kibambo & 63); }
    else { data[개수++] = 0xf0 | (msimbo_wa_kibambo >> 18); data[개수++] = 0x80 | ((msimbo_wa_kibambo >> 12) & 63); data[개수++] = 0x80 | ((msimbo_wa_kibambo >> 6) & 63); data[개수++] = 0x80 | (msimbo_wa_kibambo & 63); }
    바이트들((const char *)data, 개수);
}
mashine_Neno zana_kibambo(mashine_Neno thamani) {
    unsigned msimbo_wa_kibambo = thamani;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (msimbo_wa_kibambo >= 0xdc00 && msimbo_wa_kibambo <= 0xdfff) { kibambo(0x10000 + ((높은부분 - 0xd800) << 10) + msimbo_wa_kibambo - 0xdc00); return 1; }
        kibambo(0xfffd);
    }
    if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdbff) 대기중짝글자 = msimbo_wa_kibambo;
    else kibambo(msimbo_wa_kibambo > 0x10ffff || (msimbo_wa_kibambo >= 0xdc00 && msimbo_wa_kibambo <= 0xdfff) ? 0xfffd : msimbo_wa_kibambo);
    return 1;
}
mashine_Neno 도구출력(mashine_Neno thamani) {
    const mashine_Neno *tungo_data = (const mashine_Neno *)thamani;
    for (mashine_Neno 순번 = 0; 순번 < tungo_data[0]; 순번++) zana_kibambo(tungo_data[순번 + 1]);
    return tungo_data[0];
}
static int njia(mashine_Neno kipengee_Marejeleo, char 결과자료[512]) {
    const mashine_Neno *첫째값 = (const mashine_Neno *)kipengee_Marejeleo;
    unsigned 사용량 = 0;
    for (mashine_Neno 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned msimbo_wa_kibambo = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] mbinu_hali_tumizi 경로와 호환한다.
        if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; msimbo_wa_kibambo = 0x10000 + ((msimbo_wa_kibambo - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdfff) return -22;
        unsigned 개수 = msimbo_wa_kibambo < 128 ? 1 : msimbo_wa_kibambo < 2048 ? 2 : msimbo_wa_kibambo < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = msimbo_wa_kibambo;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (msimbo_wa_kibambo >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((msimbo_wa_kibambo >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
mashine_Neno zana_unda(mashine_Neno Jina, mashine_Neno usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma) {
    char 자료위치[512]; int kosa = njia(Jina, 자료위치);
    return (uint32_t)(kosa ? kosa : 호출(3, (mashine_Neno)자료위치, usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma, 0));
}
mashine_Neno zana_funga(mashine_Neno faili_kishiko) { return (uint32_t)호출(4, faili_kishiko, 0, 0); }
mashine_Neno 도구바이트읽기(mashine_Neno faili_kishiko) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, faili_kishiko, (mashine_Neno)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
mashine_Neno zana_andika_baiti(mashine_Neno faili_kishiko, mashine_Neno thamani) {
    unsigned char 둘째값 = thamani; return (uint32_t)호출(1, faili_kishiko, (mashine_Neno)&둘째값, 1);
}
mashine_Neno 도구읽기(mashine_Neno Jina, mashine_Neno fikio_data_anwani) {
    if (꾸러미사용중) {
        char 자료위치[512]; int kosa = njia(Jina, 자료위치); if (kosa) return (uint32_t)kosa;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; mashine_Neno *목적위치 = (mashine_Neno *)fikio_data_anwani;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int faili_kishiko = 꾸러미사용중 ? -2 : (int32_t)zana_unda(Jina, 0);
    if (faili_kishiko < 0) {
        char 자료위치[512]; int kosa = njia(Jina, 자료위치); if (kosa) return (uint32_t)kosa;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Jina; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            mashine_Neno *목적위치 = (mashine_Neno *)fikio_data_anwani;
            if (목적위치[0] < 자바클래스들[순번].panga_ukubwa) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].panga_ukubwa; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].panga_ukubwa;
        }
        return (uint32_t)faili_kishiko;
    }
    mashine_Neno *첫째값 = (mashine_Neno *)fikio_data_anwani;
    intptr_t panga_ukubwa = 호출(9, faili_kishiko, 0, 0), 완료량 = 0;
    if (panga_ukubwa < 0 || (mashine_Neno)panga_ukubwa > 첫째값[0]) { zana_funga(faili_kishiko); return (uint32_t)(panga_ukubwa < 0 ? panga_ukubwa : -27); }
    unsigned char data_zuia[256];
    while (완료량 < panga_ukubwa) {
        intptr_t 개수 = 호출(2, faili_kishiko, (mashine_Neno)data_zuia, panga_ukubwa - 완료량 < 256 ? panga_ukubwa - 완료량 : 256);
        if (개수 <= 0) { zana_funga(faili_kishiko); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = data_zuia[순번];
        완료량 += 개수;
    }
    zana_funga(faili_kishiko); return 완료량;
}
mashine_Neno zana_andika(mashine_Neno Jina, mashine_Neno 원본자료, mashine_Neno 항목수) {
    const mashine_Neno *첫째값 = (const mashine_Neno *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int faili_kishiko = (int32_t)zana_unda(Jina, 577); if (faili_kishiko < 0) return (uint32_t)faili_kishiko;
    unsigned char data_zuia[256]; mashine_Neno 완료량 = 0;
    while (완료량 < 항목수) {
        mashine_Neno 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (mashine_Neno 순번 = 0; 순번 < 개수; 순번++) data_zuia[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, faili_kishiko, (mashine_Neno)data_zuia, 개수);
        if (결과 <= 0) { zana_funga(faili_kishiko); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    zana_funga(faili_kishiko); return 항목수;
}
mashine_Neno 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mashine_Neno zana_hoja(mashine_Neno 색인) {
    static const mashine_Neno tupu_thamani[1] = {0};
    if (색인 >= 8) return (mashine_Neno)tupu_thamani;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mashine_Neno)입력결과, sizeof(입력결과));
    if (개수 < 0) return (mashine_Neno)tupu_thamani;
    mashine_Neno *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned msimbo_wa_kibambo = 입력결과[순번++], 더있음 = msimbo_wa_kibambo < 128 ? 0 : msimbo_wa_kibambo >= 0xc2 && msimbo_wa_kibambo < 0xe0 ? 1 : msimbo_wa_kibambo < 0xf0 && msimbo_wa_kibambo >= 0xe0 ? 2 : msimbo_wa_kibambo >= 0xf0 && msimbo_wa_kibambo <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) msimbo_wa_kibambo &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { msimbo_wa_kibambo = (msimbo_wa_kibambo << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || msimbo_wa_kibambo < 최소값 || msimbo_wa_kibambo > 0x10ffff || (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdfff)) msimbo_wa_kibambo = 0xfffd;
        if (msimbo_wa_kibambo >= 65536) { msimbo_wa_kibambo -= 65536; 결과자료[++항목수] = 0xd800 | (msimbo_wa_kibambo >> 10); 결과자료[++항목수] = 0xdc00 | (msimbo_wa_kibambo & 1023); }
        else 결과자료[++항목수] = msimbo_wa_kibambo;
    }
    결과자료[0] = 항목수; return (mashine_Neno)결과자료;
}
mashine_Neno 도구분류(void) { return kategoria_thamani; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); kibambo(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Anza_mtumiaji_programu(int mbinu_hali_tumizi) {
    kategoria_thamani = mbinu_hali_tumizi;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (mashine_Neno)첫항목, sizeof(첫항목));
    if (mbinu_hali_tumizi == 2 || (mbinu_hali_tumizi == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = mbinu_hali_tumizi == 2 ? 0 : 1;
        char faili_ingizo_jina[256]; intptr_t urefu_data = 호출(15, 꾸러미인수이동, (mashine_Neno)faili_ingizo_jina, sizeof(faili_ingizo_jina));
        if (urefu_data <= 0 || 꾸러미열기(faili_ingizo_jina) < 0) {
            static const char kosa[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(kosa, sizeof(kosa) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) kibambo(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Familia, namba_ya_kituo; uint32_t anwani; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned namba_ya_kituo) {
    struct 자바주소 첫째값 = {2, (uint16_t)((namba_ya_kituo << 8) | (namba_ya_kituo >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mashine_Neno 도구전문열기(mashine_Neno namba_ya_kituo) {
    intptr_t faili_kishiko = 호출(32, 2, 2, 17); if (faili_kishiko < 0) return (uint32_t)faili_kishiko;
    struct 자바주소 첫째값 = 전문주소(namba_ya_kituo);
    첫째값.anwani = 0;
    intptr_t hali_thamani = 호출(33, faili_kishiko, (mashine_Neno)&첫째값, sizeof(첫째값));
    if (hali_thamani < 0) { zana_funga(faili_kishiko); return (uint32_t)hali_thamani; }
    return faili_kishiko;
}
mashine_Neno 도구전문보내기(mashine_Neno faili_kishiko, mashine_Neno namba_ya_kituo, mashine_Neno ARRAY_thamani, mashine_Neno urefu_thamani) {
    const mashine_Neno *원본주소 = (const mashine_Neno *)ARRAY_thamani; unsigned char data[512];
    if (urefu_thamani > 512 || urefu_thamani > 원본주소[0]) return (uint32_t)-90;
    for (mashine_Neno 순번 = 0; 순번 < urefu_thamani; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(namba_ya_kituo);
    return (uint32_t)사용자호출(34, faili_kishiko, (mashine_Neno)data, urefu_thamani, 0, (mashine_Neno)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
mashine_Neno 도구전문주소보내기(mashine_Neno faili_kishiko, mashine_Neno anwani, mashine_Neno namba_ya_kituo, mashine_Neno ARRAY_thamani, mashine_Neno urefu_thamani) {
    const mashine_Neno *원본주소 = (const mashine_Neno *)ARRAY_thamani; unsigned char data[512];
    if (urefu_thamani > 512 || urefu_thamani > 원본주소[0]) return (uint32_t)-90;
    for (mashine_Neno 순번 = 0; 순번 < urefu_thamani; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(namba_ya_kituo); 첫째값.anwani = 바이트순서뒤집기(anwani);
    return (uint32_t)사용자호출(34, faili_kishiko, (mashine_Neno)data, urefu_thamani, 0, (mashine_Neno)&첫째값, sizeof(첫째값));
}
mashine_Neno zana_UNGANISHA(mashine_Neno faili_kishiko, mashine_Neno anwani, mashine_Neno namba_ya_kituo) {
    struct 자바주소 첫째값 = 전문주소(namba_ya_kituo); 첫째값.anwani = 바이트순서뒤집기(anwani);
    uint32_t endesha = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, faili_kishiko, (mashine_Neno)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - endesha) >= 1000) return (uint32_t)-110;
    }
}
mashine_Neno 도구전문받기(mashine_Neno faili_kishiko, mashine_Neno ARRAY_thamani, mashine_Neno 수용량) {
    mashine_Neno *fikio_anwani = (mashine_Neno *)ARRAY_thamani; unsigned char data[512];
    if (수용량 > 512 || fikio_anwani[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned urefu_data = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, faili_kishiko, (mashine_Neno)data, 수용량, 0, (mashine_Neno)&첫째값, (mashine_Neno)&urefu_data);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) fikio_anwani[순번 + 1] = data[순번]; fikio_anwani[513] = (첫째값.namba_ya_kituo << 8 | 첫째값.namba_ya_kituo >> 8) & 65535; fikio_anwani[514] = 바이트순서뒤집기(첫째값.anwani); }
    return (uint32_t)개수;
}
mashine_Neno 도구전문접속번호(mashine_Neno faili_kishiko) {
    struct 자바주소 첫째값; unsigned urefu_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, faili_kishiko, (mashine_Neno)&첫째값, (mashine_Neno)&urefu_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.namba_ya_kituo << 8 | 첫째값.namba_ya_kituo >> 8) & 65535);
}
mashine_Neno 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mashine_Neno 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mashine_Neno 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mashine_Neno 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
mashine_Neno 도구사각형(mashine_Neno jira_x, mashine_Neno Kitufe_cha_Y_kiratibu, mashine_Neno 너비값, mashine_Neno 높이값, mashine_Neno 색상) {
    return (uint32_t)사용자호출(13, jira_x, Kitufe_cha_Y_kiratibu, 색상, 너비값, 높이값, 0);
}

mashine_Neno zana_Stream(mashine_Neno Kitendo,mashine_Neno faili_kishiko,mashine_Neno thamani){
    if(Kitendo==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(thamani);
    if(Kitendo==1){첫째값.anwani=0;intptr_t 반환값=호출(33,faili_kishiko,(mashine_Neno)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,faili_kishiko,4,0));}
    if(Kitendo==2)return (uint32_t)호출(37,faili_kishiko,(mashine_Neno)&첫째값,sizeof(첫째값));
    if(Kitendo==3)return (uint32_t)호출(39,faili_kishiko,0,0);
    if(Kitendo==4)return 도구전문접속번호(faili_kishiko);
    if(Kitendo==5)return (uint32_t)호출(40,faili_kishiko,0,0);
    return (uint32_t)-22;
}
mashine_Neno zana_GUI(mashine_Neno Kitendo,mashine_Neno kitambulishi_thamani,mashine_Neno 첫째값,mashine_Neno 둘째값,mashine_Neno msimbo_wa_kibambo,mashine_Neno fikio_data){return (uint32_t)사용자호출(20,Kitendo,kitambulishi_thamani,첫째값,둘째값,msimbo_wa_kibambo,fikio_data);}
mashine_Neno zana_GUI_SMS(mashine_Neno kitambulishi_thamani,mashine_Neno ARRAY_thamani,mashine_Neno 개수){
    const mashine_Neno *원본주소=(const mashine_Neno *)ARRAY_thamani;uint32_t data[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(mashine_Neno 순번=0;순번<개수;순번++){unsigned kibambo_usimbaji=원본주소[순번+1];if(kibambo_usimbaji>=0xd800&&kibambo_usimbaji<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;kibambo_usimbaji=0x10000+((kibambo_usimbaji-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;data[항목수++]=kibambo_usimbaji;}
    return (uint32_t)사용자호출(21,kitambulishi_thamani,(mashine_Neno)data,항목수,0,0,0);
}
