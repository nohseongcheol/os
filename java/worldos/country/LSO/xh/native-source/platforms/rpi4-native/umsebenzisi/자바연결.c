#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 iFayili/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "umqulu.h"
typedef uintptr_t umatshini_Igama;
static int udidi_ixabiso;
static int 꾸러미사용중, 꾸러미인수이동;
static umatshini_Igama 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned 개수, umatshini_Igama 첫째값, umatshini_Igama 둘째값, umatshini_Igama ikhowudi_yekharakhtha) {
    return 사용자호출(개수, 첫째값, 둘째값, ikhowudi_yekharakhtha, 0, 0, 0);
}
static void 바이트들(const char *자료위치, size_t 개수) { 호출(1, 1, (umatshini_Igama)자료위치, 개수); }
static void ikharakhtha(unsigned ikhowudi_yekharakhtha) {
    unsigned char iingcombolo[4]; unsigned 개수 = 0;
    if (ikhowudi_yekharakhtha < 128) iingcombolo[개수++] = ikhowudi_yekharakhtha;
    else if (ikhowudi_yekharakhtha < 2048) { iingcombolo[개수++] = 0xc0 | (ikhowudi_yekharakhtha >> 6); iingcombolo[개수++] = 0x80 | (ikhowudi_yekharakhtha & 63); }
    else if (ikhowudi_yekharakhtha < 65536) { iingcombolo[개수++] = 0xe0 | (ikhowudi_yekharakhtha >> 12); iingcombolo[개수++] = 0x80 | ((ikhowudi_yekharakhtha >> 6) & 63); iingcombolo[개수++] = 0x80 | (ikhowudi_yekharakhtha & 63); }
    else { iingcombolo[개수++] = 0xf0 | (ikhowudi_yekharakhtha >> 18); iingcombolo[개수++] = 0x80 | ((ikhowudi_yekharakhtha >> 12) & 63); iingcombolo[개수++] = 0x80 | ((ikhowudi_yekharakhtha >> 6) & 63); iingcombolo[개수++] = 0x80 | (ikhowudi_yekharakhtha & 63); }
    바이트들((const char *)iingcombolo, 개수);
}
umatshini_Igama isixhobo_sokutayipha_ikharakhtha(umatshini_Igama ixabiso) {
    unsigned ikhowudi_yekharakhtha = ixabiso;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (ikhowudi_yekharakhtha >= 0xdc00 && ikhowudi_yekharakhtha <= 0xdfff) { ikharakhtha(0x10000 + ((높은부분 - 0xd800) << 10) + ikhowudi_yekharakhtha - 0xdc00); return 1; }
        ikharakhtha(0xfffd);
    }
    if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdbff) 대기중짝글자 = ikhowudi_yekharakhtha;
    else ikharakhtha(ikhowudi_yekharakhtha > 0x10ffff || (ikhowudi_yekharakhtha >= 0xdc00 && ikhowudi_yekharakhtha <= 0xdfff) ? 0xfffd : ikhowudi_yekharakhtha);
    return 1;
}
umatshini_Igama 도구출력(umatshini_Igama ixabiso) {
    const umatshini_Igama *uluhlu_lweekharektha_iingcombolo = (const umatshini_Igama *)ixabiso;
    for (umatshini_Igama 순번 = 0; 순번 < uluhlu_lweekharektha_iingcombolo[0]; 순번++) isixhobo_sokutayipha_ikharakhtha(uluhlu_lweekharektha_iingcombolo[순번 + 1]);
    return uluhlu_lweekharektha_iingcombolo[0];
}
static int INDLELA(umatshini_Igama into_Isalathiso, char 결과자료[512]) {
    const umatshini_Igama *첫째값 = (const umatshini_Igama *)into_Isalathiso;
    unsigned 사용량 = 0;
    for (umatshini_Igama 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned ikhowudi_yekharakhtha = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] imethodi_imo 경로와 호환한다.
        if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; ikhowudi_yekharakhtha = 0x10000 + ((ikhowudi_yekharakhtha - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdfff) return -22;
        unsigned 개수 = ikhowudi_yekharakhtha < 128 ? 1 : ikhowudi_yekharakhtha < 2048 ? 2 : ikhowudi_yekharakhtha < 65536 ? 3 : 4;
        if (사용량 + 개수 > 511) return -36;
        if (개수 == 1) 결과자료[사용량++] = ikhowudi_yekharakhtha;
        else {
            결과자료[사용량++] = (개수 == 2 ? 0xc0 : 개수 == 3 ? 0xe0 : 0xf0) | (ikhowudi_yekharakhtha >> (6 * (개수 - 1)));
            for (unsigned 안쪽순번 = 개수 - 1; 안쪽순번; 안쪽순번--) 결과자료[사용량++] = 0x80 | ((ikhowudi_yekharakhtha >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    결과자료[사용량] = 0; return 사용량 ? 0 : -22;
}
umatshini_Igama isixhobo_sokutayipha_vula(umatshini_Igama Igama, umatshini_Igama 설정비트) {
    char 자료위치[512]; int Impazamo = INDLELA(Igama, 자료위치);
    return (uint32_t)(Impazamo ? Impazamo : 호출(3, (umatshini_Igama)자료위치, 설정비트, 0));
}
umatshini_Igama isixhobo_sokutayipha_vala(umatshini_Igama ifayile_isibambi) { return (uint32_t)호출(4, ifayile_isibambi, 0, 0); }
umatshini_Igama 도구바이트읽기(umatshini_Igama ifayile_isibambi) {
    unsigned char 둘째값; intptr_t 개수 = 호출(2, ifayile_isibambi, (umatshini_Igama)&둘째값, 1);
    return (uint32_t)(개수 == 1 ? 둘째값 : 개수 == 0 ? 256 : 개수);
}
umatshini_Igama isixhobo_sokutayipha_bhala_ibhayithi(umatshini_Igama ifayile_isibambi, umatshini_Igama ixabiso) {
    unsigned char 둘째값 = ixabiso; return (uint32_t)호출(1, ifayile_isibambi, (umatshini_Igama)&둘째값, 1);
}
umatshini_Igama 도구읽기(umatshini_Igama Igama, umatshini_Igama indawo_ekuyiwa_kuyo_iingcombolo_idilesi) {
    if (꾸러미사용중) {
        char 자료위치[512]; int Impazamo = INDLELA(Igama, 자료위치); if (Impazamo) return (uint32_t)Impazamo;
        unsigned 개수 = 0; while (자료위치[개수]) 개수++;
        if (개수 >= 6) for (unsigned 순번 = 0; 순번 < 개수 - 6; 순번++) if (자료위치[순번] == '.') 자료위치[순번] = '/';
        unsigned char 바이트들[16384]; umatshini_Igama *목적위치 = (umatshini_Igama *)indawo_ekuyiwa_kuyo_iingcombolo_idilesi;
        int 받은수 = 꾸러미읽기(자료위치, 바이트들, 목적위치[0] < sizeof(바이트들) ? 목적위치[0] : sizeof(바이트들));
        if (받은수 >= 0) { for (int 순번 = 0; 순번 < 받은수; 순번++) 목적위치[순번 + 1] = 바이트들[순번]; return 받은수; }
        if (받은수 != -2) return (uint32_t)받은수;
    }
    int ifayile_isibambi = 꾸러미사용중 ? -2 : (int32_t)isixhobo_sokutayipha_vula(Igama, 0);
    if (ifayile_isibambi < 0) {
        char 자료위치[512]; int Impazamo = INDLELA(Igama, 자료위치); if (Impazamo) return (uint32_t)Impazamo;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *다음위치 = 자바클래스들[순번].Igama; unsigned 안쪽순번 = 0;
            while (자료위치[안쪽순번] && 자료위치[안쪽순번] == 다음위치[안쪽순번]) 안쪽순번++;
            if (자료위치[안쪽순번] || 다음위치[안쪽순번]) continue;
            umatshini_Igama *목적위치 = (umatshini_Igama *)indawo_ekuyiwa_kuyo_iingcombolo_idilesi;
            if (목적위치[0] < 자바클래스들[순번].Ubukhulu) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Ubukhulu; 안쪽순번++) 목적위치[안쪽순번 + 1] = 자바클래스들[순번].iingcombolo[안쪽순번];
            return 자바클래스들[순번].Ubukhulu;
        }
        return (uint32_t)ifayile_isibambi;
    }
    umatshini_Igama *첫째값 = (umatshini_Igama *)indawo_ekuyiwa_kuyo_iingcombolo_idilesi;
    intptr_t Ubukhulu = 호출(9, ifayile_isibambi, 0, 0), 완료량 = 0;
    if (Ubukhulu < 0 || (umatshini_Igama)Ubukhulu > 첫째값[0]) { isixhobo_sokutayipha_vala(ifayile_isibambi); return (uint32_t)(Ubukhulu < 0 ? Ubukhulu : -27); }
    unsigned char iingcombolo_thintela[256];
    while (완료량 < Ubukhulu) {
        intptr_t 개수 = 호출(2, ifayile_isibambi, (umatshini_Igama)iingcombolo_thintela, Ubukhulu - 완료량 < 256 ? Ubukhulu - 완료량 : 256);
        if (개수 <= 0) { isixhobo_sokutayipha_vala(ifayile_isibambi); return (uint32_t)(개수 ? 개수 : -5); }
        for (intptr_t 순번 = 0; 순번 < 개수; 순번++) 첫째값[1 + 완료량 + 순번] = iingcombolo_thintela[순번];
        완료량 += 개수;
    }
    isixhobo_sokutayipha_vala(ifayile_isibambi); return 완료량;
}
umatshini_Igama isixhobo_sokutayipha_bhala(umatshini_Igama Igama, umatshini_Igama 원본자료, umatshini_Igama 항목수) {
    const umatshini_Igama *첫째값 = (const umatshini_Igama *)원본자료;
    if (항목수 > 첫째값[0] || 항목수 > 16384) return (uint32_t)-27;
    int ifayile_isibambi = (int32_t)isixhobo_sokutayipha_vula(Igama, 577); if (ifayile_isibambi < 0) return (uint32_t)ifayile_isibambi;
    unsigned char iingcombolo_thintela[256]; umatshini_Igama 완료량 = 0;
    while (완료량 < 항목수) {
        umatshini_Igama 개수 = 항목수 - 완료량 < 256 ? 항목수 - 완료량 : 256;
        for (umatshini_Igama 순번 = 0; 순번 < 개수; 순번++) iingcombolo_thintela[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t 결과 = 호출(1, ifayile_isibambi, (umatshini_Igama)iingcombolo_thintela, 개수);
        if (결과 <= 0) { isixhobo_sokutayipha_vala(ifayile_isibambi); return (uint32_t)(결과 ? 결과 : -5); }
        완료량 += 결과;
    }
    isixhobo_sokutayipha_vala(ifayile_isibambi); return 항목수;
}
umatshini_Igama 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
umatshini_Igama isixhobo_sokutayipha_isiniki_myalelo(umatshini_Igama 색인) {
    static const umatshini_Igama engenanto_ixabiso[1] = {0};
    if (색인 >= 8) return (umatshini_Igama)engenanto_ixabiso;
    unsigned char 입력결과[256]; intptr_t 개수;
    if (꾸러미사용중 && 색인 == 0) { const char *자료위치 = 꾸러미진입클래스(); 개수 = 0; while (자료위치[개수] && 개수 < 255) { 입력결과[개수] = 자료위치[개수]; 개수++; } }
    else 개수 = 호출(15, 색인 + (꾸러미사용중 ? 꾸러미인수이동 : 0), (umatshini_Igama)입력결과, sizeof(입력결과));
    if (개수 < 0) return (umatshini_Igama)engenanto_ixabiso;
    umatshini_Igama *결과자료 = 전달인수[색인]; unsigned 항목수 = 0;
    for (intptr_t 순번 = 0; 순번 < 개수;) {
        unsigned ikhowudi_yekharakhtha = 입력결과[순번++], 더있음 = ikhowudi_yekharakhtha < 128 ? 0 : ikhowudi_yekharakhtha >= 0xc2 && ikhowudi_yekharakhtha < 0xe0 ? 1 : ikhowudi_yekharakhtha < 0xf0 && ikhowudi_yekharakhtha >= 0xe0 ? 2 : ikhowudi_yekharakhtha >= 0xf0 && ikhowudi_yekharakhtha <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > 개수) { 결과자료[++항목수] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) ikhowudi_yekharakhtha &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { ikhowudi_yekharakhtha = (ikhowudi_yekharakhtha << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || ikhowudi_yekharakhtha < 최소값 || ikhowudi_yekharakhtha > 0x10ffff || (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdfff)) ikhowudi_yekharakhtha = 0xfffd;
        if (ikhowudi_yekharakhtha >= 65536) { ikhowudi_yekharakhtha -= 65536; 결과자료[++항목수] = 0xd800 | (ikhowudi_yekharakhtha >> 10); 결과자료[++항목수] = 0xdc00 | (ikhowudi_yekharakhtha & 1023); }
        else 결과자료[++항목수] = ikhowudi_yekharakhtha;
    }
    결과자료[0] = 항목수; return (umatshini_Igama)결과자료;
}
umatshini_Igama 도구분류(void) { return udidi_ixabiso; }
void 커널중단(const char *알림문) {
    const char *자료위치 = 알림문; while (*자료위치) 자료위치++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, 자료위치 - 알림문); ikharakhtha(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int qala_umsebenzisi_inkqubo(int imethodi_imo) {
    udidi_ixabiso = imethodi_imo;
    unsigned char 첫항목[256]; intptr_t 개수 = 호출(15, 0, (umatshini_Igama)첫항목, sizeof(첫항목));
    if (imethodi_imo == 2 || (imethodi_imo == 1 && 개수 == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = imethodi_imo == 2 ? 0 : 1;
        char ifayile_ufako_nkcukacha_igama[256]; intptr_t ubude_iingcombolo = 호출(15, 꾸러미인수이동, (umatshini_Igama)ifayile_ufako_nkcukacha_igama, sizeof(ifayile_ufako_nkcukacha_igama));
        if (ubude_iingcombolo <= 0 || 꾸러미열기(ifayile_ufako_nkcukacha_igama) < 0) {
            static const char Impazamo[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(Impazamo, sizeof(Impazamo) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int 결과 = 자바진입();
    if (대기중짝글자) ikharakhtha(0xfffd);
    return 결과;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Usapho, 접속번호; uint32_t idilesi; unsigned char 영값[8]; };
static struct 자바주소 전문주소(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
umatshini_Igama 도구전문열기(umatshini_Igama 접속번호) {
    intptr_t ifayile_isibambi = 호출(32, 2, 2, 17); if (ifayile_isibambi < 0) return (uint32_t)ifayile_isibambi;
    struct 자바주소 첫째값 = 전문주소(접속번호);
    첫째값.idilesi = 0;
    intptr_t imo_ixabiso = 호출(33, ifayile_isibambi, (umatshini_Igama)&첫째값, sizeof(첫째값));
    if (imo_ixabiso < 0) { isixhobo_sokutayipha_vala(ifayile_isibambi); return (uint32_t)imo_ixabiso; }
    return ifayile_isibambi;
}
umatshini_Igama 도구전문보내기(umatshini_Igama ifayile_isibambi, umatshini_Igama 접속번호, umatshini_Igama ULUHLU_ixabiso, umatshini_Igama ubude_ixabiso) {
    const umatshini_Igama *원본주소 = (const umatshini_Igama *)ULUHLU_ixabiso; unsigned char iingcombolo[512];
    if (ubude_ixabiso > 512 || ubude_ixabiso > 원본주소[0]) return (uint32_t)-90;
    for (umatshini_Igama 순번 = 0; 순번 < ubude_ixabiso; 순번++) iingcombolo[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호);
    return (uint32_t)사용자호출(34, ifayile_isibambi, (umatshini_Igama)iingcombolo, ubude_ixabiso, 0, (umatshini_Igama)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t 개수) { return (개수>>24)|((개수>>8)&0xff00)|((개수<<8)&0xff0000)|(개수<<24); }
umatshini_Igama 도구전문주소보내기(umatshini_Igama ifayile_isibambi, umatshini_Igama idilesi, umatshini_Igama 접속번호, umatshini_Igama ULUHLU_ixabiso, umatshini_Igama ubude_ixabiso) {
    const umatshini_Igama *원본주소 = (const umatshini_Igama *)ULUHLU_ixabiso; unsigned char iingcombolo[512];
    if (ubude_ixabiso > 512 || ubude_ixabiso > 원본주소[0]) return (uint32_t)-90;
    for (umatshini_Igama 순번 = 0; 순번 < ubude_ixabiso; 순번++) iingcombolo[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.idilesi = 바이트순서뒤집기(idilesi);
    return (uint32_t)사용자호출(34, ifayile_isibambi, (umatshini_Igama)iingcombolo, ubude_ixabiso, 0, (umatshini_Igama)&첫째값, sizeof(첫째값));
}
umatshini_Igama isixhobo_sokutayipha_I_Connect(umatshini_Igama ifayile_isibambi, umatshini_Igama idilesi, umatshini_Igama 접속번호) {
    struct 자바주소 첫째값 = 전문주소(접속번호); 첫째값.idilesi = 바이트순서뒤집기(idilesi);
    uint32_t Phumeza = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t 결과 = 호출(37, ifayile_isibambi, (umatshini_Igama)&첫째값, sizeof(첫째값));
        if (결과 != -115) return (uint32_t)결과;
        if ((uint32_t)(호출(7, 0, 0, 0) - Phumeza) >= 1000) return (uint32_t)-110;
    }
}
umatshini_Igama 도구전문받기(umatshini_Igama ifayile_isibambi, umatshini_Igama ULUHLU_ixabiso, umatshini_Igama 수용량) {
    umatshini_Igama *indawo_ekuyiwa_kuyo_idilesi = (umatshini_Igama *)ULUHLU_ixabiso; unsigned char iingcombolo[512];
    if (수용량 > 512 || indawo_ekuyiwa_kuyo_idilesi[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned ubude_iingcombolo = sizeof(첫째값);
    intptr_t 개수 = 사용자호출(35, ifayile_isibambi, (umatshini_Igama)iingcombolo, 수용량, 0, (umatshini_Igama)&첫째값, (umatshini_Igama)&ubude_iingcombolo);
    if (개수 >= 0) { for (intptr_t 순번 = 0; 순번 < 개수; 순번++) indawo_ekuyiwa_kuyo_idilesi[순번 + 1] = iingcombolo[순번]; indawo_ekuyiwa_kuyo_idilesi[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; indawo_ekuyiwa_kuyo_idilesi[514] = 바이트순서뒤집기(첫째값.idilesi); }
    return (uint32_t)개수;
}
umatshini_Igama 도구전문접속번호(umatshini_Igama ifayile_isibambi) {
    struct 자바주소 첫째값; unsigned ubude_iingcombolo = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, ifayile_isibambi, (umatshini_Igama)&첫째값, (umatshini_Igama)&ubude_iingcombolo);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
umatshini_Igama 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
umatshini_Igama 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
umatshini_Igama 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
umatshini_Igama 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
umatshini_Igama 도구사각형(umatshini_Igama isilungelelanisi_x, umatshini_Igama 세로좌표, umatshini_Igama 너비값, umatshini_Igama 높이값, umatshini_Igama 색상) {
    return (uint32_t)사용자호출(13, isilungelelanisi_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

umatshini_Igama isixhobo_sokutayipha_Stream(umatshini_Igama Intshukumo,umatshini_Igama ifayile_isibambi,umatshini_Igama ixabiso){
    if(Intshukumo==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=전문주소(ixabiso);
    if(Intshukumo==1){첫째값.idilesi=0;intptr_t 반환값=호출(33,ifayile_isibambi,(umatshini_Igama)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,ifayile_isibambi,4,0));}
    if(Intshukumo==2)return (uint32_t)호출(37,ifayile_isibambi,(umatshini_Igama)&첫째값,sizeof(첫째값));
    if(Intshukumo==3)return (uint32_t)호출(39,ifayile_isibambi,0,0);
    if(Intshukumo==4)return 도구전문접속번호(ifayile_isibambi);
    if(Intshukumo==5)return (uint32_t)호출(40,ifayile_isibambi,0,0);
    return (uint32_t)-22;
}
umatshini_Igama isixhobo_sokutayipha_i_GUI(umatshini_Igama Intshukumo,umatshini_Igama isalathisi_ixabiso,umatshini_Igama 첫째값,umatshini_Igama 둘째값,umatshini_Igama ikhowudi_yekharakhtha,umatshini_Igama indawo_ekuyiwa_kuyo_iingcombolo){return (uint32_t)사용자호출(20,Intshukumo,isalathisi_ixabiso,첫째값,둘째값,ikhowudi_yekharakhtha,indawo_ekuyiwa_kuyo_iingcombolo);}
umatshini_Igama isixhobo_sokutayipha_i_GUI_I_SMS(umatshini_Igama isalathisi_ixabiso,umatshini_Igama ULUHLU_ixabiso,umatshini_Igama 개수){
    const umatshini_Igama *원본주소=(const umatshini_Igama *)ULUHLU_ixabiso;uint32_t iingcombolo[127];unsigned 항목수=0;
    if(개수>원본주소[0])return (uint32_t)-22;
    for(umatshini_Igama 순번=0;순번<개수;순번++){unsigned ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi=원본주소[순번+1];if(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi>=0xd800&&ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi<=0xdbff&&순번+1<개수){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi=0x10000+((ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi-0xd800)<<10)+낮은값-0xdc00;}if(항목수==127)return (uint32_t)-22;iingcombolo[항목수++]=ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi;}
    return (uint32_t)사용자호출(21,isalathisi_ixabiso,(umatshini_Igama)iingcombolo,항목수,0,0,0);
}
