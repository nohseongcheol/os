#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "rede_pilha.h"
#include "string.h"
#include "Arquivo_ABI.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int porta_de_recepção = -1, visual = -1, manual_conexão = -1, dados = -1;
static unsigned 로그인됨, usuário_OK, linha_dimensionar, 줄오류, encerrar_app, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned resposta_dimensionar, 응답전송량, Avançar_número_da_porta;
static uint32_t Atividade;
static char linha_de_entrada[256], 응답모음[2048], Arquivo_entrada_nome[64], Transferir_nome[64];
static unsigned char Transferir_Estado[16384];
static int 같은지(const char *첫째값, const char *SEGUNDO_VALOR) { while (*첫째값 && *첫째값 == *SEGUNDO_VALOR) { 첫째값++; SEGUNDO_VALOR++; } return *첫째값 == *SEGUNDO_VALOR; }
static void resposta(const char *cadeia_dados) {
    size_t item_CONT_NÚM = strlen(cadeia_dados);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, resposta_dimensionar - 응답전송량); resposta_dimensionar -= 응답전송량; 응답전송량 = 0; }
    if (item_CONT_NÚM > sizeof(응답모음) - resposta_dimensionar) { encerrar_app = 1; return; }
    memcpy(응답모음 + resposta_dimensionar, cadeia_dados, item_CONT_NÚM); resposta_dimensionar += item_CONT_NÚM;
}
static void 수치(unsigned VALOR, char *RC_dados, unsigned *item_CONT_NÚM) {
    char dígito_CONT_NÚM[10]; unsigned entrada_CONT_NÚM_8f7753a1 = 0;
    do { dígito_CONT_NÚM[entrada_CONT_NÚM_8f7753a1++] = '0' + VALOR % 10; VALOR /= 10; } while (VALOR);
    while (entrada_CONT_NÚM_8f7753a1) RC_dados[(*item_CONT_NÚM)++] = dígito_CONT_NÚM[--entrada_CONT_NÚM_8f7753a1];
}
static void Pare_Transferir(void) {
    if (dados >= 0) Close_rede(dados); if (manual_conexão >= 0) Close_rede(manual_conexão);
    dados = manual_conexão = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void desconectar(void) {
    Pare_Transferir(); if (visual >= 0) Close_rede(visual); visual = -1;
    로그인됨 = usuário_OK = linha_dimensionar = 줄오류 = resposta_dimensionar = 응답전송량 = encerrar_app = 0;
}
int transferência_de_arquivo_visual(int Acção) {
    if (Acção == 2) return porta_de_recepção >= 0;
    if (Acção == 0) { desconectar(); if (porta_de_recepção >= 0) Close_rede(porta_de_recepção); porta_de_recepção = -1; return 0; }
    if (Acção != 1) return -22; if (porta_de_recepção >= 0) return 0;
    porta_de_recepção = Criar_soquete_empresa(1); if (porta_de_recepção < 0) return porta_de_recepção;
    int 반환값 = NET_BIND(porta_de_recepção, leitura_rede_Status(0,0), 21); if (!반환값) 반환값 = NET_escutar(porta_de_recepção);
    if (반환값 < 0) { Close_rede(porta_de_recepção); porta_de_recepção = -1; } return 반환값;
}
static int caminho(const char *Nome) {
    unsigned item_CONT_NÚM = 0; if (*Nome == '/') Nome++;
    if (!*Nome || 같은지(Nome, ".") || 같은지(Nome, "..")) return 0;
    Arquivo_entrada_nome[item_CONT_NÚM++] = '/';
    while (*Nome) {
        unsigned char ponto_de_código = *Nome++;
        if (item_CONT_NÚM >= 63 || ponto_de_código < 32 || ponto_de_código == 127 || ponto_de_código == '/' || ponto_de_código == '\\') return 0;
        Arquivo_entrada_nome[item_CONT_NÚM++] = ponto_de_código;
    }
    Arquivo_entrada_nome[item_CONT_NÚM] = 0; return 1;
}
static void enviar_Lista(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int item_CONT_NÚM = 자바파일항목길이(순번); if (item_CONT_NÚM <= 0) continue;
        const char *entrelinhamento_bloco = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned entrada_CONT_NÚM_8f7753a1 = strlen(entrelinhamento_bloco); memcpy(Transferir_Estado + 사용량, entrelinhamento_bloco, entrada_CONT_NÚM_8f7753a1); 사용량 += entrada_CONT_NÚM_8f7753a1;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Transferir_Estado, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        entrada_CONT_NÚM_8f7753a1 = strlen(뒷부분); memcpy(Transferir_Estado + 사용량, 뒷부분, entrada_CONT_NÚM_8f7753a1); 사용량 += entrada_CONT_NÚM_8f7753a1;
        for (int 안쪽순번 = 0; 안쪽순번 < item_CONT_NÚM; 안쪽순번++) Transferir_Estado[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Transferir_Estado[사용량++] = '\r'; Transferir_Estado[사용량++] = '\n';
    }
}
static void Preparar_manual_conexão(int 확장여부) {
    if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
    Pare_Transferir(); manual_conexão = Criar_soquete_empresa(1);
    if (manual_conexão >= 0) 통신주소재사용(manual_conexão);
    unsigned número_da_porta = 50000 + Avançar_número_da_porta++ % 8;
    if (manual_conexão < 0 || NET_BIND(manual_conexão, leitura_rede_Status(0,0), número_da_porta) || NET_escutar(manual_conexão)) {
        Pare_Transferir(); resposta("425 Cannot open passive listener\r\n"); return;
    }
    char réplica[96]; const char *entrelinhamento_bloco = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned item_CONT_NÚM = strlen(entrelinhamento_bloco); memcpy(réplica, entrelinhamento_bloco, item_CONT_NÚM);
    if (확장여부) { 수치(número_da_porta, réplica, &item_CONT_NÚM); réplica[item_CONT_NÚM++] = '|'; }
    else {
        uint32_t Endereço=leitura_rede_Status(0,0);
        for (int cargo_ÍNDICE=24;cargo_ÍNDICE>=0;cargo_ÍNDICE-=8) { 수치((Endereço>>cargo_ÍNDICE)&255,réplica,&item_CONT_NÚM);réplica[item_CONT_NÚM++]=','; }
        수치(número_da_porta / 256, réplica, &item_CONT_NÚM); réplica[item_CONT_NÚM++] = ','; 수치(número_da_porta % 256, réplica, &item_CONT_NÚM);
    }
    réplica[item_CONT_NÚM++] = ')'; réplica[item_CONT_NÚM++] = '\r'; réplica[item_CONT_NÚM++] = '\n'; réplica[item_CONT_NÚM] = 0; resposta(réplica);
}
static void comando(void) {
    linha_de_entrada[linha_dimensionar] = 0;
    char *부가인수 = linha_de_entrada; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(linha_de_entrada, "QUIT")) { Pare_Transferir(); resposta("221 Goodbye\r\n"); encerrar_app = 1; return; }
    if (같은지(linha_de_entrada, "NOOP")) { resposta("200 OK\r\n"); return; }
    if (같은지(linha_de_entrada, "SYST")) { resposta("215 UNIX Type: L8\r\n"); return; }
    if (같은지(linha_de_entrada, "FEAT")) { resposta("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(linha_de_entrada, "USER")) { 로그인됨 = 0; usuário_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); resposta(usuário_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(linha_de_entrada, "PASS")) { 로그인됨 = usuário_OK; resposta(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { resposta("530 Login first\r\n"); return; }
    if (같은지(linha_de_entrada, "PWD")) resposta("257 \"/\"\r\n");
    else if (같은지(linha_de_entrada, "CWD")) resposta(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(linha_de_entrada, "TYPE")) resposta(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(linha_de_entrada, "OPTS")) resposta(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(linha_de_entrada, "PASV")) Preparar_manual_conexão(0);
    else if (같은지(linha_de_entrada, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) resposta("522 IPv4 only\r\n"); else Preparar_manual_conexão(1); }
    else if (같은지(linha_de_entrada, "ABOR")) { Pare_Transferir(); resposta("226 Transfer aborted\r\n"); }
    else if (같은지(linha_de_entrada, "DELE")) { resposta(caminho(부가인수) && pk_unlink(Arquivo_entrada_nome) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(linha_de_entrada, "LIST") || 같은지(linha_de_entrada, "NLST") || 같은지(linha_de_entrada, "MLSD")) {
        if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
        if (manual_conexão < 0 && dados < 0) { resposta("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { resposta("550 Root listing only\r\n"); return; }
        enviar_Lista(같은지(linha_de_entrada,"MLSD") ? 2 : 같은지(linha_de_entrada,"LIST") ? 1 : 0); 수행작업 = 2;
        resposta("150 Opening directory listing\r\n");
    }
    else if (같은지(linha_de_entrada, "SIZE")) {
        if (!caminho(부가인수)) { resposta("550 Invalid filename\r\n"); return; }
        int identificador_de_arquivo = pk_open(Arquivo_entrada_nome, somente_leitura_VALOR, 0); if (identificador_de_arquivo < 0) { resposta("550 File unavailable\r\n"); return; }
        int Tamanho = pk_size(identificador_de_arquivo); pk_close(identificador_de_arquivo); char réplica[32] = "213 "; unsigned item_CONT_NÚM = 4;
        수치(Tamanho, réplica, &item_CONT_NÚM); réplica[item_CONT_NÚM++] = '\r'; réplica[item_CONT_NÚM++] = '\n'; réplica[item_CONT_NÚM] = 0; resposta(réplica);
    } else if (같은지(linha_de_entrada, "STOR") || 같은지(linha_de_entrada, "RETR")) {
        if (수행작업) { resposta("450 Transfer in progress\r\n"); return; }
        if (manual_conexão < 0 && dados < 0) { resposta("425 Use PASV or EPSV\r\n"); return; }
        if (!caminho(부가인수)) { resposta("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(linha_de_entrada, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Transferir_nome, Arquivo_entrada_nome, strlen(Arquivo_entrada_nome) + 1);
        if (수행작업 == 2) {
            int identificador_de_arquivo = pk_open(Arquivo_entrada_nome, somente_leitura_VALOR, 0);
            if (identificador_de_arquivo < 0) { 수행작업 = 0; resposta("550 File unavailable\r\n"); return; }
            int item_CONT_NÚM = pk_read(identificador_de_arquivo, Transferir_Estado, sizeof(Transferir_Estado)); pk_close(identificador_de_arquivo);
            if (item_CONT_NÚM < 0) { 수행작업 = 0; resposta("451 Read failed\r\n"); return; } 사용량 = item_CONT_NÚM;
        }
        resposta("150 Opening binary data connection\r\n");
    } else resposta("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (porta_de_recepção < 0) return;
    int recebida_conexão = NET_aceitar(porta_de_recepção);
    if (recebida_conexão >= 0) {
        if (visual >= 0) { NET_gravar(recebida_conexão, "421 One session at a time\r\n", 27); Close_rede(recebida_conexão); }
        else { visual = recebida_conexão; Atividade = 보드밀리초(); resposta("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (visual < 0) return;
    if ((uint32_t)(보드밀리초() - Atividade) > 60000) { desconectar(); return; }
    if (!encerrar_app) for (unsigned orçamento = 0; orçamento < 256; orçamento++) {
        unsigned char ponto_de_código; int 반환값 = NET_leitura(visual, &ponto_de_código, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { desconectar(); return; } Atividade = 보드밀리초();
        if (ponto_de_código == '\n') { if (줄오류) resposta("500 Command too long or invalid\r\n"); else comando(); linha_dimensionar = 줄오류 = 0; if (encerrar_app) break; }
        else if (ponto_de_código != '\r') { if (!ponto_de_código || linha_dimensionar >= sizeof(linha_de_entrada) - 1) 줄오류 = 1; else linha_de_entrada[linha_dimensionar++] = ponto_de_código; }
    }
    if (manual_conexão >= 0 && dados < 0) {
        int 반환값 = NET_aceitar(manual_conexão);
        if (반환값 >= 0) {
            if (NET_par_email(반환값) != NET_par_email(visual)) Close_rede(반환값);
            else { dados = 반환값; Close_rede(manual_conexão); manual_conexão = -1; Atividade = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && dados >= 0) for (unsigned orçamento = 0; orçamento < 8; orçamento++) {
        unsigned char bloco_de_dados[512]; int item_CONT_NÚM = NET_leitura(dados, bloco_de_dados, sizeof(bloco_de_dados));
        if (item_CONT_NÚM == -11) break;
        if (item_CONT_NÚM < 0) { Pare_Transferir(); resposta("426 Data connection failed\r\n"); break; }
        Atividade = 보드밀리초();
        if (item_CONT_NÚM == 0) {
            int resultado = -1;
            if (!실패여부) {
                int identificador_de_arquivo = pk_open(Transferir_nome, somente_gravação_VALOR | 없으면만들기 | cortar_Sumário, 0600);
                if (identificador_de_arquivo >= 0) { resultado = pk_write(identificador_de_arquivo, Transferir_Estado, 사용량); pk_close(identificador_de_arquivo); }
            }
            int 성공여부 = !실패여부 && resultado == (int)사용량; Pare_Transferir(); resposta(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)item_CONT_NÚM > sizeof(Transferir_Estado) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Transferir_Estado + 사용량, bloco_de_dados, item_CONT_NÚM); 사용량 += item_CONT_NÚM; }
    }
    if (수행작업 == 2 && dados >= 0) {
        int item_CONT_NÚM = NET_gravar(dados, Transferir_Estado + 보낸수, 사용량 - 보낸수);
        if (item_CONT_NÚM >= 0) { 보낸수 += item_CONT_NÚM; Atividade = 보드밀리초(); if (보낸수 == 사용량) { Pare_Transferir(); resposta("226 Transfer complete\r\n"); } }
        else if (item_CONT_NÚM != -11) { Pare_Transferir(); resposta("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < resposta_dimensionar) {
        int item_CONT_NÚM = NET_gravar(visual, 응답모음 + 응답전송량, resposta_dimensionar - 응답전송량);
        if (item_CONT_NÚM > 0) 응답전송량 += item_CONT_NÚM; else if (item_CONT_NÚM != -11) { desconectar(); return; }
    }
    if (응답전송량 == resposta_dimensionar) { resposta_dimensionar = 응답전송량 = 0; if (encerrar_app) desconectar(); }
}
