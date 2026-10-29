#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fájl/Kimenet/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "köteg.h"
typedef uintptr_t gép_szó;
static int terület_ÉRTÉK;
static int 꾸러미사용중, 꾸러미인수이동;
static gép_szó 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned cikk_DARAB, gép_szó 첫째값, gép_szó MPERC_ÉRTÉK, gép_szó kódpont) {
    return 사용자호출(cikk_DARAB, 첫째값, MPERC_ÉRTÉK, kódpont, 0, 0, 0);
}
static void 바이트들(const char *adat_pozíció, size_t cikk_DARAB) { 호출(1, 1, (gép_szó)adat_pozíció, cikk_DARAB); }
static void karakter(unsigned kódpont) {
    unsigned char adat[4]; unsigned cikk_DARAB = 0;
    if (kódpont < 128) adat[cikk_DARAB++] = kódpont;
    else if (kódpont < 2048) { adat[cikk_DARAB++] = 0xc0 | (kódpont >> 6); adat[cikk_DARAB++] = 0x80 | (kódpont & 63); }
    else if (kódpont < 65536) { adat[cikk_DARAB++] = 0xe0 | (kódpont >> 12); adat[cikk_DARAB++] = 0x80 | ((kódpont >> 6) & 63); adat[cikk_DARAB++] = 0x80 | (kódpont & 63); }
    else { adat[cikk_DARAB++] = 0xf0 | (kódpont >> 18); adat[cikk_DARAB++] = 0x80 | ((kódpont >> 12) & 63); adat[cikk_DARAB++] = 0x80 | ((kódpont >> 6) & 63); adat[cikk_DARAB++] = 0x80 | (kódpont & 63); }
    바이트들((const char *)adat, cikk_DARAB);
}
gép_szó eszköz_karakter(gép_szó ÉRTÉK) {
    unsigned kódpont = ÉRTÉK;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kódpont >= 0xdc00 && kódpont <= 0xdfff) { karakter(0x10000 + ((높은부분 - 0xd800) << 10) + kódpont - 0xdc00); return 1; }
        karakter(0xfffd);
    }
    if (kódpont >= 0xd800 && kódpont <= 0xdbff) 대기중짝글자 = kódpont;
    else karakter(kódpont > 0x10ffff || (kódpont >= 0xdc00 && kódpont <= 0xdfff) ? 0xfffd : kódpont);
    return 1;
}
gép_szó 도구출력(gép_szó ÉRTÉK) {
    const gép_szó *sztring_adat = (const gép_szó *)ÉRTÉK;
    for (gép_szó 순번 = 0; 순번 < sztring_adat[0]; 순번++) eszköz_karakter(sztring_adat[순번 + 1]);
    return sztring_adat[0];
}
static int ÚTVONAL(gép_szó objektum_hivatkozik, char KR_adat[512]) {
    const gép_szó *첫째값 = (const gép_szó *)objektum_hivatkozik;
    unsigned 사용량 = 0;
    for (gép_szó 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kódpont = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metódus_mód 경로와 호환한다.
        if (kódpont >= 0xd800 && kódpont <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kódpont = 0x10000 + ((kódpont - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kódpont >= 0xd800 && kódpont <= 0xdfff) return -22;
        unsigned cikk_DARAB = kódpont < 128 ? 1 : kódpont < 2048 ? 2 : kódpont < 65536 ? 3 : 4;
        if (사용량 + cikk_DARAB > 511) return -36;
        if (cikk_DARAB == 1) KR_adat[사용량++] = kódpont;
        else {
            KR_adat[사용량++] = (cikk_DARAB == 2 ? 0xc0 : cikk_DARAB == 3 ? 0xe0 : 0xf0) | (kódpont >> (6 * (cikk_DARAB - 1)));
            for (unsigned 안쪽순번 = cikk_DARAB - 1; 안쪽순번; 안쪽순번--) KR_adat[사용량++] = 0x80 | ((kódpont >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_adat[사용량] = 0; return 사용량 ? 0 : -22;
}
gép_szó eszköz_készít(gép_szó Név, gép_szó konfiguráció_BITS) {
    char adat_pozíció[512]; int HIBA = ÚTVONAL(Név, adat_pozíció);
    return (uint32_t)(HIBA ? HIBA : 호출(3, (gép_szó)adat_pozíció, konfiguráció_BITS, 0));
}
gép_szó eszköz_bezár(gép_szó fájlleíró) { return (uint32_t)호출(4, fájlleíró, 0, 0); }
gép_szó 도구바이트읽기(gép_szó fájlleíró) {
    unsigned char MPERC_ÉRTÉK; intptr_t cikk_DARAB = 호출(2, fájlleíró, (gép_szó)&MPERC_ÉRTÉK, 1);
    return (uint32_t)(cikk_DARAB == 1 ? MPERC_ÉRTÉK : cikk_DARAB == 0 ? 256 : cikk_DARAB);
}
gép_szó eszköz_ír_bájt(gép_szó fájlleíró, gép_szó ÉRTÉK) {
    unsigned char MPERC_ÉRTÉK = ÉRTÉK; return (uint32_t)호출(1, fájlleíró, (gép_szó)&MPERC_ÉRTÉK, 1);
}
gép_szó 도구읽기(gép_szó Név, gép_szó cél_adat_CÍM) {
    if (꾸러미사용중) {
        char adat_pozíció[512]; int HIBA = ÚTVONAL(Név, adat_pozíció); if (HIBA) return (uint32_t)HIBA;
        unsigned cikk_DARAB = 0; while (adat_pozíció[cikk_DARAB]) cikk_DARAB++;
        if (cikk_DARAB >= 6) for (unsigned 순번 = 0; 순번 < cikk_DARAB - 6; 순번++) if (adat_pozíció[순번] == '.') adat_pozíció[순번] = '/';
        unsigned char 바이트들[16384]; gép_szó *cél_ÉRTÉK_pozíció = (gép_szó *)cél_adat_CÍM;
        int KAPOTT_DARAB = 꾸러미읽기(adat_pozíció, 바이트들, cél_ÉRTÉK_pozíció[0] < sizeof(바이트들) ? cél_ÉRTÉK_pozíció[0] : sizeof(바이트들));
        if (KAPOTT_DARAB >= 0) { for (int 순번 = 0; 순번 < KAPOTT_DARAB; 순번++) cél_ÉRTÉK_pozíció[순번 + 1] = 바이트들[순번]; return KAPOTT_DARAB; }
        if (KAPOTT_DARAB != -2) return (uint32_t)KAPOTT_DARAB;
    }
    int fájlleíró = 꾸러미사용중 ? -2 : (int32_t)eszköz_készít(Név, 0);
    if (fájlleíró < 0) {
        char adat_pozíció[512]; int HIBA = ÚTVONAL(Név, adat_pozíció); if (HIBA) return (uint32_t)HIBA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Tovább_Ofszet = 자바클래스들[순번].Név; unsigned 안쪽순번 = 0;
            while (adat_pozíció[안쪽순번] && adat_pozíció[안쪽순번] == Tovább_Ofszet[안쪽순번]) 안쪽순번++;
            if (adat_pozíció[안쪽순번] || Tovább_Ofszet[안쪽순번]) continue;
            gép_szó *cél_ÉRTÉK_pozíció = (gép_szó *)cél_adat_CÍM;
            if (cél_ÉRTÉK_pozíció[0] < 자바클래스들[순번].Méret) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Méret; 안쪽순번++) cél_ÉRTÉK_pozíció[안쪽순번 + 1] = 자바클래스들[순번].adat[안쪽순번];
            return 자바클래스들[순번].Méret;
        }
        return (uint32_t)fájlleíró;
    }
    gép_szó *첫째값 = (gép_szó *)cél_adat_CÍM;
    intptr_t Méret = 호출(9, fájlleíró, 0, 0), Kész_összeg = 0;
    if (Méret < 0 || (gép_szó)Méret > 첫째값[0]) { eszköz_bezár(fájlleíró); return (uint32_t)(Méret < 0 ? Méret : -27); }
    unsigned char adatblokk[256];
    while (Kész_összeg < Méret) {
        intptr_t cikk_DARAB = 호출(2, fájlleíró, (gép_szó)adatblokk, Méret - Kész_összeg < 256 ? Méret - Kész_összeg : 256);
        if (cikk_DARAB <= 0) { eszköz_bezár(fájlleíró); return (uint32_t)(cikk_DARAB ? cikk_DARAB : -5); }
        for (intptr_t 순번 = 0; 순번 < cikk_DARAB; 순번++) 첫째값[1 + Kész_összeg + 순번] = adatblokk[순번];
        Kész_összeg += cikk_DARAB;
    }
    eszköz_bezár(fájlleíró); return Kész_összeg;
}
gép_szó eszköz_ír(gép_szó Név, gép_szó 원본자료, gép_szó bejegyzés_DARAB) {
    const gép_szó *첫째값 = (const gép_szó *)원본자료;
    if (bejegyzés_DARAB > 첫째값[0] || bejegyzés_DARAB > 16384) return (uint32_t)-27;
    int fájlleíró = (int32_t)eszköz_készít(Név, 577); if (fájlleíró < 0) return (uint32_t)fájlleíró;
    unsigned char adatblokk[256]; gép_szó Kész_összeg = 0;
    while (Kész_összeg < bejegyzés_DARAB) {
        gép_szó cikk_DARAB = bejegyzés_DARAB - Kész_összeg < 256 ? bejegyzés_DARAB - Kész_összeg : 256;
        for (gép_szó 순번 = 0; 순번 < cikk_DARAB; 순번++) adatblokk[순번] = 첫째값[1 + Kész_összeg + 순번];
        intptr_t KR = 호출(1, fájlleíró, (gép_szó)adatblokk, cikk_DARAB);
        if (KR <= 0) { eszköz_bezár(fájlleíró); return (uint32_t)(KR ? KR : -5); }
        Kész_összeg += KR;
    }
    eszköz_bezár(fájlleíró); return bejegyzés_DARAB;
}
gép_szó 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
gép_szó eszköz_argumentum(gép_szó KERES_INDEX) {
    static const gép_szó üres_ÉRTÉK[1] = {0};
    if (KERES_INDEX >= 8) return (gép_szó)üres_ÉRTÉK;
    unsigned char bevitel[256]; intptr_t cikk_DARAB;
    if (꾸러미사용중 && KERES_INDEX == 0) { const char *adat_pozíció = 꾸러미진입클래스(); cikk_DARAB = 0; while (adat_pozíció[cikk_DARAB] && cikk_DARAB < 255) { bevitel[cikk_DARAB] = adat_pozíció[cikk_DARAB]; cikk_DARAB++; } }
    else cikk_DARAB = 호출(15, KERES_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (gép_szó)bevitel, sizeof(bevitel));
    if (cikk_DARAB < 0) return (gép_szó)üres_ÉRTÉK;
    gép_szó *KR_adat = 전달인수[KERES_INDEX]; unsigned bejegyzés_DARAB = 0;
    for (intptr_t 순번 = 0; 순번 < cikk_DARAB;) {
        unsigned kódpont = bevitel[순번++], 더있음 = kódpont < 128 ? 0 : kódpont >= 0xc2 && kódpont < 0xe0 ? 1 : kódpont < 0xf0 && kódpont >= 0xe0 ? 2 : kódpont >= 0xf0 && kódpont <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > cikk_DARAB) { KR_adat[++bejegyzés_DARAB] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kódpont &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (bevitel[순번] & 0xc0) == 0x80) { kódpont = (kódpont << 6) | (bevitel[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kódpont < 최소값 || kódpont > 0x10ffff || (kódpont >= 0xd800 && kódpont <= 0xdfff)) kódpont = 0xfffd;
        if (kódpont >= 65536) { kódpont -= 65536; KR_adat[++bejegyzés_DARAB] = 0xd800 | (kódpont >> 10); KR_adat[++bejegyzés_DARAB] = 0xdc00 | (kódpont & 1023); }
        else KR_adat[++bejegyzés_DARAB] = kódpont;
    }
    KR_adat[0] = bejegyzés_DARAB; return (gép_szó)KR_adat;
}
gép_szó eszköz_Altípus(void) { return terület_ÉRTÉK; }
void 커널중단(const char *alapelv_SMS) {
    const char *adat_pozíció = alapelv_SMS; while (*adat_pozíció) adat_pozíció++;
    바이트들("Java tool runtime error: ", 25); 바이트들(alapelv_SMS, adat_pozíció - alapelv_SMS); karakter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_felhasználó_app(int metódus_mód) {
    terület_ÉRTÉK = metódus_mód;
    unsigned char 첫항목[256]; intptr_t cikk_DARAB = 호출(15, 0, (gép_szó)첫항목, sizeof(첫항목));
    if (metódus_mód == 2 || (metódus_mód == 1 && cikk_DARAB == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metódus_mód == 2 ? 0 : 1;
        char Fájl_bejegyzés_név[256]; intptr_t hossz_adat = 호출(15, 꾸러미인수이동, (gép_szó)Fájl_bejegyzés_név, sizeof(Fájl_bejegyzés_név));
        if (hossz_adat <= 0 || 꾸러미열기(Fájl_bejegyzés_név) < 0) {
            static const char HIBA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(HIBA, sizeof(HIBA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int KR = 자바진입();
    if (대기중짝글자) karakter(0xfffd);
    return KR;
}

// UDP는 saját 커널의 SVC를 통과하며 aktuális_cikk 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Család, portszám; uint32_t CÍM; unsigned char nulla_ÉRTÉK[8]; };
static struct 자바주소 UDP_CÍM(unsigned portszám) {
    struct 자바주소 첫째값 = {2, (uint16_t)((portszám << 8) | (portszám >> 8)), 0x0100007f, {0}}; return 첫째값;
}
gép_szó eszköz_UDP_készít(gép_szó portszám) {
    intptr_t fájlleíró = 호출(32, 2, 2, 17); if (fájlleíró < 0) return (uint32_t)fájlleíró;
    struct 자바주소 첫째값 = UDP_CÍM(portszám);
    첫째값.CÍM = 0;
    intptr_t Állapot_ÉRTÉK = 호출(33, fájlleíró, (gép_szó)&첫째값, sizeof(첫째값));
    if (Állapot_ÉRTÉK < 0) { eszköz_bezár(fájlleíró); return (uint32_t)Állapot_ÉRTÉK; }
    return fájlleíró;
}
gép_szó eszköz_UDP_küld(gép_szó fájlleíró, gép_szó portszám, gép_szó TÖMB_ÉRTÉK, gép_szó hossz_ÉRTÉK) {
    const gép_szó *원본주소 = (const gép_szó *)TÖMB_ÉRTÉK; unsigned char adat[512];
    if (hossz_ÉRTÉK > 512 || hossz_ÉRTÉK > 원본주소[0]) return (uint32_t)-90;
    for (gép_szó 순번 = 0; 순번 < hossz_ÉRTÉK; 순번++) adat[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_CÍM(portszám);
    return (uint32_t)사용자호출(34, fájlleíró, (gép_szó)adat, hossz_ÉRTÉK, 0, (gép_szó)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t cikk_DARAB) { return (cikk_DARAB>>24)|((cikk_DARAB>>8)&0xff00)|((cikk_DARAB<<8)&0xff0000)|(cikk_DARAB<<24); }
gép_szó eszköz_UDP_küld_CÍM(gép_szó fájlleíró, gép_szó CÍM, gép_szó portszám, gép_szó TÖMB_ÉRTÉK, gép_szó hossz_ÉRTÉK) {
    const gép_szó *원본주소 = (const gép_szó *)TÖMB_ÉRTÉK; unsigned char adat[512];
    if (hossz_ÉRTÉK > 512 || hossz_ÉRTÉK > 원본주소[0]) return (uint32_t)-90;
    for (gép_szó 순번 = 0; 순번 < hossz_ÉRTÉK; 순번++) adat[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_CÍM(portszám); 첫째값.CÍM = 바이트순서뒤집기(CÍM);
    return (uint32_t)사용자호출(34, fájlleíró, (gép_szó)adat, hossz_ÉRTÉK, 0, (gép_szó)&첫째값, sizeof(첫째값));
}
gép_szó eszköz_KAPCSOLAT(gép_szó fájlleíró, gép_szó CÍM, gép_szó portszám) {
    struct 자바주소 첫째값 = UDP_CÍM(portszám); 첫째값.CÍM = 바이트순서뒤집기(CÍM);
    uint32_t Futtatás = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t KR = 호출(37, fájlleíró, (gép_szó)&첫째값, sizeof(첫째값));
        if (KR != -115) return (uint32_t)KR;
        if ((uint32_t)(호출(7, 0, 0, 0) - Futtatás) >= 1000) return (uint32_t)-110;
    }
}
gép_szó 도구전문받기(gép_szó fájlleíró, gép_szó TÖMB_ÉRTÉK, gép_szó puffer_kapacitás) {
    gép_szó *cél_CÍM_08bbd577 = (gép_szó *)TÖMB_ÉRTÉK; unsigned char adat[512];
    if (puffer_kapacitás > 512 || cél_CÍM_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned hossz_adat = sizeof(첫째값);
    intptr_t cikk_DARAB = 사용자호출(35, fájlleíró, (gép_szó)adat, puffer_kapacitás, 0, (gép_szó)&첫째값, (gép_szó)&hossz_adat);
    if (cikk_DARAB >= 0) { for (intptr_t 순번 = 0; 순번 < cikk_DARAB; 순번++) cél_CÍM_08bbd577[순번 + 1] = adat[순번]; cél_CÍM_08bbd577[513] = (첫째값.portszám << 8 | 첫째값.portszám >> 8) & 65535; cél_CÍM_08bbd577[514] = 바이트순서뒤집기(첫째값.CÍM); }
    return (uint32_t)cikk_DARAB;
}
gép_szó eszköz_UDP_port(gép_szó fájlleíró) {
    struct 자바주소 첫째값; unsigned hossz_adat = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fájlleíró, (gép_szó)&첫째값, (gép_szó)&hossz_adat);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.portszám << 8 | 첫째값.portszám >> 8) & 65535);
}
gép_szó 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
gép_szó 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
gép_szó 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
gép_szó eszköz_grafika_várj(void) { return (uint32_t)화면키기다리기(); }
gép_szó eszköz_téglalap(gép_szó x_koordináta, gép_szó Y_koordináta, gép_szó 너비값, gép_szó 높이값, gép_szó 색상) {
    return (uint32_t)사용자호출(13, x_koordináta, Y_koordináta, 색상, 너비값, 높이값, 0);
}

gép_szó eszköz_Stream(gép_szó Művelet,gép_szó fájlleíró,gép_szó ÉRTÉK){
    if(Művelet==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_CÍM(ÉRTÉK);
    if(Művelet==1){첫째값.CÍM=0;intptr_t 반환값=호출(33,fájlleíró,(gép_szó)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fájlleíró,4,0));}
    if(Művelet==2)return (uint32_t)호출(37,fájlleíró,(gép_szó)&첫째값,sizeof(첫째값));
    if(Művelet==3)return (uint32_t)호출(39,fájlleíró,0,0);
    if(Művelet==4)return eszköz_UDP_port(fájlleíró);
    if(Művelet==5)return (uint32_t)호출(40,fájlleíró,0,0);
    return (uint32_t)-22;
}
gép_szó eszköz_vizuális_felület(gép_szó Művelet,gép_szó azonosító_ÉRTÉK,gép_szó 첫째값,gép_szó MPERC_ÉRTÉK,gép_szó kódpont,gép_szó cél_adat){return (uint32_t)사용자호출(20,Művelet,azonosító_ÉRTÉK,첫째값,MPERC_ÉRTÉK,kódpont,cél_adat);}
gép_szó eszköz_vizuális_felület_SMS(gép_szó azonosító_ÉRTÉK,gép_szó TÖMB_ÉRTÉK,gép_szó cikk_DARAB){
    const gép_szó *원본주소=(const gép_szó *)TÖMB_ÉRTÉK;uint32_t adat[127];unsigned bejegyzés_DARAB=0;
    if(cikk_DARAB>원본주소[0])return (uint32_t)-22;
    for(gép_szó 순번=0;순번<cikk_DARAB;순번++){unsigned karakterkódolás=원본주소[순번+1];if(karakterkódolás>=0xd800&&karakterkódolás<=0xdbff&&순번+1<cikk_DARAB){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;karakterkódolás=0x10000+((karakterkódolás-0xd800)<<10)+낮은값-0xdc00;}if(bejegyzés_DARAB==127)return (uint32_t)-22;adat[bejegyzés_DARAB++]=karakterkódolás;}
    return (uint32_t)사용자호출(21,azonosító_ÉRTÉK,(gép_szó)adat,bejegyzés_DARAB,0,0,0);
}
