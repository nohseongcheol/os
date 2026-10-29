#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 FAYL/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "paket.h"
typedef uintptr_t maşın_Söz;
static int sahə_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static maşın_Söz 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned element_COUNT, maşın_Söz 첫째값, maşın_Söz SECOND_VALUE, maşın_Söz simvol_kodu) {
    return 사용자호출(element_COUNT, 첫째값, SECOND_VALUE, simvol_kodu, 0, 0, 0);
}
static void 바이트들(const char *verilənlər_yerinə_qoymaq, size_t element_COUNT) { 호출(1, 1, (maşın_Söz)verilənlər_yerinə_qoymaq, element_COUNT); }
static void simvol_a5317f02(unsigned simvol_kodu) {
    unsigned char verilənlər[4]; unsigned element_COUNT = 0;
    if (simvol_kodu < 128) verilənlər[element_COUNT++] = simvol_kodu;
    else if (simvol_kodu < 2048) { verilənlər[element_COUNT++] = 0xc0 | (simvol_kodu >> 6); verilənlər[element_COUNT++] = 0x80 | (simvol_kodu & 63); }
    else if (simvol_kodu < 65536) { verilənlər[element_COUNT++] = 0xe0 | (simvol_kodu >> 12); verilənlər[element_COUNT++] = 0x80 | ((simvol_kodu >> 6) & 63); verilənlər[element_COUNT++] = 0x80 | (simvol_kodu & 63); }
    else { verilənlər[element_COUNT++] = 0xf0 | (simvol_kodu >> 18); verilənlər[element_COUNT++] = 0x80 | ((simvol_kodu >> 12) & 63); verilənlər[element_COUNT++] = 0x80 | ((simvol_kodu >> 6) & 63); verilənlər[element_COUNT++] = 0x80 | (simvol_kodu & 63); }
    바이트들((const char *)verilənlər, element_COUNT);
}
maşın_Söz alət_simvol(maşın_Söz VALUE) {
    unsigned simvol_kodu = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (simvol_kodu >= 0xdc00 && simvol_kodu <= 0xdfff) { simvol_a5317f02(0x10000 + ((높은부분 - 0xd800) << 10) + simvol_kodu - 0xdc00); return 1; }
        simvol_a5317f02(0xfffd);
    }
    if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdbff) 대기중짝글자 = simvol_kodu;
    else simvol_a5317f02(simvol_kodu > 0x10ffff || (simvol_kodu >= 0xdc00 && simvol_kodu <= 0xdfff) ? 0xfffd : simvol_kodu);
    return 1;
}
maşın_Söz 도구출력(maşın_Söz VALUE) {
    const maşın_Söz *sətir_verilənlər = (const maşın_Söz *)VALUE;
    for (maşın_Söz 순번 = 0; 순번 < sətir_verilənlər[0]; 순번++) alət_simvol(sətir_verilənlər[순번 + 1]);
    return sətir_verilənlər[0];
}
static int Cığır(maşın_Söz obyekt_İstinad, char ölçü_verilənlər[512]) {
    const maşın_Söz *첫째값 = (const maşın_Söz *)obyekt_İstinad;
    unsigned 사용량 = 0;
    for (maşın_Söz 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned simvol_kodu = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metod_MODE 경로와 호환한다.
        if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; simvol_kodu = 0x10000 + ((simvol_kodu - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdfff) return -22;
        unsigned element_COUNT = simvol_kodu < 128 ? 1 : simvol_kodu < 2048 ? 2 : simvol_kodu < 65536 ? 3 : 4;
        if (사용량 + element_COUNT > 511) return -36;
        if (element_COUNT == 1) ölçü_verilənlər[사용량++] = simvol_kodu;
        else {
            ölçü_verilənlər[사용량++] = (element_COUNT == 2 ? 0xc0 : element_COUNT == 3 ? 0xe0 : 0xf0) | (simvol_kodu >> (6 * (element_COUNT - 1)));
            for (unsigned 안쪽순번 = element_COUNT - 1; 안쪽순번; 안쪽순번--) ölçü_verilənlər[사용량++] = 0x80 | ((simvol_kodu >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    ölçü_verilənlər[사용량] = 0; return 사용량 ? 0 : -22;
}
maşın_Söz alət_açmaq(maşın_Söz Ad, maşın_Söz konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti) {
    char verilənlər_yerinə_qoymaq[512]; int XƏTA = Cığır(Ad, verilənlər_yerinə_qoymaq);
    return (uint32_t)(XƏTA ? XƏTA : 호출(3, (maşın_Söz)verilənlər_yerinə_qoymaq, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, 0));
}
maşın_Söz alət_bağlamaq(maşın_Söz fayl_tutacaq) { return (uint32_t)호출(4, fayl_tutacaq, 0, 0); }
maşın_Söz 도구바이트읽기(maşın_Söz fayl_tutacaq) {
    unsigned char SECOND_VALUE; intptr_t element_COUNT = 호출(2, fayl_tutacaq, (maşın_Söz)&SECOND_VALUE, 1);
    return (uint32_t)(element_COUNT == 1 ? SECOND_VALUE : element_COUNT == 0 ? 256 : element_COUNT);
}
maşın_Söz alət_yazmaq_bayt(maşın_Söz fayl_tutacaq, maşın_Söz VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, fayl_tutacaq, (maşın_Söz)&SECOND_VALUE, 1);
}
maşın_Söz 도구읽기(maşın_Söz Ad, maşın_Söz təyinat_verilənlər_ünvan) {
    if (꾸러미사용중) {
        char verilənlər_yerinə_qoymaq[512]; int XƏTA = Cığır(Ad, verilənlər_yerinə_qoymaq); if (XƏTA) return (uint32_t)XƏTA;
        unsigned element_COUNT = 0; while (verilənlər_yerinə_qoymaq[element_COUNT]) element_COUNT++;
        if (element_COUNT >= 6) for (unsigned 순번 = 0; 순번 < element_COUNT - 6; 순번++) if (verilənlər_yerinə_qoymaq[순번] == '.') verilənlər_yerinə_qoymaq[순번] = '/';
        unsigned char 바이트들[16384]; maşın_Söz *təyinat_VALUE_yerinə_qoymaq = (maşın_Söz *)təyinat_verilənlər_ünvan;
        int RECEIVED_COUNT = 꾸러미읽기(verilənlər_yerinə_qoymaq, 바이트들, təyinat_VALUE_yerinə_qoymaq[0] < sizeof(바이트들) ? təyinat_VALUE_yerinə_qoymaq[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) təyinat_VALUE_yerinə_qoymaq[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int fayl_tutacaq = 꾸러미사용중 ? -2 : (int32_t)alət_açmaq(Ad, 0);
    if (fayl_tutacaq < 0) {
        char verilənlər_yerinə_qoymaq[512]; int XƏTA = Cığır(Ad, verilənlər_yerinə_qoymaq); if (XƏTA) return (uint32_t)XƏTA;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Sonrakı_OFFSET = 자바클래스들[순번].Ad; unsigned 안쪽순번 = 0;
            while (verilənlər_yerinə_qoymaq[안쪽순번] && verilənlər_yerinə_qoymaq[안쪽순번] == Sonrakı_OFFSET[안쪽순번]) 안쪽순번++;
            if (verilənlər_yerinə_qoymaq[안쪽순번] || Sonrakı_OFFSET[안쪽순번]) continue;
            maşın_Söz *təyinat_VALUE_yerinə_qoymaq = (maşın_Söz *)təyinat_verilənlər_ünvan;
            if (təyinat_VALUE_yerinə_qoymaq[0] < 자바클래스들[순번].Böyüklük) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Böyüklük; 안쪽순번++) təyinat_VALUE_yerinə_qoymaq[안쪽순번 + 1] = 자바클래스들[순번].verilənlər[안쪽순번];
            return 자바클래스들[순번].Böyüklük;
        }
        return (uint32_t)fayl_tutacaq;
    }
    maşın_Söz *첫째값 = (maşın_Söz *)təyinat_verilənlər_ünvan;
    intptr_t Böyüklük = 호출(9, fayl_tutacaq, 0, 0), 완료량 = 0;
    if (Böyüklük < 0 || (maşın_Söz)Böyüklük > 첫째값[0]) { alət_bağlamaq(fayl_tutacaq); return (uint32_t)(Böyüklük < 0 ? Böyüklük : -27); }
    unsigned char verilənlər_blokla[256];
    while (완료량 < Böyüklük) {
        intptr_t element_COUNT = 호출(2, fayl_tutacaq, (maşın_Söz)verilənlər_blokla, Böyüklük - 완료량 < 256 ? Böyüklük - 완료량 : 256);
        if (element_COUNT <= 0) { alət_bağlamaq(fayl_tutacaq); return (uint32_t)(element_COUNT ? element_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = verilənlər_blokla[순번];
        완료량 += element_COUNT;
    }
    alət_bağlamaq(fayl_tutacaq); return 완료량;
}
maşın_Söz alət_yazmaq(maşın_Söz Ad, maşın_Söz 원본자료, maşın_Söz daxiletmə_COUNT) {
    const maşın_Söz *첫째값 = (const maşın_Söz *)원본자료;
    if (daxiletmə_COUNT > 첫째값[0] || daxiletmə_COUNT > 16384) return (uint32_t)-27;
    int fayl_tutacaq = (int32_t)alət_açmaq(Ad, 577); if (fayl_tutacaq < 0) return (uint32_t)fayl_tutacaq;
    unsigned char verilənlər_blokla[256]; maşın_Söz 완료량 = 0;
    while (완료량 < daxiletmə_COUNT) {
        maşın_Söz element_COUNT = daxiletmə_COUNT - 완료량 < 256 ? daxiletmə_COUNT - 완료량 : 256;
        for (maşın_Söz 순번 = 0; 순번 < element_COUNT; 순번++) verilənlər_blokla[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t ölçü = 호출(1, fayl_tutacaq, (maşın_Söz)verilənlər_blokla, element_COUNT);
        if (ölçü <= 0) { alət_bağlamaq(fayl_tutacaq); return (uint32_t)(ölçü ? ölçü : -5); }
        완료량 += ölçü;
    }
    alət_bağlamaq(fayl_tutacaq); return daxiletmə_COUNT;
}
maşın_Söz 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
maşın_Söz alət_arqument(maşın_Söz LOOKUP_INDEX) {
    static const maşın_Söz boş_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (maşın_Söz)boş_VALUE;
    unsigned char 입력결과[256]; intptr_t element_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *verilənlər_yerinə_qoymaq = 꾸러미진입클래스(); element_COUNT = 0; while (verilənlər_yerinə_qoymaq[element_COUNT] && element_COUNT < 255) { 입력결과[element_COUNT] = verilənlər_yerinə_qoymaq[element_COUNT]; element_COUNT++; } }
    else element_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (maşın_Söz)입력결과, sizeof(입력결과));
    if (element_COUNT < 0) return (maşın_Söz)boş_VALUE;
    maşın_Söz *ölçü_verilənlər = 전달인수[LOOKUP_INDEX]; unsigned daxiletmə_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < element_COUNT;) {
        unsigned simvol_kodu = 입력결과[순번++], 더있음 = simvol_kodu < 128 ? 0 : simvol_kodu >= 0xc2 && simvol_kodu < 0xe0 ? 1 : simvol_kodu < 0xf0 && simvol_kodu >= 0xe0 ? 2 : simvol_kodu >= 0xf0 && simvol_kodu <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > element_COUNT) { ölçü_verilənlər[++daxiletmə_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) simvol_kodu &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { simvol_kodu = (simvol_kodu << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || simvol_kodu < 최소값 || simvol_kodu > 0x10ffff || (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdfff)) simvol_kodu = 0xfffd;
        if (simvol_kodu >= 65536) { simvol_kodu -= 65536; ölçü_verilənlər[++daxiletmə_COUNT] = 0xd800 | (simvol_kodu >> 10); ölçü_verilənlər[++daxiletmə_COUNT] = 0xdc00 | (simvol_kodu & 1023); }
        else ölçü_verilənlər[++daxiletmə_COUNT] = simvol_kodu;
    }
    ölçü_verilənlər[0] = daxiletmə_COUNT; return (maşın_Söz)ölçü_verilənlər;
}
maşın_Söz 도구분류(void) { return sahə_VALUE; }
void 커널중단(const char *알림문) {
    const char *verilənlər_yerinə_qoymaq = 알림문; while (*verilənlər_yerinə_qoymaq) verilənlər_yerinə_qoymaq++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, verilənlər_yerinə_qoymaq - 알림문); simvol_a5317f02(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Başla_istifadəçi_proqram(int metod_MODE) {
    sahə_VALUE = metod_MODE;
    unsigned char 첫항목[256]; intptr_t element_COUNT = 호출(15, 0, (maşın_Söz)첫항목, sizeof(첫항목));
    if (metod_MODE == 2 || (metod_MODE == 1 && element_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metod_MODE == 2 ? 0 : 1;
        char fayl_daxiletmə_ad[256]; intptr_t uzunluq_verilənlər = 호출(15, 꾸러미인수이동, (maşın_Söz)fayl_daxiletmə_ad, sizeof(fayl_daxiletmə_ad));
        if (uzunluq_verilənlər <= 0 || 꾸러미열기(fayl_daxiletmə_ad) < 0) {
            static const char XƏTA[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(XƏTA, sizeof(XƏTA) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int ölçü = 자바진입();
    if (대기중짝글자) simvol_a5317f02(0xfffd);
    return ölçü;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Ailə, 접속번호; uint32_t ünvan; unsigned char 영값[8]; };
static struct 자바주소 UDP_ünvan(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
maşın_Söz alət_UDP_açmaq(maşın_Söz 접속번호) {
    intptr_t fayl_tutacaq = 호출(32, 2, 2, 17); if (fayl_tutacaq < 0) return (uint32_t)fayl_tutacaq;
    struct 자바주소 첫째값 = UDP_ünvan(접속번호);
    첫째값.ünvan = 0;
    intptr_t vəziyyət_VALUE = 호출(33, fayl_tutacaq, (maşın_Söz)&첫째값, sizeof(첫째값));
    if (vəziyyət_VALUE < 0) { alət_bağlamaq(fayl_tutacaq); return (uint32_t)vəziyyət_VALUE; }
    return fayl_tutacaq;
}
maşın_Söz alət_UDP_göndərmək(maşın_Söz fayl_tutacaq, maşın_Söz 접속번호, maşın_Söz ARRAY_VALUE, maşın_Söz uzunluq_VALUE) {
    const maşın_Söz *원본주소 = (const maşın_Söz *)ARRAY_VALUE; unsigned char verilənlər[512];
    if (uzunluq_VALUE > 512 || uzunluq_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (maşın_Söz 순번 = 0; 순번 < uzunluq_VALUE; 순번++) verilənlər[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ünvan(접속번호);
    return (uint32_t)사용자호출(34, fayl_tutacaq, (maşın_Söz)verilənlər, uzunluq_VALUE, 0, (maşın_Söz)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t element_COUNT) { return (element_COUNT>>24)|((element_COUNT>>8)&0xff00)|((element_COUNT<<8)&0xff0000)|(element_COUNT<<24); }
maşın_Söz alət_UDP_göndərmək_ünvan(maşın_Söz fayl_tutacaq, maşın_Söz ünvan, maşın_Söz 접속번호, maşın_Söz ARRAY_VALUE, maşın_Söz uzunluq_VALUE) {
    const maşın_Söz *원본주소 = (const maşın_Söz *)ARRAY_VALUE; unsigned char verilənlər[512];
    if (uzunluq_VALUE > 512 || uzunluq_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (maşın_Söz 순번 = 0; 순번 < uzunluq_VALUE; 순번++) verilənlər[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ünvan(접속번호); 첫째값.ünvan = 바이트순서뒤집기(ünvan);
    return (uint32_t)사용자호출(34, fayl_tutacaq, (maşın_Söz)verilənlər, uzunluq_VALUE, 0, (maşın_Söz)&첫째값, sizeof(첫째값));
}
maşın_Söz alət_QOŞUN(maşın_Söz fayl_tutacaq, maşın_Söz ünvan, maşın_Söz 접속번호) {
    struct 자바주소 첫째값 = UDP_ünvan(접속번호); 첫째값.ünvan = 바이트순서뒤집기(ünvan);
    uint32_t İcra_Et = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t ölçü = 호출(37, fayl_tutacaq, (maşın_Söz)&첫째값, sizeof(첫째값));
        if (ölçü != -115) return (uint32_t)ölçü;
        if ((uint32_t)(호출(7, 0, 0, 0) - İcra_Et) >= 1000) return (uint32_t)-110;
    }
}
maşın_Söz 도구전문받기(maşın_Söz fayl_tutacaq, maşın_Söz ARRAY_VALUE, maşın_Söz 수용량) {
    maşın_Söz *təyinat_ünvan = (maşın_Söz *)ARRAY_VALUE; unsigned char verilənlər[512];
    if (수용량 > 512 || təyinat_ünvan[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned uzunluq_verilənlər = sizeof(첫째값);
    intptr_t element_COUNT = 사용자호출(35, fayl_tutacaq, (maşın_Söz)verilənlər, 수용량, 0, (maşın_Söz)&첫째값, (maşın_Söz)&uzunluq_verilənlər);
    if (element_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) təyinat_ünvan[순번 + 1] = verilənlər[순번]; təyinat_ünvan[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; təyinat_ünvan[514] = 바이트순서뒤집기(첫째값.ünvan); }
    return (uint32_t)element_COUNT;
}
maşın_Söz alət_UDP_port(maşın_Söz fayl_tutacaq) {
    struct 자바주소 첫째값; unsigned uzunluq_verilənlər = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fayl_tutacaq, (maşın_Söz)&첫째값, (maşın_Söz)&uzunluq_verilənlər);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
maşın_Söz 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
maşın_Söz 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
maşın_Söz 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
maşın_Söz alət_qrafik_elementlər_gözlə(void) { return (uint32_t)화면키기다리기(); }
maşın_Söz 도구사각형(maşın_Söz x_koordinatı, maşın_Söz Y_koordinat, maşın_Söz 너비값, maşın_Söz 높이값, maşın_Söz 색상) {
    return (uint32_t)사용자호출(13, x_koordinatı, Y_koordinat, 색상, 너비값, 높이값, 0);
}

maşın_Söz alət_axın(maşın_Söz Gedişat,maşın_Söz fayl_tutacaq,maşın_Söz VALUE){
    if(Gedişat==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ünvan(VALUE);
    if(Gedişat==1){첫째값.ünvan=0;intptr_t 반환값=호출(33,fayl_tutacaq,(maşın_Söz)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fayl_tutacaq,4,0));}
    if(Gedişat==2)return (uint32_t)호출(37,fayl_tutacaq,(maşın_Söz)&첫째값,sizeof(첫째값));
    if(Gedişat==3)return (uint32_t)호출(39,fayl_tutacaq,0,0);
    if(Gedişat==4)return alət_UDP_port(fayl_tutacaq);
    if(Gedişat==5)return (uint32_t)호출(40,fayl_tutacaq,0,0);
    return (uint32_t)-22;
}
maşın_Söz alət_GUI(maşın_Söz Gedişat,maşın_Söz identifikator_VALUE,maşın_Söz 첫째값,maşın_Söz SECOND_VALUE,maşın_Söz simvol_kodu,maşın_Söz təyinat_verilənlər){return (uint32_t)사용자호출(20,Gedişat,identifikator_VALUE,첫째값,SECOND_VALUE,simvol_kodu,təyinat_verilənlər);}
maşın_Söz alət_GUI_SMS(maşın_Söz identifikator_VALUE,maşın_Söz ARRAY_VALUE,maşın_Söz element_COUNT){
    const maşın_Söz *원본주소=(const maşın_Söz *)ARRAY_VALUE;uint32_t verilənlər[127];unsigned daxiletmə_COUNT=0;
    if(element_COUNT>원본주소[0])return (uint32_t)-22;
    for(maşın_Söz 순번=0;순번<element_COUNT;순번++){unsigned simvol_kodlaşdırma=원본주소[순번+1];if(simvol_kodlaşdırma>=0xd800&&simvol_kodlaşdırma<=0xdbff&&순번+1<element_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;simvol_kodlaşdırma=0x10000+((simvol_kodlaşdırma-0xd800)<<10)+낮은값-0xdc00;}if(daxiletmə_COUNT==127)return (uint32_t)-22;verilənlər[daxiletmə_COUNT++]=simvol_kodlaşdırma;}
    return (uint32_t)사용자호출(21,identifikator_VALUE,(maşın_Söz)verilənlər,daxiletmə_COUNT,0,0,0);
}
