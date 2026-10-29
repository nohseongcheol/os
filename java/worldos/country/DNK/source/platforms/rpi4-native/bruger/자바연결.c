#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fil/Udgang/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bundt.h"
typedef uintptr_t maskine_Ord;
static int område_VÆRDI;
static int 꾸러미사용중, 꾸러미인수이동;
static maskine_Ord 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned vare_TÆL, maskine_Ord 첫째값, maskine_Ord SEKUND_VÆRDI, maskine_Ord tegnkode) {
    return 사용자호출(vare_TÆL, 첫째값, SEKUND_VÆRDI, tegnkode, 0, 0, 0);
}
static void 바이트들(const char *data_placere, size_t vare_TÆL) { 호출(1, 1, (maskine_Ord)data_placere, vare_TÆL); }
static void tegn(unsigned tegnkode) {
    unsigned char data[4]; unsigned vare_TÆL = 0;
    if (tegnkode < 128) data[vare_TÆL++] = tegnkode;
    else if (tegnkode < 2048) { data[vare_TÆL++] = 0xc0 | (tegnkode >> 6); data[vare_TÆL++] = 0x80 | (tegnkode & 63); }
    else if (tegnkode < 65536) { data[vare_TÆL++] = 0xe0 | (tegnkode >> 12); data[vare_TÆL++] = 0x80 | ((tegnkode >> 6) & 63); data[vare_TÆL++] = 0x80 | (tegnkode & 63); }
    else { data[vare_TÆL++] = 0xf0 | (tegnkode >> 18); data[vare_TÆL++] = 0x80 | ((tegnkode >> 12) & 63); data[vare_TÆL++] = 0x80 | ((tegnkode >> 6) & 63); data[vare_TÆL++] = 0x80 | (tegnkode & 63); }
    바이트들((const char *)data, vare_TÆL);
}
maskine_Ord værktøj_tegn(maskine_Ord VÆRDI) {
    unsigned tegnkode = VÆRDI;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (tegnkode >= 0xdc00 && tegnkode <= 0xdfff) { tegn(0x10000 + ((높은부분 - 0xd800) << 10) + tegnkode - 0xdc00); return 1; }
        tegn(0xfffd);
    }
    if (tegnkode >= 0xd800 && tegnkode <= 0xdbff) 대기중짝글자 = tegnkode;
    else tegn(tegnkode > 0x10ffff || (tegnkode >= 0xdc00 && tegnkode <= 0xdfff) ? 0xfffd : tegnkode);
    return 1;
}
maskine_Ord 도구출력(maskine_Ord VÆRDI) {
    const maskine_Ord *streng_data = (const maskine_Ord *)VÆRDI;
    for (maskine_Ord 순번 = 0; 순번 < streng_data[0]; 순번++) værktøj_tegn(streng_data[순번 + 1]);
    return streng_data[0];
}
static int Sti(maskine_Ord objekt_referere, char KR_data[512]) {
    const maskine_Ord *첫째값 = (const maskine_Ord *)objekt_referere;
    unsigned 사용량 = 0;
    for (maskine_Ord 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned tegnkode = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metode_HYPPIGST 경로와 호환한다.
        if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; tegnkode = 0x10000 + ((tegnkode - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (tegnkode >= 0xd800 && tegnkode <= 0xdfff) return -22;
        unsigned vare_TÆL = tegnkode < 128 ? 1 : tegnkode < 2048 ? 2 : tegnkode < 65536 ? 3 : 4;
        if (사용량 + vare_TÆL > 511) return -36;
        if (vare_TÆL == 1) KR_data[사용량++] = tegnkode;
        else {
            KR_data[사용량++] = (vare_TÆL == 2 ? 0xc0 : vare_TÆL == 3 ? 0xe0 : 0xf0) | (tegnkode >> (6 * (vare_TÆL - 1)));
            for (unsigned 안쪽순번 = vare_TÆL - 1; 안쪽순번; 안쪽순번--) KR_data[사용량++] = 0x80 | ((tegnkode >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_data[사용량] = 0; return 사용량 ? 0 : -22;
}
maskine_Ord værktøj_åben(maskine_Ord Navn, maskine_Ord konfiguration_BITS) {
    char data_placere[512]; int fejl = Sti(Navn, data_placere);
    return (uint32_t)(fejl ? fejl : 호출(3, (maskine_Ord)data_placere, konfiguration_BITS, 0));
}
maskine_Ord værktøj_Luk(maskine_Ord fil_handle) { return (uint32_t)호출(4, fil_handle, 0, 0); }
maskine_Ord 도구바이트읽기(maskine_Ord fil_handle) {
    unsigned char SEKUND_VÆRDI; intptr_t vare_TÆL = 호출(2, fil_handle, (maskine_Ord)&SEKUND_VÆRDI, 1);
    return (uint32_t)(vare_TÆL == 1 ? SEKUND_VÆRDI : vare_TÆL == 0 ? 256 : vare_TÆL);
}
maskine_Ord værktøj_skrive_byte(maskine_Ord fil_handle, maskine_Ord VÆRDI) {
    unsigned char SEKUND_VÆRDI = VÆRDI; return (uint32_t)호출(1, fil_handle, (maskine_Ord)&SEKUND_VÆRDI, 1);
}
maskine_Ord 도구읽기(maskine_Ord Navn, maskine_Ord destination_data_mail) {
    if (꾸러미사용중) {
        char data_placere[512]; int fejl = Sti(Navn, data_placere); if (fejl) return (uint32_t)fejl;
        unsigned vare_TÆL = 0; while (data_placere[vare_TÆL]) vare_TÆL++;
        if (vare_TÆL >= 6) for (unsigned 순번 = 0; 순번 < vare_TÆL - 6; 순번++) if (data_placere[순번] == '.') data_placere[순번] = '/';
        unsigned char 바이트들[16384]; maskine_Ord *destination_VÆRDI_placere = (maskine_Ord *)destination_data_mail;
        int MODTAGET_VED_UDLØB_TÆL = 꾸러미읽기(data_placere, 바이트들, destination_VÆRDI_placere[0] < sizeof(바이트들) ? destination_VÆRDI_placere[0] : sizeof(바이트들));
        if (MODTAGET_VED_UDLØB_TÆL >= 0) { for (int 순번 = 0; 순번 < MODTAGET_VED_UDLØB_TÆL; 순번++) destination_VÆRDI_placere[순번 + 1] = 바이트들[순번]; return MODTAGET_VED_UDLØB_TÆL; }
        if (MODTAGET_VED_UDLØB_TÆL != -2) return (uint32_t)MODTAGET_VED_UDLØB_TÆL;
    }
    int fil_handle = 꾸러미사용중 ? -2 : (int32_t)værktøj_åben(Navn, 0);
    if (fil_handle < 0) {
        char data_placere[512]; int fejl = Sti(Navn, data_placere); if (fejl) return (uint32_t)fejl;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Næste_FORSKYDNING = 자바클래스들[순번].Navn; unsigned 안쪽순번 = 0;
            while (data_placere[안쪽순번] && data_placere[안쪽순번] == Næste_FORSKYDNING[안쪽순번]) 안쪽순번++;
            if (data_placere[안쪽순번] || Næste_FORSKYDNING[안쪽순번]) continue;
            maskine_Ord *destination_VÆRDI_placere = (maskine_Ord *)destination_data_mail;
            if (destination_VÆRDI_placere[0] < 자바클래스들[순번].Størrelse) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Størrelse; 안쪽순번++) destination_VÆRDI_placere[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Størrelse;
        }
        return (uint32_t)fil_handle;
    }
    maskine_Ord *첫째값 = (maskine_Ord *)destination_data_mail;
    intptr_t Størrelse = 호출(9, fil_handle, 0, 0), fuldført_sum = 0;
    if (Størrelse < 0 || (maskine_Ord)Størrelse > 첫째값[0]) { værktøj_Luk(fil_handle); return (uint32_t)(Størrelse < 0 ? Størrelse : -27); }
    unsigned char datablok[256];
    while (fuldført_sum < Størrelse) {
        intptr_t vare_TÆL = 호출(2, fil_handle, (maskine_Ord)datablok, Størrelse - fuldført_sum < 256 ? Størrelse - fuldført_sum : 256);
        if (vare_TÆL <= 0) { værktøj_Luk(fil_handle); return (uint32_t)(vare_TÆL ? vare_TÆL : -5); }
        for (intptr_t 순번 = 0; 순번 < vare_TÆL; 순번++) 첫째값[1 + fuldført_sum + 순번] = datablok[순번];
        fuldført_sum += vare_TÆL;
    }
    værktøj_Luk(fil_handle); return fuldført_sum;
}
maskine_Ord værktøj_skrive(maskine_Ord Navn, maskine_Ord 원본자료, maskine_Ord post_TÆL_8f7753a1) {
    const maskine_Ord *첫째값 = (const maskine_Ord *)원본자료;
    if (post_TÆL_8f7753a1 > 첫째값[0] || post_TÆL_8f7753a1 > 16384) return (uint32_t)-27;
    int fil_handle = (int32_t)værktøj_åben(Navn, 577); if (fil_handle < 0) return (uint32_t)fil_handle;
    unsigned char datablok[256]; maskine_Ord fuldført_sum = 0;
    while (fuldført_sum < post_TÆL_8f7753a1) {
        maskine_Ord vare_TÆL = post_TÆL_8f7753a1 - fuldført_sum < 256 ? post_TÆL_8f7753a1 - fuldført_sum : 256;
        for (maskine_Ord 순번 = 0; 순번 < vare_TÆL; 순번++) datablok[순번] = 첫째값[1 + fuldført_sum + 순번];
        intptr_t KR = 호출(1, fil_handle, (maskine_Ord)datablok, vare_TÆL);
        if (KR <= 0) { værktøj_Luk(fil_handle); return (uint32_t)(KR ? KR : -5); }
        fuldført_sum += KR;
    }
    værktøj_Luk(fil_handle); return post_TÆL_8f7753a1;
}
maskine_Ord 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
maskine_Ord værktøj_argument(maskine_Ord Opslag_INDEKS) {
    static const maskine_Ord 빈값[1] = {0};
    if (Opslag_INDEKS >= 8) return (maskine_Ord)빈값;
    unsigned char input[256]; intptr_t vare_TÆL;
    if (꾸러미사용중 && Opslag_INDEKS == 0) { const char *data_placere = 꾸러미진입클래스(); vare_TÆL = 0; while (data_placere[vare_TÆL] && vare_TÆL < 255) { input[vare_TÆL] = data_placere[vare_TÆL]; vare_TÆL++; } }
    else vare_TÆL = 호출(15, Opslag_INDEKS + (꾸러미사용중 ? 꾸러미인수이동 : 0), (maskine_Ord)input, sizeof(input));
    if (vare_TÆL < 0) return (maskine_Ord)빈값;
    maskine_Ord *KR_data = 전달인수[Opslag_INDEKS]; unsigned post_TÆL_8f7753a1 = 0;
    for (intptr_t 순번 = 0; 순번 < vare_TÆL;) {
        unsigned tegnkode = input[순번++], 더있음 = tegnkode < 128 ? 0 : tegnkode >= 0xc2 && tegnkode < 0xe0 ? 1 : tegnkode < 0xf0 && tegnkode >= 0xe0 ? 2 : tegnkode >= 0xf0 && tegnkode <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > vare_TÆL) { KR_data[++post_TÆL_8f7753a1] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) tegnkode &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (input[순번] & 0xc0) == 0x80) { tegnkode = (tegnkode << 6) | (input[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || tegnkode < 최소값 || tegnkode > 0x10ffff || (tegnkode >= 0xd800 && tegnkode <= 0xdfff)) tegnkode = 0xfffd;
        if (tegnkode >= 65536) { tegnkode -= 65536; KR_data[++post_TÆL_8f7753a1] = 0xd800 | (tegnkode >> 10); KR_data[++post_TÆL_8f7753a1] = 0xdc00 | (tegnkode & 1023); }
        else KR_data[++post_TÆL_8f7753a1] = tegnkode;
    }
    KR_data[0] = post_TÆL_8f7753a1; return (maskine_Ord)KR_data;
}
maskine_Ord 도구분류(void) { return område_VÆRDI; }
void 커널중단(const char *알림문) {
    const char *data_placere = 알림문; while (*data_placere) data_placere++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_placere - 알림문); tegn(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_bruger_app(int metode_HYPPIGST) {
    område_VÆRDI = metode_HYPPIGST;
    unsigned char 첫항목[256]; intptr_t vare_TÆL = 호출(15, 0, (maskine_Ord)첫항목, sizeof(첫항목));
    if (metode_HYPPIGST == 2 || (metode_HYPPIGST == 1 && vare_TÆL == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metode_HYPPIGST == 2 ? 0 : 1;
        char fil_post_navn[256]; intptr_t varighed_data = 호출(15, 꾸러미인수이동, (maskine_Ord)fil_post_navn, sizeof(fil_post_navn));
        if (varighed_data <= 0 || 꾸러미열기(fil_post_navn) < 0) {
            static const char fejl[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(fejl, sizeof(fejl) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int KR = 자바진입();
    if (대기중짝글자) tegn(0xfffd);
    return KR;
}

// UDP는 eget 커널의 SVC를 통과하며 aktuel_vare 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t serie, portnummer; uint32_t mail; unsigned char nulværdi[8]; };
static struct 자바주소 UDP_mail(unsigned portnummer) {
    struct 자바주소 첫째값 = {2, (uint16_t)((portnummer << 8) | (portnummer >> 8)), 0x0100007f, {0}}; return 첫째값;
}
maskine_Ord værktøj_UDP_åben(maskine_Ord portnummer) {
    intptr_t fil_handle = 호출(32, 2, 2, 17); if (fil_handle < 0) return (uint32_t)fil_handle;
    struct 자바주소 첫째값 = UDP_mail(portnummer);
    첫째값.mail = 0;
    intptr_t status_VÆRDI = 호출(33, fil_handle, (maskine_Ord)&첫째값, sizeof(첫째값));
    if (status_VÆRDI < 0) { værktøj_Luk(fil_handle); return (uint32_t)status_VÆRDI; }
    return fil_handle;
}
maskine_Ord værktøj_UDP_maile(maskine_Ord fil_handle, maskine_Ord portnummer, maskine_Ord MATRIX_VÆRDI, maskine_Ord varighed_VÆRDI) {
    const maskine_Ord *원본주소 = (const maskine_Ord *)MATRIX_VÆRDI; unsigned char data[512];
    if (varighed_VÆRDI > 512 || varighed_VÆRDI > 원본주소[0]) return (uint32_t)-90;
    for (maskine_Ord 순번 = 0; 순번 < varighed_VÆRDI; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_mail(portnummer);
    return (uint32_t)사용자호출(34, fil_handle, (maskine_Ord)data, varighed_VÆRDI, 0, (maskine_Ord)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t vare_TÆL) { return (vare_TÆL>>24)|((vare_TÆL>>8)&0xff00)|((vare_TÆL<<8)&0xff0000)|(vare_TÆL<<24); }
maskine_Ord værktøj_UDP_maile_mail(maskine_Ord fil_handle, maskine_Ord mail, maskine_Ord portnummer, maskine_Ord MATRIX_VÆRDI, maskine_Ord varighed_VÆRDI) {
    const maskine_Ord *원본주소 = (const maskine_Ord *)MATRIX_VÆRDI; unsigned char data[512];
    if (varighed_VÆRDI > 512 || varighed_VÆRDI > 원본주소[0]) return (uint32_t)-90;
    for (maskine_Ord 순번 = 0; 순번 < varighed_VÆRDI; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_mail(portnummer); 첫째값.mail = 바이트순서뒤집기(mail);
    return (uint32_t)사용자호출(34, fil_handle, (maskine_Ord)data, varighed_VÆRDI, 0, (maskine_Ord)&첫째값, sizeof(첫째값));
}
maskine_Ord værktøj_Forbind(maskine_Ord fil_handle, maskine_Ord mail, maskine_Ord portnummer) {
    struct 자바주소 첫째값 = UDP_mail(portnummer); 첫째값.mail = 바이트순서뒤집기(mail);
    uint32_t Kør_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t KR = 호출(37, fil_handle, (maskine_Ord)&첫째값, sizeof(첫째값));
        if (KR != -115) return (uint32_t)KR;
        if ((uint32_t)(호출(7, 0, 0, 0) - Kør_2) >= 1000) return (uint32_t)-110;
    }
}
maskine_Ord 도구전문받기(maskine_Ord fil_handle, maskine_Ord MATRIX_VÆRDI, maskine_Ord buffer_kapacitet) {
    maskine_Ord *destination_mail = (maskine_Ord *)MATRIX_VÆRDI; unsigned char data[512];
    if (buffer_kapacitet > 512 || destination_mail[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned varighed_data = sizeof(첫째값);
    intptr_t vare_TÆL = 사용자호출(35, fil_handle, (maskine_Ord)data, buffer_kapacitet, 0, (maskine_Ord)&첫째값, (maskine_Ord)&varighed_data);
    if (vare_TÆL >= 0) { for (intptr_t 순번 = 0; 순번 < vare_TÆL; 순번++) destination_mail[순번 + 1] = data[순번]; destination_mail[513] = (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535; destination_mail[514] = 바이트순서뒤집기(첫째값.mail); }
    return (uint32_t)vare_TÆL;
}
maskine_Ord værktøj_UDP_port(maskine_Ord fil_handle) {
    struct 자바주소 첫째값; unsigned varighed_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fil_handle, (maskine_Ord)&첫째값, (maskine_Ord)&varighed_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.portnummer << 8 | 첫째값.portnummer >> 8) & 65535);
}
maskine_Ord 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
maskine_Ord 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
maskine_Ord 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
maskine_Ord værktøj_grafik_vent(void) { return (uint32_t)화면키기다리기(); }
maskine_Ord værktøj_rektangel(maskine_Ord X_koordinat, maskine_Ord Y_koordinat, maskine_Ord 너비값, maskine_Ord 높이값, maskine_Ord 색상) {
    return (uint32_t)사용자호출(13, X_koordinat, Y_koordinat, 색상, 너비값, 높이값, 0);
}

maskine_Ord værktøj_strøm(maskine_Ord Handling,maskine_Ord fil_handle,maskine_Ord VÆRDI){
    if(Handling==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_mail(VÆRDI);
    if(Handling==1){첫째값.mail=0;intptr_t 반환값=호출(33,fil_handle,(maskine_Ord)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fil_handle,4,0));}
    if(Handling==2)return (uint32_t)호출(37,fil_handle,(maskine_Ord)&첫째값,sizeof(첫째값));
    if(Handling==3)return (uint32_t)호출(39,fil_handle,0,0);
    if(Handling==4)return værktøj_UDP_port(fil_handle);
    if(Handling==5)return (uint32_t)호출(40,fil_handle,0,0);
    return (uint32_t)-22;
}
maskine_Ord værktøj_GUI(maskine_Ord Handling,maskine_Ord identifikator_VÆRDI,maskine_Ord 첫째값,maskine_Ord SEKUND_VÆRDI,maskine_Ord tegnkode,maskine_Ord destination_data){return (uint32_t)사용자호출(20,Handling,identifikator_VÆRDI,첫째값,SEKUND_VÆRDI,tegnkode,destination_data);}
maskine_Ord værktøj_GUI_sms(maskine_Ord identifikator_VÆRDI,maskine_Ord MATRIX_VÆRDI,maskine_Ord vare_TÆL){
    const maskine_Ord *원본주소=(const maskine_Ord *)MATRIX_VÆRDI;uint32_t data[127];unsigned post_TÆL_8f7753a1=0;
    if(vare_TÆL>원본주소[0])return (uint32_t)-22;
    for(maskine_Ord 순번=0;순번<vare_TÆL;순번++){unsigned tegnkodning=원본주소[순번+1];if(tegnkodning>=0xd800&&tegnkodning<=0xdbff&&순번+1<vare_TÆL){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;tegnkodning=0x10000+((tegnkodning-0xd800)<<10)+낮은값-0xdc00;}if(post_TÆL_8f7753a1==127)return (uint32_t)-22;data[post_TÆL_8f7753a1++]=tegnkodning;}
    return (uint32_t)사용자호출(21,identifikator_VÆRDI,(maskine_Ord)data,post_TÆL_8f7753a1,0,0,0);
}
