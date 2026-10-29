#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Reseau_Stapel.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, Kontroll = -1, manuell_Verbindung = -1, Daten = -1;
static unsigned 로그인됨, Benotzer_OK, Zeil_d_Gréisst_veränneren, 줄오류, verloossen_App, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned äntweren_d_Gréisst_veränneren, 응답전송량, 다음접속번호;
static uint32_t Aktivitéit;
static char Zeil[256], 응답모음[2048], Fichier_Agab_Numm[64], Transfer_Numm[64];
static unsigned char Transfer_Status[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void äntweren(const char *Zeechefolleg_Daten) {
    size_t Element_COUNT = strlen(Zeechefolleg_Daten);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, äntweren_d_Gréisst_veränneren - 응답전송량); äntweren_d_Gréisst_veränneren -= 응답전송량; 응답전송량 = 0; }
    if (Element_COUNT > sizeof(응답모음) - äntweren_d_Gréisst_veränneren) { verloossen_App = 1; return; }
    memcpy(응답모음 + äntweren_d_Gréisst_veränneren, Zeechefolleg_Daten, Element_COUNT); äntweren_d_Gréisst_veränneren += Element_COUNT;
}
static void 수치(unsigned VALUE, char *Mooss_Daten, unsigned *Element_COUNT) {
    char Ziffer_COUNT[10]; unsigned Agab_COUNT = 0;
    do { Ziffer_COUNT[Agab_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (Agab_COUNT) Mooss_Daten[(*Element_COUNT)++] = Ziffer_COUNT[--Agab_COUNT];
}
static void Stoppen_Transfer(void) {
    if (Daten >= 0) Clôture_Reseau(Daten); if (manuell_Verbindung >= 0) Clôture_Reseau(manuell_Verbindung);
    Daten = manuell_Verbindung = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void deconnectéieren(void) {
    Stoppen_Transfer(); if (Kontroll >= 0) Clôture_Reseau(Kontroll); Kontroll = -1;
    로그인됨 = Benotzer_OK = Zeil_d_Gréisst_veränneren = 줄오류 = äntweren_d_Gréisst_veränneren = 응답전송량 = verloossen_App = 0;
}
int Fichier_Transfer_Kontroll(int Aktioun) {
    if (Aktioun == 2) return 수신창구 >= 0;
    if (Aktioun == 0) { deconnectéieren(); if (수신창구 >= 0) Clôture_Reseau(수신창구); 수신창구 = -1; return 0; }
    if (Aktioun != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { Clôture_Reseau(수신창구); 수신창구 = -1; } return 반환값;
}
static int Wee(const char *Numm) {
    unsigned Element_COUNT = 0; if (*Numm == '/') Numm++;
    if (!*Numm || 같은지(Numm, ".") || 같은지(Numm, "..")) return 0;
    Fichier_Agab_Numm[Element_COUNT++] = '/';
    while (*Numm) {
        unsigned char Zeechecode = *Numm++;
        if (Element_COUNT >= 63 || Zeechecode < 32 || Zeechecode == 127 || Zeechecode == '/' || Zeechecode == '\\') return 0;
        Fichier_Agab_Numm[Element_COUNT++] = Zeechecode;
    }
    Fichier_Agab_Numm[Element_COUNT] = 0; return 1;
}
static void mailen_Lëscht(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int Element_COUNT = 자바파일항목길이(순번); if (Element_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned Agab_COUNT = strlen(앞부분); memcpy(Transfer_Status + 사용량, 앞부분, Agab_COUNT); 사용량 += Agab_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Transfer_Status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        Agab_COUNT = strlen(뒷부분); memcpy(Transfer_Status + 사용량, 뒷부분, Agab_COUNT); 사용량 += Agab_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < Element_COUNT; 안쪽순번++) Transfer_Status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Transfer_Status[사용량++] = '\r'; Transfer_Status[사용량++] = '\n';
    }
}
static void Préparéieren_manuell_Verbindung(int 확장여부) {
    if (수행작업) { äntweren("450 Transfer in progress\r\n"); return; }
    Stoppen_Transfer(); manuell_Verbindung = 통신끝점만들기(1);
    if (manuell_Verbindung >= 0) 통신주소재사용(manuell_Verbindung);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (manuell_Verbindung < 0 || 망주소묶기(manuell_Verbindung, 망상태읽기(0,0), 접속번호) || 연결기다리기(manuell_Verbindung)) {
        Stoppen_Transfer(); äntweren("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned Element_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, Element_COUNT);
    if (확장여부) { 수치(접속번호, 응답자료, &Element_COUNT); 응답자료[Element_COUNT++] = '|'; }
    else {
        uint32_t Adress=망상태읽기(0,0);
        for (int positionéieren_INDEX=24;positionéieren_INDEX>=0;positionéieren_INDEX-=8) { 수치((Adress>>positionéieren_INDEX)&255,응답자료,&Element_COUNT);응답자료[Element_COUNT++]=','; }
        수치(접속번호 / 256, 응답자료, &Element_COUNT); 응답자료[Element_COUNT++] = ','; 수치(접속번호 % 256, 응답자료, &Element_COUNT);
    }
    응답자료[Element_COUNT++] = ')'; 응답자료[Element_COUNT++] = '\r'; 응답자료[Element_COUNT++] = '\n'; 응답자료[Element_COUNT] = 0; äntweren(응답자료);
}
static void Befeel(void) {
    Zeil[Zeil_d_Gréisst_veränneren] = 0;
    char *부가인수 = Zeil; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Zeil, "QUIT")) { Stoppen_Transfer(); äntweren("221 Goodbye\r\n"); verloossen_App = 1; return; }
    if (같은지(Zeil, "NOOP")) { äntweren("200 OK\r\n"); return; }
    if (같은지(Zeil, "SYST")) { äntweren("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Zeil, "FEAT")) { äntweren("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Zeil, "USER")) { 로그인됨 = 0; Benotzer_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); äntweren(Benotzer_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Zeil, "PASS")) { 로그인됨 = Benotzer_OK; äntweren(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { äntweren("530 Login first\r\n"); return; }
    if (같은지(Zeil, "PWD")) äntweren("257 \"/\"\r\n");
    else if (같은지(Zeil, "CWD")) äntweren(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Zeil, "TYPE")) äntweren(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Zeil, "OPTS")) äntweren(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Zeil, "PASV")) Préparéieren_manuell_Verbindung(0);
    else if (같은지(Zeil, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) äntweren("522 IPv4 only\r\n"); else Préparéieren_manuell_Verbindung(1); }
    else if (같은지(Zeil, "ABOR")) { Stoppen_Transfer(); äntweren("226 Transfer aborted\r\n"); }
    else if (같은지(Zeil, "DELE")) { äntweren(Wee(부가인수) && pk_unlink(Fichier_Agab_Numm) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Zeil, "LIST") || 같은지(Zeil, "NLST") || 같은지(Zeil, "MLSD")) {
        if (수행작업) { äntweren("450 Transfer in progress\r\n"); return; }
        if (manuell_Verbindung < 0 && Daten < 0) { äntweren("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { äntweren("550 Root listing only\r\n"); return; }
        mailen_Lëscht(같은지(Zeil,"MLSD") ? 2 : 같은지(Zeil,"LIST") ? 1 : 0); 수행작업 = 2;
        äntweren("150 Opening directory listing\r\n");
    }
    else if (같은지(Zeil, "SIZE")) {
        if (!Wee(부가인수)) { äntweren("550 Invalid filename\r\n"); return; }
        int Fichier_Handle = pk_open(Fichier_Agab_Numm, schreifgeschützt_VALUE, 0); if (Fichier_Handle < 0) { äntweren("550 File unavailable\r\n"); return; }
        int d_Gréisst_veränneren = pk_size(Fichier_Handle); pk_close(Fichier_Handle); char 응답자료[32] = "213 "; unsigned Element_COUNT = 4;
        수치(d_Gréisst_veränneren, 응답자료, &Element_COUNT); 응답자료[Element_COUNT++] = '\r'; 응답자료[Element_COUNT++] = '\n'; 응답자료[Element_COUNT] = 0; äntweren(응답자료);
    } else if (같은지(Zeil, "STOR") || 같은지(Zeil, "RETR")) {
        if (수행작업) { äntweren("450 Transfer in progress\r\n"); return; }
        if (manuell_Verbindung < 0 && Daten < 0) { äntweren("425 Use PASV or EPSV\r\n"); return; }
        if (!Wee(부가인수)) { äntweren("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Zeil, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Transfer_Numm, Fichier_Agab_Numm, strlen(Fichier_Agab_Numm) + 1);
        if (수행작업 == 2) {
            int Fichier_Handle = pk_open(Fichier_Agab_Numm, schreifgeschützt_VALUE, 0);
            if (Fichier_Handle < 0) { 수행작업 = 0; äntweren("550 File unavailable\r\n"); return; }
            int Element_COUNT = pk_read(Fichier_Handle, Transfer_Status, sizeof(Transfer_Status)); pk_close(Fichier_Handle);
            if (Element_COUNT < 0) { 수행작업 = 0; äntweren("451 Read failed\r\n"); return; } 사용량 = Element_COUNT;
        }
        äntweren("150 Opening binary data connection\r\n");
    } else äntweren("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int 들어온연결 = 망연결받기(수신창구);
    if (들어온연결 >= 0) {
        if (Kontroll >= 0) { 통신쓰기(들어온연결, "421 One session at a time\r\n", 27); Clôture_Reseau(들어온연결); }
        else { Kontroll = 들어온연결; Aktivitéit = 보드밀리초(); äntweren("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (Kontroll < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivitéit) > 60000) { deconnectéieren(); return; }
    if (!verloossen_App) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char Zeechecode; int 반환값 = 통신읽기(Kontroll, &Zeechecode, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { deconnectéieren(); return; } Aktivitéit = 보드밀리초();
        if (Zeechecode == '\n') { if (줄오류) äntweren("500 Command too long or invalid\r\n"); else Befeel(); Zeil_d_Gréisst_veränneren = 줄오류 = 0; if (verloossen_App) break; }
        else if (Zeechecode != '\r') { if (!Zeechecode || Zeil_d_Gréisst_veränneren >= sizeof(Zeil) - 1) 줄오류 = 1; else Zeil[Zeil_d_Gréisst_veränneren++] = Zeechecode; }
    }
    if (manuell_Verbindung >= 0 && Daten < 0) {
        int 반환값 = 망연결받기(manuell_Verbindung);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(Kontroll)) Clôture_Reseau(반환값);
            else { Daten = 반환값; Clôture_Reseau(manuell_Verbindung); manuell_Verbindung = -1; Aktivitéit = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && Daten >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char Daten_blockéieren[512]; int Element_COUNT = 통신읽기(Daten, Daten_blockéieren, sizeof(Daten_blockéieren));
        if (Element_COUNT == -11) break;
        if (Element_COUNT < 0) { Stoppen_Transfer(); äntweren("426 Data connection failed\r\n"); break; }
        Aktivitéit = 보드밀리초();
        if (Element_COUNT == 0) {
            int Mooss = -1;
            if (!실패여부) {
                int Fichier_Handle = pk_open(Transfer_Numm, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (Fichier_Handle >= 0) { Mooss = pk_write(Fichier_Handle, Transfer_Status, 사용량); pk_close(Fichier_Handle); }
            }
            int 성공여부 = !실패여부 && Mooss == (int)사용량; Stoppen_Transfer(); äntweren(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)Element_COUNT > sizeof(Transfer_Status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Transfer_Status + 사용량, Daten_blockéieren, Element_COUNT); 사용량 += Element_COUNT; }
    }
    if (수행작업 == 2 && Daten >= 0) {
        int Element_COUNT = 통신쓰기(Daten, Transfer_Status + 보낸수, 사용량 - 보낸수);
        if (Element_COUNT >= 0) { 보낸수 += Element_COUNT; Aktivitéit = 보드밀리초(); if (보낸수 == 사용량) { Stoppen_Transfer(); äntweren("226 Transfer complete\r\n"); } }
        else if (Element_COUNT != -11) { Stoppen_Transfer(); äntweren("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < äntweren_d_Gréisst_veränneren) {
        int Element_COUNT = 통신쓰기(Kontroll, 응답모음 + 응답전송량, äntweren_d_Gréisst_veränneren - 응답전송량);
        if (Element_COUNT > 0) 응답전송량 += Element_COUNT; else if (Element_COUNT != -11) { deconnectéieren(); return; }
    }
    if (응답전송량 == äntweren_d_Gréisst_veränneren) { äntweren_d_Gréisst_veränneren = 응답전송량 = 0; if (verloossen_App) deconnectéieren(); }
}
