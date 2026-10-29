#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Failas/Išvestis/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "paketas.h"
typedef uintptr_t mašina_Word;
static int sritis_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static mašina_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned prekė_COUNT, mašina_Word 첫째값, mašina_Word SECOND_VALUE, mašina_Word simbolio_kodas) {
    return 사용자호출(prekė_COUNT, 첫째값, SECOND_VALUE, simbolio_kodas, 0, 0, 0);
}
static void 바이트들(const char *duomenys_padėtis, size_t prekė_COUNT) { 호출(1, 1, (mašina_Word)duomenys_padėtis, prekė_COUNT); }
static void simbolis_a5317f02(unsigned simbolio_kodas) {
    unsigned char duomenys[4]; unsigned prekė_COUNT = 0;
    if (simbolio_kodas < 128) duomenys[prekė_COUNT++] = simbolio_kodas;
    else if (simbolio_kodas < 2048) { duomenys[prekė_COUNT++] = 0xc0 | (simbolio_kodas >> 6); duomenys[prekė_COUNT++] = 0x80 | (simbolio_kodas & 63); }
    else if (simbolio_kodas < 65536) { duomenys[prekė_COUNT++] = 0xe0 | (simbolio_kodas >> 12); duomenys[prekė_COUNT++] = 0x80 | ((simbolio_kodas >> 6) & 63); duomenys[prekė_COUNT++] = 0x80 | (simbolio_kodas & 63); }
    else { duomenys[prekė_COUNT++] = 0xf0 | (simbolio_kodas >> 18); duomenys[prekė_COUNT++] = 0x80 | ((simbolio_kodas >> 12) & 63); duomenys[prekė_COUNT++] = 0x80 | ((simbolio_kodas >> 6) & 63); duomenys[prekė_COUNT++] = 0x80 | (simbolio_kodas & 63); }
    바이트들((const char *)duomenys, prekė_COUNT);
}
mašina_Word įrankis_simbolis(mašina_Word VALUE) {
    unsigned simbolio_kodas = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (simbolio_kodas >= 0xdc00 && simbolio_kodas <= 0xdfff) { simbolis_a5317f02(0x10000 + ((높은부분 - 0xd800) << 10) + simbolio_kodas - 0xdc00); return 1; }
        simbolis_a5317f02(0xfffd);
    }
    if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdbff) 대기중짝글자 = simbolio_kodas;
    else simbolis_a5317f02(simbolio_kodas > 0x10ffff || (simbolio_kodas >= 0xdc00 && simbolio_kodas <= 0xdfff) ? 0xfffd : simbolio_kodas);
    return 1;
}
mašina_Word 도구출력(mašina_Word VALUE) {
    const mašina_Word *eilutė_duomenys = (const mašina_Word *)VALUE;
    for (mašina_Word 순번 = 0; 순번 < eilutė_duomenys[0]; 순번++) įrankis_simbolis(eilutė_duomenys[순번 + 1]);
    return eilutė_duomenys[0];
}
static int KELIAS(mašina_Word objektas_nuoroda, char KR_duomenys[512]) {
    const mašina_Word *첫째값 = (const mašina_Word *)objektas_nuoroda;
    unsigned 사용량 = 0;
    for (mašina_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned simbolio_kodas = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metodas_MODE 경로와 호환한다.
        if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; simbolio_kodas = 0x10000 + ((simbolio_kodas - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdfff) return -22;
        unsigned prekė_COUNT = simbolio_kodas < 128 ? 1 : simbolio_kodas < 2048 ? 2 : simbolio_kodas < 65536 ? 3 : 4;
        if (사용량 + prekė_COUNT > 511) return -36;
        if (prekė_COUNT == 1) KR_duomenys[사용량++] = simbolio_kodas;
        else {
            KR_duomenys[사용량++] = (prekė_COUNT == 2 ? 0xc0 : prekė_COUNT == 3 ? 0xe0 : 0xf0) | (simbolio_kodas >> (6 * (prekė_COUNT - 1)));
            for (unsigned 안쪽순번 = prekė_COUNT - 1; 안쪽순번; 안쪽순번--) KR_duomenys[사용량++] = 0x80 | ((simbolio_kodas >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_duomenys[사용량] = 0; return 사용량 ? 0 : -22;
}
mašina_Word įrankis_kurti(mašina_Word Pavadinimas_2, mašina_Word konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba) {
    char duomenys_padėtis[512]; int KLAIDA = KELIAS(Pavadinimas_2, duomenys_padėtis);
    return (uint32_t)(KLAIDA ? KLAIDA : 호출(3, (mašina_Word)duomenys_padėtis, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, 0));
}
mašina_Word įrankis_Uždaryti(mašina_Word Failas_rodyklė) { return (uint32_t)호출(4, Failas_rodyklė, 0, 0); }
mašina_Word 도구바이트읽기(mašina_Word Failas_rodyklė) {
    unsigned char SECOND_VALUE; intptr_t prekė_COUNT = 호출(2, Failas_rodyklė, (mašina_Word)&SECOND_VALUE, 1);
    return (uint32_t)(prekė_COUNT == 1 ? SECOND_VALUE : prekė_COUNT == 0 ? 256 : prekė_COUNT);
}
mašina_Word įrankis_rašymas_baitas(mašina_Word Failas_rodyklė, mašina_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, Failas_rodyklė, (mašina_Word)&SECOND_VALUE, 1);
}
mašina_Word 도구읽기(mašina_Word Pavadinimas_2, mašina_Word vieta_duomenys_ADDRESS) {
    if (꾸러미사용중) {
        char duomenys_padėtis[512]; int KLAIDA = KELIAS(Pavadinimas_2, duomenys_padėtis); if (KLAIDA) return (uint32_t)KLAIDA;
        unsigned prekė_COUNT = 0; while (duomenys_padėtis[prekė_COUNT]) prekė_COUNT++;
        if (prekė_COUNT >= 6) for (unsigned 순번 = 0; 순번 < prekė_COUNT - 6; 순번++) if (duomenys_padėtis[순번] == '.') duomenys_padėtis[순번] = '/';
        unsigned char 바이트들[16384]; mašina_Word *vieta_VALUE_padėtis = (mašina_Word *)vieta_duomenys_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(duomenys_padėtis, 바이트들, vieta_VALUE_padėtis[0] < sizeof(바이트들) ? vieta_VALUE_padėtis[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) vieta_VALUE_padėtis[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int Failas_rodyklė = 꾸러미사용중 ? -2 : (int32_t)įrankis_kurti(Pavadinimas_2, 0);
    if (Failas_rodyklė < 0) {
        char duomenys_padėtis[512]; int KLAIDA = KELIAS(Pavadinimas_2, duomenys_padėtis); if (KLAIDA) return (uint32_t)KLAIDA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *toliau_OFFSET = 자바클래스들[순번].Pavadinimas_2; unsigned 안쪽순번 = 0;
            while (duomenys_padėtis[안쪽순번] && duomenys_padėtis[안쪽순번] == toliau_OFFSET[안쪽순번]) 안쪽순번++;
            if (duomenys_padėtis[안쪽순번] || toliau_OFFSET[안쪽순번]) continue;
            mašina_Word *vieta_VALUE_padėtis = (mašina_Word *)vieta_duomenys_ADDRESS;
            if (vieta_VALUE_padėtis[0] < 자바클래스들[순번].Dydis) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Dydis; 안쪽순번++) vieta_VALUE_padėtis[안쪽순번 + 1] = 자바클래스들[순번].duomenys[안쪽순번];
            return 자바클래스들[순번].Dydis;
        }
        return (uint32_t)Failas_rodyklė;
    }
    mašina_Word *첫째값 = (mašina_Word *)vieta_duomenys_ADDRESS;
    intptr_t Dydis = 호출(9, Failas_rodyklė, 0, 0), baigta_suma = 0;
    if (Dydis < 0 || (mašina_Word)Dydis > 첫째값[0]) { įrankis_Uždaryti(Failas_rodyklė); return (uint32_t)(Dydis < 0 ? Dydis : -27); }
    unsigned char duomenų_blokas[256];
    while (baigta_suma < Dydis) {
        intptr_t prekė_COUNT = 호출(2, Failas_rodyklė, (mašina_Word)duomenų_blokas, Dydis - baigta_suma < 256 ? Dydis - baigta_suma : 256);
        if (prekė_COUNT <= 0) { įrankis_Uždaryti(Failas_rodyklė); return (uint32_t)(prekė_COUNT ? prekė_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < prekė_COUNT; 순번++) 첫째값[1 + baigta_suma + 순번] = duomenų_blokas[순번];
        baigta_suma += prekė_COUNT;
    }
    įrankis_Uždaryti(Failas_rodyklė); return baigta_suma;
}
mašina_Word įrankis_rašymas(mašina_Word Pavadinimas_2, mašina_Word 원본자료, mašina_Word įrašas_COUNT) {
    const mašina_Word *첫째값 = (const mašina_Word *)원본자료;
    if (įrašas_COUNT > 첫째값[0] || įrašas_COUNT > 16384) return (uint32_t)-27;
    int Failas_rodyklė = (int32_t)įrankis_kurti(Pavadinimas_2, 577); if (Failas_rodyklė < 0) return (uint32_t)Failas_rodyklė;
    unsigned char duomenų_blokas[256]; mašina_Word baigta_suma = 0;
    while (baigta_suma < įrašas_COUNT) {
        mašina_Word prekė_COUNT = įrašas_COUNT - baigta_suma < 256 ? įrašas_COUNT - baigta_suma : 256;
        for (mašina_Word 순번 = 0; 순번 < prekė_COUNT; 순번++) duomenų_blokas[순번] = 첫째값[1 + baigta_suma + 순번];
        intptr_t REZULTATAS = 호출(1, Failas_rodyklė, (mašina_Word)duomenų_blokas, prekė_COUNT);
        if (REZULTATAS <= 0) { įrankis_Uždaryti(Failas_rodyklė); return (uint32_t)(REZULTATAS ? REZULTATAS : -5); }
        baigta_suma += REZULTATAS;
    }
    įrankis_Uždaryti(Failas_rodyklė); return įrašas_COUNT;
}
mašina_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mašina_Word įrankis_argumentas(mašina_Word LOOKUP_INDEX) {
    static const mašina_Word 빈값[1] = {0};
    if (LOOKUP_INDEX >= 8) return (mašina_Word)빈값;
    unsigned char 입력결과[256]; intptr_t prekė_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *duomenys_padėtis = 꾸러미진입클래스(); prekė_COUNT = 0; while (duomenys_padėtis[prekė_COUNT] && prekė_COUNT < 255) { 입력결과[prekė_COUNT] = duomenys_padėtis[prekė_COUNT]; prekė_COUNT++; } }
    else prekė_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mašina_Word)입력결과, sizeof(입력결과));
    if (prekė_COUNT < 0) return (mašina_Word)빈값;
    mašina_Word *KR_duomenys = 전달인수[LOOKUP_INDEX]; unsigned įrašas_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < prekė_COUNT;) {
        unsigned simbolio_kodas = 입력결과[순번++], 더있음 = simbolio_kodas < 128 ? 0 : simbolio_kodas >= 0xc2 && simbolio_kodas < 0xe0 ? 1 : simbolio_kodas < 0xf0 && simbolio_kodas >= 0xe0 ? 2 : simbolio_kodas >= 0xf0 && simbolio_kodas <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > prekė_COUNT) { KR_duomenys[++įrašas_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) simbolio_kodas &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { simbolio_kodas = (simbolio_kodas << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || simbolio_kodas < 최소값 || simbolio_kodas > 0x10ffff || (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdfff)) simbolio_kodas = 0xfffd;
        if (simbolio_kodas >= 65536) { simbolio_kodas -= 65536; KR_duomenys[++įrašas_COUNT] = 0xd800 | (simbolio_kodas >> 10); KR_duomenys[++įrašas_COUNT] = 0xdc00 | (simbolio_kodas & 1023); }
        else KR_duomenys[++įrašas_COUNT] = simbolio_kodas;
    }
    KR_duomenys[0] = įrašas_COUNT; return (mašina_Word)KR_duomenys;
}
mašina_Word 도구분류(void) { return sritis_VALUE; }
void 커널중단(const char *pranešimas_SMS) {
    const char *duomenys_padėtis = pranešimas_SMS; while (*duomenys_padėtis) duomenys_padėtis++;
    바이트들("Java tool runtime error: ", 25); 바이트들(pranešimas_SMS, duomenys_padėtis - pranešimas_SMS); simbolis_a5317f02(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_naudotojas_programa(int metodas_MODE) {
    sritis_VALUE = metodas_MODE;
    unsigned char 첫항목[256]; intptr_t prekė_COUNT = 호출(15, 0, (mašina_Word)첫항목, sizeof(첫항목));
    if (metodas_MODE == 2 || (metodas_MODE == 1 && prekė_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metodas_MODE == 2 ? 0 : 1;
        char Failas_įrašas_pavadinimas[256]; intptr_t 길이값 = 호출(15, 꾸러미인수이동, (mašina_Word)Failas_įrašas_pavadinimas, sizeof(Failas_įrašas_pavadinimas));
        if (길이값 <= 0 || 꾸러미열기(Failas_įrašas_pavadinimas) < 0) {
            static const char KLAIDA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(KLAIDA, sizeof(KLAIDA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int REZULTATAS = 자바진입();
    if (대기중짝글자) simbolis_a5317f02(0xfffd);
    return REZULTATAS;
}

// UDP는 savas 커널의 SVC를 통과하며 dabartinis_prekė 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Šeima, prievado_numeris; uint32_t ADDRESS; unsigned char nulis_VALUE[8]; };
static struct 자바주소 UDP_ADDRESS(unsigned prievado_numeris) {
    struct 자바주소 첫째값 = {2, (uint16_t)((prievado_numeris << 8) | (prievado_numeris >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mašina_Word įrankis_UDP_kurti(mašina_Word prievado_numeris) {
    intptr_t Failas_rodyklė = 호출(32, 2, 2, 17); if (Failas_rodyklė < 0) return (uint32_t)Failas_rodyklė;
    struct 자바주소 첫째값 = UDP_ADDRESS(prievado_numeris);
    첫째값.ADDRESS = 0;
    intptr_t Būsena_VALUE = 호출(33, Failas_rodyklė, (mašina_Word)&첫째값, sizeof(첫째값));
    if (Būsena_VALUE < 0) { įrankis_Uždaryti(Failas_rodyklė); return (uint32_t)Būsena_VALUE; }
    return Failas_rodyklė;
}
mašina_Word įrankis_UDP_siųsti(mašina_Word Failas_rodyklė, mašina_Word prievado_numeris, mašina_Word ARRAY_VALUE, mašina_Word 길이) {
    const mašina_Word *원본주소 = (const mašina_Word *)ARRAY_VALUE; unsigned char duomenys[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (mašina_Word 순번 = 0; 순번 < 길이; 순번++) duomenys[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(prievado_numeris);
    return (uint32_t)사용자호출(34, Failas_rodyklė, (mašina_Word)duomenys, 길이, 0, (mašina_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t prekė_COUNT) { return (prekė_COUNT>>24)|((prekė_COUNT>>8)&0xff00)|((prekė_COUNT<<8)&0xff0000)|(prekė_COUNT<<24); }
mašina_Word įrankis_UDP_siųsti_ADDRESS(mašina_Word Failas_rodyklė, mašina_Word ADDRESS, mašina_Word prievado_numeris, mašina_Word ARRAY_VALUE, mašina_Word 길이) {
    const mašina_Word *원본주소 = (const mašina_Word *)ARRAY_VALUE; unsigned char duomenys[512];
    if (길이 > 512 || 길이 > 원본주소[0]) return (uint32_t)-90;
    for (mašina_Word 순번 = 0; 순번 < 길이; 순번++) duomenys[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(prievado_numeris); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, Failas_rodyklė, (mašina_Word)duomenys, 길이, 0, (mašina_Word)&첫째값, sizeof(첫째값));
}
mašina_Word įrankis_ryšys(mašina_Word Failas_rodyklė, mašina_Word ADDRESS, mašina_Word prievado_numeris) {
    struct 자바주소 첫째값 = UDP_ADDRESS(prievado_numeris); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t Paleisti = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t REZULTATAS = 호출(37, Failas_rodyklė, (mašina_Word)&첫째값, sizeof(첫째값));
        if (REZULTATAS != -115) return (uint32_t)REZULTATAS;
        if ((uint32_t)(호출(7, 0, 0, 0) - Paleisti) >= 1000) return (uint32_t)-110;
    }
}
mašina_Word 도구전문받기(mašina_Word Failas_rodyklė, mašina_Word ARRAY_VALUE, mašina_Word kaupti_pajėgumas) {
    mašina_Word *vieta_ADDRESS = (mašina_Word *)ARRAY_VALUE; unsigned char duomenys[512];
    if (kaupti_pajėgumas > 512 || vieta_ADDRESS[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t prekė_COUNT = 사용자호출(35, Failas_rodyklė, (mašina_Word)duomenys, kaupti_pajėgumas, 0, (mašina_Word)&첫째값, (mašina_Word)&길이값);
    if (prekė_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < prekė_COUNT; 순번++) vieta_ADDRESS[순번 + 1] = duomenys[순번]; vieta_ADDRESS[513] = (첫째값.prievado_numeris << 8 | 첫째값.prievado_numeris >> 8) & 65535; vieta_ADDRESS[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)prekė_COUNT;
}
mašina_Word įrankis_UDP_jungtis(mašina_Word Failas_rodyklė) {
    struct 자바주소 첫째값; unsigned 길이값 = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Failas_rodyklė, (mašina_Word)&첫째값, (mašina_Word)&길이값);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.prievado_numeris << 8 | 첫째값.prievado_numeris >> 8) & 65535);
}
mašina_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mašina_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mašina_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mašina_Word įrankis_grafiniai_elementai_Palauk(void) { return (uint32_t)화면키기다리기(); }
mašina_Word įrankis_stačiakampis(mašina_Word x_koordinatė, mašina_Word 세로좌표, mašina_Word 너비값, mašina_Word 높이값, mašina_Word 색상) {
    return (uint32_t)사용자호출(13, x_koordinatė, 세로좌표, 색상, 너비값, 높이값, 0);
}

mašina_Word įrankis_Stream(mašina_Word Veiksmas,mašina_Word Failas_rodyklė,mašina_Word VALUE){
    if(Veiksmas==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADDRESS(VALUE);
    if(Veiksmas==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,Failas_rodyklė,(mašina_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Failas_rodyklė,4,0));}
    if(Veiksmas==2)return (uint32_t)호출(37,Failas_rodyklė,(mašina_Word)&첫째값,sizeof(첫째값));
    if(Veiksmas==3)return (uint32_t)호출(39,Failas_rodyklė,0,0);
    if(Veiksmas==4)return įrankis_UDP_jungtis(Failas_rodyklė);
    if(Veiksmas==5)return (uint32_t)호출(40,Failas_rodyklė,0,0);
    return (uint32_t)-22;
}
mašina_Word įrankis_GUI(mašina_Word Veiksmas,mašina_Word identifikatorius_VALUE,mašina_Word 첫째값,mašina_Word SECOND_VALUE,mašina_Word simbolio_kodas,mašina_Word vieta_duomenys){return (uint32_t)사용자호출(20,Veiksmas,identifikatorius_VALUE,첫째값,SECOND_VALUE,simbolio_kodas,vieta_duomenys);}
mašina_Word įrankis_GUI_SMS(mašina_Word identifikatorius_VALUE,mašina_Word ARRAY_VALUE,mašina_Word prekė_COUNT){
    const mašina_Word *원본주소=(const mašina_Word *)ARRAY_VALUE;uint32_t duomenys[127];unsigned įrašas_COUNT=0;
    if(prekė_COUNT>원본주소[0])return (uint32_t)-22;
    for(mašina_Word 순번=0;순번<prekė_COUNT;순번++){unsigned simbolių_koduotė=원본주소[순번+1];if(simbolių_koduotė>=0xd800&&simbolių_koduotė<=0xdbff&&순번+1<prekė_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;simbolių_koduotė=0x10000+((simbolių_koduotė-0xd800)<<10)+낮은값-0xdc00;}if(įrašas_COUNT==127)return (uint32_t)-22;duomenys[įrašas_COUNT++]=simbolių_koduotė;}
    return (uint32_t)사용자호출(21,identifikatorius_VALUE,(mašina_Word)duomenys,įrašas_COUNT,0,0,0);
}
