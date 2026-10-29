#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 dosya/metinÇıktısı/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "paket_iş.h"
typedef uintptr_t makine_Word;
static int alan_değer;
static int 꾸러미사용중, 꾸러미인수이동;
static makine_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned öğe_BAĞ_DEĞ_SAY, makine_Word 첫째값, makine_Word SANİYE_değer, makine_Word kod_noktası) {
    return 사용자호출(öğe_BAĞ_DEĞ_SAY, 첫째값, SANİYE_değer, kod_noktası, 0, 0, 0);
}
static void 바이트들(const char *veri_konum, size_t öğe_BAĞ_DEĞ_SAY) { 호출(1, 1, (makine_Word)veri_konum, öğe_BAĞ_DEĞ_SAY); }
static void karakter(unsigned kod_noktası) {
    unsigned char veri[4]; unsigned öğe_BAĞ_DEĞ_SAY = 0;
    if (kod_noktası < 128) veri[öğe_BAĞ_DEĞ_SAY++] = kod_noktası;
    else if (kod_noktası < 2048) { veri[öğe_BAĞ_DEĞ_SAY++] = 0xc0 | (kod_noktası >> 6); veri[öğe_BAĞ_DEĞ_SAY++] = 0x80 | (kod_noktası & 63); }
    else if (kod_noktası < 65536) { veri[öğe_BAĞ_DEĞ_SAY++] = 0xe0 | (kod_noktası >> 12); veri[öğe_BAĞ_DEĞ_SAY++] = 0x80 | ((kod_noktası >> 6) & 63); veri[öğe_BAĞ_DEĞ_SAY++] = 0x80 | (kod_noktası & 63); }
    else { veri[öğe_BAĞ_DEĞ_SAY++] = 0xf0 | (kod_noktası >> 18); veri[öğe_BAĞ_DEĞ_SAY++] = 0x80 | ((kod_noktası >> 12) & 63); veri[öğe_BAĞ_DEĞ_SAY++] = 0x80 | ((kod_noktası >> 6) & 63); veri[öğe_BAĞ_DEĞ_SAY++] = 0x80 | (kod_noktası & 63); }
    바이트들((const char *)veri, öğe_BAĞ_DEĞ_SAY);
}
makine_Word araç_karakter(makine_Word değer) {
    unsigned kod_noktası = değer;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kod_noktası >= 0xdc00 && kod_noktası <= 0xdfff) { karakter(0x10000 + ((높은부분 - 0xd800) << 10) + kod_noktası - 0xdc00); return 1; }
        karakter(0xfffd);
    }
    if (kod_noktası >= 0xd800 && kod_noktası <= 0xdbff) 대기중짝글자 = kod_noktası;
    else karakter(kod_noktası > 0x10ffff || (kod_noktası >= 0xdc00 && kod_noktası <= 0xdfff) ? 0xfffd : kod_noktası);
    return 1;
}
makine_Word 도구출력(makine_Word değer) {
    const makine_Word *dize_veri = (const makine_Word *)değer;
    for (makine_Word 순번 = 0; 순번 < dize_veri[0]; 순번++) araç_karakter(dize_veri[순번 + 1]);
    return dize_veri[0];
}
static int yol(makine_Word nesne_Başvuru, char KR_veri[512]) {
    const makine_Word *첫째값 = (const makine_Word *)nesne_Başvuru;
    unsigned 사용량 = 0;
    for (makine_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kod_noktası = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metot_mod 경로와 호환한다.
        if (kod_noktası >= 0xd800 && kod_noktası <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kod_noktası = 0x10000 + ((kod_noktası - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kod_noktası >= 0xd800 && kod_noktası <= 0xdfff) return -22;
        unsigned öğe_BAĞ_DEĞ_SAY = kod_noktası < 128 ? 1 : kod_noktası < 2048 ? 2 : kod_noktası < 65536 ? 3 : 4;
        if (사용량 + öğe_BAĞ_DEĞ_SAY > 511) return -36;
        if (öğe_BAĞ_DEĞ_SAY == 1) KR_veri[사용량++] = kod_noktası;
        else {
            KR_veri[사용량++] = (öğe_BAĞ_DEĞ_SAY == 2 ? 0xc0 : öğe_BAĞ_DEĞ_SAY == 3 ? 0xe0 : 0xf0) | (kod_noktası >> (6 * (öğe_BAĞ_DEĞ_SAY - 1)));
            for (unsigned 안쪽순번 = öğe_BAĞ_DEĞ_SAY - 1; 안쪽순번; 안쪽순번--) KR_veri[사용량++] = 0x80 | ((kod_noktası >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_veri[사용량] = 0; return 사용량 ? 0 : -22;
}
makine_Word araç_açık(makine_Word İsim, makine_Word Yapılandırma_BITS) {
    char veri_konum[512]; int hata = yol(İsim, veri_konum);
    return (uint32_t)(hata ? hata : 호출(3, (makine_Word)veri_konum, Yapılandırma_BITS, 0));
}
makine_Word araç_Kapat(makine_Word dosya_tanıtıcısı) { return (uint32_t)호출(4, dosya_tanıtıcısı, 0, 0); }
makine_Word 도구바이트읽기(makine_Word dosya_tanıtıcısı) {
    unsigned char SANİYE_değer; intptr_t öğe_BAĞ_DEĞ_SAY = 호출(2, dosya_tanıtıcısı, (makine_Word)&SANİYE_değer, 1);
    return (uint32_t)(öğe_BAĞ_DEĞ_SAY == 1 ? SANİYE_değer : öğe_BAĞ_DEĞ_SAY == 0 ? 256 : öğe_BAĞ_DEĞ_SAY);
}
makine_Word araç_yazma_bayt(makine_Word dosya_tanıtıcısı, makine_Word değer) {
    unsigned char SANİYE_değer = değer; return (uint32_t)호출(1, dosya_tanıtıcısı, (makine_Word)&SANİYE_değer, 1);
}
makine_Word 도구읽기(makine_Word İsim, makine_Word hedef_veri_ADRES) {
    if (꾸러미사용중) {
        char veri_konum[512]; int hata = yol(İsim, veri_konum); if (hata) return (uint32_t)hata;
        unsigned öğe_BAĞ_DEĞ_SAY = 0; while (veri_konum[öğe_BAĞ_DEĞ_SAY]) öğe_BAĞ_DEĞ_SAY++;
        if (öğe_BAĞ_DEĞ_SAY >= 6) for (unsigned 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY - 6; 순번++) if (veri_konum[순번] == '.') veri_konum[순번] = '/';
        unsigned char 바이트들[16384]; makine_Word *hedef_değer_konum = (makine_Word *)hedef_veri_ADRES;
        int GETİRİ_BAĞ_DEĞ_SAY = 꾸러미읽기(veri_konum, 바이트들, hedef_değer_konum[0] < sizeof(바이트들) ? hedef_değer_konum[0] : sizeof(바이트들));
        if (GETİRİ_BAĞ_DEĞ_SAY >= 0) { for (int 순번 = 0; 순번 < GETİRİ_BAĞ_DEĞ_SAY; 순번++) hedef_değer_konum[순번 + 1] = 바이트들[순번]; return GETİRİ_BAĞ_DEĞ_SAY; }
        if (GETİRİ_BAĞ_DEĞ_SAY != -2) return (uint32_t)GETİRİ_BAĞ_DEĞ_SAY;
    }
    int dosya_tanıtıcısı = 꾸러미사용중 ? -2 : (int32_t)araç_açık(İsim, 0);
    if (dosya_tanıtıcısı < 0) {
        char veri_konum[512]; int hata = yol(İsim, veri_konum); if (hata) return (uint32_t)hata;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Sonraki_Ofset = 자바클래스들[순번].İsim; unsigned 안쪽순번 = 0;
            while (veri_konum[안쪽순번] && veri_konum[안쪽순번] == Sonraki_Ofset[안쪽순번]) 안쪽순번++;
            if (veri_konum[안쪽순번] || Sonraki_Ofset[안쪽순번]) continue;
            makine_Word *hedef_değer_konum = (makine_Word *)hedef_veri_ADRES;
            if (hedef_değer_konum[0] < 자바클래스들[순번].Boyut) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Boyut; 안쪽순번++) hedef_değer_konum[안쪽순번 + 1] = 자바클래스들[순번].veri[안쪽순번];
            return 자바클래스들[순번].Boyut;
        }
        return (uint32_t)dosya_tanıtıcısı;
    }
    makine_Word *첫째값 = (makine_Word *)hedef_veri_ADRES;
    intptr_t Boyut = 호출(9, dosya_tanıtıcısı, 0, 0), Bitenler_tutar = 0;
    if (Boyut < 0 || (makine_Word)Boyut > 첫째값[0]) { araç_Kapat(dosya_tanıtıcısı); return (uint32_t)(Boyut < 0 ? Boyut : -27); }
    unsigned char veri_bloğu[256];
    while (Bitenler_tutar < Boyut) {
        intptr_t öğe_BAĞ_DEĞ_SAY = 호출(2, dosya_tanıtıcısı, (makine_Word)veri_bloğu, Boyut - Bitenler_tutar < 256 ? Boyut - Bitenler_tutar : 256);
        if (öğe_BAĞ_DEĞ_SAY <= 0) { araç_Kapat(dosya_tanıtıcısı); return (uint32_t)(öğe_BAĞ_DEĞ_SAY ? öğe_BAĞ_DEĞ_SAY : -5); }
        for (intptr_t 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) 첫째값[1 + Bitenler_tutar + 순번] = veri_bloğu[순번];
        Bitenler_tutar += öğe_BAĞ_DEĞ_SAY;
    }
    araç_Kapat(dosya_tanıtıcısı); return Bitenler_tutar;
}
makine_Word araç_yazma(makine_Word İsim, makine_Word 원본자료, makine_Word girdi_BAĞ_DEĞ_SAY) {
    const makine_Word *첫째값 = (const makine_Word *)원본자료;
    if (girdi_BAĞ_DEĞ_SAY > 첫째값[0] || girdi_BAĞ_DEĞ_SAY > 16384) return (uint32_t)-27;
    int dosya_tanıtıcısı = (int32_t)araç_açık(İsim, 577); if (dosya_tanıtıcısı < 0) return (uint32_t)dosya_tanıtıcısı;
    unsigned char veri_bloğu[256]; makine_Word Bitenler_tutar = 0;
    while (Bitenler_tutar < girdi_BAĞ_DEĞ_SAY) {
        makine_Word öğe_BAĞ_DEĞ_SAY = girdi_BAĞ_DEĞ_SAY - Bitenler_tutar < 256 ? girdi_BAĞ_DEĞ_SAY - Bitenler_tutar : 256;
        for (makine_Word 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) veri_bloğu[순번] = 첫째값[1 + Bitenler_tutar + 순번];
        intptr_t sonuç = 호출(1, dosya_tanıtıcısı, (makine_Word)veri_bloğu, öğe_BAĞ_DEĞ_SAY);
        if (sonuç <= 0) { araç_Kapat(dosya_tanıtıcısı); return (uint32_t)(sonuç ? sonuç : -5); }
        Bitenler_tutar += sonuç;
    }
    araç_Kapat(dosya_tanıtıcısı); return girdi_BAĞ_DEĞ_SAY;
}
makine_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
makine_Word araç_bağımsız_değişken(makine_Word ARA_Dizin) {
    static const makine_Word boş_değer[1] = {0};
    if (ARA_Dizin >= 8) return (makine_Word)boş_değer;
    unsigned char artış[256]; intptr_t öğe_BAĞ_DEĞ_SAY;
    if (꾸러미사용중 && ARA_Dizin == 0) { const char *veri_konum = 꾸러미진입클래스(); öğe_BAĞ_DEĞ_SAY = 0; while (veri_konum[öğe_BAĞ_DEĞ_SAY] && öğe_BAĞ_DEĞ_SAY < 255) { artış[öğe_BAĞ_DEĞ_SAY] = veri_konum[öğe_BAĞ_DEĞ_SAY]; öğe_BAĞ_DEĞ_SAY++; } }
    else öğe_BAĞ_DEĞ_SAY = 호출(15, ARA_Dizin + (꾸러미사용중 ? 꾸러미인수이동 : 0), (makine_Word)artış, sizeof(artış));
    if (öğe_BAĞ_DEĞ_SAY < 0) return (makine_Word)boş_değer;
    makine_Word *KR_veri = 전달인수[ARA_Dizin]; unsigned girdi_BAĞ_DEĞ_SAY = 0;
    for (intptr_t 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY;) {
        unsigned kod_noktası = artış[순번++], 더있음 = kod_noktası < 128 ? 0 : kod_noktası >= 0xc2 && kod_noktası < 0xe0 ? 1 : kod_noktası < 0xf0 && kod_noktası >= 0xe0 ? 2 : kod_noktası >= 0xf0 && kod_noktası <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > öğe_BAĞ_DEĞ_SAY) { KR_veri[++girdi_BAĞ_DEĞ_SAY] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kod_noktası &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (artış[순번] & 0xc0) == 0x80) { kod_noktası = (kod_noktası << 6) | (artış[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kod_noktası < 최소값 || kod_noktası > 0x10ffff || (kod_noktası >= 0xd800 && kod_noktası <= 0xdfff)) kod_noktası = 0xfffd;
        if (kod_noktası >= 65536) { kod_noktası -= 65536; KR_veri[++girdi_BAĞ_DEĞ_SAY] = 0xd800 | (kod_noktası >> 10); KR_veri[++girdi_BAĞ_DEĞ_SAY] = 0xdc00 | (kod_noktası & 1023); }
        else KR_veri[++girdi_BAĞ_DEĞ_SAY] = kod_noktası;
    }
    KR_veri[0] = girdi_BAĞ_DEĞ_SAY; return (makine_Word)KR_veri;
}
makine_Word araç_Tip(void) { return alan_değer; }
void 커널중단(const char *uyarı_SMS) {
    const char *veri_konum = uyarı_SMS; while (*veri_konum) veri_konum++;
    바이트들("Java tool runtime error: ", 25); 바이트들(uyarı_SMS, veri_konum - uyarı_SMS); karakter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_kullanıcı_program(int metot_mod) {
    alan_değer = metot_mod;
    unsigned char 첫항목[256]; intptr_t öğe_BAĞ_DEĞ_SAY = 호출(15, 0, (makine_Word)첫항목, sizeof(첫항목));
    if (metot_mod == 2 || (metot_mod == 1 && öğe_BAĞ_DEĞ_SAY == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metot_mod == 2 ? 0 : 1;
        char Dosya_girdi_ad[256]; intptr_t süre_veri = 호출(15, 꾸러미인수이동, (makine_Word)Dosya_girdi_ad, sizeof(Dosya_girdi_ad));
        if (süre_veri <= 0 || 꾸러미열기(Dosya_girdi_ad) < 0) {
            static const char hata[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(hata, sizeof(hata) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int sonuç = 자바진입();
    if (대기중짝글자) karakter(0xfffd);
    return sonuç;
}

// UDP는 Öz 커널의 SVC를 통과하며 geçerli_öğe 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Aile, bağlantı_noktası_numarası; uint32_t ADRES; unsigned char sıfır_değer[8]; };
static struct 자바주소 UDP_ADRES(unsigned bağlantı_noktası_numarası) {
    struct 자바주소 첫째값 = {2, (uint16_t)((bağlantı_noktası_numarası << 8) | (bağlantı_noktası_numarası >> 8)), 0x0100007f, {0}}; return 첫째값;
}
makine_Word araç_UDP_açık(makine_Word bağlantı_noktası_numarası) {
    intptr_t dosya_tanıtıcısı = 호출(32, 2, 2, 17); if (dosya_tanıtıcısı < 0) return (uint32_t)dosya_tanıtıcısı;
    struct 자바주소 첫째값 = UDP_ADRES(bağlantı_noktası_numarası);
    첫째값.ADRES = 0;
    intptr_t Durum_değer = 호출(33, dosya_tanıtıcısı, (makine_Word)&첫째값, sizeof(첫째값));
    if (Durum_değer < 0) { araç_Kapat(dosya_tanıtıcısı); return (uint32_t)Durum_değer; }
    return dosya_tanıtıcısı;
}
makine_Word araç_UDP_göndermek(makine_Word dosya_tanıtıcısı, makine_Word bağlantı_noktası_numarası, makine_Word DİZİ_değer, makine_Word süre_değer) {
    const makine_Word *원본주소 = (const makine_Word *)DİZİ_değer; unsigned char veri[512];
    if (süre_değer > 512 || süre_değer > 원본주소[0]) return (uint32_t)-90;
    for (makine_Word 순번 = 0; 순번 < süre_değer; 순번++) veri[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRES(bağlantı_noktası_numarası);
    return (uint32_t)사용자호출(34, dosya_tanıtıcısı, (makine_Word)veri, süre_değer, 0, (makine_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t öğe_BAĞ_DEĞ_SAY) { return (öğe_BAĞ_DEĞ_SAY>>24)|((öğe_BAĞ_DEĞ_SAY>>8)&0xff00)|((öğe_BAĞ_DEĞ_SAY<<8)&0xff0000)|(öğe_BAĞ_DEĞ_SAY<<24); }
makine_Word araç_UDP_göndermek_ADRES(makine_Word dosya_tanıtıcısı, makine_Word ADRES, makine_Word bağlantı_noktası_numarası, makine_Word DİZİ_değer, makine_Word süre_değer) {
    const makine_Word *원본주소 = (const makine_Word *)DİZİ_değer; unsigned char veri[512];
    if (süre_değer > 512 || süre_değer > 원본주소[0]) return (uint32_t)-90;
    for (makine_Word 순번 = 0; 순번 < süre_değer; 순번++) veri[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADRES(bağlantı_noktası_numarası); 첫째값.ADRES = 바이트순서뒤집기(ADRES);
    return (uint32_t)사용자호출(34, dosya_tanıtıcısı, (makine_Word)veri, süre_değer, 0, (makine_Word)&첫째값, sizeof(첫째값));
}
makine_Word araç_bağla(makine_Word dosya_tanıtıcısı, makine_Word ADRES, makine_Word bağlantı_noktası_numarası) {
    struct 자바주소 첫째값 = UDP_ADRES(bağlantı_noktası_numarası); 첫째값.ADRES = 바이트순서뒤집기(ADRES);
    uint32_t çalıştır = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t sonuç = 호출(37, dosya_tanıtıcısı, (makine_Word)&첫째값, sizeof(첫째값));
        if (sonuç != -115) return (uint32_t)sonuç;
        if ((uint32_t)(호출(7, 0, 0, 0) - çalıştır) >= 1000) return (uint32_t)-110;
    }
}
makine_Word 도구전문받기(makine_Word dosya_tanıtıcısı, makine_Word DİZİ_değer, makine_Word tampon_kapasite) {
    makine_Word *hedef_ADRES_08bbd577 = (makine_Word *)DİZİ_değer; unsigned char veri[512];
    if (tampon_kapasite > 512 || hedef_ADRES_08bbd577[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned süre_veri = sizeof(첫째값);
    intptr_t öğe_BAĞ_DEĞ_SAY = 사용자호출(35, dosya_tanıtıcısı, (makine_Word)veri, tampon_kapasite, 0, (makine_Word)&첫째값, (makine_Word)&süre_veri);
    if (öğe_BAĞ_DEĞ_SAY >= 0) { for (intptr_t 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) hedef_ADRES_08bbd577[순번 + 1] = veri[순번]; hedef_ADRES_08bbd577[513] = (첫째값.bağlantı_noktası_numarası << 8 | 첫째값.bağlantı_noktası_numarası >> 8) & 65535; hedef_ADRES_08bbd577[514] = 바이트순서뒤집기(첫째값.ADRES); }
    return (uint32_t)öğe_BAĞ_DEĞ_SAY;
}
makine_Word araç_UDP_taşımak(makine_Word dosya_tanıtıcısı) {
    struct 자바주소 첫째값; unsigned süre_veri = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, dosya_tanıtıcısı, (makine_Word)&첫째값, (makine_Word)&süre_veri);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.bağlantı_noktası_numarası << 8 | 첫째값.bağlantı_noktası_numarası >> 8) & 65535);
}
makine_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
makine_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
makine_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
makine_Word araç_grafik_bekle(void) { return (uint32_t)화면키기다리기(); }
makine_Word araç_dikdörtgen(makine_Word x_koordinatı, makine_Word Y_koordinat, makine_Word 너비값, makine_Word 높이값, makine_Word 색상) {
    return (uint32_t)사용자호출(13, x_koordinatı, Y_koordinat, 색상, 너비값, 높이값, 0);
}

makine_Word araç_akış(makine_Word Eylem,makine_Word dosya_tanıtıcısı,makine_Word değer){
    if(Eylem==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADRES(değer);
    if(Eylem==1){첫째값.ADRES=0;intptr_t 반환값=호출(33,dosya_tanıtıcısı,(makine_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,dosya_tanıtıcısı,4,0));}
    if(Eylem==2)return (uint32_t)호출(37,dosya_tanıtıcısı,(makine_Word)&첫째값,sizeof(첫째값));
    if(Eylem==3)return (uint32_t)호출(39,dosya_tanıtıcısı,0,0);
    if(Eylem==4)return araç_UDP_taşımak(dosya_tanıtıcısı);
    if(Eylem==5)return (uint32_t)호출(40,dosya_tanıtıcısı,0,0);
    return (uint32_t)-22;
}
makine_Word araç_GUI(makine_Word Eylem,makine_Word tanımlayıcı_değer,makine_Word 첫째값,makine_Word SANİYE_değer,makine_Word kod_noktası,makine_Word hedef_veri){return (uint32_t)사용자호출(20,Eylem,tanımlayıcı_değer,첫째값,SANİYE_değer,kod_noktası,hedef_veri);}
makine_Word araç_GUI_SMS(makine_Word tanımlayıcı_değer,makine_Word DİZİ_değer,makine_Word öğe_BAĞ_DEĞ_SAY){
    const makine_Word *원본주소=(const makine_Word *)DİZİ_değer;uint32_t veri[127];unsigned girdi_BAĞ_DEĞ_SAY=0;
    if(öğe_BAĞ_DEĞ_SAY>원본주소[0])return (uint32_t)-22;
    for(makine_Word 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++){unsigned karakter_kodlaması=원본주소[순번+1];if(karakter_kodlaması>=0xd800&&karakter_kodlaması<=0xdbff&&순번+1<öğe_BAĞ_DEĞ_SAY){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;karakter_kodlaması=0x10000+((karakter_kodlaması-0xd800)<<10)+낮은값-0xdc00;}if(girdi_BAĞ_DEĞ_SAY==127)return (uint32_t)-22;veri[girdi_BAĞ_DEĞ_SAY++]=karakter_kodlaması;}
    return (uint32_t)사용자호출(21,tanımlayıcı_değer,(makine_Word)veri,girdi_BAĞ_DEĞ_SAY,0,0,0);
}
