#include "../명명/기계연결이름.h"
#include "schermata_info.h"
// EL0 Esegui_comando computer layer_VALORE. file dati/정책은 기존 AOT Java 커널에 위임한다.
#include "spazio_utente.h"
#include "File_ABI.h"
#include "rete_ABI.h"
#include "../rete_Pila/rete_Pila.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define computer_registro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributore 0xff841000ul
#define IRQ_CPU_interfaccia 0xff842000ul
#define dimensioni_della_pagina 4096ul
#define accesso_marcatore (1ul << 10)
#define no_Esegui_privilegio (1ul << 53)
#define USER_no_Esegui (1ul << 54)
#define normale_Memoria ((1ul << 2) | (3ul << 8) | accesso_marcatore)
#define kernel_pagina (3ul | normale_Memoria | no_Esegui_privilegio | USER_no_Esegui)
#define USER_in_lettura_scrittura (3ul | normale_Memoria | (1ul << 6) | no_Esegui_privilegio | USER_no_Esegui)
#define USER_di_sola_lettura (3ul | normale_Memoria | (3ul << 6) | no_Esegui_privilegio | USER_no_Esegui)
#define 사용자읽고실행 (3ul | normale_Memoria | (3ul << 6) | no_Esegui_privilegio)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t scheda_pixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t scheda_Terminale(uintptr_t);
extern int Terminale_In_sospeso(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),schermata_SMS(int,int,const uint32_t *,unsigned);
extern void inizializzare_schermata(int),화면누름(int,unsigned);
extern int USER_CV(USER_frame *,void *);
extern void 사용자실수보관(void *);
extern int USER_immettere(uintptr_t punto_di_ingresso, uintptr_t memoria_a_pila, uintptr_t 전달값);
extern void USER_Reso(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t radice_e_mail[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t pagina_elenco[USER_pagina_CONTA_NUMERI] __attribute__((aligned(4096)));
static uint8_t Autorizzazioni_elenco[USER_pagina_CONTA_NUMERI];
static int attivo, elenco_file[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Chiudi_socket_endpoint(unsigned handle_di_file){return handle_di_file<40?자바전문닫기(handle_di_file):자바흐름닫기(handle_di_file);}
static uint64_t FREQUENZA, scadenza_time;
static uintptr_t heap_chiudere;
// kernel_VALORE 셸이 준비한 UTF-8 argomenti. EL0에는 copiare_VALORE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int in_pausa_Stato,interattivo,리눅스규약,elenco_file[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argomento_array[8][256],Autorizzazioni_elenco[USER_pagina_CONTA_NUMERI];
    uintptr_t memoria_dinamica; USER_frame esecuzione_frame;
    unsigned char virgola_mobile_Stato[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int proprietario_oggetto,interattivo;
static uint32_t numero_dell_utente[4], USER_START_time[4], 사용자누적시각[4], USER_esecuzione_time[4], Avanti_numero_dell_utente=10;
static unsigned char USER_comando_nome[4][288];
uint32_t 사용자상태읽기(unsigned voce_VALORE, unsigned INDICE) {
    unsigned funzione_INDICE=INDICE&3;
    int Stato_VALORE=(attivo && proprietario_oggetto==(int)funzione_INDICE) ? 1 : 저장값[funzione_INDICE].in_pausa_Stato ? 2 : 0;
    if (voce_VALORE==0) return Stato_VALORE;
    if (!Stato_VALORE) return 0;
    if (voce_VALORE==1) return numero_dell_utente[funzione_INDICE];
    if (voce_VALORE==2) {
        unsigned char *쪽들=Stato_VALORE==1?Autorizzazioni_elenco:저장값[funzione_INDICE].Autorizzazioni_elenco;
        unsigned pagina_CONTA_NUMERI=0; for (unsigned 순번=0; 순번<USER_pagina_CONTA_NUMERI; 순번++) if(쪽들[순번]) pagina_CONTA_NUMERI++;
        return pagina_CONTA_NUMERI*4;
    }
    if (voce_VALORE==3) return (uint32_t)보드밀리초()-USER_START_time[funzione_INDICE];
    if (voce_VALORE==4) return 사용자누적시각[funzione_INDICE]+(Stato_VALORE==1?(uint32_t)보드밀리초()-USER_esecuzione_time[funzione_INDICE]:0);
    if (voce_VALORE==5) return INDICE/4<sizeof(USER_comando_nome[0])?USER_comando_nome[funzione_INDICE][INDICE/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t voce_CONTA_NUMERI) {
    if (attivo || voce_CONTA_NUMERI > 8) return (uint32_t)-22;
    전달인수개수 = voce_CONTA_NUMERI;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t CERCA_INDICE, uintptr_t Regolari_funzione, uintptr_t byte_dati) {
    if (attivo || CERCA_INDICE >= 전달인수개수 || Regolari_funzione >= 255 || Regolari_funzione != 전달인수길이[CERCA_INDICE] || !byte_dati || byte_dati > 255)
        return (uint32_t)-22;
    전달인수[CERCA_INDICE][Regolari_funzione] = byte_dati;
    전달인수길이[CERCA_INDICE] = Regolari_funzione + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t clock_VALORE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    computer_registro(IRQ_distributore + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FREQUENZA * 2, abilitare = 1;
    scadenza_time = clock_VALORE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(abilitare) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned blocco_di_dati = 0; blocco_di_dati < 4; blocco_di_dati++) {
        radice_e_mail[blocco_di_dati] = (uintptr_t)가운데[blocco_di_dati] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t e_mail = ((uintptr_t)blocco_di_dati << 30) | ((uintptr_t)순번 << 21);
            가운데[blocco_di_dati][순번] = e_mail | 1 | accesso_marcatore | USER_no_Esegui;
            if (e_mail >= 0xfc000000ul) 가운데[blocco_di_dati][순번] |= no_Esegui_privilegio; // Device-nGnRnE
            else 가운데[blocco_di_dati][순번] |= normale_Memoria; // Normal, non-cacheable
        }
    }
    for (unsigned SECONDO_VALORE = 0; SECONDO_VALORE < USER_pagina_CONTA_NUMERI / 512; SECONDO_VALORE++)
        가운데[0][(USER_BASE >> 21) + SECONDO_VALORE] = (uintptr_t)(pagina_elenco + SECONDO_VALORE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < USER_pagina_CONTA_NUMERI; 순번++) pagina_elenco[순번] = (USER_BASE + 순번 * dimensioni_della_pagina) | kernel_pagina;
    uint64_t Memoria_attributo_registro = 0x4400, e_mail_Traduzione_controllo = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memoria_attributo_registro), "r"(e_mail_Traduzione_controllo), "r"((uintptr_t)radice_e_mail) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t virgola_mobile_Stato = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(virgola_mobile_Stato) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENZA));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 punto_di_ingresso_VALORE 때만 Consenti_VALORE.
    computer_registro(IRQ_distributore) = 0;
    computer_registro(IRQ_distributore + 0x180) = 0xffffffff;
    computer_registro(IRQ_distributore + 0x80) = 0xffffffff;
    computer_registro(IRQ_distributore + 0x280) = 1u << 30;
    computer_registro(IRQ_distributore + 0x41c) = 0x80808080;
    computer_registro(IRQ_distributore + 0x100) = 1u << 30;
    computer_registro(IRQ_CPU_interfaccia + 4) = 0xff;
    computer_registro(IRQ_CPU_interfaccia + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 reparto_IT_normale 확인할 numero 있다.
    int Sicurezza = (computer_registro(IRQ_distributore + 4) & (1u << 10)) != 0;
    computer_registro(IRQ_distributore) = Sicurezza ? 1 : 3;
    computer_registro(IRQ_CPU_interfaccia) = Sicurezza ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TIPO_area, computer_TIPO; uint32_t numero_di_versione;
    uint64_t punto_di_ingresso, app_Intestazione_SCARTO, intestazione_della_sezione_SCARTO; uint32_t configurazione_BITS;
    uint16_t eseguibile_Intestazione_ridimensionare, app_Intestazione_voce_ridimensionare, app_Intestazione_CONTA_NUMERI, intestazione_della_sezione_voce_ridimensionare, intestazione_della_sezione_CONTA_NUMERI, sezione_nome_tabella_INDICE;
} 실행파일머리;
typedef struct { uint32_t TIPO_area, configurazione_BITS; uint64_t SCARTO_VALORE, e_mail, fisico_e_mail, 파일영역크기, 기억영역크기, allineare_limite; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(USER_frame) == 272, "exception assembly layout");
static int 포함된범위(uint64_t SCARTO_VALORE, uint64_t Dimensione, uint64_t chiudere_SCARTO) {
    return SCARTO_VALORE <= chiudere_SCARTO && Dimensione <= chiudere_SCARTO - SCARTO_VALORE;
}
static int 부가정보검사(const unsigned char *dati_funzione, size_t Dimensione) {
    size_t Regolari_funzione = 0;
    while (포함된범위(Regolari_funzione, 12, Dimensione)) {
        uint32_t 낱말들[3]; memcpy(낱말들, dati_funzione + Regolari_funzione, 12); Regolari_funzione += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(Regolari_funzione, 이름영역크기, Dimensione) || !포함된범위(Regolari_funzione + 이름영역크기, 설명크기, Dimensione)) return 0;
        const unsigned char Nome[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nome) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nome); 순번++) if (dati_funzione[Regolari_funzione + 순번] != Nome[순번]) 일치 = 0;
        uint32_t numero_di_versione = 0;
        if (일치) memcpy(&numero_di_versione, dati_funzione + Regolari_funzione + 이름영역크기, 4);
        if (일치 && numero_di_versione == 1) return 1;
        Regolari_funzione += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *dati, size_t Dimensione, int 리눅스방식) {
    if (Dimensione < sizeof(실행파일머리)) return USER_eseguibile_errore;
    실행파일머리 eseguibile_Intestazione; memcpy(&eseguibile_Intestazione, dati, sizeof(eseguibile_Intestazione));
    if (eseguibile_Intestazione.형식식별[0] != 127 || eseguibile_Intestazione.형식식별[1] != 'E' || eseguibile_Intestazione.형식식별[2] != 'L' || eseguibile_Intestazione.형식식별[3] != 'F' ||
        eseguibile_Intestazione.형식식별[4] != 2 || eseguibile_Intestazione.형식식별[5] != 1 || eseguibile_Intestazione.형식식별[6] != 1 || (eseguibile_Intestazione.형식식별[7] != 0 && (!리눅스방식 || eseguibile_Intestazione.형식식별[7] != 3)) ||
        eseguibile_Intestazione.TIPO_area != 2 || eseguibile_Intestazione.computer_TIPO != 183 || eseguibile_Intestazione.numero_di_versione != 1 || eseguibile_Intestazione.configurazione_BITS || eseguibile_Intestazione.eseguibile_Intestazione_ridimensionare != sizeof(eseguibile_Intestazione) ||
        eseguibile_Intestazione.app_Intestazione_voce_ridimensionare != sizeof(실행파일구획) || !eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI || eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI > 16 ||
        eseguibile_Intestazione.app_Intestazione_SCARTO < sizeof(eseguibile_Intestazione) || !포함된범위(eseguibile_Intestazione.app_Intestazione_SCARTO, (uint64_t)eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI * sizeof(실행파일구획), Dimensione)) return USER_eseguibile_errore;
    uint8_t 사용량[(USER_foto_chiudere - USER_BASE) / dimensioni_della_pagina] = {0};
    int valido_punto_di_ingresso = 0, ABI_OK = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI; 순번++) {
        실행파일구획 dati_funzione; memcpy(&dati_funzione, dati + eseguibile_Intestazione.app_Intestazione_SCARTO + 순번 * sizeof(dati_funzione), sizeof(dati_funzione));
        if (dati_funzione.TIPO_area == 4) {
            if (!포함된범위(dati_funzione.SCARTO_VALORE, dati_funzione.파일영역크기, Dimensione)) return USER_eseguibile_errore;
            if (부가정보검사(dati + dati_funzione.SCARTO_VALORE, dati_funzione.파일영역크기)) ABI_OK = 1;
            continue;
        }
        if (dati_funzione.TIPO_area == 0 || dati_funzione.TIPO_area == 6 || (dati_funzione.TIPO_area == 0x6474e551 && !(dati_funzione.configurazione_BITS & 1))) continue;
        if (dati_funzione.TIPO_area != 1) return USER_eseguibile_errore; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!dati_funzione.기억영역크기) continue;
        if (dati_funzione.configurazione_BITS & ~7u || !(dati_funzione.configurazione_BITS & 4) || (dati_funzione.configurazione_BITS & 3) == 3 || dati_funzione.파일영역크기 > dati_funzione.기억영역크기 ||
            (dati_funzione.파일영역크기 && !포함된범위(dati_funzione.SCARTO_VALORE, dati_funzione.파일영역크기, Dimensione)) || dati_funzione.e_mail < USER_BASE ||
            !포함된범위(dati_funzione.e_mail, dati_funzione.기억영역크기, USER_foto_chiudere) ||
            (!리눅스방식 && ((dati_funzione.e_mail & (dimensioni_della_pagina - 1)) || (dati_funzione.SCARTO_VALORE & (dimensioni_della_pagina - 1)) || dati_funzione.allineare_limite != dimensioni_della_pagina)) ||
            (리눅스방식 && (((dati_funzione.e_mail ^ dati_funzione.SCARTO_VALORE) & (dimensioni_della_pagina - 1)) || !dati_funzione.allineare_limite ||
                (dati_funzione.allineare_limite & (dati_funzione.allineare_limite - 1)) || dati_funzione.allineare_limite > 0x200000 || ((dati_funzione.e_mail ^ dati_funzione.SCARTO_VALORE) & (dati_funzione.allineare_limite - 1))))) return USER_eseguibile_errore;
        unsigned 첫항목 = (dati_funzione.e_mail - USER_BASE) / dimensioni_della_pagina;
        unsigned voce_CONTA_NUMERI = ((dati_funzione.e_mail & (dimensioni_della_pagina - 1)) + dati_funzione.기억영역크기 + dimensioni_della_pagina - 1) / dimensioni_della_pagina;
        for (unsigned pagina_VALORE = 첫항목; pagina_VALORE < 첫항목 + voce_CONTA_NUMERI; pagina_VALORE++) {
            if (사용량[pagina_VALORE]) return USER_eseguibile_errore;
            사용량[pagina_VALORE] = 1;
        }
        if ((dati_funzione.configurazione_BITS & 1) && eseguibile_Intestazione.punto_di_ingresso >= dati_funzione.e_mail && eseguibile_Intestazione.punto_di_ingresso < dati_funzione.e_mail + dati_funzione.파일영역크기 && !(eseguibile_Intestazione.punto_di_ingresso & 3)) valido_punto_di_ingresso = 1;
        적재구획++;
    }
    return valido_punto_di_ingresso && (리눅스방식 ? !ABI_OK : ABI_OK) && 적재구획 ? 0 : USER_eseguibile_errore;
}
int 사용자실행파일검사(const unsigned char *dati, size_t Dimensione) { return 실행파일검사(dati, Dimensione, 0); }
static void layout_di_pagina(uintptr_t e_mail, uint64_t configurazione_BITS, unsigned autorizzazioni) {
    unsigned CERCA_INDICE = (e_mail - USER_BASE) / dimensioni_della_pagina;
    pagina_elenco[CERCA_INDICE] = e_mail | configurazione_BITS;
    Autorizzazioni_elenco[CERCA_INDICE] = autorizzazioni;
}
static int USER_intervallo(uintptr_t e_mail, size_t voce_CONTA_NUMERI, int 쓰는중) {
    if (e_mail < USER_BASE || !포함된범위(e_mail, voce_CONTA_NUMERI, USER_chiudere)) return 0;
    if (!voce_CONTA_NUMERI) return 1;
    unsigned 첫항목 = (e_mail - USER_BASE) / dimensioni_della_pagina, 마지막 = (e_mail + voce_CONTA_NUMERI - 1 - USER_BASE) / dimensioni_della_pagina;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Autorizzazioni_elenco[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int copiare_percorso(uintptr_t e_mail, char *percorso) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!USER_intervallo(e_mail, 1, 0)) return -14;
        percorso[순번] = *(const char *)e_mail++;
        if (!percorso[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_KR(intptr_t risultato) { return risultato < 0 ? -numero_errore : risultato; }
static int 대응파일기술자(uint64_t handle_di_file) { return handle_di_file >= 3 && handle_di_file < 19 ? elenco_file[handle_di_file - 3] : -1; }
static int socket_endpoint_proprietario(uint64_t handle_di_file) { return handle_di_file >= 32 && handle_di_file < 56 && 통신끝점들[handle_di_file - 32]; }
static int e_mail_input(uintptr_t 가리킴값, size_t durata_VALORE, struct pk_sockaddr_in *e_mail) {
    if (durata_VALORE != sizeof(*e_mail)) return -22;
    if (!USER_intervallo(가리킴값, durata_VALORE, 0)) return -14;
    memcpy(e_mail, (const void *)가리킴값, sizeof(*e_mail));
    return e_mail->sin_family == AF_INET ? 0 : -97;
}
static int e_mail_output_assegno(uintptr_t 가리킴값, uintptr_t durata_puntatore, pk_socklen_t *buffer_capacità) {
    if (!USER_intervallo(durata_puntatore, sizeof(*buffer_capacità), 1)) return -14;
    memcpy(buffer_capacità, (const void *)durata_puntatore, sizeof(*buffer_capacità));
    if (*buffer_capacità > sizeof(struct pk_sockaddr_in)) *buffer_capacità = sizeof(struct pk_sockaddr_in);
    if (*buffer_capacità && !USER_intervallo(가리킴값, *buffer_capacità, 1)) return -14;
    return 0;
}
static void e_mail_output(uintptr_t 가리킴값, uintptr_t durata_puntatore, pk_socklen_t buffer_capacità, int e_mail, int numero_di_porta) {
    struct pk_sockaddr_in VALORE; memset(&VALORE, 0, sizeof(VALORE));
    VALORE.sin_family = AF_INET; VALORE.sin_port = pk_htons(numero_di_porta); VALORE.sin_addr.s_addr = pk_htonl(e_mail);
    if (buffer_capacità) memcpy((void *)가리킴값, &VALORE, buffer_capacità);
    pk_socklen_t durata_VALORE = sizeof(VALORE); memcpy((void *)durata_puntatore, &durata_VALORE, sizeof(durata_VALORE));
}
extern uintptr_t scheda_Canale(uintptr_t, uintptr_t);
static intptr_t nativo_Sistema_Chiama(USER_frame *File_voce) {
    uintptr_t 첫째값 = File_voce->registro_dati[0], SECONDO_VALORE = File_voce->registro_dati[1], punto_di_codice = File_voce->registro_dati[2];
    char percorso[65];
    int handle_di_file, risultato;
    switch (File_voce->registro_dati[8]) {
    case 0: return 1; // nativo ABI 버전
    case 1: // write: puntatore 전체를 검사한 BACK_VALORE uscitaTesto/file cambiare_VALORE
        if (punto_di_codice > 65536) return -22;
        if (!USER_intervallo(SECONDO_VALORE, punto_di_codice, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_output=clock_VALORE();
            for (size_t 순번 = 0; 순번 < punto_di_codice; 순번++) scheda_Canale(첫째값, ((const unsigned char *)SECONDO_VALORE)[순번]);
            /* 큰 tty를 그린 kernel_VALORE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interattivo){
                scadenza_time+=clock_VALORE()-START_output;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(scadenza_time) : "memory");
            }
            return punto_di_codice;
        }
        if(첫째값>=40&&socket_endpoint_proprietario(첫째값)){
            size_t articolo_CONTA_NUMERI=punto_di_codice>512?512:punto_di_codice;for(size_t 순번=0;순번<articolo_CONTA_NUMERI;순번++)자바전문넣기(순번,((const unsigned char *)SECONDO_VALORE)[순번]);return 자바흐름쓰기(첫째값,articolo_CONTA_NUMERI);
        }
        handle_di_file = 대응파일기술자(첫째값); if (handle_di_file < 0) return -9;
        return kernel_KR(pk_write(handle_di_file, (const void *)SECONDO_VALORE, punto_di_codice));
    case 2:
        if (punto_di_codice > 65536) return -22;
        if (!USER_intervallo(SECONDO_VALORE, punto_di_codice, 1)) return -14;
        if (첫째값 == 0) {
            size_t articolo_CONTA_NUMERI = 0;
            while (articolo_CONTA_NUMERI < punto_di_codice) {
                int carattere_VALORE = (int32_t)보드글자읽기(); if (carattere_VALORE == -2) return articolo_CONTA_NUMERI; if (carattere_VALORE < 0) break;
                ((unsigned char *)SECONDO_VALORE)[articolo_CONTA_NUMERI++] = carattere_VALORE;
            }
            return articolo_CONTA_NUMERI ? (intptr_t)articolo_CONTA_NUMERI : (punto_di_codice ? -11 : 0);
        }
        if(첫째값>=40&&socket_endpoint_proprietario(첫째값)){
            risultato=자바흐름읽기(첫째값,punto_di_codice>512?512:punto_di_codice);if(risultato>0)for(int 순번=0;순번<risultato;순번++)((unsigned char *)SECONDO_VALORE)[순번]=자바전문얻기(순번);return risultato;
        }
        handle_di_file = 대응파일기술자(첫째값); if (handle_di_file < 0) return -9;
        return kernel_KR(pk_read(handle_di_file, (void *)SECONDO_VALORE, punto_di_codice));
    case 3:
        risultato = copiare_percorso(첫째값, percorso); if (risultato) return risultato;
        if (SECONDO_VALORE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (elenco_file[순번] < 0) {
            handle_di_file = pk_open(percorso, (int)SECONDO_VALORE, 0600);
            if (handle_di_file < 0) return -numero_errore;
            elenco_file[순번] = handle_di_file; return 순번 + 3;
        }
        return -24;
    case 4:
        if (socket_endpoint_proprietario(첫째값)) { risultato = Chiudi_socket_endpoint(첫째값); if (!risultato) 통신끝점들[첫째값 - 32] = 0; return risultato; }
        handle_di_file = 대응파일기술자(첫째값); if (handle_di_file < 0) return -9;
        risultato = pk_close(handle_di_file); if (!risultato) elenco_file[첫째값 - 3] = -1;
        return kernel_KR(risultato);
    case 5:
        handle_di_file = 대응파일기술자(첫째값); if (handle_di_file < 0) return -9;
        if (punto_di_codice > 2) return -22;
        return kernel_KR(pk_lseek(handle_di_file, (int64_t)SECONDO_VALORE, punto_di_codice));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 spazio_utente RW/NX heap_VALORE, 새로 노출되는 페이지는 0으로 inizializza
        if (!첫째값) return heap_chiudere;
        if (첫째값 < USER_foto_chiudere || 첫째값 > USER_heap_chiudere) return -12;
        uintptr_t 이전쪽들 = (heap_chiudere + dimensioni_della_pagina - 1) & ~(dimensioni_della_pagina - 1);
        uintptr_t 새쪽들 = (첫째값 + dimensioni_della_pagina - 1) & ~(dimensioni_della_pagina - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t dati_funzione = 이전쪽들; dati_funzione < 새쪽들; dati_funzione += dimensioni_della_pagina) layout_di_pagina(dati_funzione, kernel_pagina, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t dati_funzione = 이전쪽들; dati_funzione < 새쪽들; dati_funzione += dimensioni_della_pagina) layout_di_pagina(dati_funzione, USER_in_lettura_scrittura, 3);
        } else {
            for (uintptr_t dati_funzione = 새쪽들; dati_funzione < 이전쪽들; dati_funzione += dimensioni_della_pagina) {
                pagina_elenco[(dati_funzione - USER_BASE) / dimensioni_della_pagina] = 0; Autorizzazioni_elenco[(dati_funzione - USER_BASE) / dimensioni_della_pagina] = 0;
            }
        }
        heap_chiudere = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        handle_di_file = 대응파일기술자(첫째값); return handle_di_file < 0 ? -9 : kernel_KR(pk_size(handle_di_file));
    case 10:
        handle_di_file = 대응파일기술자(첫째값); return handle_di_file < 0 ? -9 : kernel_KR(pk_ftruncate(handle_di_file, (int64_t)SECONDO_VALORE));
    case 11:
        risultato = copiare_percorso(첫째값, percorso); return risultato ? risultato : kernel_KR(pk_unlink(percorso));
    case 12:
        handle_di_file = 대응파일기술자(첫째값); return handle_di_file < 0 ? -9 : kernel_KR(pk_fsync(handle_di_file));
    case 13: { // 그래픽 기초 API: spazio_utente 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = File_voce->registro_dati[3], richiesto_altezza_VALORE = File_voce->registro_dati[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), schermata_durata = scheda_schermata_altezza();
        if (첫째값 > 화면폭 || SECONDO_VALORE > schermata_durata || 너비값 > 화면폭 - 첫째값 || richiesto_altezza_VALORE > schermata_durata - SECONDO_VALORE) return -22;
        for (uintptr_t Y_coordinata = SECONDO_VALORE; Y_coordinata < SECONDO_VALORE + richiesto_altezza_VALORE; Y_coordinata++) for (uintptr_t coordinata_x = 첫째값; coordinata_x < 첫째값 + 너비값; coordinata_x++) scheda_pixel(coordinata_x, Y_coordinata, punto_di_codice);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=articolo_CONTA_NUMERI; args(index,buffer,capacity)=UTF-8 durata_VALORE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (punto_di_codice <= 전달인수길이[첫째값]) return -36;
        if (!USER_intervallo(SECONDO_VALORE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECONDO_VALORE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interattivo=1;return scheda_Terminale(13);}
        if(첫째값==2){interattivo=0;return 0;}
        if(첫째값==3)return scheda_Terminale(13);
        if(첫째값!=1||!interattivo)return -22;
        risultato=(int32_t)보드글자읽기();
        if(risultato==-4096)return risultato;
        START_TIMEOUT();return risultato<0?-11:risultato;
    case 17: { // 유한한 협력 aspetta_VALORE: comunicazione 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t chiudere_time = clock_VALORE() + FREQUENZA * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (clock_VALORE() < chiudere_time);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 padre_VALORE·빈 폴더를 검사한다.
        if (SECONDO_VALORE > 2) return -22;
        risultato = copiare_percorso(첫째값, percorso); if (risultato) return risultato;
        unsigned durata_VALORE = 0; while (percorso[durata_VALORE]) durata_VALORE++;
        risultato = 자바경로시작(durata_VALORE); if (risultato < 0) return risultato;
        for (unsigned 순번 = 0; 순번 < durata_VALORE; 순번++) 자바경로바이트(순번, (unsigned char)percorso[순번]);
        return SECONDO_VALORE == 0 ? 자바항목종류() : SECONDO_VALORE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int carattere_VALORE=(int32_t)보드글자읽기();if(carattere_VALORE==-4096)return carattere_VALORE;if(carattere_VALORE>=0)화면누름(proprietario_oggetto,carattere_VALORE);START_TIMEOUT();}
        if(첫째값==3&&punto_di_codice){if(!자바셸대화형())return -95;interattivo=1;scheda_Terminale(300);}
        return 화면호출(proprietario_oggetto,첫째값,SECONDO_VALORE,punto_di_codice,File_voce->registro_dati[3],File_voce->registro_dati[4],File_voce->registro_dati[5]);
    case 21:
        if(punto_di_codice>127)return -22;if(!USER_intervallo(SECONDO_VALORE,punto_di_codice*sizeof(uint32_t),0))return -14;
        return schermata_SMS(proprietario_oggetto,첫째값,(const uint32_t *)SECONDO_VALORE,punto_di_codice);
    case 22: // schermata Dimensione query_VALORE: 0=너비, 1=altezza_VALORE. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : scheda_schermata_altezza();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECONDO_VALORE==SOCK_STREAM&&(punto_di_codice==0||punto_di_codice==6))risultato=자바흐름만들기();
        else if(SECONDO_VALORE==SOCK_DGRAM&&(punto_di_codice==0||punto_di_codice==IPPROTO_UDP))risultato=자바전문만들기(첫째값,SECONDO_VALORE,punto_di_codice);
        else return -93;
        if (risultato >= 32 && risultato < 56) 통신끝점들[risultato - 32] = 1;
        return risultato;
    case 33: {
        if (!socket_endpoint_proprietario(첫째값)) return -9;
        struct pk_sockaddr_in e_mail;
        risultato = e_mail_input(SECONDO_VALORE, punto_di_codice, &e_mail); if (risultato) return risultato;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(e_mail.sin_addr.s_addr),pk_htons(e_mail.sin_port)):자바전문묶기(첫째값, pk_htonl(e_mail.sin_addr.s_addr), pk_htons(e_mail.sin_port));
    }
    case 34: {
        if (!socket_endpoint_proprietario(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (File_voce->registro_dati[3]) return -95;
        if (punto_di_codice > 512) return -90;
        if (punto_di_codice && !USER_intervallo(SECONDO_VALORE, punto_di_codice, 0)) return -14;
        struct pk_sockaddr_in e_mail;
        risultato = e_mail_input(File_voce->registro_dati[4], File_voce->registro_dati[5], &e_mail); if (risultato) return risultato;
        for (unsigned 순번 = 0; 순번 < punto_di_codice; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECONDO_VALORE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(e_mail.sin_addr.s_addr), pk_htons(e_mail.sin_port), punto_di_codice);
    }
    case 35: {
        if (!socket_endpoint_proprietario(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (File_voce->registro_dati[3]) return -95;
        if (punto_di_codice > 512) return -90;
        if (punto_di_codice && !USER_intervallo(SECONDO_VALORE, punto_di_codice, 1)) return -14;
        pk_socklen_t buffer_capacità = 0;
        if (File_voce->registro_dati[4]) { risultato = e_mail_output_assegno(File_voce->registro_dati[4], File_voce->registro_dati[5], &buffer_capacità); if (risultato) return risultato; }
        risultato = 자바전문받기(첫째값, punto_di_codice); if (risultato < 0) return risultato;
        for (int 순번 = 0; 순번 < risultato; 순번++) ((unsigned char *)SECONDO_VALORE)[순번] = 자바전문얻기(순번);
        if (File_voce->registro_dati[4]) e_mail_output(File_voce->registro_dati[4], File_voce->registro_dati[5], buffer_capacità, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return risultato;
    }
    case 36: {
        if (!socket_endpoint_proprietario(첫째값)) return -9;
        pk_socklen_t buffer_capacità;
        risultato = e_mail_output_assegno(SECONDO_VALORE, punto_di_codice, &buffer_capacità); if (risultato) return risultato;
        e_mail_output(SECONDO_VALORE,punto_di_codice,buffer_capacità,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!socket_endpoint_proprietario(첫째값))return -9;struct pk_sockaddr_in e_mail;
        risultato=e_mail_input(SECONDO_VALORE,punto_di_codice,&e_mail);if(risultato)return risultato;
        return 자바흐름연결(첫째값,pk_htonl(e_mail.sin_addr.s_addr),pk_htons(e_mail.sin_port));
    }
    case 38: return 첫째값>=40&&socket_endpoint_proprietario(첫째값)?자바흐름듣기(첫째값,SECONDO_VALORE):-9;
    case 39:
        if(첫째값<40||!socket_endpoint_proprietario(첫째값))return -9;
        if(SECONDO_VALORE||punto_di_codice)return -95;risultato=자바흐름연결받기(첫째값);if(risultato>=40&&risultato<56)통신끝점들[risultato-32]=1;return risultato;
    case 40: return 첫째값>=40&&socket_endpoint_proprietario(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t chiamata_di_sistema(USER_frame *File_voce) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(File_voce) : nativo_Sistema_Chiama(File_voce);
}
static void Reso_kernel(USER_frame *File_voce, int risultato) {
    Stop_TIMEOUT();
    File_voce->registro_dati[0] = (uint64_t)(int64_t)risultato;
    File_voce->comando_funzione = (uintptr_t)USER_Reso;
    File_voce->codice_di_stato = 0x3c5; // EL1h, DAIF masked
}
int eccezione_utente(USER_frame *File_voce, unsigned INTERCETTA) {
    if (!attivo || (File_voce->codice_di_stato & 15) != 0) return 0;
    if (INTERCETTA) {
        uint32_t accettazione_VALORE = computer_registro(IRQ_CPU_interfaccia + 0xc), identificatore_VALORE = accettazione_VALORE & 1023;
        if (identificatore_VALORE == 30) { Reso_kernel(File_voce, USER_TIMEOUT); computer_registro(IRQ_CPU_interfaccia + 0x10) = accettazione_VALORE; return 1; }
        if (identificatore_VALORE < 1020) computer_registro(IRQ_CPU_interfaccia + 0x10) = accettazione_VALORE;
        return 1;
    }
    uint64_t eccezione_Stato; __asm__ volatile("mrs %0, esr_el1" : "=r"(eccezione_Stato));
    if (clock_VALORE() >= scadenza_time) { Reso_kernel(File_voce, USER_TIMEOUT); return 1; }
    unsigned eccezione_area = eccezione_Stato >> 26;
    if (eccezione_area == 0x15 && (eccezione_Stato & 0xffff) == 0) {
        if (리눅스규약 ? File_voce->registro_dati[8] == 93 || File_voce->registro_dati[8] == 94 : File_voce->registro_dati[8] == 6) Reso_kernel(File_voce, (int)(File_voce->registro_dati[0] & 255));
        else {
            intptr_t risultato=chiamata_di_sistema(File_voce);
            if(risultato==-4096&&interattivo){
                저장값[proprietario_oggetto].esecuzione_frame=*File_voce;저장값[proprietario_oggetto].esecuzione_frame.comando_funzione-=4;
                사용자실수보관(저장값[proprietario_oggetto].virgola_mobile_Stato);Reso_kernel(File_voce,사용자중단됨);
            }else File_voce->registro_dati[0]=(uint64_t)risultato;
        }
    } else Reso_kernel(File_voce, eccezione_area == 0x24 ? USER_dati_errore : eccezione_area == 0x20 ? USER_esecuzione_errore : USER_non_valida_istruzione);
    return 1;
}

// 생성된 const ELF gruppo_VALORE: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *dati; size_t Dimensione; unsigned 전달값; } app;
#include "programs.h"
static void *snapshot(unsigned funzione_INDICE){return (void *)(0x04000000ul+funzione_INDICE*(USER_chiudere-USER_BASE));}
static int Fine_app(int risultato){
    사용자누적시각[proprietario_oggetto]+=(uint32_t)보드밀리초()-USER_esecuzione_time[proprietario_oggetto];
    Stop_TIMEOUT();attivo=0;
    if(risultato==사용자중단됨){
        저장된작업 *stringa_dati=&저장값[proprietario_oggetto];stringa_dati->in_pausa_Stato=1;stringa_dati->interattivo=interattivo;stringa_dati->리눅스규약=리눅스규약;stringa_dati->memoria_dinamica=heap_chiudere;stringa_dati->인수개수=전달인수개수;
        memcpy(stringa_dati->Autorizzazioni_elenco,Autorizzazioni_elenco,sizeof(Autorizzazioni_elenco));memcpy(stringa_dati->elenco_file,elenco_file,sizeof(elenco_file));memcpy(stringa_dati->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(stringa_dati->argomento_array,전달인수,sizeof(전달인수));memcpy(stringa_dati->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<USER_pagina_CONTA_NUMERI;순번++)if(Autorizzazioni_elenco[순번])memcpy((unsigned char *)snapshot(proprietario_oggetto)+순번*dimensioni_della_pagina,(void *)(USER_BASE+순번*dimensioni_della_pagina),dimensioni_della_pagina);
    }else{
        저장값[proprietario_oggetto].in_pausa_Stato=0;inizializzare_schermata(proprietario_oggetto);
        for(unsigned 순번=0;순번<16;순번++)if(elenco_file[순번]>=0)pk_close(elenco_file[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Chiudi_socket_endpoint(순번+32);
    }
    for(unsigned 순번=0;순번<USER_pagina_CONTA_NUMERI;순번++){pagina_elenco[순번]=0;Autorizzazioni_elenco[순번]=0;}변환표맞추기();return risultato;
}
uintptr_t scheda_controllo_utente(uintptr_t Azione){
    unsigned funzione_INDICE=Azione&15;if(funzione_INDICE>=4||attivo)return (uint32_t)-22;
    저장된작업 *stringa_dati=&저장값[funzione_INDICE];
    if(Azione>=32){if(stringa_dati->in_pausa_Stato){for(unsigned 순번=0;순번<16;순번++)if(stringa_dati->elenco_file[순번]>=0)pk_close(stringa_dati->elenco_file[순번]);for(unsigned 순번=0;순번<24;순번++)if(stringa_dati->통신끝점들[순번])Chiudi_socket_endpoint(순번+32);}stringa_dati->in_pausa_Stato=0;inizializzare_schermata(funzione_INDICE);return 0;}
    if(Azione>=16)return stringa_dati->in_pausa_Stato;
    if(!stringa_dati->in_pausa_Stato)return (uint32_t)-22;
    proprietario_oggetto=funzione_INDICE;interattivo=stringa_dati->interattivo;리눅스규약=stringa_dati->리눅스규약;heap_chiudere=stringa_dati->memoria_dinamica;전달인수개수=stringa_dati->인수개수;
    memcpy(elenco_file,stringa_dati->elenco_file,sizeof(elenco_file));memcpy(통신끝점들,stringa_dati->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,stringa_dati->argomento_array,sizeof(전달인수));memcpy(전달인수길이,stringa_dati->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<USER_pagina_CONTA_NUMERI;순번++)pagina_elenco[순번]=(USER_BASE+순번*dimensioni_della_pagina)|kernel_pagina;변환표맞추기();
    memset((void *)USER_BASE,0,USER_chiudere-USER_BASE);
    for(unsigned 순번=0;순번<USER_pagina_CONTA_NUMERI;순번++)if(stringa_dati->Autorizzazioni_elenco[순번])memcpy((void *)(USER_BASE+순번*dimensioni_della_pagina),(unsigned char *)snapshot(funzione_INDICE)+순번*dimensioni_della_pagina,dimensioni_della_pagina);
    memcpy(Autorizzazioni_elenco,stringa_dati->Autorizzazioni_elenco,sizeof(Autorizzazioni_elenco));
    for(unsigned 순번=0;순번<USER_pagina_CONTA_NUMERI;순번++){unsigned dati_funzione=Autorizzazioni_elenco[순번];pagina_elenco[순번]=dati_funzione?(USER_BASE+순번*dimensioni_della_pagina)|(dati_funzione==3?USER_in_lettura_scrittura:dati_funzione==5?사용자읽고실행:USER_di_sola_lettura):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");attivo=1;stringa_dati->in_pausa_Stato=0;START_TIMEOUT();
    USER_esecuzione_time[proprietario_oggetto]=보드밀리초();
    return (uint32_t)Fine_app(USER_CV(&stringa_dati->esecuzione_frame,stringa_dati->virgola_mobile_Stato));
}
static int eseguire_app(const unsigned char *dati, size_t Dimensione, unsigned 전달값, int 리눅스방식, const char *Nome) {
    if (attivo) return -16;
    proprietario_oggetto=scheda_Terminale(11);if(proprietario_oggetto<0||proprietario_oggetto>3||저장값[proprietario_oggetto].in_pausa_Stato)return -16;interattivo=0;
    int valido = 실행파일검사(dati, Dimensione, 리눅스방식); if (valido) return valido;
    리눅스규약 = 리눅스방식;
    unsigned nome_INDICE=0;
    while (*Nome && nome_INDICE<31) USER_comando_nome[proprietario_oggetto][nome_INDICE++]=(unsigned char)*Nome++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nome_INDICE) USER_comando_nome[proprietario_oggetto][nome_INDICE++]=' ';
        for (unsigned funzione_INDICE=0; funzione_INDICE<전달인수길이[0]; funzione_INDICE++) USER_comando_nome[proprietario_oggetto][nome_INDICE++]=전달인수[0][funzione_INDICE];
    }
    USER_comando_nome[proprietario_oggetto][nome_INDICE]=0; numero_dell_utente[proprietario_oggetto]=Avanti_numero_dell_utente++;
    if (Avanti_numero_dell_utente>0x7fffffffu) Avanti_numero_dell_utente=10;
    USER_START_time[proprietario_oggetto]=보드밀리초(); 사용자누적시각[proprietario_oggetto]=0;
    for (unsigned 순번 = 0; 순번 < USER_pagina_CONTA_NUMERI; 순번++) pagina_elenco[순번] = (USER_BASE + 순번 * dimensioni_della_pagina) | kernel_pagina;
    변환표맞추기();
    memset((void *)USER_BASE, 0, USER_chiudere - USER_BASE);
    memset(Autorizzazioni_elenco, 0, sizeof(Autorizzazioni_elenco));
    실행파일머리 eseguibile_Intestazione; memcpy(&eseguibile_Intestazione, dati, sizeof(eseguibile_Intestazione));
    for (unsigned 순번 = 0; 순번 < eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI; 순번++) {
        실행파일구획 dati_funzione; memcpy(&dati_funzione, dati + eseguibile_Intestazione.app_Intestazione_SCARTO + 순번 * sizeof(dati_funzione), sizeof(dati_funzione));
        if (dati_funzione.TIPO_area != 1 || !dati_funzione.기억영역크기) continue;
        if (dati_funzione.파일영역크기) memcpy((void *)(uintptr_t)dati_funzione.e_mail, dati + dati_funzione.SCARTO_VALORE, dati_funzione.파일영역크기);
        for (uintptr_t Regolari_funzione = dati_funzione.e_mail & ~(dimensioni_della_pagina - 1); Regolari_funzione < dati_funzione.e_mail + dati_funzione.기억영역크기; Regolari_funzione += dimensioni_della_pagina) {
            Autorizzazioni_elenco[(Regolari_funzione - USER_BASE) / dimensioni_della_pagina] = (dati_funzione.configurazione_BITS & 2) ? 3 : ((dati_funzione.configurazione_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t Regolari_funzione = USER_Pila_e_mail; Regolari_funzione < USER_chiudere; Regolari_funzione += dimensioni_della_pagina) Autorizzazioni_elenco[(Regolari_funzione - USER_BASE) / dimensioni_della_pagina] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(eseguibile_Intestazione.punto_di_ingresso) : USER_chiudere;
    for (unsigned 순번 = 0; 순번 < USER_pagina_CONTA_NUMERI; 순번++) {
        unsigned autorizzazioni = Autorizzazioni_elenco[순번];
        pagina_elenco[순번] = autorizzazioni ? (USER_BASE + 순번 * dimensioni_della_pagina) | (autorizzazioni == 3 ? USER_in_lettura_scrittura : autorizzazioni == 5 ? 사용자읽고실행 : USER_di_sola_lettura) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) elenco_file[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    heap_chiudere = USER_foto_chiudere;
    attivo = 1; START_TIMEOUT();
    USER_esecuzione_time[proprietario_oggetto]=보드밀리초();
    int risultato = USER_immettere(eseguibile_Intestazione.punto_di_ingresso, 초기쌓임공간, 전달값);
    return Fine_app(risultato);
}
uintptr_t scheda_USER_eseguire(uintptr_t CERCA_INDICE) {
    if (CERCA_INDICE >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nome=CERCA_INDICE==10?"javac":CERCA_INDICE==11?"java":CERCA_INDICE==12?"python":CERCA_INDICE==13?"vi":CERCA_INDICE==14?"jar":CERCA_INDICE==15?"cc":CERCA_INDICE==16?"jaot":"ELF";
    return (uint32_t)eseguire_app(실행항목들[CERCA_INDICE].dati, 실행항목들[CERCA_INDICE].Dimensione, 실행항목들[CERCA_INDICE].전달값, 0, Nome);
}
static uintptr_t Esegui_File(int 리눅스방식) {
    static unsigned char foto[16384];
    if (attivo || !전달인수개수) return (uint32_t)-22;
    int handle_di_file = pk_open((const char *)전달인수[0], di_sola_lettura_VALORE, 0);
    if (handle_di_file < 0) return (uint32_t)-numero_errore;
    int Dimensione = pk_size(handle_di_file);
    if (Dimensione < 0 || (unsigned)Dimensione > sizeof(foto)) { pk_close(handle_di_file); return (uint32_t)-27; }
    int RICEV_SCAD_CONTA_NUMERI = pk_read(handle_di_file, foto, Dimensione); pk_close(handle_di_file);
    if (RICEV_SCAD_CONTA_NUMERI != Dimensione) return (uint32_t)-5;
    return (uint32_t)eseguire_app(foto, Dimensione, 0, 리눅스방식, "");
}
uintptr_t scheda_USER_File(void) { return Esegui_File(0); }
uintptr_t 보드사용자리눅스파일(void) { return Esegui_File(1); }
uintptr_t scheda_USER_convalidare(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].dati, 잘못된실행항목들[순번].Dimensione) != USER_eseguibile_errore) return 순번 + 1;
    return 0;
}
