#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fail/Väljund/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "kogum.h"
typedef uintptr_t arvuti_Word;
static int ala_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static arvuti_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned kaup_COUNT, arvuti_Word 첫째값, arvuti_Word SECOND_VALUE, arvuti_Word koodipunkt) {
    return 사용자호출(kaup_COUNT, 첫째값, SECOND_VALUE, koodipunkt, 0, 0, 0);
}
static void 바이트들(const char *andmed_ametikoht, size_t kaup_COUNT) { 호출(1, 1, (arvuti_Word)andmed_ametikoht, kaup_COUNT); }
static void märk(unsigned koodipunkt) {
    unsigned char andmed[4]; unsigned kaup_COUNT = 0;
    if (koodipunkt < 128) andmed[kaup_COUNT++] = koodipunkt;
    else if (koodipunkt < 2048) { andmed[kaup_COUNT++] = 0xc0 | (koodipunkt >> 6); andmed[kaup_COUNT++] = 0x80 | (koodipunkt & 63); }
    else if (koodipunkt < 65536) { andmed[kaup_COUNT++] = 0xe0 | (koodipunkt >> 12); andmed[kaup_COUNT++] = 0x80 | ((koodipunkt >> 6) & 63); andmed[kaup_COUNT++] = 0x80 | (koodipunkt & 63); }
    else { andmed[kaup_COUNT++] = 0xf0 | (koodipunkt >> 18); andmed[kaup_COUNT++] = 0x80 | ((koodipunkt >> 12) & 63); andmed[kaup_COUNT++] = 0x80 | ((koodipunkt >> 6) & 63); andmed[kaup_COUNT++] = 0x80 | (koodipunkt & 63); }
    바이트들((const char *)andmed, kaup_COUNT);
}
arvuti_Word tööriist_märk(arvuti_Word VALUE) {
    unsigned koodipunkt = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (koodipunkt >= 0xdc00 && koodipunkt <= 0xdfff) { märk(0x10000 + ((높은부분 - 0xd800) << 10) + koodipunkt - 0xdc00); return 1; }
        märk(0xfffd);
    }
    if (koodipunkt >= 0xd800 && koodipunkt <= 0xdbff) 대기중짝글자 = koodipunkt;
    else märk(koodipunkt > 0x10ffff || (koodipunkt >= 0xdc00 && koodipunkt <= 0xdfff) ? 0xfffd : koodipunkt);
    return 1;
}
arvuti_Word tööriist_printima(arvuti_Word VALUE) {
    const arvuti_Word *string_andmed = (const arvuti_Word *)VALUE;
    for (arvuti_Word 순번 = 0; 순번 < string_andmed[0]; 순번++) tööriist_märk(string_andmed[순번 + 1]);
    return string_andmed[0];
}
static int RADA(arvuti_Word objekt_viide, char näitaja_andmed[512]) {
    const arvuti_Word *첫째값 = (const arvuti_Word *)objekt_viide;
    unsigned 사용량 = 0;
    for (arvuti_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned koodipunkt = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] meetod_MODE 경로와 호환한다.
        if (koodipunkt >= 0xd800 && koodipunkt <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; koodipunkt = 0x10000 + ((koodipunkt - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (koodipunkt >= 0xd800 && koodipunkt <= 0xdfff) return -22;
        unsigned kaup_COUNT = koodipunkt < 128 ? 1 : koodipunkt < 2048 ? 2 : koodipunkt < 65536 ? 3 : 4;
        if (사용량 + kaup_COUNT > 511) return -36;
        if (kaup_COUNT == 1) näitaja_andmed[사용량++] = koodipunkt;
        else {
            näitaja_andmed[사용량++] = (kaup_COUNT == 2 ? 0xc0 : kaup_COUNT == 3 ? 0xe0 : 0xf0) | (koodipunkt >> (6 * (kaup_COUNT - 1)));
            for (unsigned 안쪽순번 = kaup_COUNT - 1; 안쪽순번; 안쪽순번--) näitaja_andmed[사용량++] = 0x80 | ((koodipunkt >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    näitaja_andmed[사용량] = 0; return 사용량 ? 0 : -22;
}
arvuti_Word tööriist_avama(arvuti_Word Nimi_2, arvuti_Word konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus) {
    char andmed_ametikoht[512]; int VIGA = RADA(Nimi_2, andmed_ametikoht);
    return (uint32_t)(VIGA ? VIGA : 호출(3, (arvuti_Word)andmed_ametikoht, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, 0));
}
arvuti_Word tööriist_Sule(arvuti_Word Fail_pide) { return (uint32_t)호출(4, Fail_pide, 0, 0); }
arvuti_Word 도구바이트읽기(arvuti_Word Fail_pide) {
    unsigned char SECOND_VALUE; intptr_t kaup_COUNT = 호출(2, Fail_pide, (arvuti_Word)&SECOND_VALUE, 1);
    return (uint32_t)(kaup_COUNT == 1 ? SECOND_VALUE : kaup_COUNT == 0 ? 256 : kaup_COUNT);
}
arvuti_Word tööriist_kirjutamine_bait(arvuti_Word Fail_pide, arvuti_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Fail_pide, (arvuti_Word)&SECOND_VALUE, 1);
}
arvuti_Word 도구읽기(arvuti_Word Nimi_2, arvuti_Word sihtkoht_andmed_ADDRESS) {
    if (꾸러미사용중) {
        char andmed_ametikoht[512]; int VIGA = RADA(Nimi_2, andmed_ametikoht); if (VIGA) return (uint32_t)VIGA;
        unsigned kaup_COUNT = 0; while (andmed_ametikoht[kaup_COUNT]) kaup_COUNT++;
        if (kaup_COUNT >= 6) for (unsigned 순번 = 0; 순번 < kaup_COUNT - 6; 순번++) if (andmed_ametikoht[순번] == '.') andmed_ametikoht[순번] = '/';
        unsigned char 바이트들[16384]; arvuti_Word *sihtkoht_VALUE_ametikoht = (arvuti_Word *)sihtkoht_andmed_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(andmed_ametikoht, 바이트들, sihtkoht_VALUE_ametikoht[0] < sizeof(바이트들) ? sihtkoht_VALUE_ametikoht[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) sihtkoht_VALUE_ametikoht[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Fail_pide = 꾸러미사용중 ? -2 : (int32_t)tööriist_avama(Nimi_2, 0);
    if (Fail_pide < 0) {
        char andmed_ametikoht[512]; int VIGA = RADA(Nimi_2, andmed_ametikoht); if (VIGA) return (uint32_t)VIGA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Edasi_nihe = 자바클래스들[순번].Nimi_2; unsigned 안쪽순번 = 0;
            while (andmed_ametikoht[안쪽순번] && andmed_ametikoht[안쪽순번] == Edasi_nihe[안쪽순번]) 안쪽순번++;
            if (andmed_ametikoht[안쪽순번] || Edasi_nihe[안쪽순번]) continue;
            arvuti_Word *sihtkoht_VALUE_ametikoht = (arvuti_Word *)sihtkoht_andmed_ADDRESS;
            if (sihtkoht_VALUE_ametikoht[0] < 자바클래스들[순번].Suurus) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Suurus; 안쪽순번++) sihtkoht_VALUE_ametikoht[안쪽순번 + 1] = 자바클래스들[순번].andmed[안쪽순번];
            return 자바클래스들[순번].Suurus;
        }
        return (uint32_t)Fail_pide;
    }
    arvuti_Word *첫째값 = (arvuti_Word *)sihtkoht_andmed_ADDRESS;
    intptr_t Suurus = 호출(9, Fail_pide, 0, 0), Lõpetatud_kogus = 0;
    if (Suurus < 0 || (arvuti_Word)Suurus > 첫째값[0]) { tööriist_Sule(Fail_pide); return (uint32_t)(Suurus < 0 ? Suurus : -27); }
    unsigned char andmeplokk[256];
    while (Lõpetatud_kogus < Suurus) {
        intptr_t kaup_COUNT = 호출(2, Fail_pide, (arvuti_Word)andmeplokk, Suurus - Lõpetatud_kogus < 256 ? Suurus - Lõpetatud_kogus : 256);
        if (kaup_COUNT <= 0) { tööriist_Sule(Fail_pide); return (uint32_t)(kaup_COUNT ? kaup_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < kaup_COUNT; 순번++) 첫째값[1 + Lõpetatud_kogus + 순번] = andmeplokk[순번];
        Lõpetatud_kogus += kaup_COUNT;
    }
    tööriist_Sule(Fail_pide); return Lõpetatud_kogus;
}
arvuti_Word tööriist_kirjutamine(arvuti_Word Nimi_2, arvuti_Word 원본자료, arvuti_Word kirje_COUNT) {
    const arvuti_Word *첫째값 = (const arvuti_Word *)원본자료;
    if (kirje_COUNT > 첫째값[0] || kirje_COUNT > 16384) return (uint32_t)-27;
    int Fail_pide = (int32_t)tööriist_avama(Nimi_2, 577); if (Fail_pide < 0) return (uint32_t)Fail_pide;
    unsigned char andmeplokk[256]; arvuti_Word Lõpetatud_kogus = 0;
    while (Lõpetatud_kogus < kirje_COUNT) {
        arvuti_Word kaup_COUNT = kirje_COUNT - Lõpetatud_kogus < 256 ? kirje_COUNT - Lõpetatud_kogus : 256;
        for (arvuti_Word 순번 = 0; 순번 < kaup_COUNT; 순번++) andmeplokk[순번] = 첫째값[1 + Lõpetatud_kogus + 순번];
        intptr_t TULEMUS = 호출(1, Fail_pide, (arvuti_Word)andmeplokk, kaup_COUNT);
        if (TULEMUS <= 0) { tööriist_Sule(Fail_pide); return (uint32_t)(TULEMUS ? TULEMUS : -5); }
        Lõpetatud_kogus += TULEMUS;
    }
    tööriist_Sule(Fail_pide); return kirje_COUNT;
}
arvuti_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
arvuti_Word tööriist_argument(arvuti_Word LOOKUP_INDEX) {
    static const arvuti_Word 빈값[1] = {0};
    if (LOOKUP_INDEX >= 8) return (arvuti_Word)빈값;
    unsigned char 입력결과[256]; intptr_t kaup_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *andmed_ametikoht = 꾸러미진입클래스(); kaup_COUNT = 0; while (andmed_ametikoht[kaup_COUNT] && kaup_COUNT < 255) { 입력결과[kaup_COUNT] = andmed_ametikoht[kaup_COUNT]; kaup_COUNT++; } }
    else kaup_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (arvuti_Word)입력결과, sizeof(입력결과));
    if (kaup_COUNT < 0) return (arvuti_Word)빈값;
    arvuti_Word *näitaja_andmed = 전달인수[LOOKUP_INDEX]; unsigned kirje_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < kaup_COUNT;) {
        unsigned koodipunkt = 입력결과[순번++], 더있음 = koodipunkt < 128 ? 0 : koodipunkt >= 0xc2 && koodipunkt < 0xe0 ? 1 : koodipunkt < 0xf0 && koodipunkt >= 0xe0 ? 2 : koodipunkt >= 0xf0 && koodipunkt <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > kaup_COUNT) { näitaja_andmed[++kirje_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) koodipunkt &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { koodipunkt = (koodipunkt << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || koodipunkt < 최소값 || koodipunkt > 0x10ffff || (koodipunkt >= 0xd800 && koodipunkt <= 0xdfff)) koodipunkt = 0xfffd;
        if (koodipunkt >= 65536) { koodipunkt -= 65536; näitaja_andmed[++kirje_COUNT] = 0xd800 | (koodipunkt >> 10); näitaja_andmed[++kirje_COUNT] = 0xdc00 | (koodipunkt & 1023); }
        else näitaja_andmed[++kirje_COUNT] = koodipunkt;
    }
    näitaja_andmed[0] = kirje_COUNT; return (arvuti_Word)näitaja_andmed;
}
arvuti_Word 도구분류(void) { return ala_VALUE; }
void 커널중단(const char *teatamine_SMS) {
    const char *andmed_ametikoht = teatamine_SMS; while (*andmed_ametikoht) andmed_ametikoht++;
    바이트들("Java tool runtime error: ", 25); 바이트들(teatamine_SMS, andmed_ametikoht - teatamine_SMS); märk(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_kasutaja_programm(int meetod_MODE) {
    ala_VALUE = meetod_MODE;
    unsigned char 첫항목[256]; intptr_t kaup_COUNT = 호출(15, 0, (arvuti_Word)첫항목, sizeof(첫항목));
    if (meetod_MODE == 2 || (meetod_MODE == 1 && kaup_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = meetod_MODE == 2 ? 0 : 1;
        char Fail_kirje_nimetus[256]; intptr_t 길이값 = 호출(15, 꾸러미인수이동, (arvuti_Word)Fail_kirje_nimetus, sizeof(Fail_kirje_nimetus));
        if (길이값 <= 0 || 꾸러미열기(Fail_kirje_nimetus) < 0) {
            static const char VIGA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(VIGA, sizeof(VIGA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int TULEMUS = 자바진입();
    if (대기중짝글자) märk(0xfffd);
    return TULEMUS;
}

// UDP는 oma 커널의 SVC를 통과하며 tähtaja_piires_kaup 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Pere, pordinumber; uint32_t ADDRESS; unsigned char null_VALUE[8]; };
static struct 자바주소 UDP_ADDRESS(unsigned pordinumber) {
    struct 자바주소 첫째값 = {2, (uint16_t)((pordinumber << 8) | (pordinumber >> 8)), 0x0100007f, {0}}; return 첫째값;
}
arvuti_Word tööriist_UDP_avama(arvuti_Word pordinumber) {
    intptr_t Fail_pide = 호출(32, 2, 2, 17); if (Fail_pide < 0) return (uint32_t)Fail_pide;
    struct 자바주소 첫째값 = UDP_ADDRESS(pordinumber);
    첫째값.ADDRESS = 0;
    intptr_t Olek_VALUE = 호출(33, Fail_pide, (arvuti_Word)&첫째값, sizeof(첫째값));
    if (Olek_VALUE < 0) { tööriist_Sule(Fail_pide); return (uint32_t)Olek_VALUE; }
    return Fail_pide;
}
arvuti_Word tööriist_UDP_saatma(arvuti_Word Fail_pide, arvuti_Word pordinumber, arvuti_Word ARRAY_VALUE, arvuti_Word 길이) {
    const arvuti_Word *원본주소 = (const arvuti_Word *)ARRAY_VALUE; unsigned char andmed[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (arvuti_Word 순번 = 0; 순번 < 길이; 순번++) andmed[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(pordinumber);
    return (uint32_t)사용자호출(34, Fail_pide, (arvuti_Word)andmed, 길이, 0, (arvuti_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t kaup_COUNT) { return (kaup_COUNT>>24)|((kaup_COUNT>>8)&0xff00)|((kaup_COUNT<<8)&0xff0000)|(kaup_COUNT<<24); }
arvuti_Word tööriist_UDP_saatma_ADDRESS(arvuti_Word Fail_pide, arvuti_Word ADDRESS, arvuti_Word pordinumber, arvuti_Word ARRAY_VALUE, arvuti_Word 길이) {
    const arvuti_Word *원본주소 = (const arvuti_Word *)ARRAY_VALUE; unsigned char andmed[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (arvuti_Word 순번 = 0; 순번 < 길이; 순번++) andmed[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(pordinumber); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, Fail_pide, (arvuti_Word)andmed, 길이, 0, (arvuti_Word)&첫째값, sizeof(첫째값));
}
arvuti_Word tööriist_Ühenda(arvuti_Word Fail_pide, arvuti_Word ADDRESS, arvuti_Word pordinumber) {
    struct 자바주소 첫째값 = UDP_ADDRESS(pordinumber); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t Käivita_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t TULEMUS = 호출(37, Fail_pide, (arvuti_Word)&첫째값, sizeof(첫째값));
        if (TULEMUS != -115) return (uint32_t)TULEMUS;
        if ((uint32_t)(호출(7, 0, 0, 0) - Käivita_2) >= 1000) return (uint32_t)-110;
    }
}
arvuti_Word 도구전문받기(arvuti_Word Fail_pide, arvuti_Word ARRAY_VALUE, arvuti_Word puhver_võimsus) {
    arvuti_Word *sihtkoht_ADDRESS = (arvuti_Word *)ARRAY_VALUE; unsigned char andmed[512];
    if (puhver_võimsus > 512 || sihtkoht_ADDRESS[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t kaup_COUNT = 사용자호출(35, Fail_pide, (arvuti_Word)andmed, puhver_võimsus, 0, (arvuti_Word)&첫째값, (arvuti_Word)&길이값);
    if (kaup_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < kaup_COUNT; 순번++) sihtkoht_ADDRESS[순번 + 1] = andmed[순번]; sihtkoht_ADDRESS[513] = (첫째값.pordinumber << 8 | 첫째값.pordinumber >> 8) & 65535; sihtkoht_ADDRESS[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)kaup_COUNT;
}
arvuti_Word tööriist_UDP_port(arvuti_Word Fail_pide) {
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Fail_pide, (arvuti_Word)&첫째값, (arvuti_Word)&길이값);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.pordinumber << 8 | 첫째값.pordinumber >> 8) & 65535);
}
arvuti_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
arvuti_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
arvuti_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
arvuti_Word tööriist_graafika_Oota(void) { return (uint32_t)화면키기다리기(); }
arvuti_Word tööriist_ristkülik(arvuti_Word 가로좌표, arvuti_Word 세로좌표, arvuti_Word 너비값, arvuti_Word 높이값, arvuti_Word 색상) {
    return (uint32_t)사용자호출(13, 가로좌표, 세로좌표, 색상, 너비값, 높이값, 0);
}

arvuti_Word tööriist_voog(arvuti_Word Nimi,arvuti_Word Fail_pide,arvuti_Word VALUE){
    if(Nimi==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADDRESS(VALUE);
    if(Nimi==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,Fail_pide,(arvuti_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Fail_pide,4,0));}
    if(Nimi==2)return (uint32_t)호출(37,Fail_pide,(arvuti_Word)&첫째값,sizeof(첫째값));
    if(Nimi==3)return (uint32_t)호출(39,Fail_pide,0,0);
    if(Nimi==4)return tööriist_UDP_port(Fail_pide);
    if(Nimi==5)return (uint32_t)호출(40,Fail_pide,0,0);
    return (uint32_t)-22;
}
arvuti_Word tööriist_GUI(arvuti_Word Nimi,arvuti_Word identifikaator_VALUE,arvuti_Word 첫째값,arvuti_Word SECOND_VALUE,arvuti_Word koodipunkt,arvuti_Word sihtkoht_andmed){return (uint32_t)사용자호출(20,Nimi,identifikaator_VALUE,첫째값,SECOND_VALUE,koodipunkt,sihtkoht_andmed);}
arvuti_Word tööriist_GUI_SMS(arvuti_Word identifikaator_VALUE,arvuti_Word ARRAY_VALUE,arvuti_Word kaup_COUNT){
    const arvuti_Word *원본주소=(const arvuti_Word *)ARRAY_VALUE;uint32_t andmed[127];unsigned kirje_COUNT=0;
    if(kaup_COUNT>원본주소[0])return (uint32_t)-22;
    for(arvuti_Word 순번=0;순번<kaup_COUNT;순번++){unsigned märk_kodeerimine=원본주소[순번+1];if(märk_kodeerimine>=0xd800&&märk_kodeerimine<=0xdbff&&순번+1<kaup_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;märk_kodeerimine=0x10000+((märk_kodeerimine-0xd800)<<10)+낮은값-0xdc00;}if(kirje_COUNT==127)return (uint32_t)-22;andmed[kirje_COUNT++]=märk_kodeerimine;}
    return (uint32_t)사용자호출(21,identifikaator_VALUE,(arvuti_Word)andmed,kirje_COUNT,0,0,0);
}
