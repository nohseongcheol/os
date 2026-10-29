#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fayl/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "to_plam.h"
typedef uintptr_t 기계낱말;
static int toifa_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static 기계낱말 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned element_COUNT, 기계낱말 첫째값, 기계낱말 SECOND_VALUE, 기계낱말 belgi_kodi) {
    return 사용자호출(element_COUNT, 첫째값, SECOND_VALUE, belgi_kodi, 0, 0, 0);
}
static void 바이트들(const char *ma_lumotlar_holat, size_t element_COUNT) { 호출(1, 1, (기계낱말)ma_lumotlar_holat, element_COUNT); }
static void belgi(unsigned belgi_kodi) {
    unsigned char ma_lumotlar[4]; unsigned element_COUNT = 0;
    if (belgi_kodi < 128) ma_lumotlar[element_COUNT++] = belgi_kodi;
    else if (belgi_kodi < 2048) { ma_lumotlar[element_COUNT++] = 0xc0 | (belgi_kodi >> 6); ma_lumotlar[element_COUNT++] = 0x80 | (belgi_kodi & 63); }
    else if (belgi_kodi < 65536) { ma_lumotlar[element_COUNT++] = 0xe0 | (belgi_kodi >> 12); ma_lumotlar[element_COUNT++] = 0x80 | ((belgi_kodi >> 6) & 63); ma_lumotlar[element_COUNT++] = 0x80 | (belgi_kodi & 63); }
    else { ma_lumotlar[element_COUNT++] = 0xf0 | (belgi_kodi >> 18); ma_lumotlar[element_COUNT++] = 0x80 | ((belgi_kodi >> 12) & 63); ma_lumotlar[element_COUNT++] = 0x80 | ((belgi_kodi >> 6) & 63); ma_lumotlar[element_COUNT++] = 0x80 | (belgi_kodi & 63); }
    바이트들((const char *)ma_lumotlar, element_COUNT);
}
기계낱말 vosita_belgi(기계낱말 VALUE) {
    unsigned belgi_kodi = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (belgi_kodi >= 0xdc00 && belgi_kodi <= 0xdfff) { belgi(0x10000 + ((높은부분 - 0xd800) << 10) + belgi_kodi - 0xdc00); return 1; }
        belgi(0xfffd);
    }
    if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdbff) 대기중짝글자 = belgi_kodi;
    else belgi(belgi_kodi > 0x10ffff || (belgi_kodi >= 0xdc00 && belgi_kodi <= 0xdfff) ? 0xfffd : belgi_kodi);
    return 1;
}
기계낱말 도구출력(기계낱말 VALUE) {
    const 기계낱말 *satr_ma_lumotlar = (const 기계낱말 *)VALUE;
    for (기계낱말 순번 = 0; 순번 < satr_ma_lumotlar[0]; 순번++) vosita_belgi(satr_ma_lumotlar[순번 + 1]);
    return satr_ma_lumotlar[0];
}
static int yo_l(기계낱말 obyekt_Ma_lumotnomalar, char o_lchov_ma_lumotlar[512]) {
    const 기계낱말 *첫째값 = (const 기계낱말 *)obyekt_Ma_lumotnomalar;
    unsigned 사용량 = 0;
    for (기계낱말 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned belgi_kodi = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] uslub_MODE 경로와 호환한다.
        if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; belgi_kodi = 0x10000 + ((belgi_kodi - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdfff) return -22;
        unsigned element_COUNT = belgi_kodi < 128 ? 1 : belgi_kodi < 2048 ? 2 : belgi_kodi < 65536 ? 3 : 4;
        if (사용량 + element_COUNT > 511) return -36;
        if (element_COUNT == 1) o_lchov_ma_lumotlar[사용량++] = belgi_kodi;
        else {
            o_lchov_ma_lumotlar[사용량++] = (element_COUNT == 2 ? 0xc0 : element_COUNT == 3 ? 0xe0 : 0xf0) | (belgi_kodi >> (6 * (element_COUNT - 1)));
            for (unsigned 안쪽순번 = element_COUNT - 1; 안쪽순번; 안쪽순번--) o_lchov_ma_lumotlar[사용량++] = 0x80 | ((belgi_kodi >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    o_lchov_ma_lumotlar[사용량] = 0; return 사용량 ? 0 : -22;
}
기계낱말 vosita_ochmoq(기계낱말 Nomi, 기계낱말 tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati) {
    char ma_lumotlar_holat[512]; int Xato = yo_l(Nomi, ma_lumotlar_holat);
    return (uint32_t)(Xato ? Xato : 호출(3, (기계낱말)ma_lumotlar_holat, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, 0));
}
기계낱말 vosita_yopmoq(기계낱말 fayl_deskriptor) { return (uint32_t)호출(4, fayl_deskriptor, 0, 0); }
기계낱말 도구바이트읽기(기계낱말 fayl_deskriptor) {
    unsigned char SECOND_VALUE; intptr_t element_COUNT = 호출(2, fayl_deskriptor, (기계낱말)&SECOND_VALUE, 1);
    return (uint32_t)(element_COUNT == 1 ? SECOND_VALUE : element_COUNT == 0 ? 256 : element_COUNT);
}
기계낱말 vosita_yozmoq_bayt(기계낱말 fayl_deskriptor, 기계낱말 VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, fayl_deskriptor, (기계낱말)&SECOND_VALUE, 1);
}
기계낱말 도구읽기(기계낱말 Nomi, 기계낱말 ko_chirish_joyi_ma_lumotlar_manzil) {
    if (꾸러미사용중) {
        char ma_lumotlar_holat[512]; int Xato = yo_l(Nomi, ma_lumotlar_holat); if (Xato) return (uint32_t)Xato;
        unsigned element_COUNT = 0; while (ma_lumotlar_holat[element_COUNT]) element_COUNT++;
        if (element_COUNT >= 6) for (unsigned 순번 = 0; 순번 < element_COUNT - 6; 순번++) if (ma_lumotlar_holat[순번] == '.') ma_lumotlar_holat[순번] = '/';
        unsigned char 바이트들[16384]; 기계낱말 *ko_chirish_joyi_VALUE_holat = (기계낱말 *)ko_chirish_joyi_ma_lumotlar_manzil;
        int RECEIVED_COUNT = 꾸러미읽기(ma_lumotlar_holat, 바이트들, ko_chirish_joyi_VALUE_holat[0] < sizeof(바이트들) ? ko_chirish_joyi_VALUE_holat[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) ko_chirish_joyi_VALUE_holat[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int fayl_deskriptor = 꾸러미사용중 ? -2 : (int32_t)vosita_ochmoq(Nomi, 0);
    if (fayl_deskriptor < 0) {
        char ma_lumotlar_holat[512]; int Xato = yo_l(Nomi, ma_lumotlar_holat); if (Xato) return (uint32_t)Xato;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Keyingi_OFFSET = 자바클래스들[순번].Nomi; unsigned 안쪽순번 = 0;
            while (ma_lumotlar_holat[안쪽순번] && ma_lumotlar_holat[안쪽순번] == Keyingi_OFFSET[안쪽순번]) 안쪽순번++;
            if (ma_lumotlar_holat[안쪽순번] || Keyingi_OFFSET[안쪽순번]) continue;
            기계낱말 *ko_chirish_joyi_VALUE_holat = (기계낱말 *)ko_chirish_joyi_ma_lumotlar_manzil;
            if (ko_chirish_joyi_VALUE_holat[0] < 자바클래스들[순번].Hajmi) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Hajmi; 안쪽순번++) ko_chirish_joyi_VALUE_holat[안쪽순번 + 1] = 자바클래스들[순번].ma_lumotlar[안쪽순번];
            return 자바클래스들[순번].Hajmi;
        }
        return (uint32_t)fayl_deskriptor;
    }
    기계낱말 *첫째값 = (기계낱말 *)ko_chirish_joyi_ma_lumotlar_manzil;
    intptr_t Hajmi = 호출(9, fayl_deskriptor, 0, 0), 완료량 = 0;
    if (Hajmi < 0 || (기계낱말)Hajmi > 첫째값[0]) { vosita_yopmoq(fayl_deskriptor); return (uint32_t)(Hajmi < 0 ? Hajmi : -27); }
    unsigned char ma_lumotlar_bloklash[256];
    while (완료량 < Hajmi) {
        intptr_t element_COUNT = 호출(2, fayl_deskriptor, (기계낱말)ma_lumotlar_bloklash, Hajmi - 완료량 < 256 ? Hajmi - 완료량 : 256);
        if (element_COUNT <= 0) { vosita_yopmoq(fayl_deskriptor); return (uint32_t)(element_COUNT ? element_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = ma_lumotlar_bloklash[순번];
        완료량 += element_COUNT;
    }
    vosita_yopmoq(fayl_deskriptor); return 완료량;
}
기계낱말 vosita_yozmoq(기계낱말 Nomi, 기계낱말 원본자료, 기계낱말 kiritish_COUNT) {
    const 기계낱말 *첫째값 = (const 기계낱말 *)원본자료;
    if (kiritish_COUNT > 첫째값[0] || kiritish_COUNT > 16384) return (uint32_t)-27;
    int fayl_deskriptor = (int32_t)vosita_ochmoq(Nomi, 577); if (fayl_deskriptor < 0) return (uint32_t)fayl_deskriptor;
    unsigned char ma_lumotlar_bloklash[256]; 기계낱말 완료량 = 0;
    while (완료량 < kiritish_COUNT) {
        기계낱말 element_COUNT = kiritish_COUNT - 완료량 < 256 ? kiritish_COUNT - 완료량 : 256;
        for (기계낱말 순번 = 0; 순번 < element_COUNT; 순번++) ma_lumotlar_bloklash[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t o_lchov = 호출(1, fayl_deskriptor, (기계낱말)ma_lumotlar_bloklash, element_COUNT);
        if (o_lchov <= 0) { vosita_yopmoq(fayl_deskriptor); return (uint32_t)(o_lchov ? o_lchov : -5); }
        완료량 += o_lchov;
    }
    vosita_yopmoq(fayl_deskriptor); return kiritish_COUNT;
}
기계낱말 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
기계낱말 vosita_dalil(기계낱말 LOOKUP_INDEX) {
    static const 기계낱말 bo_sh_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (기계낱말)bo_sh_VALUE;
    unsigned char 입력결과[256]; intptr_t element_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *ma_lumotlar_holat = 꾸러미진입클래스(); element_COUNT = 0; while (ma_lumotlar_holat[element_COUNT] && element_COUNT < 255) { 입력결과[element_COUNT] = ma_lumotlar_holat[element_COUNT]; element_COUNT++; } }
    else element_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (기계낱말)입력결과, sizeof(입력결과));
    if (element_COUNT < 0) return (기계낱말)bo_sh_VALUE;
    기계낱말 *o_lchov_ma_lumotlar = 전달인수[LOOKUP_INDEX]; unsigned kiritish_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < element_COUNT;) {
        unsigned belgi_kodi = 입력결과[순번++], 더있음 = belgi_kodi < 128 ? 0 : belgi_kodi >= 0xc2 && belgi_kodi < 0xe0 ? 1 : belgi_kodi < 0xf0 && belgi_kodi >= 0xe0 ? 2 : belgi_kodi >= 0xf0 && belgi_kodi <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > element_COUNT) { o_lchov_ma_lumotlar[++kiritish_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) belgi_kodi &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { belgi_kodi = (belgi_kodi << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || belgi_kodi < 최소값 || belgi_kodi > 0x10ffff || (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdfff)) belgi_kodi = 0xfffd;
        if (belgi_kodi >= 65536) { belgi_kodi -= 65536; o_lchov_ma_lumotlar[++kiritish_COUNT] = 0xd800 | (belgi_kodi >> 10); o_lchov_ma_lumotlar[++kiritish_COUNT] = 0xdc00 | (belgi_kodi & 1023); }
        else o_lchov_ma_lumotlar[++kiritish_COUNT] = belgi_kodi;
    }
    o_lchov_ma_lumotlar[0] = kiritish_COUNT; return (기계낱말)o_lchov_ma_lumotlar;
}
기계낱말 도구분류(void) { return toifa_VALUE; }
void 커널중단(const char *알림문) {
    const char *ma_lumotlar_holat = 알림문; while (*ma_lumotlar_holat) ma_lumotlar_holat++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, ma_lumotlar_holat - 알림문); belgi(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_foydalanuvchi_ilova(int uslub_MODE) {
    toifa_VALUE = uslub_MODE;
    unsigned char 첫항목[256]; intptr_t element_COUNT = 호출(15, 0, (기계낱말)첫항목, sizeof(첫항목));
    if (uslub_MODE == 2 || (uslub_MODE == 1 && element_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = uslub_MODE == 2 ? 0 : 1;
        char fayl_kiritish_nom[256]; intptr_t uzunlik_ma_lumotlar = 호출(15, 꾸러미인수이동, (기계낱말)fayl_kiritish_nom, sizeof(fayl_kiritish_nom));
        if (uzunlik_ma_lumotlar <= 0 || 꾸러미열기(fayl_kiritish_nom) < 0) {
            static const char Xato[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Xato, sizeof(Xato) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int o_lchov = 자바진입();
    if (대기중짝글자) belgi(0xfffd);
    return o_lchov;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Oila, 접속번호; uint32_t manzil; unsigned char 영값[8]; };
static struct 자바주소 UDP_manzil(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
기계낱말 vosita_UDP_ochmoq(기계낱말 접속번호) {
    intptr_t fayl_deskriptor = 호출(32, 2, 2, 17); if (fayl_deskriptor < 0) return (uint32_t)fayl_deskriptor;
    struct 자바주소 첫째값 = UDP_manzil(접속번호);
    첫째값.manzil = 0;
    intptr_t holat_VALUE_e10195a1 = 호출(33, fayl_deskriptor, (기계낱말)&첫째값, sizeof(첫째값));
    if (holat_VALUE_e10195a1 < 0) { vosita_yopmoq(fayl_deskriptor); return (uint32_t)holat_VALUE_e10195a1; }
    return fayl_deskriptor;
}
기계낱말 vosita_UDP_yuborish(기계낱말 fayl_deskriptor, 기계낱말 접속번호, 기계낱말 ARRAY_VALUE, 기계낱말 uzunlik_VALUE) {
    const 기계낱말 *원본주소 = (const 기계낱말 *)ARRAY_VALUE; unsigned char ma_lumotlar[512];
    if (uzunlik_VALUE > 512 || uzunlik_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (기계낱말 순번 = 0; 순번 < uzunlik_VALUE; 순번++) ma_lumotlar[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_manzil(접속번호);
    return (uint32_t)사용자호출(34, fayl_deskriptor, (기계낱말)ma_lumotlar, uzunlik_VALUE, 0, (기계낱말)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t element_COUNT) { return (element_COUNT>>24)|((element_COUNT>>8)&0xff00)|((element_COUNT<<8)&0xff0000)|(element_COUNT<<24); }
기계낱말 vosita_UDP_yuborish_manzil(기계낱말 fayl_deskriptor, 기계낱말 manzil, 기계낱말 접속번호, 기계낱말 ARRAY_VALUE, 기계낱말 uzunlik_VALUE) {
    const 기계낱말 *원본주소 = (const 기계낱말 *)ARRAY_VALUE; unsigned char ma_lumotlar[512];
    if (uzunlik_VALUE > 512 || uzunlik_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (기계낱말 순번 = 0; 순번 < uzunlik_VALUE; 순번++) ma_lumotlar[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_manzil(접속번호); 첫째값.manzil = 바이트순서뒤집기(manzil);
    return (uint32_t)사용자호출(34, fayl_deskriptor, (기계낱말)ma_lumotlar, uzunlik_VALUE, 0, (기계낱말)&첫째값, sizeof(첫째값));
}
기계낱말 vosita_ulash(기계낱말 fayl_deskriptor, 기계낱말 manzil, 기계낱말 접속번호) {
    struct 자바주소 첫째값 = UDP_manzil(접속번호); 첫째값.manzil = 바이트순서뒤집기(manzil);
    uint32_t Bajarish = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t o_lchov = 호출(37, fayl_deskriptor, (기계낱말)&첫째값, sizeof(첫째값));
        if (o_lchov != -115) return (uint32_t)o_lchov;
        if ((uint32_t)(호출(7, 0, 0, 0) - Bajarish) >= 1000) return (uint32_t)-110;
    }
}
기계낱말 도구전문받기(기계낱말 fayl_deskriptor, 기계낱말 ARRAY_VALUE, 기계낱말 수용량) {
    기계낱말 *ko_chirish_joyi_manzil = (기계낱말 *)ARRAY_VALUE; unsigned char ma_lumotlar[512];
    if (수용량 > 512 || ko_chirish_joyi_manzil[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned uzunlik_ma_lumotlar = sizeof(첫째값);
    intptr_t element_COUNT = 사용자호출(35, fayl_deskriptor, (기계낱말)ma_lumotlar, 수용량, 0, (기계낱말)&첫째값, (기계낱말)&uzunlik_ma_lumotlar);
    if (element_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) ko_chirish_joyi_manzil[순번 + 1] = ma_lumotlar[순번]; ko_chirish_joyi_manzil[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; ko_chirish_joyi_manzil[514] = 바이트순서뒤집기(첫째값.manzil); }
    return (uint32_t)element_COUNT;
}
기계낱말 vosita_UDP_port(기계낱말 fayl_deskriptor) {
    struct 자바주소 첫째값; unsigned uzunlik_ma_lumotlar = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fayl_deskriptor, (기계낱말)&첫째값, (기계낱말)&uzunlik_ma_lumotlar);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
기계낱말 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
기계낱말 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
기계낱말 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
기계낱말 vosita_grafika_bir_daqiqa(void) { return (uint32_t)화면키기다리기(); }
기계낱말 도구사각형(기계낱말 x_koordinata, 기계낱말 Y_tugmasi_koordinat, 기계낱말 너비값, 기계낱말 높이값, 기계낱말 색상) {
    return (uint32_t)사용자호출(13, x_koordinata, Y_tugmasi_koordinat, 색상, 너비값, 높이값, 0);
}

기계낱말 vosita_oqim(기계낱말 Amal,기계낱말 fayl_deskriptor,기계낱말 VALUE){
    if(Amal==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_manzil(VALUE);
    if(Amal==1){첫째값.manzil=0;intptr_t 반환값=호출(33,fayl_deskriptor,(기계낱말)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fayl_deskriptor,4,0));}
    if(Amal==2)return (uint32_t)호출(37,fayl_deskriptor,(기계낱말)&첫째값,sizeof(첫째값));
    if(Amal==3)return (uint32_t)호출(39,fayl_deskriptor,0,0);
    if(Amal==4)return vosita_UDP_port(fayl_deskriptor);
    if(Amal==5)return (uint32_t)호출(40,fayl_deskriptor,0,0);
    return (uint32_t)-22;
}
기계낱말 vosita_GUI(기계낱말 Amal,기계낱말 identifikator_VALUE,기계낱말 첫째값,기계낱말 SECOND_VALUE,기계낱말 belgi_kodi,기계낱말 ko_chirish_joyi_ma_lumotlar){return (uint32_t)사용자호출(20,Amal,identifikator_VALUE,첫째값,SECOND_VALUE,belgi_kodi,ko_chirish_joyi_ma_lumotlar);}
기계낱말 vosita_GUI_SMS(기계낱말 identifikator_VALUE,기계낱말 ARRAY_VALUE,기계낱말 element_COUNT){
    const 기계낱말 *원본주소=(const 기계낱말 *)ARRAY_VALUE;uint32_t ma_lumotlar[127];unsigned kiritish_COUNT=0;
    if(element_COUNT>원본주소[0])return (uint32_t)-22;
    for(기계낱말 순번=0;순번<element_COUNT;순번++){unsigned belgi_kodlash=원본주소[순번+1];if(belgi_kodlash>=0xd800&&belgi_kodlash<=0xdbff&&순번+1<element_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;belgi_kodlash=0x10000+((belgi_kodlash-0xd800)<<10)+낮은값-0xdc00;}if(kiritish_COUNT==127)return (uint32_t)-22;ma_lumotlar[kiritish_COUNT++]=belgi_kodlash;}
    return (uint32_t)사용자호출(21,identifikator_VALUE,(기계낱말)ma_lumotlar,kiritish_COUNT,0,0,0);
}
