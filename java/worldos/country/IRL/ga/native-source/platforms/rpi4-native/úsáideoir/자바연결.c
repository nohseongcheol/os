#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Comhad/Aschur/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "beart.h"
typedef uintptr_t meaisín_Word;
static int catagóir_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static meaisín_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned mír_COUNT, meaisín_Word 첫째값, meaisín_Word SECOND_VALUE, meaisín_Word pointe_cóid) {
    return 사용자호출(mír_COUNT, 첫째값, SECOND_VALUE, pointe_cóid, 0, 0, 0);
}
static void 바이트들(const char *sonraí_suíomh, size_t mír_COUNT) { 호출(1, 1, (meaisín_Word)sonraí_suíomh, mír_COUNT); }
static void carachtar(unsigned pointe_cóid) {
    unsigned char sonraí[4]; unsigned mír_COUNT = 0;
    if (pointe_cóid < 128) sonraí[mír_COUNT++] = pointe_cóid;
    else if (pointe_cóid < 2048) { sonraí[mír_COUNT++] = 0xc0 | (pointe_cóid >> 6); sonraí[mír_COUNT++] = 0x80 | (pointe_cóid & 63); }
    else if (pointe_cóid < 65536) { sonraí[mír_COUNT++] = 0xe0 | (pointe_cóid >> 12); sonraí[mír_COUNT++] = 0x80 | ((pointe_cóid >> 6) & 63); sonraí[mír_COUNT++] = 0x80 | (pointe_cóid & 63); }
    else { sonraí[mír_COUNT++] = 0xf0 | (pointe_cóid >> 18); sonraí[mír_COUNT++] = 0x80 | ((pointe_cóid >> 12) & 63); sonraí[mír_COUNT++] = 0x80 | ((pointe_cóid >> 6) & 63); sonraí[mír_COUNT++] = 0x80 | (pointe_cóid & 63); }
    바이트들((const char *)sonraí, mír_COUNT);
}
meaisín_Word uirlis_carachtar(meaisín_Word VALUE) {
    unsigned pointe_cóid = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (pointe_cóid >= 0xdc00 && pointe_cóid <= 0xdfff) { carachtar(0x10000 + ((높은부분 - 0xd800) << 10) + pointe_cóid - 0xdc00); return 1; }
        carachtar(0xfffd);
    }
    if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdbff) 대기중짝글자 = pointe_cóid;
    else carachtar(pointe_cóid > 0x10ffff || (pointe_cóid >= 0xdc00 && pointe_cóid <= 0xdfff) ? 0xfffd : pointe_cóid);
    return 1;
}
meaisín_Word 도구출력(meaisín_Word VALUE) {
    const meaisín_Word *teaghrán_sonraí = (const meaisín_Word *)VALUE;
    for (meaisín_Word 순번 = 0; 순번 < teaghrán_sonraí[0]; 순번++) uirlis_carachtar(teaghrán_sonraí[순번 + 1]);
    return teaghrán_sonraí[0];
}
static int CONAIR(meaisín_Word oibiacht_Leabhair_thagartha, char tomhas_sonraí[512]) {
    const meaisín_Word *첫째값 = (const meaisín_Word *)oibiacht_Leabhair_thagartha;
    unsigned 사용량 = 0;
    for (meaisín_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned pointe_cóid = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] modh_mód 경로와 호환한다.
        if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; pointe_cóid = 0x10000 + ((pointe_cóid - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdfff) return -22;
        unsigned mír_COUNT = pointe_cóid < 128 ? 1 : pointe_cóid < 2048 ? 2 : pointe_cóid < 65536 ? 3 : 4;
        if (사용량 + mír_COUNT > 511) return -36;
        if (mír_COUNT == 1) tomhas_sonraí[사용량++] = pointe_cóid;
        else {
            tomhas_sonraí[사용량++] = (mír_COUNT == 2 ? 0xc0 : mír_COUNT == 3 ? 0xe0 : 0xf0) | (pointe_cóid >> (6 * (mír_COUNT - 1)));
            for (unsigned 안쪽순번 = mír_COUNT - 1; 안쪽순번; 안쪽순번--) tomhas_sonraí[사용량++] = 0x80 | ((pointe_cóid >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    tomhas_sonraí[사용량] = 0; return 사용량 ? 0 : -22;
}
meaisín_Word uirlis_oscail(meaisín_Word Ainm, meaisín_Word 설정비트) {
    char sonraí_suíomh[512]; int ERREÁID = CONAIR(Ainm, sonraí_suíomh);
    return (uint32_t)(ERREÁID ? ERREÁID : 호출(3, (meaisín_Word)sonraí_suíomh, 설정비트, 0));
}
meaisín_Word uirlis_dún(meaisín_Word comhad_hanla) { return (uint32_t)호출(4, comhad_hanla, 0, 0); }
meaisín_Word 도구바이트읽기(meaisín_Word comhad_hanla) {
    unsigned char SECOND_VALUE; intptr_t mír_COUNT = 호출(2, comhad_hanla, (meaisín_Word)&SECOND_VALUE, 1);
    return (uint32_t)(mír_COUNT == 1 ? SECOND_VALUE : mír_COUNT == 0 ? 256 : mír_COUNT);
}
meaisín_Word uirlis_scríobh_beart(meaisín_Word comhad_hanla, meaisín_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, comhad_hanla, (meaisín_Word)&SECOND_VALUE, 1);
}
meaisín_Word 도구읽기(meaisín_Word Ainm, meaisín_Word sprioc_sonraí_ADDRESS) {
    if (꾸러미사용중) {
        char sonraí_suíomh[512]; int ERREÁID = CONAIR(Ainm, sonraí_suíomh); if (ERREÁID) return (uint32_t)ERREÁID;
        unsigned mír_COUNT = 0; while (sonraí_suíomh[mír_COUNT]) mír_COUNT++;
        if (mír_COUNT >= 6) for (unsigned 순번 = 0; 순번 < mír_COUNT - 6; 순번++) if (sonraí_suíomh[순번] == '.') sonraí_suíomh[순번] = '/';
        unsigned char 바이트들[16384]; meaisín_Word *sprioc_VALUE_suíomh = (meaisín_Word *)sprioc_sonraí_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(sonraí_suíomh, 바이트들, sprioc_VALUE_suíomh[0] < sizeof(바이트들) ? sprioc_VALUE_suíomh[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) sprioc_VALUE_suíomh[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int comhad_hanla = 꾸러미사용중 ? -2 : (int32_t)uirlis_oscail(Ainm, 0);
    if (comhad_hanla < 0) {
        char sonraí_suíomh[512]; int ERREÁID = CONAIR(Ainm, sonraí_suíomh); if (ERREÁID) return (uint32_t)ERREÁID;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Ar_aghaidh_OFFSET = 자바클래스들[순번].Ainm; unsigned 안쪽순번 = 0;
            while (sonraí_suíomh[안쪽순번] && sonraí_suíomh[안쪽순번] == Ar_aghaidh_OFFSET[안쪽순번]) 안쪽순번++;
            if (sonraí_suíomh[안쪽순번] || Ar_aghaidh_OFFSET[안쪽순번]) continue;
            meaisín_Word *sprioc_VALUE_suíomh = (meaisín_Word *)sprioc_sonraí_ADDRESS;
            if (sprioc_VALUE_suíomh[0] < 자바클래스들[순번].Méid) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Méid; 안쪽순번++) sprioc_VALUE_suíomh[안쪽순번 + 1] = 자바클래스들[순번].sonraí[안쪽순번];
            return 자바클래스들[순번].Méid;
        }
        return (uint32_t)comhad_hanla;
    }
    meaisín_Word *첫째값 = (meaisín_Word *)sprioc_sonraí_ADDRESS;
    intptr_t Méid = 호출(9, comhad_hanla, 0, 0), 완료량 = 0;
    if (Méid < 0 || (meaisín_Word)Méid > 첫째값[0]) { uirlis_dún(comhad_hanla); return (uint32_t)(Méid < 0 ? Méid : -27); }
    unsigned char sonraí_bac[256];
    while (완료량 < Méid) {
        intptr_t mír_COUNT = 호출(2, comhad_hanla, (meaisín_Word)sonraí_bac, Méid - 완료량 < 256 ? Méid - 완료량 : 256);
        if (mír_COUNT <= 0) { uirlis_dún(comhad_hanla); return (uint32_t)(mír_COUNT ? mír_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < mír_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = sonraí_bac[순번];
        완료량 += mír_COUNT;
    }
    uirlis_dún(comhad_hanla); return 완료량;
}
meaisín_Word uirlis_scríobh(meaisín_Word Ainm, meaisín_Word 원본자료, meaisín_Word iontráil_COUNT) {
    const meaisín_Word *첫째값 = (const meaisín_Word *)원본자료;
    if (iontráil_COUNT > 첫째값[0] || iontráil_COUNT > 16384) return (uint32_t)-27;
    int comhad_hanla = (int32_t)uirlis_oscail(Ainm, 577); if (comhad_hanla < 0) return (uint32_t)comhad_hanla;
    unsigned char sonraí_bac[256]; meaisín_Word 완료량 = 0;
    while (완료량 < iontráil_COUNT) {
        meaisín_Word mír_COUNT = iontráil_COUNT - 완료량 < 256 ? iontráil_COUNT - 완료량 : 256;
        for (meaisín_Word 순번 = 0; 순번 < mír_COUNT; 순번++) sonraí_bac[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t tomhas = 호출(1, comhad_hanla, (meaisín_Word)sonraí_bac, mír_COUNT);
        if (tomhas <= 0) { uirlis_dún(comhad_hanla); return (uint32_t)(tomhas ? tomhas : -5); }
        완료량 += tomhas;
    }
    uirlis_dún(comhad_hanla); return iontráil_COUNT;
}
meaisín_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
meaisín_Word uirlis_argóint(meaisín_Word LOOKUP_INDEX) {
    static const meaisín_Word folamh_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (meaisín_Word)folamh_VALUE;
    unsigned char 입력결과[256]; intptr_t mír_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *sonraí_suíomh = 꾸러미진입클래스(); mír_COUNT = 0; while (sonraí_suíomh[mír_COUNT] && mír_COUNT < 255) { 입력결과[mír_COUNT] = sonraí_suíomh[mír_COUNT]; mír_COUNT++; } }
    else mír_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (meaisín_Word)입력결과, sizeof(입력결과));
    if (mír_COUNT < 0) return (meaisín_Word)folamh_VALUE;
    meaisín_Word *tomhas_sonraí = 전달인수[LOOKUP_INDEX]; unsigned iontráil_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < mír_COUNT;) {
        unsigned pointe_cóid = 입력결과[순번++], 더있음 = pointe_cóid < 128 ? 0 : pointe_cóid >= 0xc2 && pointe_cóid < 0xe0 ? 1 : pointe_cóid < 0xf0 && pointe_cóid >= 0xe0 ? 2 : pointe_cóid >= 0xf0 && pointe_cóid <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > mír_COUNT) { tomhas_sonraí[++iontráil_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) pointe_cóid &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { pointe_cóid = (pointe_cóid << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || pointe_cóid < 최소값 || pointe_cóid > 0x10ffff || (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdfff)) pointe_cóid = 0xfffd;
        if (pointe_cóid >= 65536) { pointe_cóid -= 65536; tomhas_sonraí[++iontráil_COUNT] = 0xd800 | (pointe_cóid >> 10); tomhas_sonraí[++iontráil_COUNT] = 0xdc00 | (pointe_cóid & 1023); }
        else tomhas_sonraí[++iontráil_COUNT] = pointe_cóid;
    }
    tomhas_sonraí[0] = iontráil_COUNT; return (meaisín_Word)tomhas_sonraí;
}
meaisín_Word 도구분류(void) { return catagóir_VALUE; }
void 커널중단(const char *알림문) {
    const char *sonraí_suíomh = 알림문; while (*sonraí_suíomh) sonraí_suíomh++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, sonraí_suíomh - 알림문); carachtar(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_úsáideoir_clár(int modh_mód) {
    catagóir_VALUE = modh_mód;
    unsigned char 첫항목[256]; intptr_t mír_COUNT = 호출(15, 0, (meaisín_Word)첫항목, sizeof(첫항목));
    if (modh_mód == 2 || (modh_mód == 1 && mír_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = modh_mód == 2 ? 0 : 1;
        char comhad_iontráil_ainm[256]; intptr_t fad_sonraí = 호출(15, 꾸러미인수이동, (meaisín_Word)comhad_iontráil_ainm, sizeof(comhad_iontráil_ainm));
        if (fad_sonraí <= 0 || 꾸러미열기(comhad_iontráil_ainm) < 0) {
            static const char ERREÁID[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(ERREÁID, sizeof(ERREÁID) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int tomhas = 자바진입();
    if (대기중짝글자) carachtar(0xfffd);
    return tomhas;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Teaghlach, uimhir_phoirt; uint32_t ADDRESS; unsigned char 영값[8]; };
static struct 자바주소 UDP_ADDRESS(unsigned uimhir_phoirt) {
    struct 자바주소 첫째값 = {2, (uint16_t)((uimhir_phoirt << 8) | (uimhir_phoirt >> 8)), 0x0100007f, {0}}; return 첫째값;
}
meaisín_Word uirlis_UDP_oscail(meaisín_Word uimhir_phoirt) {
    intptr_t comhad_hanla = 호출(32, 2, 2, 17); if (comhad_hanla < 0) return (uint32_t)comhad_hanla;
    struct 자바주소 첫째값 = UDP_ADDRESS(uimhir_phoirt);
    첫째값.ADDRESS = 0;
    intptr_t staid_VALUE = 호출(33, comhad_hanla, (meaisín_Word)&첫째값, sizeof(첫째값));
    if (staid_VALUE < 0) { uirlis_dún(comhad_hanla); return (uint32_t)staid_VALUE; }
    return comhad_hanla;
}
meaisín_Word uirlis_UDP_seol(meaisín_Word comhad_hanla, meaisín_Word uimhir_phoirt, meaisín_Word ARRAY_VALUE, meaisín_Word fad_VALUE) {
    const meaisín_Word *원본주소 = (const meaisín_Word *)ARRAY_VALUE; unsigned char sonraí[512];
    if (fad_VALUE > 512 || fad_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (meaisín_Word 순번 = 0; 순번 < fad_VALUE; 순번++) sonraí[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(uimhir_phoirt);
    return (uint32_t)사용자호출(34, comhad_hanla, (meaisín_Word)sonraí, fad_VALUE, 0, (meaisín_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t mír_COUNT) { return (mír_COUNT>>24)|((mír_COUNT>>8)&0xff00)|((mír_COUNT<<8)&0xff0000)|(mír_COUNT<<24); }
meaisín_Word uirlis_UDP_seol_ADDRESS(meaisín_Word comhad_hanla, meaisín_Word ADDRESS, meaisín_Word uimhir_phoirt, meaisín_Word ARRAY_VALUE, meaisín_Word fad_VALUE) {
    const meaisín_Word *원본주소 = (const meaisín_Word *)ARRAY_VALUE; unsigned char sonraí[512];
    if (fad_VALUE > 512 || fad_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (meaisín_Word 순번 = 0; 순번 < fad_VALUE; 순번++) sonraí[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(uimhir_phoirt); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, comhad_hanla, (meaisín_Word)sonraí, fad_VALUE, 0, (meaisín_Word)&첫째값, sizeof(첫째값));
}
meaisín_Word uirlis_nasc(meaisín_Word comhad_hanla, meaisín_Word ADDRESS, meaisín_Word uimhir_phoirt) {
    struct 자바주소 첫째값 = UDP_ADDRESS(uimhir_phoirt); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t Rith_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t tomhas = 호출(37, comhad_hanla, (meaisín_Word)&첫째값, sizeof(첫째값));
        if (tomhas != -115) return (uint32_t)tomhas;
        if ((uint32_t)(호출(7, 0, 0, 0) - Rith_2) >= 1000) return (uint32_t)-110;
    }
}
meaisín_Word 도구전문받기(meaisín_Word comhad_hanla, meaisín_Word ARRAY_VALUE, meaisín_Word 수용량) {
    meaisín_Word *sprioc_ADDRESS_08bbd577 = (meaisín_Word *)ARRAY_VALUE; unsigned char sonraí[512];
    if (수용량 > 512 || sprioc_ADDRESS_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned fad_sonraí = sizeof(첫째값);
    intptr_t mír_COUNT = 사용자호출(35, comhad_hanla, (meaisín_Word)sonraí, 수용량, 0, (meaisín_Word)&첫째값, (meaisín_Word)&fad_sonraí);
    if (mír_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < mír_COUNT; 순번++) sprioc_ADDRESS_08bbd577[순번 + 1] = sonraí[순번]; sprioc_ADDRESS_08bbd577[513] = (첫째값.uimhir_phoirt << 8 | 첫째값.uimhir_phoirt >> 8) & 65535; sprioc_ADDRESS_08bbd577[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)mír_COUNT;
}
meaisín_Word uirlis_UDP_port(meaisín_Word comhad_hanla) {
    struct 자바주소 첫째값; unsigned fad_sonraí = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, comhad_hanla, (meaisín_Word)&첫째값, (meaisín_Word)&fad_sonraí);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.uimhir_phoirt << 8 | 첫째값.uimhir_phoirt >> 8) & 65535);
}
meaisín_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
meaisín_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
meaisín_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
meaisín_Word 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
meaisín_Word 도구사각형(meaisín_Word x_chomhordanáid, meaisín_Word 세로좌표, meaisín_Word 너비값, meaisín_Word 높이값, meaisín_Word 색상) {
    return (uint32_t)사용자호출(13, x_chomhordanáid, 세로좌표, 색상, 너비값, 높이값, 0);
}

meaisín_Word uirlis_sruth(meaisín_Word Gníomh,meaisín_Word comhad_hanla,meaisín_Word VALUE){
    if(Gníomh==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADDRESS(VALUE);
    if(Gníomh==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,comhad_hanla,(meaisín_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,comhad_hanla,4,0));}
    if(Gníomh==2)return (uint32_t)호출(37,comhad_hanla,(meaisín_Word)&첫째값,sizeof(첫째값));
    if(Gníomh==3)return (uint32_t)호출(39,comhad_hanla,0,0);
    if(Gníomh==4)return uirlis_UDP_port(comhad_hanla);
    if(Gníomh==5)return (uint32_t)호출(40,comhad_hanla,0,0);
    return (uint32_t)-22;
}
meaisín_Word uirlis_GUI(meaisín_Word Gníomh,meaisín_Word aitheantóir_VALUE,meaisín_Word 첫째값,meaisín_Word SECOND_VALUE,meaisín_Word pointe_cóid,meaisín_Word sprioc_sonraí){return (uint32_t)사용자호출(20,Gníomh,aitheantóir_VALUE,첫째값,SECOND_VALUE,pointe_cóid,sprioc_sonraí);}
meaisín_Word uirlis_GUI_SMS(meaisín_Word aitheantóir_VALUE,meaisín_Word ARRAY_VALUE,meaisín_Word mír_COUNT){
    const meaisín_Word *원본주소=(const meaisín_Word *)ARRAY_VALUE;uint32_t sonraí[127];unsigned iontráil_COUNT=0;
    if(mír_COUNT>원본주소[0])return (uint32_t)-22;
    for(meaisín_Word 순번=0;순번<mír_COUNT;순번++){unsigned carachtar_ionchódú=원본주소[순번+1];if(carachtar_ionchódú>=0xd800&&carachtar_ionchódú<=0xdbff&&순번+1<mír_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;carachtar_ionchódú=0x10000+((carachtar_ionchódú-0xd800)<<10)+낮은값-0xdc00;}if(iontráil_COUNT==127)return (uint32_t)-22;sonraí[iontráil_COUNT++]=carachtar_ionchódú;}
    return (uint32_t)사용자호출(21,aitheantóir_VALUE,(meaisín_Word)sonraí,iontráil_COUNT,0,0,0);
}
