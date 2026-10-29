#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "usuari.h"
#include "../xarxa_Pila/xarxa_Pila.h"
typedef uintptr_t màquina_Word;
#define màquina_registrar_se(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define bústia_ADREÇA 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Rellotge_COMPT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCIA;
static volatile uint32_t bústia_dades[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *dades_càrrec, int codi_de_caràcter, size_t element_COMPT) { unsigned char *Següent_DESPLAÇAMENT = dades_càrrec; while (element_COMPT--) *Següent_DESPLAÇAMENT++ = codi_de_caràcter; return dades_càrrec; }
void *memcpy(void *destinació_dades, const void *cadena_dades, size_t element_COMPT) { unsigned char *첫째값 = destinació_dades; const unsigned char *SEGON_VALOR = cadena_dades; while (element_COMPT--) *첫째값++ = *SEGON_VALOR++; return destinació_dades; }

static int bústia(void) {
    uint32_t sol_licitud = (uint32_t)(uintptr_t)bústia_dades | 8;
    uint64_t Executa_2 = Rellotge_COMPT();
    기억장벽();
    while (màquina_registrar_se(bústia_ADREÇA + 0x38) & 0x80000000u)
        if (Rellotge_COMPT() - Executa_2 > FREQUENCIA) return 0;
    màquina_registrar_se(bústia_ADREÇA + 0x20) = sol_licitud;
    for (;;) {
        if (!(màquina_registrar_se(bústia_ADREÇA + 0x18) & 0x40000000u)) {
            uint32_t resposta = màquina_registrar_se(bústia_ADREÇA);
            if (resposta == sol_licitud) { 기억장벽(); return bústia_dades[1] == 0x80000000u; }
        }
        if (Rellotge_COMPT() - Executa_2 > FREQUENCIA) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_pendent(void);
extern void Terminal_punter(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../remot_VALOR/remot_VALOR.h"
static int Seqüències;
static unsigned 직렬이전글자;
màquina_Word Tauler_Seqüències(màquina_Word 사용여부) { Seqüències=사용여부!=0; return 0; }
màquina_Word Tauler_Canal(màquina_Word Canal, màquina_Word codi_de_caràcter) {
    if(Seqüències && 자바셸출력((int32_t)Canal,(int32_t)(codi_de_caràcter&255))) return 0;
    Terminal_byte(codi_de_caràcter&255);
    원격출력(codi_de_caràcter&255);
    if ((codi_de_caràcter&255)==10 && 직렬이전글자!=13) {
        while (màquina_registrar_se(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        màquina_registrar_se(직렬장치)=13;
    }
    직렬이전글자=codi_de_caràcter&255;
    while (màquina_registrar_se(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    màquina_registrar_se(직렬장치) = (uint32_t)codi_de_caràcter & 255;
    return 0;
}
màquina_Word 보드글자쓰기(màquina_Word codi_de_caràcter) { return Tauler_Canal(1,codi_de_caràcter); }
màquina_Word 보드원시글자읽기(void) {
    int remot_caràcter=원격입력();if(remot_caràcter>=0)return remot_caràcter;
    if (màquina_registrar_se(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALOR = màquina_registrar_se(직렬장치);
    if (VALOR & 0xf00) { màquina_registrar_se(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALOR & 255;
}
màquina_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paquet_dades[6];
    if(Terminal_pendent())return (uint32_t)-4096;
    if(Seqüències){int32_t codi_de_caràcter=자바셸입력();if(codi_de_caràcter!=-3)return (uint32_t)codi_de_caràcter;}
    for(;;){
        int codi_de_caràcter=(int32_t)보드원시글자읽기();if(codi_de_caràcter<0)return (uint32_t)codi_de_caràcter;
        if(!꾸러미안쪽){if(codi_de_caràcter!=30)return codi_de_caràcter;꾸러미안쪽=1;사용량=0;continue;}
        paquet_dades[사용량++]=codi_de_caràcter;if(사용량<6)continue;꾸러미안쪽=0;
        if(paquet_dades[0]==1)Terminal_punter(paquet_dades[1],paquet_dades[2]+paquet_dades[3]*256,paquet_dades[4]+paquet_dades[5]*256);
        if(paquet_dades[0]==2)터미널바로가기키(paquet_dades[1]);
        if(paquet_dades[0]==3)터미널입력방식(paquet_dades[1]);
        if(Terminal_pendent())return (uint32_t)-4096;
    }
}
màquina_Word 보드밀리초(void) { return (uint32_t)(Rellotge_COMPT() / (FREQUENCIA / 1000)); }
màquina_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *cadena_dades) { while (*cadena_dades) 보드글자쓰기((unsigned char)*cadena_dades++); }
static void 직렬열여섯진출력(màquina_Word element_COMPT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int cadena_dades = 60; cadena_dades >= 0; cadena_dades -= 4) 보드글자쓰기(열여섯진숫자[(element_COMPT >> cadena_dades) & 15]); }
màquina_Word Tauler_aturar(màquina_Word Estat_VALOR) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Estat_VALOR); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tauler_aturar(1); __builtin_unreachable(); }
void Tauler_excepció(màquina_Word excepció_Estat, màquina_Word ordre_càrrec, màquina_Word invàlid_ADREÇA) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(excepció_Estat);
    직렬글출력(" PC="); 직렬열여섯진출력(ordre_càrrec); 직렬글출력(" FAR="); 직렬열여섯진출력(invàlid_ADREÇA);
    Tauler_aturar(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    bústia_dades[0]=32;bústia_dades[1]=0;bústia_dades[2]=0x10004;bústia_dades[3]=8;bústia_dades[4]=0;
    bústia_dades[5]=bústia_dades[6]=bústia_dades[7]=0;
    return bústia()&&bústia_dades[4]==0x80000008u&&(bústia_dades[5]||bústia_dades[6]);
}
int Tauler_màquina_ADREÇA(unsigned char *Adreça) {
    bústia_dades[0]=32;bústia_dades[1]=0;bústia_dades[2]=0x10003;bústia_dades[3]=8;bústia_dades[4]=0;
    bústia_dades[5]=bústia_dades[6]=bústia_dades[7]=0;
    if(!bústia()||(bústia_dades[4]&0x80000000u)==0||(bústia_dades[4]&0xffff)!=6)return 0;
    const unsigned char *dades=(const unsigned char*)&bústia_dades[5];unsigned SUMA_VALOR=0;
    for(unsigned 순번=0;순번<6;순번++){Adreça[순번]=dades[순번];SUMA_VALOR|=dades[순번];}return SUMA_VALOR&&!(Adreça[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCIA));
    màquina_registrar_se(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    màquina_registrar_se(범용입출력 + 4) = (màquina_registrar_se(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    màquina_registrar_se(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. error_VALOR 시 config.txt의 48MHz를 사용한다.
    bústia_dades[0] = 36; bústia_dades[1] = 0; bústia_dades[2] = 0x38002; bústia_dades[3] = 12;
    bústia_dades[4] = 0; bústia_dades[5] = 2; bústia_dades[6] = 48000000; bústia_dades[7] = 0; bústia_dades[8] = 0;
    int 시계정상 = bústia();
    uint32_t 속도 = 시계정상 && bústia_dades[6] >= 1843200 ? bústia_dades[6] : 48000000;
    bústia_dades[0]=32; bústia_dades[1]=0; bústia_dades[2]=0x10005; bústia_dades[3]=8; bústia_dades[4]=0;
    bústia_dades[5]=bústia_dades[6]=bústia_dades[7]=0;
    if (bústia() && bústia_dades[4]==0x80000008u) 팔기억킬로바이트=bústia_dades[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    màquina_registrar_se(직렬장치 + 0x44) = 0x7ff;
    màquina_registrar_se(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    màquina_registrar_se(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    màquina_registrar_se(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    màquina_registrar_se(직렬장치 + 0x38) = 0;
    màquina_registrar_se(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
màquina_Word Tauler_FTP(màquina_Word Acció) { return (uint32_t)ftp_control((int)Acció); }
màquina_Word Tauler_xarxa_estat(màquina_Word introducció_VALOR, màquina_Word INDEX) { return tancar_xarxa_estat(introducció_VALOR, INDEX); }
màquina_Word Tauler_xarxa_Configuració(màquina_Word Acció, màquina_Word Adreça, màquina_Word màscara_VALOR, màquina_Word passarel_la_VALOR) { return (uint32_t)configurar_xarxa(Acció, Adreça, màscara_VALOR, passarel_la_VALOR); }
màquina_Word Tauler_enviar_resposta(màquina_Word Adreça, màquina_Word comanda_VALOR) { return (uint32_t)응답시험시작(Adreça, comanda_VALOR); }
màquina_Word Tauler_tancar_resposta(màquina_Word introducció_VALOR) { return (uint32_t)응답시험읽기(introducció_VALOR); }
màquina_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Tanca_xarxa(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Tauler_control_d_usuari(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (màquina_registrar_se(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    màquina_registrar_se(0xfe100020ul)=0x5a000000u | (màquina_registrar_se(0xfe100020ul)&~0xfffu) | 0x555;
    màquina_registrar_se(0xfe100024ul)=0x5a000000u | 10;
    màquina_registrar_se(0xfe10001cul)=0x5a000000u | (màquina_registrar_se(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

màquina_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t cerca_VALOR[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(cerca_VALOR)/4; 순번++) bústia_dades[순번] = cerca_VALOR[순번];
    if (bústia() && bústia_dades[4] == 0x80000008u &&
        bústia_dades[5] >= 640 && bústia_dades[5] <= 1920 &&
        bústia_dades[6] >= 480 && bústia_dades[6] <= 1080) {
        요청너비 = bústia_dades[5]; 요청높이 = bústia_dades[6];
    }
    const uint32_t sol_licitud[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, 요청높이,
        0x48004, 8, 0, 요청너비, 요청높이,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(sol_licitud)/4; 순번++) bústia_dades[순번] = sol_licitud[순번];
    // 위 메시지의 real_dades 길이를 ús_VALOR: 태그 Annexa_introducció 시 durada_VALOR 불일치를 방지한다.
    bústia_dades[0] = sizeof(sol_licitud);
    if (!bústia()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned resposta_durada[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (bústia_dades[응답들[순번]] != (0x80000000u | resposta_durada[순번])) return 0;
    uint32_t Fons_VALOR = bústia_dades[28] & 0x3fffffffu;
    uint32_t Mida = bústia_dades[29];
    uint32_t 받은너비 = bústia_dades[5], 받은높이 = bústia_dades[6], CANTIDAD_RECIBIDA_interlineat = bústia_dades[33];
    if (bústia_dades[15] != 32 || bústia_dades[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        bústia_dades[10] < 받은너비 || bústia_dades[11] < 받은높이 || bústia_dades[23] || bústia_dades[24] ||
        !Fons_VALOR || Fons_VALOR < 0x1000000 || (Fons_VALOR & 3) || CANTIDAD_RECIBIDA_interlineat < 받은너비 * 4 || (CANTIDAD_RECIBIDA_interlineat & 3) ||
        (uint64_t)CANTIDAD_RECIBIDA_interlineat * 받은높이 > Mida || (uint64_t)Fons_VALOR + Mida > 0x40000000u)
        return 0;
    Tauler_Prepara_dibuix((volatile uint32_t *)(uintptr_t)Fons_VALOR, 받은너비, 받은높이, CANTIDAD_RECIBIDA_interlineat);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 fil_VALOR. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int tecnologies_de_la_informació_Atletisme[3] = {1, 0, 0};
static int 현재작업;
extern void 작업문맥바꾸기(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
màquina_Word Tauler_RENDTO(void) {
    network_poll();
    int 이전 = 현재작업, Següent_element = (이전 + 1) % 3;
    while (Següent_element != 이전 && !tecnologies_de_la_informació_Atletisme[Següent_element]) Següent_element = (Següent_element + 1) % 3;
    if (Següent_element != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (tecnologies_de_la_informació_Atletisme[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Següent_element;
        작업문맥바꾸기(&작업문맥들[이전], &작업문맥들[Següent_element]);
    }
    return 0;
}
static void tasca_inici(void) {
    자바작업(현재작업);
    tecnologies_de_la_informació_Atletisme[현재작업] = 0;
    Tauler_RENDTO();
    커널중단("finished task resumed");
}
màquina_Word Tauler_tasca_Crear(màquina_Word identificador_VALOR) {
    if (identificador_VALOR < 1 || identificador_VALOR > 2 || tecnologies_de_la_informació_Atletisme[identificador_VALOR]) return (uint32_t)-1;
    memset(&작업문맥들[identificador_VALOR], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[identificador_VALOR - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identificador_VALOR].저장값[11] = (uintptr_t)tasca_inici;
    작업문맥들[identificador_VALOR].저장값[12] = (uintptr_t)(쌓임공간들[identificador_VALOR - 1] + sizeof(쌓임공간들[0]));
    tecnologies_de_la_informació_Atletisme[identificador_VALOR] = 1;
    return 0;
}
màquina_Word Tauler_tasca_Estat(màquina_Word identificador_VALOR) { return identificador_VALOR < 3 ? tecnologies_de_la_informació_Atletisme[identificador_VALOR] : (uint32_t)-1; }
extern màquina_Word 미리번역기억조회(màquina_Word);
extern uint32_t tancar_usuari_Estat(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
màquina_Word Tauler_cerca_sistema(màquina_Word introducció_VALOR, màquina_Word INDEX) {
    if (introducció_VALOR==0) return 팔기억킬로바이트;
    if (introducció_VALOR==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (introducció_VALOR==2 || introducció_VALOR==3) return 미리번역기억조회(introducció_VALOR==3);
    if (introducció_VALOR==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (introducció_VALOR==5) return 80*1024; /* Executa_ordre 공간 16 MiB + 네 세션 보관 공간. */
    if (introducció_VALOR>=20) return tancar_usuari_Estat(introducció_VALOR-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
