#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 bestand/tekstuitvoer/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bundel.h"
typedef uintptr_t machine_Word;
static int gebied_WAARDE;
static int 꾸러미사용중, 꾸러미인수이동;
static machine_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned item_AANTAL, machine_Word 첫째값, machine_Word SECONDE_WAARDE, machine_Word codepoint) {
    return 사용자호출(item_AANTAL, 첫째값, SECONDE_WAARDE, codepoint, 0, 0, 0);
}
static void 바이트들(const char *gegevens_functie, size_t item_AANTAL) { 호출(1, 1, (machine_Word)gegevens_functie, item_AANTAL); }
static void teken(unsigned codepoint) {
    unsigned char gegevens[4]; unsigned item_AANTAL = 0;
    if (codepoint < 128) gegevens[item_AANTAL++] = codepoint;
    else if (codepoint < 2048) { gegevens[item_AANTAL++] = 0xc0 | (codepoint >> 6); gegevens[item_AANTAL++] = 0x80 | (codepoint & 63); }
    else if (codepoint < 65536) { gegevens[item_AANTAL++] = 0xe0 | (codepoint >> 12); gegevens[item_AANTAL++] = 0x80 | ((codepoint >> 6) & 63); gegevens[item_AANTAL++] = 0x80 | (codepoint & 63); }
    else { gegevens[item_AANTAL++] = 0xf0 | (codepoint >> 18); gegevens[item_AANTAL++] = 0x80 | ((codepoint >> 12) & 63); gegevens[item_AANTAL++] = 0x80 | ((codepoint >> 6) & 63); gegevens[item_AANTAL++] = 0x80 | (codepoint & 63); }
    바이트들((const char *)gegevens, item_AANTAL);
}
machine_Word hulpmiddel_teken(machine_Word WAARDE) {
    unsigned codepoint = WAARDE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (codepoint >= 0xdc00 && codepoint <= 0xdfff) { teken(0x10000 + ((높은부분 - 0xd800) << 10) + codepoint - 0xdc00); return 1; }
        teken(0xfffd);
    }
    if (codepoint >= 0xd800 && codepoint <= 0xdbff) 대기중짝글자 = codepoint;
    else teken(codepoint > 0x10ffff || (codepoint >= 0xdc00 && codepoint <= 0xdfff) ? 0xfffd : codepoint);
    return 1;
}
machine_Word hulpmiddel_afdrukken(machine_Word WAARDE) {
    const machine_Word *tekenreeks_gegevens = (const machine_Word *)WAARDE;
    for (machine_Word 순번 = 0; 순번 < tekenreeks_gegevens[0]; 순번++) hulpmiddel_teken(tekenreeks_gegevens[순번 + 1]);
    return tekenreeks_gegevens[0];
}
static int pad(machine_Word object_verwijzen, char HR_gegevens[512]) {
    const machine_Word *첫째값 = (const machine_Word *)object_verwijzen;
    unsigned 사용량 = 0;
    for (machine_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned codepoint = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] methode_MODUS 경로와 호환한다.
        if (codepoint >= 0xd800 && codepoint <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; codepoint = 0x10000 + ((codepoint - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (codepoint >= 0xd800 && codepoint <= 0xdfff) return -22;
        unsigned item_AANTAL = codepoint < 128 ? 1 : codepoint < 2048 ? 2 : codepoint < 65536 ? 3 : 4;
        if (사용량 + item_AANTAL > 511) return -36;
        if (item_AANTAL == 1) HR_gegevens[사용량++] = codepoint;
        else {
            HR_gegevens[사용량++] = (item_AANTAL == 2 ? 0xc0 : item_AANTAL == 3 ? 0xe0 : 0xf0) | (codepoint >> (6 * (item_AANTAL - 1)));
            for (unsigned 안쪽순번 = item_AANTAL - 1; 안쪽순번; 안쪽순번--) HR_gegevens[사용량++] = 0x80 | ((codepoint >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    HR_gegevens[사용량] = 0; return 사용량 ? 0 : -22;
}
machine_Word hulpmiddel_open(machine_Word Naam, machine_Word configuratie_BITS) {
    char gegevens_functie[512]; int fout = pad(Naam, gegevens_functie);
    return (uint32_t)(fout ? fout : 호출(3, (machine_Word)gegevens_functie, configuratie_BITS, 0));
}
machine_Word hulpmiddel_Sluiten(machine_Word bestandsingang) { return (uint32_t)호출(4, bestandsingang, 0, 0); }
machine_Word 도구바이트읽기(machine_Word bestandsingang) {
    unsigned char SECONDE_WAARDE; intptr_t item_AANTAL = 호출(2, bestandsingang, (machine_Word)&SECONDE_WAARDE, 1);
    return (uint32_t)(item_AANTAL == 1 ? SECONDE_WAARDE : item_AANTAL == 0 ? 256 : item_AANTAL);
}
machine_Word hulpmiddel_schrijven_byte(machine_Word bestandsingang, machine_Word WAARDE) {
    unsigned char SECONDE_WAARDE = WAARDE; return (uint32_t)호출(1, bestandsingang, (machine_Word)&SECONDE_WAARDE, 1);
}
machine_Word 도구읽기(machine_Word Naam, machine_Word doel_gegevens_ADRES) {
    if (꾸러미사용중) {
        char gegevens_functie[512]; int fout = pad(Naam, gegevens_functie); if (fout) return (uint32_t)fout;
        unsigned item_AANTAL = 0; while (gegevens_functie[item_AANTAL]) item_AANTAL++;
        if (item_AANTAL >= 6) for (unsigned 순번 = 0; 순번 < item_AANTAL - 6; 순번++) if (gegevens_functie[순번] == '.') gegevens_functie[순번] = '/';
        unsigned char 바이트들[16384]; machine_Word *doel_WAARDE_functie = (machine_Word *)doel_gegevens_ADRES;
        int OPBRENGST_AANTAL = 꾸러미읽기(gegevens_functie, 바이트들, doel_WAARDE_functie[0] < sizeof(바이트들) ? doel_WAARDE_functie[0] : sizeof(바이트들));
        if (OPBRENGST_AANTAL >= 0) { for (int 순번 = 0; 순번 < OPBRENGST_AANTAL; 순번++) doel_WAARDE_functie[순번 + 1] = 바이트들[순번]; return OPBRENGST_AANTAL; }
        if (OPBRENGST_AANTAL != -2) return (uint32_t)OPBRENGST_AANTAL;
    }
    int bestandsingang = 꾸러미사용중 ? -2 : (int32_t)hulpmiddel_open(Naam, 0);
    if (bestandsingang < 0) {
        char gegevens_functie[512]; int fout = pad(Naam, gegevens_functie); if (fout) return (uint32_t)fout;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Volgende_VERSCHUIVING = 자바클래스들[순번].Naam; unsigned 안쪽순번 = 0;
            while (gegevens_functie[안쪽순번] && gegevens_functie[안쪽순번] == Volgende_VERSCHUIVING[안쪽순번]) 안쪽순번++;
            if (gegevens_functie[안쪽순번] || Volgende_VERSCHUIVING[안쪽순번]) continue;
            machine_Word *doel_WAARDE_functie = (machine_Word *)doel_gegevens_ADRES;
            if (doel_WAARDE_functie[0] < 자바클래스들[순번].Grootte) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Grootte; 안쪽순번++) doel_WAARDE_functie[안쪽순번 + 1] = 자바클래스들[순번].gegevens[안쪽순번];
            return 자바클래스들[순번].Grootte;
        }
        return (uint32_t)bestandsingang;
    }
    machine_Word *첫째값 = (machine_Word *)doel_gegevens_ADRES;
    intptr_t Grootte = 호출(9, bestandsingang, 0, 0), Voltooid_aantal = 0;
    if (Grootte < 0 || (machine_Word)Grootte > 첫째값[0]) { hulpmiddel_Sluiten(bestandsingang); return (uint32_t)(Grootte < 0 ? Grootte : -27); }
    unsigned char gegevensblok[256];
    while (Voltooid_aantal < Grootte) {
        intptr_t item_AANTAL = 호출(2, bestandsingang, (machine_Word)gegevensblok, Grootte - Voltooid_aantal < 256 ? Grootte - Voltooid_aantal : 256);
        if (item_AANTAL <= 0) { hulpmiddel_Sluiten(bestandsingang); return (uint32_t)(item_AANTAL ? item_AANTAL : -5); }
        for (intptr_t 순번 = 0; 순번 < item_AANTAL; 순번++) 첫째값[1 + Voltooid_aantal + 순번] = gegevensblok[순번];
        Voltooid_aantal += item_AANTAL;
    }
    hulpmiddel_Sluiten(bestandsingang); return Voltooid_aantal;
}
machine_Word hulpmiddel_schrijven(machine_Word Naam, machine_Word 원본자료, machine_Word invoer_AANTAL_8f7753a1) {
    const machine_Word *첫째값 = (const machine_Word *)원본자료;
    if (invoer_AANTAL_8f7753a1 > 첫째값[0] || invoer_AANTAL_8f7753a1 > 16384) return (uint32_t)-27;
    int bestandsingang = (int32_t)hulpmiddel_open(Naam, 577); if (bestandsingang < 0) return (uint32_t)bestandsingang;
    unsigned char gegevensblok[256]; machine_Word Voltooid_aantal = 0;
    while (Voltooid_aantal < invoer_AANTAL_8f7753a1) {
        machine_Word item_AANTAL = invoer_AANTAL_8f7753a1 - Voltooid_aantal < 256 ? invoer_AANTAL_8f7753a1 - Voltooid_aantal : 256;
        for (machine_Word 순번 = 0; 순번 < item_AANTAL; 순번++) gegevensblok[순번] = 첫째값[1 + Voltooid_aantal + 순번];
        intptr_t resultaat = 호출(1, bestandsingang, (machine_Word)gegevensblok, item_AANTAL);
        if (resultaat <= 0) { hulpmiddel_Sluiten(bestandsingang); return (uint32_t)(resultaat ? resultaat : -5); }
        Voltooid_aantal += resultaat;
    }
    hulpmiddel_Sluiten(bestandsingang); return invoer_AANTAL_8f7753a1;
}
machine_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
machine_Word hulpmiddel_argument(machine_Word ZOEKEN_INDEX) {
    static const machine_Word leeg_WAARDE[1] = {0};
    if (ZOEKEN_INDEX >= 8) return (machine_Word)leeg_WAARDE;
    unsigned char invoer[256]; intptr_t item_AANTAL;
    if (꾸러미사용중 && ZOEKEN_INDEX == 0) { const char *gegevens_functie = 꾸러미진입클래스(); item_AANTAL = 0; while (gegevens_functie[item_AANTAL] && item_AANTAL < 255) { invoer[item_AANTAL] = gegevens_functie[item_AANTAL]; item_AANTAL++; } }
    else item_AANTAL = 호출(15, ZOEKEN_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (machine_Word)invoer, sizeof(invoer));
    if (item_AANTAL < 0) return (machine_Word)leeg_WAARDE;
    machine_Word *HR_gegevens = 전달인수[ZOEKEN_INDEX]; unsigned invoer_AANTAL_8f7753a1 = 0;
    for (intptr_t 순번 = 0; 순번 < item_AANTAL;) {
        unsigned codepoint = invoer[순번++], 더있음 = codepoint < 128 ? 0 : codepoint >= 0xc2 && codepoint < 0xe0 ? 1 : codepoint < 0xf0 && codepoint >= 0xe0 ? 2 : codepoint >= 0xf0 && codepoint <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > item_AANTAL) { HR_gegevens[++invoer_AANTAL_8f7753a1] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) codepoint &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (invoer[순번] & 0xc0) == 0x80) { codepoint = (codepoint << 6) | (invoer[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || codepoint < 최소값 || codepoint > 0x10ffff || (codepoint >= 0xd800 && codepoint <= 0xdfff)) codepoint = 0xfffd;
        if (codepoint >= 65536) { codepoint -= 65536; HR_gegevens[++invoer_AANTAL_8f7753a1] = 0xd800 | (codepoint >> 10); HR_gegevens[++invoer_AANTAL_8f7753a1] = 0xdc00 | (codepoint & 1023); }
        else HR_gegevens[++invoer_AANTAL_8f7753a1] = codepoint;
    }
    HR_gegevens[0] = invoer_AANTAL_8f7753a1; return (machine_Word)HR_gegevens;
}
machine_Word hulpmiddel_soort(void) { return gebied_WAARDE; }
void 커널중단(const char *kennisgeving_sms) {
    const char *gegevens_functie = kennisgeving_sms; while (*gegevens_functie) gegevens_functie++;
    바이트들("Java tool runtime error: ", 25); 바이트들(kennisgeving_sms, gegevens_functie - kennisgeving_sms); teken(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_gebruiker_app(int methode_MODUS) {
    gebied_WAARDE = methode_MODUS;
    unsigned char 첫항목[256]; intptr_t item_AANTAL = 호출(15, 0, (machine_Word)첫항목, sizeof(첫항목));
    if (methode_MODUS == 2 || (methode_MODUS == 1 && item_AANTAL == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = methode_MODUS == 2 ? 0 : 1;
        char Bestand_invoer_naam[256]; intptr_t tijdsduur_gegevens = 호출(15, 꾸러미인수이동, (machine_Word)Bestand_invoer_naam, sizeof(Bestand_invoer_naam));
        if (tijdsduur_gegevens <= 0 || 꾸러미열기(Bestand_invoer_naam) < 0) {
            static const char fout[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(fout, sizeof(fout) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int resultaat = 자바진입();
    if (대기중짝글자) teken(0xfffd);
    return resultaat;
}

// UDP는 Eigen 커널의 SVC를 통과하며 actueel_item 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Gezin, poortnummer; uint32_t ADRES; unsigned char nulwaarde[8]; };
static struct 자바주소 UDP_ADRES(unsigned poortnummer) {
    struct 자바주소 첫째값 = {2, (uint16_t)((poortnummer << 8) | (poortnummer >> 8)), 0x0100007f, {0}}; return 첫째값;
}
machine_Word hulpmiddel_UDP_open(machine_Word poortnummer) {
    intptr_t bestandsingang = 호출(32, 2, 2, 17); if (bestandsingang < 0) return (uint32_t)bestandsingang;
    struct 자바주소 첫째값 = UDP_ADRES(poortnummer);
    첫째값.ADRES = 0;
    intptr_t Status_WAARDE = 호출(33, bestandsingang, (machine_Word)&첫째값, sizeof(첫째값));
    if (Status_WAARDE < 0) { hulpmiddel_Sluiten(bestandsingang); return (uint32_t)Status_WAARDE; }
    return bestandsingang;
}
machine_Word hulpmiddel_UDP_e_mailen(machine_Word bestandsingang, machine_Word poortnummer, machine_Word MATRIX_WAARDE, machine_Word tijdsduur_WAARDE) {
    const machine_Word *원본주소 = (const machine_Word *)MATRIX_WAARDE; unsigned char gegevens[512];
    if (tijdsduur_WAARDE > 512 || tijdsduur_WAARDE > 원본주소[0]) return (uint32_t)-90;
    for (machine_Word 순번 = 0; 순번 < tijdsduur_WAARDE; 순번++) gegevens[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRES(poortnummer);
    return (uint32_t)사용자호출(34, bestandsingang, (machine_Word)gegevens, tijdsduur_WAARDE, 0, (machine_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t item_AANTAL) { return (item_AANTAL>>24)|((item_AANTAL>>8)&0xff00)|((item_AANTAL<<8)&0xff0000)|(item_AANTAL<<24); }
machine_Word hulpmiddel_UDP_e_mailen_ADRES(machine_Word bestandsingang, machine_Word ADRES, machine_Word poortnummer, machine_Word MATRIX_WAARDE, machine_Word tijdsduur_WAARDE) {
    const machine_Word *원본주소 = (const machine_Word *)MATRIX_WAARDE; unsigned char gegevens[512];
    if (tijdsduur_WAARDE > 512 || tijdsduur_WAARDE > 원본주소[0]) return (uint32_t)-90;
    for (machine_Word 순번 = 0; 순번 < tijdsduur_WAARDE; 순번++) gegevens[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRES(poortnummer); 첫째값.ADRES = 바이트순서뒤집기(ADRES);
    return (uint32_t)사용자호출(34, bestandsingang, (machine_Word)gegevens, tijdsduur_WAARDE, 0, (machine_Word)&첫째값, sizeof(첫째값));
}
machine_Word hulpmiddel_VERBINDEN(machine_Word bestandsingang, machine_Word ADRES, machine_Word poortnummer) {
    struct 자바주소 첫째값 = UDP_ADRES(poortnummer); 첫째값.ADRES = 바이트순서뒤집기(ADRES);
    uint32_t starten = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t resultaat = 호출(37, bestandsingang, (machine_Word)&첫째값, sizeof(첫째값));
        if (resultaat != -115) return (uint32_t)resultaat;
        if ((uint32_t)(호출(7, 0, 0, 0) - starten) >= 1000) return (uint32_t)-110;
    }
}
machine_Word 도구전문받기(machine_Word bestandsingang, machine_Word MATRIX_WAARDE, machine_Word buffer_capaciteit) {
    machine_Word *doel_ADRES_08bbd577 = (machine_Word *)MATRIX_WAARDE; unsigned char gegevens[512];
    if (buffer_capaciteit > 512 || doel_ADRES_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned tijdsduur_gegevens = sizeof(첫째값);
    intptr_t item_AANTAL = 사용자호출(35, bestandsingang, (machine_Word)gegevens, buffer_capaciteit, 0, (machine_Word)&첫째값, (machine_Word)&tijdsduur_gegevens);
    if (item_AANTAL >= 0) { for (intptr_t 순번 = 0; 순번 < item_AANTAL; 순번++) doel_ADRES_08bbd577[순번 + 1] = gegevens[순번]; doel_ADRES_08bbd577[513] = (첫째값.poortnummer << 8 | 첫째값.poortnummer >> 8) & 65535; doel_ADRES_08bbd577[514] = 바이트순서뒤집기(첫째값.ADRES); }
    return (uint32_t)item_AANTAL;
}
machine_Word hulpmiddel_UDP_poort(machine_Word bestandsingang) {
    struct 자바주소 첫째값; unsigned tijdsduur_gegevens = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, bestandsingang, (machine_Word)&첫째값, (machine_Word)&tijdsduur_gegevens);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.poortnummer << 8 | 첫째값.poortnummer >> 8) & 65535);
}
machine_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
machine_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
machine_Word hulpmiddel_scherm_hoogte(void) { return (uint32_t)화면높이읽기(); }
machine_Word hulpmiddel_graphics_wachten(void) { return (uint32_t)화면키기다리기(); }
machine_Word hulpmiddel_rechthoek(machine_Word x_coördinaat, machine_Word Y_coördinaat, machine_Word 너비값, machine_Word aangevraagd_hoogte_WAARDE, machine_Word 색상) {
    return (uint32_t)사용자호출(13, x_coördinaat, Y_coördinaat, 색상, 너비값, aangevraagd_hoogte_WAARDE, 0);
}

machine_Word hulpmiddel_Stream(machine_Word Actie,machine_Word bestandsingang,machine_Word WAARDE){
    if(Actie==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADRES(WAARDE);
    if(Actie==1){첫째값.ADRES=0;intptr_t 반환값=호출(33,bestandsingang,(machine_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,bestandsingang,4,0));}
    if(Actie==2)return (uint32_t)호출(37,bestandsingang,(machine_Word)&첫째값,sizeof(첫째값));
    if(Actie==3)return (uint32_t)호출(39,bestandsingang,0,0);
    if(Actie==4)return hulpmiddel_UDP_poort(bestandsingang);
    if(Actie==5)return (uint32_t)호출(40,bestandsingang,0,0);
    return (uint32_t)-22;
}
machine_Word hulpmiddel_GUI(machine_Word Actie,machine_Word id_WAARDE,machine_Word 첫째값,machine_Word SECONDE_WAARDE,machine_Word codepoint,machine_Word doel_gegevens){return (uint32_t)사용자호출(20,Actie,id_WAARDE,첫째값,SECONDE_WAARDE,codepoint,doel_gegevens);}
machine_Word hulpmiddel_GUI_sms(machine_Word id_WAARDE,machine_Word MATRIX_WAARDE,machine_Word item_AANTAL){
    const machine_Word *원본주소=(const machine_Word *)MATRIX_WAARDE;uint32_t gegevens[127];unsigned invoer_AANTAL_8f7753a1=0;
    if(item_AANTAL>원본주소[0])return (uint32_t)-22;
    for(machine_Word 순번=0;순번<item_AANTAL;순번++){unsigned tekencodering=원본주소[순번+1];if(tekencodering>=0xd800&&tekencodering<=0xdbff&&순번+1<item_AANTAL){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;tekencodering=0x10000+((tekencodering-0xd800)<<10)+낮은값-0xdc00;}if(invoer_AANTAL_8f7753a1==127)return (uint32_t)-22;gegevens[invoer_AANTAL_8f7753a1++]=tekencodering;}
    return (uint32_t)사용자호출(21,id_WAARDE,(machine_Word)gegevens,invoer_AANTAL_8f7753a1,0,0,0);
}
