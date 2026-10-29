#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fitxer/Sortida/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "paquet.h"
typedef uintptr_t màquina_Word;
static int Categoria_VALOR;
static int 꾸러미사용중, 꾸러미인수이동;
static màquina_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned element_COMPT, màquina_Word 첫째값, màquina_Word SEGON_VALOR, màquina_Word codi_de_caràcter) {
    return 사용자호출(element_COMPT, 첫째값, SEGON_VALOR, codi_de_caràcter, 0, 0, 0);
}
static void 바이트들(const char *dades_càrrec, size_t element_COMPT) { 호출(1, 1, (màquina_Word)dades_càrrec, element_COMPT); }
static void caràcter(unsigned codi_de_caràcter) {
    unsigned char dades[4]; unsigned element_COMPT = 0;
    if (codi_de_caràcter < 128) dades[element_COMPT++] = codi_de_caràcter;
    else if (codi_de_caràcter < 2048) { dades[element_COMPT++] = 0xc0 | (codi_de_caràcter >> 6); dades[element_COMPT++] = 0x80 | (codi_de_caràcter & 63); }
    else if (codi_de_caràcter < 65536) { dades[element_COMPT++] = 0xe0 | (codi_de_caràcter >> 12); dades[element_COMPT++] = 0x80 | ((codi_de_caràcter >> 6) & 63); dades[element_COMPT++] = 0x80 | (codi_de_caràcter & 63); }
    else { dades[element_COMPT++] = 0xf0 | (codi_de_caràcter >> 18); dades[element_COMPT++] = 0x80 | ((codi_de_caràcter >> 12) & 63); dades[element_COMPT++] = 0x80 | ((codi_de_caràcter >> 6) & 63); dades[element_COMPT++] = 0x80 | (codi_de_caràcter & 63); }
    바이트들((const char *)dades, element_COMPT);
}
màquina_Word eina_caràcter(màquina_Word VALOR) {
    unsigned codi_de_caràcter = VALOR;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (codi_de_caràcter >= 0xdc00 && codi_de_caràcter <= 0xdfff) { caràcter(0x10000 + ((높은부분 - 0xd800) << 10) + codi_de_caràcter - 0xdc00); return 1; }
        caràcter(0xfffd);
    }
    if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdbff) 대기중짝글자 = codi_de_caràcter;
    else caràcter(codi_de_caràcter > 0x10ffff || (codi_de_caràcter >= 0xdc00 && codi_de_caràcter <= 0xdfff) ? 0xfffd : codi_de_caràcter);
    return 1;
}
màquina_Word eina_imprimir(màquina_Word VALOR) {
    const màquina_Word *cadena_dades = (const màquina_Word *)VALOR;
    for (màquina_Word 순번 = 0; 순번 < cadena_dades[0]; 순번++) eina_caràcter(cadena_dades[순번 + 1]);
    return cadena_dades[0];
}
static int Camí(màquina_Word objecte_Referència, char mesura_dades[512]) {
    const màquina_Word *첫째값 = (const màquina_Word *)objecte_Referència;
    unsigned 사용량 = 0;
    for (màquina_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned codi_de_caràcter = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] 방식 경로와 호환한다.
        if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; codi_de_caràcter = 0x10000 + ((codi_de_caràcter - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdfff) return -22;
        unsigned element_COMPT = codi_de_caràcter < 128 ? 1 : codi_de_caràcter < 2048 ? 2 : codi_de_caràcter < 65536 ? 3 : 4;
        if (사용량 + element_COMPT > 511) return -36;
        if (element_COMPT == 1) mesura_dades[사용량++] = codi_de_caràcter;
        else {
            mesura_dades[사용량++] = (element_COMPT == 2 ? 0xc0 : element_COMPT == 3 ? 0xe0 : 0xf0) | (codi_de_caràcter >> (6 * (element_COMPT - 1)));
            for (unsigned 안쪽순번 = element_COMPT - 1; 안쪽순번; 안쪽순번--) mesura_dades[사용량++] = 0x80 | ((codi_de_caràcter >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    mesura_dades[사용량] = 0; return 사용량 ? 0 : -22;
}
màquina_Word eina_crear(màquina_Word Nom, màquina_Word configuració_Servei_de_transferència_intel_ligent_en_segon_terme) {
    char dades_càrrec[512]; int s_ha_produït_un_error = Camí(Nom, dades_càrrec);
    return (uint32_t)(s_ha_produït_un_error ? s_ha_produït_un_error : 호출(3, (màquina_Word)dades_càrrec, configuració_Servei_de_transferència_intel_ligent_en_segon_terme, 0));
}
màquina_Word eina_Tanca(màquina_Word arxiu_control_7f4cdfd5) { return (uint32_t)호출(4, arxiu_control_7f4cdfd5, 0, 0); }
màquina_Word eina_tancar_byte(màquina_Word arxiu_control_7f4cdfd5) {
    unsigned char SEGON_VALOR; intptr_t element_COMPT = 호출(2, arxiu_control_7f4cdfd5, (màquina_Word)&SEGON_VALOR, 1);
    return (uint32_t)(element_COMPT == 1 ? SEGON_VALOR : element_COMPT == 0 ? 256 : element_COMPT);
}
màquina_Word eina_escriure_byte(màquina_Word arxiu_control_7f4cdfd5, màquina_Word VALOR) {
    unsigned char SEGON_VALOR = VALOR; return (uint32_t)호출(1, arxiu_control_7f4cdfd5, (màquina_Word)&SEGON_VALOR, 1);
}
màquina_Word eina_tancar(màquina_Word Nom, màquina_Word destinació_dades_ADREÇA) {
    if (꾸러미사용중) {
        char dades_càrrec[512]; int s_ha_produït_un_error = Camí(Nom, dades_càrrec); if (s_ha_produït_un_error) return (uint32_t)s_ha_produït_un_error;
        unsigned element_COMPT = 0; while (dades_càrrec[element_COMPT]) element_COMPT++;
        if (element_COMPT >= 6) for (unsigned 순번 = 0; 순번 < element_COMPT - 6; 순번++) if (dades_càrrec[순번] == '.') dades_càrrec[순번] = '/';
        unsigned char 바이트들[16384]; màquina_Word *destinació_VALOR_càrrec = (màquina_Word *)destinació_dades_ADREÇA;
        int CANTIDAD_RECIBIDA_COMPT = 꾸러미읽기(dades_càrrec, 바이트들, destinació_VALOR_càrrec[0] < sizeof(바이트들) ? destinació_VALOR_càrrec[0] : sizeof(바이트들));
        if (CANTIDAD_RECIBIDA_COMPT >= 0) { for (int 순번 = 0; 순번 < CANTIDAD_RECIBIDA_COMPT; 순번++) destinació_VALOR_càrrec[순번 + 1] = 바이트들[순번]; return CANTIDAD_RECIBIDA_COMPT; }
        if (CANTIDAD_RECIBIDA_COMPT != -2) return (uint32_t)CANTIDAD_RECIBIDA_COMPT;
    }
    int arxiu_control_7f4cdfd5 = 꾸러미사용중 ? -2 : (int32_t)eina_crear(Nom, 0);
    if (arxiu_control_7f4cdfd5 < 0) {
        char dades_càrrec[512]; int s_ha_produït_un_error = Camí(Nom, dades_càrrec); if (s_ha_produït_un_error) return (uint32_t)s_ha_produït_un_error;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Següent_DESPLAÇAMENT = 자바클래스들[순번].Nom; unsigned 안쪽순번 = 0;
            while (dades_càrrec[안쪽순번] && dades_càrrec[안쪽순번] == Següent_DESPLAÇAMENT[안쪽순번]) 안쪽순번++;
            if (dades_càrrec[안쪽순번] || Següent_DESPLAÇAMENT[안쪽순번]) continue;
            màquina_Word *destinació_VALOR_càrrec = (màquina_Word *)destinació_dades_ADREÇA;
            if (destinació_VALOR_càrrec[0] < 자바클래스들[순번].Mida) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Mida; 안쪽순번++) destinació_VALOR_càrrec[안쪽순번 + 1] = 자바클래스들[순번].dades[안쪽순번];
            return 자바클래스들[순번].Mida;
        }
        return (uint32_t)arxiu_control_7f4cdfd5;
    }
    màquina_Word *첫째값 = (màquina_Word *)destinació_dades_ADREÇA;
    intptr_t Mida = 호출(9, arxiu_control_7f4cdfd5, 0, 0), Completades_quantitat = 0;
    if (Mida < 0 || (màquina_Word)Mida > 첫째값[0]) { eina_Tanca(arxiu_control_7f4cdfd5); return (uint32_t)(Mida < 0 ? Mida : -27); }
    unsigned char dades_bloquejar[256];
    while (Completades_quantitat < Mida) {
        intptr_t element_COMPT = 호출(2, arxiu_control_7f4cdfd5, (màquina_Word)dades_bloquejar, Mida - Completades_quantitat < 256 ? Mida - Completades_quantitat : 256);
        if (element_COMPT <= 0) { eina_Tanca(arxiu_control_7f4cdfd5); return (uint32_t)(element_COMPT ? element_COMPT : -5); }
        for (intptr_t 순번 = 0; 순번 < element_COMPT; 순번++) 첫째값[1 + Completades_quantitat + 순번] = dades_bloquejar[순번];
        Completades_quantitat += element_COMPT;
    }
    eina_Tanca(arxiu_control_7f4cdfd5); return Completades_quantitat;
}
màquina_Word eina_escriure(màquina_Word Nom, màquina_Word 원본자료, màquina_Word introducció_COMPT) {
    const màquina_Word *첫째값 = (const màquina_Word *)원본자료;
    if (introducció_COMPT > 첫째값[0] || introducció_COMPT > 16384) return (uint32_t)-27;
    int arxiu_control_7f4cdfd5 = (int32_t)eina_crear(Nom, 577); if (arxiu_control_7f4cdfd5 < 0) return (uint32_t)arxiu_control_7f4cdfd5;
    unsigned char dades_bloquejar[256]; màquina_Word Completades_quantitat = 0;
    while (Completades_quantitat < introducció_COMPT) {
        màquina_Word element_COMPT = introducció_COMPT - Completades_quantitat < 256 ? introducció_COMPT - Completades_quantitat : 256;
        for (màquina_Word 순번 = 0; 순번 < element_COMPT; 순번++) dades_bloquejar[순번] = 첫째값[1 + Completades_quantitat + 순번];
        intptr_t RESULTAT = 호출(1, arxiu_control_7f4cdfd5, (màquina_Word)dades_bloquejar, element_COMPT);
        if (RESULTAT <= 0) { eina_Tanca(arxiu_control_7f4cdfd5); return (uint32_t)(RESULTAT ? RESULTAT : -5); }
        Completades_quantitat += RESULTAT;
    }
    eina_Tanca(arxiu_control_7f4cdfd5); return introducció_COMPT;
}
màquina_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
màquina_Word eina_arg(màquina_Word Cerca_INDEX) {
    static const màquina_Word 빈값[1] = {0};
    if (Cerca_INDEX >= 8) return (màquina_Word)빈값;
    unsigned char 입력결과[256]; intptr_t element_COMPT;
    if (꾸러미사용중 && Cerca_INDEX == 0) { const char *dades_càrrec = 꾸러미진입클래스(); element_COMPT = 0; while (dades_càrrec[element_COMPT] && element_COMPT < 255) { 입력결과[element_COMPT] = dades_càrrec[element_COMPT]; element_COMPT++; } }
    else element_COMPT = 호출(15, Cerca_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (màquina_Word)입력결과, sizeof(입력결과));
    if (element_COMPT < 0) return (màquina_Word)빈값;
    màquina_Word *mesura_dades = 전달인수[Cerca_INDEX]; unsigned introducció_COMPT = 0;
    for (intptr_t 순번 = 0; 순번 < element_COMPT;) {
        unsigned codi_de_caràcter = 입력결과[순번++], 더있음 = codi_de_caràcter < 128 ? 0 : codi_de_caràcter >= 0xc2 && codi_de_caràcter < 0xe0 ? 1 : codi_de_caràcter < 0xf0 && codi_de_caràcter >= 0xe0 ? 2 : codi_de_caràcter >= 0xf0 && codi_de_caràcter <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > element_COMPT) { mesura_dades[++introducció_COMPT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) codi_de_caràcter &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { codi_de_caràcter = (codi_de_caràcter << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || codi_de_caràcter < 최소값 || codi_de_caràcter > 0x10ffff || (codi_de_caràcter >= 0xd800 && codi_de_caràcter <= 0xdfff)) codi_de_caràcter = 0xfffd;
        if (codi_de_caràcter >= 65536) { codi_de_caràcter -= 65536; mesura_dades[++introducció_COMPT] = 0xd800 | (codi_de_caràcter >> 10); mesura_dades[++introducció_COMPT] = 0xdc00 | (codi_de_caràcter & 1023); }
        else mesura_dades[++introducció_COMPT] = codi_de_caràcter;
    }
    mesura_dades[0] = introducció_COMPT; return (màquina_Word)mesura_dades;
}
màquina_Word 도구분류(void) { return Categoria_VALOR; }
void 커널중단(const char *알림문) {
    const char *dades_càrrec = 알림문; while (*dades_càrrec) dades_càrrec++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, dades_càrrec - 알림문); caràcter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Inici_usuari_programa(int 방식) {
    Categoria_VALOR = 방식;
    unsigned char 첫항목[256]; intptr_t element_COMPT = 호출(15, 0, (màquina_Word)첫항목, sizeof(첫항목));
    if (방식 == 2 || (방식 == 1 && element_COMPT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = 방식 == 2 ? 0 : 1;
        char arxiu_introducció_nom[256]; intptr_t durada_dades = 호출(15, 꾸러미인수이동, (màquina_Word)arxiu_introducció_nom, sizeof(arxiu_introducció_nom));
        if (durada_dades <= 0 || 꾸러미열기(arxiu_introducció_nom) < 0) {
            static const char s_ha_produït_un_error[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(s_ha_produït_un_error, sizeof(s_ha_produït_un_error) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int RESULTAT = 자바진입();
    if (대기중짝글자) caràcter(0xfffd);
    return RESULTAT;
}

// UDP는 propi 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Família, número_de_port; uint32_t Adreça; unsigned char 영값[8]; };
static struct 자바주소 UDP_ADREÇA(unsigned número_de_port) {
    struct 자바주소 첫째값 = {2, (uint16_t)((número_de_port << 8) | (número_de_port >> 8)), 0x0100007f, {0}}; return 첫째값;
}
màquina_Word eina_UDP_crear(màquina_Word número_de_port) {
    intptr_t arxiu_control_7f4cdfd5 = 호출(32, 2, 2, 17); if (arxiu_control_7f4cdfd5 < 0) return (uint32_t)arxiu_control_7f4cdfd5;
    struct 자바주소 첫째값 = UDP_ADREÇA(número_de_port);
    첫째값.Adreça = 0;
    intptr_t Estat_VALOR = 호출(33, arxiu_control_7f4cdfd5, (màquina_Word)&첫째값, sizeof(첫째값));
    if (Estat_VALOR < 0) { eina_Tanca(arxiu_control_7f4cdfd5); return (uint32_t)Estat_VALOR; }
    return arxiu_control_7f4cdfd5;
}
màquina_Word eina_UDP_enviar(màquina_Word arxiu_control_7f4cdfd5, màquina_Word número_de_port, màquina_Word MATRIU_VALOR, màquina_Word durada_VALOR) {
    const màquina_Word *원본주소 = (const màquina_Word *)MATRIU_VALOR; unsigned char dades[512];
    if (durada_VALOR > 512 || durada_VALOR > 원본주소[0]) return (uint32_t)-90;
    for (màquina_Word 순번 = 0; 순번 < durada_VALOR; 순번++) dades[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADREÇA(número_de_port);
    return (uint32_t)사용자호출(34, arxiu_control_7f4cdfd5, (màquina_Word)dades, durada_VALOR, 0, (màquina_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t element_COMPT) { return (element_COMPT>>24)|((element_COMPT>>8)&0xff00)|((element_COMPT<<8)&0xff0000)|(element_COMPT<<24); }
màquina_Word eina_UDP_enviar_ADREÇA(màquina_Word arxiu_control_7f4cdfd5, màquina_Word Adreça, màquina_Word número_de_port, màquina_Word MATRIU_VALOR, màquina_Word durada_VALOR) {
    const màquina_Word *원본주소 = (const màquina_Word *)MATRIU_VALOR; unsigned char dades[512];
    if (durada_VALOR > 512 || durada_VALOR > 원본주소[0]) return (uint32_t)-90;
    for (màquina_Word 순번 = 0; 순번 < durada_VALOR; 순번++) dades[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_ADREÇA(número_de_port); 첫째값.Adreça = 바이트순서뒤집기(Adreça);
    return (uint32_t)사용자호출(34, arxiu_control_7f4cdfd5, (màquina_Word)dades, durada_VALOR, 0, (màquina_Word)&첫째값, sizeof(첫째값));
}
màquina_Word eina_CONNECTA(màquina_Word arxiu_control_7f4cdfd5, màquina_Word Adreça, màquina_Word número_de_port) {
    struct 자바주소 첫째값 = UDP_ADREÇA(número_de_port); 첫째값.Adreça = 바이트순서뒤집기(Adreça);
    uint32_t Executa_2 = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t RESULTAT = 호출(37, arxiu_control_7f4cdfd5, (màquina_Word)&첫째값, sizeof(첫째값));
        if (RESULTAT != -115) return (uint32_t)RESULTAT;
        if ((uint32_t)(호출(7, 0, 0, 0) - Executa_2) >= 1000) return (uint32_t)-110;
    }
}
màquina_Word 도구전문받기(màquina_Word arxiu_control_7f4cdfd5, màquina_Word MATRIU_VALOR, màquina_Word memòria_intermèdia_capacitat) {
    màquina_Word *destinació_ADREÇA = (màquina_Word *)MATRIU_VALOR; unsigned char dades[512];
    if (memòria_intermèdia_capacitat > 512 || destinació_ADREÇA[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned durada_dades = sizeof(첫째값);
    intptr_t element_COMPT = 사용자호출(35, arxiu_control_7f4cdfd5, (màquina_Word)dades, memòria_intermèdia_capacitat, 0, (màquina_Word)&첫째값, (màquina_Word)&durada_dades);
    if (element_COMPT >= 0) { for (intptr_t 순번 = 0; 순번 < element_COMPT; 순번++) destinació_ADREÇA[순번 + 1] = dades[순번]; destinació_ADREÇA[513] = (첫째값.número_de_port << 8 | 첫째값.número_de_port >> 8) & 65535; destinació_ADREÇA[514] = 바이트순서뒤집기(첫째값.Adreça); }
    return (uint32_t)element_COMPT;
}
màquina_Word eina_UDP_port(màquina_Word arxiu_control_7f4cdfd5) {
    struct 자바주소 첫째값; unsigned durada_dades = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, arxiu_control_7f4cdfd5, (màquina_Word)&첫째값, (màquina_Word)&durada_dades);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.número_de_port << 8 | 첫째값.número_de_port >> 8) & 65535);
}
màquina_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
màquina_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
màquina_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
màquina_Word eina_gràfics_Espera(void) { return (uint32_t)화면키기다리기(); }
màquina_Word 도구사각형(màquina_Word X_coordenada, màquina_Word Y_coordenada, màquina_Word 너비값, màquina_Word 높이값, màquina_Word 색상) {
    return (uint32_t)사용자호출(13, X_coordenada, Y_coordenada, 색상, 너비값, 높이값, 0);
}

màquina_Word eina_flux(màquina_Word Acció,màquina_Word arxiu_control_7f4cdfd5,màquina_Word VALOR){
    if(Acció==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_ADREÇA(VALOR);
    if(Acció==1){첫째값.Adreça=0;intptr_t 반환값=호출(33,arxiu_control_7f4cdfd5,(màquina_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,arxiu_control_7f4cdfd5,4,0));}
    if(Acció==2)return (uint32_t)호출(37,arxiu_control_7f4cdfd5,(màquina_Word)&첫째값,sizeof(첫째값));
    if(Acció==3)return (uint32_t)호출(39,arxiu_control_7f4cdfd5,0,0);
    if(Acció==4)return eina_UDP_port(arxiu_control_7f4cdfd5);
    if(Acció==5)return (uint32_t)호출(40,arxiu_control_7f4cdfd5,0,0);
    return (uint32_t)-22;
}
màquina_Word eina_GUI(màquina_Word Acció,màquina_Word identificador_VALOR,màquina_Word 첫째값,màquina_Word SEGON_VALOR,màquina_Word codi_de_caràcter,màquina_Word destinació_dades){return (uint32_t)사용자호출(20,Acció,identificador_VALOR,첫째값,SEGON_VALOR,codi_de_caràcter,destinació_dades);}
màquina_Word eina_GUI_SMS(màquina_Word identificador_VALOR,màquina_Word MATRIU_VALOR,màquina_Word element_COMPT){
    const màquina_Word *원본주소=(const màquina_Word *)MATRIU_VALOR;uint32_t dades[127];unsigned introducció_COMPT=0;
    if(element_COMPT>원본주소[0])return (uint32_t)-22;
    for(màquina_Word 순번=0;순번<element_COMPT;순번++){unsigned caràcter_codificació=원본주소[순번+1];if(caràcter_codificació>=0xd800&&caràcter_codificació<=0xdbff&&순번+1<element_COMPT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;caràcter_codificació=0x10000+((caràcter_codificació-0xd800)<<10)+낮은값-0xdc00;}if(introducció_COMPT==127)return (uint32_t)-22;dades[introducció_COMPT++]=caràcter_codificació;}
    return (uint32_t)사용자호출(21,identificador_VALOR,(màquina_Word)dades,introducció_COMPT,0,0,0);
}
