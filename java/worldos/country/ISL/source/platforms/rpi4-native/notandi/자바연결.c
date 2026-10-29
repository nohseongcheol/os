#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Skrá/úttak/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "búnt.h"
typedef uintptr_t vél_Word;
static int tegund_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static vél_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned vara_COUNT, vél_Word 첫째값, vél_Word SECOND_VALUE, vél_Word stafkóði) {
    return 사용자호출(vara_COUNT, 첫째값, SECOND_VALUE, stafkóði, 0, 0, 0);
}
static void 바이트들(const char *gögn_staða, size_t vara_COUNT) { 호출(1, 1, (vél_Word)gögn_staða, vara_COUNT); }
static void stafur(unsigned stafkóði) {
    unsigned char gögn[4]; unsigned vara_COUNT = 0;
    if (stafkóði < 128) gögn[vara_COUNT++] = stafkóði;
    else if (stafkóði < 2048) { gögn[vara_COUNT++] = 0xc0 | (stafkóði >> 6); gögn[vara_COUNT++] = 0x80 | (stafkóði & 63); }
    else if (stafkóði < 65536) { gögn[vara_COUNT++] = 0xe0 | (stafkóði >> 12); gögn[vara_COUNT++] = 0x80 | ((stafkóði >> 6) & 63); gögn[vara_COUNT++] = 0x80 | (stafkóði & 63); }
    else { gögn[vara_COUNT++] = 0xf0 | (stafkóði >> 18); gögn[vara_COUNT++] = 0x80 | ((stafkóði >> 12) & 63); gögn[vara_COUNT++] = 0x80 | ((stafkóði >> 6) & 63); gögn[vara_COUNT++] = 0x80 | (stafkóði & 63); }
    바이트들((const char *)gögn, vara_COUNT);
}
vél_Word verkfæri_stafur(vél_Word VALUE) {
    unsigned stafkóði = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (stafkóði >= 0xdc00 && stafkóði <= 0xdfff) { stafur(0x10000 + ((높은부분 - 0xd800) << 10) + stafkóði - 0xdc00); return 1; }
        stafur(0xfffd);
    }
    if (stafkóði >= 0xd800 && stafkóði <= 0xdbff) 대기중짝글자 = stafkóði;
    else stafur(stafkóði > 0x10ffff || (stafkóði >= 0xdc00 && stafkóði <= 0xdfff) ? 0xfffd : stafkóði);
    return 1;
}
vél_Word 도구출력(vél_Word VALUE) {
    const vél_Word *strengur_gögn = (const vél_Word *)VALUE;
    for (vél_Word 순번 = 0; 순번 < strengur_gögn[0]; 순번++) verkfæri_stafur(strengur_gögn[순번 + 1]);
    return strengur_gögn[0];
}
static int SLÓÐ(vél_Word hlutur_tilvísun, char mæld_stærð_gögn[512]) {
    const vél_Word *첫째값 = (const vél_Word *)hlutur_tilvísun;
    unsigned 사용량 = 0;
    for (vél_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned stafkóði = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] aðferð_MODE 경로와 호환한다.
        if (stafkóði >= 0xd800 && stafkóði <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; stafkóði = 0x10000 + ((stafkóði - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (stafkóði >= 0xd800 && stafkóði <= 0xdfff) return -22;
        unsigned vara_COUNT = stafkóði < 128 ? 1 : stafkóði < 2048 ? 2 : stafkóði < 65536 ? 3 : 4;
        if (사용량 + vara_COUNT > 511) return -36;
        if (vara_COUNT == 1) mæld_stærð_gögn[사용량++] = stafkóði;
        else {
            mæld_stærð_gögn[사용량++] = (vara_COUNT == 2 ? 0xc0 : vara_COUNT == 3 ? 0xe0 : 0xf0) | (stafkóði >> (6 * (vara_COUNT - 1)));
            for (unsigned 안쪽순번 = vara_COUNT - 1; 안쪽순번; 안쪽순번--) mæld_stærð_gögn[사용량++] = 0x80 | ((stafkóði >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    mæld_stærð_gögn[사용량] = 0; return 사용량 ? 0 : -22;
}
vél_Word verkfæri_opið(vél_Word Heiti, vél_Word afbrigði_Background_Intelligent_Transfer_Service) {
    char gögn_staða[512]; int Villa = SLÓÐ(Heiti, gögn_staða);
    return (uint32_t)(Villa ? Villa : 호출(3, (vél_Word)gögn_staða, afbrigði_Background_Intelligent_Transfer_Service, 0));
}
vél_Word verkfæri_loka(vél_Word skrá_hald) { return (uint32_t)호출(4, skrá_hald, 0, 0); }
vél_Word 도구바이트읽기(vél_Word skrá_hald) {
    unsigned char SECOND_VALUE; intptr_t vara_COUNT = 호출(2, skrá_hald, (vél_Word)&SECOND_VALUE, 1);
    return (uint32_t)(vara_COUNT == 1 ? SECOND_VALUE : vara_COUNT == 0 ? 256 : vara_COUNT);
}
vél_Word verkfæri_skrifa_bæti(vél_Word skrá_hald, vél_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, skrá_hald, (vél_Word)&SECOND_VALUE, 1);
}
vél_Word 도구읽기(vél_Word Heiti, vél_Word endastaður_gögn_slóð) {
    if (꾸러미사용중) {
        char gögn_staða[512]; int Villa = SLÓÐ(Heiti, gögn_staða); if (Villa) return (uint32_t)Villa;
        unsigned vara_COUNT = 0; while (gögn_staða[vara_COUNT]) vara_COUNT++;
        if (vara_COUNT >= 6) for (unsigned 순번 = 0; 순번 < vara_COUNT - 6; 순번++) if (gögn_staða[순번] == '.') gögn_staða[순번] = '/';
        unsigned char 바이트들[16384]; vél_Word *endastaður_VALUE_staða = (vél_Word *)endastaður_gögn_slóð;
        int RECEIVED_COUNT = 꾸러미읽기(gögn_staða, 바이트들, endastaður_VALUE_staða[0] < sizeof(바이트들) ? endastaður_VALUE_staða[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) endastaður_VALUE_staða[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int skrá_hald = 꾸러미사용중 ? -2 : (int32_t)verkfæri_opið(Heiti, 0);
    if (skrá_hald < 0) {
        char gögn_staða[512]; int Villa = SLÓÐ(Heiti, gögn_staða); if (Villa) return (uint32_t)Villa;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Áfram_OFFSET = 자바클래스들[순번].Heiti; unsigned 안쪽순번 = 0;
            while (gögn_staða[안쪽순번] && gögn_staða[안쪽순번] == Áfram_OFFSET[안쪽순번]) 안쪽순번++;
            if (gögn_staða[안쪽순번] || Áfram_OFFSET[안쪽순번]) continue;
            vél_Word *endastaður_VALUE_staða = (vél_Word *)endastaður_gögn_slóð;
            if (endastaður_VALUE_staða[0] < 자바클래스들[순번].Stærð) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Stærð; 안쪽순번++) endastaður_VALUE_staða[안쪽순번 + 1] = 자바클래스들[순번].gögn[안쪽순번];
            return 자바클래스들[순번].Stærð;
        }
        return (uint32_t)skrá_hald;
    }
    vél_Word *첫째값 = (vél_Word *)endastaður_gögn_slóð;
    intptr_t Stærð = 호출(9, skrá_hald, 0, 0), lokið_upphæð = 0;
    if (Stærð < 0 || (vél_Word)Stærð > 첫째값[0]) { verkfæri_loka(skrá_hald); return (uint32_t)(Stærð < 0 ? Stærð : -27); }
    unsigned char gögn_útiloka[256];
    while (lokið_upphæð < Stærð) {
        intptr_t vara_COUNT = 호출(2, skrá_hald, (vél_Word)gögn_útiloka, Stærð - lokið_upphæð < 256 ? Stærð - lokið_upphæð : 256);
        if (vara_COUNT <= 0) { verkfæri_loka(skrá_hald); return (uint32_t)(vara_COUNT ? vara_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < vara_COUNT; 순번++) 첫째값[1 + lokið_upphæð + 순번] = gögn_útiloka[순번];
        lokið_upphæð += vara_COUNT;
    }
    verkfæri_loka(skrá_hald); return lokið_upphæð;
}
vél_Word verkfæri_skrifa(vél_Word Heiti, vél_Word 원본자료, vél_Word færsla_COUNT) {
    const vél_Word *첫째값 = (const vél_Word *)원본자료;
    if (færsla_COUNT > 첫째값[0] || færsla_COUNT > 16384) return (uint32_t)-27;
    int skrá_hald = (int32_t)verkfæri_opið(Heiti, 577); if (skrá_hald < 0) return (uint32_t)skrá_hald;
    unsigned char gögn_útiloka[256]; vél_Word lokið_upphæð = 0;
    while (lokið_upphæð < færsla_COUNT) {
        vél_Word vara_COUNT = færsla_COUNT - lokið_upphæð < 256 ? færsla_COUNT - lokið_upphæð : 256;
        for (vél_Word 순번 = 0; 순번 < vara_COUNT; 순번++) gögn_útiloka[순번] = 첫째값[1 + lokið_upphæð + 순번];
        intptr_t NIÐURSTAÐA = 호출(1, skrá_hald, (vél_Word)gögn_útiloka, vara_COUNT);
        if (NIÐURSTAÐA <= 0) { verkfæri_loka(skrá_hald); return (uint32_t)(NIÐURSTAÐA ? NIÐURSTAÐA : -5); }
        lokið_upphæð += NIÐURSTAÐA;
    }
    verkfæri_loka(skrá_hald); return færsla_COUNT;
}
vél_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
vél_Word verkfæri_frumbreyta(vél_Word LOOKUP_INDEX) {
    static const vél_Word autt_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (vél_Word)autt_VALUE;
    unsigned char 입력결과[256]; intptr_t vara_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *gögn_staða = 꾸러미진입클래스(); vara_COUNT = 0; while (gögn_staða[vara_COUNT] && vara_COUNT < 255) { 입력결과[vara_COUNT] = gögn_staða[vara_COUNT]; vara_COUNT++; } }
    else vara_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (vél_Word)입력결과, sizeof(입력결과));
    if (vara_COUNT < 0) return (vél_Word)autt_VALUE;
    vél_Word *mæld_stærð_gögn = 전달인수[LOOKUP_INDEX]; unsigned færsla_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < vara_COUNT;) {
        unsigned stafkóði = 입력결과[순번++], 더있음 = stafkóði < 128 ? 0 : stafkóði >= 0xc2 && stafkóði < 0xe0 ? 1 : stafkóði < 0xf0 && stafkóði >= 0xe0 ? 2 : stafkóði >= 0xf0 && stafkóði <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > vara_COUNT) { mæld_stærð_gögn[++færsla_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) stafkóði &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { stafkóði = (stafkóði << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || stafkóði < 최소값 || stafkóði > 0x10ffff || (stafkóði >= 0xd800 && stafkóði <= 0xdfff)) stafkóði = 0xfffd;
        if (stafkóði >= 65536) { stafkóði -= 65536; mæld_stærð_gögn[++færsla_COUNT] = 0xd800 | (stafkóði >> 10); mæld_stærð_gögn[++færsla_COUNT] = 0xdc00 | (stafkóði & 1023); }
        else mæld_stærð_gögn[++færsla_COUNT] = stafkóði;
    }
    mæld_stærð_gögn[0] = færsla_COUNT; return (vél_Word)mæld_stærð_gögn;
}
vél_Word 도구분류(void) { return tegund_VALUE; }
void 커널중단(const char *알림문) {
    const char *gögn_staða = 알림문; while (*gögn_staða) gögn_staða++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, gögn_staða - 알림문); stafur(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Opna_notandi_forrit(int aðferð_MODE) {
    tegund_VALUE = aðferð_MODE;
    unsigned char 첫항목[256]; intptr_t vara_COUNT = 호출(15, 0, (vél_Word)첫항목, sizeof(첫항목));
    if (aðferð_MODE == 2 || (aðferð_MODE == 1 && vara_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = aðferð_MODE == 2 ? 0 : 1;
        char skrá_færsla_heiti[256]; intptr_t lengd_gögn = 호출(15, 꾸러미인수이동, (vél_Word)skrá_færsla_heiti, sizeof(skrá_færsla_heiti));
        if (lengd_gögn <= 0 || 꾸러미열기(skrá_færsla_heiti) < 0) {
            static const char Villa[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Villa, sizeof(Villa) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int NIÐURSTAÐA = 자바진입();
    if (대기중짝글자) stafur(0xfffd);
    return NIÐURSTAÐA;
}

// UDP는 eigin 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Fjölskylda, tengisnúmer; uint32_t slóð; unsigned char 영값[8]; };
static struct 자바주소 UDP_slóð(unsigned tengisnúmer) {
    struct 자바주소 첫째값 = {2, (uint16_t)((tengisnúmer << 8) | (tengisnúmer >> 8)), 0x0100007f, {0}}; return 첫째값;
}
vél_Word verkfæri_UDP_opið(vél_Word tengisnúmer) {
    intptr_t skrá_hald = 호출(32, 2, 2, 17); if (skrá_hald < 0) return (uint32_t)skrá_hald;
    struct 자바주소 첫째값 = UDP_slóð(tengisnúmer);
    첫째값.slóð = 0;
    intptr_t staða_VALUE_e10195a1 = 호출(33, skrá_hald, (vél_Word)&첫째값, sizeof(첫째값));
    if (staða_VALUE_e10195a1 < 0) { verkfæri_loka(skrá_hald); return (uint32_t)staða_VALUE_e10195a1; }
    return skrá_hald;
}
vél_Word verkfæri_UDP_senda(vél_Word skrá_hald, vél_Word tengisnúmer, vél_Word ARRAY_VALUE, vél_Word lengd_VALUE) {
    const vél_Word *원본주소 = (const vél_Word *)ARRAY_VALUE; unsigned char gögn[512];
    if (lengd_VALUE > 512 || lengd_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (vél_Word 순번 = 0; 순번 < lengd_VALUE; 순번++) gögn[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_slóð(tengisnúmer);
    return (uint32_t)사용자호출(34, skrá_hald, (vél_Word)gögn, lengd_VALUE, 0, (vél_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t vara_COUNT) { return (vara_COUNT>>24)|((vara_COUNT>>8)&0xff00)|((vara_COUNT<<8)&0xff0000)|(vara_COUNT<<24); }
vél_Word verkfæri_UDP_senda_slóð(vél_Word skrá_hald, vél_Word slóð, vél_Word tengisnúmer, vél_Word ARRAY_VALUE, vél_Word lengd_VALUE) {
    const vél_Word *원본주소 = (const vél_Word *)ARRAY_VALUE; unsigned char gögn[512];
    if (lengd_VALUE > 512 || lengd_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (vél_Word 순번 = 0; 순번 < lengd_VALUE; 순번++) gögn[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_slóð(tengisnúmer); 첫째값.slóð = 바이트순서뒤집기(slóð);
    return (uint32_t)사용자호출(34, skrá_hald, (vél_Word)gögn, lengd_VALUE, 0, (vél_Word)&첫째값, sizeof(첫째값));
}
vél_Word verkfæri_TENGJA(vél_Word skrá_hald, vél_Word slóð, vél_Word tengisnúmer) {
    struct 자바주소 첫째값 = UDP_slóð(tengisnúmer); 첫째값.slóð = 바이트순서뒤집기(slóð);
    uint32_t Keyra_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t NIÐURSTAÐA = 호출(37, skrá_hald, (vél_Word)&첫째값, sizeof(첫째값));
        if (NIÐURSTAÐA != -115) return (uint32_t)NIÐURSTAÐA;
        if ((uint32_t)(호출(7, 0, 0, 0) - Keyra_2) >= 1000) return (uint32_t)-110;
    }
}
vél_Word 도구전문받기(vél_Word skrá_hald, vél_Word ARRAY_VALUE, vél_Word biðminni_afkastageta) {
    vél_Word *endastaður_slóð_08bbd577 = (vél_Word *)ARRAY_VALUE; unsigned char gögn[512];
    if (biðminni_afkastageta > 512 || endastaður_slóð_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned lengd_gögn = sizeof(첫째값);
    intptr_t vara_COUNT = 사용자호출(35, skrá_hald, (vél_Word)gögn, biðminni_afkastageta, 0, (vél_Word)&첫째값, (vél_Word)&lengd_gögn);
    if (vara_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < vara_COUNT; 순번++) endastaður_slóð_08bbd577[순번 + 1] = gögn[순번]; endastaður_slóð_08bbd577[513] = (첫째값.tengisnúmer << 8 | 첫째값.tengisnúmer >> 8) & 65535; endastaður_slóð_08bbd577[514] = 바이트순서뒤집기(첫째값.slóð); }
    return (uint32_t)vara_COUNT;
}
vél_Word verkfæri_UDP_gátt(vél_Word skrá_hald) {
    struct 자바주소 첫째값; unsigned lengd_gögn = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, skrá_hald, (vél_Word)&첫째값, (vél_Word)&lengd_gögn);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.tengisnúmer << 8 | 첫째값.tengisnúmer >> 8) & 65535);
}
vél_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
vél_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
vél_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
vél_Word verkfæri_myndefni_Bíddu(void) { return (uint32_t)화면키기다리기(); }
vél_Word 도구사각형(vél_Word x_hnit, vél_Word Y_hnit, vél_Word 너비값, vél_Word 높이값, vél_Word 색상) {
    return (uint32_t)사용자호출(13, x_hnit, Y_hnit, 색상, 너비값, 높이값, 0);
}

vél_Word verkfæri_Stream(vél_Word Aðgerð,vél_Word skrá_hald,vél_Word VALUE){
    if(Aðgerð==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_slóð(VALUE);
    if(Aðgerð==1){첫째값.slóð=0;intptr_t 반환값=호출(33,skrá_hald,(vél_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,skrá_hald,4,0));}
    if(Aðgerð==2)return (uint32_t)호출(37,skrá_hald,(vél_Word)&첫째값,sizeof(첫째값));
    if(Aðgerð==3)return (uint32_t)호출(39,skrá_hald,0,0);
    if(Aðgerð==4)return verkfæri_UDP_gátt(skrá_hald);
    if(Aðgerð==5)return (uint32_t)호출(40,skrá_hald,0,0);
    return (uint32_t)-22;
}
vél_Word verkfæri_GUI(vél_Word Aðgerð,vél_Word auðkenni_VALUE,vél_Word 첫째값,vél_Word SECOND_VALUE,vél_Word stafkóði,vél_Word endastaður_gögn){return (uint32_t)사용자호출(20,Aðgerð,auðkenni_VALUE,첫째값,SECOND_VALUE,stafkóði,endastaður_gögn);}
vél_Word verkfæri_GUI_SMS(vél_Word auðkenni_VALUE,vél_Word ARRAY_VALUE,vél_Word vara_COUNT){
    const vél_Word *원본주소=(const vél_Word *)ARRAY_VALUE;uint32_t gögn[127];unsigned færsla_COUNT=0;
    if(vara_COUNT>원본주소[0])return (uint32_t)-22;
    for(vél_Word 순번=0;순번<vara_COUNT;순번++){unsigned stafur_kóðun=원본주소[순번+1];if(stafur_kóðun>=0xd800&&stafur_kóðun<=0xdbff&&순번+1<vara_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;stafur_kóðun=0x10000+((stafur_kóðun-0xd800)<<10)+낮은값-0xdc00;}if(færsla_COUNT==127)return (uint32_t)-22;gögn[færsla_COUNT++]=stafur_kóðun;}
    return (uint32_t)사용자호출(21,auðkenni_VALUE,(vél_Word)gögn,færsla_COUNT,0,0,0);
}
