#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Rede_Montón.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, control = -1, manual_conexión = -1, datos = -1;
static unsigned 로그인됨, usuario_Aceptar, 줄길이, 줄오류, saír_apl_55b3a1cd, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned 응답크기, 응답전송량, Seguinte_número_do_porto;
static uint32_t Actividade;
static char Liña[256], 응답모음[2048], Ficheiro_introdución_nome[64], Transferir_nome[64];
static unsigned char Transferir_Estado[16384];
static int 같은지(const char *첫째값, const char *SEGUNDO_VALOR) { while (*첫째값 && *첫째값 == *SEGUNDO_VALOR) { 첫째값++; SEGUNDO_VALOR++; } return *첫째값 == *SEGUNDO_VALOR; }
static void resposta(const char *cadea_datos) {
    size_t elemento_CONTAR = strlen(cadea_datos);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, 응답크기 - 응답전송량); 응답크기 -= 응답전송량; 응답전송량 = 0; }
    if (elemento_CONTAR > sizeof(응답모음) - 응답크기) { saír_apl_55b3a1cd = 1; return; }
    memcpy(응답모음 + 응답크기, cadea_datos, elemento_CONTAR); 응답크기 += elemento_CONTAR;
}
static void 수치(unsigned VALOR, char *medida_datos, unsigned *elemento_CONTAR) {
    char díxito_CONTAR[10]; unsigned introdución_CONTAR = 0;
    do { díxito_CONTAR[introdución_CONTAR++] = '0' + VALOR % 10; VALOR /= 10; } while (VALOR);
    while (introdución_CONTAR) medida_datos[(*elemento_CONTAR)++] = díxito_CONTAR[--introdución_CONTAR];
}
static void Stop_Transferir(void) {
    if (datos >= 0) peche_Rede(datos); if (manual_conexión >= 0) peche_Rede(manual_conexión);
    datos = manual_conexión = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void desconectar(void) {
    Stop_Transferir(); if (control >= 0) peche_Rede(control); control = -1;
    로그인됨 = usuario_Aceptar = 줄길이 = 줄오류 = 응답크기 = 응답전송량 = saír_apl_55b3a1cd = 0;
}
int transferencia_de_ficheiros_control(int Acción) {
    if (Acción == 2) return 수신창구 >= 0;
    if (Acción == 0) { desconectar(); if (수신창구 >= 0) peche_Rede(수신창구); 수신창구 = -1; return 0; }
    if (Acción != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { peche_Rede(수신창구); 수신창구 = -1; } return 반환값;
}
static int CAMIÑO(const char *Nome) {
    unsigned elemento_CONTAR = 0; if (*Nome == '/') Nome++;
    if (!*Nome || 같은지(Nome, ".") || 같은지(Nome, "..")) return 0;
    Ficheiro_introdución_nome[elemento_CONTAR++] = '/';
    while (*Nome) {
        unsigned char código_de_carácter = *Nome++;
        if (elemento_CONTAR >= 63 || código_de_carácter < 32 || código_de_carácter == 127 || código_de_carácter == '/' || código_de_carácter == '\\') return 0;
        Ficheiro_introdución_nome[elemento_CONTAR++] = código_de_carácter;
    }
    Ficheiro_introdución_nome[elemento_CONTAR] = 0; return 1;
}
static void enviar_Lista(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int elemento_CONTAR = 자바파일항목길이(순번); if (elemento_CONTAR <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned introdución_CONTAR = strlen(앞부분); memcpy(Transferir_Estado + 사용량, 앞부분, introdución_CONTAR); 사용량 += introdución_CONTAR;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Transferir_Estado, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        introdución_CONTAR = strlen(뒷부분); memcpy(Transferir_Estado + 사용량, 뒷부분, introdución_CONTAR); 사용량 += introdución_CONTAR;
        for (int 안쪽순번 = 0; 안쪽순번 < elemento_CONTAR; 안쪽순번++) Transferir_Estado[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Transferir_Estado[사용량++] = '\r'; Transferir_Estado[사용량++] = '\n';
    }
}
static void 수동연결준비(int 확장여부) {
    if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
    Stop_Transferir(); manual_conexión = 통신끝점만들기(1);
    if (manual_conexión >= 0) 통신주소재사용(manual_conexión);
    unsigned número_do_porto = 50000 + Seguinte_número_do_porto++ % 8;
    if (manual_conexión < 0 || 망주소묶기(manual_conexión, 망상태읽기(0,0), número_do_porto) || 연결기다리기(manual_conexión)) {
        Stop_Transferir(); resposta("425 Cannot open passive listener\r\n"); return;
    }
    char resposta_1262b476[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned elemento_CONTAR = strlen(앞부분); memcpy(resposta_1262b476, 앞부분, elemento_CONTAR);
    if (확장여부) { 수치(número_do_porto, resposta_1262b476, &elemento_CONTAR); resposta_1262b476[elemento_CONTAR++] = '|'; }
    else {
        uint32_t ENDEREZO=망상태읽기(0,0);
        for (int cargo_ÍNDICE=24;cargo_ÍNDICE>=0;cargo_ÍNDICE-=8) { 수치((ENDEREZO>>cargo_ÍNDICE)&255,resposta_1262b476,&elemento_CONTAR);resposta_1262b476[elemento_CONTAR++]=','; }
        수치(número_do_porto / 256, resposta_1262b476, &elemento_CONTAR); resposta_1262b476[elemento_CONTAR++] = ','; 수치(número_do_porto % 256, resposta_1262b476, &elemento_CONTAR);
    }
    resposta_1262b476[elemento_CONTAR++] = ')'; resposta_1262b476[elemento_CONTAR++] = '\r'; resposta_1262b476[elemento_CONTAR++] = '\n'; resposta_1262b476[elemento_CONTAR] = 0; resposta(resposta_1262b476);
}
static void Orde(void) {
    Liña[줄길이] = 0;
    char *부가인수 = Liña; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Liña, "QUIT")) { Stop_Transferir(); resposta("221 Goodbye\r\n"); saír_apl_55b3a1cd = 1; return; }
    if (같은지(Liña, "NOOP")) { resposta("200 OK\r\n"); return; }
    if (같은지(Liña, "SYST")) { resposta("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Liña, "FEAT")) { resposta("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Liña, "USER")) { 로그인됨 = 0; usuario_Aceptar = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); resposta(usuario_Aceptar ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Liña, "PASS")) { 로그인됨 = usuario_Aceptar; resposta(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { resposta("530 Login first\r\n"); return; }
    if (같은지(Liña, "PWD")) resposta("257 \"/\"\r\n");
    else if (같은지(Liña, "CWD")) resposta(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Liña, "TYPE")) resposta(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Liña, "OPTS")) resposta(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Liña, "PASV")) 수동연결준비(0);
    else if (같은지(Liña, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) resposta("522 IPv4 only\r\n"); else 수동연결준비(1); }
    else if (같은지(Liña, "ABOR")) { Stop_Transferir(); resposta("226 Transfer aborted\r\n"); }
    else if (같은지(Liña, "DELE")) { resposta(CAMIÑO(부가인수) && pk_unlink(Ficheiro_introdución_nome) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Liña, "LIST") || 같은지(Liña, "NLST") || 같은지(Liña, "MLSD")) {
        if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
        if (manual_conexión < 0 && datos < 0) { resposta("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { resposta("550 Root listing only\r\n"); return; }
        enviar_Lista(같은지(Liña,"MLSD") ? 2 : 같은지(Liña,"LIST") ? 1 : 0); 수행작업 = 2;
        resposta("150 Opening directory listing\r\n");
    }
    else if (같은지(Liña, "SIZE")) {
        if (!CAMIÑO(부가인수)) { resposta("550 Invalid filename\r\n"); return; }
        int Ficheiro_agarradoira = pk_open(Ficheiro_introdución_nome, só_de_lectura_VALOR, 0); if (Ficheiro_agarradoira < 0) { resposta("550 File unavailable\r\n"); return; }
        int Tamaño = pk_size(Ficheiro_agarradoira); pk_close(Ficheiro_agarradoira); char resposta_1262b476[32] = "213 "; unsigned elemento_CONTAR = 4;
        수치(Tamaño, resposta_1262b476, &elemento_CONTAR); resposta_1262b476[elemento_CONTAR++] = '\r'; resposta_1262b476[elemento_CONTAR++] = '\n'; resposta_1262b476[elemento_CONTAR] = 0; resposta(resposta_1262b476);
    } else if (같은지(Liña, "STOR") || 같은지(Liña, "RETR")) {
        if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
        if (manual_conexión < 0 && datos < 0) { resposta("425 Use PASV or EPSV\r\n"); return; }
        if (!CAMIÑO(부가인수)) { resposta("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Liña, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Transferir_nome, Ficheiro_introdución_nome, strlen(Ficheiro_introdución_nome) + 1);
        if (수행작업 == 2) {
            int Ficheiro_agarradoira = pk_open(Ficheiro_introdución_nome, só_de_lectura_VALOR, 0);
            if (Ficheiro_agarradoira < 0) { 수행작업 = 0; resposta("550 File unavailable\r\n"); return; }
            int elemento_CONTAR = pk_read(Ficheiro_agarradoira, Transferir_Estado, sizeof(Transferir_Estado)); pk_close(Ficheiro_agarradoira);
            if (elemento_CONTAR < 0) { 수행작업 = 0; resposta("451 Read failed\r\n"); return; } 사용량 = elemento_CONTAR;
        }
        resposta("150 Opening binary data connection\r\n");
    } else resposta("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Entrante_conexión = 망연결받기(수신창구);
    if (Entrante_conexión >= 0) {
        if (control >= 0) { 통신쓰기(Entrante_conexión, "421 One session at a time\r\n", 27); peche_Rede(Entrante_conexión); }
        else { control = Entrante_conexión; Actividade = 보드밀리초(); resposta("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (control < 0) return;
    if ((uint32_t)(보드밀리초() - Actividade) > 60000) { desconectar(); return; }
    if (!saír_apl_55b3a1cd) for (unsigned orzamento_atribuído = 0; orzamento_atribuído < 256; orzamento_atribuído++) {
        unsigned char código_de_carácter; int 반환값 = 통신읽기(control, &código_de_carácter, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { desconectar(); return; } Actividade = 보드밀리초();
        if (código_de_carácter == '\n') { if (줄오류) resposta("500 Command too long or invalid\r\n"); else Orde(); 줄길이 = 줄오류 = 0; if (saír_apl_55b3a1cd) break; }
        else if (código_de_carácter != '\r') { if (!código_de_carácter || 줄길이 >= sizeof(Liña) - 1) 줄오류 = 1; else Liña[줄길이++] = código_de_carácter; }
    }
    if (manual_conexión >= 0 && datos < 0) {
        int 반환값 = 망연결받기(manual_conexión);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(control)) peche_Rede(반환값);
            else { datos = 반환값; peche_Rede(manual_conexión); manual_conexión = -1; Actividade = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && datos >= 0) for (unsigned orzamento_atribuído = 0; orzamento_atribuído < 8; orzamento_atribuído++) {
        unsigned char datos_bloquear[512]; int elemento_CONTAR = 통신읽기(datos, datos_bloquear, sizeof(datos_bloquear));
        if (elemento_CONTAR == -11) break;
        if (elemento_CONTAR < 0) { Stop_Transferir(); resposta("426 Data connection failed\r\n"); break; }
        Actividade = 보드밀리초();
        if (elemento_CONTAR == 0) {
            int RESULTANTE = -1;
            if (!실패여부) {
                int Ficheiro_agarradoira = pk_open(Transferir_nome, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (Ficheiro_agarradoira >= 0) { RESULTANTE = pk_write(Ficheiro_agarradoira, Transferir_Estado, 사용량); pk_close(Ficheiro_agarradoira); }
            }
            int 성공여부 = !실패여부 && RESULTANTE == (int)사용량; Stop_Transferir(); resposta(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)elemento_CONTAR > sizeof(Transferir_Estado) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Transferir_Estado + 사용량, datos_bloquear, elemento_CONTAR); 사용량 += elemento_CONTAR; }
    }
    if (수행작업 == 2 && datos >= 0) {
        int elemento_CONTAR = 통신쓰기(datos, Transferir_Estado + 보낸수, 사용량 - 보낸수);
        if (elemento_CONTAR >= 0) { 보낸수 += elemento_CONTAR; Actividade = 보드밀리초(); if (보낸수 == 사용량) { Stop_Transferir(); resposta("226 Transfer complete\r\n"); } }
        else if (elemento_CONTAR != -11) { Stop_Transferir(); resposta("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < 응답크기) {
        int elemento_CONTAR = 통신쓰기(control, 응답모음 + 응답전송량, 응답크기 - 응답전송량);
        if (elemento_CONTAR > 0) 응답전송량 += elemento_CONTAR; else if (elemento_CONTAR != -11) { desconectar(); return; }
    }
    if (응답전송량 == 응답크기) { 응답크기 = 응답전송량 = 0; if (saír_apl_55b3a1cd) desconectar(); }
}
