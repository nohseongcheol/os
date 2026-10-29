#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "rete_Pila.h"
#include "string.h"
#include "File_ABI.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int porta_di_ricezione = -1, controllo = -1, manuale_connessione = -1, dati = -1;
static unsigned 로그인됨, USER_OK, riga_ridimensionare, 줄오류, esci_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned replica_ridimensionare, 응답전송량, Avanti_numero_di_porta;
static uint32_t Azioni;
static char riga_di_ingresso[256], 응답모음[2048], File_voce_nome[64], trasferire_nome[64];
static unsigned char trasferire_Stato[16384];
static int 같은지(const char *첫째값, const char *SECONDO_VALORE) { while (*첫째값 && *첫째값 == *SECONDO_VALORE) { 첫째값++; SECONDO_VALORE++; } return *첫째값 == *SECONDO_VALORE; }
static void replica(const char *stringa_dati) {
    size_t articolo_CONTA_NUMERI = strlen(stringa_dati);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, replica_ridimensionare - 응답전송량); replica_ridimensionare -= 응답전송량; 응답전송량 = 0; }
    if (articolo_CONTA_NUMERI > sizeof(응답모음) - replica_ridimensionare) { esci_app = 1; return; }
    memcpy(응답모음 + replica_ridimensionare, stringa_dati, articolo_CONTA_NUMERI); replica_ridimensionare += articolo_CONTA_NUMERI;
}
static void 수치(unsigned VALORE, char *KR_dati, unsigned *articolo_CONTA_NUMERI) {
    char cifra_CONTA_NUMERI[10]; unsigned voce_CONTA_NUMERI = 0;
    do { cifra_CONTA_NUMERI[voce_CONTA_NUMERI++] = '0' + VALORE % 10; VALORE /= 10; } while (VALORE);
    while (voce_CONTA_NUMERI) KR_dati[(*articolo_CONTA_NUMERI)++] = cifra_CONTA_NUMERI[--voce_CONTA_NUMERI];
}
static void Stop_trasferire(void) {
    if (dati >= 0) Chiudi_rete(dati); if (manuale_connessione >= 0) Chiudi_rete(manuale_connessione);
    dati = manuale_connessione = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void scollegare(void) {
    Stop_trasferire(); if (controllo >= 0) Chiudi_rete(controllo); controllo = -1;
    로그인됨 = USER_OK = riga_ridimensionare = 줄오류 = replica_ridimensionare = 응답전송량 = esci_app = 0;
}
int trasferimento_di_file_controllo(int Azione) {
    if (Azione == 2) return porta_di_ricezione >= 0;
    if (Azione == 0) { scollegare(); if (porta_di_ricezione >= 0) Chiudi_rete(porta_di_ricezione); porta_di_ricezione = -1; return 0; }
    if (Azione != 1) return -22; if (porta_di_ricezione >= 0) return 0;
    porta_di_ricezione = Crea_socket_endpoint(1); if (porta_di_ricezione < 0) return porta_di_ricezione;
    int 반환값 = NET_BIND(porta_di_ricezione, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_essere_in_ascolto(porta_di_ricezione);
    if (반환값 < 0) { Chiudi_rete(porta_di_ricezione); porta_di_ricezione = -1; } return 반환값;
}
static int percorso(const char *Nome) {
    unsigned articolo_CONTA_NUMERI = 0; if (*Nome == '/') Nome++;
    if (!*Nome || 같은지(Nome, ".") || 같은지(Nome, "..")) return 0;
    File_voce_nome[articolo_CONTA_NUMERI++] = '/';
    while (*Nome) {
        unsigned char punto_di_codice = *Nome++;
        if (articolo_CONTA_NUMERI >= 63 || punto_di_codice < 32 || punto_di_codice == 127 || punto_di_codice == '/' || punto_di_codice == '\\') return 0;
        File_voce_nome[articolo_CONTA_NUMERI++] = punto_di_codice;
    }
    File_voce_nome[articolo_CONTA_NUMERI] = 0; return 1;
}
static void inviare_elenco(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int articolo_CONTA_NUMERI = 자바파일항목길이(순번); if (articolo_CONTA_NUMERI <= 0) continue;
        const char *interlinea_parte = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned voce_CONTA_NUMERI = strlen(interlinea_parte); memcpy(trasferire_Stato + 사용량, interlinea_parte, voce_CONTA_NUMERI); 사용량 += voce_CONTA_NUMERI;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)trasferire_Stato, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        voce_CONTA_NUMERI = strlen(뒷부분); memcpy(trasferire_Stato + 사용량, 뒷부분, voce_CONTA_NUMERI); 사용량 += voce_CONTA_NUMERI;
        for (int 안쪽순번 = 0; 안쪽순번 < articolo_CONTA_NUMERI; 안쪽순번++) trasferire_Stato[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        trasferire_Stato[사용량++] = '\r'; trasferire_Stato[사용량++] = '\n';
    }
}
static void Prepara_manuale_connessione(int 확장여부) {
    if (수행작업) { replica("450 Transfer in progress\r\n"); return; }
    Stop_trasferire(); manuale_connessione = Crea_socket_endpoint(1);
    if (manuale_connessione >= 0) 통신주소재사용(manuale_connessione);
    unsigned numero_di_porta = 50000 + Avanti_numero_di_porta++ % 8;
    if (manuale_connessione < 0 || NET_BIND(manuale_connessione, 망상태읽기(0,0), numero_di_porta) || NET_essere_in_ascolto(manuale_connessione)) {
        Stop_trasferire(); replica("425 Cannot open passive listener\r\n"); return;
    }
    char risposta[96]; const char *interlinea_parte = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned articolo_CONTA_NUMERI = strlen(interlinea_parte); memcpy(risposta, interlinea_parte, articolo_CONTA_NUMERI);
    if (확장여부) { 수치(numero_di_porta, risposta, &articolo_CONTA_NUMERI); risposta[articolo_CONTA_NUMERI++] = '|'; }
    else {
        uint32_t e_mail=망상태읽기(0,0);
        for (int funzione_INDICE=24;funzione_INDICE>=0;funzione_INDICE-=8) { 수치((e_mail>>funzione_INDICE)&255,risposta,&articolo_CONTA_NUMERI);risposta[articolo_CONTA_NUMERI++]=','; }
        수치(numero_di_porta / 256, risposta, &articolo_CONTA_NUMERI); risposta[articolo_CONTA_NUMERI++] = ','; 수치(numero_di_porta % 256, risposta, &articolo_CONTA_NUMERI);
    }
    risposta[articolo_CONTA_NUMERI++] = ')'; risposta[articolo_CONTA_NUMERI++] = '\r'; risposta[articolo_CONTA_NUMERI++] = '\n'; risposta[articolo_CONTA_NUMERI] = 0; replica(risposta);
}
static void comando(void) {
    riga_di_ingresso[riga_ridimensionare] = 0;
    char *부가인수 = riga_di_ingresso; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(riga_di_ingresso, "QUIT")) { Stop_trasferire(); replica("221 Goodbye\r\n"); esci_app = 1; return; }
    if (같은지(riga_di_ingresso, "NOOP")) { replica("200 OK\r\n"); return; }
    if (같은지(riga_di_ingresso, "SYST")) { replica("215 UNIX Type: L8\r\n"); return; }
    if (같은지(riga_di_ingresso, "FEAT")) { replica("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(riga_di_ingresso, "USER")) { 로그인됨 = 0; USER_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); replica(USER_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(riga_di_ingresso, "PASS")) { 로그인됨 = USER_OK; replica(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { replica("530 Login first\r\n"); return; }
    if (같은지(riga_di_ingresso, "PWD")) replica("257 \"/\"\r\n");
    else if (같은지(riga_di_ingresso, "CWD")) replica(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(riga_di_ingresso, "TYPE")) replica(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(riga_di_ingresso, "OPTS")) replica(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(riga_di_ingresso, "PASV")) Prepara_manuale_connessione(0);
    else if (같은지(riga_di_ingresso, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) replica("522 IPv4 only\r\n"); else Prepara_manuale_connessione(1); }
    else if (같은지(riga_di_ingresso, "ABOR")) { Stop_trasferire(); replica("226 Transfer aborted\r\n"); }
    else if (같은지(riga_di_ingresso, "DELE")) { replica(percorso(부가인수) && pk_unlink(File_voce_nome) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(riga_di_ingresso, "LIST") || 같은지(riga_di_ingresso, "NLST") || 같은지(riga_di_ingresso, "MLSD")) {
        if (수행작업) { replica("450 Transfer in progress\r\n"); return; }
        if (manuale_connessione < 0 && dati < 0) { replica("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { replica("550 Root listing only\r\n"); return; }
        inviare_elenco(같은지(riga_di_ingresso,"MLSD") ? 2 : 같은지(riga_di_ingresso,"LIST") ? 1 : 0); 수행작업 = 2;
        replica("150 Opening directory listing\r\n");
    }
    else if (같은지(riga_di_ingresso, "SIZE")) {
        if (!percorso(부가인수)) { replica("550 Invalid filename\r\n"); return; }
        int handle_di_file = pk_open(File_voce_nome, di_sola_lettura_VALORE, 0); if (handle_di_file < 0) { replica("550 File unavailable\r\n"); return; }
        int Dimensione = pk_size(handle_di_file); pk_close(handle_di_file); char risposta[32] = "213 "; unsigned articolo_CONTA_NUMERI = 4;
        수치(Dimensione, risposta, &articolo_CONTA_NUMERI); risposta[articolo_CONTA_NUMERI++] = '\r'; risposta[articolo_CONTA_NUMERI++] = '\n'; risposta[articolo_CONTA_NUMERI] = 0; replica(risposta);
    } else if (같은지(riga_di_ingresso, "STOR") || 같은지(riga_di_ingresso, "RETR")) {
        if (수행작업) { replica("450 Transfer in progress\r\n"); return; }
        if (manuale_connessione < 0 && dati < 0) { replica("425 Use PASV or EPSV\r\n"); return; }
        if (!percorso(부가인수)) { replica("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(riga_di_ingresso, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(trasferire_nome, File_voce_nome, strlen(File_voce_nome) + 1);
        if (수행작업 == 2) {
            int handle_di_file = pk_open(File_voce_nome, di_sola_lettura_VALORE, 0);
            if (handle_di_file < 0) { 수행작업 = 0; replica("550 File unavailable\r\n"); return; }
            int articolo_CONTA_NUMERI = pk_read(handle_di_file, trasferire_Stato, sizeof(trasferire_Stato)); pk_close(handle_di_file);
            if (articolo_CONTA_NUMERI < 0) { 수행작업 = 0; replica("451 Read failed\r\n"); return; } 사용량 = articolo_CONTA_NUMERI;
        }
        replica("150 Opening binary data connection\r\n");
    } else replica("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (porta_di_ricezione < 0) return;
    int Ricevuta_connessione = NET_accettare(porta_di_ricezione);
    if (Ricevuta_connessione >= 0) {
        if (controllo >= 0) { NET_scrivere(Ricevuta_connessione, "421 One session at a time\r\n", 27); Chiudi_rete(Ricevuta_connessione); }
        else { controllo = Ricevuta_connessione; Azioni = 보드밀리초(); replica("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (controllo < 0) return;
    if ((uint32_t)(보드밀리초() - Azioni) > 60000) { scollegare(); return; }
    if (!esci_app) for (unsigned budget = 0; budget < 256; budget++) {
        unsigned char punto_di_codice; int 반환값 = 통신읽기(controllo, &punto_di_codice, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { scollegare(); return; } Azioni = 보드밀리초();
        if (punto_di_codice == '\n') { if (줄오류) replica("500 Command too long or invalid\r\n"); else comando(); riga_ridimensionare = 줄오류 = 0; if (esci_app) break; }
        else if (punto_di_codice != '\r') { if (!punto_di_codice || riga_ridimensionare >= sizeof(riga_di_ingresso) - 1) 줄오류 = 1; else riga_di_ingresso[riga_ridimensionare++] = punto_di_codice; }
    }
    if (manuale_connessione >= 0 && dati < 0) {
        int 반환값 = NET_accettare(manuale_connessione);
        if (반환값 >= 0) {
            if (NET_peer_e_mail(반환값) != NET_peer_e_mail(controllo)) Chiudi_rete(반환값);
            else { dati = 반환값; Chiudi_rete(manuale_connessione); manuale_connessione = -1; Azioni = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && dati >= 0) for (unsigned budget = 0; budget < 8; budget++) {
        unsigned char blocco_di_dati[512]; int articolo_CONTA_NUMERI = 통신읽기(dati, blocco_di_dati, sizeof(blocco_di_dati));
        if (articolo_CONTA_NUMERI == -11) break;
        if (articolo_CONTA_NUMERI < 0) { Stop_trasferire(); replica("426 Data connection failed\r\n"); break; }
        Azioni = 보드밀리초();
        if (articolo_CONTA_NUMERI == 0) {
            int risultato = -1;
            if (!실패여부) {
                int handle_di_file = pk_open(trasferire_nome, sola_scrittura_VALORE | 없으면만들기 | tagliare_Sommario, 0600);
                if (handle_di_file >= 0) { risultato = pk_write(handle_di_file, trasferire_Stato, 사용량); pk_close(handle_di_file); }
            }
            int 성공여부 = !실패여부 && risultato == (int)사용량; Stop_trasferire(); replica(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)articolo_CONTA_NUMERI > sizeof(trasferire_Stato) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(trasferire_Stato + 사용량, blocco_di_dati, articolo_CONTA_NUMERI); 사용량 += articolo_CONTA_NUMERI; }
    }
    if (수행작업 == 2 && dati >= 0) {
        int articolo_CONTA_NUMERI = NET_scrivere(dati, trasferire_Stato + 보낸수, 사용량 - 보낸수);
        if (articolo_CONTA_NUMERI >= 0) { 보낸수 += articolo_CONTA_NUMERI; Azioni = 보드밀리초(); if (보낸수 == 사용량) { Stop_trasferire(); replica("226 Transfer complete\r\n"); } }
        else if (articolo_CONTA_NUMERI != -11) { Stop_trasferire(); replica("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < replica_ridimensionare) {
        int articolo_CONTA_NUMERI = NET_scrivere(controllo, 응답모음 + 응답전송량, replica_ridimensionare - 응답전송량);
        if (articolo_CONTA_NUMERI > 0) 응답전송량 += articolo_CONTA_NUMERI; else if (articolo_CONTA_NUMERI != -11) { scollegare(); return; }
    }
    if (응답전송량 == replica_ridimensionare) { replica_ridimensionare = 응답전송량 = 0; if (esci_app) scollegare(); }
}
