#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 tiedoston_nimi/tulostuspaikka/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "nippu.h"
typedef uintptr_t kone_Word;
static int alue_ARVO;
static int 꾸러미사용중, 꾸러미인수이동;
static kone_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned kohde_LASKE, kone_Word 첫째값, kone_Word SEKUNNIT_ARVO, kone_Word merkkikoodi) {
    return 사용자호출(kohde_LASKE, 첫째값, SEKUNNIT_ARVO, merkkikoodi, 0, 0, 0);
}
static void 바이트들(const char *data_toimi, size_t kohde_LASKE) { 호출(1, 1, (kone_Word)data_toimi, kohde_LASKE); }
static void merkki(unsigned merkkikoodi) {
    unsigned char data[4]; unsigned kohde_LASKE = 0;
    if (merkkikoodi < 128) data[kohde_LASKE++] = merkkikoodi;
    else if (merkkikoodi < 2048) { data[kohde_LASKE++] = 0xc0 | (merkkikoodi >> 6); data[kohde_LASKE++] = 0x80 | (merkkikoodi & 63); }
    else if (merkkikoodi < 65536) { data[kohde_LASKE++] = 0xe0 | (merkkikoodi >> 12); data[kohde_LASKE++] = 0x80 | ((merkkikoodi >> 6) & 63); data[kohde_LASKE++] = 0x80 | (merkkikoodi & 63); }
    else { data[kohde_LASKE++] = 0xf0 | (merkkikoodi >> 18); data[kohde_LASKE++] = 0x80 | ((merkkikoodi >> 12) & 63); data[kohde_LASKE++] = 0x80 | ((merkkikoodi >> 6) & 63); data[kohde_LASKE++] = 0x80 | (merkkikoodi & 63); }
    바이트들((const char *)data, kohde_LASKE);
}
kone_Word työkalu_merkki(kone_Word ARVO) {
    unsigned merkkikoodi = ARVO;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (merkkikoodi >= 0xdc00 && merkkikoodi <= 0xdfff) { merkki(0x10000 + ((높은부분 - 0xd800) << 10) + merkkikoodi - 0xdc00); return 1; }
        merkki(0xfffd);
    }
    if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdbff) 대기중짝글자 = merkkikoodi;
    else merkki(merkkikoodi > 0x10ffff || (merkkikoodi >= 0xdc00 && merkkikoodi <= 0xdfff) ? 0xfffd : merkkikoodi);
    return 1;
}
kone_Word 도구출력(kone_Word ARVO) {
    const kone_Word *merkkijono_data = (const kone_Word *)ARVO;
    for (kone_Word 순번 = 0; 순번 < merkkijono_data[0]; 순번++) työkalu_merkki(merkkijono_data[순번 + 1]);
    return merkkijono_data[0];
}
static int polku_2(kone_Word objekti_viite, char KR_data[512]) {
    const kone_Word *첫째값 = (const kone_Word *)objekti_viite;
    unsigned 사용량 = 0;
    for (kone_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned merkkikoodi = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] menetelmä_tila 경로와 호환한다.
        if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; merkkikoodi = 0x10000 + ((merkkikoodi - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdfff) return -22;
        unsigned kohde_LASKE = merkkikoodi < 128 ? 1 : merkkikoodi < 2048 ? 2 : merkkikoodi < 65536 ? 3 : 4;
        if (사용량 + kohde_LASKE > 511) return -36;
        if (kohde_LASKE == 1) KR_data[사용량++] = merkkikoodi;
        else {
            KR_data[사용량++] = (kohde_LASKE == 2 ? 0xc0 : kohde_LASKE == 3 ? 0xe0 : 0xf0) | (merkkikoodi >> (6 * (kohde_LASKE - 1)));
            for (unsigned 안쪽순번 = kohde_LASKE - 1; 안쪽순번; 안쪽순번--) KR_data[사용량++] = 0x80 | ((merkkikoodi >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_data[사용량] = 0; return 사용량 ? 0 : -22;
}
kone_Word työkalu_avata(kone_Word Nimi, kone_Word määritys_Background_Intelligent_Transfer_Service) {
    char data_toimi[512]; int VIRHE = polku_2(Nimi, data_toimi);
    return (uint32_t)(VIRHE ? VIRHE : 호출(3, (kone_Word)data_toimi, määritys_Background_Intelligent_Transfer_Service, 0));
}
kone_Word työkalu_Sulje(kone_Word Tiedosto_kahva) { return (uint32_t)호출(4, Tiedosto_kahva, 0, 0); }
kone_Word työkalu_lukea_tavu(kone_Word Tiedosto_kahva) {
    unsigned char SEKUNNIT_ARVO; intptr_t kohde_LASKE = 호출(2, Tiedosto_kahva, (kone_Word)&SEKUNNIT_ARVO, 1);
    return (uint32_t)(kohde_LASKE == 1 ? SEKUNNIT_ARVO : kohde_LASKE == 0 ? 256 : kohde_LASKE);
}
kone_Word työkalu_kirjoitus_tavu(kone_Word Tiedosto_kahva, kone_Word ARVO) {
    unsigned char SEKUNNIT_ARVO = ARVO; return (uint32_t)호출(1, Tiedosto_kahva, (kone_Word)&SEKUNNIT_ARVO, 1);
}
kone_Word työkalu_lukea(kone_Word Nimi, kone_Word kohde_data_OSOITE) {
    if (꾸러미사용중) {
        char data_toimi[512]; int VIRHE = polku_2(Nimi, data_toimi); if (VIRHE) return (uint32_t)VIRHE;
        unsigned kohde_LASKE = 0; while (data_toimi[kohde_LASKE]) kohde_LASKE++;
        if (kohde_LASKE >= 6) for (unsigned 순번 = 0; 순번 < kohde_LASKE - 6; 순번++) if (data_toimi[순번] == '.') data_toimi[순번] = '/';
        unsigned char 바이트들[16384]; kone_Word *kohde_ARVO_toimi = (kone_Word *)kohde_data_OSOITE;
        int SAATU_HINTA_LASKE = 꾸러미읽기(data_toimi, 바이트들, kohde_ARVO_toimi[0] < sizeof(바이트들) ? kohde_ARVO_toimi[0] : sizeof(바이트들));
        if (SAATU_HINTA_LASKE >= 0) { for (int 순번 = 0; 순번 < SAATU_HINTA_LASKE; 순번++) kohde_ARVO_toimi[순번 + 1] = 바이트들[순번]; return SAATU_HINTA_LASKE; }
        if (SAATU_HINTA_LASKE != -2) return (uint32_t)SAATU_HINTA_LASKE;
    }
    int Tiedosto_kahva = 꾸러미사용중 ? -2 : (int32_t)työkalu_avata(Nimi, 0);
    if (Tiedosto_kahva < 0) {
        char data_toimi[512]; int VIRHE = polku_2(Nimi, data_toimi); if (VIRHE) return (uint32_t)VIRHE;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Seuraava_SIIRTYMÄ = 자바클래스들[순번].Nimi; unsigned 안쪽순번 = 0;
            while (data_toimi[안쪽순번] && data_toimi[안쪽순번] == Seuraava_SIIRTYMÄ[안쪽순번]) 안쪽순번++;
            if (data_toimi[안쪽순번] || Seuraava_SIIRTYMÄ[안쪽순번]) continue;
            kone_Word *kohde_ARVO_toimi = (kone_Word *)kohde_data_OSOITE;
            if (kohde_ARVO_toimi[0] < 자바클래스들[순번].Koko) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Koko; 안쪽순번++) kohde_ARVO_toimi[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Koko;
        }
        return (uint32_t)Tiedosto_kahva;
    }
    kone_Word *첫째값 = (kone_Word *)kohde_data_OSOITE;
    intptr_t Koko = 호출(9, Tiedosto_kahva, 0, 0), valmis_määrä = 0;
    if (Koko < 0 || (kone_Word)Koko > 첫째값[0]) { työkalu_Sulje(Tiedosto_kahva); return (uint32_t)(Koko < 0 ? Koko : -27); }
    unsigned char tietolohko[256];
    while (valmis_määrä < Koko) {
        intptr_t kohde_LASKE = 호출(2, Tiedosto_kahva, (kone_Word)tietolohko, Koko - valmis_määrä < 256 ? Koko - valmis_määrä : 256);
        if (kohde_LASKE <= 0) { työkalu_Sulje(Tiedosto_kahva); return (uint32_t)(kohde_LASKE ? kohde_LASKE : -5); }
        for (intptr_t 순번 = 0; 순번 < kohde_LASKE; 순번++) 첫째값[1 + valmis_määrä + 순번] = tietolohko[순번];
        valmis_määrä += kohde_LASKE;
    }
    työkalu_Sulje(Tiedosto_kahva); return valmis_määrä;
}
kone_Word työkalu_kirjoitus(kone_Word Nimi, kone_Word 원본자료, kone_Word merkintä_LASKE) {
    const kone_Word *첫째값 = (const kone_Word *)원본자료;
    if (merkintä_LASKE > 첫째값[0] || merkintä_LASKE > 16384) return (uint32_t)-27;
    int Tiedosto_kahva = (int32_t)työkalu_avata(Nimi, 577); if (Tiedosto_kahva < 0) return (uint32_t)Tiedosto_kahva;
    unsigned char tietolohko[256]; kone_Word valmis_määrä = 0;
    while (valmis_määrä < merkintä_LASKE) {
        kone_Word kohde_LASKE = merkintä_LASKE - valmis_määrä < 256 ? merkintä_LASKE - valmis_määrä : 256;
        for (kone_Word 순번 = 0; 순번 < kohde_LASKE; 순번++) tietolohko[순번] = 첫째값[1 + valmis_määrä + 순번];
        intptr_t TULOS = 호출(1, Tiedosto_kahva, (kone_Word)tietolohko, kohde_LASKE);
        if (TULOS <= 0) { työkalu_Sulje(Tiedosto_kahva); return (uint32_t)(TULOS ? TULOS : -5); }
        valmis_määrä += TULOS;
    }
    työkalu_Sulje(Tiedosto_kahva); return merkintä_LASKE;
}
kone_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
kone_Word työkalu_argumentti(kone_Word HAKU_INDEKSI) {
    static const kone_Word 빈값[1] = {0};
    if (HAKU_INDEKSI >= 8) return (kone_Word)빈값;
    unsigned char syöte[256]; intptr_t kohde_LASKE;
    if (꾸러미사용중 && HAKU_INDEKSI == 0) { const char *data_toimi = 꾸러미진입클래스(); kohde_LASKE = 0; while (data_toimi[kohde_LASKE] && kohde_LASKE < 255) { syöte[kohde_LASKE] = data_toimi[kohde_LASKE]; kohde_LASKE++; } }
    else kohde_LASKE = 호출(15, HAKU_INDEKSI + (꾸러미사용중 ? 꾸러미인수이동 : 0), (kone_Word)syöte, sizeof(syöte));
    if (kohde_LASKE < 0) return (kone_Word)빈값;
    kone_Word *KR_data = 전달인수[HAKU_INDEKSI]; unsigned merkintä_LASKE = 0;
    for (intptr_t 순번 = 0; 순번 < kohde_LASKE;) {
        unsigned merkkikoodi = syöte[순번++], 더있음 = merkkikoodi < 128 ? 0 : merkkikoodi >= 0xc2 && merkkikoodi < 0xe0 ? 1 : merkkikoodi < 0xf0 && merkkikoodi >= 0xe0 ? 2 : merkkikoodi >= 0xf0 && merkkikoodi <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > kohde_LASKE) { KR_data[++merkintä_LASKE] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) merkkikoodi &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (syöte[순번] & 0xc0) == 0x80) { merkkikoodi = (merkkikoodi << 6) | (syöte[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || merkkikoodi < 최소값 || merkkikoodi > 0x10ffff || (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdfff)) merkkikoodi = 0xfffd;
        if (merkkikoodi >= 65536) { merkkikoodi -= 65536; KR_data[++merkintä_LASKE] = 0xd800 | (merkkikoodi >> 10); KR_data[++merkintä_LASKE] = 0xdc00 | (merkkikoodi & 1023); }
        else KR_data[++merkintä_LASKE] = merkkikoodi;
    }
    KR_data[0] = merkintä_LASKE; return (kone_Word)KR_data;
}
kone_Word 도구분류(void) { return alue_ARVO; }
void 커널중단(const char *알림문) {
    const char *data_toimi = 알림문; while (*data_toimi) data_toimi++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_toimi - 알림문); merkki(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int alku_käyttäjä_ohjelma(int menetelmä_tila) {
    alue_ARVO = menetelmä_tila;
    unsigned char 첫항목[256]; intptr_t kohde_LASKE = 호출(15, 0, (kone_Word)첫항목, sizeof(첫항목));
    if (menetelmä_tila == 2 || (menetelmä_tila == 1 && kohde_LASKE == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = menetelmä_tila == 2 ? 0 : 1;
        char Tiedosto_merkintä_nimi[256]; intptr_t kesto_data = 호출(15, 꾸러미인수이동, (kone_Word)Tiedosto_merkintä_nimi, sizeof(Tiedosto_merkintä_nimi));
        if (kesto_data <= 0 || 꾸러미열기(Tiedosto_merkintä_nimi) < 0) {
            static const char VIRHE[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(VIRHE, sizeof(VIRHE) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int TULOS = 자바진입();
    if (대기중짝글자) merkki(0xfffd);
    return TULOS;
}

// UDP는 oma 커널의 SVC를 통과하며 nykyinen_kohde 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Perhe, portin_numero; uint32_t OSOITE; unsigned char nolla_ARVO[8]; };
static struct 자바주소 UDP_OSOITE(unsigned portin_numero) {
    struct 자바주소 첫째값 = {2, (uint16_t)((portin_numero << 8) | (portin_numero >> 8)), 0x0100007f, {0}}; return 첫째값;
}
kone_Word työkalu_UDP_avata(kone_Word portin_numero) {
    intptr_t Tiedosto_kahva = 호출(32, 2, 2, 17); if (Tiedosto_kahva < 0) return (uint32_t)Tiedosto_kahva;
    struct 자바주소 첫째값 = UDP_OSOITE(portin_numero);
    첫째값.OSOITE = 0;
    intptr_t Tila_ARVO = 호출(33, Tiedosto_kahva, (kone_Word)&첫째값, sizeof(첫째값));
    if (Tila_ARVO < 0) { työkalu_Sulje(Tiedosto_kahva); return (uint32_t)Tila_ARVO; }
    return Tiedosto_kahva;
}
kone_Word työkalu_UDP_lähettää(kone_Word Tiedosto_kahva, kone_Word portin_numero, kone_Word MATRIISI_ARVO, kone_Word kesto_ARVO) {
    const kone_Word *원본주소 = (const kone_Word *)MATRIISI_ARVO; unsigned char data[512];
    if (kesto_ARVO > 512 || kesto_ARVO > 원본주소[0]) return (uint32_t)-90;
    for (kone_Word 순번 = 0; 순번 < kesto_ARVO; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_OSOITE(portin_numero);
    return (uint32_t)사용자호출(34, Tiedosto_kahva, (kone_Word)data, kesto_ARVO, 0, (kone_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t kohde_LASKE) { return (kohde_LASKE>>24)|((kohde_LASKE>>8)&0xff00)|((kohde_LASKE<<8)&0xff0000)|(kohde_LASKE<<24); }
kone_Word työkalu_UDP_lähettää_OSOITE(kone_Word Tiedosto_kahva, kone_Word OSOITE, kone_Word portin_numero, kone_Word MATRIISI_ARVO, kone_Word kesto_ARVO) {
    const kone_Word *원본주소 = (const kone_Word *)MATRIISI_ARVO; unsigned char data[512];
    if (kesto_ARVO > 512 || kesto_ARVO > 원본주소[0]) return (uint32_t)-90;
    for (kone_Word 순번 = 0; 순번 < kesto_ARVO; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_OSOITE(portin_numero); 첫째값.OSOITE = 바이트순서뒤집기(OSOITE);
    return (uint32_t)사용자호출(34, Tiedosto_kahva, (kone_Word)data, kesto_ARVO, 0, (kone_Word)&첫째값, sizeof(첫째값));
}
kone_Word työkalu_YHDISTÄ(kone_Word Tiedosto_kahva, kone_Word OSOITE, kone_Word portin_numero) {
    struct 자바주소 첫째값 = UDP_OSOITE(portin_numero); 첫째값.OSOITE = 바이트순서뒤집기(OSOITE);
    uint32_t Suorita_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t TULOS = 호출(37, Tiedosto_kahva, (kone_Word)&첫째값, sizeof(첫째값));
        if (TULOS != -115) return (uint32_t)TULOS;
        if ((uint32_t)(호출(7, 0, 0, 0) - Suorita_2) >= 1000) return (uint32_t)-110;
    }
}
kone_Word 도구전문받기(kone_Word Tiedosto_kahva, kone_Word MATRIISI_ARVO, kone_Word puskuri_kapasiteetti) {
    kone_Word *kohde_OSOITE_08bbd577 = (kone_Word *)MATRIISI_ARVO; unsigned char data[512];
    if (puskuri_kapasiteetti > 512 || kohde_OSOITE_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned kesto_data = sizeof(첫째값);
    intptr_t kohde_LASKE = 사용자호출(35, Tiedosto_kahva, (kone_Word)data, puskuri_kapasiteetti, 0, (kone_Word)&첫째값, (kone_Word)&kesto_data);
    if (kohde_LASKE >= 0) { for (intptr_t 순번 = 0; 순번 < kohde_LASKE; 순번++) kohde_OSOITE_08bbd577[순번 + 1] = data[순번]; kohde_OSOITE_08bbd577[513] = (첫째값.portin_numero << 8 | 첫째값.portin_numero >> 8) & 65535; kohde_OSOITE_08bbd577[514] = 바이트순서뒤집기(첫째값.OSOITE); }
    return (uint32_t)kohde_LASKE;
}
kone_Word työkalu_UDP_portti(kone_Word Tiedosto_kahva) {
    struct 자바주소 첫째값; unsigned kesto_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Tiedosto_kahva, (kone_Word)&첫째값, (kone_Word)&kesto_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.portin_numero << 8 | 첫째값.portin_numero >> 8) & 65535);
}
kone_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
kone_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
kone_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
kone_Word työkalu_grafiikka_odottaa(void) { return (uint32_t)화면키기다리기(); }
kone_Word työkalu_suorakulmio(kone_Word x_koordinaatti, kone_Word Y_koordinaatti, kone_Word 너비값, kone_Word 높이값, kone_Word 색상) {
    return (uint32_t)사용자호출(13, x_koordinaatti, Y_koordinaatti, 색상, 너비값, 높이값, 0);
}

kone_Word työkalu_virta(kone_Word Toiminto,kone_Word Tiedosto_kahva,kone_Word ARVO){
    if(Toiminto==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_OSOITE(ARVO);
    if(Toiminto==1){첫째값.OSOITE=0;intptr_t 반환값=호출(33,Tiedosto_kahva,(kone_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Tiedosto_kahva,4,0));}
    if(Toiminto==2)return (uint32_t)호출(37,Tiedosto_kahva,(kone_Word)&첫째값,sizeof(첫째값));
    if(Toiminto==3)return (uint32_t)호출(39,Tiedosto_kahva,0,0);
    if(Toiminto==4)return työkalu_UDP_portti(Tiedosto_kahva);
    if(Toiminto==5)return (uint32_t)호출(40,Tiedosto_kahva,0,0);
    return (uint32_t)-22;
}
kone_Word työkalu_GUI(kone_Word Toiminto,kone_Word tunniste_ARVO,kone_Word 첫째값,kone_Word SEKUNNIT_ARVO,kone_Word merkkikoodi,kone_Word kohde_data){return (uint32_t)사용자호출(20,Toiminto,tunniste_ARVO,첫째값,SEKUNNIT_ARVO,merkkikoodi,kohde_data);}
kone_Word työkalu_GUI_SMS(kone_Word tunniste_ARVO,kone_Word MATRIISI_ARVO,kone_Word kohde_LASKE){
    const kone_Word *원본주소=(const kone_Word *)MATRIISI_ARVO;uint32_t data[127];unsigned merkintä_LASKE=0;
    if(kohde_LASKE>원본주소[0])return (uint32_t)-22;
    for(kone_Word 순번=0;순번<kohde_LASKE;순번++){unsigned merkkikoodaus=원본주소[순번+1];if(merkkikoodaus>=0xd800&&merkkikoodaus<=0xdbff&&순번+1<kohde_LASKE){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;merkkikoodaus=0x10000+((merkkikoodaus-0xd800)<<10)+낮은값-0xdc00;}if(merkintä_LASKE==127)return (uint32_t)-22;data[merkintä_LASKE++]=merkkikoodaus;}
    return (uint32_t)사용자호출(21,tunniste_ARVO,(kone_Word)data,merkintä_LASKE,0,0,0);
}
