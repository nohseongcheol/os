#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 filnamn/utmatningsposition/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bunt.h"
typedef uintptr_t dator_Ord;
static int område_värde;
static int 꾸러미사용중, 꾸러미인수이동;
static dator_Ord 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned objekt_ANTAL, dator_Ord 첫째값, dator_Ord SEKUND_värde, dator_Ord kodpunkt) {
    return 사용자호출(objekt_ANTAL, 첫째값, SEKUND_värde, kodpunkt, 0, 0, 0);
}
static void 바이트들(const char *data_placera, size_t objekt_ANTAL) { 호출(1, 1, (dator_Ord)data_placera, objekt_ANTAL); }
static void tecken(unsigned kodpunkt) {
    unsigned char data[4]; unsigned objekt_ANTAL = 0;
    if (kodpunkt < 128) data[objekt_ANTAL++] = kodpunkt;
    else if (kodpunkt < 2048) { data[objekt_ANTAL++] = 0xc0 | (kodpunkt >> 6); data[objekt_ANTAL++] = 0x80 | (kodpunkt & 63); }
    else if (kodpunkt < 65536) { data[objekt_ANTAL++] = 0xe0 | (kodpunkt >> 12); data[objekt_ANTAL++] = 0x80 | ((kodpunkt >> 6) & 63); data[objekt_ANTAL++] = 0x80 | (kodpunkt & 63); }
    else { data[objekt_ANTAL++] = 0xf0 | (kodpunkt >> 18); data[objekt_ANTAL++] = 0x80 | ((kodpunkt >> 12) & 63); data[objekt_ANTAL++] = 0x80 | ((kodpunkt >> 6) & 63); data[objekt_ANTAL++] = 0x80 | (kodpunkt & 63); }
    바이트들((const char *)data, objekt_ANTAL);
}
dator_Ord verktyg_tecken(dator_Ord värde) {
    unsigned kodpunkt = värde;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kodpunkt >= 0xdc00 && kodpunkt <= 0xdfff) { tecken(0x10000 + ((높은부분 - 0xd800) << 10) + kodpunkt - 0xdc00); return 1; }
        tecken(0xfffd);
    }
    if (kodpunkt >= 0xd800 && kodpunkt <= 0xdbff) 대기중짝글자 = kodpunkt;
    else tecken(kodpunkt > 0x10ffff || (kodpunkt >= 0xdc00 && kodpunkt <= 0xdfff) ? 0xfffd : kodpunkt);
    return 1;
}
dator_Ord verktyg_skriva_ut(dator_Ord värde) {
    const dator_Ord *sträng_data = (const dator_Ord *)värde;
    for (dator_Ord 순번 = 0; 순번 < sträng_data[0]; 순번++) verktyg_tecken(sträng_data[순번 + 1]);
    return sträng_data[0];
}
static int sökväg_2(dator_Ord objekt_referens, char KR_data[512]) {
    const dator_Ord *첫째값 = (const dator_Ord *)objekt_referens;
    unsigned 사용량 = 0;
    for (dator_Ord 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kodpunkt = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metod_läge 경로와 호환한다.
        if (kodpunkt >= 0xd800 && kodpunkt <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kodpunkt = 0x10000 + ((kodpunkt - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kodpunkt >= 0xd800 && kodpunkt <= 0xdfff) return -22;
        unsigned objekt_ANTAL = kodpunkt < 128 ? 1 : kodpunkt < 2048 ? 2 : kodpunkt < 65536 ? 3 : 4;
        if (사용량 + objekt_ANTAL > 511) return -36;
        if (objekt_ANTAL == 1) KR_data[사용량++] = kodpunkt;
        else {
            KR_data[사용량++] = (objekt_ANTAL == 2 ? 0xc0 : objekt_ANTAL == 3 ? 0xe0 : 0xf0) | (kodpunkt >> (6 * (objekt_ANTAL - 1)));
            for (unsigned 안쪽순번 = objekt_ANTAL - 1; 안쪽순번; 안쪽순번--) KR_data[사용량++] = 0x80 | ((kodpunkt >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_data[사용량] = 0; return 사용량 ? 0 : -22;
}
dator_Ord verktyg_skapa(dator_Ord Namn, dator_Ord konfiguration_BITS) {
    char data_placera[512]; int fel = sökväg_2(Namn, data_placera);
    return (uint32_t)(fel ? fel : 호출(3, (dator_Ord)data_placera, konfiguration_BITS, 0));
}
dator_Ord verktyg_Stäng(dator_Ord filreferens) { return (uint32_t)호출(4, filreferens, 0, 0); }
dator_Ord verktyg_läsa_byte(dator_Ord filreferens) {
    unsigned char SEKUND_värde; intptr_t objekt_ANTAL = 호출(2, filreferens, (dator_Ord)&SEKUND_värde, 1);
    return (uint32_t)(objekt_ANTAL == 1 ? SEKUND_värde : objekt_ANTAL == 0 ? 256 : objekt_ANTAL);
}
dator_Ord verktyg_skriva_byte(dator_Ord filreferens, dator_Ord värde) {
    unsigned char SEKUND_värde = värde; return (uint32_t)호출(1, filreferens, (dator_Ord)&SEKUND_värde, 1);
}
dator_Ord verktyg_läsa(dator_Ord Namn, dator_Ord mål_data_ADRESS) {
    if (꾸러미사용중) {
        char data_placera[512]; int fel = sökväg_2(Namn, data_placera); if (fel) return (uint32_t)fel;
        unsigned objekt_ANTAL = 0; while (data_placera[objekt_ANTAL]) objekt_ANTAL++;
        if (objekt_ANTAL >= 6) for (unsigned 순번 = 0; 순번 < objekt_ANTAL - 6; 순번++) if (data_placera[순번] == '.') data_placera[순번] = '/';
        unsigned char 바이트들[16384]; dator_Ord *mål_värde_placera = (dator_Ord *)mål_data_ADRESS;
        int BELOPP_ANTAL = 꾸러미읽기(data_placera, 바이트들, mål_värde_placera[0] < sizeof(바이트들) ? mål_värde_placera[0] : sizeof(바이트들));
        if (BELOPP_ANTAL >= 0) { for (int 순번 = 0; 순번 < BELOPP_ANTAL; 순번++) mål_värde_placera[순번 + 1] = 바이트들[순번]; return BELOPP_ANTAL; }
        if (BELOPP_ANTAL != -2) return (uint32_t)BELOPP_ANTAL;
    }
    int filreferens = 꾸러미사용중 ? -2 : (int32_t)verktyg_skapa(Namn, 0);
    if (filreferens < 0) {
        char data_placera[512]; int fel = sökväg_2(Namn, data_placera); if (fel) return (uint32_t)fel;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Nästa_FÖRSKJUTNING = 자바클래스들[순번].Namn; unsigned 안쪽순번 = 0;
            while (data_placera[안쪽순번] && data_placera[안쪽순번] == Nästa_FÖRSKJUTNING[안쪽순번]) 안쪽순번++;
            if (data_placera[안쪽순번] || Nästa_FÖRSKJUTNING[안쪽순번]) continue;
            dator_Ord *mål_värde_placera = (dator_Ord *)mål_data_ADRESS;
            if (mål_värde_placera[0] < 자바클래스들[순번].Storlek) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Storlek; 안쪽순번++) mål_värde_placera[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Storlek;
        }
        return (uint32_t)filreferens;
    }
    dator_Ord *첫째값 = (dator_Ord *)mål_data_ADRESS;
    intptr_t Storlek = 호출(9, filreferens, 0, 0), Slutfört_belopp = 0;
    if (Storlek < 0 || (dator_Ord)Storlek > 첫째값[0]) { verktyg_Stäng(filreferens); return (uint32_t)(Storlek < 0 ? Storlek : -27); }
    unsigned char datablock[256];
    while (Slutfört_belopp < Storlek) {
        intptr_t objekt_ANTAL = 호출(2, filreferens, (dator_Ord)datablock, Storlek - Slutfört_belopp < 256 ? Storlek - Slutfört_belopp : 256);
        if (objekt_ANTAL <= 0) { verktyg_Stäng(filreferens); return (uint32_t)(objekt_ANTAL ? objekt_ANTAL : -5); }
        for (intptr_t 순번 = 0; 순번 < objekt_ANTAL; 순번++) 첫째값[1 + Slutfört_belopp + 순번] = datablock[순번];
        Slutfört_belopp += objekt_ANTAL;
    }
    verktyg_Stäng(filreferens); return Slutfört_belopp;
}
dator_Ord verktyg_skriva(dator_Ord Namn, dator_Ord 원본자료, dator_Ord post_ANTAL) {
    const dator_Ord *첫째값 = (const dator_Ord *)원본자료;
    if (post_ANTAL > 첫째값[0] || post_ANTAL > 16384) return (uint32_t)-27;
    int filreferens = (int32_t)verktyg_skapa(Namn, 577); if (filreferens < 0) return (uint32_t)filreferens;
    unsigned char datablock[256]; dator_Ord Slutfört_belopp = 0;
    while (Slutfört_belopp < post_ANTAL) {
        dator_Ord objekt_ANTAL = post_ANTAL - Slutfört_belopp < 256 ? post_ANTAL - Slutfört_belopp : 256;
        for (dator_Ord 순번 = 0; 순번 < objekt_ANTAL; 순번++) datablock[순번] = 첫째값[1 + Slutfört_belopp + 순번];
        intptr_t RESULTAT = 호출(1, filreferens, (dator_Ord)datablock, objekt_ANTAL);
        if (RESULTAT <= 0) { verktyg_Stäng(filreferens); return (uint32_t)(RESULTAT ? RESULTAT : -5); }
        Slutfört_belopp += RESULTAT;
    }
    verktyg_Stäng(filreferens); return post_ANTAL;
}
dator_Ord 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
dator_Ord verktyg_argument(dator_Ord LETAUPP_INDEX) {
    static const dator_Ord 빈값[1] = {0};
    if (LETAUPP_INDEX >= 8) return (dator_Ord)빈값;
    unsigned char indata[256]; intptr_t objekt_ANTAL;
    if (꾸러미사용중 && LETAUPP_INDEX == 0) { const char *data_placera = 꾸러미진입클래스(); objekt_ANTAL = 0; while (data_placera[objekt_ANTAL] && objekt_ANTAL < 255) { indata[objekt_ANTAL] = data_placera[objekt_ANTAL]; objekt_ANTAL++; } }
    else objekt_ANTAL = 호출(15, LETAUPP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (dator_Ord)indata, sizeof(indata));
    if (objekt_ANTAL < 0) return (dator_Ord)빈값;
    dator_Ord *KR_data = 전달인수[LETAUPP_INDEX]; unsigned post_ANTAL = 0;
    for (intptr_t 순번 = 0; 순번 < objekt_ANTAL;) {
        unsigned kodpunkt = indata[순번++], 더있음 = kodpunkt < 128 ? 0 : kodpunkt >= 0xc2 && kodpunkt < 0xe0 ? 1 : kodpunkt < 0xf0 && kodpunkt >= 0xe0 ? 2 : kodpunkt >= 0xf0 && kodpunkt <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > objekt_ANTAL) { KR_data[++post_ANTAL] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kodpunkt &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (indata[순번] & 0xc0) == 0x80) { kodpunkt = (kodpunkt << 6) | (indata[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kodpunkt < 최소값 || kodpunkt > 0x10ffff || (kodpunkt >= 0xd800 && kodpunkt <= 0xdfff)) kodpunkt = 0xfffd;
        if (kodpunkt >= 65536) { kodpunkt -= 65536; KR_data[++post_ANTAL] = 0xd800 | (kodpunkt >> 10); KR_data[++post_ANTAL] = 0xdc00 | (kodpunkt & 1023); }
        else KR_data[++post_ANTAL] = kodpunkt;
    }
    KR_data[0] = post_ANTAL; return (dator_Ord)KR_data;
}
dator_Ord verktyg_variant(void) { return område_värde; }
void 커널중단(const char *알림문) {
    const char *data_placera = 알림문; while (*data_placera) data_placera++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_placera - 알림문); tecken(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_användare_app(int metod_läge) {
    område_värde = metod_läge;
    unsigned char 첫항목[256]; intptr_t objekt_ANTAL = 호출(15, 0, (dator_Ord)첫항목, sizeof(첫항목));
    if (metod_läge == 2 || (metod_läge == 1 && objekt_ANTAL == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metod_läge == 2 ? 0 : 1;
        char fil_post_namn[256]; intptr_t längd_data = 호출(15, 꾸러미인수이동, (dator_Ord)fil_post_namn, sizeof(fil_post_namn));
        if (längd_data <= 0 || 꾸러미열기(fil_post_namn) < 0) {
            static const char fel[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(fel, sizeof(fel) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int RESULTAT = 자바진입();
    if (대기중짝글자) tecken(0xfffd);
    return RESULTAT;
}

// UDP는 eget 커널의 SVC를 통과하며 aktuellt_objekt 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t serie, portnummer; uint32_t Adress; unsigned char nollvärde[8]; };
static struct 자바주소 UDP_ADRESS(unsigned portnummer) {
    struct 자바주소 첫째값 = {2, (uint16_t)((portnummer << 8) | (portnummer >> 8)), 0x0100007f, {0}}; return 첫째값;
}
dator_Ord verktyg_UDP_skapa(dator_Ord portnummer) {
    intptr_t filreferens = 호출(32, 2, 2, 17); if (filreferens < 0) return (uint32_t)filreferens;
    struct 자바주소 첫째값 = UDP_ADRESS(portnummer);
    첫째값.Adress = 0;
    intptr_t status_värde = 호출(33, filreferens, (dator_Ord)&첫째값, sizeof(첫째값));
    if (status_värde < 0) { verktyg_Stäng(filreferens); return (uint32_t)status_värde; }
    return filreferens;
}
dator_Ord verktyg_UDP_skicka(dator_Ord filreferens, dator_Ord portnummer, dator_Ord MATRIS_värde, dator_Ord längd_värde) {
    const dator_Ord *원본주소 = (const dator_Ord *)MATRIS_värde; unsigned char data[512];
    if (längd_värde > 512 || längd_värde > 원본주소[0]) return (uint32_t)-90;
    for (dator_Ord 순번 = 0; 순번 < längd_värde; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRESS(portnummer);
    return (uint32_t)사용자호출(34, filreferens, (dator_Ord)data, längd_värde, 0, (dator_Ord)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t objekt_ANTAL) { return (objekt_ANTAL>>24)|((objekt_ANTAL>>8)&0xff00)|((objekt_ANTAL<<8)&0xff0000)|(objekt_ANTAL<<24); }
dator_Ord verktyg_UDP_skicka_ADRESS(dator_Ord filreferens, dator_Ord Adress, dator_Ord portnummer, dator_Ord MATRIS_värde, dator_Ord längd_värde) {
    const dator_Ord *원본주소 = (const dator_Ord *)MATRIS_värde; unsigned char data[512];
    if (längd_värde > 512 || längd_värde > 원본주소[0]) return (uint32_t)-90;
    for (dator_Ord 순번 = 0; 순번 < längd_värde; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRESS(portnummer); 첫째값.Adress = 바이트순서뒤집기(Adress);
    return (uint32_t)사용자호출(34, filreferens, (dator_Ord)data, längd_värde, 0, (dator_Ord)&첫째값, sizeof(첫째값));
}
dator_Ord verktyg_ANSLUT(dator_Ord filreferens, dator_Ord Adress, dator_Ord portnummer) {
    struct 자바주소 첫째값 = UDP_ADRESS(portnummer); 첫째값.Adress = 바이트순서뒤집기(Adress);
    uint32_t Kör = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t RESULTAT = 호출(37, filreferens, (dator_Ord)&첫째값, sizeof(첫째값));
        if (RESULTAT != -115) return (uint32_t)RESULTAT;
        if ((uint32_t)(호출(7, 0, 0, 0) - Kör) >= 1000) return (uint32_t)-110;
    }
}
dator_Ord 도구전문받기(dator_Ord filreferens, dator_Ord MATRIS_värde, dator_Ord buffra_kapacitet) {
    dator_Ord *mål_ADRESS_08bbd577 = (dator_Ord *)MATRIS_värde; unsigned char data[512];
    if (buffra_kapacitet > 512 || mål_ADRESS_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned längd_data = sizeof(첫째값);
    intptr_t objekt_ANTAL = 사용자호출(35, filreferens, (dator_Ord)data, buffra_kapacitet, 0, (dator_Ord)&첫째값, (dator_Ord)&längd_data);
    if (objekt_ANTAL >= 0) { for (intptr_t 순번 = 0; 순번 < objekt_ANTAL; 순번++) mål_ADRESS_08bbd577[순번 + 1] = data[순번]; mål_ADRESS_08bbd577[513] = (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535; mål_ADRESS_08bbd577[514] = 바이트순서뒤집기(첫째값.Adress); }
    return (uint32_t)objekt_ANTAL;
}
dator_Ord verktyg_UDP_port(dator_Ord filreferens) {
    struct 자바주소 첫째값; unsigned längd_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, filreferens, (dator_Ord)&첫째값, (dator_Ord)&längd_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535);
}
dator_Ord 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
dator_Ord 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
dator_Ord 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
dator_Ord verktyg_grafik_vänta(void) { return (uint32_t)화면키기다리기(); }
dator_Ord verktyg_rektangel(dator_Ord x_koordinat, dator_Ord Y_koordinat, dator_Ord 너비값, dator_Ord 높이값, dator_Ord 색상) {
    return (uint32_t)사용자호출(13, x_koordinat, Y_koordinat, 색상, 너비값, 높이값, 0);
}

dator_Ord verktyg_flöde(dator_Ord Åtgärd,dator_Ord filreferens,dator_Ord värde){
    if(Åtgärd==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADRESS(värde);
    if(Åtgärd==1){첫째값.Adress=0;intptr_t 반환값=호출(33,filreferens,(dator_Ord)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,filreferens,4,0));}
    if(Åtgärd==2)return (uint32_t)호출(37,filreferens,(dator_Ord)&첫째값,sizeof(첫째값));
    if(Åtgärd==3)return (uint32_t)호출(39,filreferens,0,0);
    if(Åtgärd==4)return verktyg_UDP_port(filreferens);
    if(Åtgärd==5)return (uint32_t)호출(40,filreferens,0,0);
    return (uint32_t)-22;
}
dator_Ord verktyg_GUI(dator_Ord Åtgärd,dator_Ord identifierare_värde,dator_Ord 첫째값,dator_Ord SEKUND_värde,dator_Ord kodpunkt,dator_Ord mål_data){return (uint32_t)사용자호출(20,Åtgärd,identifierare_värde,첫째값,SEKUND_värde,kodpunkt,mål_data);}
dator_Ord verktyg_GUI_SMS(dator_Ord identifierare_värde,dator_Ord MATRIS_värde,dator_Ord objekt_ANTAL){
    const dator_Ord *원본주소=(const dator_Ord *)MATRIS_värde;uint32_t data[127];unsigned post_ANTAL=0;
    if(objekt_ANTAL>원본주소[0])return (uint32_t)-22;
    for(dator_Ord 순번=0;순번<objekt_ANTAL;순번++){unsigned teckenkodning=원본주소[순번+1];if(teckenkodning>=0xd800&&teckenkodning<=0xdbff&&순번+1<objekt_ANTAL){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;teckenkodning=0x10000+((teckenkodning-0xd800)<<10)+낮은값-0xdc00;}if(post_ANTAL==127)return (uint32_t)-22;data[post_ANTAL++]=teckenkodning;}
    return (uint32_t)사용자호출(21,identifierare_värde,(dator_Ord)data,post_ANTAL,0,0,0);
}
