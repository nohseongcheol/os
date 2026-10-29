#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fails/Izvade/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "saistīt.h"
typedef uintptr_t mašīna_Word;
static int joma_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static mašīna_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned krājums_COUNT, mašīna_Word 첫째값, mašīna_Word SECOND_VALUE, mašīna_Word koda_punkts) {
    return 사용자호출(krājums_COUNT, 첫째값, SECOND_VALUE, koda_punkts, 0, 0, 0);
}
static void 바이트들(const char *dati_amats, size_t krājums_COUNT) { 호출(1, 1, (mašīna_Word)dati_amats, krājums_COUNT); }
static void rakstzīme(unsigned koda_punkts) {
    unsigned char dati[4]; unsigned krājums_COUNT = 0;
    if (koda_punkts < 128) dati[krājums_COUNT++] = koda_punkts;
    else if (koda_punkts < 2048) { dati[krājums_COUNT++] = 0xc0 | (koda_punkts >> 6); dati[krājums_COUNT++] = 0x80 | (koda_punkts & 63); }
    else if (koda_punkts < 65536) { dati[krājums_COUNT++] = 0xe0 | (koda_punkts >> 12); dati[krājums_COUNT++] = 0x80 | ((koda_punkts >> 6) & 63); dati[krājums_COUNT++] = 0x80 | (koda_punkts & 63); }
    else { dati[krājums_COUNT++] = 0xf0 | (koda_punkts >> 18); dati[krājums_COUNT++] = 0x80 | ((koda_punkts >> 12) & 63); dati[krājums_COUNT++] = 0x80 | ((koda_punkts >> 6) & 63); dati[krājums_COUNT++] = 0x80 | (koda_punkts & 63); }
    바이트들((const char *)dati, krājums_COUNT);
}
mašīna_Word rīks_rakstzīme(mašīna_Word VALUE) {
    unsigned koda_punkts = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (koda_punkts >= 0xdc00 && koda_punkts <= 0xdfff) { rakstzīme(0x10000 + ((높은부분 - 0xd800) << 10) + koda_punkts - 0xdc00); return 1; }
        rakstzīme(0xfffd);
    }
    if (koda_punkts >= 0xd800 && koda_punkts <= 0xdbff) 대기중짝글자 = koda_punkts;
    else rakstzīme(koda_punkts > 0x10ffff || (koda_punkts >= 0xdc00 && koda_punkts <= 0xdfff) ? 0xfffd : koda_punkts);
    return 1;
}
mašīna_Word 도구출력(mašīna_Word VALUE) {
    const mašīna_Word *virkne_dati = (const mašīna_Word *)VALUE;
    for (mašīna_Word 순번 = 0; 순번 < virkne_dati[0]; 순번++) rīks_rakstzīme(virkne_dati[순번 + 1]);
    return virkne_dati[0];
}
static int CEĻŠ(mašīna_Word objekts_Uzziņas, char mērs_dati[512]) {
    const mašīna_Word *첫째값 = (const mašīna_Word *)objekts_Uzziņas;
    unsigned 사용량 = 0;
    for (mašīna_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned koda_punkts = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metode_MODE 경로와 호환한다.
        if (koda_punkts >= 0xd800 && koda_punkts <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; koda_punkts = 0x10000 + ((koda_punkts - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (koda_punkts >= 0xd800 && koda_punkts <= 0xdfff) return -22;
        unsigned krājums_COUNT = koda_punkts < 128 ? 1 : koda_punkts < 2048 ? 2 : koda_punkts < 65536 ? 3 : 4;
        if (사용량 + krājums_COUNT > 511) return -36;
        if (krājums_COUNT == 1) mērs_dati[사용량++] = koda_punkts;
        else {
            mērs_dati[사용량++] = (krājums_COUNT == 2 ? 0xc0 : krājums_COUNT == 3 ? 0xe0 : 0xf0) | (koda_punkts >> (6 * (krājums_COUNT - 1)));
            for (unsigned 안쪽순번 = krājums_COUNT - 1; 안쪽순번; 안쪽순번--) mērs_dati[사용량++] = 0x80 | ((koda_punkts >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    mērs_dati[사용량] = 0; return 사용량 ? 0 : -22;
}
mašīna_Word rīks_atvērt(mašīna_Word Nosaukums, mašīna_Word konfigurācija_Background_Intelligent_Transfer_Service) {
    char dati_amats[512]; int Kļūda = CEĻŠ(Nosaukums, dati_amats);
    return (uint32_t)(Kļūda ? Kļūda : 호출(3, (mašīna_Word)dati_amats, konfigurācija_Background_Intelligent_Transfer_Service, 0));
}
mašīna_Word rīks_Aizvērt(mašīna_Word Fails_turis) { return (uint32_t)호출(4, Fails_turis, 0, 0); }
mašīna_Word 도구바이트읽기(mašīna_Word Fails_turis) {
    unsigned char SECOND_VALUE; intptr_t krājums_COUNT = 호출(2, Fails_turis, (mašīna_Word)&SECOND_VALUE, 1);
    return (uint32_t)(krājums_COUNT == 1 ? SECOND_VALUE : krājums_COUNT == 0 ? 256 : krājums_COUNT);
}
mašīna_Word rīks_rakstīšana_byte(mašīna_Word Fails_turis, mašīna_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Fails_turis, (mašīna_Word)&SECOND_VALUE, 1);
}
mašīna_Word 도구읽기(mašīna_Word Nosaukums, mašīna_Word mērķis_dati_adrese) {
    if (꾸러미사용중) {
        char dati_amats[512]; int Kļūda = CEĻŠ(Nosaukums, dati_amats); if (Kļūda) return (uint32_t)Kļūda;
        unsigned krājums_COUNT = 0; while (dati_amats[krājums_COUNT]) krājums_COUNT++;
        if (krājums_COUNT >= 6) for (unsigned 순번 = 0; 순번 < krājums_COUNT - 6; 순번++) if (dati_amats[순번] == '.') dati_amats[순번] = '/';
        unsigned char 바이트들[16384]; mašīna_Word *mērķis_VALUE_amats = (mašīna_Word *)mērķis_dati_adrese;
        int RECEIVED_COUNT = 꾸러미읽기(dati_amats, 바이트들, mērķis_VALUE_amats[0] < sizeof(바이트들) ? mērķis_VALUE_amats[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) mērķis_VALUE_amats[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Fails_turis = 꾸러미사용중 ? -2 : (int32_t)rīks_atvērt(Nosaukums, 0);
    if (Fails_turis < 0) {
        char dati_amats[512]; int Kļūda = CEĻŠ(Nosaukums, dati_amats); if (Kļūda) return (uint32_t)Kļūda;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Tālāk_Nobīde = 자바클래스들[순번].Nosaukums; unsigned 안쪽순번 = 0;
            while (dati_amats[안쪽순번] && dati_amats[안쪽순번] == Tālāk_Nobīde[안쪽순번]) 안쪽순번++;
            if (dati_amats[안쪽순번] || Tālāk_Nobīde[안쪽순번]) continue;
            mašīna_Word *mērķis_VALUE_amats = (mašīna_Word *)mērķis_dati_adrese;
            if (mērķis_VALUE_amats[0] < 자바클래스들[순번].Izmērs) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Izmērs; 안쪽순번++) mērķis_VALUE_amats[안쪽순번 + 1] = 자바클래스들[순번].dati[안쪽순번];
            return 자바클래스들[순번].Izmērs;
        }
        return (uint32_t)Fails_turis;
    }
    mašīna_Word *첫째값 = (mašīna_Word *)mērķis_dati_adrese;
    intptr_t Izmērs = 호출(9, Fails_turis, 0, 0), Pabeigti_summa = 0;
    if (Izmērs < 0 || (mašīna_Word)Izmērs > 첫째값[0]) { rīks_Aizvērt(Fails_turis); return (uint32_t)(Izmērs < 0 ? Izmērs : -27); }
    unsigned char datu_bloks[256];
    while (Pabeigti_summa < Izmērs) {
        intptr_t krājums_COUNT = 호출(2, Fails_turis, (mašīna_Word)datu_bloks, Izmērs - Pabeigti_summa < 256 ? Izmērs - Pabeigti_summa : 256);
        if (krājums_COUNT <= 0) { rīks_Aizvērt(Fails_turis); return (uint32_t)(krājums_COUNT ? krājums_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < krājums_COUNT; 순번++) 첫째값[1 + Pabeigti_summa + 순번] = datu_bloks[순번];
        Pabeigti_summa += krājums_COUNT;
    }
    rīks_Aizvērt(Fails_turis); return Pabeigti_summa;
}
mašīna_Word rīks_rakstīšana(mašīna_Word Nosaukums, mašīna_Word 원본자료, mašīna_Word ievade_COUNT) {
    const mašīna_Word *첫째값 = (const mašīna_Word *)원본자료;
    if (ievade_COUNT > 첫째값[0] || ievade_COUNT > 16384) return (uint32_t)-27;
    int Fails_turis = (int32_t)rīks_atvērt(Nosaukums, 577); if (Fails_turis < 0) return (uint32_t)Fails_turis;
    unsigned char datu_bloks[256]; mašīna_Word Pabeigti_summa = 0;
    while (Pabeigti_summa < ievade_COUNT) {
        mašīna_Word krājums_COUNT = ievade_COUNT - Pabeigti_summa < 256 ? ievade_COUNT - Pabeigti_summa : 256;
        for (mašīna_Word 순번 = 0; 순번 < krājums_COUNT; 순번++) datu_bloks[순번] = 첫째값[1 + Pabeigti_summa + 순번];
        intptr_t mērs = 호출(1, Fails_turis, (mašīna_Word)datu_bloks, krājums_COUNT);
        if (mērs <= 0) { rīks_Aizvērt(Fails_turis); return (uint32_t)(mērs ? mērs : -5); }
        Pabeigti_summa += mērs;
    }
    rīks_Aizvērt(Fails_turis); return ievade_COUNT;
}
mašīna_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mašīna_Word rīks_arg(mašīna_Word LOOKUP_INDEX) {
    static const mašīna_Word 빈값[1] = {0};
    if (LOOKUP_INDEX >= 8) return (mašīna_Word)빈값;
    unsigned char 입력결과[256]; intptr_t krājums_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *dati_amats = 꾸러미진입클래스(); krājums_COUNT = 0; while (dati_amats[krājums_COUNT] && krājums_COUNT < 255) { 입력결과[krājums_COUNT] = dati_amats[krājums_COUNT]; krājums_COUNT++; } }
    else krājums_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mašīna_Word)입력결과, sizeof(입력결과));
    if (krājums_COUNT < 0) return (mašīna_Word)빈값;
    mašīna_Word *mērs_dati = 전달인수[LOOKUP_INDEX]; unsigned ievade_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < krājums_COUNT;) {
        unsigned koda_punkts = 입력결과[순번++], 더있음 = koda_punkts < 128 ? 0 : koda_punkts >= 0xc2 && koda_punkts < 0xe0 ? 1 : koda_punkts < 0xf0 && koda_punkts >= 0xe0 ? 2 : koda_punkts >= 0xf0 && koda_punkts <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > krājums_COUNT) { mērs_dati[++ievade_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) koda_punkts &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { koda_punkts = (koda_punkts << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || koda_punkts < 최소값 || koda_punkts > 0x10ffff || (koda_punkts >= 0xd800 && koda_punkts <= 0xdfff)) koda_punkts = 0xfffd;
        if (koda_punkts >= 65536) { koda_punkts -= 65536; mērs_dati[++ievade_COUNT] = 0xd800 | (koda_punkts >> 10); mērs_dati[++ievade_COUNT] = 0xdc00 | (koda_punkts & 1023); }
        else mērs_dati[++ievade_COUNT] = koda_punkts;
    }
    mērs_dati[0] = ievade_COUNT; return (mašīna_Word)mērs_dati;
}
mašīna_Word 도구분류(void) { return joma_VALUE; }
void 커널중단(const char *informēšana_SMS) {
    const char *dati_amats = informēšana_SMS; while (*dati_amats) dati_amats++;
    바이트들("Java tool runtime error: ", 25); 바이트들(informēšana_SMS, dati_amats - informēšana_SMS); rakstzīme(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Sākt_lietotājs_programma(int metode_MODE) {
    joma_VALUE = metode_MODE;
    unsigned char 첫항목[256]; intptr_t krājums_COUNT = 호출(15, 0, (mašīna_Word)첫항목, sizeof(첫항목));
    if (metode_MODE == 2 || (metode_MODE == 1 && krājums_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metode_MODE == 2 ? 0 : 1;
        char Fails_ievade_nosaukums[256]; intptr_t 길이값 = 호출(15, 꾸러미인수이동, (mašīna_Word)Fails_ievade_nosaukums, sizeof(Fails_ievade_nosaukums));
        if (길이값 <= 0 || 꾸러미열기(Fails_ievade_nosaukums) < 0) {
            static const char Kļūda[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Kļūda, sizeof(Kļūda) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int mērs = 자바진입();
    if (대기중짝글자) rakstzīme(0xfffd);
    return mērs;
}

// UDP는 savs 커널의 SVC를 통과하며 pašreizējais_krājums 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t saime, porta_numurs; uint32_t adrese; unsigned char nulle_VALUE[8]; };
static struct 자바주소 UDP_adrese(unsigned porta_numurs) {
    struct 자바주소 첫째값 = {2, (uint16_t)((porta_numurs << 8) | (porta_numurs >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mašīna_Word rīks_UDP_atvērt(mašīna_Word porta_numurs) {
    intptr_t Fails_turis = 호출(32, 2, 2, 17); if (Fails_turis < 0) return (uint32_t)Fails_turis;
    struct 자바주소 첫째값 = UDP_adrese(porta_numurs);
    첫째값.adrese = 0;
    intptr_t Statuss_VALUE = 호출(33, Fails_turis, (mašīna_Word)&첫째값, sizeof(첫째값));
    if (Statuss_VALUE < 0) { rīks_Aizvērt(Fails_turis); return (uint32_t)Statuss_VALUE; }
    return Fails_turis;
}
mašīna_Word rīks_UDP_sūtīt(mašīna_Word Fails_turis, mašīna_Word porta_numurs, mašīna_Word ARRAY_VALUE, mašīna_Word 길이) {
    const mašīna_Word *원본주소 = (const mašīna_Word *)ARRAY_VALUE; unsigned char dati[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (mašīna_Word 순번 = 0; 순번 < 길이; 순번++) dati[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adrese(porta_numurs);
    return (uint32_t)사용자호출(34, Fails_turis, (mašīna_Word)dati, 길이, 0, (mašīna_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t krājums_COUNT) { return (krājums_COUNT>>24)|((krājums_COUNT>>8)&0xff00)|((krājums_COUNT<<8)&0xff0000)|(krājums_COUNT<<24); }
mašīna_Word rīks_UDP_sūtīt_adrese(mašīna_Word Fails_turis, mašīna_Word adrese, mašīna_Word porta_numurs, mašīna_Word ARRAY_VALUE, mašīna_Word 길이) {
    const mašīna_Word *원본주소 = (const mašīna_Word *)ARRAY_VALUE; unsigned char dati[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (mašīna_Word 순번 = 0; 순번 < 길이; 순번++) dati[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_adrese(porta_numurs); 첫째값.adrese = 바이트순서뒤집기(adrese);
    return (uint32_t)사용자호출(34, Fails_turis, (mašīna_Word)dati, 길이, 0, (mašīna_Word)&첫째값, sizeof(첫째값));
}
mašīna_Word rīks_saziņa(mašīna_Word Fails_turis, mašīna_Word adrese, mašīna_Word porta_numurs) {
    struct 자바주소 첫째값 = UDP_adrese(porta_numurs); 첫째값.adrese = 바이트순서뒤집기(adrese);
    uint32_t Palaist = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t mērs = 호출(37, Fails_turis, (mašīna_Word)&첫째값, sizeof(첫째값));
        if (mērs != -115) return (uint32_t)mērs;
        if ((uint32_t)(호출(7, 0, 0, 0) - Palaist) >= 1000) return (uint32_t)-110;
    }
}
mašīna_Word 도구전문받기(mašīna_Word Fails_turis, mašīna_Word ARRAY_VALUE, mašīna_Word buferis_noslodze) {
    mašīna_Word *mērķis_adrese_08bbd577 = (mašīna_Word *)ARRAY_VALUE; unsigned char dati[512];
    if (buferis_noslodze > 512 || mērķis_adrese_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t krājums_COUNT = 사용자호출(35, Fails_turis, (mašīna_Word)dati, buferis_noslodze, 0, (mašīna_Word)&첫째값, (mašīna_Word)&길이값);
    if (krājums_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < krājums_COUNT; 순번++) mērķis_adrese_08bbd577[순번 + 1] = dati[순번]; mērķis_adrese_08bbd577[513] = (첫째값.porta_numurs << 8 | 첫째값.porta_numurs >> 8) & 65535; mērķis_adrese_08bbd577[514] = 바이트순서뒤집기(첫째값.adrese); }
    return (uint32_t)krājums_COUNT;
}
mašīna_Word rīks_UDP_ports(mašīna_Word Fails_turis) {
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Fails_turis, (mašīna_Word)&첫째값, (mašīna_Word)&길이값);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.porta_numurs << 8 | 첫째값.porta_numurs >> 8) & 65535);
}
mašīna_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mašīna_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mašīna_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mašīna_Word rīks_grafika_pagaidi(void) { return (uint32_t)화면키기다리기(); }
mašīna_Word rīks_taisnstūris(mašīna_Word x_koordināta, mašīna_Word 세로좌표, mašīna_Word 너비값, mašīna_Word 높이값, mašīna_Word 색상) {
    return (uint32_t)사용자호출(13, x_koordināta, 세로좌표, 색상, 너비값, 높이값, 0);
}

mašīna_Word rīks_Stream(mašīna_Word Darbība,mašīna_Word Fails_turis,mašīna_Word VALUE){
    if(Darbība==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_adrese(VALUE);
    if(Darbība==1){첫째값.adrese=0;intptr_t 반환값=호출(33,Fails_turis,(mašīna_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Fails_turis,4,0));}
    if(Darbība==2)return (uint32_t)호출(37,Fails_turis,(mašīna_Word)&첫째값,sizeof(첫째값));
    if(Darbība==3)return (uint32_t)호출(39,Fails_turis,0,0);
    if(Darbība==4)return rīks_UDP_ports(Fails_turis);
    if(Darbība==5)return (uint32_t)호출(40,Fails_turis,0,0);
    return (uint32_t)-22;
}
mašīna_Word rīks_GUI(mašīna_Word Darbība,mašīna_Word identifikators_VALUE,mašīna_Word 첫째값,mašīna_Word SECOND_VALUE,mašīna_Word koda_punkts,mašīna_Word mērķis_dati){return (uint32_t)사용자호출(20,Darbība,identifikators_VALUE,첫째값,SECOND_VALUE,koda_punkts,mērķis_dati);}
mašīna_Word rīks_GUI_SMS(mašīna_Word identifikators_VALUE,mašīna_Word ARRAY_VALUE,mašīna_Word krājums_COUNT){
    const mašīna_Word *원본주소=(const mašīna_Word *)ARRAY_VALUE;uint32_t dati[127];unsigned ievade_COUNT=0;
    if(krājums_COUNT>원본주소[0])return (uint32_t)-22;
    for(mašīna_Word 순번=0;순번<krājums_COUNT;순번++){unsigned rakstzīmju_kodēšana=원본주소[순번+1];if(rakstzīmju_kodēšana>=0xd800&&rakstzīmju_kodēšana<=0xdbff&&순번+1<krājums_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;rakstzīmju_kodēšana=0x10000+((rakstzīmju_kodēšana-0xd800)<<10)+낮은값-0xdc00;}if(ievade_COUNT==127)return (uint32_t)-22;dati[ievade_COUNT++]=rakstzīmju_kodēšana;}
    return (uint32_t)사용자호출(21,identifikators_VALUE,(mašīna_Word)dati,ievade_COUNT,0,0,0);
}
