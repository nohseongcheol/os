#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 file/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "bundle.h"
typedef uintptr_t machine_Word;
static int kategorya_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static machine_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned item_COUNT, machine_Word 첫째값, machine_Word SECOND_VALUE, machine_Word character_code) {
    return 사용자호출(item_COUNT, 첫째값, SECOND_VALUE, character_code, 0, 0, 0);
}
static void 바이트들(const char *data_posisyon, size_t item_COUNT) { 호출(1, 1, (machine_Word)data_posisyon, item_COUNT); }
static void karakter(unsigned character_code) {
    unsigned char data[4]; unsigned item_COUNT = 0;
    if (character_code < 128) data[item_COUNT++] = character_code;
    else if (character_code < 2048) { data[item_COUNT++] = 0xc0 | (character_code >> 6); data[item_COUNT++] = 0x80 | (character_code & 63); }
    else if (character_code < 65536) { data[item_COUNT++] = 0xe0 | (character_code >> 12); data[item_COUNT++] = 0x80 | ((character_code >> 6) & 63); data[item_COUNT++] = 0x80 | (character_code & 63); }
    else { data[item_COUNT++] = 0xf0 | (character_code >> 18); data[item_COUNT++] = 0x80 | ((character_code >> 12) & 63); data[item_COUNT++] = 0x80 | ((character_code >> 6) & 63); data[item_COUNT++] = 0x80 | (character_code & 63); }
    바이트들((const char *)data, item_COUNT);
}
machine_Word tool_karakter(machine_Word VALUE) {
    unsigned character_code = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (character_code >= 0xdc00 && character_code <= 0xdfff) { karakter(0x10000 + ((높은부분 - 0xd800) << 10) + character_code - 0xdc00); return 1; }
        karakter(0xfffd);
    }
    if (character_code >= 0xd800 && character_code <= 0xdbff) 대기중짝글자 = character_code;
    else karakter(character_code > 0x10ffff || (character_code >= 0xdc00 && character_code <= 0xdfff) ? 0xfffd : character_code);
    return 1;
}
machine_Word 도구출력(machine_Word VALUE) {
    const machine_Word *string_data = (const machine_Word *)VALUE;
    for (machine_Word 순번 = 0; 순번 < string_data[0]; 순번++) tool_karakter(string_data[순번 + 1]);
    return string_data[0];
}
static int path(machine_Word bagay_Sanggunian, char sukat_data[512]) {
    const machine_Word *첫째값 = (const machine_Word *)bagay_Sanggunian;
    unsigned 사용량 = 0;
    for (machine_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned character_code = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] pamamaraan_MODE 경로와 호환한다.
        if (character_code >= 0xd800 && character_code <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; character_code = 0x10000 + ((character_code - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (character_code >= 0xd800 && character_code <= 0xdfff) return -22;
        unsigned item_COUNT = character_code < 128 ? 1 : character_code < 2048 ? 2 : character_code < 65536 ? 3 : 4;
        if (사용량 + item_COUNT > 511) return -36;
        if (item_COUNT == 1) sukat_data[사용량++] = character_code;
        else {
            sukat_data[사용량++] = (item_COUNT == 2 ? 0xc0 : item_COUNT == 3 ? 0xe0 : 0xf0) | (character_code >> (6 * (item_COUNT - 1)));
            for (unsigned 안쪽순번 = item_COUNT - 1; 안쪽순번; 안쪽순번--) sukat_data[사용량++] = 0x80 | ((character_code >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    sukat_data[사용량] = 0; return 사용량 ? 0 : -22;
}
machine_Word tool_buksan(machine_Word pangalan, machine_Word kompigurasyon_Background_Intelligent_Transfer_Service) {
    char data_posisyon[512]; int error = path(pangalan, data_posisyon);
    return (uint32_t)(error ? error : 호출(3, (machine_Word)data_posisyon, kompigurasyon_Background_Intelligent_Transfer_Service, 0));
}
machine_Word tool_isara(machine_Word file_hawakán) { return (uint32_t)호출(4, file_hawakán, 0, 0); }
machine_Word 도구바이트읽기(machine_Word file_hawakán) {
    unsigned char SECOND_VALUE; intptr_t item_COUNT = 호출(2, file_hawakán, (machine_Word)&SECOND_VALUE, 1);
    return (uint32_t)(item_COUNT == 1 ? SECOND_VALUE : item_COUNT == 0 ? 256 : item_COUNT);
}
machine_Word tool_sumulat_byte(machine_Word file_hawakán, machine_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, file_hawakán, (machine_Word)&SECOND_VALUE, 1);
}
machine_Word 도구읽기(machine_Word pangalan, machine_Word patutunguhan_data_email) {
    if (꾸러미사용중) {
        char data_posisyon[512]; int error = path(pangalan, data_posisyon); if (error) return (uint32_t)error;
        unsigned item_COUNT = 0; while (data_posisyon[item_COUNT]) item_COUNT++;
        if (item_COUNT >= 6) for (unsigned 순번 = 0; 순번 < item_COUNT - 6; 순번++) if (data_posisyon[순번] == '.') data_posisyon[순번] = '/';
        unsigned char 바이트들[16384]; machine_Word *patutunguhan_VALUE_posisyon = (machine_Word *)patutunguhan_data_email;
        int RECEIVED_COUNT = 꾸러미읽기(data_posisyon, 바이트들, patutunguhan_VALUE_posisyon[0] < sizeof(바이트들) ? patutunguhan_VALUE_posisyon[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) patutunguhan_VALUE_posisyon[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int file_hawakán = 꾸러미사용중 ? -2 : (int32_t)tool_buksan(pangalan, 0);
    if (file_hawakán < 0) {
        char data_posisyon[512]; int error = path(pangalan, data_posisyon); if (error) return (uint32_t)error;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Susunod_OFFSET = 자바클래스들[순번].pangalan; unsigned 안쪽순번 = 0;
            while (data_posisyon[안쪽순번] && data_posisyon[안쪽순번] == Susunod_OFFSET[안쪽순번]) 안쪽순번++;
            if (data_posisyon[안쪽순번] || Susunod_OFFSET[안쪽순번]) continue;
            machine_Word *patutunguhan_VALUE_posisyon = (machine_Word *)patutunguhan_data_email;
            if (patutunguhan_VALUE_posisyon[0] < 자바클래스들[순번].sukat_82232621) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].sukat_82232621; 안쪽순번++) patutunguhan_VALUE_posisyon[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].sukat_82232621;
        }
        return (uint32_t)file_hawakán;
    }
    machine_Word *첫째값 = (machine_Word *)patutunguhan_data_email;
    intptr_t sukat_82232621 = 호출(9, file_hawakán, 0, 0), 완료량 = 0;
    if (sukat_82232621 < 0 || (machine_Word)sukat_82232621 > 첫째값[0]) { tool_isara(file_hawakán); return (uint32_t)(sukat_82232621 < 0 ? sukat_82232621 : -27); }
    unsigned char data_i_block[256];
    while (완료량 < sukat_82232621) {
        intptr_t item_COUNT = 호출(2, file_hawakán, (machine_Word)data_i_block, sukat_82232621 - 완료량 < 256 ? sukat_82232621 - 완료량 : 256);
        if (item_COUNT <= 0) { tool_isara(file_hawakán); return (uint32_t)(item_COUNT ? item_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) 첫째값[1 + 완료량 + 순번] = data_i_block[순번];
        완료량 += item_COUNT;
    }
    tool_isara(file_hawakán); return 완료량;
}
machine_Word tool_sumulat(machine_Word pangalan, machine_Word 원본자료, machine_Word pagpasok_COUNT) {
    const machine_Word *첫째값 = (const machine_Word *)원본자료;
    if (pagpasok_COUNT > 첫째값[0] || pagpasok_COUNT > 16384) return (uint32_t)-27;
    int file_hawakán = (int32_t)tool_buksan(pangalan, 577); if (file_hawakán < 0) return (uint32_t)file_hawakán;
    unsigned char data_i_block[256]; machine_Word 완료량 = 0;
    while (완료량 < pagpasok_COUNT) {
        machine_Word item_COUNT = pagpasok_COUNT - 완료량 < 256 ? pagpasok_COUNT - 완료량 : 256;
        for (machine_Word 순번 = 0; 순번 < item_COUNT; 순번++) data_i_block[순번] = 첫째값[1 + 완료량 + 순번];
        intptr_t sukat = 호출(1, file_hawakán, (machine_Word)data_i_block, item_COUNT);
        if (sukat <= 0) { tool_isara(file_hawakán); return (uint32_t)(sukat ? sukat : -5); }
        완료량 += sukat;
    }
    tool_isara(file_hawakán); return pagpasok_COUNT;
}
machine_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
machine_Word tool_argumento(machine_Word LOOKUP_INDEX) {
    static const machine_Word walang_laman_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (machine_Word)walang_laman_VALUE;
    unsigned char 입력결과[256]; intptr_t item_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *data_posisyon = 꾸러미진입클래스(); item_COUNT = 0; while (data_posisyon[item_COUNT] && item_COUNT < 255) { 입력결과[item_COUNT] = data_posisyon[item_COUNT]; item_COUNT++; } }
    else item_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (machine_Word)입력결과, sizeof(입력결과));
    if (item_COUNT < 0) return (machine_Word)walang_laman_VALUE;
    machine_Word *sukat_data = 전달인수[LOOKUP_INDEX]; unsigned pagpasok_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < item_COUNT;) {
        unsigned character_code = 입력결과[순번++], 더있음 = character_code < 128 ? 0 : character_code >= 0xc2 && character_code < 0xe0 ? 1 : character_code < 0xf0 && character_code >= 0xe0 ? 2 : character_code >= 0xf0 && character_code <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > item_COUNT) { sukat_data[++pagpasok_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) character_code &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { character_code = (character_code << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || character_code < 최소값 || character_code > 0x10ffff || (character_code >= 0xd800 && character_code <= 0xdfff)) character_code = 0xfffd;
        if (character_code >= 65536) { character_code -= 65536; sukat_data[++pagpasok_COUNT] = 0xd800 | (character_code >> 10); sukat_data[++pagpasok_COUNT] = 0xdc00 | (character_code & 1023); }
        else sukat_data[++pagpasok_COUNT] = character_code;
    }
    sukat_data[0] = pagpasok_COUNT; return (machine_Word)sukat_data;
}
machine_Word 도구분류(void) { return kategorya_VALUE; }
void 커널중단(const char *알림문) {
    const char *data_posisyon = 알림문; while (*data_posisyon) data_posisyon++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_posisyon - 알림문); karakter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Start_gumagamit_app(int pamamaraan_MODE) {
    kategorya_VALUE = pamamaraan_MODE;
    unsigned char 첫항목[256]; intptr_t item_COUNT = 호출(15, 0, (machine_Word)첫항목, sizeof(첫항목));
    if (pamamaraan_MODE == 2 || (pamamaraan_MODE == 1 && item_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = pamamaraan_MODE == 2 ? 0 : 1;
        char file_pagpasok_pangalan[256]; intptr_t haba_data = 호출(15, 꾸러미인수이동, (machine_Word)file_pagpasok_pangalan, sizeof(file_pagpasok_pangalan));
        if (haba_data <= 0 || 꾸러미열기(file_pagpasok_pangalan) < 0) {
            static const char error[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(error, sizeof(error) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int sukat = 자바진입();
    if (대기중짝글자) karakter(0xfffd);
    return sukat;
}

// UDP는 자체 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Pamilya, numero_ng_port; uint32_t email; unsigned char 영값[8]; };
static struct 자바주소 UDP_email(unsigned numero_ng_port) {
    struct 자바주소 첫째값 = {2, (uint16_t)((numero_ng_port << 8) | (numero_ng_port >> 8)), 0x0100007f, {0}}; return 첫째값;
}
machine_Word tool_UDP_buksan(machine_Word numero_ng_port) {
    intptr_t file_hawakán = 호출(32, 2, 2, 17); if (file_hawakán < 0) return (uint32_t)file_hawakán;
    struct 자바주소 첫째값 = UDP_email(numero_ng_port);
    첫째값.email = 0;
    intptr_t katayuan_VALUE = 호출(33, file_hawakán, (machine_Word)&첫째값, sizeof(첫째값));
    if (katayuan_VALUE < 0) { tool_isara(file_hawakán); return (uint32_t)katayuan_VALUE; }
    return file_hawakán;
}
machine_Word tool_UDP_i_email(machine_Word file_hawakán, machine_Word numero_ng_port, machine_Word ARRAY_VALUE, machine_Word haba_VALUE) {
    const machine_Word *원본주소 = (const machine_Word *)ARRAY_VALUE; unsigned char data[512];
    if (haba_VALUE > 512 || haba_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (machine_Word 순번 = 0; 순번 < haba_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_email(numero_ng_port);
    return (uint32_t)사용자호출(34, file_hawakán, (machine_Word)data, haba_VALUE, 0, (machine_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t item_COUNT) { return (item_COUNT>>24)|((item_COUNT>>8)&0xff00)|((item_COUNT<<8)&0xff0000)|(item_COUNT<<24); }
machine_Word tool_UDP_i_email_email(machine_Word file_hawakán, machine_Word email, machine_Word numero_ng_port, machine_Word ARRAY_VALUE, machine_Word haba_VALUE) {
    const machine_Word *원본주소 = (const machine_Word *)ARRAY_VALUE; unsigned char data[512];
    if (haba_VALUE > 512 || haba_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (machine_Word 순번 = 0; 순번 < haba_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_email(numero_ng_port); 첫째값.email = 바이트순서뒤집기(email);
    return (uint32_t)사용자호출(34, file_hawakán, (machine_Word)data, haba_VALUE, 0, (machine_Word)&첫째값, sizeof(첫째값));
}
machine_Word tool_CONNECT(machine_Word file_hawakán, machine_Word email, machine_Word numero_ng_port) {
    struct 자바주소 첫째값 = UDP_email(numero_ng_port); 첫째값.email = 바이트순서뒤집기(email);
    uint32_t run = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t sukat = 호출(37, file_hawakán, (machine_Word)&첫째값, sizeof(첫째값));
        if (sukat != -115) return (uint32_t)sukat;
        if ((uint32_t)(호출(7, 0, 0, 0) - run) >= 1000) return (uint32_t)-110;
    }
}
machine_Word 도구전문받기(machine_Word file_hawakán, machine_Word ARRAY_VALUE, machine_Word 수용량) {
    machine_Word *patutunguhan_email = (machine_Word *)ARRAY_VALUE; unsigned char data[512];
    if (수용량 > 512 || patutunguhan_email[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned haba_data = sizeof(첫째값);
    intptr_t item_COUNT = 사용자호출(35, file_hawakán, (machine_Word)data, 수용량, 0, (machine_Word)&첫째값, (machine_Word)&haba_data);
    if (item_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) patutunguhan_email[순번 + 1] = data[순번]; patutunguhan_email[513] = (첫째값.numero_ng_port << 8 | 첫째값.numero_ng_port >> 8) & 65535; patutunguhan_email[514] = 바이트순서뒤집기(첫째값.email); }
    return (uint32_t)item_COUNT;
}
machine_Word tool_UDP_port(machine_Word file_hawakán) {
    struct 자바주소 첫째값; unsigned haba_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, file_hawakán, (machine_Word)&첫째값, (machine_Word)&haba_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.numero_ng_port << 8 | 첫째값.numero_ng_port >> 8) & 65535);
}
machine_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
machine_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
machine_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
machine_Word tool_graphics_maghintay(void) { return (uint32_t)화면키기다리기(); }
machine_Word 도구사각형(machine_Word x_coordinate, machine_Word Y_button_coordinate, machine_Word 너비값, machine_Word 높이값, machine_Word 색상) {
    return (uint32_t)사용자호출(13, x_coordinate, Y_button_coordinate, 색상, 너비값, 높이값, 0);
}

machine_Word tool_Stream(machine_Word aksyon,machine_Word file_hawakán,machine_Word VALUE){
    if(aksyon==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_email(VALUE);
    if(aksyon==1){첫째값.email=0;intptr_t 반환값=호출(33,file_hawakán,(machine_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,file_hawakán,4,0));}
    if(aksyon==2)return (uint32_t)호출(37,file_hawakán,(machine_Word)&첫째값,sizeof(첫째값));
    if(aksyon==3)return (uint32_t)호출(39,file_hawakán,0,0);
    if(aksyon==4)return tool_UDP_port(file_hawakán);
    if(aksyon==5)return (uint32_t)호출(40,file_hawakán,0,0);
    return (uint32_t)-22;
}
machine_Word tool_GUI(machine_Word aksyon,machine_Word tagakilala_VALUE,machine_Word 첫째값,machine_Word SECOND_VALUE,machine_Word character_code,machine_Word patutunguhan_data){return (uint32_t)사용자호출(20,aksyon,tagakilala_VALUE,첫째값,SECOND_VALUE,character_code,patutunguhan_data);}
machine_Word tool_GUI_SMS(machine_Word tagakilala_VALUE,machine_Word ARRAY_VALUE,machine_Word item_COUNT){
    const machine_Word *원본주소=(const machine_Word *)ARRAY_VALUE;uint32_t data[127];unsigned pagpasok_COUNT=0;
    if(item_COUNT>원본주소[0])return (uint32_t)-22;
    for(machine_Word 순번=0;순번<item_COUNT;순번++){unsigned karakter_pag_encode=원본주소[순번+1];if(karakter_pag_encode>=0xd800&&karakter_pag_encode<=0xdbff&&순번+1<item_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;karakter_pag_encode=0x10000+((karakter_pag_encode-0xd800)<<10)+낮은값-0xdc00;}if(pagpasok_COUNT==127)return (uint32_t)-22;data[pagpasok_COUNT++]=karakter_pag_encode;}
    return (uint32_t)사용자호출(21,tagakilala_VALUE,(machine_Word)data,pagpasok_COUNT,0,0,0);
}
