#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 fajl/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "lott.h"
typedef uintptr_t kompjuter_Word;
static int kategorija_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static kompjuter_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned element_COUNT, kompjuter_Word 첫째값, kompjuter_Word SECOND_VALUE, kompjuter_Word kodiċi_tal_karattru) {
    return 사용자호출(element_COUNT, 첫째값, SECOND_VALUE, kodiċi_tal_karattru, 0, 0, 0);
}
static void 바이트들(const char *data_pożizzjoni, size_t element_COUNT) { 호출(1, 1, (kompjuter_Word)data_pożizzjoni, element_COUNT); }
static void karattru(unsigned kodiċi_tal_karattru) {
    unsigned char data[4]; unsigned element_COUNT = 0;
    if (kodiċi_tal_karattru < 128) data[element_COUNT++] = kodiċi_tal_karattru;
    else if (kodiċi_tal_karattru < 2048) { data[element_COUNT++] = 0xc0 | (kodiċi_tal_karattru >> 6); data[element_COUNT++] = 0x80 | (kodiċi_tal_karattru & 63); }
    else if (kodiċi_tal_karattru < 65536) { data[element_COUNT++] = 0xe0 | (kodiċi_tal_karattru >> 12); data[element_COUNT++] = 0x80 | ((kodiċi_tal_karattru >> 6) & 63); data[element_COUNT++] = 0x80 | (kodiċi_tal_karattru & 63); }
    else { data[element_COUNT++] = 0xf0 | (kodiċi_tal_karattru >> 18); data[element_COUNT++] = 0x80 | ((kodiċi_tal_karattru >> 12) & 63); data[element_COUNT++] = 0x80 | ((kodiċi_tal_karattru >> 6) & 63); data[element_COUNT++] = 0x80 | (kodiċi_tal_karattru & 63); }
    바이트들((const char *)data, element_COUNT);
}
kompjuter_Word għodda_karattru(kompjuter_Word VALUE) {
    unsigned kodiċi_tal_karattru = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kodiċi_tal_karattru >= 0xdc00 && kodiċi_tal_karattru <= 0xdfff) { karattru(0x10000 + ((높은부분 - 0xd800) << 10) + kodiċi_tal_karattru - 0xdc00); return 1; }
        karattru(0xfffd);
    }
    if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdbff) 대기중짝글자 = kodiċi_tal_karattru;
    else karattru(kodiċi_tal_karattru > 0x10ffff || (kodiċi_tal_karattru >= 0xdc00 && kodiċi_tal_karattru <= 0xdfff) ? 0xfffd : kodiċi_tal_karattru);
    return 1;
}
kompjuter_Word 도구출력(kompjuter_Word VALUE) {
    const kompjuter_Word *string_data = (const kompjuter_Word *)VALUE;
    for (kompjuter_Word 순번 = 0; 순번 < string_data[0]; 순번++) għodda_karattru(string_data[순번 + 1]);
    return string_data[0];
}
static int mogħdija(kompjuter_Word oġġett_Referenza, char miżura_data[512]) {
    const kompjuter_Word *첫째값 = (const kompjuter_Word *)oġġett_Referenza;
    unsigned 사용량 = 0;
    for (kompjuter_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kodiċi_tal_karattru = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metodu_MODE 경로와 호환한다.
        if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kodiċi_tal_karattru = 0x10000 + ((kodiċi_tal_karattru - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdfff) return -22;
        unsigned element_COUNT = kodiċi_tal_karattru < 128 ? 1 : kodiċi_tal_karattru < 2048 ? 2 : kodiċi_tal_karattru < 65536 ? 3 : 4;
        if (사용량 + element_COUNT > 511) return -36;
        if (element_COUNT == 1) miżura_data[사용량++] = kodiċi_tal_karattru;
        else {
            miżura_data[사용량++] = (element_COUNT == 2 ? 0xc0 : element_COUNT == 3 ? 0xe0 : 0xf0) | (kodiċi_tal_karattru >> (6 * (element_COUNT - 1)));
            for (unsigned 안쪽순번 = element_COUNT - 1; 안쪽순번; 안쪽순번--) miżura_data[사용량++] = 0x80 | ((kodiċi_tal_karattru >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    miżura_data[사용량] = 0; return 사용량 ? 0 : -22;
}
kompjuter_Word għodda_fetaħ(kompjuter_Word isem, kompjuter_Word 설정비트) {
    char data_pożizzjoni[512]; int żball = mogħdija(isem, data_pożizzjoni);
    return (uint32_t)(żball ? żball : 호출(3, (kompjuter_Word)data_pożizzjoni, 설정비트, 0));
}
kompjuter_Word għodda_agħlaq(kompjuter_Word fajl_handle) { return (uint32_t)호출(4, fajl_handle, 0, 0); }
kompjuter_Word 도구바이트읽기(kompjuter_Word fajl_handle) {
    unsigned char SECOND_VALUE; intptr_t element_COUNT = 호출(2, fajl_handle, (kompjuter_Word)&SECOND_VALUE, 1);
    return (uint32_t)(element_COUNT == 1 ? SECOND_VALUE : element_COUNT == 0 ? 256 : element_COUNT);
}
kompjuter_Word għodda_kiteb_byte(kompjuter_Word fajl_handle, kompjuter_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, fajl_handle, (kompjuter_Word)&SECOND_VALUE, 1);
}
kompjuter_Word 도구읽기(kompjuter_Word isem, kompjuter_Word destinazzjoni_data_ADDRESS) {
    if (꾸러미사용중) {
        char data_pożizzjoni[512]; int żball = mogħdija(isem, data_pożizzjoni); if (żball) return (uint32_t)żball;
        unsigned element_COUNT = 0; while (data_pożizzjoni[element_COUNT]) element_COUNT++;
        if (element_COUNT >= 6) for (unsigned 순번 = 0; 순번 < element_COUNT - 6; 순번++) if (data_pożizzjoni[순번] == '.') data_pożizzjoni[순번] = '/';
        unsigned char 바이트들[16384]; kompjuter_Word *destinazzjoni_VALUE_pożizzjoni = (kompjuter_Word *)destinazzjoni_data_ADDRESS;
        int RECEIVED_COUNT = 꾸러미읽기(data_pożizzjoni, 바이트들, destinazzjoni_VALUE_pożizzjoni[0] < sizeof(바이트들) ? destinazzjoni_VALUE_pożizzjoni[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) destinazzjoni_VALUE_pożizzjoni[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int fajl_handle = 꾸러미사용중 ? -2 : (int32_t)għodda_fetaħ(isem, 0);
    if (fajl_handle < 0) {
        char data_pożizzjoni[512]; int żball = mogħdija(isem, data_pożizzjoni); if (żball) return (uint32_t)żball;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Li_Jmiss_OFFSET = 자바클래스들[순번].isem; unsigned 안쪽순번 = 0;
            while (data_pożizzjoni[안쪽순번] && data_pożizzjoni[안쪽순번] == Li_Jmiss_OFFSET[안쪽순번]) 안쪽순번++;
            if (data_pożizzjoni[안쪽순번] || Li_Jmiss_OFFSET[안쪽순번]) continue;
            kompjuter_Word *destinazzjoni_VALUE_pożizzjoni = (kompjuter_Word *)destinazzjoni_data_ADDRESS;
            if (destinazzjoni_VALUE_pożizzjoni[0] < 자바클래스들[순번].daqqas) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].daqqas; 안쪽순번++) destinazzjoni_VALUE_pożizzjoni[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].daqqas;
        }
        return (uint32_t)fajl_handle;
    }
    kompjuter_Word *첫째값 = (kompjuter_Word *)destinazzjoni_data_ADDRESS;
    intptr_t daqqas = 호출(9, fajl_handle, 0, 0), 완료량 = 0;
    if (daqqas < 0 || (kompjuter_Word)daqqas > 첫째값[0]) { għodda_agħlaq(fajl_handle); return (uint32_t)(daqqas < 0 ? daqqas : -27); }
    unsigned char data_imblokka[256];
    while (완료량 < daqqas) {
        intptr_t element_COUNT = 호출(2, fajl_handle, (kompjuter_Word)data_imblokka, daqqas - 완료량 < 256 ? daqqas - 완료량 : 256);
        if (element_COUNT <= 0) { għodda_agħlaq(fajl_handle); return (uint32_t)(element_COUNT ? element_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = data_imblokka[순번];
        완료량 += element_COUNT;
    }
    għodda_agħlaq(fajl_handle); return 완료량;
}
kompjuter_Word għodda_kiteb(kompjuter_Word isem, kompjuter_Word 원본자료, kompjuter_Word entrata_COUNT) {
    const kompjuter_Word *첫째값 = (const kompjuter_Word *)원본자료;
    if (entrata_COUNT > 첫째값[0] || entrata_COUNT > 16384) return (uint32_t)-27;
    int fajl_handle = (int32_t)għodda_fetaħ(isem, 577); if (fajl_handle < 0) return (uint32_t)fajl_handle;
    unsigned char data_imblokka[256]; kompjuter_Word 완료량 = 0;
    while (완료량 < entrata_COUNT) {
        kompjuter_Word element_COUNT = entrata_COUNT - 완료량 < 256 ? entrata_COUNT - 완료량 : 256;
        for (kompjuter_Word 순번 = 0; 순번 < element_COUNT; 순번++) data_imblokka[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t miżura = 호출(1, fajl_handle, (kompjuter_Word)data_imblokka, element_COUNT);
        if (miżura <= 0) { għodda_agħlaq(fajl_handle); return (uint32_t)(miżura ? miżura : -5); }
        완료량 += miżura;
    }
    għodda_agħlaq(fajl_handle); return entrata_COUNT;
}
kompjuter_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
kompjuter_Word għodda_argument(kompjuter_Word LOOKUP_INDEX) {
    static const kompjuter_Word vojt_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (kompjuter_Word)vojt_VALUE;
    unsigned char 입력결과[256]; intptr_t element_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *data_pożizzjoni = 꾸러미진입클래스(); element_COUNT = 0; while (data_pożizzjoni[element_COUNT] && element_COUNT < 255) { 입력결과[element_COUNT] = data_pożizzjoni[element_COUNT]; element_COUNT++; } }
    else element_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (kompjuter_Word)입력결과, sizeof(입력결과));
    if (element_COUNT < 0) return (kompjuter_Word)vojt_VALUE;
    kompjuter_Word *miżura_data = 전달인수[LOOKUP_INDEX]; unsigned entrata_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < element_COUNT;) {
        unsigned kodiċi_tal_karattru = 입력결과[순번++], 더있음 = kodiċi_tal_karattru < 128 ? 0 : kodiċi_tal_karattru >= 0xc2 && kodiċi_tal_karattru < 0xe0 ? 1 : kodiċi_tal_karattru < 0xf0 && kodiċi_tal_karattru >= 0xe0 ? 2 : kodiċi_tal_karattru >= 0xf0 && kodiċi_tal_karattru <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > element_COUNT) { miżura_data[++entrata_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kodiċi_tal_karattru &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kodiċi_tal_karattru = (kodiċi_tal_karattru << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kodiċi_tal_karattru < 최소값 || kodiċi_tal_karattru > 0x10ffff || (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdfff)) kodiċi_tal_karattru = 0xfffd;
        if (kodiċi_tal_karattru >= 65536) { kodiċi_tal_karattru -= 65536; miżura_data[++entrata_COUNT] = 0xd800 | (kodiċi_tal_karattru >> 10); miżura_data[++entrata_COUNT] = 0xdc00 | (kodiċi_tal_karattru & 1023); }
        else miżura_data[++entrata_COUNT] = kodiċi_tal_karattru;
    }
    miżura_data[0] = entrata_COUNT; return (kompjuter_Word)miżura_data;
}
kompjuter_Word 도구분류(void) { return kategorija_VALUE; }
void 커널중단(const char *알림문) {
    const char *data_pożizzjoni = 알림문; while (*data_pożizzjoni) data_pożizzjoni++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_pożizzjoni - 알림문); karattru(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Bidu_utent_programm(int metodu_MODE) {
    kategorija_VALUE = metodu_MODE;
    unsigned char 첫항목[256]; intptr_t element_COUNT = 호출(15, 0, (kompjuter_Word)첫항목, sizeof(첫항목));
    if (metodu_MODE == 2 || (metodu_MODE == 1 && element_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metodu_MODE == 2 ? 0 : 1;
        char fajl_entrata_isem[256]; intptr_t tul_data = 호출(15, 꾸러미인수이동, (kompjuter_Word)fajl_entrata_isem, sizeof(fajl_entrata_isem));
        if (tul_data <= 0 || 꾸러미열기(fajl_entrata_isem) < 0) {
            static const char żball[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(żball, sizeof(żball) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int miżura = 자바진입();
    if (대기중짝글자) karattru(0xfffd);
    return miżura;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Familja, 접속번호; uint32_t ADDRESS; unsigned char 영값[8]; };
static struct 자바주소 UDP_ADDRESS(unsigned 접속번호) {
    struct 자바주소 첫째값 = {2, (uint16_t)((접속번호 << 8) | (접속번호 >> 8)), 0x0100007f, {0}}; return 첫째값;
}
kompjuter_Word għodda_UDP_fetaħ(kompjuter_Word 접속번호) {
    intptr_t fajl_handle = 호출(32, 2, 2, 17); if (fajl_handle < 0) return (uint32_t)fajl_handle;
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호);
    첫째값.ADDRESS = 0;
    intptr_t stat_VALUE = 호출(33, fajl_handle, (kompjuter_Word)&첫째값, sizeof(첫째값));
    if (stat_VALUE < 0) { għodda_agħlaq(fajl_handle); return (uint32_t)stat_VALUE; }
    return fajl_handle;
}
kompjuter_Word għodda_UDP_bagħat(kompjuter_Word fajl_handle, kompjuter_Word 접속번호, kompjuter_Word ARRAY_VALUE, kompjuter_Word tul_VALUE) {
    const kompjuter_Word *원본주소 = (const kompjuter_Word *)ARRAY_VALUE; unsigned char data[512];
    if (tul_VALUE > 512 || tul_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (kompjuter_Word 순번 = 0; 순번 < tul_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호);
    return (uint32_t)사용자호출(34, fajl_handle, (kompjuter_Word)data, tul_VALUE, 0, (kompjuter_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t element_COUNT) { return (element_COUNT>>24)|((element_COUNT>>8)&0xff00)|((element_COUNT<<8)&0xff0000)|(element_COUNT<<24); }
kompjuter_Word għodda_UDP_bagħat_ADDRESS(kompjuter_Word fajl_handle, kompjuter_Word ADDRESS, kompjuter_Word 접속번호, kompjuter_Word ARRAY_VALUE, kompjuter_Word tul_VALUE) {
    const kompjuter_Word *원본주소 = (const kompjuter_Word *)ARRAY_VALUE; unsigned char data[512];
    if (tul_VALUE > 512 || tul_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (kompjuter_Word 순번 = 0; 순번 < tul_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    return (uint32_t)사용자호출(34, fajl_handle, (kompjuter_Word)data, tul_VALUE, 0, (kompjuter_Word)&첫째값, sizeof(첫째값));
}
kompjuter_Word għodda_AQBAD(kompjuter_Word fajl_handle, kompjuter_Word ADDRESS, kompjuter_Word 접속번호) {
    struct 자바주소 첫째값 = UDP_ADDRESS(접속번호); 첫째값.ADDRESS = 바이트순서뒤집기(ADDRESS);
    uint32_t serje = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t miżura = 호출(37, fajl_handle, (kompjuter_Word)&첫째값, sizeof(첫째값));
        if (miżura != -115) return (uint32_t)miżura;
        if ((uint32_t)(호출(7, 0, 0, 0) - serje) >= 1000) return (uint32_t)-110;
    }
}
kompjuter_Word 도구전문받기(kompjuter_Word fajl_handle, kompjuter_Word ARRAY_VALUE, kompjuter_Word 수용량) {
    kompjuter_Word *destinazzjoni_ADDRESS = (kompjuter_Word *)ARRAY_VALUE; unsigned char data[512];
    if (수용량 > 512 || destinazzjoni_ADDRESS[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned tul_data = sizeof(첫째값);
    intptr_t element_COUNT = 사용자호출(35, fajl_handle, (kompjuter_Word)data, 수용량, 0, (kompjuter_Word)&첫째값, (kompjuter_Word)&tul_data);
    if (element_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < element_COUNT; 순번++) destinazzjoni_ADDRESS[순번 + 1] = data[순번]; destinazzjoni_ADDRESS[513] = (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535; destinazzjoni_ADDRESS[514] = 바이트순서뒤집기(첫째값.ADDRESS); }
    return (uint32_t)element_COUNT;
}
kompjuter_Word għodda_UDP_port(kompjuter_Word fajl_handle) {
    struct 자바주소 첫째값; unsigned tul_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fajl_handle, (kompjuter_Word)&첫째값, (kompjuter_Word)&tul_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.접속번호 << 8 | 첫째값.접속번호 >> 8) & 65535);
}
kompjuter_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
kompjuter_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
kompjuter_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
kompjuter_Word 도구화면기다리기(void) { return (uint32_t)화면키기다리기(); }
kompjuter_Word 도구사각형(kompjuter_Word koordinat_x, kompjuter_Word 세로좌표, kompjuter_Word 너비값, kompjuter_Word 높이값, kompjuter_Word 색상) {
    return (uint32_t)사용자호출(13, koordinat_x, 세로좌표, 색상, 너비값, 높이값, 0);
}

kompjuter_Word għodda_Stream(kompjuter_Word azzjoni,kompjuter_Word fajl_handle,kompjuter_Word VALUE){
    if(azzjoni==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADDRESS(VALUE);
    if(azzjoni==1){첫째값.ADDRESS=0;intptr_t 반환값=호출(33,fajl_handle,(kompjuter_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fajl_handle,4,0));}
    if(azzjoni==2)return (uint32_t)호출(37,fajl_handle,(kompjuter_Word)&첫째값,sizeof(첫째값));
    if(azzjoni==3)return (uint32_t)호출(39,fajl_handle,0,0);
    if(azzjoni==4)return għodda_UDP_port(fajl_handle);
    if(azzjoni==5)return (uint32_t)호출(40,fajl_handle,0,0);
    return (uint32_t)-22;
}
kompjuter_Word għodda_GUI(kompjuter_Word azzjoni,kompjuter_Word identifikatur_VALUE,kompjuter_Word 첫째값,kompjuter_Word SECOND_VALUE,kompjuter_Word kodiċi_tal_karattru,kompjuter_Word destinazzjoni_data){return (uint32_t)사용자호출(20,azzjoni,identifikatur_VALUE,첫째값,SECOND_VALUE,kodiċi_tal_karattru,destinazzjoni_data);}
kompjuter_Word għodda_GUI_SMS(kompjuter_Word identifikatur_VALUE,kompjuter_Word ARRAY_VALUE,kompjuter_Word element_COUNT){
    const kompjuter_Word *원본주소=(const kompjuter_Word *)ARRAY_VALUE;uint32_t data[127];unsigned entrata_COUNT=0;
    if(element_COUNT>원본주소[0])return (uint32_t)-22;
    for(kompjuter_Word 순번=0;순번<element_COUNT;순번++){unsigned karattru_kodifikar=원본주소[순번+1];if(karattru_kodifikar>=0xd800&&karattru_kodifikar<=0xdbff&&순번+1<element_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;karattru_kodifikar=0x10000+((karattru_kodifikar-0xd800)<<10)+낮은값-0xdc00;}if(entrata_COUNT==127)return (uint32_t)-22;data[entrata_COUNT++]=karattru_kodifikar;}
    return (uint32_t)사용자호출(21,identifikatur_VALUE,(kompjuter_Word)data,entrata_COUNT,0,0,0);
}
