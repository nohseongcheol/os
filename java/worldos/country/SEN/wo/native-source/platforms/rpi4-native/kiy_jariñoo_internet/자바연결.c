#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 bara_denc/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "takku_xéewël.h"
typedef uintptr_t masin_Word;
static int ngiir_xëyma;
static int 꾸러미사용중, 꾸러미인수이동;
static masin_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, masin_Word 첫째값, masin_Word 둘째값, masin_Word kotu_araf) {
    return 사용자호출(개수, 첫째값, 둘째값, kotu_araf, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (masin_Word)자료위치, 개수); }
static void Araf(unsigned kotu_araf) {
    unsigned char mbir[4]; unsigned 개수 = 0;
    if (kotu_araf < 128) mbir[개수++] = kotu_araf;
    else if (kotu_araf < 2048) { mbir[개수++] = 0xc0 | (kotu_araf >> 6); mbir[개수++] = 0x80 | (kotu_araf & 63); }
    else if (kotu_araf < 65536) { mbir[개수++] = 0xe0 | (kotu_araf >> 12); mbir[개수++] = 0x80 | ((kotu_araf >> 6) & 63); mbir[개수++] = 0x80 | (kotu_araf & 63); }
    else { mbir[개수++] = 0xf0 | (kotu_araf >> 18); mbir[개수++] = 0x80 | ((kotu_araf >> 12) & 63); mbir[개수++] = 0x80 | ((kotu_araf >> 6) & 63); mbir[개수++] = 0x80 | (kotu_araf & 63); }
    바이트들((const char *)mbir, 개수);
}
masin_Word jumtukaay_Araf(masin_Word xëyma) {
    unsigned kotu_araf = xëyma;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kotu_araf >= 0xdc00 && kotu_araf <= 0xdfff) { Araf(0x10000 + ((높은부분 - 0xd800) << 10) + kotu_araf - 0xdc00); return 1; }
        Araf(0xfffd);
    }
    if (kotu_araf >= 0xd800 && kotu_araf <= 0xdbff) 대기중짝글자 = kotu_araf;
    else Araf(kotu_araf > 0x10ffff || (kotu_araf >= 0xdc00 && kotu_araf <= 0xdfff) ? 0xfffd : kotu_araf);
    return 1;
}
masin_Word 도구출력(masin_Word xëyma) {
    const masin_Word *araf_yu_bennoo_mbir = (const masin_Word *)xëyma;
    for (masin_Word 순번 = 0; 순번 < araf_yu_bennoo_mbir[0]; 순번++) jumtukaay_Araf(araf_yu_bennoo_mbir[순번 + 1]);
    return araf_yu_bennoo_mbir[0];
}
static int Yoonu_jëmale(masin_Word yëf_Royukaay, char 결과자료[512]) {
    const masin_Word *첫째값 = (const masin_Word *)yëf_Royukaay;
    unsigned 사용량 = 0;
    for (masin_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kotu_araf = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] doxalin_anam 경로와 호환한다.
        if (kotu_araf >= 0xd800 && kotu_araf <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kotu_araf = 0x10000 + ((kotu_araf - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kotu_araf >= 0xd800 && kotu_araf <= 0xdfff) return -22;
        unsigned 개수 = kotu_araf < 128 ? 1 : kotu_araf < 2048 ? 2 : kotu_araf < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = kotu_araf;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (kotu_araf >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((kotu_araf >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
masin_Word jumtukaay_sos(masin_Word tur_253d1510, masin_Word 설정비트) {
    char 자료위치[512]; int njumte = Yoonu_jëmale(tur_253d1510, 자료위치);
    return (uint32_t)(njumte ? njumte : 호출(3, (masin_Word)자료위치, 설정비트, 0));
}
masin_Word jumtukaay_Tej(masin_Word bara_denc_yombal) { return (uint32_t)호출(4, bara_denc_yombal, 0, 0); }
masin_Word 도구바이트읽기(masin_Word bara_denc_yombal) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, bara_denc_yombal, (masin_Word)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
masin_Word jumtukaay_biir_okte(masin_Word bara_denc_yombal, masin_Word xëyma) {
    unsigned char 둘째값 = xëyma; return (uint32_t)호출(1, bara_denc_yombal, (masin_Word)&둘째값, 1);
}
masin_Word 도구읽기(masin_Word tur_253d1510, masin_Word jëmmukaay_mbir_dëkkuwaay) {
    if (꾸러미사용중) {
        char 자료위치[512]; int njumte = Yoonu_jëmale(tur_253d1510, 자료위치); if (njumte) return (uint32_t)njumte;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; masin_Word *목적위치 = (masin_Word *)jëmmukaay_mbir_dëkkuwaay;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int bara_denc_yombal = 꾸러미사용중 ? -2 : (int32_t)jumtukaay_sos(tur_253d1510, 0);
    if (bara_denc_yombal < 0) {
        char 자료위치[512]; int njumte = Yoonu_jëmale(tur_253d1510, 자료위치); if (njumte) return (uint32_t)njumte;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].tur_253d1510; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            masin_Word *목적위치 = (masin_Word *)jëmmukaay_mbir_dëkkuwaay;
            if (목적위치[0] < 자바클래스들[순번].tolluwaay) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].tolluwaay; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].mbir[안쪽순번];
            return 자바클래스들[순번].tolluwaay;
        }
        return (uint32_t)bara_denc_yombal;
    }
    masin_Word *첫째값 = (masin_Word *)jëmmukaay_mbir_dëkkuwaay;
    intptr_t tolluwaay = 호출(9, bara_denc_yombal, 0, 0), 완료량 = 0;
    if (tolluwaay < 0 || (masin_Word)tolluwaay > 첫째값[0]) { jumtukaay_Tej(bara_denc_yombal); return (uint32_t)(tolluwaay < 0 ? tolluwaay : -27); }
    unsigned char mbir_gatandu[256];
    while (완료량 < tolluwaay) {
        intptr_t 개수 = 호출(2, bara_denc_yombal, (masin_Word)mbir_gatandu, tolluwaay - 완료량 < 256 ? tolluwaay - 완료량 : 256);
        if (개수 <= 0) { jumtukaay_Tej(bara_denc_yombal); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = mbir_gatandu[순번];
        완료량 += 개수;
    }
    jumtukaay_Tej(bara_denc_yombal); return 완료량;
}
masin_Word jumtukaay_biir(masin_Word tur_253d1510, masin_Word 원본자료, masin_Word 항목수) {
    const masin_Word *첫째값 = (const masin_Word *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int bara_denc_yombal = (int32_t)jumtukaay_sos(tur_253d1510, 577); if (bara_denc_yombal < 0) return (uint32_t)bara_denc_yombal;
    unsigned char mbir_gatandu[256]; masin_Word 완료량 = 0;
    while (완료량 < 항목수) {
        masin_Word 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (masin_Word 순번 = 0; 순번 < 개수; 순번++) mbir_gatandu[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, bara_denc_yombal, (masin_Word)mbir_gatandu, 개수);
        if (결과 <= 0) { jumtukaay_Tej(bara_denc_yombal); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    jumtukaay_Tej(bara_denc_yombal); return 항목수;
}
masin_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
masin_Word jumtukaay_Tegtal(masin_Word 색인) {
    static const masin_Word neen_xëyma[1] = {0};
    if (색인 >= 8) return (masin_Word)neen_xëyma;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (masin_Word)입력결과, sizeof(입력결과));
    if (개수 < 0) return (masin_Word)neen_xëyma;
    masin_Word *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned kotu_araf = 입력결과[순번++], 더있음 = kotu_araf < 128 ? 0 : kotu_araf >= 0xc2 && kotu_araf < 0xe0 ? 1 : kotu_araf < 0xf0 && kotu_araf >= 0xe0 ? 2 : kotu_araf >= 0xf0 && kotu_araf <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kotu_araf &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kotu_araf = (kotu_araf << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kotu_araf < 최소값 || kotu_araf > 0x10ffff || (kotu_araf >= 0xd800 && kotu_araf <= 0xdfff)) kotu_araf = 0xfffd;
        if (kotu_araf >= 65536) { kotu_araf -= 65536; 결과자료[++항목수] = 0xd800 | (kotu_araf >> 10); 결과자료[++항목수] = 0xdc00 | (kotu_araf & 1023); }
        else 결과자료[++항목수] = kotu_araf;
    }
    결과자료[0] = 항목수; return (masin_Word)결과자료;
}
masin_Word 도구분류(void) { return ngiir_xëyma; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); Araf(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Door_kiy_jariñoo_internet_jëfekaay(int doxalin_anam) {
    ngiir_xëyma = doxalin_anam;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (masin_Word)첫항목, sizeof(첫항목));
    if (doxalin_anam == 2 || (doxalin_anam == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = doxalin_anam == 2 ? 0 : 1;
        char bara_denc_dugal_xabaar_tur[256]; intptr_t diir_mbir = 호출(15, 꾸러미인수이동, (masin_Word)bara_denc_dugal_xabaar_tur, sizeof(bara_denc_dugal_xabaar_tur));
        if (diir_mbir <= 0 || 꾸러미열기(bara_denc_dugal_xabaar_tur) < 0) {
            static const char njumte[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(njumte, sizeof(njumte) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) Araf(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Njaboot, 접속번호; uint32_t dëkkuwaay; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
masin_Word 도구전문열기(masin_Word 접속번호) {
    intptr_t bara_denc_yombal = 호출(32, 2, 2, 17); if (bara_denc_yombal < 0) return (uint32_t)bara_denc_yombal;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.dëkkuwaay = 0;
    intptr_t nekkin_xëyma = 호출(33, bara_denc_yombal, (masin_Word)&첫째값, sizeof(첫째값));
    if (nekkin_xëyma < 0) { jumtukaay_Tej(bara_denc_yombal); return (uint32_t)nekkin_xëyma; }
    return bara_denc_yombal;
}
masin_Word 도구전문보내기(masin_Word bara_denc_yombal, masin_Word 접속번호, masin_Word TABLO_xëyma, masin_Word diir_xëyma) {
    const masin_Word *원본주소 = (const masin_Word *)TABLO_xëyma; unsigned char mbir[512];
    if (diir_xëyma > 512 || diir_xëyma > 원본주소[0]) return (uint32_t)-90;
    for (masin_Word 순번 = 0; 순번 < diir_xëyma; 순번++) mbir[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, bara_denc_yombal, (masin_Word)mbir, diir_xëyma, 0, (masin_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
masin_Word 도구전문주소보내기(masin_Word bara_denc_yombal, masin_Word dëkkuwaay, masin_Word 접속번호, masin_Word TABLO_xëyma, masin_Word diir_xëyma) {
    const masin_Word *원본주소 = (const masin_Word *)TABLO_xëyma; unsigned char mbir[512];
    if (diir_xëyma > 512 || diir_xëyma > 원본주소[0]) return (uint32_t)-90;
    for (masin_Word 순번 = 0; 순번 < diir_xëyma; 순번++) mbir[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.dëkkuwaay = 바이트순서뒤집기(dëkkuwaay);
    return (uint32_t)사용자호출(34, bara_denc_yombal, (masin_Word)mbir, diir_xëyma, 0, (masin_Word)&첫째값, sizeof(첫째값));
}
masin_Word jumtukaay_JOKKOO(masin_Word bara_denc_yombal, masin_Word dëkkuwaay, masin_Word 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.dëkkuwaay = 바이트순서뒤집기(dëkkuwaay);
    uint32_t daw = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, bara_denc_yombal, (masin_Word)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - daw) >= 1000) return (uint32_t)-110;
    }
}
masin_Word 도구전문받기(masin_Word bara_denc_yombal, masin_Word TABLO_xëyma, masin_Word 수용량) {
    masin_Word *jëmmukaay_dëkkuwaay = (masin_Word *)TABLO_xëyma; unsigned char mbir[512];
    if (수용량 > 512 || jëmmukaay_dëkkuwaay[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned diir_mbir = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, bara_denc_yombal, (masin_Word)mbir, 수용량, 0, (masin_Word)&첫째값, (masin_Word)&diir_mbir);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) jëmmukaay_dëkkuwaay[순번 + 1] = mbir[순번]; jëmmukaay_dëkkuwaay[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; jëmmukaay_dëkkuwaay[514] = 바이트순서뒤집기(첫째값.dëkkuwaay); }
    return (uint32_t)개수;
}
masin_Word 도구전문접속번호(masin_Word bara_denc_yombal) {
    struct 자바주소 첫째값; unsigned diir_mbir = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, bara_denc_yombal, (masin_Word)&첫째값, (masin_Word)&diir_mbir);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
masin_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
masin_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
masin_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
masin_Word 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
masin_Word 도구사각형(masin_Word rëddu_iks_yi, masin_Word 세로좌표, masin_Word 너비값, masin_Word 높이값, masin_Word 색상) {
    return (uint32_t)사용자호출(13, rëddu_iks_yi, 세로좌표, 색상, 너비값, 높이값, 0);
}

masin_Word jumtukaay_dawal(masin_Word jëf,masin_Word bara_denc_yombal,masin_Word xëyma){
    if(jëf==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(xëyma);
    if(jëf==1){첫째값.dëkkuwaay=0;intptr_t 반환값=호출(33,bara_denc_yombal,(masin_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,bara_denc_yombal,4,0));}
    if(jëf==2)return (uint32_t)호출(37,bara_denc_yombal,(masin_Word)&첫째값,sizeof(첫째값));
    if(jëf==3)return (uint32_t)호출(39,bara_denc_yombal,0,0);
    if(jëf==4)return 도구전문접속번호(bara_denc_yombal);
    if(jëf==5)return (uint32_t)호출(40,bara_denc_yombal,0,0);
    return (uint32_t)-22;
}
masin_Word jumtukaay_GUI(masin_Word jëf,masin_Word raññeekaay_xëyma,masin_Word 첫째값,masin_Word 둘째값,masin_Word kotu_araf,masin_Word jëmmukaay_mbir){return (uint32_t)사용자호출(20,jëf,raññeekaay_xëyma,첫째값,둘째값,kotu_araf,jëmmukaay_mbir);}
masin_Word jumtukaay_GUI_SMS(masin_Word raññeekaay_xëyma,masin_Word TABLO_xëyma,masin_Word 개수){
    const masin_Word *원본주소=(const masin_Word *)TABLO_xëyma;uint32_t mbir[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(masin_Word 순번=0;순번<개수;순번++){unsigned Araf_nëbbin_ci_lim=원본주소[순번+1];if(Araf_nëbbin_ci_lim>=0xd800&&Araf_nëbbin_ci_lim<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;Araf_nëbbin_ci_lim=0x10000+((Araf_nëbbin_ci_lim-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;mbir[항목수++]=Araf_nëbbin_ci_lim;}
    return (uint32_t)사용자호출(21,raññeekaay_xëyma,(masin_Word)mbir,항목수,0,0,0);
}
