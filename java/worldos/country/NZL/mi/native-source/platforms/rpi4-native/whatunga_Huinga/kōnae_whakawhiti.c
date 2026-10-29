#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "whatunga_Huinga.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, mana = -1, ā_ringa_hononga = -1, raraunga = -1;
static unsigned 로그인됨, kaiwhakamahi_ĀE, hononga_rahi, 줄오류, wehe_kaupapa, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned whakautu_rahi, 응답전송량, 다음접속번호;
static uint32_t Ngohe;
static char hononga[256], 응답모음[2048], kōnae_tāurunga_ingoa[64], whakawhiti_ingoa[64];
static unsigned char whakawhiti_tūnga[16384];
static int 같은지(const char *첫째값, const char *SECOND_uara) { while (*첫째값 && *첫째값 == *SECOND_uara) { 첫째값++; SECOND_uara++; } return *첫째값 == *SECOND_uara; }
static void whakautu(const char *aho_raraunga) {
    size_t tuemi_COUNT = strlen(aho_raraunga);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, whakautu_rahi - 응답전송량); whakautu_rahi -= 응답전송량; 응답전송량 = 0; }
    if (tuemi_COUNT > sizeof(응답모음) - whakautu_rahi) { wehe_kaupapa = 1; return; }
    memcpy(응답모음 + whakautu_rahi, aho_raraunga, tuemi_COUNT); whakautu_rahi += tuemi_COUNT;
}
static void 수치(unsigned uara, char *mēhua_raraunga, unsigned *tuemi_COUNT) {
    char mati_COUNT[10]; unsigned tāurunga_COUNT = 0;
    do { mati_COUNT[tāurunga_COUNT++] = '0' + uara % 10; uara /= 10; } while (uara);
    while (tāurunga_COUNT) mēhua_raraunga[(*tuemi_COUNT)++] = mati_COUNT[--tāurunga_COUNT];
}
static void tāpu_whakawhiti(void) {
    if (raraunga >= 0) kati_whatunga(raraunga); if (ā_ringa_hononga >= 0) kati_whatunga(ā_ringa_hononga);
    raraunga = ā_ringa_hononga = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void momotu(void) {
    tāpu_whakawhiti(); if (mana >= 0) kati_whatunga(mana); mana = -1;
    로그인됨 = kaiwhakamahi_ĀE = hononga_rahi = 줄오류 = whakautu_rahi = 응답전송량 = wehe_kaupapa = 0;
}
int kōnae_whakawhiti_mana(int hohenga) {
    if (hohenga == 2) return 수신창구 >= 0;
    if (hohenga == 0) { momotu(); if (수신창구 >= 0) kati_whatunga(수신창구); 수신창구 = -1; return 0; }
    if (hohenga != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { kati_whatunga(수신창구); 수신창구 = -1; } return 반환값;
}
static int ara(const char *Ingoa) {
    unsigned tuemi_COUNT = 0; if (*Ingoa == '/') Ingoa++;
    if (!*Ingoa || 같은지(Ingoa, ".") || 같은지(Ingoa, "..")) return 0;
    kōnae_tāurunga_ingoa[tuemi_COUNT++] = '/';
    while (*Ingoa) {
        unsigned char waehere_pūāhua = *Ingoa++;
        if (tuemi_COUNT >= 63 || waehere_pūāhua < 32 || waehere_pūāhua == 127 || waehere_pūāhua == '/' || waehere_pūāhua == '\\') return 0;
        kōnae_tāurunga_ingoa[tuemi_COUNT++] = waehere_pūāhua;
    }
    kōnae_tāurunga_ingoa[tuemi_COUNT] = 0; return 1;
}
static void tuku_Rārangi(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int tuemi_COUNT = 자바파일항목길이(순번); if (tuemi_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned tāurunga_COUNT = strlen(앞부분); memcpy(whakawhiti_tūnga + 사용량, 앞부분, tāurunga_COUNT); 사용량 += tāurunga_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)whakawhiti_tūnga, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        tāurunga_COUNT = strlen(뒷부분); memcpy(whakawhiti_tūnga + 사용량, 뒷부분, tāurunga_COUNT); 사용량 += tāurunga_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < tuemi_COUNT; 안쪽순번++) whakawhiti_tūnga[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        whakawhiti_tūnga[사용량++] = '\r'; whakawhiti_tūnga[사용량++] = '\n';
    }
}
static void Whakarite_ā_ringa_hononga(int 확장여부) {
    if (수행작업) { whakautu("450 Transfer in progress\r\n"); return; }
    tāpu_whakawhiti(); ā_ringa_hononga = 통신끝점만들기(1);
    if (ā_ringa_hononga >= 0) 통신주소재사용(ā_ringa_hononga);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (ā_ringa_hononga < 0 || 망주소묶기(ā_ringa_hononga, 망상태읽기(0,0), 접속번호) || 연결기다리기(ā_ringa_hononga)) {
        tāpu_whakawhiti(); whakautu("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned tuemi_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, tuemi_COUNT);
    if (확장여부) { 수치(접속번호, 응답자료, &tuemi_COUNT); 응답자료[tuemi_COUNT++] = '|'; }
    else {
        uint32_t ADDRESS=망상태읽기(0,0);
        for (int tūranga_INDEX=24;tūranga_INDEX>=0;tūranga_INDEX-=8) { 수치((ADDRESS>>tūranga_INDEX)&255,응답자료,&tuemi_COUNT);응답자료[tuemi_COUNT++]=','; }
        수치(접속번호 / 256, 응답자료, &tuemi_COUNT); 응답자료[tuemi_COUNT++] = ','; 수치(접속번호 % 256, 응답자료, &tuemi_COUNT);
    }
    응답자료[tuemi_COUNT++] = ')'; 응답자료[tuemi_COUNT++] = '\r'; 응답자료[tuemi_COUNT++] = '\n'; 응답자료[tuemi_COUNT] = 0; whakautu(응답자료);
}
static void tono(void) {
    hononga[hononga_rahi] = 0;
    char *부가인수 = hononga; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(hononga, "QUIT")) { tāpu_whakawhiti(); whakautu("221 Goodbye\r\n"); wehe_kaupapa = 1; return; }
    if (같은지(hononga, "NOOP")) { whakautu("200 OK\r\n"); return; }
    if (같은지(hononga, "SYST")) { whakautu("215 UNIX Type: L8\r\n"); return; }
    if (같은지(hononga, "FEAT")) { whakautu("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(hononga, "USER")) { 로그인됨 = 0; kaiwhakamahi_ĀE = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); whakautu(kaiwhakamahi_ĀE ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(hononga, "PASS")) { 로그인됨 = kaiwhakamahi_ĀE; whakautu(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { whakautu("530 Login first\r\n"); return; }
    if (같은지(hononga, "PWD")) whakautu("257 \"/\"\r\n");
    else if (같은지(hononga, "CWD")) whakautu(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(hononga, "TYPE")) whakautu(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(hononga, "OPTS")) whakautu(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(hononga, "PASV")) Whakarite_ā_ringa_hononga(0);
    else if (같은지(hononga, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) whakautu("522 IPv4 only\r\n"); else Whakarite_ā_ringa_hononga(1); }
    else if (같은지(hononga, "ABOR")) { tāpu_whakawhiti(); whakautu("226 Transfer aborted\r\n"); }
    else if (같은지(hononga, "DELE")) { whakautu(ara(부가인수) && pk_unlink(kōnae_tāurunga_ingoa) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(hononga, "LIST") || 같은지(hononga, "NLST") || 같은지(hononga, "MLSD")) {
        if (수행작업) { whakautu("450 Transfer in progress\r\n"); return; }
        if (ā_ringa_hononga < 0 && raraunga < 0) { whakautu("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { whakautu("550 Root listing only\r\n"); return; }
        tuku_Rārangi(같은지(hononga,"MLSD") ? 2 : 같은지(hononga,"LIST") ? 1 : 0); 수행작업 = 2;
        whakautu("150 Opening directory listing\r\n");
    }
    else if (같은지(hononga, "SIZE")) {
        if (!ara(부가인수)) { whakautu("550 Invalid filename\r\n"); return; }
        int kōnae_raweke = pk_open(kōnae_tāurunga_ingoa, pānui_anake_uara, 0); if (kōnae_raweke < 0) { whakautu("550 File unavailable\r\n"); return; }
        int rahi = pk_size(kōnae_raweke); pk_close(kōnae_raweke); char 응답자료[32] = "213 "; unsigned tuemi_COUNT = 4;
        수치(rahi, 응답자료, &tuemi_COUNT); 응답자료[tuemi_COUNT++] = '\r'; 응답자료[tuemi_COUNT++] = '\n'; 응답자료[tuemi_COUNT] = 0; whakautu(응답자료);
    } else if (같은지(hononga, "STOR") || 같은지(hononga, "RETR")) {
        if (수행작업) { whakautu("450 Transfer in progress\r\n"); return; }
        if (ā_ringa_hononga < 0 && raraunga < 0) { whakautu("425 Use PASV or EPSV\r\n"); return; }
        if (!ara(부가인수)) { whakautu("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(hononga, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(whakawhiti_ingoa, kōnae_tāurunga_ingoa, strlen(kōnae_tāurunga_ingoa) + 1);
        if (수행작업 == 2) {
            int kōnae_raweke = pk_open(kōnae_tāurunga_ingoa, pānui_anake_uara, 0);
            if (kōnae_raweke < 0) { 수행작업 = 0; whakautu("550 File unavailable\r\n"); return; }
            int tuemi_COUNT = pk_read(kōnae_raweke, whakawhiti_tūnga, sizeof(whakawhiti_tūnga)); pk_close(kōnae_raweke);
            if (tuemi_COUNT < 0) { 수행작업 = 0; whakautu("451 Read failed\r\n"); return; } 사용량 = tuemi_COUNT;
        }
        whakautu("150 Opening binary data connection\r\n");
    } else whakautu("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (mana >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); kati_whatunga(들어온연결); }
        else { mana = 들어온연결; Ngohe = 보드밀리초(); whakautu("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (mana < 0) return;
    if ((uint32_t)(보드밀리초() - Ngohe) > 60000) { momotu(); return; }
    if (!wehe_kaupapa) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char waehere_pūāhua; int 반환값 = 통신읽기(mana, &waehere_pūāhua, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { momotu(); return; } Ngohe = 보드밀리초();
        if (waehere_pūāhua == '\n') { if (줄오류) whakautu("500 Command too long or invalid\r\n"); else tono(); hononga_rahi = 줄오류 = 0; if (wehe_kaupapa) break; }
        else if (waehere_pūāhua != '\r') { if (!waehere_pūāhua || hononga_rahi >= sizeof(hononga) - 1) 줄오류 = 1; else hononga[hononga_rahi++] = waehere_pūāhua; }
    }
    if (ā_ringa_hononga >= 0 && raraunga < 0) {
        int 반환값 = 망연결받기(ā_ringa_hononga);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(mana)) kati_whatunga(반환값);
            else { raraunga = 반환값; kati_whatunga(ā_ringa_hononga); ā_ringa_hononga = -1; Ngohe = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && raraunga >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char raraunga_aukati[512]; int tuemi_COUNT = 통신읽기(raraunga, raraunga_aukati, sizeof(raraunga_aukati));
        if (tuemi_COUNT == -11) break;
        if (tuemi_COUNT < 0) { tāpu_whakawhiti(); whakautu("426 Data connection failed\r\n"); break; }
        Ngohe = 보드밀리초();
        if (tuemi_COUNT == 0) {
            int mēhua = -1;
            if (!실패여부) {
                int kōnae_raweke = pk_open(whakawhiti_ingoa, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (kōnae_raweke >= 0) { mēhua = pk_write(kōnae_raweke, whakawhiti_tūnga, 사용량); pk_close(kōnae_raweke); }
            }
            int 성공여부 = !실패여부 && mēhua == (int)사용량; tāpu_whakawhiti(); whakautu(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)tuemi_COUNT > sizeof(whakawhiti_tūnga) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(whakawhiti_tūnga + 사용량, raraunga_aukati, tuemi_COUNT); 사용량 += tuemi_COUNT; }
    }
    if (수행작업 == 2 && raraunga >= 0) {
        int tuemi_COUNT = 통신쓰기(raraunga, whakawhiti_tūnga + 보낸수, 사용량 - 보낸수);
        if (tuemi_COUNT >= 0) { 보낸수 += tuemi_COUNT; Ngohe = 보드밀리초(); if (보낸수 == 사용량) { tāpu_whakawhiti(); whakautu("226 Transfer complete\r\n"); } }
        else if (tuemi_COUNT != -11) { tāpu_whakawhiti(); whakautu("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < whakautu_rahi) {
        int tuemi_COUNT = 통신쓰기(mana, 응답모음 + 응답전송량, whakautu_rahi - 응답전송량);
        if (tuemi_COUNT > 0) 응답전송량 += tuemi_COUNT; else if (tuemi_COUNT != -11) { momotu(); return; }
    }
    if (응답전송량 == whakautu_rahi) { whakautu_rahi = 응답전송량 = 0; if (wehe_kaupapa) momotu(); }
}
