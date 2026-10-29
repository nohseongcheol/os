#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 faidhle/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "trusgan.h"
typedef uintptr_t inneal_Word;
static int roinn_seòrsa_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static inneal_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned nì_COUNT, inneal_Word 첫째값, inneal_Word SECOND_VALUE, inneal_Word còd_a_charactair) {
    return 사용자호출(nì_COUNT, 첫째값, SECOND_VALUE, còd_a_charactair, 0, 0, 0);
}
static void 바이트들(const char *dàta_suidhich, size_t nì_COUNT) { 호출(1, 1, (inneal_Word)dàta_suidhich, nì_COUNT); }
static void caractar(unsigned còd_a_charactair) {
    unsigned char dàta[4]; unsigned nì_COUNT = 0;
    if (còd_a_charactair < 128) dàta[nì_COUNT++] = còd_a_charactair;
    else if (còd_a_charactair < 2048) { dàta[nì_COUNT++] = 0xc0 | (còd_a_charactair >> 6); dàta[nì_COUNT++] = 0x80 | (còd_a_charactair & 63); }
    else if (còd_a_charactair < 65536) { dàta[nì_COUNT++] = 0xe0 | (còd_a_charactair >> 12); dàta[nì_COUNT++] = 0x80 | ((còd_a_charactair >> 6) & 63); dàta[nì_COUNT++] = 0x80 | (còd_a_charactair & 63); }
    else { dàta[nì_COUNT++] = 0xf0 | (còd_a_charactair >> 18); dàta[nì_COUNT++] = 0x80 | ((còd_a_charactair >> 12) & 63); dàta[nì_COUNT++] = 0x80 | ((còd_a_charactair >> 6) & 63); dàta[nì_COUNT++] = 0x80 | (còd_a_charactair & 63); }
    바이트들((const char *)dàta, nì_COUNT);
}
inneal_Word inneal_caractar(inneal_Word VALUE) {
    unsigned còd_a_charactair = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (còd_a_charactair >= 0xdc00 && còd_a_charactair <= 0xdfff) { caractar(0x10000 + ((높은부분 - 0xd800) << 10) + còd_a_charactair - 0xdc00); return 1; }
        caractar(0xfffd);
    }
    if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdbff) 대기중짝글자 = còd_a_charactair;
    else caractar(còd_a_charactair > 0x10ffff || (còd_a_charactair >= 0xdc00 && còd_a_charactair <= 0xdfff) ? 0xfffd : còd_a_charactair);
    return 1;
}
inneal_Word 도구출력(inneal_Word VALUE) {
    const inneal_Word *sreang_dàta = (const inneal_Word *)VALUE;
    for (inneal_Word 순번 = 0; 순번 < sreang_dàta[0]; 순번++) inneal_caractar(sreang_dàta[순번 + 1]);
    return sreang_dàta[0];
}
static int Slighe(inneal_Word nì_fiosrachadh, char tomhas_dàta[512]) {
    const inneal_Word *첫째값 = (const inneal_Word *)nì_fiosrachadh;
    unsigned 사용량 = 0;
    for (inneal_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned còd_a_charactair = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] dòigh_MODE 경로와 호환한다.
        if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; còd_a_charactair = 0x10000 + ((còd_a_charactair - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdfff) return -22;
        unsigned nì_COUNT = còd_a_charactair < 128 ? 1 : còd_a_charactair < 2048 ? 2 : còd_a_charactair < 65536 ? 3 : 4;
        if (사용량 + nì_COUNT > 511) return -36;
        if (nì_COUNT == 1) tomhas_dàta[사용량++] = còd_a_charactair;
        else {
            tomhas_dàta[사용량++] = (nì_COUNT == 2 ? 0xc0 : nì_COUNT == 3 ? 0xe0 : 0xf0) | (còd_a_charactair >> (6 * (nì_COUNT - 1)));
            for (unsigned 안쪽순번 = nì_COUNT - 1; 안쪽순번; 안쪽순번--) tomhas_dàta[사용량++] = 0x80 | ((còd_a_charactair >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    tomhas_dàta[사용량] = 0; return 사용량 ? 0 : -22;
}
inneal_Word inneal_fosgail(inneal_Word Ainm, inneal_Word 설정비트) {
    char dàta_suidhich[512]; int Mearachd = Slighe(Ainm, dàta_suidhich);
    return (uint32_t)(Mearachd ? Mearachd : 호출(3, (inneal_Word)dàta_suidhich, 설정비트, 0));
}
inneal_Word inneal_dùin(inneal_Word faidhle_làmhrachan) { return (uint32_t)호출(4, faidhle_làmhrachan, 0, 0); }
inneal_Word 도구바이트읽기(inneal_Word faidhle_làmhrachan) {
    unsigned char SECOND_VALUE; intptr_t nì_COUNT = 호출(2, faidhle_làmhrachan, (inneal_Word)&SECOND_VALUE, 1);
    return (uint32_t)(nì_COUNT == 1 ? SECOND_VALUE : nì_COUNT == 0 ? 256 : nì_COUNT);
}
inneal_Word inneal_sgrìobh_baidht(inneal_Word faidhle_làmhrachan, inneal_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, faidhle_làmhrachan, (inneal_Word)&SECOND_VALUE, 1);
}
inneal_Word 도구읽기(inneal_Word Ainm, inneal_Word ceann_uidhe_dàta_ADDRESS) {
    if (꾸러미사용중) {
        char dàta_suidhich[512]; int Mearachd = Slighe(Ainm, dàta_suidhich); if (Mearachd) return (uint32_t)Mearachd;
        unsigned nì_COUNT = 0; while (dàta_suidhich[nì_COUNT]) nì_COUNT++;
        if (nì_COUNT >= 6) for (unsigned 순번 = 0; 순번 < nì_COUNT - 6; 순번++) if (dàta_suidhich[순번] == '.') dàta_suidhich[순번] = '/';
        unsigned char 바이트들[16384]; inneal_Word *ceann_uidhe_VALUE_suidhich = (inneal_Word *)ceann_uidhe_dàta_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(dàta_suidhich, 바이트들, ceann_uidhe_VALUE_suidhich[0] < sizeof(바이트들) ? ceann_uidhe_VALUE_suidhich[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) ceann_uidhe_VALUE_suidhich[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int faidhle_làmhrachan = 꾸러미사용중 ? -2 : (int32_t)inneal_fosgail(Ainm, 0);
    if (faidhle_làmhrachan < 0) {
        char dàta_suidhich[512]; int Mearachd = Slighe(Ainm, dàta_suidhich); if (Mearachd) return (uint32_t)Mearachd;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *air_adhart_OFFSET = 자바클래스들[순번].Ainm; unsigned 안쪽순번 = 0;
            while (dàta_suidhich[안쪽순번] && dàta_suidhich[안쪽순번] == air_adhart_OFFSET[안쪽순번]) 안쪽순번++;
            if (dàta_suidhich[안쪽순번] || air_adhart_OFFSET[안쪽순번]) continue;
            inneal_Word *ceann_uidhe_VALUE_suidhich = (inneal_Word *)ceann_uidhe_dàta_ADDRESS;
            if (ceann_uidhe_VALUE_suidhich[0] < 자바클래스들[순번].atharraich_am_meud) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].atharraich_am_meud; 안쪽순번++) ceann_uidhe_VALUE_suidhich[안쪽순번 + 1] = 자바클래스들[순번].dàta[안쪽순번];
            return 자바클래스들[순번].atharraich_am_meud;
        }
        return (uint32_t)faidhle_làmhrachan;
    }
    inneal_Word *첫째값 = (inneal_Word *)ceann_uidhe_dàta_ADDRESS;
    intptr_t atharraich_am_meud = 호출(9, faidhle_làmhrachan, 0, 0), 완료량 = 0;
    if (atharraich_am_meud < 0 || (inneal_Word)atharraich_am_meud > 첫째값[0]) { inneal_dùin(faidhle_làmhrachan); return (uint32_t)(atharraich_am_meud < 0 ? atharraich_am_meud : -27); }
    unsigned char dàta_bac[256];
    while (완료량 < atharraich_am_meud) {
        intptr_t nì_COUNT = 호출(2, faidhle_làmhrachan, (inneal_Word)dàta_bac, atharraich_am_meud - 완료량 < 256 ? atharraich_am_meud - 완료량 : 256);
        if (nì_COUNT <= 0) { inneal_dùin(faidhle_làmhrachan); return (uint32_t)(nì_COUNT ? nì_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < nì_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = dàta_bac[순번];
        완료량 += nì_COUNT;
    }
    inneal_dùin(faidhle_làmhrachan); return 완료량;
}
inneal_Word inneal_sgrìobh(inneal_Word Ainm, inneal_Word 원본자료, inneal_Word cur_a_steach_COUNT) {
    const inneal_Word *첫째값 = (const inneal_Word *)원본자료;
    if (cur_a_steach_COUNT > 첫째값[0] || cur_a_steach_COUNT > 16384) return (uint32_t)-27;
    int faidhle_làmhrachan = (int32_t)inneal_fosgail(Ainm, 577); if (faidhle_làmhrachan < 0) return (uint32_t)faidhle_làmhrachan;
    unsigned char dàta_bac[256]; inneal_Word 완료량 = 0;
    while (완료량 < cur_a_steach_COUNT) {
        inneal_Word nì_COUNT = cur_a_steach_COUNT - 완료량 < 256 ? cur_a_steach_COUNT - 완료량 : 256;
        for (inneal_Word 순번 = 0; 순번 < nì_COUNT; 순번++) dàta_bac[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t tomhas = 호출(1, faidhle_làmhrachan, (inneal_Word)dàta_bac, nì_COUNT);
        if (tomhas <= 0) { inneal_dùin(faidhle_làmhrachan); return (uint32_t)(tomhas ? tomhas : -5); }
        완료량 += tomhas;
    }
    inneal_dùin(faidhle_làmhrachan); return cur_a_steach_COUNT;
}
inneal_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
inneal_Word inneal_argamaid(inneal_Word LOOKUP_INDEX) {
    static const inneal_Word falamh_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (inneal_Word)falamh_VALUE;
    unsigned char 입력결과[256]; intptr_t nì_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *dàta_suidhich = 꾸러미진입클래스(); nì_COUNT = 0; while (dàta_suidhich[nì_COUNT] && nì_COUNT < 255) { 입력결과[nì_COUNT] = dàta_suidhich[nì_COUNT]; nì_COUNT++; } }
    else nì_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (inneal_Word)입력결과, sizeof(입력결과));
    if (nì_COUNT < 0) return (inneal_Word)falamh_VALUE;
    inneal_Word *tomhas_dàta = 전달인수[LOOKUP_INDEX]; unsigned cur_a_steach_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < nì_COUNT;) {
        unsigned còd_a_charactair = 입력결과[순번++], 더있음 = còd_a_charactair < 128 ? 0 : còd_a_charactair >= 0xc2 && còd_a_charactair < 0xe0 ? 1 : còd_a_charactair < 0xf0 && còd_a_charactair >= 0xe0 ? 2 : còd_a_charactair >= 0xf0 && còd_a_charactair <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > nì_COUNT) { tomhas_dàta[++cur_a_steach_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) còd_a_charactair &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { còd_a_charactair = (còd_a_charactair << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || còd_a_charactair < 최소값 || còd_a_charactair > 0x10ffff || (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdfff)) còd_a_charactair = 0xfffd;
        if (còd_a_charactair >= 65536) { còd_a_charactair -= 65536; tomhas_dàta[++cur_a_steach_COUNT] = 0xd800 | (còd_a_charactair >> 10); tomhas_dàta[++cur_a_steach_COUNT] = 0xdc00 | (còd_a_charactair & 1023); }
        else tomhas_dàta[++cur_a_steach_COUNT] = còd_a_charactair;
    }
    tomhas_dàta[0] = cur_a_steach_COUNT; return (inneal_Word)tomhas_dàta;
}
inneal_Word 도구분류(void) { return roinn_seòrsa_VALUE; }
void 커널중단(const char *알림문) {
    const char *dàta_suidhich = 알림문; while (*dàta_suidhich) dàta_suidhich++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, dàta_suidhich - 알림문); caractar(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_cleachdaiche_ap(int dòigh_MODE) {
    roinn_seòrsa_VALUE = dòigh_MODE;
    unsigned char 첫항목[256]; intptr_t nì_COUNT = 호출(15, 0, (inneal_Word)첫항목, sizeof(첫항목));
    if (dòigh_MODE == 2 || (dòigh_MODE == 1 && nì_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = dòigh_MODE == 2 ? 0 : 1;
        char faidhle_cur_a_steach_ainm[256]; intptr_t faid_dàta = 호출(15, 꾸러미인수이동, (inneal_Word)faidhle_cur_a_steach_ainm, sizeof(faidhle_cur_a_steach_ainm));
        if (faid_dàta <= 0 || 꾸러미열기(faidhle_cur_a_steach_ainm) < 0) {
            static const char Mearachd[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Mearachd, sizeof(Mearachd) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int tomhas = 자바진입();
    if (대기중짝글자) caractar(0xfffd);
    return tomhas;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t teaghlach, 접속번호; uint32_t ADDRESS; unsigned char 영값[8]; };
static struct 자바주소 UDP_ADDRESS(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
inneal_Word inneal_UDP_fosgail(inneal_Word 접속번호) {
    intptr_t faidhle_làmhrachan = 호출(32, 2, 2, 17); if (faidhle_làmhrachan < 0) return (uint32_t)faidhle_làmhrachan;
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호);
    첫째값.ADDRESS = 0;
    intptr_t cor_VALUE = 호출(33, faidhle_làmhrachan, (inneal_Word)&첫째값, sizeof(첫째값));
    if (cor_VALUE < 0) { inneal_dùin(faidhle_làmhrachan); return (uint32_t)cor_VALUE; }
    return faidhle_làmhrachan;
}
inneal_Word inneal_UDP_cuir(inneal_Word faidhle_làmhrachan, inneal_Word 접속번호, inneal_Word ARRAY_VALUE, inneal_Word faid_VALUE) {
    const inneal_Word *원본주소 = (const inneal_Word *)ARRAY_VALUE; unsigned char dàta[512];
    if (faid_VALUE > 512 || faid_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (inneal_Word 순번 = 0; 순번 < faid_VALUE; 순번++) dàta[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호);
    return (uint32_t)사용자호출(34, faidhle_làmhrachan, (inneal_Word)dàta, faid_VALUE, 0, (inneal_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t nì_COUNT) { return (nì_COUNT>>24)|((nì_COUNT>>8)&0xff00)|((nì_COUNT<<8)&0xff0000)|(nì_COUNT<<24); }
inneal_Word inneal_UDP_cuir_ADDRESS(inneal_Word faidhle_làmhrachan, inneal_Word ADDRESS, inneal_Word 접속번호, inneal_Word ARRAY_VALUE, inneal_Word faid_VALUE) {
    const inneal_Word *원본주소 = (const inneal_Word *)ARRAY_VALUE; unsigned char dàta[512];
    if (faid_VALUE > 512 || faid_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (inneal_Word 순번 = 0; 순번 < faid_VALUE; 순번++) dàta[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, faidhle_làmhrachan, (inneal_Word)dàta, faid_VALUE, 0, (inneal_Word)&첫째값, sizeof(첫째값));
}
inneal_Word inneal_CONNECT(inneal_Word faidhle_làmhrachan, inneal_Word ADDRESS, inneal_Word 접속번호) {
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t ruith = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t tomhas = 호출(37, faidhle_làmhrachan, (inneal_Word)&첫째값, sizeof(첫째값));
        if (tomhas != -115) return (uint32_t)tomhas;
        if ((uint32_t)(호출(7, 0, 0, 0) - ruith) >= 1000) return (uint32_t)-110;
    }
}
inneal_Word 도구전문받기(inneal_Word faidhle_làmhrachan, inneal_Word ARRAY_VALUE, inneal_Word 수용량) {
    inneal_Word *ceann_uidhe_ADDRESS = (inneal_Word *)ARRAY_VALUE; unsigned char dàta[512];
    if (수용량 > 512 || ceann_uidhe_ADDRESS[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned faid_dàta = sizeof(첫째값);
    intptr_t nì_COUNT = 사용자호출(35, faidhle_làmhrachan, (inneal_Word)dàta, 수용량, 0, (inneal_Word)&첫째값, (inneal_Word)&faid_dàta);
    if (nì_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < nì_COUNT; 순번++) ceann_uidhe_ADDRESS[순번 + 1] = dàta[순번]; ceann_uidhe_ADDRESS[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; ceann_uidhe_ADDRESS[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)nì_COUNT;
}
inneal_Word inneal_UDP_port(inneal_Word faidhle_làmhrachan) {
    struct 자바주소 첫째값; unsigned faid_dàta = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, faidhle_làmhrachan, (inneal_Word)&첫째값, (inneal_Word)&faid_dàta);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
inneal_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
inneal_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
inneal_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
inneal_Word inneal_grafaigean_fuirich(void) { return (uint32_t)화면키기다리기(); }
inneal_Word 도구사각형(inneal_Word co_chomharra_x, inneal_Word 세로좌표, inneal_Word 너비값, inneal_Word 높이값, inneal_Word 색상) {
    return (uint32_t)사용자호출(13, co_chomharra_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

inneal_Word inneal_sruth(inneal_Word Gnìomh,inneal_Word faidhle_làmhrachan,inneal_Word VALUE){
    if(Gnìomh==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADDRESS(VALUE);
    if(Gnìomh==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,faidhle_làmhrachan,(inneal_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,faidhle_làmhrachan,4,0));}
    if(Gnìomh==2)return (uint32_t)호출(37,faidhle_làmhrachan,(inneal_Word)&첫째값,sizeof(첫째값));
    if(Gnìomh==3)return (uint32_t)호출(39,faidhle_làmhrachan,0,0);
    if(Gnìomh==4)return inneal_UDP_port(faidhle_làmhrachan);
    if(Gnìomh==5)return (uint32_t)호출(40,faidhle_làmhrachan,0,0);
    return (uint32_t)-22;
}
inneal_Word inneal_GUI(inneal_Word Gnìomh,inneal_Word aithnichear_VALUE,inneal_Word 첫째값,inneal_Word SECOND_VALUE,inneal_Word còd_a_charactair,inneal_Word ceann_uidhe_dàta){return (uint32_t)사용자호출(20,Gnìomh,aithnichear_VALUE,첫째값,SECOND_VALUE,còd_a_charactair,ceann_uidhe_dàta);}
inneal_Word inneal_GUI_SMS(inneal_Word aithnichear_VALUE,inneal_Word ARRAY_VALUE,inneal_Word nì_COUNT){
    const inneal_Word *원본주소=(const inneal_Word *)ARRAY_VALUE;uint32_t dàta[127];unsigned cur_a_steach_COUNT=0;
    if(nì_COUNT>원본주소[0])return (uint32_t)-22;
    for(inneal_Word 순번=0;순번<nì_COUNT;순번++){unsigned caractar_còdachadh=원본주소[순번+1];if(caractar_còdachadh>=0xd800&&caractar_còdachadh<=0xdbff&&순번+1<nì_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;caractar_còdachadh=0x10000+((caractar_còdachadh-0xd800)<<10)+낮은값-0xdc00;}if(cur_a_steach_COUNT==127)return (uint32_t)-22;dàta[cur_a_steach_COUNT++]=caractar_còdachadh;}
    return (uint32_t)사용자호출(21,aithnichear_VALUE,(inneal_Word)dàta,cur_a_steach_COUNT,0,0,0);
}
