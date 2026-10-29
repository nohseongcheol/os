#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "net_stack.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int ontvangen_poort = -1, controle = -1, handmatig_verbinding = -1, gegevens = -1;
static unsigned 로그인됨, gebruiker_OK, lijn_formaat_wijzigen, 줄오류, sluiten_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned reactie_formaat_wijzigen, 응답전송량, Volgende_poortnummer;
static uint32_t Activiteit;
static char invoerregel[256], 응답모음[2048], Bestand_invoer_naam[64], transfer_naam[64];
static unsigned char transfer_Status[16384];
static int 같은지(const char *첫째값, const char *SECONDE_WAARDE) { while (*첫째값 && *첫째값 == *SECONDE_WAARDE) { 첫째값++; SECONDE_WAARDE++; } return *첫째값 == *SECONDE_WAARDE; }
static void reactie(const char *tekenreeks_gegevens) {
    size_t item_AANTAL = strlen(tekenreeks_gegevens);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, reactie_formaat_wijzigen - 응답전송량); reactie_formaat_wijzigen -= 응답전송량; 응답전송량 = 0; }
    if (item_AANTAL > sizeof(응답모음) - reactie_formaat_wijzigen) { sluiten_app = 1; return; }
    memcpy(응답모음 + reactie_formaat_wijzigen, tekenreeks_gegevens, item_AANTAL); reactie_formaat_wijzigen += item_AANTAL;
}
static void 수치(unsigned WAARDE, char *HR_gegevens, unsigned *item_AANTAL) {
    char cijfer_AANTAL[10]; unsigned invoer_AANTAL_8f7753a1 = 0;
    do { cijfer_AANTAL[invoer_AANTAL_8f7753a1++] = '0' + WAARDE % 10; WAARDE /= 10; } while (WAARDE);
    while (invoer_AANTAL_8f7753a1) HR_gegevens[(*item_AANTAL)++] = cijfer_AANTAL[--invoer_AANTAL_8f7753a1];
}
static void Stop_transfer(void) {
    if (gegevens >= 0) Sluiten_net(gegevens); if (handmatig_verbinding >= 0) Sluiten_net(handmatig_verbinding);
    gegevens = handmatig_verbinding = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void verbinding_verbreken(void) {
    Stop_transfer(); if (controle >= 0) Sluiten_net(controle); controle = -1;
    로그인됨 = gebruiker_OK = lijn_formaat_wijzigen = 줄오류 = reactie_formaat_wijzigen = 응답전송량 = sluiten_app = 0;
}
int bestandsoverdracht_controle(int Actie) {
    if (Actie == 2) return ontvangen_poort >= 0;
    if (Actie == 0) { verbinding_verbreken(); if (ontvangen_poort >= 0) Sluiten_net(ontvangen_poort); ontvangen_poort = -1; return 0; }
    if (Actie != 1) return -22; if (ontvangen_poort >= 0) return 0;
    ontvangen_poort = maken_socket_eindpunt(1); if (ontvangen_poort < 0) return ontvangen_poort;
    int 반환값 = NET_BIND(ontvangen_poort, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(ontvangen_poort);
    if (반환값 < 0) { Sluiten_net(ontvangen_poort); ontvangen_poort = -1; } return 반환값;
}
static int pad(const char *Naam) {
    unsigned item_AANTAL = 0; if (*Naam == '/') Naam++;
    if (!*Naam || 같은지(Naam, ".") || 같은지(Naam, "..")) return 0;
    Bestand_invoer_naam[item_AANTAL++] = '/';
    while (*Naam) {
        unsigned char codepoint = *Naam++;
        if (item_AANTAL >= 63 || codepoint < 32 || codepoint == 127 || codepoint == '/' || codepoint == '\\') return 0;
        Bestand_invoer_naam[item_AANTAL++] = codepoint;
    }
    Bestand_invoer_naam[item_AANTAL] = 0; return 1;
}
static void e_mailen_Lijst(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int item_AANTAL = 자바파일항목길이(순번); if (item_AANTAL <= 0) continue;
        const char *interlinie_tegel = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned invoer_AANTAL_8f7753a1 = strlen(interlinie_tegel); memcpy(transfer_Status + 사용량, interlinie_tegel, invoer_AANTAL_8f7753a1); 사용량 += invoer_AANTAL_8f7753a1;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)transfer_Status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        invoer_AANTAL_8f7753a1 = strlen(뒷부분); memcpy(transfer_Status + 사용량, 뒷부분, invoer_AANTAL_8f7753a1); 사용량 += invoer_AANTAL_8f7753a1;
        for (int 안쪽순번 = 0; 안쪽순번 < item_AANTAL; 안쪽순번++) transfer_Status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        transfer_Status[사용량++] = '\r'; transfer_Status[사용량++] = '\n';
    }
}
static void Bereid_voor_handmatig_verbinding(int 확장여부) {
    if (수행작업) { reactie("450 Transfer in progress\r\n"); return; }
    Stop_transfer(); handmatig_verbinding = maken_socket_eindpunt(1);
    if (handmatig_verbinding >= 0) 통신주소재사용(handmatig_verbinding);
    unsigned poortnummer = 50000 + Volgende_poortnummer++ % 8;
    if (handmatig_verbinding < 0 || NET_BIND(handmatig_verbinding, 망상태읽기(0,0), poortnummer) || 연결기다리기(handmatig_verbinding)) {
        Stop_transfer(); reactie("425 Cannot open passive listener\r\n"); return;
    }
    char reactie_1262b476[96]; const char *interlinie_tegel = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned item_AANTAL = strlen(interlinie_tegel); memcpy(reactie_1262b476, interlinie_tegel, item_AANTAL);
    if (확장여부) { 수치(poortnummer, reactie_1262b476, &item_AANTAL); reactie_1262b476[item_AANTAL++] = '|'; }
    else {
        uint32_t ADRES=망상태읽기(0,0);
        for (int plaatsingsindex=24;plaatsingsindex>=0;plaatsingsindex-=8) { 수치((ADRES>>plaatsingsindex)&255,reactie_1262b476,&item_AANTAL);reactie_1262b476[item_AANTAL++]=','; }
        수치(poortnummer / 256, reactie_1262b476, &item_AANTAL); reactie_1262b476[item_AANTAL++] = ','; 수치(poortnummer % 256, reactie_1262b476, &item_AANTAL);
    }
    reactie_1262b476[item_AANTAL++] = ')'; reactie_1262b476[item_AANTAL++] = '\r'; reactie_1262b476[item_AANTAL++] = '\n'; reactie_1262b476[item_AANTAL] = 0; reactie(reactie_1262b476);
}
static void opdracht(void) {
    invoerregel[lijn_formaat_wijzigen] = 0;
    char *부가인수 = invoerregel; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(invoerregel, "QUIT")) { Stop_transfer(); reactie("221 Goodbye\r\n"); sluiten_app = 1; return; }
    if (같은지(invoerregel, "NOOP")) { reactie("200 OK\r\n"); return; }
    if (같은지(invoerregel, "SYST")) { reactie("215 UNIX Type: L8\r\n"); return; }
    if (같은지(invoerregel, "FEAT")) { reactie("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(invoerregel, "USER")) { 로그인됨 = 0; gebruiker_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); reactie(gebruiker_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(invoerregel, "PASS")) { 로그인됨 = gebruiker_OK; reactie(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { reactie("530 Login first\r\n"); return; }
    if (같은지(invoerregel, "PWD")) reactie("257 \"/\"\r\n");
    else if (같은지(invoerregel, "CWD")) reactie(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(invoerregel, "TYPE")) reactie(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(invoerregel, "OPTS")) reactie(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(invoerregel, "PASV")) Bereid_voor_handmatig_verbinding(0);
    else if (같은지(invoerregel, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) reactie("522 IPv4 only\r\n"); else Bereid_voor_handmatig_verbinding(1); }
    else if (같은지(invoerregel, "ABOR")) { Stop_transfer(); reactie("226 Transfer aborted\r\n"); }
    else if (같은지(invoerregel, "DELE")) { reactie(pad(부가인수) && pk_unlink(Bestand_invoer_naam) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(invoerregel, "LIST") || 같은지(invoerregel, "NLST") || 같은지(invoerregel, "MLSD")) {
        if (수행작업) { reactie("450 Transfer in progress\r\n"); return; }
        if (handmatig_verbinding < 0 && gegevens < 0) { reactie("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { reactie("550 Root listing only\r\n"); return; }
        e_mailen_Lijst(같은지(invoerregel,"MLSD") ? 2 : 같은지(invoerregel,"LIST") ? 1 : 0); 수행작업 = 2;
        reactie("150 Opening directory listing\r\n");
    }
    else if (같은지(invoerregel, "SIZE")) {
        if (!pad(부가인수)) { reactie("550 Invalid filename\r\n"); return; }
        int bestandsingang = pk_open(Bestand_invoer_naam, alleen_lezen_WAARDE, 0); if (bestandsingang < 0) { reactie("550 File unavailable\r\n"); return; }
        int Grootte = pk_size(bestandsingang); pk_close(bestandsingang); char reactie_1262b476[32] = "213 "; unsigned item_AANTAL = 4;
        수치(Grootte, reactie_1262b476, &item_AANTAL); reactie_1262b476[item_AANTAL++] = '\r'; reactie_1262b476[item_AANTAL++] = '\n'; reactie_1262b476[item_AANTAL] = 0; reactie(reactie_1262b476);
    } else if (같은지(invoerregel, "STOR") || 같은지(invoerregel, "RETR")) {
        if (수행작업) { reactie("450 Transfer in progress\r\n"); return; }
        if (handmatig_verbinding < 0 && gegevens < 0) { reactie("425 Use PASV or EPSV\r\n"); return; }
        if (!pad(부가인수)) { reactie("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(invoerregel, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(transfer_naam, Bestand_invoer_naam, strlen(Bestand_invoer_naam) + 1);
        if (수행작업 == 2) {
            int bestandsingang = pk_open(Bestand_invoer_naam, alleen_lezen_WAARDE, 0);
            if (bestandsingang < 0) { 수행작업 = 0; reactie("550 File unavailable\r\n"); return; }
            int item_AANTAL = pk_read(bestandsingang, transfer_Status, sizeof(transfer_Status)); pk_close(bestandsingang);
            if (item_AANTAL < 0) { 수행작업 = 0; reactie("451 Read failed\r\n"); return; } 사용량 = item_AANTAL;
        }
        reactie("150 Opening binary data connection\r\n");
    } else reactie("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (ontvangen_poort < 0) return;
    int Inkomend_verbinding = NET_accepteren(ontvangen_poort);
    if (Inkomend_verbinding >= 0) {
        if (controle >= 0) { NET_schrijven(Inkomend_verbinding, "421 One session at a time\r\n", 27); Sluiten_net(Inkomend_verbinding); }
        else { controle = Inkomend_verbinding; Activiteit = 보드밀리초(); reactie("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (controle < 0) return;
    if ((uint32_t)(보드밀리초() - Activiteit) > 60000) { verbinding_verbreken(); return; }
    if (!sluiten_app) for (unsigned budget = 0; budget < 256; budget++) {
        unsigned char codepoint; int 반환값 = 통신읽기(controle, &codepoint, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { verbinding_verbreken(); return; } Activiteit = 보드밀리초();
        if (codepoint == '\n') { if (줄오류) reactie("500 Command too long or invalid\r\n"); else opdracht(); lijn_formaat_wijzigen = 줄오류 = 0; if (sluiten_app) break; }
        else if (codepoint != '\r') { if (!codepoint || lijn_formaat_wijzigen >= sizeof(invoerregel) - 1) 줄오류 = 1; else invoerregel[lijn_formaat_wijzigen++] = codepoint; }
    }
    if (handmatig_verbinding >= 0 && gegevens < 0) {
        int 반환값 = NET_accepteren(handmatig_verbinding);
        if (반환값 >= 0) {
            if (NET_peer_ADRES(반환값) != NET_peer_ADRES(controle)) Sluiten_net(반환값);
            else { gegevens = 반환값; Sluiten_net(handmatig_verbinding); handmatig_verbinding = -1; Activiteit = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && gegevens >= 0) for (unsigned budget = 0; budget < 8; budget++) {
        unsigned char gegevensblok[512]; int item_AANTAL = 통신읽기(gegevens, gegevensblok, sizeof(gegevensblok));
        if (item_AANTAL == -11) break;
        if (item_AANTAL < 0) { Stop_transfer(); reactie("426 Data connection failed\r\n"); break; }
        Activiteit = 보드밀리초();
        if (item_AANTAL == 0) {
            int resultaat = -1;
            if (!실패여부) {
                int bestandsingang = pk_open(transfer_naam, 쓰기전용 | 없으면만들기 | afkappen_Inhoud, 0600);
                if (bestandsingang >= 0) { resultaat = pk_write(bestandsingang, transfer_Status, 사용량); pk_close(bestandsingang); }
            }
            int 성공여부 = !실패여부 && resultaat == (int)사용량; Stop_transfer(); reactie(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)item_AANTAL > sizeof(transfer_Status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(transfer_Status + 사용량, gegevensblok, item_AANTAL); 사용량 += item_AANTAL; }
    }
    if (수행작업 == 2 && gegevens >= 0) {
        int item_AANTAL = NET_schrijven(gegevens, transfer_Status + 보낸수, 사용량 - 보낸수);
        if (item_AANTAL >= 0) { 보낸수 += item_AANTAL; Activiteit = 보드밀리초(); if (보낸수 == 사용량) { Stop_transfer(); reactie("226 Transfer complete\r\n"); } }
        else if (item_AANTAL != -11) { Stop_transfer(); reactie("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < reactie_formaat_wijzigen) {
        int item_AANTAL = NET_schrijven(controle, 응답모음 + 응답전송량, reactie_formaat_wijzigen - 응답전송량);
        if (item_AANTAL > 0) 응답전송량 += item_AANTAL; else if (item_AANTAL != -11) { verbinding_verbreken(); return; }
    }
    if (응답전송량 == reactie_formaat_wijzigen) { reactie_formaat_wijzigen = 응답전송량 = 0; if (sluiten_app) verbinding_verbreken(); }
}
