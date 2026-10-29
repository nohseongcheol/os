#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "xarxa_Pila.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int rebre_port = -1, control = -1, manual_connexió = -1, dades = -1;
static unsigned 로그인됨, usuari_D_acord, línia_canviar_la_mida, 줄오류, sortir_programa, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned resposta_canviar_la_mida, 응답전송량, Següent_número_de_port;
static uint32_t Activitat;
static char línia[256], 응답모음[2048], arxiu_introducció_nom[64], transferir_nom[64];
static unsigned char transferir_Estat[16384];
static int 같은지(const char *첫째값, const char *SEGON_VALOR) { while (*첫째값 && *첫째값 == *SEGON_VALOR) { 첫째값++; SEGON_VALOR++; } return *첫째값 == *SEGON_VALOR; }
static void resposta(const char *cadena_dades) {
    size_t element_COMPT = strlen(cadena_dades);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, resposta_canviar_la_mida - 응답전송량); resposta_canviar_la_mida -= 응답전송량; 응답전송량 = 0; }
    if (element_COMPT > sizeof(응답모음) - resposta_canviar_la_mida) { sortir_programa = 1; return; }
    memcpy(응답모음 + resposta_canviar_la_mida, cadena_dades, element_COMPT); resposta_canviar_la_mida += element_COMPT;
}
static void 수치(unsigned VALOR, char *mesura_dades, unsigned *element_COMPT) {
    char dígit_COMPT[10]; unsigned introducció_COMPT = 0;
    do { dígit_COMPT[introducció_COMPT++] = '0' + VALOR % 10; VALOR /= 10; } while (VALOR);
    while (introducció_COMPT) mesura_dades[(*element_COMPT)++] = dígit_COMPT[--introducció_COMPT];
}
static void aturar_transferir(void) {
    if (dades >= 0) Tanca_xarxa(dades); if (manual_connexió >= 0) Tanca_xarxa(manual_connexió);
    dades = manual_connexió = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void desconnectar(void) {
    aturar_transferir(); if (control >= 0) Tanca_xarxa(control); control = -1;
    로그인됨 = usuari_D_acord = línia_canviar_la_mida = 줄오류 = resposta_canviar_la_mida = 응답전송량 = sortir_programa = 0;
}
int transferència_de_fitxers_control(int Acció) {
    if (Acció == 2) return rebre_port >= 0;
    if (Acció == 0) { desconnectar(); if (rebre_port >= 0) Tanca_xarxa(rebre_port); rebre_port = -1; return 0; }
    if (Acció != 1) return -22; if (rebre_port >= 0) return 0;
    rebre_port = 통신끝점만들기(1); if (rebre_port < 0) return rebre_port;
    int 반환값 = 망주소묶기(rebre_port, tancar_xarxa_estat(0,0), 21); if (!반환값) 반환값 = 연결기다리기(rebre_port);
    if (반환값 < 0) { Tanca_xarxa(rebre_port); rebre_port = -1; } return 반환값;
}
static int Camí(const char *Nom) {
    unsigned element_COMPT = 0; if (*Nom == '/') Nom++;
    if (!*Nom || 같은지(Nom, ".") || 같은지(Nom, "..")) return 0;
    arxiu_introducció_nom[element_COMPT++] = '/';
    while (*Nom) {
        unsigned char codi_de_caràcter = *Nom++;
        if (element_COMPT >= 63 || codi_de_caràcter < 32 || codi_de_caràcter == 127 || codi_de_caràcter == '/' || codi_de_caràcter == '\\') return 0;
        arxiu_introducció_nom[element_COMPT++] = codi_de_caràcter;
    }
    arxiu_introducció_nom[element_COMPT] = 0; return 1;
}
static void enviar_Llista(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int element_COMPT = 자바파일항목길이(순번); if (element_COMPT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned introducció_COMPT = strlen(앞부분); memcpy(transferir_Estat + 사용량, 앞부분, introducció_COMPT); 사용량 += introducció_COMPT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)transferir_Estat, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        introducció_COMPT = strlen(뒷부분); memcpy(transferir_Estat + 사용량, 뒷부분, introducció_COMPT); 사용량 += introducció_COMPT;
        for (int 안쪽순번 = 0; 안쪽순번 < element_COMPT; 안쪽순번++) transferir_Estat[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        transferir_Estat[사용량++] = '\r'; transferir_Estat[사용량++] = '\n';
    }
}
static void Prepara_manual_connexió(int 확장여부) {
    if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
    aturar_transferir(); manual_connexió = 통신끝점만들기(1);
    if (manual_connexió >= 0) 통신주소재사용(manual_connexió);
    unsigned número_de_port = 50000 + Següent_número_de_port++ % 8;
    if (manual_connexió < 0 || 망주소묶기(manual_connexió, tancar_xarxa_estat(0,0), número_de_port) || 연결기다리기(manual_connexió)) {
        aturar_transferir(); resposta("425 Cannot open passive listener\r\n"); return;
    }
    char resposta_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned element_COMPT = strlen(앞부분); memcpy(resposta_1262b476, 앞부분, element_COMPT);
    if (확장여부) { 수치(número_de_port, resposta_1262b476, &element_COMPT); resposta_1262b476[element_COMPT++] = '|'; }
    else {
        uint32_t Adreça=tancar_xarxa_estat(0,0);
        for (int càrrec_INDEX=24;càrrec_INDEX>=0;càrrec_INDEX-=8) { 수치((Adreça>>càrrec_INDEX)&255,resposta_1262b476,&element_COMPT);resposta_1262b476[element_COMPT++]=','; }
        수치(número_de_port / 256, resposta_1262b476, &element_COMPT); resposta_1262b476[element_COMPT++] = ','; 수치(número_de_port % 256, resposta_1262b476, &element_COMPT);
    }
    resposta_1262b476[element_COMPT++] = ')'; resposta_1262b476[element_COMPT++] = '\r'; resposta_1262b476[element_COMPT++] = '\n'; resposta_1262b476[element_COMPT] = 0; resposta(resposta_1262b476);
}
static void Ordre(void) {
    línia[línia_canviar_la_mida] = 0;
    char *부가인수 = línia; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(línia, "QUIT")) { aturar_transferir(); resposta("221 Goodbye\r\n"); sortir_programa = 1; return; }
    if (같은지(línia, "NOOP")) { resposta("200 OK\r\n"); return; }
    if (같은지(línia, "SYST")) { resposta("215 UNIX Type: L8\r\n"); return; }
    if (같은지(línia, "FEAT")) { resposta("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(línia, "USER")) { 로그인됨 = 0; usuari_D_acord = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); resposta(usuari_D_acord ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(línia, "PASS")) { 로그인됨 = usuari_D_acord; resposta(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { resposta("530 Login first\r\n"); return; }
    if (같은지(línia, "PWD")) resposta("257 \"/\"\r\n");
    else if (같은지(línia, "CWD")) resposta(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(línia, "TYPE")) resposta(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(línia, "OPTS")) resposta(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(línia, "PASV")) Prepara_manual_connexió(0);
    else if (같은지(línia, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) resposta("522 IPv4 only\r\n"); else Prepara_manual_connexió(1); }
    else if (같은지(línia, "ABOR")) { aturar_transferir(); resposta("226 Transfer aborted\r\n"); }
    else if (같은지(línia, "DELE")) { resposta(Camí(부가인수) && pk_unlink(arxiu_introducció_nom) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(línia, "LIST") || 같은지(línia, "NLST") || 같은지(línia, "MLSD")) {
        if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
        if (manual_connexió < 0 && dades < 0) { resposta("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { resposta("550 Root listing only\r\n"); return; }
        enviar_Llista(같은지(línia,"MLSD") ? 2 : 같은지(línia,"LIST") ? 1 : 0); 수행작업 = 2;
        resposta("150 Opening directory listing\r\n");
    }
    else if (같은지(línia, "SIZE")) {
        if (!Camí(부가인수)) { resposta("550 Invalid filename\r\n"); return; }
        int arxiu_control_7f4cdfd5 = pk_open(arxiu_introducció_nom, només_de_lectura_VALOR, 0); if (arxiu_control_7f4cdfd5 < 0) { resposta("550 File unavailable\r\n"); return; }
        int Mida = pk_size(arxiu_control_7f4cdfd5); pk_close(arxiu_control_7f4cdfd5); char resposta_1262b476[32] = "213 "; unsigned element_COMPT = 4;
        수치(Mida, resposta_1262b476, &element_COMPT); resposta_1262b476[element_COMPT++] = '\r'; resposta_1262b476[element_COMPT++] = '\n'; resposta_1262b476[element_COMPT] = 0; resposta(resposta_1262b476);
    } else if (같은지(línia, "STOR") || 같은지(línia, "RETR")) {
        if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
        if (manual_connexió < 0 && dades < 0) { resposta("425 Use PASV or EPSV\r\n"); return; }
        if (!Camí(부가인수)) { resposta("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(línia, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(transferir_nom, arxiu_introducció_nom, strlen(arxiu_introducció_nom) + 1);
        if (수행작업 == 2) {
            int arxiu_control_7f4cdfd5 = pk_open(arxiu_introducció_nom, només_de_lectura_VALOR, 0);
            if (arxiu_control_7f4cdfd5 < 0) { 수행작업 = 0; resposta("550 File unavailable\r\n"); return; }
            int element_COMPT = pk_read(arxiu_control_7f4cdfd5, transferir_Estat, sizeof(transferir_Estat)); pk_close(arxiu_control_7f4cdfd5);
            if (element_COMPT < 0) { 수행작업 = 0; resposta("451 Read failed\r\n"); return; } 사용량 = element_COMPT;
        }
        resposta("150 Opening binary data connection\r\n");
    } else resposta("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (rebre_port < 0) return;
    int Entrant_connexió = 망연결받기(rebre_port);
    if (Entrant_connexió >= 0) {
        if (control >= 0) { 통신쓰기(Entrant_connexió, "421 One session at a time\r\n", 27); Tanca_xarxa(Entrant_connexió); }
        else { control = Entrant_connexió; Activitat = 보드밀리초(); resposta("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (control < 0) return;
    if ((uint32_t)(보드밀리초() - Activitat) > 60000) { desconnectar(); return; }
    if (!sortir_programa) for (unsigned pressupost_assignat = 0; pressupost_assignat < 256; pressupost_assignat++) {
        unsigned char codi_de_caràcter; int 반환값 = 통신읽기(control, &codi_de_caràcter, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { desconnectar(); return; } Activitat = 보드밀리초();
        if (codi_de_caràcter == '\n') { if (줄오류) resposta("500 Command too long or invalid\r\n"); else Ordre(); línia_canviar_la_mida = 줄오류 = 0; if (sortir_programa) break; }
        else if (codi_de_caràcter != '\r') { if (!codi_de_caràcter || línia_canviar_la_mida >= sizeof(línia) - 1) 줄오류 = 1; else línia[línia_canviar_la_mida++] = codi_de_caràcter; }
    }
    if (manual_connexió >= 0 && dades < 0) {
        int 반환값 = 망연결받기(manual_connexió);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(control)) Tanca_xarxa(반환값);
            else { dades = 반환값; Tanca_xarxa(manual_connexió); manual_connexió = -1; Activitat = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && dades >= 0) for (unsigned pressupost_assignat = 0; pressupost_assignat < 8; pressupost_assignat++) {
        unsigned char dades_bloquejar[512]; int element_COMPT = 통신읽기(dades, dades_bloquejar, sizeof(dades_bloquejar));
        if (element_COMPT == -11) break;
        if (element_COMPT < 0) { aturar_transferir(); resposta("426 Data connection failed\r\n"); break; }
        Activitat = 보드밀리초();
        if (element_COMPT == 0) {
            int RESULTAT = -1;
            if (!실패여부) {
                int arxiu_control_7f4cdfd5 = pk_open(transferir_nom, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (arxiu_control_7f4cdfd5 >= 0) { RESULTAT = pk_write(arxiu_control_7f4cdfd5, transferir_Estat, 사용량); pk_close(arxiu_control_7f4cdfd5); }
            }
            int 성공여부 = !실패여부 && RESULTAT == (int)사용량; aturar_transferir(); resposta(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)element_COMPT > sizeof(transferir_Estat) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(transferir_Estat + 사용량, dades_bloquejar, element_COMPT); 사용량 += element_COMPT; }
    }
    if (수행작업 == 2 && dades >= 0) {
        int element_COMPT = 통신쓰기(dades, transferir_Estat + 보낸수, 사용량 - 보낸수);
        if (element_COMPT >= 0) { 보낸수 += element_COMPT; Activitat = 보드밀리초(); if (보낸수 == 사용량) { aturar_transferir(); resposta("226 Transfer complete\r\n"); } }
        else if (element_COMPT != -11) { aturar_transferir(); resposta("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < resposta_canviar_la_mida) {
        int element_COMPT = 통신쓰기(control, 응답모음 + 응답전송량, resposta_canviar_la_mida - 응답전송량);
        if (element_COMPT > 0) 응답전송량 += element_COMPT; else if (element_COMPT != -11) { desconnectar(); return; }
    }
    if (응답전송량 == resposta_canviar_la_mida) { resposta_canviar_la_mida = 응답전송량 = 0; if (sortir_programa) desconnectar(); }
}
