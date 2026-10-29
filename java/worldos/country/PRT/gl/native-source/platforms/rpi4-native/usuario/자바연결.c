#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Ficheiro/Saída/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "paquete.h"
typedef uintptr_t máquina_Word;
static int Categoría_VALOR;
static int 꾸러미사용중, 꾸러미인수이동;
static máquina_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned elemento_CONTAR, máquina_Word 첫째값, máquina_Word SEGUNDO_VALOR, máquina_Word código_de_carácter) {
    return 사용자호출(elemento_CONTAR, 첫째값, SEGUNDO_VALOR, código_de_carácter, 0, 0, 0);
}
static void 바이트들(const char *datos_cargo, size_t elemento_CONTAR) { 호출(1, 1, (máquina_Word)datos_cargo, elemento_CONTAR); }
static void carácter(unsigned código_de_carácter) {
    unsigned char datos[4]; unsigned elemento_CONTAR = 0;
    if (código_de_carácter < 128) datos[elemento_CONTAR++] = código_de_carácter;
    else if (código_de_carácter < 2048) { datos[elemento_CONTAR++] = 0xc0 | (código_de_carácter >> 6); datos[elemento_CONTAR++] = 0x80 | (código_de_carácter & 63); }
    else if (código_de_carácter < 65536) { datos[elemento_CONTAR++] = 0xe0 | (código_de_carácter >> 12); datos[elemento_CONTAR++] = 0x80 | ((código_de_carácter >> 6) & 63); datos[elemento_CONTAR++] = 0x80 | (código_de_carácter & 63); }
    else { datos[elemento_CONTAR++] = 0xf0 | (código_de_carácter >> 18); datos[elemento_CONTAR++] = 0x80 | ((código_de_carácter >> 12) & 63); datos[elemento_CONTAR++] = 0x80 | ((código_de_carácter >> 6) & 63); datos[elemento_CONTAR++] = 0x80 | (código_de_carácter & 63); }
    바이트들((const char *)datos, elemento_CONTAR);
}
máquina_Word ferramenta_carácter(máquina_Word VALOR) {
    unsigned código_de_carácter = VALOR;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (código_de_carácter >= 0xdc00 && código_de_carácter <= 0xdfff) { carácter(0x10000 + ((높은부분 - 0xd800) << 10) + código_de_carácter - 0xdc00); return 1; }
        carácter(0xfffd);
    }
    if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdbff) 대기중짝글자 = código_de_carácter;
    else carácter(código_de_carácter > 0x10ffff || (código_de_carácter >= 0xdc00 && código_de_carácter <= 0xdfff) ? 0xfffd : código_de_carácter);
    return 1;
}
máquina_Word 도구출력(máquina_Word VALOR) {
    const máquina_Word *cadea_datos = (const máquina_Word *)VALOR;
    for (máquina_Word 순번 = 0; 순번 < cadea_datos[0]; 순번++) ferramenta_carácter(cadea_datos[순번 + 1]);
    return cadea_datos[0];
}
static int CAMIÑO(máquina_Word obxecto_Material_de_referencia, char medida_datos[512]) {
    const máquina_Word *첫째값 = (const máquina_Word *)obxecto_Material_de_referencia;
    unsigned 사용량 = 0;
    for (máquina_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned código_de_carácter = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] 방식 경로와 호환한다.
        if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; código_de_carácter = 0x10000 + ((código_de_carácter - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdfff) return -22;
        unsigned elemento_CONTAR = código_de_carácter < 128 ? 1 : código_de_carácter < 2048 ? 2 : código_de_carácter < 65536 ? 3 : 4;
        if (사용량 + elemento_CONTAR > 511) return -36;
        if (elemento_CONTAR == 1) medida_datos[사용량++] = código_de_carácter;
        else {
            medida_datos[사용량++] = (elemento_CONTAR == 2 ? 0xc0 : elemento_CONTAR == 3 ? 0xe0 : 0xf0) | (código_de_carácter >> (6 * (elemento_CONTAR - 1)));
            for (unsigned 안쪽순번 = elemento_CONTAR - 1; 안쪽순번; 안쪽순번--) medida_datos[사용량++] = 0x80 | ((código_de_carácter >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    medida_datos[사용량] = 0; return 사용량 ? 0 : -22;
}
máquina_Word ferramenta_abrir(máquina_Word Nome, máquina_Word configuración_Servizo_de_transferencia_intelixente_en_segundo_plano) {
    char datos_cargo[512]; int ERRO = CAMIÑO(Nome, datos_cargo);
    return (uint32_t)(ERRO ? ERRO : 호출(3, (máquina_Word)datos_cargo, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, 0));
}
máquina_Word ferramenta_peche(máquina_Word Ficheiro_agarradoira) { return (uint32_t)호출(4, Ficheiro_agarradoira, 0, 0); }
máquina_Word 도구바이트읽기(máquina_Word Ficheiro_agarradoira) {
    unsigned char SEGUNDO_VALOR; intptr_t elemento_CONTAR = 호출(2, Ficheiro_agarradoira, (máquina_Word)&SEGUNDO_VALOR, 1);
    return (uint32_t)(elemento_CONTAR == 1 ? SEGUNDO_VALOR : elemento_CONTAR == 0 ? 256 : elemento_CONTAR);
}
máquina_Word ferramenta_escribir_byte(máquina_Word Ficheiro_agarradoira, máquina_Word VALOR) {
    unsigned char SEGUNDO_VALOR = VALOR; return (uint32_t)호출(1, Ficheiro_agarradoira, (máquina_Word)&SEGUNDO_VALOR, 1);
}
máquina_Word 도구읽기(máquina_Word Nome, máquina_Word destino_datos_ENDEREZO) {
    if (꾸러미사용중) {
        char datos_cargo[512]; int ERRO = CAMIÑO(Nome, datos_cargo); if (ERRO) return (uint32_t)ERRO;
        unsigned elemento_CONTAR = 0; while (datos_cargo[elemento_CONTAR]) elemento_CONTAR++;
        if (elemento_CONTAR >= 6) for (unsigned 순번 = 0; 순번 < elemento_CONTAR - 6; 순번++) if (datos_cargo[순번] == '.') datos_cargo[순번] = '/';
        unsigned char 바이트들[16384]; máquina_Word *destino_VALOR_cargo = (máquina_Word *)destino_datos_ENDEREZO;
        int RECIBIDO_CONTAR = 꾸러미읽기(datos_cargo, 바이트들, destino_VALOR_cargo[0] < sizeof(바이트들) ? destino_VALOR_cargo[0] : sizeof(바이트들));
        if (RECIBIDO_CONTAR >= 0) { for (int 순번 = 0; 순번 < RECIBIDO_CONTAR; 순번++) destino_VALOR_cargo[순번 + 1] = 바이트들[순번]; return RECIBIDO_CONTAR; }
        if (RECIBIDO_CONTAR != -2) return (uint32_t)RECIBIDO_CONTAR;
    }
    int Ficheiro_agarradoira = 꾸러미사용중 ? -2 : (int32_t)ferramenta_abrir(Nome, 0);
    if (Ficheiro_agarradoira < 0) {
        char datos_cargo[512]; int ERRO = CAMIÑO(Nome, datos_cargo); if (ERRO) return (uint32_t)ERRO;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Seguinte_DESPRAZAMENTO = 자바클래스들[순번].Nome; unsigned 안쪽순번 = 0;
            while (datos_cargo[안쪽순번] && datos_cargo[안쪽순번] == Seguinte_DESPRAZAMENTO[안쪽순번]) 안쪽순번++;
            if (datos_cargo[안쪽순번] || Seguinte_DESPRAZAMENTO[안쪽순번]) continue;
            máquina_Word *destino_VALOR_cargo = (máquina_Word *)destino_datos_ENDEREZO;
            if (destino_VALOR_cargo[0] < 자바클래스들[순번].Tamaño) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Tamaño; 안쪽순번++) destino_VALOR_cargo[안쪽순번 + 1] = 자바클래스들[순번].datos[안쪽순번];
            return 자바클래스들[순번].Tamaño;
        }
        return (uint32_t)Ficheiro_agarradoira;
    }
    máquina_Word *첫째값 = (máquina_Word *)destino_datos_ENDEREZO;
    intptr_t Tamaño = 호출(9, Ficheiro_agarradoira, 0, 0), Completadas_cantidade = 0;
    if (Tamaño < 0 || (máquina_Word)Tamaño > 첫째값[0]) { ferramenta_peche(Ficheiro_agarradoira); return (uint32_t)(Tamaño < 0 ? Tamaño : -27); }
    unsigned char datos_bloquear[256];
    while (Completadas_cantidade < Tamaño) {
        intptr_t elemento_CONTAR = 호출(2, Ficheiro_agarradoira, (máquina_Word)datos_bloquear, Tamaño - Completadas_cantidade < 256 ? Tamaño - Completadas_cantidade : 256);
        if (elemento_CONTAR <= 0) { ferramenta_peche(Ficheiro_agarradoira); return (uint32_t)(elemento_CONTAR ? elemento_CONTAR : -5); }
        for (intptr_t 순번 = 0; 순번 < elemento_CONTAR; 순번++) 첫째값[1 + Completadas_cantidade + 순번] = datos_bloquear[순번];
        Completadas_cantidade += elemento_CONTAR;
    }
    ferramenta_peche(Ficheiro_agarradoira); return Completadas_cantidade;
}
máquina_Word ferramenta_escribir(máquina_Word Nome, máquina_Word 원본자료, máquina_Word introdución_CONTAR) {
    const máquina_Word *첫째값 = (const máquina_Word *)원본자료;
    if (introdución_CONTAR > 첫째값[0] || introdución_CONTAR > 16384) return (uint32_t)-27;
    int Ficheiro_agarradoira = (int32_t)ferramenta_abrir(Nome, 577); if (Ficheiro_agarradoira < 0) return (uint32_t)Ficheiro_agarradoira;
    unsigned char datos_bloquear[256]; máquina_Word Completadas_cantidade = 0;
    while (Completadas_cantidade < introdución_CONTAR) {
        máquina_Word elemento_CONTAR = introdución_CONTAR - Completadas_cantidade < 256 ? introdución_CONTAR - Completadas_cantidade : 256;
        for (máquina_Word 순번 = 0; 순번 < elemento_CONTAR; 순번++) datos_bloquear[순번] = 첫째값[1 + Completadas_cantidade + 순번];
        intptr_t RESULTANTE = 호출(1, Ficheiro_agarradoira, (máquina_Word)datos_bloquear, elemento_CONTAR);
        if (RESULTANTE <= 0) { ferramenta_peche(Ficheiro_agarradoira); return (uint32_t)(RESULTANTE ? RESULTANTE : -5); }
        Completadas_cantidade += RESULTANTE;
    }
    ferramenta_peche(Ficheiro_agarradoira); return introdución_CONTAR;
}
máquina_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
máquina_Word ferramenta_argumento(máquina_Word Busca_ÍNDICE) {
    static const máquina_Word baleiro_VALOR[1] = {0};
    if (Busca_ÍNDICE >= 8) return (máquina_Word)baleiro_VALOR;
    unsigned char 입력결과[256]; intptr_t elemento_CONTAR;
    if (꾸러미사용중 && Busca_ÍNDICE == 0) { const char *datos_cargo = 꾸러미진입클래스(); elemento_CONTAR = 0; while (datos_cargo[elemento_CONTAR] && elemento_CONTAR < 255) { 입력결과[elemento_CONTAR] = datos_cargo[elemento_CONTAR]; elemento_CONTAR++; } }
    else elemento_CONTAR = 호출(15, Busca_ÍNDICE + (꾸러미사용중 ? 꾸러미인수이동 : 0), (máquina_Word)입력결과, sizeof(입력결과));
    if (elemento_CONTAR < 0) return (máquina_Word)baleiro_VALOR;
    máquina_Word *medida_datos = 전달인수[Busca_ÍNDICE]; unsigned introdución_CONTAR = 0;
    for (intptr_t 순번 = 0; 순번 < elemento_CONTAR;) {
        unsigned código_de_carácter = 입력결과[순번++], 더있음 = código_de_carácter < 128 ? 0 : código_de_carácter >= 0xc2 && código_de_carácter < 0xe0 ? 1 : código_de_carácter < 0xf0 && código_de_carácter >= 0xe0 ? 2 : código_de_carácter >= 0xf0 && código_de_carácter <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > elemento_CONTAR) { medida_datos[++introdución_CONTAR] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) código_de_carácter &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { código_de_carácter = (código_de_carácter << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || código_de_carácter < 최소값 || código_de_carácter > 0x10ffff || (código_de_carácter >= 0xd800 && código_de_carácter <= 0xdfff)) código_de_carácter = 0xfffd;
        if (código_de_carácter >= 65536) { código_de_carácter -= 65536; medida_datos[++introdución_CONTAR] = 0xd800 | (código_de_carácter >> 10); medida_datos[++introdución_CONTAR] = 0xdc00 | (código_de_carácter & 1023); }
        else medida_datos[++introdución_CONTAR] = código_de_carácter;
    }
    medida_datos[0] = introdución_CONTAR; return (máquina_Word)medida_datos;
}
máquina_Word 도구분류(void) { return Categoría_VALOR; }
void 커널중단(const char *알림문) {
    const char *datos_cargo = 알림문; while (*datos_cargo) datos_cargo++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, datos_cargo - 알림문); carácter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_usuario_apl(int 방식) {
    Categoría_VALOR = 방식;
    unsigned char 첫항목[256]; intptr_t elemento_CONTAR = 호출(15, 0, (máquina_Word)첫항목, sizeof(첫항목));
    if (방식 == 2 || (방식 == 1 && elemento_CONTAR == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = 방식 == 2 ? 0 : 1;
        char Ficheiro_introdución_nome[256]; intptr_t duración_datos = 호출(15, 꾸러미인수이동, (máquina_Word)Ficheiro_introdución_nome, sizeof(Ficheiro_introdución_nome));
        if (duración_datos <= 0 || 꾸러미열기(Ficheiro_introdución_nome) < 0) {
            static const char ERRO[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(ERRO, sizeof(ERRO) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int RESULTANTE = 자바진입();
    if (대기중짝글자) carácter(0xfffd);
    return RESULTANTE;
}

// UDP는 자체 커널의 SVC를 통과하며 ao_corrente_elemento 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Familia, número_do_porto; uint32_t ENDEREZO; unsigned char 영값[8]; };
static struct 자바주소 UDP_ENDEREZO(unsigned número_do_porto) {
    struct 자바주소 첫째값 = {2, (uint16_t)((número_do_porto << 8) | (número_do_porto >> 8)), 0x0100007f, {0}}; return 첫째값;
}
máquina_Word ferramenta_UDP_abrir(máquina_Word número_do_porto) {
    intptr_t Ficheiro_agarradoira = 호출(32, 2, 2, 17); if (Ficheiro_agarradoira < 0) return (uint32_t)Ficheiro_agarradoira;
    struct 자바주소 첫째값 = UDP_ENDEREZO(número_do_porto);
    첫째값.ENDEREZO = 0;
    intptr_t Estado_VALOR = 호출(33, Ficheiro_agarradoira, (máquina_Word)&첫째값, sizeof(첫째값));
    if (Estado_VALOR < 0) { ferramenta_peche(Ficheiro_agarradoira); return (uint32_t)Estado_VALOR; }
    return Ficheiro_agarradoira;
}
máquina_Word ferramenta_UDP_enviar(máquina_Word Ficheiro_agarradoira, máquina_Word número_do_porto, máquina_Word MATRIZ_VALOR, máquina_Word duración_VALOR) {
    const máquina_Word *원본주소 = (const máquina_Word *)MATRIZ_VALOR; unsigned char datos[512];
    if (duración_VALOR > 512 || duración_VALOR > 원본주소[0]) return (uint32_t)-90;
    for (máquina_Word 순번 = 0; 순번 < duración_VALOR; 순번++) datos[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ENDEREZO(número_do_porto);
    return (uint32_t)사용자호출(34, Ficheiro_agarradoira, (máquina_Word)datos, duración_VALOR, 0, (máquina_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t elemento_CONTAR) { return (elemento_CONTAR>>24)|((elemento_CONTAR>>8)&0xff00)|((elemento_CONTAR<<8)&0xff0000)|(elemento_CONTAR<<24); }
máquina_Word ferramenta_UDP_enviar_ENDEREZO(máquina_Word Ficheiro_agarradoira, máquina_Word ENDEREZO, máquina_Word número_do_porto, máquina_Word MATRIZ_VALOR, máquina_Word duración_VALOR) {
    const máquina_Word *원본주소 = (const máquina_Word *)MATRIZ_VALOR; unsigned char datos[512];
    if (duración_VALOR > 512 || duración_VALOR > 원본주소[0]) return (uint32_t)-90;
    for (máquina_Word 순번 = 0; 순번 < duración_VALOR; 순번++) datos[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ENDEREZO(número_do_porto); 첫째값.ENDEREZO = 바이트순서뒤집기(ENDEREZO);
    return (uint32_t)사용자호출(34, Ficheiro_agarradoira, (máquina_Word)datos, duración_VALOR, 0, (máquina_Word)&첫째값, sizeof(첫째값));
}
máquina_Word ferramenta_CONECTAR(máquina_Word Ficheiro_agarradoira, máquina_Word ENDEREZO, máquina_Word número_do_porto) {
    struct 자바주소 첫째값 = UDP_ENDEREZO(número_do_porto); 첫째값.ENDEREZO = 바이트순서뒤집기(ENDEREZO);
    uint32_t Executar_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t RESULTANTE = 호출(37, Ficheiro_agarradoira, (máquina_Word)&첫째값, sizeof(첫째값));
        if (RESULTANTE != -115) return (uint32_t)RESULTANTE;
        if ((uint32_t)(호출(7, 0, 0, 0) - Executar_2) >= 1000) return (uint32_t)-110;
    }
}
máquina_Word 도구전문받기(máquina_Word Ficheiro_agarradoira, máquina_Word MATRIZ_VALOR, máquina_Word búfer_capacidade) {
    máquina_Word *destino_ENDEREZO = (máquina_Word *)MATRIZ_VALOR; unsigned char datos[512];
    if (búfer_capacidade > 512 || destino_ENDEREZO[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned duración_datos = sizeof(첫째값);
    intptr_t elemento_CONTAR = 사용자호출(35, Ficheiro_agarradoira, (máquina_Word)datos, búfer_capacidade, 0, (máquina_Word)&첫째값, (máquina_Word)&duración_datos);
    if (elemento_CONTAR >= 0) { for (intptr_t 순번 = 0; 순번 < elemento_CONTAR; 순번++) destino_ENDEREZO[순번 + 1] = datos[순번]; destino_ENDEREZO[513] = (첫째값.número_do_porto << 8 | 첫째값.número_do_porto >> 8) & 65535; destino_ENDEREZO[514] = 바이트순서뒤집기(첫째값.ENDEREZO); }
    return (uint32_t)elemento_CONTAR;
}
máquina_Word ferramenta_UDP_porto(máquina_Word Ficheiro_agarradoira) {
    struct 자바주소 첫째값; unsigned duración_datos = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, Ficheiro_agarradoira, (máquina_Word)&첫째값, (máquina_Word)&duración_datos);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.número_do_porto << 8 | 첫째값.número_do_porto >> 8) & 65535);
}
máquina_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
máquina_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
máquina_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
máquina_Word ferramenta_gráficos_agarda(void) { return (uint32_t)화면키기다리기(); }
máquina_Word 도구사각형(máquina_Word X_coordenada, máquina_Word Y_coordenada, máquina_Word 너비값, máquina_Word 높이값, máquina_Word 색상) {
    return (uint32_t)사용자호출(13, X_coordenada, Y_coordenada, 색상, 너비값, 높이값, 0);
}

máquina_Word ferramenta_fluxo(máquina_Word Acción,máquina_Word Ficheiro_agarradoira,máquina_Word VALOR){
    if(Acción==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ENDEREZO(VALOR);
    if(Acción==1){첫째값.ENDEREZO=0;intptr_t 반환값=호출(33,Ficheiro_agarradoira,(máquina_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,Ficheiro_agarradoira,4,0));}
    if(Acción==2)return (uint32_t)호출(37,Ficheiro_agarradoira,(máquina_Word)&첫째값,sizeof(첫째값));
    if(Acción==3)return (uint32_t)호출(39,Ficheiro_agarradoira,0,0);
    if(Acción==4)return ferramenta_UDP_porto(Ficheiro_agarradoira);
    if(Acción==5)return (uint32_t)호출(40,Ficheiro_agarradoira,0,0);
    return (uint32_t)-22;
}
máquina_Word ferramenta_GUI(máquina_Word Acción,máquina_Word 식별자,máquina_Word 첫째값,máquina_Word SEGUNDO_VALOR,máquina_Word código_de_carácter,máquina_Word destino_datos){return (uint32_t)사용자호출(20,Acción,식별자,첫째값,SEGUNDO_VALOR,código_de_carácter,destino_datos);}
máquina_Word ferramenta_GUI_SMS(máquina_Word 식별자,máquina_Word MATRIZ_VALOR,máquina_Word elemento_CONTAR){
    const máquina_Word *원본주소=(const máquina_Word *)MATRIZ_VALOR;uint32_t datos[127];unsigned introdución_CONTAR=0;
    if(elemento_CONTAR>원본주소[0])return (uint32_t)-22;
    for(máquina_Word 순번=0;순번<elemento_CONTAR;순번++){unsigned carácter_codificación=원본주소[순번+1];if(carácter_codificación>=0xd800&&carácter_codificación<=0xdbff&&순번+1<elemento_CONTAR){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;carácter_codificación=0x10000+((carácter_codificación-0xd800)<<10)+낮은값-0xdc00;}if(introdución_CONTAR==127)return (uint32_t)-22;datos[introdución_CONTAR++]=carácter_codificación;}
    return (uint32_t)사용자호출(21,식별자,(máquina_Word)datos,introdución_CONTAR,0,0,0);
}
