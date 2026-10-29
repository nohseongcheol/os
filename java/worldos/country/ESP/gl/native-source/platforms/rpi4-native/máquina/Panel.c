#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "usuario.h"
#include "../Rede_Montón/Rede_Montón.h"
typedef uintptr_t máquina_Word;
#define máquina_rexistrarse(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define caixa_de_correo_ENDEREZO 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Reloxo_CONTAR(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FRECUENCIA;
static volatile uint32_t caixa_de_correo_datos[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *datos_cargo, int código_de_carácter, size_t elemento_CONTAR) { unsigned char *Seguinte_DESPRAZAMENTO = datos_cargo; while (elemento_CONTAR--) *Seguinte_DESPRAZAMENTO++ = código_de_carácter; return datos_cargo; }
void *memcpy(void *destino_datos, const void *cadea_datos, size_t elemento_CONTAR) { unsigned char *첫째값 = destino_datos; const unsigned char *SEGUNDO_VALOR = cadea_datos; while (elemento_CONTAR--) *첫째값++ = *SEGUNDO_VALOR++; return destino_datos; }

static int caixa_de_correo(void) {
    uint32_t solicitude = (uint32_t)(uintptr_t)caixa_de_correo_datos | 8;
    uint64_t Executar_2 = Reloxo_CONTAR();
    기억장벽();
    while (máquina_rexistrarse(caixa_de_correo_ENDEREZO + 0x38) & 0x80000000u)
        if (Reloxo_CONTAR() - Executar_2 > FRECUENCIA) return 0;
    máquina_rexistrarse(caixa_de_correo_ENDEREZO + 0x20) = solicitude;
    for (;;) {
        if (!(máquina_rexistrarse(caixa_de_correo_ENDEREZO + 0x18) & 0x40000000u)) {
            uint32_t resposta = máquina_rexistrarse(caixa_de_correo_ENDEREZO);
            if (resposta == solicitude) { 기억장벽(); return caixa_de_correo_datos[1] == 0x80000000u; }
        }
        if (Reloxo_CONTAR() - Executar_2 > FRECUENCIA) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_pendente(void);
extern void Terminal_punteiro(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../remoto_VALOR/remoto_VALOR.h"
static int Secuencias;
static unsigned 직렬이전글자;
máquina_Word Panel_Secuencias(máquina_Word 사용여부) { Secuencias=사용여부!=0; return 0; }
máquina_Word Panel_Canle(máquina_Word Canle, máquina_Word código_de_carácter) {
    if(Secuencias && 자바셸출력((int32_t)Canle,(int32_t)(código_de_carácter&255))) return 0;
    Terminal_byte(código_de_carácter&255);
    원격출력(código_de_carácter&255);
    if ((código_de_carácter&255)==10 && 직렬이전글자!=13) {
        while (máquina_rexistrarse(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        máquina_rexistrarse(직렬장치)=13;
    }
    직렬이전글자=código_de_carácter&255;
    while (máquina_rexistrarse(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    máquina_rexistrarse(직렬장치) = (uint32_t)código_de_carácter & 255;
    return 0;
}
máquina_Word 보드글자쓰기(máquina_Word código_de_carácter) { return Panel_Canle(1,código_de_carácter); }
máquina_Word 보드원시글자읽기(void) {
    int remoto_carácter=원격입력();if(remoto_carácter>=0)return remoto_carácter;
    if (máquina_rexistrarse(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALOR = máquina_rexistrarse(직렬장치);
    if (VALOR & 0xf00) { máquina_rexistrarse(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALOR & 255;
}
máquina_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paquete_datos[6];
    if(Terminal_pendente())return (uint32_t)-4096;
    if(Secuencias){int32_t código_de_carácter=자바셸입력();if(código_de_carácter!=-3)return (uint32_t)código_de_carácter;}
    for(;;){
        int código_de_carácter=(int32_t)보드원시글자읽기();if(código_de_carácter<0)return (uint32_t)código_de_carácter;
        if(!꾸러미안쪽){if(código_de_carácter!=30)return código_de_carácter;꾸러미안쪽=1;사용량=0;continue;}
        paquete_datos[사용량++]=código_de_carácter;if(사용량<6)continue;꾸러미안쪽=0;
        if(paquete_datos[0]==1)Terminal_punteiro(paquete_datos[1],paquete_datos[2]+paquete_datos[3]*256,paquete_datos[4]+paquete_datos[5]*256);
        if(paquete_datos[0]==2)터미널바로가기키(paquete_datos[1]);
        if(paquete_datos[0]==3)터미널입력방식(paquete_datos[1]);
        if(Terminal_pendente())return (uint32_t)-4096;
    }
}
máquina_Word 보드밀리초(void) { return (uint32_t)(Reloxo_CONTAR() / (FRECUENCIA / 1000)); }
máquina_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *cadea_datos) { while (*cadea_datos) 보드글자쓰기((unsigned char)*cadea_datos++); }
static void 직렬열여섯진출력(máquina_Word elemento_CONTAR) { const char *열여섯진숫자 = "0123456789abcdef"; for (int cadea_datos = 60; cadea_datos >= 0; cadea_datos -= 4) 보드글자쓰기(열여섯진숫자[(elemento_CONTAR >> cadea_datos) & 15]); }
máquina_Word Panel_Stop(máquina_Word Estado_VALOR) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Estado_VALOR); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Panel_Stop(1); __builtin_unreachable(); }
void Panel_excepción(máquina_Word excepción_Estado, máquina_Word comando_cargo, máquina_Word non_válido_ENDEREZO) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(excepción_Estado);
    직렬글출력(" PC="); 직렬열여섯진출력(comando_cargo); 직렬글출력(" FAR="); 직렬열여섯진출력(non_válido_ENDEREZO);
    Panel_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    caixa_de_correo_datos[0]=32;caixa_de_correo_datos[1]=0;caixa_de_correo_datos[2]=0x10004;caixa_de_correo_datos[3]=8;caixa_de_correo_datos[4]=0;
    caixa_de_correo_datos[5]=caixa_de_correo_datos[6]=caixa_de_correo_datos[7]=0;
    return caixa_de_correo()&&caixa_de_correo_datos[4]==0x80000008u&&(caixa_de_correo_datos[5]||caixa_de_correo_datos[6]);
}
int Panel_máquina_ENDEREZO(unsigned char *ENDEREZO) {
    caixa_de_correo_datos[0]=32;caixa_de_correo_datos[1]=0;caixa_de_correo_datos[2]=0x10003;caixa_de_correo_datos[3]=8;caixa_de_correo_datos[4]=0;
    caixa_de_correo_datos[5]=caixa_de_correo_datos[6]=caixa_de_correo_datos[7]=0;
    if(!caixa_de_correo()||(caixa_de_correo_datos[4]&0x80000000u)==0||(caixa_de_correo_datos[4]&0xffff)!=6)return 0;
    const unsigned char *datos=(const unsigned char*)&caixa_de_correo_datos[5];unsigned SUMA_VALOR=0;
    for(unsigned 순번=0;순번<6;순번++){ENDEREZO[순번]=datos[순번];SUMA_VALOR|=datos[순번];}return SUMA_VALOR&&!(ENDEREZO[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FRECUENCIA));
    máquina_rexistrarse(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    máquina_rexistrarse(범용입출력 + 4) = (máquina_rexistrarse(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    máquina_rexistrarse(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. erro_VALOR 시 config.txt의 48MHz를 사용한다.
    caixa_de_correo_datos[0] = 36; caixa_de_correo_datos[1] = 0; caixa_de_correo_datos[2] = 0x38002; caixa_de_correo_datos[3] = 12;
    caixa_de_correo_datos[4] = 0; caixa_de_correo_datos[5] = 2; caixa_de_correo_datos[6] = 48000000; caixa_de_correo_datos[7] = 0; caixa_de_correo_datos[8] = 0;
    int 시계정상 = caixa_de_correo();
    uint32_t 속도 = 시계정상 && caixa_de_correo_datos[6] >= 1843200 ? caixa_de_correo_datos[6] : 48000000;
    caixa_de_correo_datos[0]=32; caixa_de_correo_datos[1]=0; caixa_de_correo_datos[2]=0x10005; caixa_de_correo_datos[3]=8; caixa_de_correo_datos[4]=0;
    caixa_de_correo_datos[5]=caixa_de_correo_datos[6]=caixa_de_correo_datos[7]=0;
    if (caixa_de_correo() && caixa_de_correo_datos[4]==0x80000008u) 팔기억킬로바이트=caixa_de_correo_datos[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    máquina_rexistrarse(직렬장치 + 0x44) = 0x7ff;
    máquina_rexistrarse(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    máquina_rexistrarse(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    máquina_rexistrarse(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    máquina_rexistrarse(직렬장치 + 0x38) = 0;
    máquina_rexistrarse(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
máquina_Word Panel_FTP(máquina_Word Acción) { return (uint32_t)ftp_control((int)Acción); }
máquina_Word Panel_Rede_estado(máquina_Word introdución_VALOR, máquina_Word ÍNDICE) { return 망상태읽기(introdución_VALOR, ÍNDICE); }
máquina_Word Panel_Rede_Configuración(máquina_Word Acción, máquina_Word ENDEREZO, máquina_Word máscara_VALOR, máquina_Word pasarela_VALOR) { return (uint32_t)configurar_Rede(Acción, ENDEREZO, máscara_VALOR, pasarela_VALOR); }
máquina_Word Panel_enviar_resposta(máquina_Word ENDEREZO, máquina_Word orde_VALOR) { return (uint32_t)응답시험시작(ENDEREZO, orde_VALOR); }
máquina_Word 보드응답읽기(máquina_Word introdución_VALOR) { return (uint32_t)응답시험읽기(introdución_VALOR); }
máquina_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned ÍNDICE=0; ÍNDICE<32; ÍNDICE++) peche_Rede(ÍNDICE);
    for (unsigned ÍNDICE=0; ÍNDICE<4; ÍNDICE++) Panel_control_do_usuario(32+ÍNDICE);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (máquina_rexistrarse(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    máquina_rexistrarse(0xfe100020ul)=0x5a000000u | (máquina_rexistrarse(0xfe100020ul)&~0xfffu) | 0x555;
    máquina_rexistrarse(0xfe100024ul)=0x5a000000u | 10;
    máquina_rexistrarse(0xfe10001cul)=0x5a000000u | (máquina_rexistrarse(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

máquina_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 ao_corrente_elemento 크기를 읽는다. */
    const uint32_t consulta_VALOR[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(consulta_VALOR)/4; 순번++) caixa_de_correo_datos[순번] = consulta_VALOR[순번];
    if (caixa_de_correo() && caixa_de_correo_datos[4] == 0x80000008u &&
        caixa_de_correo_datos[5] >= 640 && caixa_de_correo_datos[5] <= 1920 &&
        caixa_de_correo_datos[6] >= 480 && caixa_de_correo_datos[6] <= 1080) {
        요청너비 = caixa_de_correo_datos[5]; 요청높이 = caixa_de_correo_datos[6];
    }
    const uint32_t solicitude[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(solicitude)/4; 순번++) caixa_de_correo_datos[순번] = solicitude[순번];
    // 위 메시지의 real_datos 길이를 사용: 태그 Anexar_introdución 시 duración_VALOR 불일치를 방지한다.
    caixa_de_correo_datos[0] = sizeof(solicitude);
    if (!caixa_de_correo()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned resposta_duración[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (caixa_de_correo_datos[응답들[순번]] != (0x80000000u | resposta_duración[순번])) return 0;
    uint32_t Fondo_VALOR = caixa_de_correo_datos[28] & 0x3fffffffu;
    uint32_t Tamaño = caixa_de_correo_datos[29];
    uint32_t 받은너비 = caixa_de_correo_datos[5], 받은높이 = caixa_de_correo_datos[6], RECIBIDO_espazamento_entre_liñas = caixa_de_correo_datos[33];
    if (caixa_de_correo_datos[15] != 32 || caixa_de_correo_datos[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        caixa_de_correo_datos[10] < 받은너비 || caixa_de_correo_datos[11] < 받은높이 || caixa_de_correo_datos[23] || caixa_de_correo_datos[24] ||
        !Fondo_VALOR || Fondo_VALOR < 0x1000000 || (Fondo_VALOR & 3) || RECIBIDO_espazamento_entre_liñas < 받은너비 * 4 || (RECIBIDO_espazamento_entre_liñas & 3) ||
        (uint64_t)RECIBIDO_espazamento_entre_liñas * 받은높이 > Tamaño || (uint64_t)Fondo_VALOR + Tamaño > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)Fondo_VALOR, 받은너비, 받은높이, RECIBIDO_espazamento_entre_liñas);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 tema_VALOR. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int Tecnoloxía_da_información_TI_Atletismo[3] = {1, 0, 0};
static int ao_corrente_tarefa;
extern void 작업문맥바꾸기(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
máquina_Word Panel_suspender(void) {
    network_poll();
    int 이전 = ao_corrente_tarefa, Seguinte_elemento = (이전 + 1) % 3;
    while (Seguinte_elemento != 이전 && !Tecnoloxía_da_información_TI_Atletismo[Seguinte_elemento]) Seguinte_elemento = (Seguinte_elemento + 1) % 3;
    if (Seguinte_elemento != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (Tecnoloxía_da_información_TI_Atletismo[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        ao_corrente_tarefa = Seguinte_elemento;
        작업문맥바꾸기(&작업문맥들[이전], &작업문맥들[Seguinte_elemento]);
    }
    return 0;
}
static void tarefa_inicio(void) {
    자바작업(ao_corrente_tarefa);
    Tecnoloxía_da_información_TI_Atletismo[ao_corrente_tarefa] = 0;
    Panel_suspender();
    커널중단("finished task resumed");
}
máquina_Word Panel_tarefa_crear(máquina_Word 식별자) {
    if (식별자 < 1 || 식별자 > 2 || Tecnoloxía_da_información_TI_Atletismo[식별자]) return (uint32_t)-1;
    memset(&작업문맥들[식별자], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[식별자 - 1] = 0x6b6f726f7373746bull;
    작업문맥들[식별자].저장값[11] = (uintptr_t)tarefa_inicio;
    작업문맥들[식별자].저장값[12] = (uintptr_t)(쌓임공간들[식별자 - 1] + sizeof(쌓임공간들[0]));
    Tecnoloxía_da_información_TI_Atletismo[식별자] = 1;
    return 0;
}
máquina_Word Panel_tarefa_Estado(máquina_Word 식별자) { return 식별자 < 3 ? Tecnoloxía_da_información_TI_Atletismo[식별자] : (uint32_t)-1; }
extern máquina_Word 미리번역기억조회(máquina_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
máquina_Word Panel_consulta_sistema(máquina_Word introdución_VALOR, máquina_Word ÍNDICE) {
    if (introdución_VALOR==0) return 팔기억킬로바이트;
    if (introdución_VALOR==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (introdución_VALOR==2 || introdución_VALOR==3) return 미리번역기억조회(introdución_VALOR==3);
    if (introdución_VALOR==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (introdución_VALOR==5) return 80*1024; /* executar_comando 공간 16 MiB + 네 세션 보관 공간. */
    if (introdución_VALOR>=20) return 사용자상태읽기(introdución_VALOR-20, ÍNDICE);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[ao_corrente_tarefa]; }
