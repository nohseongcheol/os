#include "../명명/기계연결이름.h"
#include "schermata_info.h"
#include <stdint.h>
#include <stddef.h>
#include "spazio_utente.h"
#include "../rete_Pila/rete_Pila.h"
typedef uintptr_t computer_Word;
#define computer_registro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define seriale_cellulare 0xfe201000u
#define 범용입출력 0xfe200000u
#define cassetta_postale_e_mail 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t clock_CONTA_NUMERI(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENZA;
static volatile uint32_t cassetta_postale_dati[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *dati_funzione, int punto_di_codice, size_t articolo_CONTA_NUMERI) { unsigned char *Avanti_SCARTO = dati_funzione; while (articolo_CONTA_NUMERI--) *Avanti_SCARTO++ = punto_di_codice; return dati_funzione; }
void *memcpy(void *meta_dati, const void *stringa_dati, size_t articolo_CONTA_NUMERI) { unsigned char *첫째값 = meta_dati; const unsigned char *SECONDO_VALORE = stringa_dati; while (articolo_CONTA_NUMERI--) *첫째값++ = *SECONDO_VALORE++; return meta_dati; }

static int cassetta_postale(void) {
    uint32_t richiesta = (uint32_t)(uintptr_t)cassetta_postale_dati | 8;
    uint64_t avvia = clock_CONTA_NUMERI();
    기억장벽();
    while (computer_registro(cassetta_postale_e_mail + 0x38) & 0x80000000u)
        if (clock_CONTA_NUMERI() - avvia > FREQUENZA) return 0;
    computer_registro(cassetta_postale_e_mail + 0x20) = richiesta;
    for (;;) {
        if (!(computer_registro(cassetta_postale_e_mail + 0x18) & 0x40000000u)) {
            uint32_t replica = computer_registro(cassetta_postale_e_mail);
            if (replica == richiesta) { 기억장벽(); return cassetta_postale_dati[1] == 0x80000000u; }
        }
        if (clock_CONTA_NUMERI() - avvia > FREQUENZA) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminale_byte(unsigned);
extern int Terminale_In_sospeso(void);
extern void Terminale_puntatore(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminale_input_MODA(unsigned);
#include "../remoto_VALORE/remoto_VALORE.h"
static int Flussi;
static unsigned 직렬이전글자;
computer_Word scheda_Flussi(computer_Word 사용여부) { Flussi=사용여부!=0; return 0; }
computer_Word scheda_Canale(computer_Word Canale, computer_Word punto_di_codice) {
    if(Flussi && 자바셸출력((int32_t)Canale,(int32_t)(punto_di_codice&255))) return 0;
    Terminale_byte(punto_di_codice&255);
    remoto_output(punto_di_codice&255);
    if ((punto_di_codice&255)==10 && 직렬이전글자!=13) {
        while (computer_registro(seriale_cellulare + 0x18) & 0x20) __asm__ volatile("yield");
        computer_registro(seriale_cellulare)=13;
    }
    직렬이전글자=punto_di_codice&255;
    while (computer_registro(seriale_cellulare + 0x18) & 0x20) __asm__ volatile("yield");
    computer_registro(seriale_cellulare) = (uint32_t)punto_di_codice & 255;
    return 0;
}
computer_Word 보드글자쓰기(computer_Word punto_di_codice) { return scheda_Canale(1,punto_di_codice); }
computer_Word 보드원시글자읽기(void) {
    int remoto_carattere=remoto_input();if(remoto_carattere>=0)return remoto_carattere;
    if (computer_registro(seriale_cellulare + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALORE = computer_registro(seriale_cellulare);
    if (VALORE & 0xf00) { computer_registro(seriale_cellulare + 4) = 0; return (uint32_t)-1; }
    return VALORE & 255;
}
computer_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pacchetto_dati[6];
    if(Terminale_In_sospeso())return (uint32_t)-4096;
    if(Flussi){int32_t punto_di_codice=자바셸입력();if(punto_di_codice!=-3)return (uint32_t)punto_di_codice;}
    for(;;){
        int punto_di_codice=(int32_t)보드원시글자읽기();if(punto_di_codice<0)return (uint32_t)punto_di_codice;
        if(!꾸러미안쪽){if(punto_di_codice!=30)return punto_di_codice;꾸러미안쪽=1;사용량=0;continue;}
        pacchetto_dati[사용량++]=punto_di_codice;if(사용량<6)continue;꾸러미안쪽=0;
        if(pacchetto_dati[0]==1)Terminale_puntatore(pacchetto_dati[1],pacchetto_dati[2]+pacchetto_dati[3]*256,pacchetto_dati[4]+pacchetto_dati[5]*256);
        if(pacchetto_dati[0]==2)터미널바로가기키(pacchetto_dati[1]);
        if(pacchetto_dati[0]==3)Terminale_input_MODA(pacchetto_dati[1]);
        if(Terminale_In_sospeso())return (uint32_t)-4096;
    }
}
computer_Word 보드밀리초(void) { return (uint32_t)(clock_CONTA_NUMERI() / (FREQUENZA / 1000)); }
computer_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *stringa_dati) { while (*stringa_dati) 보드글자쓰기((unsigned char)*stringa_dati++); }
static void 직렬열여섯진출력(computer_Word articolo_CONTA_NUMERI) { const char *열여섯진숫자 = "0123456789abcdef"; for (int stringa_dati = 60; stringa_dati >= 0; stringa_dati -= 4) 보드글자쓰기(열여섯진숫자[(articolo_CONTA_NUMERI >> stringa_dati) & 15]); }
computer_Word scheda_Stop(computer_Word Stato_VALORE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Stato_VALORE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); scheda_Stop(1); __builtin_unreachable(); }
void scheda_eccezione(computer_Word eccezione_Stato, computer_Word comando_funzione, computer_Word non_valida_e_mail) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(eccezione_Stato);
    직렬글출력(" PC="); 직렬열여섯진출력(comando_funzione); 직렬글출력(" FAR="); 직렬열여섯진출력(non_valida_e_mail);
    scheda_Stop(2);
}
int scheda_fisico_hardware(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    cassetta_postale_dati[0]=32;cassetta_postale_dati[1]=0;cassetta_postale_dati[2]=0x10004;cassetta_postale_dati[3]=8;cassetta_postale_dati[4]=0;
    cassetta_postale_dati[5]=cassetta_postale_dati[6]=cassetta_postale_dati[7]=0;
    return cassetta_postale()&&cassetta_postale_dati[4]==0x80000008u&&(cassetta_postale_dati[5]||cassetta_postale_dati[6]);
}
int scheda_indirizzo_reale(unsigned char *e_mail) {
    cassetta_postale_dati[0]=32;cassetta_postale_dati[1]=0;cassetta_postale_dati[2]=0x10003;cassetta_postale_dati[3]=8;cassetta_postale_dati[4]=0;
    cassetta_postale_dati[5]=cassetta_postale_dati[6]=cassetta_postale_dati[7]=0;
    if(!cassetta_postale()||(cassetta_postale_dati[4]&0x80000000u)==0||(cassetta_postale_dati[4]&0xffff)!=6)return 0;
    const unsigned char *dati=(const unsigned char*)&cassetta_postale_dati[5];unsigned SUM_VALORE=0;
    for(unsigned 순번=0;순번<6;순번++){e_mail[순번]=dati[순번];SUM_VALORE|=dati[순번];}return SUM_VALORE&&!(e_mail[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENZA));
    computer_registro(seriale_cellulare + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    computer_registro(범용입출력 + 4) = (computer_registro(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    computer_registro(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. errore_VALORE 시 config.txt의 48MHz를 사용한다.
    cassetta_postale_dati[0] = 36; cassetta_postale_dati[1] = 0; cassetta_postale_dati[2] = 0x38002; cassetta_postale_dati[3] = 12;
    cassetta_postale_dati[4] = 0; cassetta_postale_dati[5] = 2; cassetta_postale_dati[6] = 48000000; cassetta_postale_dati[7] = 0; cassetta_postale_dati[8] = 0;
    int clock_integro = cassetta_postale();
    uint32_t 속도 = clock_integro && cassetta_postale_dati[6] >= 1843200 ? cassetta_postale_dati[6] : 48000000;
    cassetta_postale_dati[0]=32; cassetta_postale_dati[1]=0; cassetta_postale_dati[2]=0x10005; cassetta_postale_dati[3]=8; cassetta_postale_dati[4]=0;
    cassetta_postale_dati[5]=cassetta_postale_dati[6]=cassetta_postale_dati[7]=0;
    if (cassetta_postale() && cassetta_postale_dati[4]==0x80000008u) 팔기억킬로바이트=cassetta_postale_dati[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    computer_registro(seriale_cellulare + 0x44) = 0x7ff;
    computer_registro(seriale_cellulare + 0x24) = 육십사배나눔수 / 64;
    computer_registro(seriale_cellulare + 0x28) = 육십사배나눔수 % 64;
    computer_registro(seriale_cellulare + 0x2c) = (3u << 5) | (1u << 4);
    computer_registro(seriale_cellulare + 0x38) = 0;
    computer_registro(seriale_cellulare + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
computer_Word scheda_FTP(computer_Word Azione) { return (uint32_t)ftp_control((int)Azione); }
computer_Word scheda_rete_stato(computer_Word voce_VALORE, computer_Word INDICE) { return 망상태읽기(voce_VALORE, INDICE); }
computer_Word scheda_rete_Impostazioni(computer_Word Azione, computer_Word e_mail, computer_Word maschera_VALORE, computer_Word gateway_VALORE) { return (uint32_t)configurare_rete(Azione, e_mail, maschera_VALORE, gateway_VALORE); }
computer_Word scheda_inviare_risposta(computer_Word e_mail, computer_Word ordine_VALORE) { return (uint32_t)START_risposta_test(e_mail, ordine_VALORE); }
computer_Word 보드응답읽기(computer_Word voce_VALORE) { return (uint32_t)응답시험읽기(voce_VALORE); }
computer_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDICE=0; INDICE<32; INDICE++) Chiudi_rete(INDICE);
    for (unsigned INDICE=0; INDICE<4; INDICE++) scheda_controllo_utente(32+INDICE);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (computer_registro(seriale_cellulare+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    computer_registro(0xfe100020ul)=0x5a000000u | (computer_registro(0xfe100020ul)&~0xfffu) | 0x555;
    computer_registro(0xfe100024ul)=0x5a000000u | 10;
    computer_registro(0xfe10001cul)=0x5a000000u | (computer_registro(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

computer_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 Regolari_articolo 크기를 읽는다. */
    const uint32_t query_VALORE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, richiesto_altezza = 480;
    for (size_t 순번 = 0; 순번 < sizeof(query_VALORE)/4; 순번++) cassetta_postale_dati[순번] = query_VALORE[순번];
    if (cassetta_postale() && cassetta_postale_dati[4] == 0x80000008u &&
        cassetta_postale_dati[5] >= 640 && cassetta_postale_dati[5] <= 1920 &&
        cassetta_postale_dati[6] >= 480 && cassetta_postale_dati[6] <= 1080) {
        요청너비 = cassetta_postale_dati[5]; richiesto_altezza = cassetta_postale_dati[6];
    }
    const uint32_t richiesta[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, richiesto_altezza,
        0x48004, 8, 0, 요청너비, richiesto_altezza,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(richiesta)/4; 순번++) cassetta_postale_dati[순번] = richiesta[순번];
    // 위 메시지의 effettivo_dati 길이를 usare_VALORE: 태그 Aggiunta_voce 시 durata_VALORE 불일치를 방지한다.
    cassetta_postale_dati[0] = sizeof(richiesta);
    if (!cassetta_postale()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned risposta_durata[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (cassetta_postale_dati[응답들[순번]] != (0x80000000u | risposta_durata[순번])) return 0;
    uint32_t sfondo_VALORE = cassetta_postale_dati[28] & 0x3fffffffu;
    uint32_t Dimensione = cassetta_postale_dati[29];
    uint32_t 받은너비 = cassetta_postale_dati[5], RICEV_SCAD_altezza = cassetta_postale_dati[6], RICEV_SCAD_interlinea = cassetta_postale_dati[33];
    if (cassetta_postale_dati[15] != 32 || cassetta_postale_dati[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || RICEV_SCAD_altezza < 480 || RICEV_SCAD_altezza > 1080 ||
        cassetta_postale_dati[10] < 받은너비 || cassetta_postale_dati[11] < RICEV_SCAD_altezza || cassetta_postale_dati[23] || cassetta_postale_dati[24] ||
        !sfondo_VALORE || sfondo_VALORE < 0x1000000 || (sfondo_VALORE & 3) || RICEV_SCAD_interlinea < 받은너비 * 4 || (RICEV_SCAD_interlinea & 3) ||
        (uint64_t)RICEV_SCAD_interlinea * RICEV_SCAD_altezza > Dimensione || (uint64_t)sfondo_VALORE + Dimensione > 0x40000000u)
        return 0;
    scheda_Prepara_disegno((volatile uint32_t *)(uintptr_t)sfondo_VALORE, 받은너비, RICEV_SCAD_altezza, RICEV_SCAD_interlinea);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 thread_VALORE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } contesto;
static contesto 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int reparto_IT_Corsa[3] = {1, 0, 0};
static int Regolari_task;
extern void cambio_di_contesto(contesto *, contesto *);
extern void 자바작업(int32_t);
computer_Word scheda_REND(void) {
    network_poll();
    int Indietro_articolo = Regolari_task, Avanti_articolo = (Indietro_articolo + 1) % 3;
    while (Avanti_articolo != Indietro_articolo && !reparto_IT_Corsa[Avanti_articolo]) Avanti_articolo = (Avanti_articolo + 1) % 3;
    if (Avanti_articolo != Indietro_articolo) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (reparto_IT_Corsa[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        Regolari_task = Avanti_articolo;
        cambio_di_contesto(&작업문맥들[Indietro_articolo], &작업문맥들[Avanti_articolo]);
    }
    return 0;
}
static void task_avvio(void) {
    자바작업(Regolari_task);
    reparto_IT_Corsa[Regolari_task] = 0;
    scheda_REND();
    커널중단("finished task resumed");
}
computer_Word scheda_task_Crea(computer_Word identificatore_VALORE) {
    if (identificatore_VALORE < 1 || identificatore_VALORE > 2 || reparto_IT_Corsa[identificatore_VALORE]) return (uint32_t)-1;
    memset(&작업문맥들[identificatore_VALORE], 0, sizeof(contesto));
    *(uint64_t *)쌓임공간들[identificatore_VALORE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identificatore_VALORE].저장값[11] = (uintptr_t)task_avvio;
    작업문맥들[identificatore_VALORE].저장값[12] = (uintptr_t)(쌓임공간들[identificatore_VALORE - 1] + sizeof(쌓임공간들[0]));
    reparto_IT_Corsa[identificatore_VALORE] = 1;
    return 0;
}
computer_Word scheda_task_Stato(computer_Word identificatore_VALORE) { return identificatore_VALORE < 3 ? reparto_IT_Corsa[identificatore_VALORE] : (uint32_t)-1; }
extern computer_Word AOT_Memoria_CERCA(computer_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
computer_Word scheda_query_Sistema(computer_Word voce_VALORE, computer_Word INDICE) {
    if (voce_VALORE==0) return 팔기억킬로바이트;
    if (voce_VALORE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (voce_VALORE==2 || voce_VALORE==3) return AOT_Memoria_CERCA(voce_VALORE==3);
    if (voce_VALORE==4) return 화면준비됨 ? (보드화면너비()*scheda_schermata_altezza()*4+1023)/1024 : 0;
    if (voce_VALORE==5) return 80*1024; /* Esegui_comando e_mail_area 16 MiB + 네 세션 보관 e_mail_area. */
    if (voce_VALORE>=20) return 사용자상태읽기(voce_VALORE-20, INDICE);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[Regolari_task]; }
