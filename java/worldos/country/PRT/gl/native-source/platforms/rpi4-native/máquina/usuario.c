#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 executar_comando máquina capa_VALOR. Ficheiro datos/정책은 기존 AOT Java 커널에 위임한다.
#include "usuario.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Rede_Montón/Rede_Montón.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define máquina_rexistrarse(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distribuidor 0xff841000ul
#define IRQ_CPU_interface 0xff842000ul
#define tamaño_da_páxina 4096ul
#define 접근표시 (1ul << 10)
#define non_executar_permiso (1ul << 53)
#define usuario_non_executar (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kernel_páxina (3ul | 보통기억 | non_executar_permiso | usuario_non_executar)
#define usuario_de_lectura_e_escrita (3ul | 보통기억 | (1ul << 6) | non_executar_permiso | usuario_non_executar)
#define usuario_só_de_lectura (3ul | 보통기억 | (3ul << 6) | non_executar_permiso | usuario_non_executar)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | non_executar_permiso)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Panel_píxel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Panel_Terminal(uintptr_t);
extern int Terminal_pendente(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int usuario_CV(usuario_marco *,void *);
extern void 사용자실수보관(void *);
extern int usuario_introducir(uintptr_t introdución_p, uintptr_t Montón_Almacenamento, uintptr_t 전달값);
extern void usuario_devolver(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t raíz_ENDEREZO[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t páxina_Lista[usuario_páxina_CONTAR] __attribute__((aligned(4096)));
static uint8_t Permisos_Lista[usuario_páxina_CONTAR];
static int Activo, Ficheiro_Lista[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Ficheiro_agarradoira){return Ficheiro_agarradoira<40?자바전문닫기(Ficheiro_agarradoira):자바흐름닫기(Ficheiro_agarradoira);}
static uint64_t FRECUENCIA, 마감시각;
static uintptr_t 동적기억끝;
// kernel_VALOR 셸이 준비한 UTF-8 Argumentos. EL0에는 copiar_VALOR 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interactivo,리눅스규약,Ficheiro_Lista[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumento_MATRIZ[8][256],Permisos_Lista[usuario_páxina_CONTAR];
    uintptr_t 동적기억공간; usuario_marco 실행틀;
    unsigned char flotante_p_Estado[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int propietario_obxecto,interactivo;
static uint32_t número_de_usuario[4], usuario_START_hora[4], 사용자누적시각[4], 사용자실행시각[4], Seguinte_número_de_usuario=10;
static unsigned char usuario_comando_nome[4][288];
uint32_t 사용자상태읽기(unsigned introdución_VALOR, unsigned ÍNDICE) {
    unsigned cargo_ÍNDICE=ÍNDICE&3;
    int Estado_VALOR=(Activo && propietario_obxecto==(int)cargo_ÍNDICE) ? 1 : 저장값[cargo_ÍNDICE].멈춤상태 ? 2 : 0;
    if (introdución_VALOR==0) return Estado_VALOR;
    if (!Estado_VALOR) return 0;
    if (introdución_VALOR==1) return número_de_usuario[cargo_ÍNDICE];
    if (introdución_VALOR==2) {
        unsigned char *쪽들=Estado_VALOR==1?Permisos_Lista:저장값[cargo_ÍNDICE].Permisos_Lista;
        unsigned páxina_CONTAR=0; for (unsigned 순번=0; 순번<usuario_páxina_CONTAR; 순번++) if(쪽들[순번]) páxina_CONTAR++;
        return páxina_CONTAR*4;
    }
    if (introdución_VALOR==3) return (uint32_t)보드밀리초()-usuario_START_hora[cargo_ÍNDICE];
    if (introdución_VALOR==4) return 사용자누적시각[cargo_ÍNDICE]+(Estado_VALOR==1?(uint32_t)보드밀리초()-사용자실행시각[cargo_ÍNDICE]:0);
    if (introdución_VALOR==5) return ÍNDICE/4<sizeof(usuario_comando_nome[0])?usuario_comando_nome[cargo_ÍNDICE][ÍNDICE/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t introdución_CONTAR) {
    if (Activo || introdución_CONTAR > 8) return (uint32_t)-22;
    전달인수개수 = introdución_CONTAR;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t Busca_ÍNDICE, uintptr_t ao_corrente_cargo, uintptr_t byte_datos) {
    if (Activo || Busca_ÍNDICE >= 전달인수개수 || ao_corrente_cargo >= 255 || ao_corrente_cargo != 전달인수길이[Busca_ÍNDICE] || !byte_datos || byte_datos > 255)
        return (uint32_t)-22;
    전달인수[Busca_ÍNDICE][ao_corrente_cargo] = byte_datos;
    전달인수길이[Busca_ÍNDICE] = ao_corrente_cargo + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Reloxo_VALOR(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    máquina_rexistrarse(IRQ_distribuidor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = FRECUENCIA * 2, activar = 1;
    마감시각 = Reloxo_VALOR() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(activar) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned datos_bloquear = 0; datos_bloquear < 4; datos_bloquear++) {
        raíz_ENDEREZO[datos_bloquear] = (uintptr_t)가운데[datos_bloquear] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ENDEREZO = ((uintptr_t)datos_bloquear << 30) | ((uintptr_t)순번 << 21);
            가운데[datos_bloquear][순번] = ENDEREZO | 1 | 접근표시 | usuario_non_executar;
            if (ENDEREZO >= 0xfc000000ul) 가운데[datos_bloquear][순번] |= non_executar_permiso; // Device-nGnRnE
            else 가운데[datos_bloquear][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SEGUNDO_VALOR = 0; SEGUNDO_VALOR < usuario_páxina_CONTAR / 512; SEGUNDO_VALOR++)
        가운데[0][(usuario_BASE >> 21) + SEGUNDO_VALOR] = (uintptr_t)(páxina_Lista + SEGUNDO_VALOR * 512) | 3;
    for (unsigned 순번 = 0; 순번 < usuario_páxina_CONTAR; 순번++) páxina_Lista[순번] = (usuario_BASE + 순번 * tamaño_da_páxina) | kernel_páxina;
    uint64_t Memoria_atributo_rexistrarse = 0x4400, ENDEREZO_Tradución_control = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memoria_atributo_rexistrarse), "r"(ENDEREZO_Tradución_control), "r"((uintptr_t)raíz_ENDEREZO) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t flotante_p_Estado = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(flotante_p_Estado) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FRECUENCIA));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 introdución_p_VALOR 때만 Permitir_VALOR.
    máquina_rexistrarse(IRQ_distribuidor) = 0;
    máquina_rexistrarse(IRQ_distribuidor + 0x180) = 0xffffffff;
    máquina_rexistrarse(IRQ_distribuidor + 0x80) = 0xffffffff;
    máquina_rexistrarse(IRQ_distribuidor + 0x280) = 1u << 30;
    máquina_rexistrarse(IRQ_distribuidor + 0x41c) = 0x80808080;
    máquina_rexistrarse(IRQ_distribuidor + 0x100) = 1u << 30;
    máquina_rexistrarse(IRQ_CPU_interface + 4) = 0xff;
    máquina_rexistrarse(IRQ_CPU_interface + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Seguranza = (máquina_rexistrarse(IRQ_distribuidor + 4) & (1u << 10)) != 0;
    máquina_rexistrarse(IRQ_distribuidor) = Seguranza ? 1 : 3;
    máquina_rexistrarse(IRQ_CPU_interface) = Seguranza ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TIPO_Categoría, máquina_TIPO; uint32_t 판번호;
    uint64_t introdución_p, apl_Cabeceira_DESPRAZAMENTO, sección_Cabeceira_DESPRAZAMENTO; uint32_t configuración_Servizo_de_transferencia_intelixente_en_segundo_plano;
    uint16_t 실행머리크기, 프로그램머리항목크기, apl_Cabeceira_CONTAR, 구역머리항목크기, sección_Cabeceira_CONTAR, sección_nome_táboa_ÍNDICE;
} 실행파일머리;
typedef struct { uint32_t TIPO_Categoría, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano; uint64_t DESPRAZAMENTO_VALOR, ENDEREZO, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(usuario_marco) == 272, "exception assembly layout");
static int 포함된범위(uint64_t DESPRAZAMENTO_VALOR, uint64_t Tamaño, uint64_t finalizar_DESPRAZAMENTO) {
    return DESPRAZAMENTO_VALOR <= finalizar_DESPRAZAMENTO && Tamaño <= finalizar_DESPRAZAMENTO - DESPRAZAMENTO_VALOR;
}
static int 부가정보검사(const unsigned char *datos_cargo, size_t Tamaño) {
    size_t ao_corrente_cargo = 0;
    while (포함된범위(ao_corrente_cargo, 12, Tamaño)) {
        uint32_t 낱말들[3]; memcpy(낱말들, datos_cargo + ao_corrente_cargo, 12); ao_corrente_cargo += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(ao_corrente_cargo, 이름영역크기, Tamaño) || !포함된범위(ao_corrente_cargo + 이름영역크기, 설명크기, Tamaño)) return 0;
        const unsigned char Nome[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nome) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nome); 순번++) if (datos_cargo[ao_corrente_cargo + 순번] != Nome[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, datos_cargo + ao_corrente_cargo + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        ao_corrente_cargo += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *datos, size_t Tamaño, int 리눅스방식) {
    if (Tamaño < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, datos, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TIPO_Categoría != 2 || 실행머리.máquina_TIPO != 183 || 실행머리.판번호 != 1 || 실행머리.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.프로그램머리항목크기 != sizeof(실행파일구획) || !실행머리.apl_Cabeceira_CONTAR || 실행머리.apl_Cabeceira_CONTAR > 16 ||
        실행머리.apl_Cabeceira_DESPRAZAMENTO < sizeof(실행머리) || !포함된범위(실행머리.apl_Cabeceira_DESPRAZAMENTO, (uint64_t)실행머리.apl_Cabeceira_CONTAR * sizeof(실행파일구획), Tamaño)) return 사용자실행파일오류;
    uint8_t 사용량[(usuario_IMAXE_finalizar - usuario_BASE) / tamaño_da_páxina] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.apl_Cabeceira_CONTAR; 순번++) {
        실행파일구획 datos_cargo; memcpy(&datos_cargo, datos + 실행머리.apl_Cabeceira_DESPRAZAMENTO + 순번 * sizeof(datos_cargo), sizeof(datos_cargo));
        if (datos_cargo.TIPO_Categoría == 4) {
            if (!포함된범위(datos_cargo.DESPRAZAMENTO_VALOR, datos_cargo.파일영역크기, Tamaño)) return 사용자실행파일오류;
            if (부가정보검사(datos + datos_cargo.DESPRAZAMENTO_VALOR, datos_cargo.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (datos_cargo.TIPO_Categoría == 0 || datos_cargo.TIPO_Categoría == 6 || (datos_cargo.TIPO_Categoría == 0x6474e551 && !(datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano & 1))) continue;
        if (datos_cargo.TIPO_Categoría != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!datos_cargo.기억영역크기) continue;
        if (datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano & ~7u || !(datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano & 4) || (datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano & 3) == 3 || datos_cargo.파일영역크기 > datos_cargo.기억영역크기 ||
            (datos_cargo.파일영역크기 && !포함된범위(datos_cargo.DESPRAZAMENTO_VALOR, datos_cargo.파일영역크기, Tamaño)) || datos_cargo.ENDEREZO < usuario_BASE ||
            !포함된범위(datos_cargo.ENDEREZO, datos_cargo.기억영역크기, usuario_IMAXE_finalizar) ||
            (!리눅스방식 && ((datos_cargo.ENDEREZO & (tamaño_da_páxina - 1)) || (datos_cargo.DESPRAZAMENTO_VALOR & (tamaño_da_páxina - 1)) || datos_cargo.맞춤 != tamaño_da_páxina)) ||
            (리눅스방식 && (((datos_cargo.ENDEREZO ^ datos_cargo.DESPRAZAMENTO_VALOR) & (tamaño_da_páxina - 1)) || !datos_cargo.맞춤 ||
                (datos_cargo.맞춤 & (datos_cargo.맞춤 - 1)) || datos_cargo.맞춤 > 0x200000 || ((datos_cargo.ENDEREZO ^ datos_cargo.DESPRAZAMENTO_VALOR) & (datos_cargo.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (datos_cargo.ENDEREZO - usuario_BASE) / tamaño_da_páxina;
        unsigned introdución_CONTAR = ((datos_cargo.ENDEREZO & (tamaño_da_páxina - 1)) + datos_cargo.기억영역크기 + tamaño_da_páxina - 1) / tamaño_da_páxina;
        for (unsigned páxina_VALOR = 첫항목; páxina_VALOR < 첫항목 + introdución_CONTAR; páxina_VALOR++) {
            if (사용량[páxina_VALOR]) return 사용자실행파일오류;
            사용량[páxina_VALOR] = 1;
        }
        if ((datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano & 1) && 실행머리.introdución_p >= datos_cargo.ENDEREZO && 실행머리.introdución_p < datos_cargo.ENDEREZO + datos_cargo.파일영역크기 && !(실행머리.introdución_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *datos, size_t Tamaño) { return 실행파일검사(datos, Tamaño, 0); }
static void deseño_da_páxina(uintptr_t ENDEREZO, uint64_t configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, unsigned permisos) {
    unsigned Busca_ÍNDICE = (ENDEREZO - usuario_BASE) / tamaño_da_páxina;
    páxina_Lista[Busca_ÍNDICE] = ENDEREZO | configuración_Servizo_de_transferencia_intelixente_en_segundo_plano;
    Permisos_Lista[Busca_ÍNDICE] = permisos;
}
static int usuario_intervalo(uintptr_t ENDEREZO, size_t introdución_CONTAR, int 쓰는중) {
    if (ENDEREZO < usuario_BASE || !포함된범위(ENDEREZO, introdución_CONTAR, usuario_finalizar)) return 0;
    if (!introdución_CONTAR) return 1;
    unsigned 첫항목 = (ENDEREZO - usuario_BASE) / tamaño_da_páxina, 마지막 = (ENDEREZO + introdución_CONTAR - 1 - usuario_BASE) / tamaño_da_páxina;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Permisos_Lista[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int copiar_camiño(uintptr_t ENDEREZO, char *CAMIÑO) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!usuario_intervalo(ENDEREZO, 1, 0)) return -14;
        CAMIÑO[순번] = *(const char *)ENDEREZO++;
        if (!CAMIÑO[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_medida(intptr_t RESULTANTE) { return RESULTANTE < 0 ? -número_de_erro : RESULTANTE; }
static int 대응파일기술자(uint64_t Ficheiro_agarradoira) { return Ficheiro_agarradoira >= 3 && Ficheiro_agarradoira < 19 ? Ficheiro_Lista[Ficheiro_agarradoira - 3] : -1; }
static int 통신끝점소유(uint64_t Ficheiro_agarradoira) { return Ficheiro_agarradoira >= 32 && Ficheiro_agarradoira < 56 && 통신끝점들[Ficheiro_agarradoira - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t duración_VALOR, struct pk_sockaddr_in *ENDEREZO) {
    if (duración_VALOR != sizeof(*ENDEREZO)) return -22;
    if (!usuario_intervalo(가리킴값, duración_VALOR, 0)) return -14;
    memcpy(ENDEREZO, (const void *)가리킴값, sizeof(*ENDEREZO));
    return ENDEREZO->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t duración_punteiro, pk_socklen_t *búfer_capacidade) {
    if (!usuario_intervalo(duración_punteiro, sizeof(*búfer_capacidade), 1)) return -14;
    memcpy(búfer_capacidade, (const void *)duración_punteiro, sizeof(*búfer_capacidade));
    if (*búfer_capacidade > sizeof(struct pk_sockaddr_in)) *búfer_capacidade = sizeof(struct pk_sockaddr_in);
    if (*búfer_capacidade && !usuario_intervalo(가리킴값, *búfer_capacidade, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t duración_punteiro, pk_socklen_t búfer_capacidade, int ENDEREZO, int número_do_porto) {
    struct pk_sockaddr_in VALOR; memset(&VALOR, 0, sizeof(VALOR));
    VALOR.sin_family = AF_INET; VALOR.sin_port = pk_htons(número_do_porto); VALOR.sin_addr.s_addr = pk_htonl(ENDEREZO);
    if (búfer_capacidade) memcpy((void *)가리킴값, &VALOR, búfer_capacidade);
    pk_socklen_t duración_VALOR = sizeof(VALOR); memcpy((void *)duración_punteiro, &duración_VALOR, sizeof(duración_VALOR));
}
extern uintptr_t Panel_Canle(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(usuario_marco *Ficheiro_introdución) {
    uintptr_t 첫째값 = Ficheiro_introdución->rexistrarse_datos[0], SEGUNDO_VALOR = Ficheiro_introdución->rexistrarse_datos[1], código_de_carácter = Ficheiro_introdución->rexistrarse_datos[2];
    char CAMIÑO[65];
    int Ficheiro_agarradoira, RESULTANTE;
    switch (Ficheiro_introdución->rexistrarse_datos[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: punteiro 전체를 검사한 ATRÁS_VALOR Saída/Ficheiro modificar_VALOR
        if (código_de_carácter > 65536) return -22;
        if (!usuario_intervalo(SEGUNDO_VALOR, código_de_carácter, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Reloxo_VALOR();
            for (size_t 순번 = 0; 순번 < código_de_carácter; 순번++) Panel_Canle(첫째값, ((const unsigned char *)SEGUNDO_VALOR)[순번]);
            /* 큰 tty를 그린 kernel_VALOR 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interactivo){
                마감시각+=Reloxo_VALOR()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return código_de_carácter;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t elemento_CONTAR=código_de_carácter>512?512:código_de_carácter;for(size_t 순번=0;순번<elemento_CONTAR;순번++)자바전문넣기(순번,((const unsigned char *)SEGUNDO_VALOR)[순번]);return 자바흐름쓰기(첫째값,elemento_CONTAR);
        }
        Ficheiro_agarradoira = 대응파일기술자(첫째값); if (Ficheiro_agarradoira < 0) return -9;
        return kernel_medida(pk_write(Ficheiro_agarradoira, (const void *)SEGUNDO_VALOR, código_de_carácter));
    case 2:
        if (código_de_carácter > 65536) return -22;
        if (!usuario_intervalo(SEGUNDO_VALOR, código_de_carácter, 1)) return -14;
        if (첫째값 == 0) {
            size_t elemento_CONTAR = 0;
            while (elemento_CONTAR < código_de_carácter) {
                int carácter_VALOR = (int32_t)보드글자읽기(); if (carácter_VALOR == -2) return elemento_CONTAR; if (carácter_VALOR < 0) break;
                ((unsigned char *)SEGUNDO_VALOR)[elemento_CONTAR++] = carácter_VALOR;
            }
            return elemento_CONTAR ? (intptr_t)elemento_CONTAR : (código_de_carácter ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            RESULTANTE=자바흐름읽기(첫째값,código_de_carácter>512?512:código_de_carácter);if(RESULTANTE>0)for(int 순번=0;순번<RESULTANTE;순번++)((unsigned char *)SEGUNDO_VALOR)[순번]=자바전문얻기(순번);return RESULTANTE;
        }
        Ficheiro_agarradoira = 대응파일기술자(첫째값); if (Ficheiro_agarradoira < 0) return -9;
        return kernel_medida(pk_read(Ficheiro_agarradoira, (void *)SEGUNDO_VALOR, código_de_carácter));
    case 3:
        RESULTANTE = copiar_camiño(첫째값, CAMIÑO); if (RESULTANTE) return RESULTANTE;
        if (SEGUNDO_VALOR > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Ficheiro_Lista[순번] < 0) {
            Ficheiro_agarradoira = pk_open(CAMIÑO, (int)SEGUNDO_VALOR, 0600);
            if (Ficheiro_agarradoira < 0) return -número_de_erro;
            Ficheiro_Lista[순번] = Ficheiro_agarradoira; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { RESULTANTE = 통신끝점닫기(첫째값); if (!RESULTANTE) 통신끝점들[첫째값 - 32] = 0; return RESULTANTE; }
        Ficheiro_agarradoira = 대응파일기술자(첫째값); if (Ficheiro_agarradoira < 0) return -9;
        RESULTANTE = pk_close(Ficheiro_agarradoira); if (!RESULTANTE) Ficheiro_Lista[첫째값 - 3] = -1;
        return kernel_medida(RESULTANTE);
    case 5:
        Ficheiro_agarradoira = 대응파일기술자(첫째값); if (Ficheiro_agarradoira < 0) return -9;
        if (código_de_carácter > 2) return -22;
        return kernel_medida(pk_lseek(Ficheiro_agarradoira, (int64_t)SEGUNDO_VALOR, código_de_carácter));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 usuario RW/NX 힙, 새로 노출되는 페이지는 0으로 iniciar
        if (!첫째값) return 동적기억끝;
        if (첫째값 < usuario_IMAXE_finalizar || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + tamaño_da_páxina - 1) & ~(tamaño_da_páxina - 1);
        uintptr_t 새쪽들 = (첫째값 + tamaño_da_páxina - 1) & ~(tamaño_da_páxina - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t datos_cargo = 이전쪽들; datos_cargo < 새쪽들; datos_cargo += tamaño_da_páxina) deseño_da_páxina(datos_cargo, kernel_páxina, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t datos_cargo = 이전쪽들; datos_cargo < 새쪽들; datos_cargo += tamaño_da_páxina) deseño_da_páxina(datos_cargo, usuario_de_lectura_e_escrita, 3);
        } else {
            for (uintptr_t datos_cargo = 새쪽들; datos_cargo < 이전쪽들; datos_cargo += tamaño_da_páxina) {
                páxina_Lista[(datos_cargo - usuario_BASE) / tamaño_da_páxina] = 0; Permisos_Lista[(datos_cargo - usuario_BASE) / tamaño_da_páxina] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Ficheiro_agarradoira = 대응파일기술자(첫째값); return Ficheiro_agarradoira < 0 ? -9 : kernel_medida(pk_size(Ficheiro_agarradoira));
    case 10:
        Ficheiro_agarradoira = 대응파일기술자(첫째값); return Ficheiro_agarradoira < 0 ? -9 : kernel_medida(pk_ftruncate(Ficheiro_agarradoira, (int64_t)SEGUNDO_VALOR));
    case 11:
        RESULTANTE = copiar_camiño(첫째값, CAMIÑO); return RESULTANTE ? RESULTANTE : kernel_medida(pk_unlink(CAMIÑO));
    case 12:
        Ficheiro_agarradoira = 대응파일기술자(첫째값); return Ficheiro_agarradoira < 0 ? -9 : kernel_medida(pk_fsync(Ficheiro_agarradoira));
    case 13: { // 그래픽 기초 API: usuario 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Ficheiro_introdución->rexistrarse_datos[3], 높이값 = Ficheiro_introdución->rexistrarse_datos[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SEGUNDO_VALOR > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SEGUNDO_VALOR) return -22;
        for (uintptr_t Y_coordenada = SEGUNDO_VALOR; Y_coordenada < SEGUNDO_VALOR + 높이값; Y_coordenada++) for (uintptr_t X_coordenada = 첫째값; X_coordenada < 첫째값 + 너비값; X_coordenada++) Panel_píxel(X_coordenada, Y_coordenada, código_de_carácter);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=elemento_CONTAR; args(index,buffer,capacity)=UTF-8 duración_VALOR
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (código_de_carácter <= 전달인수길이[첫째값]) return -36;
        if (!usuario_intervalo(SEGUNDO_VALOR, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEGUNDO_VALOR, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interactivo=1;return Panel_Terminal(13);}
        if(첫째값==2){interactivo=0;return 0;}
        if(첫째값==3)return Panel_Terminal(13);
        if(첫째값!=1||!interactivo)return -22;
        RESULTANTE=(int32_t)보드글자읽기();
        if(RESULTANTE==-4096)return RESULTANTE;
        START_TIMEOUT();return RESULTANTE<0?-11:RESULTANTE;
    case 17: { // 유한한 협력 agarda_VALOR: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t finalizar_hora = Reloxo_VALOR() + FRECUENCIA * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Reloxo_VALOR() < finalizar_hora);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SEGUNDO_VALOR > 2) return -22;
        RESULTANTE = copiar_camiño(첫째값, CAMIÑO); if (RESULTANTE) return RESULTANTE;
        unsigned duración_VALOR = 0; while (CAMIÑO[duración_VALOR]) duración_VALOR++;
        RESULTANTE = 자바경로시작(duración_VALOR); if (RESULTANTE < 0) return RESULTANTE;
        for (unsigned 순번 = 0; 순번 < duración_VALOR; 순번++) 자바경로바이트(순번, (unsigned char)CAMIÑO[순번]);
        return SEGUNDO_VALOR == 0 ? 자바항목종류() : SEGUNDO_VALOR == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int carácter_VALOR=(int32_t)보드글자읽기();if(carácter_VALOR==-4096)return carácter_VALOR;if(carácter_VALOR>=0)화면누름(propietario_obxecto,carácter_VALOR);START_TIMEOUT();}
        if(첫째값==3&&código_de_carácter){if(!자바셸대화형())return -95;interactivo=1;Panel_Terminal(300);}
        return 화면호출(propietario_obxecto,첫째값,SEGUNDO_VALOR,código_de_carácter,Ficheiro_introdución->rexistrarse_datos[3],Ficheiro_introdución->rexistrarse_datos[4],Ficheiro_introdución->rexistrarse_datos[5]);
    case 21:
        if(código_de_carácter>127)return -22;if(!usuario_intervalo(SEGUNDO_VALOR,código_de_carácter*sizeof(uint32_t),0))return -14;
        return 화면글(propietario_obxecto,첫째값,(const uint32_t *)SEGUNDO_VALOR,código_de_carácter);
    case 22: // 화면 Tamaño consulta_VALOR: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEGUNDO_VALOR==SOCK_STREAM&&(código_de_carácter==0||código_de_carácter==6))RESULTANTE=자바흐름만들기();
        else if(SEGUNDO_VALOR==SOCK_DGRAM&&(código_de_carácter==0||código_de_carácter==IPPROTO_UDP))RESULTANTE=자바전문만들기(첫째값,SEGUNDO_VALOR,código_de_carácter);
        else return -93;
        if (RESULTANTE >= 32 && RESULTANTE < 56) 통신끝점들[RESULTANTE - 32] = 1;
        return RESULTANTE;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ENDEREZO;
        RESULTANTE = 주소입력(SEGUNDO_VALOR, código_de_carácter, &ENDEREZO); if (RESULTANTE) return RESULTANTE;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ENDEREZO.sin_addr.s_addr),pk_htons(ENDEREZO.sin_port)):자바전문묶기(첫째값, pk_htonl(ENDEREZO.sin_addr.s_addr), pk_htons(ENDEREZO.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Ficheiro_introdución->rexistrarse_datos[3]) return -95;
        if (código_de_carácter > 512) return -90;
        if (código_de_carácter && !usuario_intervalo(SEGUNDO_VALOR, código_de_carácter, 0)) return -14;
        struct pk_sockaddr_in ENDEREZO;
        RESULTANTE = 주소입력(Ficheiro_introdución->rexistrarse_datos[4], Ficheiro_introdución->rexistrarse_datos[5], &ENDEREZO); if (RESULTANTE) return RESULTANTE;
        for (unsigned 순번 = 0; 순번 < código_de_carácter; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEGUNDO_VALOR)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ENDEREZO.sin_addr.s_addr), pk_htons(ENDEREZO.sin_port), código_de_carácter);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Ficheiro_introdución->rexistrarse_datos[3]) return -95;
        if (código_de_carácter > 512) return -90;
        if (código_de_carácter && !usuario_intervalo(SEGUNDO_VALOR, código_de_carácter, 1)) return -14;
        pk_socklen_t búfer_capacidade = 0;
        if (Ficheiro_introdución->rexistrarse_datos[4]) { RESULTANTE = 주소출력검사(Ficheiro_introdución->rexistrarse_datos[4], Ficheiro_introdución->rexistrarse_datos[5], &búfer_capacidade); if (RESULTANTE) return RESULTANTE; }
        RESULTANTE = 자바전문받기(첫째값, código_de_carácter); if (RESULTANTE < 0) return RESULTANTE;
        for (int 순번 = 0; 순번 < RESULTANTE; 순번++) ((unsigned char *)SEGUNDO_VALOR)[순번] = 자바전문얻기(순번);
        if (Ficheiro_introdución->rexistrarse_datos[4]) 주소출력(Ficheiro_introdución->rexistrarse_datos[4], Ficheiro_introdución->rexistrarse_datos[5], búfer_capacidade, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return RESULTANTE;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t búfer_capacidade;
        RESULTANTE = 주소출력검사(SEGUNDO_VALOR, código_de_carácter, &búfer_capacidade); if (RESULTANTE) return RESULTANTE;
        주소출력(SEGUNDO_VALOR,código_de_carácter,búfer_capacidade,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ENDEREZO;
        RESULTANTE=주소입력(SEGUNDO_VALOR,código_de_carácter,&ENDEREZO);if(RESULTANTE)return RESULTANTE;
        return 자바흐름연결(첫째값,pk_htonl(ENDEREZO.sin_addr.s_addr),pk_htons(ENDEREZO.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SEGUNDO_VALOR):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SEGUNDO_VALOR||código_de_carácter)return -95;RESULTANTE=자바흐름연결받기(첫째값);if(RESULTANTE>=40&&RESULTANTE<56)통신끝점들[RESULTANTE-32]=1;return RESULTANTE;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(usuario_marco *Ficheiro_introdución) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Ficheiro_introdución) : 자체체계호출(Ficheiro_introdución);
}
static void devolver_kernel(usuario_marco *Ficheiro_introdución, int RESULTANTE) {
    Stop_TIMEOUT();
    Ficheiro_introdución->rexistrarse_datos[0] = (uint64_t)(int64_t)RESULTANTE;
    Ficheiro_introdución->comando_cargo = (uintptr_t)usuario_devolver;
    Ficheiro_introdución->Estado_CÓDIGO = 0x3c5; // EL1h, DAIF masked
}
int usuario_excepción(usuario_marco *Ficheiro_introdución, unsigned INTERSECCIÓN) {
    if (!Activo || (Ficheiro_introdución->Estado_CÓDIGO & 15) != 0) return 0;
    if (INTERSECCIÓN) {
        uint32_t 승인값 = máquina_rexistrarse(IRQ_CPU_interface + 0xc), 식별자 = 승인값 & 1023;
        if (식별자 == 30) { devolver_kernel(Ficheiro_introdución, usuario_TIMEOUT); máquina_rexistrarse(IRQ_CPU_interface + 0x10) = 승인값; return 1; }
        if (식별자 < 1020) máquina_rexistrarse(IRQ_CPU_interface + 0x10) = 승인값;
        return 1;
    }
    uint64_t excepción_Estado; __asm__ volatile("mrs %0, esr_el1" : "=r"(excepción_Estado));
    if (Reloxo_VALOR() >= 마감시각) { devolver_kernel(Ficheiro_introdución, usuario_TIMEOUT); return 1; }
    unsigned excepción_Categoría = excepción_Estado >> 26;
    if (excepción_Categoría == 0x15 && (excepción_Estado & 0xffff) == 0) {
        if (리눅스규약 ? Ficheiro_introdución->rexistrarse_datos[8] == 93 || Ficheiro_introdución->rexistrarse_datos[8] == 94 : Ficheiro_introdución->rexistrarse_datos[8] == 6) devolver_kernel(Ficheiro_introdución, (int)(Ficheiro_introdución->rexistrarse_datos[0] & 255));
        else {
            intptr_t RESULTANTE=체계호출(Ficheiro_introdución);
            if(RESULTANTE==-4096&&interactivo){
                저장값[propietario_obxecto].실행틀=*Ficheiro_introdución;저장값[propietario_obxecto].실행틀.comando_cargo-=4;
                사용자실수보관(저장값[propietario_obxecto].flotante_p_Estado);devolver_kernel(Ficheiro_introdución,사용자중단됨);
            }else Ficheiro_introdución->rexistrarse_datos[0]=(uint64_t)RESULTANTE;
        }
    } else devolver_kernel(Ficheiro_introdución, excepción_Categoría == 0x24 ? usuario_datos_erro : excepción_Categoría == 0x20 ? 사용자실행오류 : usuario_non_válido_instrución);
    return 1;
}

// 생성된 const ELF Grupo_VALOR: 실행은 반드시 apl_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *datos; size_t Tamaño; unsigned 전달값; } apl;
#include "programs.h"
static void *instantánea(unsigned cargo_ÍNDICE){return (void *)(0x04000000ul+cargo_ÍNDICE*(usuario_finalizar-usuario_BASE));}
static int fin_apl(int RESULTANTE){
    사용자누적시각[propietario_obxecto]+=(uint32_t)보드밀리초()-사용자실행시각[propietario_obxecto];
    Stop_TIMEOUT();Activo=0;
    if(RESULTANTE==사용자중단됨){
        저장된작업 *cadea_datos=&저장값[propietario_obxecto];cadea_datos->멈춤상태=1;cadea_datos->interactivo=interactivo;cadea_datos->리눅스규약=리눅스규약;cadea_datos->동적기억공간=동적기억끝;cadea_datos->인수개수=전달인수개수;
        memcpy(cadea_datos->Permisos_Lista,Permisos_Lista,sizeof(Permisos_Lista));memcpy(cadea_datos->Ficheiro_Lista,Ficheiro_Lista,sizeof(Ficheiro_Lista));memcpy(cadea_datos->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(cadea_datos->argumento_MATRIZ,전달인수,sizeof(전달인수));memcpy(cadea_datos->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<usuario_páxina_CONTAR;순번++)if(Permisos_Lista[순번])memcpy((unsigned char *)instantánea(propietario_obxecto)+순번*tamaño_da_páxina,(void *)(usuario_BASE+순번*tamaño_da_páxina),tamaño_da_páxina);
    }else{
        저장값[propietario_obxecto].멈춤상태=0;화면초기화(propietario_obxecto);
        for(unsigned 순번=0;순번<16;순번++)if(Ficheiro_Lista[순번]>=0)pk_close(Ficheiro_Lista[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<usuario_páxina_CONTAR;순번++){páxina_Lista[순번]=0;Permisos_Lista[순번]=0;}변환표맞추기();return RESULTANTE;
}
uintptr_t Panel_control_do_usuario(uintptr_t Acción){
    unsigned cargo_ÍNDICE=Acción&15;if(cargo_ÍNDICE>=4||Activo)return (uint32_t)-22;
    저장된작업 *cadea_datos=&저장값[cargo_ÍNDICE];
    if(Acción>=32){if(cadea_datos->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(cadea_datos->Ficheiro_Lista[순번]>=0)pk_close(cadea_datos->Ficheiro_Lista[순번]);for(unsigned 순번=0;순번<24;순번++)if(cadea_datos->통신끝점들[순번])통신끝점닫기(순번+32);}cadea_datos->멈춤상태=0;화면초기화(cargo_ÍNDICE);return 0;}
    if(Acción>=16)return cadea_datos->멈춤상태;
    if(!cadea_datos->멈춤상태)return (uint32_t)-22;
    propietario_obxecto=cargo_ÍNDICE;interactivo=cadea_datos->interactivo;리눅스규약=cadea_datos->리눅스규약;동적기억끝=cadea_datos->동적기억공간;전달인수개수=cadea_datos->인수개수;
    memcpy(Ficheiro_Lista,cadea_datos->Ficheiro_Lista,sizeof(Ficheiro_Lista));memcpy(통신끝점들,cadea_datos->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,cadea_datos->argumento_MATRIZ,sizeof(전달인수));memcpy(전달인수길이,cadea_datos->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<usuario_páxina_CONTAR;순번++)páxina_Lista[순번]=(usuario_BASE+순번*tamaño_da_páxina)|kernel_páxina;변환표맞추기();
    memset((void *)usuario_BASE,0,usuario_finalizar-usuario_BASE);
    for(unsigned 순번=0;순번<usuario_páxina_CONTAR;순번++)if(cadea_datos->Permisos_Lista[순번])memcpy((void *)(usuario_BASE+순번*tamaño_da_páxina),(unsigned char *)instantánea(cargo_ÍNDICE)+순번*tamaño_da_páxina,tamaño_da_páxina);
    memcpy(Permisos_Lista,cadea_datos->Permisos_Lista,sizeof(Permisos_Lista));
    for(unsigned 순번=0;순번<usuario_páxina_CONTAR;순번++){unsigned datos_cargo=Permisos_Lista[순번];páxina_Lista[순번]=datos_cargo?(usuario_BASE+순번*tamaño_da_páxina)|(datos_cargo==3?usuario_de_lectura_e_escrita:datos_cargo==5?사용자읽고실행:usuario_só_de_lectura):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Activo=1;cadea_datos->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[propietario_obxecto]=보드밀리초();
    return (uint32_t)fin_apl(usuario_CV(&cadea_datos->실행틀,cadea_datos->flotante_p_Estado));
}
static int executar_apl(const unsigned char *datos, size_t Tamaño, unsigned 전달값, int 리눅스방식, const char *Nome) {
    if (Activo) return -16;
    propietario_obxecto=Panel_Terminal(11);if(propietario_obxecto<0||propietario_obxecto>3||저장값[propietario_obxecto].멈춤상태)return -16;interactivo=0;
    int 유효함 = 실행파일검사(datos, Tamaño, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned nome_ÍNDICE=0;
    while (*Nome && nome_ÍNDICE<31) usuario_comando_nome[propietario_obxecto][nome_ÍNDICE++]=(unsigned char)*Nome++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nome_ÍNDICE) usuario_comando_nome[propietario_obxecto][nome_ÍNDICE++]=' ';
        for (unsigned cargo_ÍNDICE=0; cargo_ÍNDICE<전달인수길이[0]; cargo_ÍNDICE++) usuario_comando_nome[propietario_obxecto][nome_ÍNDICE++]=전달인수[0][cargo_ÍNDICE];
    }
    usuario_comando_nome[propietario_obxecto][nome_ÍNDICE]=0; número_de_usuario[propietario_obxecto]=Seguinte_número_de_usuario++;
    if (Seguinte_número_de_usuario>0x7fffffffu) Seguinte_número_de_usuario=10;
    usuario_START_hora[propietario_obxecto]=보드밀리초(); 사용자누적시각[propietario_obxecto]=0;
    for (unsigned 순번 = 0; 순번 < usuario_páxina_CONTAR; 순번++) páxina_Lista[순번] = (usuario_BASE + 순번 * tamaño_da_páxina) | kernel_páxina;
    변환표맞추기();
    memset((void *)usuario_BASE, 0, usuario_finalizar - usuario_BASE);
    memset(Permisos_Lista, 0, sizeof(Permisos_Lista));
    실행파일머리 실행머리; memcpy(&실행머리, datos, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.apl_Cabeceira_CONTAR; 순번++) {
        실행파일구획 datos_cargo; memcpy(&datos_cargo, datos + 실행머리.apl_Cabeceira_DESPRAZAMENTO + 순번 * sizeof(datos_cargo), sizeof(datos_cargo));
        if (datos_cargo.TIPO_Categoría != 1 || !datos_cargo.기억영역크기) continue;
        if (datos_cargo.파일영역크기) memcpy((void *)(uintptr_t)datos_cargo.ENDEREZO, datos + datos_cargo.DESPRAZAMENTO_VALOR, datos_cargo.파일영역크기);
        for (uintptr_t ao_corrente_cargo = datos_cargo.ENDEREZO & ~(tamaño_da_páxina - 1); ao_corrente_cargo < datos_cargo.ENDEREZO + datos_cargo.기억영역크기; ao_corrente_cargo += tamaño_da_páxina) {
            Permisos_Lista[(ao_corrente_cargo - usuario_BASE) / tamaño_da_páxina] = (datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano & 2) ? 3 : ((datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano & 1) ? 5 : 1);
        }
    }
    for (uintptr_t ao_corrente_cargo = usuario_Montón_ENDEREZO; ao_corrente_cargo < usuario_finalizar; ao_corrente_cargo += tamaño_da_páxina) Permisos_Lista[(ao_corrente_cargo - usuario_BASE) / tamaño_da_páxina] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.introdución_p) : usuario_finalizar;
    for (unsigned 순번 = 0; 순번 < usuario_páxina_CONTAR; 순번++) {
        unsigned permisos = Permisos_Lista[순번];
        páxina_Lista[순번] = permisos ? (usuario_BASE + 순번 * tamaño_da_páxina) | (permisos == 3 ? usuario_de_lectura_e_escrita : permisos == 5 ? 사용자읽고실행 : usuario_só_de_lectura) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Ficheiro_Lista[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = usuario_IMAXE_finalizar;
    Activo = 1; START_TIMEOUT();
    사용자실행시각[propietario_obxecto]=보드밀리초();
    int RESULTANTE = usuario_introducir(실행머리.introdución_p, 초기쌓임공간, 전달값);
    return fin_apl(RESULTANTE);
}
uintptr_t Panel_usuario_executar(uintptr_t Busca_ÍNDICE) {
    if (Busca_ÍNDICE >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nome=Busca_ÍNDICE==10?"javac":Busca_ÍNDICE==11?"java":Busca_ÍNDICE==12?"python":Busca_ÍNDICE==13?"vi":Busca_ÍNDICE==14?"jar":Busca_ÍNDICE==15?"cc":Busca_ÍNDICE==16?"jaot":"ELF";
    return (uint32_t)executar_apl(실행항목들[Busca_ÍNDICE].datos, 실행항목들[Busca_ÍNDICE].Tamaño, 실행항목들[Busca_ÍNDICE].전달값, 0, Nome);
}
static uintptr_t executar_Ficheiro(int 리눅스방식) {
    static unsigned char IMAXE[16384];
    if (Activo || !전달인수개수) return (uint32_t)-22;
    int Ficheiro_agarradoira = pk_open((const char *)전달인수[0], só_de_lectura_VALOR, 0);
    if (Ficheiro_agarradoira < 0) return (uint32_t)-número_de_erro;
    int Tamaño = pk_size(Ficheiro_agarradoira);
    if (Tamaño < 0 || (unsigned)Tamaño > sizeof(IMAXE)) { pk_close(Ficheiro_agarradoira); return (uint32_t)-27; }
    int RECIBIDO_CONTAR = pk_read(Ficheiro_agarradoira, IMAXE, Tamaño); pk_close(Ficheiro_agarradoira);
    if (RECIBIDO_CONTAR != Tamaño) return (uint32_t)-5;
    return (uint32_t)executar_apl(IMAXE, Tamaño, 0, 리눅스방식, "");
}
uintptr_t Panel_usuario_Ficheiro(void) { return executar_Ficheiro(0); }
uintptr_t 보드사용자리눅스파일(void) { return executar_Ficheiro(1); }
uintptr_t Panel_usuario_validar(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].datos, 잘못된실행항목들[순번].Tamaño) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
