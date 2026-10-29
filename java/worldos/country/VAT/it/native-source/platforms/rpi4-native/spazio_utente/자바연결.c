#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 file/uscitaTesto/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "aggregare.h"
typedef uintptr_t computer_Word;
static int Valore_categoria;
static int 꾸러미사용중, 꾸러미인수이동;
static computer_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned articolo_CONTA_NUMERI, computer_Word 첫째값, computer_Word SECONDO_VALORE, computer_Word punto_di_codice) {
    return 사용자호출(articolo_CONTA_NUMERI, 첫째값, SECONDO_VALORE, punto_di_codice, 0, 0, 0);
}
static void 바이트들(const char *dati_funzione, size_t articolo_CONTA_NUMERI) { 호출(1, 1, (computer_Word)dati_funzione, articolo_CONTA_NUMERI); }
static void carattere(unsigned punto_di_codice) {
    unsigned char dati[4]; unsigned articolo_CONTA_NUMERI = 0;
    if (punto_di_codice < 128) dati[articolo_CONTA_NUMERI++] = punto_di_codice;
    else if (punto_di_codice < 2048) { dati[articolo_CONTA_NUMERI++] = 0xc0 | (punto_di_codice >> 6); dati[articolo_CONTA_NUMERI++] = 0x80 | (punto_di_codice & 63); }
    else if (punto_di_codice < 65536) { dati[articolo_CONTA_NUMERI++] = 0xe0 | (punto_di_codice >> 12); dati[articolo_CONTA_NUMERI++] = 0x80 | ((punto_di_codice >> 6) & 63); dati[articolo_CONTA_NUMERI++] = 0x80 | (punto_di_codice & 63); }
    else { dati[articolo_CONTA_NUMERI++] = 0xf0 | (punto_di_codice >> 18); dati[articolo_CONTA_NUMERI++] = 0x80 | ((punto_di_codice >> 12) & 63); dati[articolo_CONTA_NUMERI++] = 0x80 | ((punto_di_codice >> 6) & 63); dati[articolo_CONTA_NUMERI++] = 0x80 | (punto_di_codice & 63); }
    바이트들((const char *)dati, articolo_CONTA_NUMERI);
}
computer_Word strumento_carattere(computer_Word VALORE) {
    unsigned punto_di_codice = VALORE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (punto_di_codice >= 0xdc00 && punto_di_codice <= 0xdfff) { carattere(0x10000 + ((높은부분 - 0xd800) << 10) + punto_di_codice - 0xdc00); return 1; }
        carattere(0xfffd);
    }
    if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdbff) 대기중짝글자 = punto_di_codice;
    else carattere(punto_di_codice > 0x10ffff || (punto_di_codice >= 0xdc00 && punto_di_codice <= 0xdfff) ? 0xfffd : punto_di_codice);
    return 1;
}
computer_Word strumento_stampare(computer_Word VALORE) {
    const computer_Word *stringa_dati = (const computer_Word *)VALORE;
    for (computer_Word 순번 = 0; 순번 < stringa_dati[0]; 순번++) strumento_carattere(stringa_dati[순번 + 1]);
    return stringa_dati[0];
}
static int percorso(computer_Word oggetto_fonti, char KR_dati[512]) {
    const computer_Word *첫째값 = (const computer_Word *)oggetto_fonti;
    unsigned 사용량 = 0;
    for (computer_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned punto_di_codice = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metodo_MODA 경로와 호환한다.
        if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; punto_di_codice = 0x10000 + ((punto_di_codice - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdfff) return -22;
        unsigned articolo_CONTA_NUMERI = punto_di_codice < 128 ? 1 : punto_di_codice < 2048 ? 2 : punto_di_codice < 65536 ? 3 : 4;
        if (사용량 + articolo_CONTA_NUMERI > 511) return -36;
        if (articolo_CONTA_NUMERI == 1) KR_dati[사용량++] = punto_di_codice;
        else {
            KR_dati[사용량++] = (articolo_CONTA_NUMERI == 2 ? 0xc0 : articolo_CONTA_NUMERI == 3 ? 0xe0 : 0xf0) | (punto_di_codice >> (6 * (articolo_CONTA_NUMERI - 1)));
            for (unsigned 안쪽순번 = articolo_CONTA_NUMERI - 1; 안쪽순번; 안쪽순번--) KR_dati[사용량++] = 0x80 | ((punto_di_codice >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_dati[사용량] = 0; return 사용량 ? 0 : -22;
}
computer_Word strumento_aperto(computer_Word Nome, computer_Word configurazione_BITS) {
    char dati_funzione[512]; int errore = percorso(Nome, dati_funzione);
    return (uint32_t)(errore ? errore : 호출(3, (computer_Word)dati_funzione, configurazione_BITS, 0));
}
computer_Word strumento_Chiudi(computer_Word handle_di_file) { return (uint32_t)호출(4, handle_di_file, 0, 0); }
computer_Word 도구바이트읽기(computer_Word handle_di_file) {
    unsigned char SECONDO_VALORE; intptr_t articolo_CONTA_NUMERI = 호출(2, handle_di_file, (computer_Word)&SECONDO_VALORE, 1);
    return (uint32_t)(articolo_CONTA_NUMERI == 1 ? SECONDO_VALORE : articolo_CONTA_NUMERI == 0 ? 256 : articolo_CONTA_NUMERI);
}
computer_Word strumento_scrivere_byte(computer_Word handle_di_file, computer_Word VALORE) {
    unsigned char SECONDO_VALORE = VALORE; return (uint32_t)호출(1, handle_di_file, (computer_Word)&SECONDO_VALORE, 1);
}
computer_Word 도구읽기(computer_Word Nome, computer_Word meta_dati_e_mail) {
    if (꾸러미사용중) {
        char dati_funzione[512]; int errore = percorso(Nome, dati_funzione); if (errore) return (uint32_t)errore;
        unsigned articolo_CONTA_NUMERI = 0; while (dati_funzione[articolo_CONTA_NUMERI]) articolo_CONTA_NUMERI++;
        if (articolo_CONTA_NUMERI >= 6) for (unsigned 순번 = 0; 순번 < articolo_CONTA_NUMERI - 6; 순번++) if (dati_funzione[순번] == '.') dati_funzione[순번] = '/';
        unsigned char 바이트들[16384]; computer_Word *meta_VALORE_funzione = (computer_Word *)meta_dati_e_mail;
        int RICEV_SCAD_CONTA_NUMERI = 꾸러미읽기(dati_funzione, 바이트들, meta_VALORE_funzione[0] < sizeof(바이트들) ? meta_VALORE_funzione[0] : sizeof(바이트들));
        if (RICEV_SCAD_CONTA_NUMERI >= 0) { for (int 순번 = 0; 순번 < RICEV_SCAD_CONTA_NUMERI; 순번++) meta_VALORE_funzione[순번 + 1] = 바이트들[순번]; return RICEV_SCAD_CONTA_NUMERI; }
        if (RICEV_SCAD_CONTA_NUMERI != -2) return (uint32_t)RICEV_SCAD_CONTA_NUMERI;
    }
    int handle_di_file = 꾸러미사용중 ? -2 : (int32_t)strumento_aperto(Nome, 0);
    if (handle_di_file < 0) {
        char dati_funzione[512]; int errore = percorso(Nome, dati_funzione); if (errore) return (uint32_t)errore;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Avanti_SCARTO = 자바클래스들[순번].Nome; unsigned 안쪽순번 = 0;
            while (dati_funzione[안쪽순번] && dati_funzione[안쪽순번] == Avanti_SCARTO[안쪽순번]) 안쪽순번++;
            if (dati_funzione[안쪽순번] || Avanti_SCARTO[안쪽순번]) continue;
            computer_Word *meta_VALORE_funzione = (computer_Word *)meta_dati_e_mail;
            if (meta_VALORE_funzione[0] < 자바클래스들[순번].Dimensione) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Dimensione; 안쪽순번++) meta_VALORE_funzione[안쪽순번 + 1] = 자바클래스들[순번].dati[안쪽순번];
            return 자바클래스들[순번].Dimensione;
        }
        return (uint32_t)handle_di_file;
    }
    computer_Word *첫째값 = (computer_Word *)meta_dati_e_mail;
    intptr_t Dimensione = 호출(9, handle_di_file, 0, 0), Completate_importo = 0;
    if (Dimensione < 0 || (computer_Word)Dimensione > 첫째값[0]) { strumento_Chiudi(handle_di_file); return (uint32_t)(Dimensione < 0 ? Dimensione : -27); }
    unsigned char blocco_di_dati[256];
    while (Completate_importo < Dimensione) {
        intptr_t articolo_CONTA_NUMERI = 호출(2, handle_di_file, (computer_Word)blocco_di_dati, Dimensione - Completate_importo < 256 ? Dimensione - Completate_importo : 256);
        if (articolo_CONTA_NUMERI <= 0) { strumento_Chiudi(handle_di_file); return (uint32_t)(articolo_CONTA_NUMERI ? articolo_CONTA_NUMERI : -5); }
        for (intptr_t 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) 첫째값[1 + Completate_importo + 순번] = blocco_di_dati[순번];
        Completate_importo += articolo_CONTA_NUMERI;
    }
    strumento_Chiudi(handle_di_file); return Completate_importo;
}
computer_Word strumento_scrivere(computer_Word Nome, computer_Word 원본자료, computer_Word voce_CONTA_NUMERI) {
    const computer_Word *첫째값 = (const computer_Word *)원본자료;
    if (voce_CONTA_NUMERI > 첫째값[0] || voce_CONTA_NUMERI > 16384) return (uint32_t)-27;
    int handle_di_file = (int32_t)strumento_aperto(Nome, 577); if (handle_di_file < 0) return (uint32_t)handle_di_file;
    unsigned char blocco_di_dati[256]; computer_Word Completate_importo = 0;
    while (Completate_importo < voce_CONTA_NUMERI) {
        computer_Word articolo_CONTA_NUMERI = voce_CONTA_NUMERI - Completate_importo < 256 ? voce_CONTA_NUMERI - Completate_importo : 256;
        for (computer_Word 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) blocco_di_dati[순번] = 첫째값[1 + Completate_importo + 순번];
        intptr_t risultato = 호출(1, handle_di_file, (computer_Word)blocco_di_dati, articolo_CONTA_NUMERI);
        if (risultato <= 0) { strumento_Chiudi(handle_di_file); return (uint32_t)(risultato ? risultato : -5); }
        Completate_importo += risultato;
    }
    strumento_Chiudi(handle_di_file); return voce_CONTA_NUMERI;
}
computer_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
computer_Word strumento_argomento(computer_Word CERCA_INDICE) {
    static const computer_Word vuota_VALORE[1] = {0};
    if (CERCA_INDICE >= 8) return (computer_Word)vuota_VALORE;
    unsigned char input[256]; intptr_t articolo_CONTA_NUMERI;
    if (꾸러미사용중 && CERCA_INDICE == 0) { const char *dati_funzione = 꾸러미진입클래스(); articolo_CONTA_NUMERI = 0; while (dati_funzione[articolo_CONTA_NUMERI] && articolo_CONTA_NUMERI < 255) { input[articolo_CONTA_NUMERI] = dati_funzione[articolo_CONTA_NUMERI]; articolo_CONTA_NUMERI++; } }
    else articolo_CONTA_NUMERI = 호출(15, CERCA_INDICE + (꾸러미사용중 ? 꾸러미인수이동 : 0), (computer_Word)input, sizeof(input));
    if (articolo_CONTA_NUMERI < 0) return (computer_Word)vuota_VALORE;
    computer_Word *KR_dati = 전달인수[CERCA_INDICE]; unsigned voce_CONTA_NUMERI = 0;
    for (intptr_t 순번 = 0; 순번 < articolo_CONTA_NUMERI;) {
        unsigned punto_di_codice = input[순번++], 더있음 = punto_di_codice < 128 ? 0 : punto_di_codice >= 0xc2 && punto_di_codice < 0xe0 ? 1 : punto_di_codice < 0xf0 && punto_di_codice >= 0xe0 ? 2 : punto_di_codice >= 0xf0 && punto_di_codice <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > articolo_CONTA_NUMERI) { KR_dati[++voce_CONTA_NUMERI] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) punto_di_codice &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (input[순번] & 0xc0) == 0x80) { punto_di_codice = (punto_di_codice << 6) | (input[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || punto_di_codice < 최소값 || punto_di_codice > 0x10ffff || (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdfff)) punto_di_codice = 0xfffd;
        if (punto_di_codice >= 65536) { punto_di_codice -= 65536; KR_dati[++voce_CONTA_NUMERI] = 0xd800 | (punto_di_codice >> 10); KR_dati[++voce_CONTA_NUMERI] = 0xdc00 | (punto_di_codice & 1023); }
        else KR_dati[++voce_CONTA_NUMERI] = punto_di_codice;
    }
    KR_dati[0] = voce_CONTA_NUMERI; return (computer_Word)KR_dati;
}
computer_Word strumento_Kind(void) { return Valore_categoria; }
void 커널중단(const char *informativa_SMS) {
    const char *dati_funzione = informativa_SMS; while (*dati_funzione) dati_funzione++;
    바이트들("Java tool runtime error: ", 25); 바이트들(informativa_SMS, dati_funzione - informativa_SMS); carattere(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int START_USER_app(int metodo_MODA) {
    Valore_categoria = metodo_MODA;
    unsigned char 첫항목[256]; intptr_t articolo_CONTA_NUMERI = 호출(15, 0, (computer_Word)첫항목, sizeof(첫항목));
    if (metodo_MODA == 2 || (metodo_MODA == 1 && articolo_CONTA_NUMERI == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metodo_MODA == 2 ? 0 : 1;
        char File_voce_nome[256]; intptr_t durata_dati = 호출(15, 꾸러미인수이동, (computer_Word)File_voce_nome, sizeof(File_voce_nome));
        if (durata_dati <= 0 || 꾸러미열기(File_voce_nome) < 0) {
            static const char errore[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(errore, sizeof(errore) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int risultato = 자바진입();
    if (대기중짝글자) carattere(0xfffd);
    return risultato;
}

// UDP는 nativo 커널의 SVC를 통과하며 Regolari_articolo 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t serie, numero_di_porta; uint32_t e_mail; unsigned char valore_uguale_a_zero[8]; };
static struct 자바주소 UDP_e_mail(unsigned numero_di_porta) {
    struct 자바주소 첫째값 = {2, (uint16_t)((numero_di_porta << 8) | (numero_di_porta >> 8)), 0x0100007f, {0}}; return 첫째값;
}
computer_Word strumento_UDP_aperto(computer_Word numero_di_porta) {
    intptr_t handle_di_file = 호출(32, 2, 2, 17); if (handle_di_file < 0) return (uint32_t)handle_di_file;
    struct 자바주소 첫째값 = UDP_e_mail(numero_di_porta);
    첫째값.e_mail = 0;
    intptr_t Stato_VALORE = 호출(33, handle_di_file, (computer_Word)&첫째값, sizeof(첫째값));
    if (Stato_VALORE < 0) { strumento_Chiudi(handle_di_file); return (uint32_t)Stato_VALORE; }
    return handle_di_file;
}
computer_Word strumento_UDP_inviare(computer_Word handle_di_file, computer_Word numero_di_porta, computer_Word array_VALORE, computer_Word durata_VALORE) {
    const computer_Word *원본주소 = (const computer_Word *)array_VALORE; unsigned char dati[512];
    if (durata_VALORE > 512 || durata_VALORE > 원본주소[0]) return (uint32_t)-90;
    for (computer_Word 순번 = 0; 순번 < durata_VALORE; 순번++) dati[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_e_mail(numero_di_porta);
    return (uint32_t)사용자호출(34, handle_di_file, (computer_Word)dati, durata_VALORE, 0, (computer_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t articolo_CONTA_NUMERI) { return (articolo_CONTA_NUMERI>>24)|((articolo_CONTA_NUMERI>>8)&0xff00)|((articolo_CONTA_NUMERI<<8)&0xff0000)|(articolo_CONTA_NUMERI<<24); }
computer_Word strumento_UDP_inviare_e_mail(computer_Word handle_di_file, computer_Word e_mail, computer_Word numero_di_porta, computer_Word array_VALORE, computer_Word durata_VALORE) {
    const computer_Word *원본주소 = (const computer_Word *)array_VALORE; unsigned char dati[512];
    if (durata_VALORE > 512 || durata_VALORE > 원본주소[0]) return (uint32_t)-90;
    for (computer_Word 순번 = 0; 순번 < durata_VALORE; 순번++) dati[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_e_mail(numero_di_porta); 첫째값.e_mail = 바이트순서뒤집기(e_mail);
    return (uint32_t)사용자호출(34, handle_di_file, (computer_Word)dati, durata_VALORE, 0, (computer_Word)&첫째값, sizeof(첫째값));
}
computer_Word strumento_CONNETTI(computer_Word handle_di_file, computer_Word e_mail, computer_Word numero_di_porta) {
    struct 자바주소 첫째값 = UDP_e_mail(numero_di_porta); 첫째값.e_mail = 바이트순서뒤집기(e_mail);
    uint32_t avvia = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t risultato = 호출(37, handle_di_file, (computer_Word)&첫째값, sizeof(첫째값));
        if (risultato != -115) return (uint32_t)risultato;
        if ((uint32_t)(호출(7, 0, 0, 0) - avvia) >= 1000) return (uint32_t)-110;
    }
}
computer_Word 도구전문받기(computer_Word handle_di_file, computer_Word array_VALORE, computer_Word buffer_capacità) {
    computer_Word *meta_e_mail = (computer_Word *)array_VALORE; unsigned char dati[512];
    if (buffer_capacità > 512 || meta_e_mail[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned durata_dati = sizeof(첫째값);
    intptr_t articolo_CONTA_NUMERI = 사용자호출(35, handle_di_file, (computer_Word)dati, buffer_capacità, 0, (computer_Word)&첫째값, (computer_Word)&durata_dati);
    if (articolo_CONTA_NUMERI >= 0) { for (intptr_t 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) meta_e_mail[순번 + 1] = dati[순번]; meta_e_mail[513] = (첫째값.numero_di_porta << 8 | 첫째값.numero_di_porta >> 8) & 65535; meta_e_mail[514] = 바이트순서뒤집기(첫째값.e_mail); }
    return (uint32_t)articolo_CONTA_NUMERI;
}
computer_Word strumento_UDP_porta(computer_Word handle_di_file) {
    struct 자바주소 첫째값; unsigned durata_dati = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, handle_di_file, (computer_Word)&첫째값, (computer_Word)&durata_dati);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.numero_di_porta << 8 | 첫째값.numero_di_porta >> 8) & 65535);
}
computer_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
computer_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
computer_Word strumento_schermata_altezza(void) { return (uint32_t)화면높이읽기(); }
computer_Word strumento_grafica_aspetta(void) { return (uint32_t)화면키기다리기(); }
computer_Word strumento_rettangolo(computer_Word coordinata_x, computer_Word Y_coordinata, computer_Word 너비값, computer_Word richiesto_altezza_VALORE, computer_Word 색상) {
    return (uint32_t)사용자호출(13, coordinata_x, Y_coordinata, 색상, 너비값, richiesto_altezza_VALORE, 0);
}

computer_Word strumento_Stream(computer_Word Azione,computer_Word handle_di_file,computer_Word VALORE){
    if(Azione==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_e_mail(VALORE);
    if(Azione==1){첫째값.e_mail=0;intptr_t 반환값=호출(33,handle_di_file,(computer_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,handle_di_file,4,0));}
    if(Azione==2)return (uint32_t)호출(37,handle_di_file,(computer_Word)&첫째값,sizeof(첫째값));
    if(Azione==3)return (uint32_t)호출(39,handle_di_file,0,0);
    if(Azione==4)return strumento_UDP_porta(handle_di_file);
    if(Azione==5)return (uint32_t)호출(40,handle_di_file,0,0);
    return (uint32_t)-22;
}
computer_Word strumento_GUI(computer_Word Azione,computer_Word identificatore_VALORE,computer_Word 첫째값,computer_Word SECONDO_VALORE,computer_Word punto_di_codice,computer_Word meta_dati){return (uint32_t)사용자호출(20,Azione,identificatore_VALORE,첫째값,SECONDO_VALORE,punto_di_codice,meta_dati);}
computer_Word strumento_GUI_SMS(computer_Word identificatore_VALORE,computer_Word array_VALORE,computer_Word articolo_CONTA_NUMERI){
    const computer_Word *원본주소=(const computer_Word *)array_VALORE;uint32_t dati[127];unsigned voce_CONTA_NUMERI=0;
    if(articolo_CONTA_NUMERI>원본주소[0])return (uint32_t)-22;
    for(computer_Word 순번=0;순번<articolo_CONTA_NUMERI;순번++){unsigned codifica_dei_caratteri=원본주소[순번+1];if(codifica_dei_caratteri>=0xd800&&codifica_dei_caratteri<=0xdbff&&순번+1<articolo_CONTA_NUMERI){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;codifica_dei_caratteri=0x10000+((codifica_dei_caratteri-0xd800)<<10)+낮은값-0xdc00;}if(voce_CONTA_NUMERI==127)return (uint32_t)-22;dati[voce_CONTA_NUMERI++]=codifica_dei_caratteri;}
    return (uint32_t)사용자호출(21,identificatore_VALORE,(computer_Word)dati,voce_CONTA_NUMERI,0,0,0);
}
