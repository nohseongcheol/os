#include "../명명/기계연결이름.h"
#include "tela_informações.h"
#include <stdint.h>
#include <stddef.h>
#include "espaço_do_utilizador.h"
#include "../rede_pilha/rede_pilha.h"
typedef uintptr_t computador_Word;
#define computador_registro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define caixa_de_correio_email 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Relógio_CONT_NÚM(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQÜÊNCIA;
static volatile uint32_t caixa_de_correio_dados[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *dados_cargo, int ponto_de_código, size_t item_CONT_NÚM) { unsigned char *Avançar_DESLOC = dados_cargo; while (item_CONT_NÚM--) *Avançar_DESLOC++ = ponto_de_código; return dados_cargo; }
void *memcpy(void *destino_dados, const void *cadeia_dados, size_t item_CONT_NÚM) { unsigned char *첫째값 = destino_dados; const unsigned char *SEGUNDO_VALOR = cadeia_dados; while (item_CONT_NÚM--) *첫째값++ = *SEGUNDO_VALOR++; return destino_dados; }

static int caixa_de_correio(void) {
    uint32_t solicitação = (uint32_t)(uintptr_t)caixa_de_correio_dados | 8;
    uint64_t iniciar = Relógio_CONT_NÚM();
    기억장벽();
    while (computador_registro(caixa_de_correio_email + 0x38) & 0x80000000u)
        if (Relógio_CONT_NÚM() - iniciar > FREQÜÊNCIA) return 0;
    computador_registro(caixa_de_correio_email + 0x20) = solicitação;
    for (;;) {
        if (!(computador_registro(caixa_de_correio_email + 0x18) & 0x40000000u)) {
            uint32_t resposta = computador_registro(caixa_de_correio_email);
            if (resposta == solicitação) { 기억장벽(); return caixa_de_correio_dados[1] == 0x80000000u; }
        }
        if (Relógio_CONT_NÚM() - iniciar > FREQÜÊNCIA) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_Pendente(void);
extern void Terminal_ponteiro(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminal_entrada_MODO(unsigned);
#include "../remoto_VALOR/remoto_VALOR.h"
static int Fluxos;
static unsigned 직렬이전글자;
computador_Word Quadro_Fluxos(computador_Word 사용여부) { Fluxos=사용여부!=0; return 0; }
computador_Word Quadro_Canal(computador_Word Canal, computador_Word ponto_de_código) {
    if(Fluxos && 자바셸출력((int32_t)Canal,(int32_t)(ponto_de_código&255))) return 0;
    Terminal_byte(ponto_de_código&255);
    remoto_saída(ponto_de_código&255);
    if ((ponto_de_código&255)==10 && 직렬이전글자!=13) {
        while (computador_registro(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        computador_registro(직렬장치)=13;
    }
    직렬이전글자=ponto_de_código&255;
    while (computador_registro(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    computador_registro(직렬장치) = (uint32_t)ponto_de_código & 255;
    return 0;
}
computador_Word 보드글자쓰기(computador_Word ponto_de_código) { return Quadro_Canal(1,ponto_de_código); }
computador_Word 보드원시글자읽기(void) {
    int remoto_caractere=remoto_entrada();if(remoto_caractere>=0)return remoto_caractere;
    if (computador_registro(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALOR = computador_registro(직렬장치);
    if (VALOR & 0xf00) { computador_registro(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALOR & 255;
}
computador_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pacote_dados[6];
    if(Terminal_Pendente())return (uint32_t)-4096;
    if(Fluxos){int32_t ponto_de_código=자바셸입력();if(ponto_de_código!=-3)return (uint32_t)ponto_de_código;}
    for(;;){
        int ponto_de_código=(int32_t)보드원시글자읽기();if(ponto_de_código<0)return (uint32_t)ponto_de_código;
        if(!꾸러미안쪽){if(ponto_de_código!=30)return ponto_de_código;꾸러미안쪽=1;사용량=0;continue;}
        pacote_dados[사용량++]=ponto_de_código;if(사용량<6)continue;꾸러미안쪽=0;
        if(pacote_dados[0]==1)Terminal_ponteiro(pacote_dados[1],pacote_dados[2]+pacote_dados[3]*256,pacote_dados[4]+pacote_dados[5]*256);
        if(pacote_dados[0]==2)터미널바로가기키(pacote_dados[1]);
        if(pacote_dados[0]==3)Terminal_entrada_MODO(pacote_dados[1]);
        if(Terminal_Pendente())return (uint32_t)-4096;
    }
}
computador_Word 보드밀리초(void) { return (uint32_t)(Relógio_CONT_NÚM() / (FREQÜÊNCIA / 1000)); }
computador_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *cadeia_dados) { while (*cadeia_dados) 보드글자쓰기((unsigned char)*cadeia_dados++); }
static void 직렬열여섯진출력(computador_Word item_CONT_NÚM) { const char *열여섯진숫자 = "0123456789abcdef"; for (int cadeia_dados = 60; cadeia_dados >= 0; cadeia_dados -= 4) 보드글자쓰기(열여섯진숫자[(item_CONT_NÚM >> cadeia_dados) & 15]); }
computador_Word Quadro_Pare(computador_Word Estado_VALOR) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Estado_VALOR); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Quadro_Pare(1); __builtin_unreachable(); }
void Quadro_exceção(computador_Word exceção_Estado, computador_Word comando_cargo, computador_Word inválido_email) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(exceção_Estado);
    직렬글출력(" PC="); 직렬열여섯진출력(comando_cargo); 직렬글출력(" FAR="); 직렬열여섯진출력(inválido_email);
    Quadro_Pare(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    caixa_de_correio_dados[0]=32;caixa_de_correio_dados[1]=0;caixa_de_correio_dados[2]=0x10004;caixa_de_correio_dados[3]=8;caixa_de_correio_dados[4]=0;
    caixa_de_correio_dados[5]=caixa_de_correio_dados[6]=caixa_de_correio_dados[7]=0;
    return caixa_de_correio()&&caixa_de_correio_dados[4]==0x80000008u&&(caixa_de_correio_dados[5]||caixa_de_correio_dados[6]);
}
int Quadro_endereço_real(unsigned char *Endereço) {
    caixa_de_correio_dados[0]=32;caixa_de_correio_dados[1]=0;caixa_de_correio_dados[2]=0x10003;caixa_de_correio_dados[3]=8;caixa_de_correio_dados[4]=0;
    caixa_de_correio_dados[5]=caixa_de_correio_dados[6]=caixa_de_correio_dados[7]=0;
    if(!caixa_de_correio()||(caixa_de_correio_dados[4]&0x80000000u)==0||(caixa_de_correio_dados[4]&0xffff)!=6)return 0;
    const unsigned char *dados=(const unsigned char*)&caixa_de_correio_dados[5];unsigned SUM_VALOR=0;
    for(unsigned 순번=0;순번<6;순번++){Endereço[순번]=dados[순번];SUM_VALOR|=dados[순번];}return SUM_VALOR&&!(Endereço[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQÜÊNCIA));
    computador_registro(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    computador_registro(범용입출력 + 4) = (computador_registro(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    computador_registro(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. falha_VALOR 시 config.txt의 48MHz를 사용한다.
    caixa_de_correio_dados[0] = 36; caixa_de_correio_dados[1] = 0; caixa_de_correio_dados[2] = 0x38002; caixa_de_correio_dados[3] = 12;
    caixa_de_correio_dados[4] = 0; caixa_de_correio_dados[5] = 2; caixa_de_correio_dados[6] = 48000000; caixa_de_correio_dados[7] = 0; caixa_de_correio_dados[8] = 0;
    int Relógio_íntegro = caixa_de_correio();
    uint32_t 속도 = Relógio_íntegro && caixa_de_correio_dados[6] >= 1843200 ? caixa_de_correio_dados[6] : 48000000;
    caixa_de_correio_dados[0]=32; caixa_de_correio_dados[1]=0; caixa_de_correio_dados[2]=0x10005; caixa_de_correio_dados[3]=8; caixa_de_correio_dados[4]=0;
    caixa_de_correio_dados[5]=caixa_de_correio_dados[6]=caixa_de_correio_dados[7]=0;
    if (caixa_de_correio() && caixa_de_correio_dados[4]==0x80000008u) 팔기억킬로바이트=caixa_de_correio_dados[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    computador_registro(직렬장치 + 0x44) = 0x7ff;
    computador_registro(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    computador_registro(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    computador_registro(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    computador_registro(직렬장치 + 0x38) = 0;
    computador_registro(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
computador_Word Quadro_FTP(computador_Word Acção) { return (uint32_t)ftp_control((int)Acção); }
computador_Word Quadro_rede_Status(computador_Word entrada_VALOR_962f286b, computador_Word ÍNDICE) { return leitura_rede_Status(entrada_VALOR_962f286b, ÍNDICE); }
computador_Word Quadro_rede_Configurações(computador_Word Acção, computador_Word Endereço, computador_Word máscara_VALOR, computador_Word gateway_VALOR) { return (uint32_t)configurar_rede(Acção, Endereço, máscara_VALOR, gateway_VALOR); }
computador_Word Quadro_enviar_réplica(computador_Word Endereço, computador_Word ordem_VALOR) { return (uint32_t)START_réplica_teste(Endereço, ordem_VALOR); }
computador_Word Quadro_leitura_réplica(computador_Word entrada_VALOR_962f286b) { return (uint32_t)leitura_réplica_teste(entrada_VALOR_962f286b); }
computador_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned ÍNDICE=0; ÍNDICE<32; ÍNDICE++) Close_rede(ÍNDICE);
    for (unsigned ÍNDICE=0; ÍNDICE<4; ÍNDICE++) Quadro_controle_de_usuário(32+ÍNDICE);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (computador_registro(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    computador_registro(0xfe100020ul)=0x5a000000u | (computador_registro(0xfe100020ul)&~0xfffu) | 0x555;
    computador_registro(0xfe100024ul)=0x5a000000u | 10;
    computador_registro(0xfe10001cul)=0x5a000000u | (computador_registro(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

computador_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 em_dia_item 크기를 읽는다. */
    const uint32_t consulta_VALOR[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, solicitado_altura = 480;
    for (size_t 순번 = 0; 순번 < sizeof(consulta_VALOR)/4; 순번++) caixa_de_correio_dados[순번] = consulta_VALOR[순번];
    if (caixa_de_correio() && caixa_de_correio_dados[4] == 0x80000008u &&
        caixa_de_correio_dados[5] >= 640 && caixa_de_correio_dados[5] <= 1920 &&
        caixa_de_correio_dados[6] >= 480 && caixa_de_correio_dados[6] <= 1080) {
        요청너비 = caixa_de_correio_dados[5]; solicitado_altura = caixa_de_correio_dados[6];
    }
    const uint32_t solicitação[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, solicitado_altura,
        0x48004, 8, 0, 요청너비, solicitado_altura,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(solicitação)/4; 순번++) caixa_de_correio_dados[순번] = solicitação[순번];
    // 위 메시지의 real_dados 길이를 uso_VALOR: 태그 Acrescentar_entrada 시 duração_VALOR 불일치를 방지한다.
    caixa_de_correio_dados[0] = sizeof(solicitação);
    if (!caixa_de_correio()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned réplica_duração[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (caixa_de_correio_dados[응답들[순번]] != (0x80000000u | réplica_duração[순번])) return 0;
    uint32_t Tela_de_fundo_VALOR = caixa_de_correio_dados[28] & 0x3fffffffu;
    uint32_t Tamanho = caixa_de_correio_dados[29];
    uint32_t 받은너비 = caixa_de_correio_dados[5], RECEBER_altura = caixa_de_correio_dados[6], RECEBER_entrelinhamento = caixa_de_correio_dados[33];
    if (caixa_de_correio_dados[15] != 32 || caixa_de_correio_dados[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || RECEBER_altura < 480 || RECEBER_altura > 1080 ||
        caixa_de_correio_dados[10] < 받은너비 || caixa_de_correio_dados[11] < RECEBER_altura || caixa_de_correio_dados[23] || caixa_de_correio_dados[24] ||
        !Tela_de_fundo_VALOR || Tela_de_fundo_VALOR < 0x1000000 || (Tela_de_fundo_VALOR & 3) || RECEBER_entrelinhamento < 받은너비 * 4 || (RECEBER_entrelinhamento & 3) ||
        (uint64_t)RECEBER_entrelinhamento * RECEBER_altura > Tamanho || (uint64_t)Tela_de_fundo_VALOR + Tamanho > 0x40000000u)
        return 0;
    Quadro_Preparar_desenho((volatile uint32_t *)(uintptr_t)Tela_de_fundo_VALOR, 받은너비, RECEBER_altura, RECEBER_entrelinhamento);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 thread_VALOR. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } contexto;
static contexto 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int TI_Corrida[3] = {1, 0, 0};
static int em_dia_Tarefa;
extern void alternância_de_contexto(contexto *, contexto *);
extern void 자바작업(int32_t);
computador_Word Quadro_LUCRO(void) {
    network_poll();
    int Anterior_item = em_dia_Tarefa, Avançar_item = (Anterior_item + 1) % 3;
    while (Avançar_item != Anterior_item && !TI_Corrida[Avançar_item]) Avançar_item = (Avançar_item + 1) % 3;
    if (Avançar_item != Anterior_item) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (TI_Corrida[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        em_dia_Tarefa = Avançar_item;
        alternância_de_contexto(&작업문맥들[Anterior_item], &작업문맥들[Avançar_item]);
    }
    return 0;
}
static void Tarefa_inicialização(void) {
    자바작업(em_dia_Tarefa);
    TI_Corrida[em_dia_Tarefa] = 0;
    Quadro_LUCRO();
    커널중단("finished task resumed");
}
computador_Word Quadro_Tarefa_Criar(computador_Word identificador_VALOR) {
    if (identificador_VALOR < 1 || identificador_VALOR > 2 || TI_Corrida[identificador_VALOR]) return (uint32_t)-1;
    memset(&작업문맥들[identificador_VALOR], 0, sizeof(contexto));
    *(uint64_t *)쌓임공간들[identificador_VALOR - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identificador_VALOR].저장값[11] = (uintptr_t)Tarefa_inicialização;
    작업문맥들[identificador_VALOR].저장값[12] = (uintptr_t)(쌓임공간들[identificador_VALOR - 1] + sizeof(쌓임공간들[0]));
    TI_Corrida[identificador_VALOR] = 1;
    return 0;
}
computador_Word Quadro_Tarefa_Estado(computador_Word identificador_VALOR) { return identificador_VALOR < 3 ? TI_Corrida[identificador_VALOR] : (uint32_t)-1; }
extern computador_Word AOT_Memória_PROC(computador_Word);
extern uint32_t leitura_usuário_Estado(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
computador_Word Quadro_consulta_Sistema(computador_Word entrada_VALOR_962f286b, computador_Word ÍNDICE) {
    if (entrada_VALOR_962f286b==0) return 팔기억킬로바이트;
    if (entrada_VALOR_962f286b==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (entrada_VALOR_962f286b==2 || entrada_VALOR_962f286b==3) return AOT_Memória_PROC(entrada_VALOR_962f286b==3);
    if (entrada_VALOR_962f286b==4) return 화면준비됨 ? (보드화면너비()*Quadro_tela_altura()*4+1023)/1024 : 0;
    if (entrada_VALOR_962f286b==5) return 80*1024; /* Executar_comando email_região 16 MiB + 네 세션 보관 email_região. */
    if (entrada_VALOR_962f286b>=20) return leitura_usuário_Estado(entrada_VALOR_962f286b-20, ÍNDICE);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[em_dia_Tarefa]; }
