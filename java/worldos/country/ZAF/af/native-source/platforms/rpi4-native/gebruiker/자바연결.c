#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Lêer/Afvoer/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bondel.h"
typedef uintptr_t masjien_Word;
static int kategorie_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static masjien_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned item_COUNT, masjien_Word 첫째값, masjien_Word SECOND_VALUE, masjien_Word karakterkode) {
    return 사용자호출(item_COUNT, 첫째값, SECOND_VALUE, karakterkode, 0, 0, 0);
}
static void 바이트들(const char *data_plaas, size_t item_COUNT) { 호출(1, 1, (masjien_Word)data_plaas, item_COUNT); }
static void karakter(unsigned karakterkode) {
    unsigned char data[4]; unsigned item_COUNT = 0;
    if (karakterkode < 128) data[item_COUNT++] = karakterkode;
    else if (karakterkode < 2048) { data[item_COUNT++] = 0xc0 | (karakterkode >> 6); data[item_COUNT++] = 0x80 | (karakterkode & 63); }
    else if (karakterkode < 65536) { data[item_COUNT++] = 0xe0 | (karakterkode >> 12); data[item_COUNT++] = 0x80 | ((karakterkode >> 6) & 63); data[item_COUNT++] = 0x80 | (karakterkode & 63); }
    else { data[item_COUNT++] = 0xf0 | (karakterkode >> 18); data[item_COUNT++] = 0x80 | ((karakterkode >> 12) & 63); data[item_COUNT++] = 0x80 | ((karakterkode >> 6) & 63); data[item_COUNT++] = 0x80 | (karakterkode & 63); }
    바이트들((const char *)data, item_COUNT);
}
masjien_Word nutsmiddel_karakter(masjien_Word VALUE) {
    unsigned karakterkode = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (karakterkode >= 0xdc00 && karakterkode <= 0xdfff) { karakter(0x10000 + ((높은부분 - 0xd800) << 10) + karakterkode - 0xdc00); return 1; }
        karakter(0xfffd);
    }
    if (karakterkode >= 0xd800 && karakterkode <= 0xdbff) 대기중짝글자 = karakterkode;
    else karakter(karakterkode > 0x10ffff || (karakterkode >= 0xdc00 && karakterkode <= 0xdfff) ? 0xfffd : karakterkode);
    return 1;
}
masjien_Word 도구출력(masjien_Word VALUE) {
    const masjien_Word *string_data = (const masjien_Word *)VALUE;
    for (masjien_Word 순번 = 0; 순번 < string_data[0]; 순번++) nutsmiddel_karakter(string_data[순번 + 1]);
    return string_data[0];
}
static int Pad(masjien_Word objek_Naslaan, char maatreël_data[512]) {
    const masjien_Word *첫째값 = (const masjien_Word *)objek_Naslaan;
    unsigned 사용량 = 0;
    for (masjien_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned karakterkode = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metode_MODE 경로와 호환한다.
        if (karakterkode >= 0xd800 && karakterkode <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; karakterkode = 0x10000 + ((karakterkode - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (karakterkode >= 0xd800 && karakterkode <= 0xdfff) return -22;
        unsigned item_COUNT = karakterkode < 128 ? 1 : karakterkode < 2048 ? 2 : karakterkode < 65536 ? 3 : 4;
        if (사용량 + item_COUNT > 511) return -36;
        if (item_COUNT == 1) maatreël_data[사용량++] = karakterkode;
        else {
            maatreël_data[사용량++] = (item_COUNT == 2 ? 0xc0 : item_COUNT == 3 ? 0xe0 : 0xf0) | (karakterkode >> (6 * (item_COUNT - 1)));
            for (unsigned 안쪽순번 = item_COUNT - 1; 안쪽순번; 안쪽순번--) maatreël_data[사용량++] = 0x80 | ((karakterkode >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    maatreël_data[사용량] = 0; return 사용량 ? 0 : -22;
}
masjien_Word nutsmiddel_skep(masjien_Word Naam, masjien_Word konfigurasie_Agtergrond_intelligente_oordragdiens) {
    char data_plaas[512]; int Fout = Pad(Naam, data_plaas);
    return (uint32_t)(Fout ? Fout : 호출(3, (masjien_Word)data_plaas, konfigurasie_Agtergrond_intelligente_oordragdiens, 0));
}
masjien_Word nutsmiddel_sluit(masjien_Word lêer_handvatsel) { return (uint32_t)호출(4, lêer_handvatsel, 0, 0); }
masjien_Word 도구바이트읽기(masjien_Word lêer_handvatsel) {
    unsigned char SECOND_VALUE; intptr_t item_COUNT = 호출(2, lêer_handvatsel, (masjien_Word)&SECOND_VALUE, 1);
    return (uint32_t)(item_COUNT == 1 ? SECOND_VALUE : item_COUNT == 0 ? 256 : item_COUNT);
}
masjien_Word nutsmiddel_skryf_greep(masjien_Word lêer_handvatsel, masjien_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, lêer_handvatsel, (masjien_Word)&SECOND_VALUE, 1);
}
masjien_Word 도구읽기(masjien_Word Naam, masjien_Word bestemming_data_adres) {
    if (꾸러미사용중) {
        char data_plaas[512]; int Fout = Pad(Naam, data_plaas); if (Fout) return (uint32_t)Fout;
        unsigned item_COUNT = 0; while (data_plaas[item_COUNT]) item_COUNT++;
        if (item_COUNT >= 6) for (unsigned 순번 = 0; 순번 < item_COUNT - 6; 순번++) if (data_plaas[순번] == '.') data_plaas[순번] = '/';
        unsigned char 바이트들[16384]; masjien_Word *bestemming_VALUE_plaas = (masjien_Word *)bestemming_data_adres;
        int RECEIVED_COUNT = 꾸러미읽기(data_plaas, 바이트들, bestemming_VALUE_plaas[0] < sizeof(바이트들) ? bestemming_VALUE_plaas[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) bestemming_VALUE_plaas[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int lêer_handvatsel = 꾸러미사용중 ? -2 : (int32_t)nutsmiddel_skep(Naam, 0);
    if (lêer_handvatsel < 0) {
        char data_plaas[512]; int Fout = Pad(Naam, data_plaas); if (Fout) return (uint32_t)Fout;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Volgende_OFFSET = 자바클래스들[순번].Naam; unsigned 안쪽순번 = 0;
            while (data_plaas[안쪽순번] && data_plaas[안쪽순번] == Volgende_OFFSET[안쪽순번]) 안쪽순번++;
            if (data_plaas[안쪽순번] || Volgende_OFFSET[안쪽순번]) continue;
            masjien_Word *bestemming_VALUE_plaas = (masjien_Word *)bestemming_data_adres;
            if (bestemming_VALUE_plaas[0] < 자바클래스들[순번].Grootte) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Grootte; 안쪽순번++) bestemming_VALUE_plaas[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Grootte;
        }
        return (uint32_t)lêer_handvatsel;
    }
    masjien_Word *첫째값 = (masjien_Word *)bestemming_data_adres;
    intptr_t Grootte = 호출(9, lêer_handvatsel, 0, 0), 완료량 = 0;
    if (Grootte < 0 || (masjien_Word)Grootte > 첫째값[0]) { nutsmiddel_sluit(lêer_handvatsel); return (uint32_t)(Grootte < 0 ? Grootte : -27); }
    unsigned char data_blokkeer[256];
    while (완료량 < Grootte) {
        intptr_t item_COUNT = 호출(2, lêer_handvatsel, (masjien_Word)data_blokkeer, Grootte - 완료량 < 256 ? Grootte - 완료량 : 256);
        if (item_COUNT <= 0) { nutsmiddel_sluit(lêer_handvatsel); return (uint32_t)(item_COUNT ? item_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = data_blokkeer[순번];
        완료량 += item_COUNT;
    }
    nutsmiddel_sluit(lêer_handvatsel); return 완료량;
}
masjien_Word nutsmiddel_skryf(masjien_Word Naam, masjien_Word 원본자료, masjien_Word inskrywing_COUNT) {
    const masjien_Word *첫째값 = (const masjien_Word *)원본자료;
    if (inskrywing_COUNT > 첫째값[0] || inskrywing_COUNT > 16384) return (uint32_t)-27;
    int lêer_handvatsel = (int32_t)nutsmiddel_skep(Naam, 577); if (lêer_handvatsel < 0) return (uint32_t)lêer_handvatsel;
    unsigned char data_blokkeer[256]; masjien_Word 완료량 = 0;
    while (완료량 < inskrywing_COUNT) {
        masjien_Word item_COUNT = inskrywing_COUNT - 완료량 < 256 ? inskrywing_COUNT - 완료량 : 256;
        for (masjien_Word 순번 = 0; 순번 < item_COUNT; 순번++) data_blokkeer[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t maatreël = 호출(1, lêer_handvatsel, (masjien_Word)data_blokkeer, item_COUNT);
        if (maatreël <= 0) { nutsmiddel_sluit(lêer_handvatsel); return (uint32_t)(maatreël ? maatreël : -5); }
        완료량 += maatreël;
    }
    nutsmiddel_sluit(lêer_handvatsel); return inskrywing_COUNT;
}
masjien_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
masjien_Word nutsmiddel_argument(masjien_Word LOOKUP_INDEX) {
    static const masjien_Word leeg_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (masjien_Word)leeg_VALUE;
    unsigned char 입력결과[256]; intptr_t item_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *data_plaas = 꾸러미진입클래스(); item_COUNT = 0; while (data_plaas[item_COUNT] && item_COUNT < 255) { 입력결과[item_COUNT] = data_plaas[item_COUNT]; item_COUNT++; } }
    else item_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (masjien_Word)입력결과, sizeof(입력결과));
    if (item_COUNT < 0) return (masjien_Word)leeg_VALUE;
    masjien_Word *maatreël_data = 전달인수[LOOKUP_INDEX]; unsigned inskrywing_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < item_COUNT;) {
        unsigned karakterkode = 입력결과[순번++], 더있음 = karakterkode < 128 ? 0 : karakterkode >= 0xc2 && karakterkode < 0xe0 ? 1 : karakterkode < 0xf0 && karakterkode >= 0xe0 ? 2 : karakterkode >= 0xf0 && karakterkode <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > item_COUNT) { maatreël_data[++inskrywing_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) karakterkode &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { karakterkode = (karakterkode << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || karakterkode < 최소값 || karakterkode > 0x10ffff || (karakterkode >= 0xd800 && karakterkode <= 0xdfff)) karakterkode = 0xfffd;
        if (karakterkode >= 65536) { karakterkode -= 65536; maatreël_data[++inskrywing_COUNT] = 0xd800 | (karakterkode >> 10); maatreël_data[++inskrywing_COUNT] = 0xdc00 | (karakterkode & 1023); }
        else maatreël_data[++inskrywing_COUNT] = karakterkode;
    }
    maatreël_data[0] = inskrywing_COUNT; return (masjien_Word)maatreël_data;
}
masjien_Word 도구분류(void) { return kategorie_VALUE; }
void 커널중단(const char *알림문) {
    const char *data_plaas = 알림문; while (*data_plaas) data_plaas++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_plaas - 알림문); karakter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int BEGIN_gebruiker_program(int metode_MODE) {
    kategorie_VALUE = metode_MODE;
    unsigned char 첫항목[256]; intptr_t item_COUNT = 호출(15, 0, (masjien_Word)첫항목, sizeof(첫항목));
    if (metode_MODE == 2 || (metode_MODE == 1 && item_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metode_MODE == 2 ? 0 : 1;
        char lêer_inskrywing_naam[256]; intptr_t lengte_data = 호출(15, 꾸러미인수이동, (masjien_Word)lêer_inskrywing_naam, sizeof(lêer_inskrywing_naam));
        if (lengte_data <= 0 || 꾸러미열기(lêer_inskrywing_naam) < 0) {
            static const char Fout[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Fout, sizeof(Fout) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int maatreël = 자바진입();
    if (대기중짝글자) karakter(0xfffd);
    return maatreël;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Gesin, 접속번호; uint32_t adres; unsigned char 영값[8]; };
static struct 자바주소 GDP_Gebruikersdatagramprotokol_adres(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
masjien_Word nutsmiddel_GDP_Gebruikersdatagramprotokol_skep(masjien_Word 접속번호) {
    intptr_t lêer_handvatsel = 호출(32, 2, 2, 17); if (lêer_handvatsel < 0) return (uint32_t)lêer_handvatsel;
    struct 자바주소 첫째값 = GDP_Gebruikersdatagramprotokol_adres(접속번호);
    첫째값.adres = 0;
    intptr_t stand_VALUE = 호출(33, lêer_handvatsel, (masjien_Word)&첫째값, sizeof(첫째값));
    if (stand_VALUE < 0) { nutsmiddel_sluit(lêer_handvatsel); return (uint32_t)stand_VALUE; }
    return lêer_handvatsel;
}
masjien_Word nutsmiddel_GDP_Gebruikersdatagramprotokol_e_pos(masjien_Word lêer_handvatsel, masjien_Word 접속번호, masjien_Word ARRAY_VALUE, masjien_Word lengte_VALUE) {
    const masjien_Word *원본주소 = (const masjien_Word *)ARRAY_VALUE; unsigned char data[512];
    if (lengte_VALUE > 512 || lengte_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (masjien_Word 순번 = 0; 순번 < lengte_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = GDP_Gebruikersdatagramprotokol_adres(접속번호);
    return (uint32_t)사용자호출(34, lêer_handvatsel, (masjien_Word)data, lengte_VALUE, 0, (masjien_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t item_COUNT) { return (item_COUNT>>24)|((item_COUNT>>8)&0xff00)|((item_COUNT<<8)&0xff0000)|(item_COUNT<<24); }
masjien_Word nutsmiddel_GDP_Gebruikersdatagramprotokol_e_pos_adres(masjien_Word lêer_handvatsel, masjien_Word adres, masjien_Word 접속번호, masjien_Word ARRAY_VALUE, masjien_Word lengte_VALUE) {
    const masjien_Word *원본주소 = (const masjien_Word *)ARRAY_VALUE; unsigned char data[512];
    if (lengte_VALUE > 512 || lengte_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (masjien_Word 순번 = 0; 순번 < lengte_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = GDP_Gebruikersdatagramprotokol_adres(접속번호); 첫째값.adres = 바이트순서뒤집기(adres);
    return (uint32_t)사용자호출(34, lêer_handvatsel, (masjien_Word)data, lengte_VALUE, 0, (masjien_Word)&첫째값, sizeof(첫째값));
}
masjien_Word nutsmiddel_KOPPEL(masjien_Word lêer_handvatsel, masjien_Word adres, masjien_Word 접속번호) {
    struct 자바주소 첫째값 = GDP_Gebruikersdatagramprotokol_adres(접속번호); 첫째값.adres = 바이트순서뒤집기(adres);
    uint32_t Loop = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t maatreël = 호출(37, lêer_handvatsel, (masjien_Word)&첫째값, sizeof(첫째값));
        if (maatreël != -115) return (uint32_t)maatreël;
        if ((uint32_t)(호출(7, 0, 0, 0) - Loop) >= 1000) return (uint32_t)-110;
    }
}
masjien_Word 도구전문받기(masjien_Word lêer_handvatsel, masjien_Word ARRAY_VALUE, masjien_Word 수용량) {
    masjien_Word *bestemming_adres = (masjien_Word *)ARRAY_VALUE; unsigned char data[512];
    if (수용량 > 512 || bestemming_adres[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned lengte_data = sizeof(첫째값);
    intptr_t item_COUNT = 사용자호출(35, lêer_handvatsel, (masjien_Word)data, 수용량, 0, (masjien_Word)&첫째값, (masjien_Word)&lengte_data);
    if (item_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) bestemming_adres[순번 + 1] = data[순번]; bestemming_adres[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; bestemming_adres[514] = 바이트순서뒤집기(첫째값.adres); }
    return (uint32_t)item_COUNT;
}
masjien_Word nutsmiddel_GDP_Gebruikersdatagramprotokol_ombou(masjien_Word lêer_handvatsel) {
    struct 자바주소 첫째값; unsigned lengte_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, lêer_handvatsel, (masjien_Word)&첫째값, (masjien_Word)&lengte_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
masjien_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
masjien_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
masjien_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
masjien_Word nutsmiddel_grafika_wag(void) { return (uint32_t)화면키기다리기(); }
masjien_Word 도구사각형(masjien_Word x_koördinaat, masjien_Word Y_koördinaat, masjien_Word 너비값, masjien_Word 높이값, masjien_Word 색상) {
    return (uint32_t)사용자호출(13, x_koördinaat, Y_koördinaat, 색상, 너비값, 높이값, 0);
}

masjien_Word nutsmiddel_Stream(masjien_Word Aksie,masjien_Word lêer_handvatsel,masjien_Word VALUE){
    if(Aksie==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=GDP_Gebruikersdatagramprotokol_adres(VALUE);
    if(Aksie==1){첫째값.adres=0;intptr_t 반환값=호출(33,lêer_handvatsel,(masjien_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,lêer_handvatsel,4,0));}
    if(Aksie==2)return (uint32_t)호출(37,lêer_handvatsel,(masjien_Word)&첫째값,sizeof(첫째값));
    if(Aksie==3)return (uint32_t)호출(39,lêer_handvatsel,0,0);
    if(Aksie==4)return nutsmiddel_GDP_Gebruikersdatagramprotokol_ombou(lêer_handvatsel);
    if(Aksie==5)return (uint32_t)호출(40,lêer_handvatsel,0,0);
    return (uint32_t)-22;
}
masjien_Word nutsmiddel_GUI(masjien_Word Aksie,masjien_Word waarde_VALUE,masjien_Word 첫째값,masjien_Word SECOND_VALUE,masjien_Word karakterkode,masjien_Word bestemming_data){return (uint32_t)사용자호출(20,Aksie,waarde_VALUE,첫째값,SECOND_VALUE,karakterkode,bestemming_data);}
masjien_Word nutsmiddel_GUI_SMS(masjien_Word waarde_VALUE,masjien_Word ARRAY_VALUE,masjien_Word item_COUNT){
    const masjien_Word *원본주소=(const masjien_Word *)ARRAY_VALUE;uint32_t data[127];unsigned inskrywing_COUNT=0;
    if(item_COUNT>원본주소[0])return (uint32_t)-22;
    for(masjien_Word 순번=0;순번<item_COUNT;순번++){unsigned karakter_enkodering=원본주소[순번+1];if(karakter_enkodering>=0xd800&&karakter_enkodering<=0xdbff&&순번+1<item_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;karakter_enkodering=0x10000+((karakter_enkodering-0xd800)<<10)+낮은값-0xdc00;}if(inskrywing_COUNT==127)return (uint32_t)-22;data[inskrywing_COUNT++]=karakter_enkodering;}
    return (uint32_t)사용자호출(21,waarde_VALUE,(masjien_Word)data,inskrywing_COUNT,0,0,0);
}
