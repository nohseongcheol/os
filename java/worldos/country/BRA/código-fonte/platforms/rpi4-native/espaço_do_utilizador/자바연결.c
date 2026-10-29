#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 ficheiro/saídaTexto/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "grupo.h"
typedef uintptr_t computador_Word;
static int área_VALOR;
static int 꾸러미사용중, 꾸러미인수이동;
static computador_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned item_CONT_NÚM, computador_Word 첫째값, computador_Word SEGUNDO_VALOR, computador_Word ponto_de_código) {
    return 사용자호출(item_CONT_NÚM, 첫째값, SEGUNDO_VALOR, ponto_de_código, 0, 0, 0);
}
static void 바이트들(const char *dados_cargo, size_t item_CONT_NÚM) { 호출(1, 1, (computador_Word)dados_cargo, item_CONT_NÚM); }
static void caractere(unsigned ponto_de_código) {
    unsigned char dados[4]; unsigned item_CONT_NÚM = 0;
    if (ponto_de_código < 128) dados[item_CONT_NÚM++] = ponto_de_código;
    else if (ponto_de_código < 2048) { dados[item_CONT_NÚM++] = 0xc0 | (ponto_de_código >> 6); dados[item_CONT_NÚM++] = 0x80 | (ponto_de_código & 63); }
    else if (ponto_de_código < 65536) { dados[item_CONT_NÚM++] = 0xe0 | (ponto_de_código >> 12); dados[item_CONT_NÚM++] = 0x80 | ((ponto_de_código >> 6) & 63); dados[item_CONT_NÚM++] = 0x80 | (ponto_de_código & 63); }
    else { dados[item_CONT_NÚM++] = 0xf0 | (ponto_de_código >> 18); dados[item_CONT_NÚM++] = 0x80 | ((ponto_de_código >> 12) & 63); dados[item_CONT_NÚM++] = 0x80 | ((ponto_de_código >> 6) & 63); dados[item_CONT_NÚM++] = 0x80 | (ponto_de_código & 63); }
    바이트들((const char *)dados, item_CONT_NÚM);
}
computador_Word ferramenta_caractere(computador_Word VALOR) {
    unsigned ponto_de_código = VALOR;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (ponto_de_código >= 0xdc00 && ponto_de_código <= 0xdfff) { caractere(0x10000 + ((높은부분 - 0xd800) << 10) + ponto_de_código - 0xdc00); return 1; }
        caractere(0xfffd);
    }
    if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdbff) 대기중짝글자 = ponto_de_código;
    else caractere(ponto_de_código > 0x10ffff || (ponto_de_código >= 0xdc00 && ponto_de_código <= 0xdfff) ? 0xfffd : ponto_de_código);
    return 1;
}
computador_Word ferramenta_imprimir(computador_Word VALOR) {
    const computador_Word *cadeia_dados = (const computador_Word *)VALOR;
    for (computador_Word 순번 = 0; 순번 < cadeia_dados[0]; 순번++) ferramenta_caractere(cadeia_dados[순번 + 1]);
    return cadeia_dados[0];
}
static int caminho(computador_Word objeto_Referência, char RC_dados[512]) {
    const computador_Word *첫째값 = (const computador_Word *)objeto_Referência;
    unsigned 사용량 = 0;
    for (computador_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned ponto_de_código = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] método_MODO 경로와 호환한다.
        if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; ponto_de_código = 0x10000 + ((ponto_de_código - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdfff) return -22;
        unsigned item_CONT_NÚM = ponto_de_código < 128 ? 1 : ponto_de_código < 2048 ? 2 : ponto_de_código < 65536 ? 3 : 4;
        if (사용량 + item_CONT_NÚM > 511) return -36;
        if (item_CONT_NÚM == 1) RC_dados[사용량++] = ponto_de_código;
        else {
            RC_dados[사용량++] = (item_CONT_NÚM == 2 ? 0xc0 : item_CONT_NÚM == 3 ? 0xe0 : 0xf0) | (ponto_de_código >> (6 * (item_CONT_NÚM - 1)));
            for (unsigned 안쪽순번 = item_CONT_NÚM - 1; 안쪽순번; 안쪽순번--) RC_dados[사용량++] = 0x80 | ((ponto_de_código >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    RC_dados[사용량] = 0; return 사용량 ? 0 : -22;
}
computador_Word ferramenta_abrir(computador_Word Nome, computador_Word Configuração_BITS) {
    char dados_cargo[512]; int erro = caminho(Nome, dados_cargo);
    return (uint32_t)(erro ? erro : 호출(3, (computador_Word)dados_cargo, Configuração_BITS, 0));
}
computador_Word ferramenta_Close(computador_Word identificador_de_arquivo) { return (uint32_t)호출(4, identificador_de_arquivo, 0, 0); }
computador_Word ferramenta_leitura_byte(computador_Word identificador_de_arquivo) {
    unsigned char SEGUNDO_VALOR; intptr_t item_CONT_NÚM = 호출(2, identificador_de_arquivo, (computador_Word)&SEGUNDO_VALOR, 1);
    return (uint32_t)(item_CONT_NÚM == 1 ? SEGUNDO_VALOR : item_CONT_NÚM == 0 ? 256 : item_CONT_NÚM);
}
computador_Word ferramenta_gravar_byte(computador_Word identificador_de_arquivo, computador_Word VALOR) {
    unsigned char SEGUNDO_VALOR = VALOR; return (uint32_t)호출(1, identificador_de_arquivo, (computador_Word)&SEGUNDO_VALOR, 1);
}
computador_Word ferramenta_leitura(computador_Word Nome, computador_Word destino_dados_email) {
    if (꾸러미사용중) {
        char dados_cargo[512]; int erro = caminho(Nome, dados_cargo); if (erro) return (uint32_t)erro;
        unsigned item_CONT_NÚM = 0; while (dados_cargo[item_CONT_NÚM]) item_CONT_NÚM++;
        if (item_CONT_NÚM >= 6) for (unsigned 순번 = 0; 순번 < item_CONT_NÚM - 6; 순번++) if (dados_cargo[순번] == '.') dados_cargo[순번] = '/';
        unsigned char 바이트들[16384]; computador_Word *destino_VALOR_cargo = (computador_Word *)destino_dados_email;
        int RECEBER_CONT_NÚM = 꾸러미읽기(dados_cargo, 바이트들, destino_VALOR_cargo[0] < sizeof(바이트들) ? destino_VALOR_cargo[0] : sizeof(바이트들));
        if (RECEBER_CONT_NÚM >= 0) { for (int 순번 = 0; 순번 < RECEBER_CONT_NÚM; 순번++) destino_VALOR_cargo[순번 + 1] = 바이트들[순번]; return RECEBER_CONT_NÚM; }
        if (RECEBER_CONT_NÚM != -2) return (uint32_t)RECEBER_CONT_NÚM;
    }
    int identificador_de_arquivo = 꾸러미사용중 ? -2 : (int32_t)ferramenta_abrir(Nome, 0);
    if (identificador_de_arquivo < 0) {
        char dados_cargo[512]; int erro = caminho(Nome, dados_cargo); if (erro) return (uint32_t)erro;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Avançar_DESLOC = 자바클래스들[순번].Nome; unsigned 안쪽순번 = 0;
            while (dados_cargo[안쪽순번] && dados_cargo[안쪽순번] == Avançar_DESLOC[안쪽순번]) 안쪽순번++;
            if (dados_cargo[안쪽순번] || Avançar_DESLOC[안쪽순번]) continue;
            computador_Word *destino_VALOR_cargo = (computador_Word *)destino_dados_email;
            if (destino_VALOR_cargo[0] < 자바클래스들[순번].Tamanho) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Tamanho; 안쪽순번++) destino_VALOR_cargo[안쪽순번 + 1] = 자바클래스들[순번].dados[안쪽순번];
            return 자바클래스들[순번].Tamanho;
        }
        return (uint32_t)identificador_de_arquivo;
    }
    computador_Word *첫째값 = (computador_Word *)destino_dados_email;
    intptr_t Tamanho = 호출(9, identificador_de_arquivo, 0, 0), concluído_valor = 0;
    if (Tamanho < 0 || (computador_Word)Tamanho > 첫째값[0]) { ferramenta_Close(identificador_de_arquivo); return (uint32_t)(Tamanho < 0 ? Tamanho : -27); }
    unsigned char bloco_de_dados[256];
    while (concluído_valor < Tamanho) {
        intptr_t item_CONT_NÚM = 호출(2, identificador_de_arquivo, (computador_Word)bloco_de_dados, Tamanho - concluído_valor < 256 ? Tamanho - concluído_valor : 256);
        if (item_CONT_NÚM <= 0) { ferramenta_Close(identificador_de_arquivo); return (uint32_t)(item_CONT_NÚM ? item_CONT_NÚM : -5); }
        for (intptr_t 순번 = 0; 순번 < item_CONT_NÚM; 순번++) 첫째값[1 + concluído_valor + 순번] = bloco_de_dados[순번];
        concluído_valor += item_CONT_NÚM;
    }
    ferramenta_Close(identificador_de_arquivo); return concluído_valor;
}
computador_Word ferramenta_gravar(computador_Word Nome, computador_Word 원본자료, computador_Word entrada_CONT_NÚM_8f7753a1) {
    const computador_Word *첫째값 = (const computador_Word *)원본자료;
    if (entrada_CONT_NÚM_8f7753a1 > 첫째값[0] || entrada_CONT_NÚM_8f7753a1 > 16384) return (uint32_t)-27;
    int identificador_de_arquivo = (int32_t)ferramenta_abrir(Nome, 577); if (identificador_de_arquivo < 0) return (uint32_t)identificador_de_arquivo;
    unsigned char bloco_de_dados[256]; computador_Word concluído_valor = 0;
    while (concluído_valor < entrada_CONT_NÚM_8f7753a1) {
        computador_Word item_CONT_NÚM = entrada_CONT_NÚM_8f7753a1 - concluído_valor < 256 ? entrada_CONT_NÚM_8f7753a1 - concluído_valor : 256;
        for (computador_Word 순번 = 0; 순번 < item_CONT_NÚM; 순번++) bloco_de_dados[순번] = 첫째값[1 + concluído_valor + 순번];
        intptr_t resultado = 호출(1, identificador_de_arquivo, (computador_Word)bloco_de_dados, item_CONT_NÚM);
        if (resultado <= 0) { ferramenta_Close(identificador_de_arquivo); return (uint32_t)(resultado ? resultado : -5); }
        concluído_valor += resultado;
    }
    ferramenta_Close(identificador_de_arquivo); return entrada_CONT_NÚM_8f7753a1;
}
computador_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
computador_Word ferramenta_argumento(computador_Word PROC_ÍNDICE) {
    static const computador_Word vazio_VALOR[1] = {0};
    if (PROC_ÍNDICE >= 8) return (computador_Word)vazio_VALOR;
    unsigned char entrada[256]; intptr_t item_CONT_NÚM;
    if (꾸러미사용중 && PROC_ÍNDICE == 0) { const char *dados_cargo = 꾸러미진입클래스(); item_CONT_NÚM = 0; while (dados_cargo[item_CONT_NÚM] && item_CONT_NÚM < 255) { entrada[item_CONT_NÚM] = dados_cargo[item_CONT_NÚM]; item_CONT_NÚM++; } }
    else item_CONT_NÚM = 호출(15, PROC_ÍNDICE + (꾸러미사용중 ? 꾸러미인수이동 : 0), (computador_Word)entrada, sizeof(entrada));
    if (item_CONT_NÚM < 0) return (computador_Word)vazio_VALOR;
    computador_Word *RC_dados = 전달인수[PROC_ÍNDICE]; unsigned entrada_CONT_NÚM_8f7753a1 = 0;
    for (intptr_t 순번 = 0; 순번 < item_CONT_NÚM;) {
        unsigned ponto_de_código = entrada[순번++], 더있음 = ponto_de_código < 128 ? 0 : ponto_de_código >= 0xc2 && ponto_de_código < 0xe0 ? 1 : ponto_de_código < 0xf0 && ponto_de_código >= 0xe0 ? 2 : ponto_de_código >= 0xf0 && ponto_de_código <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > item_CONT_NÚM) { RC_dados[++entrada_CONT_NÚM_8f7753a1] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) ponto_de_código &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (entrada[순번] & 0xc0) == 0x80) { ponto_de_código = (ponto_de_código << 6) | (entrada[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || ponto_de_código < 최소값 || ponto_de_código > 0x10ffff || (ponto_de_código >= 0xd800 && ponto_de_código <= 0xdfff)) ponto_de_código = 0xfffd;
        if (ponto_de_código >= 65536) { ponto_de_código -= 65536; RC_dados[++entrada_CONT_NÚM_8f7753a1] = 0xd800 | (ponto_de_código >> 10); RC_dados[++entrada_CONT_NÚM_8f7753a1] = 0xdc00 | (ponto_de_código & 1023); }
        else RC_dados[++entrada_CONT_NÚM_8f7753a1] = ponto_de_código;
    }
    RC_dados[0] = entrada_CONT_NÚM_8f7753a1; return (computador_Word)RC_dados;
}
computador_Word ferramenta_Tipo(void) { return área_VALOR; }
void 커널중단(const char *aviso_SMS) {
    const char *dados_cargo = aviso_SMS; while (*dados_cargo) dados_cargo++;
    바이트들("Java tool runtime error: ", 25); 바이트들(aviso_SMS, dados_cargo - aviso_SMS); caractere(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_usuário_app(int método_MODO) {
    área_VALOR = método_MODO;
    unsigned char 첫항목[256]; intptr_t item_CONT_NÚM = 호출(15, 0, (computador_Word)첫항목, sizeof(첫항목));
    if (método_MODO == 2 || (método_MODO == 1 && item_CONT_NÚM == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = método_MODO == 2 ? 0 : 1;
        char Arquivo_entrada_nome[256]; intptr_t duração_dados = 호출(15, 꾸러미인수이동, (computador_Word)Arquivo_entrada_nome, sizeof(Arquivo_entrada_nome));
        if (duração_dados <= 0 || 꾸러미열기(Arquivo_entrada_nome) < 0) {
            static const char erro[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(erro, sizeof(erro) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int resultado = 자바진입();
    if (대기중짝글자) caractere(0xfffd);
    return resultado;
}

// UDP는 nativo 커널의 SVC를 통과하며 em_dia_item 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Família, número_da_porta; uint32_t Endereço; unsigned char valor_zero[8]; };
static struct 자바주소 UDP_email(unsigned número_da_porta) {
    struct 자바주소 첫째값 = {2, (uint16_t)((número_da_porta << 8) | (número_da_porta >> 8)), 0x0100007f, {0}}; return 첫째값;
}
computador_Word ferramenta_UDP_abrir(computador_Word número_da_porta) {
    intptr_t identificador_de_arquivo = 호출(32, 2, 2, 17); if (identificador_de_arquivo < 0) return (uint32_t)identificador_de_arquivo;
    struct 자바주소 첫째값 = UDP_email(número_da_porta);
    첫째값.Endereço = 0;
    intptr_t Estado_VALOR = 호출(33, identificador_de_arquivo, (computador_Word)&첫째값, sizeof(첫째값));
    if (Estado_VALOR < 0) { ferramenta_Close(identificador_de_arquivo); return (uint32_t)Estado_VALOR; }
    return identificador_de_arquivo;
}
computador_Word ferramenta_UDP_enviar(computador_Word identificador_de_arquivo, computador_Word número_da_porta, computador_Word MATRIZ_VALOR, computador_Word duração_VALOR) {
    const computador_Word *원본주소 = (const computador_Word *)MATRIZ_VALOR; unsigned char dados[512];
    if (duração_VALOR > 512 || duração_VALOR > 원본주소[0]) return (uint32_t)-90;
    for (computador_Word 순번 = 0; 순번 < duração_VALOR; 순번++) dados[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_email(número_da_porta);
    return (uint32_t)사용자호출(34, identificador_de_arquivo, (computador_Word)dados, duração_VALOR, 0, (computador_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t item_CONT_NÚM) { return (item_CONT_NÚM>>24)|((item_CONT_NÚM>>8)&0xff00)|((item_CONT_NÚM<<8)&0xff0000)|(item_CONT_NÚM<<24); }
computador_Word ferramenta_UDP_enviar_email(computador_Word identificador_de_arquivo, computador_Word Endereço, computador_Word número_da_porta, computador_Word MATRIZ_VALOR, computador_Word duração_VALOR) {
    const computador_Word *원본주소 = (const computador_Word *)MATRIZ_VALOR; unsigned char dados[512];
    if (duração_VALOR > 512 || duração_VALOR > 원본주소[0]) return (uint32_t)-90;
    for (computador_Word 순번 = 0; 순번 < duração_VALOR; 순번++) dados[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_email(número_da_porta); 첫째값.Endereço = 바이트순서뒤집기(Endereço);
    return (uint32_t)사용자호출(34, identificador_de_arquivo, (computador_Word)dados, duração_VALOR, 0, (computador_Word)&첫째값, sizeof(첫째값));
}
computador_Word ferramenta_Conexão(computador_Word identificador_de_arquivo, computador_Word Endereço, computador_Word número_da_porta) {
    struct 자바주소 첫째값 = UDP_email(número_da_porta); 첫째값.Endereço = 바이트순서뒤집기(Endereço);
    uint32_t iniciar = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t resultado = 호출(37, identificador_de_arquivo, (computador_Word)&첫째값, sizeof(첫째값));
        if (resultado != -115) return (uint32_t)resultado;
        if ((uint32_t)(호출(7, 0, 0, 0) - iniciar) >= 1000) return (uint32_t)-110;
    }
}
computador_Word 도구전문받기(computador_Word identificador_de_arquivo, computador_Word MATRIZ_VALOR, computador_Word buffer_capacidade) {
    computador_Word *destino_email = (computador_Word *)MATRIZ_VALOR; unsigned char dados[512];
    if (buffer_capacidade > 512 || destino_email[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned duração_dados = sizeof(첫째값);
    intptr_t item_CONT_NÚM = 사용자호출(35, identificador_de_arquivo, (computador_Word)dados, buffer_capacidade, 0, (computador_Word)&첫째값, (computador_Word)&duração_dados);
    if (item_CONT_NÚM >= 0) { for (intptr_t 순번 = 0; 순번 < item_CONT_NÚM; 순번++) destino_email[순번 + 1] = dados[순번]; destino_email[513] = (첫째값.número_da_porta << 8 | 첫째값.número_da_porta >> 8) & 65535; destino_email[514] = 바이트순서뒤집기(첫째값.Endereço); }
    return (uint32_t)item_CONT_NÚM;
}
computador_Word ferramenta_UDP_porta(computador_Word identificador_de_arquivo) {
    struct 자바주소 첫째값; unsigned duração_dados = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, identificador_de_arquivo, (computador_Word)&첫째값, (computador_Word)&duração_dados);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.número_da_porta << 8 | 첫째값.número_da_porta >> 8) & 65535);
}
computador_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
computador_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
computador_Word ferramenta_tela_altura(void) { return (uint32_t)leitura_tela_altura(); }
computador_Word ferramenta_gráficos_aguarde(void) { return (uint32_t)화면키기다리기(); }
computador_Word ferramenta_retângulo(computador_Word coordenada_X, computador_Word Y_coordenada, computador_Word 너비값, computador_Word solicitado_altura_VALOR, computador_Word 색상) {
    return (uint32_t)사용자호출(13, coordenada_X, Y_coordenada, 색상, 너비값, solicitado_altura_VALOR, 0);
}

computador_Word ferramenta_fluxo(computador_Word Acção,computador_Word identificador_de_arquivo,computador_Word VALOR){
    if(Acção==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_email(VALOR);
    if(Acção==1){첫째값.Endereço=0;intptr_t 반환값=호출(33,identificador_de_arquivo,(computador_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,identificador_de_arquivo,4,0));}
    if(Acção==2)return (uint32_t)호출(37,identificador_de_arquivo,(computador_Word)&첫째값,sizeof(첫째값));
    if(Acção==3)return (uint32_t)호출(39,identificador_de_arquivo,0,0);
    if(Acção==4)return ferramenta_UDP_porta(identificador_de_arquivo);
    if(Acção==5)return (uint32_t)호출(40,identificador_de_arquivo,0,0);
    return (uint32_t)-22;
}
computador_Word ferramenta_GUI(computador_Word Acção,computador_Word identificador_VALOR,computador_Word 첫째값,computador_Word SEGUNDO_VALOR,computador_Word ponto_de_código,computador_Word destino_dados){return (uint32_t)사용자호출(20,Acção,identificador_VALOR,첫째값,SEGUNDO_VALOR,ponto_de_código,destino_dados);}
computador_Word ferramenta_GUI_SMS(computador_Word identificador_VALOR,computador_Word MATRIZ_VALOR,computador_Word item_CONT_NÚM){
    const computador_Word *원본주소=(const computador_Word *)MATRIZ_VALOR;uint32_t dados[127];unsigned entrada_CONT_NÚM_8f7753a1=0;
    if(item_CONT_NÚM>원본주소[0])return (uint32_t)-22;
    for(computador_Word 순번=0;순번<item_CONT_NÚM;순번++){unsigned codificação_de_caracteres=원본주소[순번+1];if(codificação_de_caracteres>=0xd800&&codificação_de_caracteres<=0xdbff&&순번+1<item_CONT_NÚM){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;codificação_de_caracteres=0x10000+((codificação_de_caracteres-0xd800)<<10)+낮은값-0xdc00;}if(entrada_CONT_NÚM_8f7753a1==127)return (uint32_t)-22;dados[entrada_CONT_NÚM_8f7753a1++]=codificação_de_caracteres;}
    return (uint32_t)사용자호출(21,identificador_VALOR,(computador_Word)dados,entrada_CONT_NÚM_8f7753a1,0,0,0);
}
