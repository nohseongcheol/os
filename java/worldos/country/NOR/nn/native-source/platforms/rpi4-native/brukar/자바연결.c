#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fil/Utdata/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bunt.h"
typedef uintptr_t maskin_Word;
static int kategori_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static maskin_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned vare_COUNT, maskin_Word 첫째값, maskin_Word SECOND_VALUE, maskin_Word teiknkode) {
    return 사용자호출(vare_COUNT, 첫째값, SECOND_VALUE, teiknkode, 0, 0, 0);
}
static void 바이트들(const char *data_plassere, size_t vare_COUNT) { 호출(1, 1, (maskin_Word)data_plassere, vare_COUNT); }
static void teikn(unsigned teiknkode) {
    unsigned char data[4]; unsigned vare_COUNT = 0;
    if (teiknkode < 128) data[vare_COUNT++] = teiknkode;
    else if (teiknkode < 2048) { data[vare_COUNT++] = 0xc0 | (teiknkode >> 6); data[vare_COUNT++] = 0x80 | (teiknkode & 63); }
    else if (teiknkode < 65536) { data[vare_COUNT++] = 0xe0 | (teiknkode >> 12); data[vare_COUNT++] = 0x80 | ((teiknkode >> 6) & 63); data[vare_COUNT++] = 0x80 | (teiknkode & 63); }
    else { data[vare_COUNT++] = 0xf0 | (teiknkode >> 18); data[vare_COUNT++] = 0x80 | ((teiknkode >> 12) & 63); data[vare_COUNT++] = 0x80 | ((teiknkode >> 6) & 63); data[vare_COUNT++] = 0x80 | (teiknkode & 63); }
    바이트들((const char *)data, vare_COUNT);
}
maskin_Word verktøy_teikn(maskin_Word VALUE) {
    unsigned teiknkode = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (teiknkode >= 0xdc00 && teiknkode <= 0xdfff) { teikn(0x10000 + ((높은부분 - 0xd800) << 10) + teiknkode - 0xdc00); return 1; }
        teikn(0xfffd);
    }
    if (teiknkode >= 0xd800 && teiknkode <= 0xdbff) 대기중짝글자 = teiknkode;
    else teikn(teiknkode > 0x10ffff || (teiknkode >= 0xdc00 && teiknkode <= 0xdfff) ? 0xfffd : teiknkode);
    return 1;
}
maskin_Word 도구출력(maskin_Word VALUE) {
    const maskin_Word *streng_data = (const maskin_Word *)VALUE;
    for (maskin_Word 순번 = 0; 순번 < streng_data[0]; 순번++) verktøy_teikn(streng_data[순번 + 1]);
    return streng_data[0];
}
static int STIGE(maskin_Word objekt_Oppslagsverk, char forretningsmål_data[512]) {
    const maskin_Word *첫째값 = (const maskin_Word *)objekt_Oppslagsverk;
    unsigned 사용량 = 0;
    for (maskin_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned teiknkode = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metode_MODE 경로와 호환한다.
        if (teiknkode >= 0xd800 && teiknkode <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; teiknkode = 0x10000 + ((teiknkode - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (teiknkode >= 0xd800 && teiknkode <= 0xdfff) return -22;
        unsigned vare_COUNT = teiknkode < 128 ? 1 : teiknkode < 2048 ? 2 : teiknkode < 65536 ? 3 : 4;
        if (사용량 + vare_COUNT > 511) return -36;
        if (vare_COUNT == 1) forretningsmål_data[사용량++] = teiknkode;
        else {
            forretningsmål_data[사용량++] = (vare_COUNT == 2 ? 0xc0 : vare_COUNT == 3 ? 0xe0 : 0xf0) | (teiknkode >> (6 * (vare_COUNT - 1)));
            for (unsigned 안쪽순번 = vare_COUNT - 1; 안쪽순번; 안쪽순번--) forretningsmål_data[사용량++] = 0x80 | ((teiknkode >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    forretningsmål_data[사용량] = 0; return 사용량 ? 0 : -22;
}
maskin_Word verktøy_opne(maskin_Word Namn, maskin_Word 설정비트) {
    char data_plassere[512]; int FEIL = STIGE(Namn, data_plassere);
    return (uint32_t)(FEIL ? FEIL : 호출(3, (maskin_Word)data_plassere, 설정비트, 0));
}
maskin_Word verktøy_Lukk(maskin_Word fil_handtak) { return (uint32_t)호출(4, fil_handtak, 0, 0); }
maskin_Word 도구바이트읽기(maskin_Word fil_handtak) {
    unsigned char SECOND_VALUE; intptr_t vare_COUNT = 호출(2, fil_handtak, (maskin_Word)&SECOND_VALUE, 1);
    return (uint32_t)(vare_COUNT == 1 ? SECOND_VALUE : vare_COUNT == 0 ? 256 : vare_COUNT);
}
maskin_Word verktøy_skrive_byte(maskin_Word fil_handtak, maskin_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, fil_handtak, (maskin_Word)&SECOND_VALUE, 1);
}
maskin_Word 도구읽기(maskin_Word Namn, maskin_Word mål_data_ADDRESS) {
    if (꾸러미사용중) {
        char data_plassere[512]; int FEIL = STIGE(Namn, data_plassere); if (FEIL) return (uint32_t)FEIL;
        unsigned vare_COUNT = 0; while (data_plassere[vare_COUNT]) vare_COUNT++;
        if (vare_COUNT >= 6) for (unsigned 순번 = 0; 순번 < vare_COUNT - 6; 순번++) if (data_plassere[순번] == '.') data_plassere[순번] = '/';
        unsigned char 바이트들[16384]; maskin_Word *mål_VALUE_plassere = (maskin_Word *)mål_data_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(data_plassere, 바이트들, mål_VALUE_plassere[0] < sizeof(바이트들) ? mål_VALUE_plassere[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) mål_VALUE_plassere[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int fil_handtak = 꾸러미사용중 ? -2 : (int32_t)verktøy_opne(Namn, 0);
    if (fil_handtak < 0) {
        char data_plassere[512]; int FEIL = STIGE(Namn, data_plassere); if (FEIL) return (uint32_t)FEIL;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Neste_OFFSET = 자바클래스들[순번].Namn; unsigned 안쪽순번 = 0;
            while (data_plassere[안쪽순번] && data_plassere[안쪽순번] == Neste_OFFSET[안쪽순번]) 안쪽순번++;
            if (data_plassere[안쪽순번] || Neste_OFFSET[안쪽순번]) continue;
            maskin_Word *mål_VALUE_plassere = (maskin_Word *)mål_data_ADDRESS;
            if (mål_VALUE_plassere[0] < 자바클래스들[순번].Storleik) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Storleik; 안쪽순번++) mål_VALUE_plassere[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Storleik;
        }
        return (uint32_t)fil_handtak;
    }
    maskin_Word *첫째값 = (maskin_Word *)mål_data_ADDRESS;
    intptr_t Storleik = 호출(9, fil_handtak, 0, 0), 완료량 = 0;
    if (Storleik < 0 || (maskin_Word)Storleik > 첫째값[0]) { verktøy_Lukk(fil_handtak); return (uint32_t)(Storleik < 0 ? Storleik : -27); }
    unsigned char data_Blokker[256];
    while (완료량 < Storleik) {
        intptr_t vare_COUNT = 호출(2, fil_handtak, (maskin_Word)data_Blokker, Storleik - 완료량 < 256 ? Storleik - 완료량 : 256);
        if (vare_COUNT <= 0) { verktøy_Lukk(fil_handtak); return (uint32_t)(vare_COUNT ? vare_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < vare_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = data_Blokker[순번];
        완료량 += vare_COUNT;
    }
    verktøy_Lukk(fil_handtak); return 완료량;
}
maskin_Word verktøy_skrive(maskin_Word Namn, maskin_Word 원본자료, maskin_Word oppføring_COUNT) {
    const maskin_Word *첫째값 = (const maskin_Word *)원본자료;
    if (oppføring_COUNT > 첫째값[0] || oppføring_COUNT > 16384) return (uint32_t)-27;
    int fil_handtak = (int32_t)verktøy_opne(Namn, 577); if (fil_handtak < 0) return (uint32_t)fil_handtak;
    unsigned char data_Blokker[256]; maskin_Word 완료량 = 0;
    while (완료량 < oppføring_COUNT) {
        maskin_Word vare_COUNT = oppføring_COUNT - 완료량 < 256 ? oppføring_COUNT - 완료량 : 256;
        for (maskin_Word 순번 = 0; 순번 < vare_COUNT; 순번++) data_Blokker[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t forretningsmål = 호출(1, fil_handtak, (maskin_Word)data_Blokker, vare_COUNT);
        if (forretningsmål <= 0) { verktøy_Lukk(fil_handtak); return (uint32_t)(forretningsmål ? forretningsmål : -5); }
        완료량 += forretningsmål;
    }
    verktøy_Lukk(fil_handtak); return oppføring_COUNT;
}
maskin_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
maskin_Word verktøy_argument(maskin_Word LOOKUP_INDEX) {
    static const maskin_Word tom_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (maskin_Word)tom_VALUE;
    unsigned char 입력결과[256]; intptr_t vare_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *data_plassere = 꾸러미진입클래스(); vare_COUNT = 0; while (data_plassere[vare_COUNT] && vare_COUNT < 255) { 입력결과[vare_COUNT] = data_plassere[vare_COUNT]; vare_COUNT++; } }
    else vare_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (maskin_Word)입력결과, sizeof(입력결과));
    if (vare_COUNT < 0) return (maskin_Word)tom_VALUE;
    maskin_Word *forretningsmål_data = 전달인수[LOOKUP_INDEX]; unsigned oppføring_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < vare_COUNT;) {
        unsigned teiknkode = 입력결과[순번++], 더있음 = teiknkode < 128 ? 0 : teiknkode >= 0xc2 && teiknkode < 0xe0 ? 1 : teiknkode < 0xf0 && teiknkode >= 0xe0 ? 2 : teiknkode >= 0xf0 && teiknkode <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > vare_COUNT) { forretningsmål_data[++oppføring_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) teiknkode &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { teiknkode = (teiknkode << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || teiknkode < 최소값 || teiknkode > 0x10ffff || (teiknkode >= 0xd800 && teiknkode <= 0xdfff)) teiknkode = 0xfffd;
        if (teiknkode >= 65536) { teiknkode -= 65536; forretningsmål_data[++oppføring_COUNT] = 0xd800 | (teiknkode >> 10); forretningsmål_data[++oppføring_COUNT] = 0xdc00 | (teiknkode & 1023); }
        else forretningsmål_data[++oppføring_COUNT] = teiknkode;
    }
    forretningsmål_data[0] = oppføring_COUNT; return (maskin_Word)forretningsmål_data;
}
maskin_Word 도구분류(void) { return kategori_VALUE; }
void 커널중단(const char *알림문) {
    const char *data_plassere = 알림문; while (*data_plassere) data_plassere++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_plassere - 알림문); teikn(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_brukar_app(int metode_MODE) {
    kategori_VALUE = metode_MODE;
    unsigned char 첫항목[256]; intptr_t vare_COUNT = 호출(15, 0, (maskin_Word)첫항목, sizeof(첫항목));
    if (metode_MODE == 2 || (metode_MODE == 1 && vare_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metode_MODE == 2 ? 0 : 1;
        char fil_oppføring_namn[256]; intptr_t lengd_data = 호출(15, 꾸러미인수이동, (maskin_Word)fil_oppføring_namn, sizeof(fil_oppføring_namn));
        if (lengd_data <= 0 || 꾸러미열기(fil_oppføring_namn) < 0) {
            static const char FEIL[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(FEIL, sizeof(FEIL) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int forretningsmål = 자바진입();
    if (대기중짝글자) teikn(0xfffd);
    return forretningsmål;
}

// UDP는 자체 커널의 SVC를 통과하며 betalt_vare 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Familie, portnummer; uint32_t ADDRESS; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned portnummer) {
    struct 자바주소 첫째값 = {2, (uint16_t)((portnummer << 8) | (portnummer >> 8)), 0x0100007f, {0}}; return 첫째값;
}
maskin_Word 도구전문열기(maskin_Word portnummer) {
    intptr_t fil_handtak = 호출(32, 2, 2, 17); if (fil_handtak < 0) return (uint32_t)fil_handtak;
    struct 자바주소 첫째값 = 전문주소(portnummer);
    첫째값.ADDRESS = 0;
    intptr_t status_VALUE = 호출(33, fil_handtak, (maskin_Word)&첫째값, sizeof(첫째값));
    if (status_VALUE < 0) { verktøy_Lukk(fil_handtak); return (uint32_t)status_VALUE; }
    return fil_handtak;
}
maskin_Word 도구전문보내기(maskin_Word fil_handtak, maskin_Word portnummer, maskin_Word ARRAY_VALUE, maskin_Word lengd_VALUE) {
    const maskin_Word *원본주소 = (const maskin_Word *)ARRAY_VALUE; unsigned char data[512];
    if (lengd_VALUE > 512 || lengd_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (maskin_Word 순번 = 0; 순번 < lengd_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(portnummer);
    return (uint32_t)사용자호출(34, fil_handtak, (maskin_Word)data, lengd_VALUE, 0, (maskin_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t vare_COUNT) { return (vare_COUNT>>24)|((vare_COUNT>>8)&0xff00)|((vare_COUNT<<8)&0xff0000)|(vare_COUNT<<24); }
maskin_Word 도구전문주소보내기(maskin_Word fil_handtak, maskin_Word ADDRESS, maskin_Word portnummer, maskin_Word ARRAY_VALUE, maskin_Word lengd_VALUE) {
    const maskin_Word *원본주소 = (const maskin_Word *)ARRAY_VALUE; unsigned char data[512];
    if (lengd_VALUE > 512 || lengd_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (maskin_Word 순번 = 0; 순번 < lengd_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(portnummer); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, fil_handtak, (maskin_Word)data, lengd_VALUE, 0, (maskin_Word)&첫째값, sizeof(첫째값));
}
maskin_Word verktøy_KOPLE_TIL(maskin_Word fil_handtak, maskin_Word ADDRESS, maskin_Word portnummer) {
    struct 자바주소 첫째값 = 전문주소(portnummer); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t Køyr_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t forretningsmål = 호출(37, fil_handtak, (maskin_Word)&첫째값, sizeof(첫째값));
        if (forretningsmål != -115) return (uint32_t)forretningsmål;
        if ((uint32_t)(호출(7, 0, 0, 0) - Køyr_2) >= 1000) return (uint32_t)-110;
    }
}
maskin_Word 도구전문받기(maskin_Word fil_handtak, maskin_Word ARRAY_VALUE, maskin_Word 수용량) {
    maskin_Word *mål_ADDRESS_08bbd577 = (maskin_Word *)ARRAY_VALUE; unsigned char data[512];
    if (수용량 > 512 || mål_ADDRESS_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned lengd_data = sizeof(첫째값);
    intptr_t vare_COUNT = 사용자호출(35, fil_handtak, (maskin_Word)data, 수용량, 0, (maskin_Word)&첫째값, (maskin_Word)&lengd_data);
    if (vare_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < vare_COUNT; 순번++) mål_ADDRESS_08bbd577[순번 + 1] = data[순번]; mål_ADDRESS_08bbd577[513] = (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535; mål_ADDRESS_08bbd577[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)vare_COUNT;
}
maskin_Word 도구전문접속번호(maskin_Word fil_handtak) {
    struct 자바주소 첫째값; unsigned lengd_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fil_handtak, (maskin_Word)&첫째값, (maskin_Word)&lengd_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535);
}
maskin_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
maskin_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
maskin_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
maskin_Word verktøy_grafikk_vent(void) { return (uint32_t)화면키기다리기(); }
maskin_Word 도구사각형(maskin_Word x_koordinat, maskin_Word Y_koordinat, maskin_Word 너비값, maskin_Word 높이값, maskin_Word 색상) {
    return (uint32_t)사용자호출(13, x_koordinat, Y_koordinat, 색상, 너비값, 높이값, 0);
}

maskin_Word verktøy_Stream(maskin_Word Handling,maskin_Word fil_handtak,maskin_Word VALUE){
    if(Handling==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(VALUE);
    if(Handling==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,fil_handtak,(maskin_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fil_handtak,4,0));}
    if(Handling==2)return (uint32_t)호출(37,fil_handtak,(maskin_Word)&첫째값,sizeof(첫째값));
    if(Handling==3)return (uint32_t)호출(39,fil_handtak,0,0);
    if(Handling==4)return 도구전문접속번호(fil_handtak);
    if(Handling==5)return (uint32_t)호출(40,fil_handtak,0,0);
    return (uint32_t)-22;
}
maskin_Word verktøy_GUI(maskin_Word Handling,maskin_Word identifikator_VALUE,maskin_Word 첫째값,maskin_Word SECOND_VALUE,maskin_Word teiknkode,maskin_Word mål_data){return (uint32_t)사용자호출(20,Handling,identifikator_VALUE,첫째값,SECOND_VALUE,teiknkode,mål_data);}
maskin_Word verktøy_GUI_SMS(maskin_Word identifikator_VALUE,maskin_Word ARRAY_VALUE,maskin_Word vare_COUNT){
    const maskin_Word *원본주소=(const maskin_Word *)ARRAY_VALUE;uint32_t data[127];unsigned oppføring_COUNT=0;
    if(vare_COUNT>원본주소[0])return (uint32_t)-22;
    for(maskin_Word 순번=0;순번<vare_COUNT;순번++){unsigned teikn_koding=원본주소[순번+1];if(teikn_koding>=0xd800&&teikn_koding<=0xdbff&&순번+1<vare_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;teikn_koding=0x10000+((teikn_koding-0xd800)<<10)+낮은값-0xdc00;}if(oppføring_COUNT==127)return (uint32_t)-22;data[oppføring_COUNT++]=teikn_koding;}
    return (uint32_t)사용자호출(21,identifikator_VALUE,(maskin_Word)data,oppføring_COUNT,0,0,0);
}
