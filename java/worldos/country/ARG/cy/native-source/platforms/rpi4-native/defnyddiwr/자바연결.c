#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Ffeil/Allbwn/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bwndel.h"
typedef uintptr_t peiriant_Word;
static int ardal_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static peiriant_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned eitem_COUNT, peiriant_Word 첫째값, peiriant_Word SECOND_VALUE, peiriant_Word cod_nod) {
    return 사용자호출(eitem_COUNT, 첫째값, SECOND_VALUE, cod_nod, 0, 0, 0);
}
static void 바이트들(const char *data_safle, size_t eitem_COUNT) { 호출(1, 1, (peiriant_Word)data_safle, eitem_COUNT); }
static void nod(unsigned cod_nod) {
    unsigned char data[4]; unsigned eitem_COUNT = 0;
    if (cod_nod < 128) data[eitem_COUNT++] = cod_nod;
    else if (cod_nod < 2048) { data[eitem_COUNT++] = 0xc0 | (cod_nod >> 6); data[eitem_COUNT++] = 0x80 | (cod_nod & 63); }
    else if (cod_nod < 65536) { data[eitem_COUNT++] = 0xe0 | (cod_nod >> 12); data[eitem_COUNT++] = 0x80 | ((cod_nod >> 6) & 63); data[eitem_COUNT++] = 0x80 | (cod_nod & 63); }
    else { data[eitem_COUNT++] = 0xf0 | (cod_nod >> 18); data[eitem_COUNT++] = 0x80 | ((cod_nod >> 12) & 63); data[eitem_COUNT++] = 0x80 | ((cod_nod >> 6) & 63); data[eitem_COUNT++] = 0x80 | (cod_nod & 63); }
    바이트들((const char *)data, eitem_COUNT);
}
peiriant_Word offeryn_nod(peiriant_Word VALUE) {
    unsigned cod_nod = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (cod_nod >= 0xdc00 && cod_nod <= 0xdfff) { nod(0x10000 + ((높은부분 - 0xd800) << 10) + cod_nod - 0xdc00); return 1; }
        nod(0xfffd);
    }
    if (cod_nod >= 0xd800 && cod_nod <= 0xdbff) 대기중짝글자 = cod_nod;
    else nod(cod_nod > 0x10ffff || (cod_nod >= 0xdc00 && cod_nod <= 0xdfff) ? 0xfffd : cod_nod);
    return 1;
}
peiriant_Word 도구출력(peiriant_Word VALUE) {
    const peiriant_Word *testun_data = (const peiriant_Word *)VALUE;
    for (peiriant_Word 순번 = 0; 순번 < testun_data[0]; 순번++) offeryn_nod(testun_data[순번 + 1]);
    return testun_data[0];
}
static int LLWYBR(peiriant_Word gwrthrych_cyfeiriad, char mesur_data[512]) {
    const peiriant_Word *첫째값 = (const peiriant_Word *)gwrthrych_cyfeiriad;
    unsigned 사용량 = 0;
    for (peiriant_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned cod_nod = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] dull_MODE 경로와 호환한다.
        if (cod_nod >= 0xd800 && cod_nod <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; cod_nod = 0x10000 + ((cod_nod - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (cod_nod >= 0xd800 && cod_nod <= 0xdfff) return -22;
        unsigned eitem_COUNT = cod_nod < 128 ? 1 : cod_nod < 2048 ? 2 : cod_nod < 65536 ? 3 : 4;
        if (사용량 + eitem_COUNT > 511) return -36;
        if (eitem_COUNT == 1) mesur_data[사용량++] = cod_nod;
        else {
            mesur_data[사용량++] = (eitem_COUNT == 2 ? 0xc0 : eitem_COUNT == 3 ? 0xe0 : 0xf0) | (cod_nod >> (6 * (eitem_COUNT - 1)));
            for (unsigned 안쪽순번 = eitem_COUNT - 1; 안쪽순번; 안쪽순번--) mesur_data[사용량++] = 0x80 | ((cod_nod >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    mesur_data[사용량] = 0; return 사용량 ? 0 : -22;
}
peiriant_Word offeryn_agor(peiriant_Word Enw, peiriant_Word 설정비트) {
    char data_safle[512]; int Gwall = LLWYBR(Enw, data_safle);
    return (uint32_t)(Gwall ? Gwall : 호출(3, (peiriant_Word)data_safle, 설정비트, 0));
}
peiriant_Word offeryn_cau(peiriant_Word ffeil_dolen) { return (uint32_t)호출(4, ffeil_dolen, 0, 0); }
peiriant_Word 도구바이트읽기(peiriant_Word ffeil_dolen) {
    unsigned char SECOND_VALUE; intptr_t eitem_COUNT = 호출(2, ffeil_dolen, (peiriant_Word)&SECOND_VALUE, 1);
    return (uint32_t)(eitem_COUNT == 1 ? SECOND_VALUE : eitem_COUNT == 0 ? 256 : eitem_COUNT);
}
peiriant_Word offeryn_ysgrifennu_beit(peiriant_Word ffeil_dolen, peiriant_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, ffeil_dolen, (peiriant_Word)&SECOND_VALUE, 1);
}
peiriant_Word 도구읽기(peiriant_Word Enw, peiriant_Word cyrchfan_data_ADDRESS) {
    if (꾸러미사용중) {
        char data_safle[512]; int Gwall = LLWYBR(Enw, data_safle); if (Gwall) return (uint32_t)Gwall;
        unsigned eitem_COUNT = 0; while (data_safle[eitem_COUNT]) eitem_COUNT++;
        if (eitem_COUNT >= 6) for (unsigned 순번 = 0; 순번 < eitem_COUNT - 6; 순번++) if (data_safle[순번] == '.') data_safle[순번] = '/';
        unsigned char 바이트들[16384]; peiriant_Word *cyrchfan_VALUE_safle = (peiriant_Word *)cyrchfan_data_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(data_safle, 바이트들, cyrchfan_VALUE_safle[0] < sizeof(바이트들) ? cyrchfan_VALUE_safle[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) cyrchfan_VALUE_safle[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int ffeil_dolen = 꾸러미사용중 ? -2 : (int32_t)offeryn_agor(Enw, 0);
    if (ffeil_dolen < 0) {
        char data_safle[512]; int Gwall = LLWYBR(Enw, data_safle); if (Gwall) return (uint32_t)Gwall;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Nesaf_OFFSET = 자바클래스들[순번].Enw; unsigned 안쪽순번 = 0;
            while (data_safle[안쪽순번] && data_safle[안쪽순번] == Nesaf_OFFSET[안쪽순번]) 안쪽순번++;
            if (data_safle[안쪽순번] || Nesaf_OFFSET[안쪽순번]) continue;
            peiriant_Word *cyrchfan_VALUE_safle = (peiriant_Word *)cyrchfan_data_ADDRESS;
            if (cyrchfan_VALUE_safle[0] < 자바클래스들[순번].Maint) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Maint; 안쪽순번++) cyrchfan_VALUE_safle[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Maint;
        }
        return (uint32_t)ffeil_dolen;
    }
    peiriant_Word *첫째값 = (peiriant_Word *)cyrchfan_data_ADDRESS;
    intptr_t Maint = 호출(9, ffeil_dolen, 0, 0), 완료량 = 0;
    if (Maint < 0 || (peiriant_Word)Maint > 첫째값[0]) { offeryn_cau(ffeil_dolen); return (uint32_t)(Maint < 0 ? Maint : -27); }
    unsigned char data_rhwystro[256];
    while (완료량 < Maint) {
        intptr_t eitem_COUNT = 호출(2, ffeil_dolen, (peiriant_Word)data_rhwystro, Maint - 완료량 < 256 ? Maint - 완료량 : 256);
        if (eitem_COUNT <= 0) { offeryn_cau(ffeil_dolen); return (uint32_t)(eitem_COUNT ? eitem_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < eitem_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = data_rhwystro[순번];
        완료량 += eitem_COUNT;
    }
    offeryn_cau(ffeil_dolen); return 완료량;
}
peiriant_Word offeryn_ysgrifennu(peiriant_Word Enw, peiriant_Word 원본자료, peiriant_Word cofnod_COUNT) {
    const peiriant_Word *첫째값 = (const peiriant_Word *)원본자료;
    if (cofnod_COUNT > 첫째값[0] || cofnod_COUNT > 16384) return (uint32_t)-27;
    int ffeil_dolen = (int32_t)offeryn_agor(Enw, 577); if (ffeil_dolen < 0) return (uint32_t)ffeil_dolen;
    unsigned char data_rhwystro[256]; peiriant_Word 완료량 = 0;
    while (완료량 < cofnod_COUNT) {
        peiriant_Word eitem_COUNT = cofnod_COUNT - 완료량 < 256 ? cofnod_COUNT - 완료량 : 256;
        for (peiriant_Word 순번 = 0; 순번 < eitem_COUNT; 순번++) data_rhwystro[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t mesur = 호출(1, ffeil_dolen, (peiriant_Word)data_rhwystro, eitem_COUNT);
        if (mesur <= 0) { offeryn_cau(ffeil_dolen); return (uint32_t)(mesur ? mesur : -5); }
        완료량 += mesur;
    }
    offeryn_cau(ffeil_dolen); return cofnod_COUNT;
}
peiriant_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
peiriant_Word offeryn_arg(peiriant_Word LOOKUP_INDEX) {
    static const peiriant_Word gwag_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (peiriant_Word)gwag_VALUE;
    unsigned char 입력결과[256]; intptr_t eitem_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *data_safle = 꾸러미진입클래스(); eitem_COUNT = 0; while (data_safle[eitem_COUNT] && eitem_COUNT < 255) { 입력결과[eitem_COUNT] = data_safle[eitem_COUNT]; eitem_COUNT++; } }
    else eitem_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (peiriant_Word)입력결과, sizeof(입력결과));
    if (eitem_COUNT < 0) return (peiriant_Word)gwag_VALUE;
    peiriant_Word *mesur_data = 전달인수[LOOKUP_INDEX]; unsigned cofnod_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < eitem_COUNT;) {
        unsigned cod_nod = 입력결과[순번++], 더있음 = cod_nod < 128 ? 0 : cod_nod >= 0xc2 && cod_nod < 0xe0 ? 1 : cod_nod < 0xf0 && cod_nod >= 0xe0 ? 2 : cod_nod >= 0xf0 && cod_nod <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > eitem_COUNT) { mesur_data[++cofnod_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) cod_nod &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { cod_nod = (cod_nod << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || cod_nod < 최소값 || cod_nod > 0x10ffff || (cod_nod >= 0xd800 && cod_nod <= 0xdfff)) cod_nod = 0xfffd;
        if (cod_nod >= 65536) { cod_nod -= 65536; mesur_data[++cofnod_COUNT] = 0xd800 | (cod_nod >> 10); mesur_data[++cofnod_COUNT] = 0xdc00 | (cod_nod & 1023); }
        else mesur_data[++cofnod_COUNT] = cod_nod;
    }
    mesur_data[0] = cofnod_COUNT; return (peiriant_Word)mesur_data;
}
peiriant_Word 도구분류(void) { return ardal_VALUE; }
void 커널중단(const char *알림문) {
    const char *data_safle = 알림문; while (*data_safle) data_safle++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_safle - 알림문); nod(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_defnyddiwr_Rhaglen(int dull_MODE) {
    ardal_VALUE = dull_MODE;
    unsigned char 첫항목[256]; intptr_t eitem_COUNT = 호출(15, 0, (peiriant_Word)첫항목, sizeof(첫항목));
    if (dull_MODE == 2 || (dull_MODE == 1 && eitem_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = dull_MODE == 2 ? 0 : 1;
        char ffeil_cofnod_enw[256]; intptr_t hyd_data = 호출(15, 꾸러미인수이동, (peiriant_Word)ffeil_cofnod_enw, sizeof(ffeil_cofnod_enw));
        if (hyd_data <= 0 || 꾸러미열기(ffeil_cofnod_enw) < 0) {
            static const char Gwall[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Gwall, sizeof(Gwall) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int mesur = 자바진입();
    if (대기중짝글자) nod(0xfffd);
    return mesur;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Teulu, rhif_porth; uint32_t ADDRESS; unsigned char 영값[8]; };
static struct 자바주소 UDP_ADDRESS(unsigned rhif_porth) {
    struct 자바주소 첫째값 = {2, (uint16_t)((rhif_porth << 8) | (rhif_porth >> 8)), 0x0100007f, {0}}; return 첫째값;
}
peiriant_Word offeryn_UDP_agor(peiriant_Word rhif_porth) {
    intptr_t ffeil_dolen = 호출(32, 2, 2, 17); if (ffeil_dolen < 0) return (uint32_t)ffeil_dolen;
    struct 자바주소 첫째값 = UDP_ADDRESS(rhif_porth);
    첫째값.ADDRESS = 0;
    intptr_t cyflwr_VALUE = 호출(33, ffeil_dolen, (peiriant_Word)&첫째값, sizeof(첫째값));
    if (cyflwr_VALUE < 0) { offeryn_cau(ffeil_dolen); return (uint32_t)cyflwr_VALUE; }
    return ffeil_dolen;
}
peiriant_Word offeryn_UDP_anfon(peiriant_Word ffeil_dolen, peiriant_Word rhif_porth, peiriant_Word ARAE_VALUE, peiriant_Word hyd_VALUE) {
    const peiriant_Word *원본주소 = (const peiriant_Word *)ARAE_VALUE; unsigned char data[512];
    if (hyd_VALUE > 512 || hyd_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (peiriant_Word 순번 = 0; 순번 < hyd_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(rhif_porth);
    return (uint32_t)사용자호출(34, ffeil_dolen, (peiriant_Word)data, hyd_VALUE, 0, (peiriant_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t eitem_COUNT) { return (eitem_COUNT>>24)|((eitem_COUNT>>8)&0xff00)|((eitem_COUNT<<8)&0xff0000)|(eitem_COUNT<<24); }
peiriant_Word offeryn_UDP_anfon_ADDRESS(peiriant_Word ffeil_dolen, peiriant_Word ADDRESS, peiriant_Word rhif_porth, peiriant_Word ARAE_VALUE, peiriant_Word hyd_VALUE) {
    const peiriant_Word *원본주소 = (const peiriant_Word *)ARAE_VALUE; unsigned char data[512];
    if (hyd_VALUE > 512 || hyd_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (peiriant_Word 순번 = 0; 순번 < hyd_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(rhif_porth); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, ffeil_dolen, (peiriant_Word)data, hyd_VALUE, 0, (peiriant_Word)&첫째값, sizeof(첫째값));
}
peiriant_Word offeryn_Cysylltu(peiriant_Word ffeil_dolen, peiriant_Word ADDRESS, peiriant_Word rhif_porth) {
    struct 자바주소 첫째값 = UDP_ADDRESS(rhif_porth); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t Gweithredu_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t mesur = 호출(37, ffeil_dolen, (peiriant_Word)&첫째값, sizeof(첫째값));
        if (mesur != -115) return (uint32_t)mesur;
        if ((uint32_t)(호출(7, 0, 0, 0) - Gweithredu_2) >= 1000) return (uint32_t)-110;
    }
}
peiriant_Word 도구전문받기(peiriant_Word ffeil_dolen, peiriant_Word ARAE_VALUE, peiriant_Word 수용량) {
    peiriant_Word *cyrchfan_ADDRESS = (peiriant_Word *)ARAE_VALUE; unsigned char data[512];
    if (수용량 > 512 || cyrchfan_ADDRESS[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned hyd_data = sizeof(첫째값);
    intptr_t eitem_COUNT = 사용자호출(35, ffeil_dolen, (peiriant_Word)data, 수용량, 0, (peiriant_Word)&첫째값, (peiriant_Word)&hyd_data);
    if (eitem_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < eitem_COUNT; 순번++) cyrchfan_ADDRESS[순번 + 1] = data[순번]; cyrchfan_ADDRESS[513] = (첫째값.rhif_porth << 8 | 첫째값.rhif_porth >> 8) & 65535; cyrchfan_ADDRESS[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)eitem_COUNT;
}
peiriant_Word offeryn_UDP_porth(peiriant_Word ffeil_dolen) {
    struct 자바주소 첫째값; unsigned hyd_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, ffeil_dolen, (peiriant_Word)&첫째값, (peiriant_Word)&hyd_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.rhif_porth << 8 | 첫째값.rhif_porth >> 8) & 65535);
}
peiriant_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
peiriant_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
peiriant_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
peiriant_Word offeryn_graffeg_aros(void) { return (uint32_t)화면키기다리기(); }
peiriant_Word 도구사각형(peiriant_Word cyfesuryn_x, peiriant_Word Y_cyfesuryn, peiriant_Word 너비값, peiriant_Word 높이값, peiriant_Word 색상) {
    return (uint32_t)사용자호출(13, cyfesuryn_x, Y_cyfesuryn, 색상, 너비값, 높이값, 0);
}

peiriant_Word offeryn_ffrwd(peiriant_Word Gweithrediad,peiriant_Word ffeil_dolen,peiriant_Word VALUE){
    if(Gweithrediad==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADDRESS(VALUE);
    if(Gweithrediad==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,ffeil_dolen,(peiriant_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,ffeil_dolen,4,0));}
    if(Gweithrediad==2)return (uint32_t)호출(37,ffeil_dolen,(peiriant_Word)&첫째값,sizeof(첫째값));
    if(Gweithrediad==3)return (uint32_t)호출(39,ffeil_dolen,0,0);
    if(Gweithrediad==4)return offeryn_UDP_porth(ffeil_dolen);
    if(Gweithrediad==5)return (uint32_t)호출(40,ffeil_dolen,0,0);
    return (uint32_t)-22;
}
peiriant_Word offeryn_GUI(peiriant_Word Gweithrediad,peiriant_Word dynodwr_VALUE,peiriant_Word 첫째값,peiriant_Word SECOND_VALUE,peiriant_Word cod_nod,peiriant_Word cyrchfan_data){return (uint32_t)사용자호출(20,Gweithrediad,dynodwr_VALUE,첫째값,SECOND_VALUE,cod_nod,cyrchfan_data);}
peiriant_Word offeryn_GUI_SMS(peiriant_Word dynodwr_VALUE,peiriant_Word ARAE_VALUE,peiriant_Word eitem_COUNT){
    const peiriant_Word *원본주소=(const peiriant_Word *)ARAE_VALUE;uint32_t data[127];unsigned cofnod_COUNT=0;
    if(eitem_COUNT>원본주소[0])return (uint32_t)-22;
    for(peiriant_Word 순번=0;순번<eitem_COUNT;순번++){unsigned nod_amgodio=원본주소[순번+1];if(nod_amgodio>=0xd800&&nod_amgodio<=0xdbff&&순번+1<eitem_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;nod_amgodio=0x10000+((nod_amgodio-0xd800)<<10)+낮은값-0xdc00;}if(cofnod_COUNT==127)return (uint32_t)-22;data[cofnod_COUNT++]=nod_amgodio;}
    return (uint32_t)사용자호출(21,dynodwr_VALUE,(peiriant_Word)data,cofnod_COUNT,0,0,0);
}
