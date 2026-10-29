#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Network_Stack.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, control = -1, mano_mano_koneksyon = -1, data = -1;
static unsigned 로그인됨, gumagamit_OK, linya_sukat, 줄오류, lumabas_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned tumugon_sukat, 응답전송량, Susunod_numero_ng_port;
static uint32_t Aktibidad;
static char linya[256], 응답모음[2048], file_pagpasok_pangalan[64], lipat_pangalan[64];
static unsigned char lipat_katayuan[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void tumugon(const char *string_data) {
    size_t item_COUNT = strlen(string_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, tumugon_sukat - 응답전송량); tumugon_sukat -= 응답전송량; 응답전송량 = 0; }
    if (item_COUNT > sizeof(응답모음) - tumugon_sukat) { lumabas_app = 1; return; }
    memcpy(응답모음 + tumugon_sukat, string_data, item_COUNT); tumugon_sukat += item_COUNT;
}
static void 수치(unsigned VALUE, char *sukat_data, unsigned *item_COUNT) {
    char digit_COUNT[10]; unsigned pagpasok_COUNT = 0;
    do { digit_COUNT[pagpasok_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (pagpasok_COUNT) sukat_data[(*item_COUNT)++] = digit_COUNT[--pagpasok_COUNT];
}
static void Hinto_lipat(void) {
    if (data >= 0) isara_Network(data); if (mano_mano_koneksyon >= 0) isara_Network(mano_mano_koneksyon);
    data = mano_mano_koneksyon = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void idiskonekta(void) {
    Hinto_lipat(); if (control >= 0) isara_Network(control); control = -1;
    로그인됨 = gumagamit_OK = linya_sukat = 줄오류 = tumugon_sukat = 응답전송량 = lumabas_app = 0;
}
int file_lipat_control(int aksyon) {
    if (aksyon == 2) return 수신창구 >= 0;
    if (aksyon == 0) { idiskonekta(); if (수신창구 >= 0) isara_Network(수신창구); 수신창구 = -1; return 0; }
    if (aksyon != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { isara_Network(수신창구); 수신창구 = -1; } return 반환값;
}
static int path(const char *pangalan) {
    unsigned item_COUNT = 0; if (*pangalan == '/') pangalan++;
    if (!*pangalan || 같은지(pangalan, ".") || 같은지(pangalan, "..")) return 0;
    file_pagpasok_pangalan[item_COUNT++] = '/';
    while (*pangalan) {
        unsigned char character_code = *pangalan++;
        if (item_COUNT >= 63 || character_code < 32 || character_code == 127 || character_code == '/' || character_code == '\\') return 0;
        file_pagpasok_pangalan[item_COUNT++] = character_code;
    }
    file_pagpasok_pangalan[item_COUNT] = 0; return 1;
}
static void i_email_list(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int item_COUNT = 자바파일항목길이(순번); if (item_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned pagpasok_COUNT = strlen(앞부분); memcpy(lipat_katayuan + 사용량, 앞부분, pagpasok_COUNT); 사용량 += pagpasok_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)lipat_katayuan, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        pagpasok_COUNT = strlen(뒷부분); memcpy(lipat_katayuan + 사용량, 뒷부분, pagpasok_COUNT); 사용량 += pagpasok_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < item_COUNT; 안쪽순번++) lipat_katayuan[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        lipat_katayuan[사용량++] = '\r'; lipat_katayuan[사용량++] = '\n';
    }
}
static void Ihanda_mano_mano_koneksyon(int 확장여부) {
    if (수행작업) { tumugon("450 Transfer in progress\r\n"); return; }
    Hinto_lipat(); mano_mano_koneksyon = 통신끝점만들기(1);
    if (mano_mano_koneksyon >= 0) 통신주소재사용(mano_mano_koneksyon);
    unsigned numero_ng_port = 50000 + Susunod_numero_ng_port++ % 8;
    if (mano_mano_koneksyon < 0 || 망주소묶기(mano_mano_koneksyon, 망상태읽기(0,0), numero_ng_port) || 연결기다리기(mano_mano_koneksyon)) {
        Hinto_lipat(); tumugon("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned item_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, item_COUNT);
    if (확장여부) { 수치(numero_ng_port, 응답자료, &item_COUNT); 응답자료[item_COUNT++] = '|'; }
    else {
        uint32_t email=망상태읽기(0,0);
        for (int posisyon_INDEX=24;posisyon_INDEX>=0;posisyon_INDEX-=8) { 수치((email>>posisyon_INDEX)&255,응답자료,&item_COUNT);응답자료[item_COUNT++]=','; }
        수치(numero_ng_port / 256, 응답자료, &item_COUNT); 응답자료[item_COUNT++] = ','; 수치(numero_ng_port % 256, 응답자료, &item_COUNT);
    }
    응답자료[item_COUNT++] = ')'; 응답자료[item_COUNT++] = '\r'; 응답자료[item_COUNT++] = '\n'; 응답자료[item_COUNT] = 0; tumugon(응답자료);
}
static void utos(void) {
    linya[linya_sukat] = 0;
    char *부가인수 = linya; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(linya, "QUIT")) { Hinto_lipat(); tumugon("221 Goodbye\r\n"); lumabas_app = 1; return; }
    if (같은지(linya, "NOOP")) { tumugon("200 OK\r\n"); return; }
    if (같은지(linya, "SYST")) { tumugon("215 UNIX Type: L8\r\n"); return; }
    if (같은지(linya, "FEAT")) { tumugon("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(linya, "USER")) { 로그인됨 = 0; gumagamit_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); tumugon(gumagamit_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(linya, "PASS")) { 로그인됨 = gumagamit_OK; tumugon(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { tumugon("530 Login first\r\n"); return; }
    if (같은지(linya, "PWD")) tumugon("257 \"/\"\r\n");
    else if (같은지(linya, "CWD")) tumugon(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(linya, "TYPE")) tumugon(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(linya, "OPTS")) tumugon(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(linya, "PASV")) Ihanda_mano_mano_koneksyon(0);
    else if (같은지(linya, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) tumugon("522 IPv4 only\r\n"); else Ihanda_mano_mano_koneksyon(1); }
    else if (같은지(linya, "ABOR")) { Hinto_lipat(); tumugon("226 Transfer aborted\r\n"); }
    else if (같은지(linya, "DELE")) { tumugon(path(부가인수) && pk_unlink(file_pagpasok_pangalan) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(linya, "LIST") || 같은지(linya, "NLST") || 같은지(linya, "MLSD")) {
        if (수행작업) { tumugon("450 Transfer in progress\r\n"); return; }
        if (mano_mano_koneksyon < 0 && data < 0) { tumugon("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { tumugon("550 Root listing only\r\n"); return; }
        i_email_list(같은지(linya,"MLSD") ? 2 : 같은지(linya,"LIST") ? 1 : 0); 수행작업 = 2;
        tumugon("150 Opening directory listing\r\n");
    }
    else if (같은지(linya, "SIZE")) {
        if (!path(부가인수)) { tumugon("550 Invalid filename\r\n"); return; }
        int file_hawakán = pk_open(file_pagpasok_pangalan, mababasa_lamang_VALUE, 0); if (file_hawakán < 0) { tumugon("550 File unavailable\r\n"); return; }
        int sukat_82232621 = pk_size(file_hawakán); pk_close(file_hawakán); char 응답자료[32] = "213 "; unsigned item_COUNT = 4;
        수치(sukat_82232621, 응답자료, &item_COUNT); 응답자료[item_COUNT++] = '\r'; 응답자료[item_COUNT++] = '\n'; 응답자료[item_COUNT] = 0; tumugon(응답자료);
    } else if (같은지(linya, "STOR") || 같은지(linya, "RETR")) {
        if (수행작업) { tumugon("450 Transfer in progress\r\n"); return; }
        if (mano_mano_koneksyon < 0 && data < 0) { tumugon("425 Use PASV or EPSV\r\n"); return; }
        if (!path(부가인수)) { tumugon("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(linya, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(lipat_pangalan, file_pagpasok_pangalan, strlen(file_pagpasok_pangalan) + 1);
        if (수행작업 == 2) {
            int file_hawakán = pk_open(file_pagpasok_pangalan, mababasa_lamang_VALUE, 0);
            if (file_hawakán < 0) { 수행작업 = 0; tumugon("550 File unavailable\r\n"); return; }
            int item_COUNT = pk_read(file_hawakán, lipat_katayuan, sizeof(lipat_katayuan)); pk_close(file_hawakán);
            if (item_COUNT < 0) { 수행작업 = 0; tumugon("451 Read failed\r\n"); return; } 사용량 = item_COUNT;
        }
        tumugon("150 Opening binary data connection\r\n");
    } else tumugon("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Papasok_koneksyon = 망연결받기(수신창구);
    if (Papasok_koneksyon >= 0) {
        if (control >= 0) { 통신쓰기(Papasok_koneksyon, "421 One session at a time\r\n", 27); isara_Network(Papasok_koneksyon); }
        else { control = Papasok_koneksyon; Aktibidad = 보드밀리초(); tumugon("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (control < 0) return;
    if ((uint32_t)(보드밀리초() - Aktibidad) > 60000) { idiskonekta(); return; }
    if (!lumabas_app) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char character_code; int 반환값 = 통신읽기(control, &character_code, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { idiskonekta(); return; } Aktibidad = 보드밀리초();
        if (character_code == '\n') { if (줄오류) tumugon("500 Command too long or invalid\r\n"); else utos(); linya_sukat = 줄오류 = 0; if (lumabas_app) break; }
        else if (character_code != '\r') { if (!character_code || linya_sukat >= sizeof(linya) - 1) 줄오류 = 1; else linya[linya_sukat++] = character_code; }
    }
    if (mano_mano_koneksyon >= 0 && data < 0) {
        int 반환값 = 망연결받기(mano_mano_koneksyon);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(control)) isara_Network(반환값);
            else { data = 반환값; isara_Network(mano_mano_koneksyon); mano_mano_koneksyon = -1; Aktibidad = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char data_i_block[512]; int item_COUNT = 통신읽기(data, data_i_block, sizeof(data_i_block));
        if (item_COUNT == -11) break;
        if (item_COUNT < 0) { Hinto_lipat(); tumugon("426 Data connection failed\r\n"); break; }
        Aktibidad = 보드밀리초();
        if (item_COUNT == 0) {
            int sukat = -1;
            if (!실패여부) {
                int file_hawakán = pk_open(lipat_pangalan, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (file_hawakán >= 0) { sukat = pk_write(file_hawakán, lipat_katayuan, 사용량); pk_close(file_hawakán); }
            }
            int 성공여부 = !실패여부 && sukat == (int)사용량; Hinto_lipat(); tumugon(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)item_COUNT > sizeof(lipat_katayuan) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(lipat_katayuan + 사용량, data_i_block, item_COUNT); 사용량 += item_COUNT; }
    }
    if (수행작업 == 2 && data >= 0) {
        int item_COUNT = 통신쓰기(data, lipat_katayuan + 보낸수, 사용량 - 보낸수);
        if (item_COUNT >= 0) { 보낸수 += item_COUNT; Aktibidad = 보드밀리초(); if (보낸수 == 사용량) { Hinto_lipat(); tumugon("226 Transfer complete\r\n"); } }
        else if (item_COUNT != -11) { Hinto_lipat(); tumugon("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < tumugon_sukat) {
        int item_COUNT = 통신쓰기(control, 응답모음 + 응답전송량, tumugon_sukat - 응답전송량);
        if (item_COUNT > 0) 응답전송량 += item_COUNT; else if (item_COUNT != -11) { idiskonekta(); return; }
    }
    if (응답전송량 == tumugon_sukat) { tumugon_sukat = 응답전송량 = 0; if (lumabas_app) idiskonekta(); }
}
