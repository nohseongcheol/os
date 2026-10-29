#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fil/Utgang/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bunt.h"
typedef uintptr_t maskin_ord;
static int område_VERDI;
static int 꾸러미사용중, 꾸러미인수이동;
static maskin_ord 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned vare_ANTALL, maskin_ord 첫째값, maskin_ord SEKUND_VERDI, maskin_ord tegnkode) {
    return 사용자호출(vare_ANTALL, 첫째값, SEKUND_VERDI, tegnkode, 0, 0, 0);
}
static void 바이트들(const char *data_plassere, size_t vare_ANTALL) { 호출(1, 1, (maskin_ord)data_plassere, vare_ANTALL); }
static void tegn(unsigned tegnkode) {
    unsigned char data[4]; unsigned vare_ANTALL = 0;
    if (tegnkode < 128) data[vare_ANTALL++] = tegnkode;
    else if (tegnkode < 2048) { data[vare_ANTALL++] = 0xc0 | (tegnkode >> 6); data[vare_ANTALL++] = 0x80 | (tegnkode & 63); }
    else if (tegnkode < 65536) { data[vare_ANTALL++] = 0xe0 | (tegnkode >> 12); data[vare_ANTALL++] = 0x80 | ((tegnkode >> 6) & 63); data[vare_ANTALL++] = 0x80 | (tegnkode & 63); }
    else { data[vare_ANTALL++] = 0xf0 | (tegnkode >> 18); data[vare_ANTALL++] = 0x80 | ((tegnkode >> 12) & 63); data[vare_ANTALL++] = 0x80 | ((tegnkode >> 6) & 63); data[vare_ANTALL++] = 0x80 | (tegnkode & 63); }
    바이트들((const char *)data, vare_ANTALL);
}
maskin_ord verktøy_tegn(maskin_ord VERDI) {
    unsigned tegnkode = VERDI;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (tegnkode >= 0xdc00 && tegnkode <= 0xdfff) { tegn(0x10000 + ((높은부분 - 0xd800) << 10) + tegnkode - 0xdc00); return 1; }
        tegn(0xfffd);
    }
    if (tegnkode >= 0xd800 && tegnkode <= 0xdbff) 대기중짝글자 = tegnkode;
    else tegn(tegnkode > 0x10ffff || (tegnkode >= 0xdc00 && tegnkode <= 0xdfff) ? 0xfffd : tegnkode);
    return 1;
}
maskin_ord 도구출력(maskin_ord VERDI) {
    const maskin_ord *streng_data = (const maskin_ord *)VERDI;
    for (maskin_ord 순번 = 0; 순번 < streng_data[0]; 순번++) verktøy_tegn(streng_data[순번 + 1]);
    return streng_data[0];
}
static int Sti(maskin_ord objekt_referere, char KR_data[512]) {
    const maskin_ord *첫째값 = (const maskin_ord *)objekt_referere;
    unsigned 사용량 = 0;
    for (maskin_ord 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned tegnkode = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metode_MODUS 경로와 호환한다.
        if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; tegnkode = 0x10000 + ((tegnkode - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (tegnkode >= 0xd800 && tegnkode <= 0xdfff) return -22;
        unsigned vare_ANTALL = tegnkode < 128 ? 1 : tegnkode < 2048 ? 2 : tegnkode < 65536 ? 3 : 4;
        if (사용량 + vare_ANTALL > 511) return -36;
        if (vare_ANTALL == 1) KR_data[사용량++] = tegnkode;
        else {
            KR_data[사용량++] = (vare_ANTALL == 2 ? 0xc0 : vare_ANTALL == 3 ? 0xe0 : 0xf0) | (tegnkode >> (6 * (vare_ANTALL - 1)));
            for (unsigned 안쪽순번 = vare_ANTALL - 1; 안쪽순번; 안쪽순번--) KR_data[사용량++] = 0x80 | ((tegnkode >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_data[사용량] = 0; return 사용량 ? 0 : -22;
}
maskin_ord verktøy_åpen(maskin_ord Navn, maskin_ord konfigurasjon_BITS) {
    char data_plassere[512]; int feil = Sti(Navn, data_plassere);
    return (uint32_t)(feil ? feil : 호출(3, (maskin_ord)data_plassere, konfigurasjon_BITS, 0));
}
maskin_ord verktøy_Lukk(maskin_ord Fil_håndtak) { return (uint32_t)호출(4, Fil_håndtak, 0, 0); }
maskin_ord 도구바이트읽기(maskin_ord Fil_håndtak) {
    unsigned char SEKUND_VERDI; intptr_t vare_ANTALL = 호출(2, Fil_håndtak, (maskin_ord)&SEKUND_VERDI, 1);
    return (uint32_t)(vare_ANTALL == 1 ? SEKUND_VERDI : vare_ANTALL == 0 ? 256 : vare_ANTALL);
}
maskin_ord verktøy_skrive_byte(maskin_ord Fil_håndtak, maskin_ord VERDI) {
    unsigned char SEKUND_VERDI = VERDI; return (uint32_t)호출(1, Fil_håndtak, (maskin_ord)&SEKUND_VERDI, 1);
}
maskin_ord 도구읽기(maskin_ord Navn, maskin_ord mål_data_e_post) {
    if (꾸러미사용중) {
        char data_plassere[512]; int feil = Sti(Navn, data_plassere); if (feil) return (uint32_t)feil;
        unsigned vare_ANTALL = 0; while (data_plassere[vare_ANTALL]) vare_ANTALL++;
        if (vare_ANTALL >= 6) for (unsigned 순번 = 0; 순번 < vare_ANTALL - 6; 순번++) if (data_plassere[순번] == '.') data_plassere[순번] = '/';
        unsigned char 바이트들[16384]; maskin_ord *mål_VERDI_plassere = (maskin_ord *)mål_data_e_post;
        int MOTTATT_AVKAST_ANTALL = 꾸러미읽기(data_plassere, 바이트들, mål_VERDI_plassere[0] < sizeof(바이트들) ? mål_VERDI_plassere[0] : sizeof(바이트들));
        if (MOTTATT_AVKAST_ANTALL >= 0) { for (int 순번 = 0; 순번 < MOTTATT_AVKAST_ANTALL; 순번++) mål_VERDI_plassere[순번 + 1] = 바이트들[순번]; return MOTTATT_AVKAST_ANTALL; }
        if (MOTTATT_AVKAST_ANTALL != -2) return (uint32_t)MOTTATT_AVKAST_ANTALL;
    }
    int Fil_håndtak = 꾸러미사용중 ? -2 : (int32_t)verktøy_åpen(Navn, 0);
    if (Fil_håndtak < 0) {
        char data_plassere[512]; int feil = Sti(Navn, data_plassere); if (feil) return (uint32_t)feil;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Neste_FORSKYVNING = 자바클래스들[순번].Navn; unsigned 안쪽순번 = 0;
            while (data_plassere[안쪽순번] && data_plassere[안쪽순번] == Neste_FORSKYVNING[안쪽순번]) 안쪽순번++;
            if (data_plassere[안쪽순번] || Neste_FORSKYVNING[안쪽순번]) continue;
            maskin_ord *mål_VERDI_plassere = (maskin_ord *)mål_data_e_post;
            if (mål_VERDI_plassere[0] < 자바클래스들[순번].Størrelse) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Størrelse; 안쪽순번++) mål_VERDI_plassere[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Størrelse;
        }
        return (uint32_t)Fil_håndtak;
    }
    maskin_ord *첫째값 = (maskin_ord *)mål_data_e_post;
    intptr_t Størrelse = 호출(9, Fil_håndtak, 0, 0), Fullført_beløp = 0;
    if (Størrelse < 0 || (maskin_ord)Størrelse > 첫째값[0]) { verktøy_Lukk(Fil_håndtak); return (uint32_t)(Størrelse < 0 ? Størrelse : -27); }
    unsigned char data_blokk[256];
    while (Fullført_beløp < Størrelse) {
        intptr_t vare_ANTALL = 호출(2, Fil_håndtak, (maskin_ord)data_blokk, Størrelse - Fullført_beløp < 256 ? Størrelse - Fullført_beløp : 256);
        if (vare_ANTALL <= 0) { verktøy_Lukk(Fil_håndtak); return (uint32_t)(vare_ANTALL ? vare_ANTALL : -5); }
        for (intptr_t 순번 = 0; 순번 < vare_ANTALL; 순번++) 첫째값[1 + Fullført_beløp + 순번] = data_blokk[순번];
        Fullført_beløp += vare_ANTALL;
    }
    verktøy_Lukk(Fil_håndtak); return Fullført_beløp;
}
maskin_ord verktøy_skrive(maskin_ord Navn, maskin_ord 원본자료, maskin_ord oppføring_ANTALL) {
    const maskin_ord *첫째값 = (const maskin_ord *)원본자료;
    if (oppføring_ANTALL > 첫째값[0] || oppføring_ANTALL > 16384) return (uint32_t)-27;
    int Fil_håndtak = (int32_t)verktøy_åpen(Navn, 577); if (Fil_håndtak < 0) return (uint32_t)Fil_håndtak;
    unsigned char data_blokk[256]; maskin_ord Fullført_beløp = 0;
    while (Fullført_beløp < oppføring_ANTALL) {
        maskin_ord vare_ANTALL = oppføring_ANTALL - Fullført_beløp < 256 ? oppføring_ANTALL - Fullført_beløp : 256;
        for (maskin_ord 순번 = 0; 순번 < vare_ANTALL; 순번++) data_blokk[순번] = 첫째값[1 + Fullført_beløp + 순번];
        intptr_t KR = 호출(1, Fil_håndtak, (maskin_ord)data_blokk, vare_ANTALL);
        if (KR <= 0) { verktøy_Lukk(Fil_håndtak); return (uint32_t)(KR ? KR : -5); }
        Fullført_beløp += KR;
    }
    verktøy_Lukk(Fil_håndtak); return oppføring_ANTALL;
}
maskin_ord 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
maskin_ord verktøy_argument(maskin_ord Oppslag_INDEKS) {
    static const maskin_ord tom_VERDI[1] = {0};
    if (Oppslag_INDEKS >= 8) return (maskin_ord)tom_VERDI;
    unsigned char inndata[256]; intptr_t vare_ANTALL;
    if (꾸러미사용중 && Oppslag_INDEKS == 0) { const char *data_plassere = 꾸러미진입클래스(); vare_ANTALL = 0; while (data_plassere[vare_ANTALL] && vare_ANTALL < 255) { inndata[vare_ANTALL] = data_plassere[vare_ANTALL]; vare_ANTALL++; } }
    else vare_ANTALL = 호출(15, Oppslag_INDEKS + (꾸러미사용중 ? 꾸러미인수이동 : 0), (maskin_ord)inndata, sizeof(inndata));
    if (vare_ANTALL < 0) return (maskin_ord)tom_VERDI;
    maskin_ord *KR_data = 전달인수[Oppslag_INDEKS]; unsigned oppføring_ANTALL = 0;
    for (intptr_t 순번 = 0; 순번 < vare_ANTALL;) {
        unsigned tegnkode = inndata[순번++], 더있음 = tegnkode < 128 ? 0 : tegnkode >= 0xc2 && tegnkode < 0xe0 ? 1 : tegnkode < 0xf0 && tegnkode >= 0xe0 ? 2 : tegnkode >= 0xf0 && tegnkode <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > vare_ANTALL) { KR_data[++oppføring_ANTALL] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) tegnkode &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (inndata[순번] & 0xc0) == 0x80) { tegnkode = (tegnkode << 6) | (inndata[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || tegnkode < 최소값 || tegnkode > 0x10ffff || (tegnkode >= 0xd800 && tegnkode <= 0xdfff)) tegnkode = 0xfffd;
        if (tegnkode >= 65536) { tegnkode -= 65536; KR_data[++oppføring_ANTALL] = 0xd800 | (tegnkode >> 10); KR_data[++oppføring_ANTALL] = 0xdc00 | (tegnkode & 1023); }
        else KR_data[++oppføring_ANTALL] = tegnkode;
    }
    KR_data[0] = oppføring_ANTALL; return (maskin_ord)KR_data;
}
maskin_ord 도구분류(void) { return område_VERDI; }
void 커널중단(const char *notice_SMS) {
    const char *data_plassere = notice_SMS; while (*data_plassere) data_plassere++;
    바이트들("Java tool runtime error: ", 25); 바이트들(notice_SMS, data_plassere - notice_SMS); tegn(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_bruker_app(int metode_MODUS) {
    område_VERDI = metode_MODUS;
    unsigned char 첫항목[256]; intptr_t vare_ANTALL = 호출(15, 0, (maskin_ord)첫항목, sizeof(첫항목));
    if (metode_MODUS == 2 || (metode_MODUS == 1 && vare_ANTALL == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metode_MODUS == 2 ? 0 : 1;
        char Fil_oppføring_navn[256]; intptr_t lengde_data = 호출(15, 꾸러미인수이동, (maskin_ord)Fil_oppføring_navn, sizeof(Fil_oppføring_navn));
        if (lengde_data <= 0 || 꾸러미열기(Fil_oppføring_navn) < 0) {
            static const char feil[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(feil, sizeof(feil) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int KR = 자바진입();
    if (대기중짝글자) tegn(0xfffd);
    return KR;
}

// UDP는 eget 커널의 SVC를 통과하며 betalt_vare 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t serie, portnummer; uint32_t e_post; unsigned char null_VERDI[8]; };
static struct 자바주소 UDP_e_post(unsigned portnummer) {
    struct 자바주소 첫째값 = {2, (uint16_t)((portnummer << 8) | (portnummer >> 8)), 0x0100007f, {0}}; return 첫째값;
}
maskin_ord verktøy_UDP_åpen(maskin_ord portnummer) {
    intptr_t Fil_håndtak = 호출(32, 2, 2, 17); if (Fil_håndtak < 0) return (uint32_t)Fil_håndtak;
    struct 자바주소 첫째값 = UDP_e_post(portnummer);
    첫째값.e_post = 0;
    intptr_t status_VERDI = 호출(33, Fil_håndtak, (maskin_ord)&첫째값, sizeof(첫째값));
    if (status_VERDI < 0) { verktøy_Lukk(Fil_håndtak); return (uint32_t)status_VERDI; }
    return Fil_håndtak;
}
maskin_ord verktøy_UDP_sende(maskin_ord Fil_håndtak, maskin_ord portnummer, maskin_ord MATRISE_VERDI, maskin_ord lengde_VERDI) {
    const maskin_ord *원본주소 = (const maskin_ord *)MATRISE_VERDI; unsigned char data[512];
    if (lengde_VERDI > 512 || lengde_VERDI > 원본주소[0]) return (uint32_t)-90;
    for (maskin_ord 순번 = 0; 순번 < lengde_VERDI; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_e_post(portnummer);
    return (uint32_t)사용자호출(34, Fil_håndtak, (maskin_ord)data, lengde_VERDI, 0, (maskin_ord)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t vare_ANTALL) { return (vare_ANTALL>>24)|((vare_ANTALL>>8)&0xff00)|((vare_ANTALL<<8)&0xff0000)|(vare_ANTALL<<24); }
maskin_ord verktøy_UDP_sende_e_post(maskin_ord Fil_håndtak, maskin_ord e_post, maskin_ord portnummer, maskin_ord MATRISE_VERDI, maskin_ord lengde_VERDI) {
    const maskin_ord *원본주소 = (const maskin_ord *)MATRISE_VERDI; unsigned char data[512];
    if (lengde_VERDI > 512 || lengde_VERDI > 원본주소[0]) return (uint32_t)-90;
    for (maskin_ord 순번 = 0; 순번 < lengde_VERDI; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_e_post(portnummer); 첫째값.e_post = 바이트순서뒤집기(e_post);
    return (uint32_t)사용자호출(34, Fil_håndtak, (maskin_ord)data, lengde_VERDI, 0, (maskin_ord)&첫째값, sizeof(첫째값));
}
maskin_ord verktøy_KOBLE_TIL(maskin_ord Fil_håndtak, maskin_ord e_post, maskin_ord portnummer) {
    struct 자바주소 첫째값 = UDP_e_post(portnummer); 첫째값.e_post = 바이트순서뒤집기(e_post);
    uint32_t Kjør_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t KR = 호출(37, Fil_håndtak, (maskin_ord)&첫째값, sizeof(첫째값));
        if (KR != -115) return (uint32_t)KR;
        if ((uint32_t)(호출(7, 0, 0, 0) - Kjør_2) >= 1000) return (uint32_t)-110;
    }
}
maskin_ord 도구전문받기(maskin_ord Fil_håndtak, maskin_ord MATRISE_VERDI, maskin_ord bufre_kapasitet) {
    maskin_ord *mål_e_post_08bbd577 = (maskin_ord *)MATRISE_VERDI; unsigned char data[512];
    if (bufre_kapasitet > 512 || mål_e_post_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned lengde_data = sizeof(첫째값);
    intptr_t vare_ANTALL = 사용자호출(35, Fil_håndtak, (maskin_ord)data, bufre_kapasitet, 0, (maskin_ord)&첫째값, (maskin_ord)&lengde_data);
    if (vare_ANTALL >= 0) { for (intptr_t 순번 = 0; 순번 < vare_ANTALL; 순번++) mål_e_post_08bbd577[순번 + 1] = data[순번]; mål_e_post_08bbd577[513] = (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535; mål_e_post_08bbd577[514] = 바이트순서뒤집기(첫째값.e_post); }
    return (uint32_t)vare_ANTALL;
}
maskin_ord verktøy_UDP_port(maskin_ord Fil_håndtak) {
    struct 자바주소 첫째값; unsigned lengde_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Fil_håndtak, (maskin_ord)&첫째값, (maskin_ord)&lengde_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535);
}
maskin_ord 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
maskin_ord 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
maskin_ord 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
maskin_ord verktøy_grafikk_vent(void) { return (uint32_t)화면키기다리기(); }
maskin_ord verktøy_rektangel(maskin_ord x_koordinat, maskin_ord Y_koordinat, maskin_ord 너비값, maskin_ord 높이값, maskin_ord 색상) {
    return (uint32_t)사용자호출(13, x_koordinat, Y_koordinat, 색상, 너비값, 높이값, 0);
}

maskin_ord verktøy_strøm(maskin_ord Handling,maskin_ord Fil_håndtak,maskin_ord VERDI){
    if(Handling==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_e_post(VERDI);
    if(Handling==1){첫째값.e_post=0;intptr_t 반환값=호출(33,Fil_håndtak,(maskin_ord)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Fil_håndtak,4,0));}
    if(Handling==2)return (uint32_t)호출(37,Fil_håndtak,(maskin_ord)&첫째값,sizeof(첫째값));
    if(Handling==3)return (uint32_t)호출(39,Fil_håndtak,0,0);
    if(Handling==4)return verktøy_UDP_port(Fil_håndtak);
    if(Handling==5)return (uint32_t)호출(40,Fil_håndtak,0,0);
    return (uint32_t)-22;
}
maskin_ord verktøy_GUI(maskin_ord Handling,maskin_ord identifikator_VERDI,maskin_ord 첫째값,maskin_ord SEKUND_VERDI,maskin_ord tegnkode,maskin_ord mål_data){return (uint32_t)사용자호출(20,Handling,identifikator_VERDI,첫째값,SEKUND_VERDI,tegnkode,mål_data);}
maskin_ord verktøy_GUI_SMS(maskin_ord identifikator_VERDI,maskin_ord MATRISE_VERDI,maskin_ord vare_ANTALL){
    const maskin_ord *원본주소=(const maskin_ord *)MATRISE_VERDI;uint32_t data[127];unsigned oppføring_ANTALL=0;
    if(vare_ANTALL>원본주소[0])return (uint32_t)-22;
    for(maskin_ord 순번=0;순번<vare_ANTALL;순번++){unsigned tegn_koding=원본주소[순번+1];if(tegn_koding>=0xd800&&tegn_koding<=0xdbff&&순번+1<vare_ANTALL){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;tegn_koding=0x10000+((tegn_koding-0xd800)<<10)+낮은값-0xdc00;}if(oppføring_ANTALL==127)return (uint32_t)-22;data[oppføring_ANTALL++]=tegn_koding;}
    return (uint32_t)사용자호출(21,identifikator_VERDI,(maskin_ord)data,oppføring_ANTALL,0,0,0);
}
