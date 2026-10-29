#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Kōnae/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "pūpū.h"
typedef uintptr_t mīhini_Word;
static int kāwai_uara;
static int 꾸러미사용중, 꾸러미인수이동;
static mīhini_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned tuemi_COUNT, mīhini_Word 첫째값, mīhini_Word SECOND_uara, mīhini_Word waehere_pūāhua) {
    return 사용자호출(tuemi_COUNT, 첫째값, SECOND_uara, waehere_pūāhua, 0, 0, 0);
}
static void 바이트들(const char *raraunga_tūranga, size_t tuemi_COUNT) { 호출(1, 1, (mīhini_Word)raraunga_tūranga, tuemi_COUNT); }
static void pūāhua(unsigned waehere_pūāhua) {
    unsigned char raraunga[4]; unsigned tuemi_COUNT = 0;
    if (waehere_pūāhua < 128) raraunga[tuemi_COUNT++] = waehere_pūāhua;
    else if (waehere_pūāhua < 2048) { raraunga[tuemi_COUNT++] = 0xc0 | (waehere_pūāhua >> 6); raraunga[tuemi_COUNT++] = 0x80 | (waehere_pūāhua & 63); }
    else if (waehere_pūāhua < 65536) { raraunga[tuemi_COUNT++] = 0xe0 | (waehere_pūāhua >> 12); raraunga[tuemi_COUNT++] = 0x80 | ((waehere_pūāhua >> 6) & 63); raraunga[tuemi_COUNT++] = 0x80 | (waehere_pūāhua & 63); }
    else { raraunga[tuemi_COUNT++] = 0xf0 | (waehere_pūāhua >> 18); raraunga[tuemi_COUNT++] = 0x80 | ((waehere_pūāhua >> 12) & 63); raraunga[tuemi_COUNT++] = 0x80 | ((waehere_pūāhua >> 6) & 63); raraunga[tuemi_COUNT++] = 0x80 | (waehere_pūāhua & 63); }
    바이트들((const char *)raraunga, tuemi_COUNT);
}
mīhini_Word utauta_pūāhua(mīhini_Word uara) {
    unsigned waehere_pūāhua = uara;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (waehere_pūāhua >= 0xdc00 && waehere_pūāhua <= 0xdfff) { pūāhua(0x10000 + ((높은부분 - 0xd800) << 10) + waehere_pūāhua - 0xdc00); return 1; }
        pūāhua(0xfffd);
    }
    if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdbff) 대기중짝글자 = waehere_pūāhua;
    else pūāhua(waehere_pūāhua > 0x10ffff || (waehere_pūāhua >= 0xdc00 && waehere_pūāhua <= 0xdfff) ? 0xfffd : waehere_pūāhua);
    return 1;
}
mīhini_Word 도구출력(mīhini_Word uara) {
    const mīhini_Word *aho_raraunga = (const mīhini_Word *)uara;
    for (mīhini_Word 순번 = 0; 순번 < aho_raraunga[0]; 순번++) utauta_pūāhua(aho_raraunga[순번 + 1]);
    return aho_raraunga[0];
}
static int ara(mīhini_Word ahanoa_Pūranga_kōrero, char mēhua_raraunga[512]) {
    const mīhini_Word *첫째값 = (const mīhini_Word *)ahanoa_Pūranga_kōrero;
    unsigned 사용량 = 0;
    for (mīhini_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned waehere_pūāhua = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] aratuka_MODE 경로와 호환한다.
        if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; waehere_pūāhua = 0x10000 + ((waehere_pūāhua - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdfff) return -22;
        unsigned tuemi_COUNT = waehere_pūāhua < 128 ? 1 : waehere_pūāhua < 2048 ? 2 : waehere_pūāhua < 65536 ? 3 : 4;
        if (사용량 + tuemi_COUNT > 511) return -36;
        if (tuemi_COUNT == 1) mēhua_raraunga[사용량++] = waehere_pūāhua;
        else {
            mēhua_raraunga[사용량++] = (tuemi_COUNT == 2 ? 0xc0 : tuemi_COUNT == 3 ? 0xe0 : 0xf0) | (waehere_pūāhua >> (6 * (tuemi_COUNT - 1)));
            for (unsigned 안쪽순번 = tuemi_COUNT - 1; 안쪽순번; 안쪽순번--) mēhua_raraunga[사용량++] = 0x80 | ((waehere_pūāhua >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    mēhua_raraunga[사용량] = 0; return 사용량 ? 0 : -22;
}
mīhini_Word utauta_tiwhikete(mīhini_Word Ingoa, mīhini_Word 설정비트) {
    char raraunga_tūranga[512]; int Pōhēhē = ara(Ingoa, raraunga_tūranga);
    return (uint32_t)(Pōhēhē ? Pōhēhē : 호출(3, (mīhini_Word)raraunga_tūranga, 설정비트, 0));
}
mīhini_Word utauta_kati(mīhini_Word kōnae_raweke) { return (uint32_t)호출(4, kōnae_raweke, 0, 0); }
mīhini_Word 도구바이트읽기(mīhini_Word kōnae_raweke) {
    unsigned char SECOND_uara; intptr_t tuemi_COUNT = 호출(2, kōnae_raweke, (mīhini_Word)&SECOND_uara, 1);
    return (uint32_t)(tuemi_COUNT == 1 ? SECOND_uara : tuemi_COUNT == 0 ? 256 : tuemi_COUNT);
}
mīhini_Word utauta_tuhi_paita(mīhini_Word kōnae_raweke, mīhini_Word uara) {
    unsigned char SECOND_uara = uara; return (uint32_t)호출(1, kōnae_raweke, (mīhini_Word)&SECOND_uara, 1);
}
mīhini_Word 도구읽기(mīhini_Word Ingoa, mīhini_Word ūnga_raraunga_ADDRESS) {
    if (꾸러미사용중) {
        char raraunga_tūranga[512]; int Pōhēhē = ara(Ingoa, raraunga_tūranga); if (Pōhēhē) return (uint32_t)Pōhēhē;
        unsigned tuemi_COUNT = 0; while (raraunga_tūranga[tuemi_COUNT]) tuemi_COUNT++;
        if (tuemi_COUNT >= 6) for (unsigned 순번 = 0; 순번 < tuemi_COUNT - 6; 순번++) if (raraunga_tūranga[순번] == '.') raraunga_tūranga[순번] = '/';
        unsigned char 바이트들[16384]; mīhini_Word *ūnga_uara_tūranga = (mīhini_Word *)ūnga_raraunga_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(raraunga_tūranga, 바이트들, ūnga_uara_tūranga[0] < sizeof(바이트들) ? ūnga_uara_tūranga[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) ūnga_uara_tūranga[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int kōnae_raweke = 꾸러미사용중 ? -2 : (int32_t)utauta_tiwhikete(Ingoa, 0);
    if (kōnae_raweke < 0) {
        char raraunga_tūranga[512]; int Pōhēhē = ara(Ingoa, raraunga_tūranga); if (Pōhēhē) return (uint32_t)Pōhēhē;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Panuku_OFFSET = 자바클래스들[순번].Ingoa; unsigned 안쪽순번 = 0;
            while (raraunga_tūranga[안쪽순번] && raraunga_tūranga[안쪽순번] == Panuku_OFFSET[안쪽순번]) 안쪽순번++;
            if (raraunga_tūranga[안쪽순번] || Panuku_OFFSET[안쪽순번]) continue;
            mīhini_Word *ūnga_uara_tūranga = (mīhini_Word *)ūnga_raraunga_ADDRESS;
            if (ūnga_uara_tūranga[0] < 자바클래스들[순번].rahi) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].rahi; 안쪽순번++) ūnga_uara_tūranga[안쪽순번 + 1] = 자바클래스들[순번].raraunga[안쪽순번];
            return 자바클래스들[순번].rahi;
        }
        return (uint32_t)kōnae_raweke;
    }
    mīhini_Word *첫째값 = (mīhini_Word *)ūnga_raraunga_ADDRESS;
    intptr_t rahi = 호출(9, kōnae_raweke, 0, 0), 완료량 = 0;
    if (rahi < 0 || (mīhini_Word)rahi > 첫째값[0]) { utauta_kati(kōnae_raweke); return (uint32_t)(rahi < 0 ? rahi : -27); }
    unsigned char raraunga_aukati[256];
    while (완료량 < rahi) {
        intptr_t tuemi_COUNT = 호출(2, kōnae_raweke, (mīhini_Word)raraunga_aukati, rahi - 완료량 < 256 ? rahi - 완료량 : 256);
        if (tuemi_COUNT <= 0) { utauta_kati(kōnae_raweke); return (uint32_t)(tuemi_COUNT ? tuemi_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < tuemi_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = raraunga_aukati[순번];
        완료량 += tuemi_COUNT;
    }
    utauta_kati(kōnae_raweke); return 완료량;
}
mīhini_Word utauta_tuhi(mīhini_Word Ingoa, mīhini_Word 원본자료, mīhini_Word tāurunga_COUNT) {
    const mīhini_Word *첫째값 = (const mīhini_Word *)원본자료;
    if (tāurunga_COUNT > 첫째값[0] || tāurunga_COUNT > 16384) return (uint32_t)-27;
    int kōnae_raweke = (int32_t)utauta_tiwhikete(Ingoa, 577); if (kōnae_raweke < 0) return (uint32_t)kōnae_raweke;
    unsigned char raraunga_aukati[256]; mīhini_Word 완료량 = 0;
    while (완료량 < tāurunga_COUNT) {
        mīhini_Word tuemi_COUNT = tāurunga_COUNT - 완료량 < 256 ? tāurunga_COUNT - 완료량 : 256;
        for (mīhini_Word 순번 = 0; 순번 < tuemi_COUNT; 순번++) raraunga_aukati[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t mēhua = 호출(1, kōnae_raweke, (mīhini_Word)raraunga_aukati, tuemi_COUNT);
        if (mēhua <= 0) { utauta_kati(kōnae_raweke); return (uint32_t)(mēhua ? mēhua : -5); }
        완료량 += mēhua;
    }
    utauta_kati(kōnae_raweke); return tāurunga_COUNT;
}
mīhini_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mīhini_Word utauta_tohenga(mīhini_Word Rapu_INDEX) {
    static const mīhini_Word putua_uara[1] = {0};
    if (Rapu_INDEX >= 8) return (mīhini_Word)putua_uara;
    unsigned char 입력결과[256]; intptr_t tuemi_COUNT;
    if (꾸러미사용중 && Rapu_INDEX == 0) { const char *raraunga_tūranga = 꾸러미진입클래스(); tuemi_COUNT = 0; while (raraunga_tūranga[tuemi_COUNT] && tuemi_COUNT < 255) { 입력결과[tuemi_COUNT] = raraunga_tūranga[tuemi_COUNT]; tuemi_COUNT++; } }
    else tuemi_COUNT = 호출(15, Rapu_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mīhini_Word)입력결과, sizeof(입력결과));
    if (tuemi_COUNT < 0) return (mīhini_Word)putua_uara;
    mīhini_Word *mēhua_raraunga = 전달인수[Rapu_INDEX]; unsigned tāurunga_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < tuemi_COUNT;) {
        unsigned waehere_pūāhua = 입력결과[순번++], 더있음 = waehere_pūāhua < 128 ? 0 : waehere_pūāhua >= 0xc2 && waehere_pūāhua < 0xe0 ? 1 : waehere_pūāhua < 0xf0 && waehere_pūāhua >= 0xe0 ? 2 : waehere_pūāhua >= 0xf0 && waehere_pūāhua <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > tuemi_COUNT) { mēhua_raraunga[++tāurunga_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) waehere_pūāhua &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { waehere_pūāhua = (waehere_pūāhua << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || waehere_pūāhua < 최소값 || waehere_pūāhua > 0x10ffff || (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdfff)) waehere_pūāhua = 0xfffd;
        if (waehere_pūāhua >= 65536) { waehere_pūāhua -= 65536; mēhua_raraunga[++tāurunga_COUNT] = 0xd800 | (waehere_pūāhua >> 10); mēhua_raraunga[++tāurunga_COUNT] = 0xdc00 | (waehere_pūāhua & 1023); }
        else mēhua_raraunga[++tāurunga_COUNT] = waehere_pūāhua;
    }
    mēhua_raraunga[0] = tāurunga_COUNT; return (mīhini_Word)mēhua_raraunga;
}
mīhini_Word 도구분류(void) { return kāwai_uara; }
void 커널중단(const char *알림문) {
    const char *raraunga_tūranga = 알림문; while (*raraunga_tūranga) raraunga_tūranga++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, raraunga_tūranga - 알림문); pūāhua(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_kaiwhakamahi_kaupapa(int aratuka_MODE) {
    kāwai_uara = aratuka_MODE;
    unsigned char 첫항목[256]; intptr_t tuemi_COUNT = 호출(15, 0, (mīhini_Word)첫항목, sizeof(첫항목));
    if (aratuka_MODE == 2 || (aratuka_MODE == 1 && tuemi_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = aratuka_MODE == 2 ? 0 : 1;
        char kōnae_tāurunga_ingoa[256]; intptr_t roa_raraunga = 호출(15, 꾸러미인수이동, (mīhini_Word)kōnae_tāurunga_ingoa, sizeof(kōnae_tāurunga_ingoa));
        if (roa_raraunga <= 0 || 꾸러미열기(kōnae_tāurunga_ingoa) < 0) {
            static const char Pōhēhē[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Pōhēhē, sizeof(Pōhēhē) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int mēhua = 자바진입();
    if (대기중짝글자) pūāhua(0xfffd);
    return mēhua;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Whānau, 접속번호; uint32_t ADDRESS; unsigned char 영값[8]; };
static struct 자바주소 UDP_ADDRESS(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mīhini_Word utauta_UDP_tiwhikete(mīhini_Word 접속번호) {
    intptr_t kōnae_raweke = 호출(32, 2, 2, 17); if (kōnae_raweke < 0) return (uint32_t)kōnae_raweke;
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호);
    첫째값.ADDRESS = 0;
    intptr_t tūnga_uara = 호출(33, kōnae_raweke, (mīhini_Word)&첫째값, sizeof(첫째값));
    if (tūnga_uara < 0) { utauta_kati(kōnae_raweke); return (uint32_t)tūnga_uara; }
    return kōnae_raweke;
}
mīhini_Word utauta_UDP_tuku(mīhini_Word kōnae_raweke, mīhini_Word 접속번호, mīhini_Word HUĀNGA_uara, mīhini_Word roa_uara) {
    const mīhini_Word *원본주소 = (const mīhini_Word *)HUĀNGA_uara; unsigned char raraunga[512];
    if (roa_uara > 512 || roa_uara > 원본주소[0]) return (uint32_t)-90;
    for (mīhini_Word 순번 = 0; 순번 < roa_uara; 순번++) raraunga[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호);
    return (uint32_t)사용자호출(34, kōnae_raweke, (mīhini_Word)raraunga, roa_uara, 0, (mīhini_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t tuemi_COUNT) { return (tuemi_COUNT>>24)|((tuemi_COUNT>>8)&0xff00)|((tuemi_COUNT<<8)&0xff0000)|(tuemi_COUNT<<24); }
mīhini_Word utauta_UDP_tuku_ADDRESS(mīhini_Word kōnae_raweke, mīhini_Word ADDRESS, mīhini_Word 접속번호, mīhini_Word HUĀNGA_uara, mīhini_Word roa_uara) {
    const mīhini_Word *원본주소 = (const mīhini_Word *)HUĀNGA_uara; unsigned char raraunga[512];
    if (roa_uara > 512 || roa_uara > 원본주소[0]) return (uint32_t)-90;
    for (mīhini_Word 순번 = 0; 순번 < roa_uara; 순번++) raraunga[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, kōnae_raweke, (mīhini_Word)raraunga, roa_uara, 0, (mīhini_Word)&첫째값, sizeof(첫째값));
}
mīhini_Word utauta_TŪHONO(mīhini_Word kōnae_raweke, mīhini_Word ADDRESS, mīhini_Word 접속번호) {
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t whakahaere = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t mēhua = 호출(37, kōnae_raweke, (mīhini_Word)&첫째값, sizeof(첫째값));
        if (mēhua != -115) return (uint32_t)mēhua;
        if ((uint32_t)(호출(7, 0, 0, 0) - whakahaere) >= 1000) return (uint32_t)-110;
    }
}
mīhini_Word 도구전문받기(mīhini_Word kōnae_raweke, mīhini_Word HUĀNGA_uara, mīhini_Word 수용량) {
    mīhini_Word *ūnga_ADDRESS_08bbd577 = (mīhini_Word *)HUĀNGA_uara; unsigned char raraunga[512];
    if (수용량 > 512 || ūnga_ADDRESS_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned roa_raraunga = sizeof(첫째값);
    intptr_t tuemi_COUNT = 사용자호출(35, kōnae_raweke, (mīhini_Word)raraunga, 수용량, 0, (mīhini_Word)&첫째값, (mīhini_Word)&roa_raraunga);
    if (tuemi_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < tuemi_COUNT; 순번++) ūnga_ADDRESS_08bbd577[순번 + 1] = raraunga[순번]; ūnga_ADDRESS_08bbd577[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; ūnga_ADDRESS_08bbd577[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)tuemi_COUNT;
}
mīhini_Word utauta_UDP_kawe(mīhini_Word kōnae_raweke) {
    struct 자바주소 첫째값; unsigned roa_raraunga = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, kōnae_raweke, (mīhini_Word)&첫째값, (mīhini_Word)&roa_raraunga);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
mīhini_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mīhini_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mīhini_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mīhini_Word 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
mīhini_Word 도구사각형(mīhini_Word taunga_x, mīhini_Word 세로좌표, mīhini_Word 너비값, mīhini_Word 높이값, mīhini_Word 색상) {
    return (uint32_t)사용자호출(13, taunga_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

mīhini_Word utauta_roma(mīhini_Word hohenga,mīhini_Word kōnae_raweke,mīhini_Word uara){
    if(hohenga==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADDRESS(uara);
    if(hohenga==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,kōnae_raweke,(mīhini_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,kōnae_raweke,4,0));}
    if(hohenga==2)return (uint32_t)호출(37,kōnae_raweke,(mīhini_Word)&첫째값,sizeof(첫째값));
    if(hohenga==3)return (uint32_t)호출(39,kōnae_raweke,0,0);
    if(hohenga==4)return utauta_UDP_kawe(kōnae_raweke);
    if(hohenga==5)return (uint32_t)호출(40,kōnae_raweke,0,0);
    return (uint32_t)-22;
}
mīhini_Word utauta_AKW(mīhini_Word hohenga,mīhini_Word pūtāutu_uara,mīhini_Word 첫째값,mīhini_Word SECOND_uara,mīhini_Word waehere_pūāhua,mīhini_Word ūnga_raraunga){return (uint32_t)사용자호출(20,hohenga,pūtāutu_uara,첫째값,SECOND_uara,waehere_pūāhua,ūnga_raraunga);}
mīhini_Word utauta_AKW_TEXT(mīhini_Word pūtāutu_uara,mīhini_Word HUĀNGA_uara,mīhini_Word tuemi_COUNT){
    const mīhini_Word *원본주소=(const mīhini_Word *)HUĀNGA_uara;uint32_t raraunga[127];unsigned tāurunga_COUNT=0;
    if(tuemi_COUNT>원본주소[0])return (uint32_t)-22;
    for(mīhini_Word 순번=0;순번<tuemi_COUNT;순번++){unsigned pūāhua_whakawaehere=원본주소[순번+1];if(pūāhua_whakawaehere>=0xd800&&pūāhua_whakawaehere<=0xdbff&&순번+1<tuemi_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;pūāhua_whakawaehere=0x10000+((pūāhua_whakawaehere-0xd800)<<10)+낮은값-0xdc00;}if(tāurunga_COUNT==127)return (uint32_t)-22;raraunga[tāurunga_COUNT++]=pūāhua_whakawaehere;}
    return (uint32_t)사용자호출(21,pūtāutu_uara,(mīhini_Word)raraunga,tāurunga_COUNT,0,0,0);
}
