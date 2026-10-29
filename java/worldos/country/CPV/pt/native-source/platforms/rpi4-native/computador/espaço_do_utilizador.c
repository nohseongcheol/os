#include "../명명/기계연결이름.h"
#include "tela_informações.h"
// EL0 Executar_comando computador camada_VALOR. ficheiro dados/정책은 기존 AOT Java 커널에 위임한다.
#include "espaço_do_utilizador.h"
#include "Arquivo_ABI.h"
#include "rede_ABI.h"
#include "../rede_pilha/rede_pilha.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define computador_registro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distribuidor 0xff841000ul
#define IRQ_CPU_interface 0xff842000ul
#define tamanho_da_página 4096ul
#define acesso_favorito (1ul << 10)
#define não_Executar_Permissão (1ul << 53)
#define usuário_não_Executar (1ul << 54)
#define normal_Memória ((1ul << 2) | (3ul << 8) | acesso_favorito)
#define kernel_página (3ul | normal_Memória | não_Executar_Permissão | usuário_não_Executar)
#define usuário_de_leitura_gravação (3ul | normal_Memória | (1ul << 6) | não_Executar_Permissão | usuário_não_Executar)
#define usuário_somente_leitura (3ul | normal_Memória | (3ul << 6) | não_Executar_Permissão | usuário_não_Executar)
#define usuário_leitura_Executar (3ul | normal_Memória | (3ul << 6) | não_Executar_Permissão)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Quadro_pixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Quadro_Terminal(uintptr_t);
extern int Terminal_Pendente(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),tela_SMS(int,int,const uint32_t *,unsigned);
extern void inicializar_tela(int),화면누름(int,unsigned);
extern int usuário_CV(usuário_quadro *,void *);
extern void 사용자실수보관(void *);
extern int usuário_inserir(uintptr_t ponto_de_entrada, uintptr_t memória_de_pilha, uintptr_t 전달값);
extern void usuário_devolver(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t raiz_email[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t página_Lista[usuário_página_CONT_NÚM] __attribute__((aligned(4096)));
static uint8_t Permissões_Lista[usuário_página_CONT_NÚM];
static int Ativo, lista_de_arquivos[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int Close_soquete_empresa(unsigned identificador_de_arquivo){return identificador_de_arquivo<40?자바전문닫기(identificador_de_arquivo):자바흐름닫기(identificador_de_arquivo);}
static uint64_t FREQÜÊNCIA, data_limite_time;
static uintptr_t heap_encerrar;
// kernel_VALOR 셸이 준비한 UTF-8 argumentos. EL0에는 copiar_VALOR 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int em_pausa_Estado,interativo,리눅스규약,lista_de_arquivos[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumento_MATRIZ[8][256],Permissões_Lista[usuário_página_CONT_NÚM];
    uintptr_t memória_dinâmica; usuário_quadro execução_quadro;
    unsigned char ponto_flutuante_Estado[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int proprietário_objeto,interativo;
static uint32_t número_do_usuário[4], usuário_START_time[4], 사용자누적시각[4], usuário_execução_time[4], Avançar_número_do_usuário=10;
static unsigned char usuário_comando_nome[4][288];
uint32_t leitura_usuário_Estado(unsigned entrada_VALOR_962f286b, unsigned ÍNDICE) {
    unsigned cargo_ÍNDICE=ÍNDICE&3;
    int Estado_VALOR=(Ativo && proprietário_objeto==(int)cargo_ÍNDICE) ? 1 : 저장값[cargo_ÍNDICE].em_pausa_Estado ? 2 : 0;
    if (entrada_VALOR_962f286b==0) return Estado_VALOR;
    if (!Estado_VALOR) return 0;
    if (entrada_VALOR_962f286b==1) return número_do_usuário[cargo_ÍNDICE];
    if (entrada_VALOR_962f286b==2) {
        unsigned char *쪽들=Estado_VALOR==1?Permissões_Lista:저장값[cargo_ÍNDICE].Permissões_Lista;
        unsigned página_CONT_NÚM=0; for (unsigned 순번=0; 순번<usuário_página_CONT_NÚM; 순번++) if(쪽들[순번]) página_CONT_NÚM++;
        return página_CONT_NÚM*4;
    }
    if (entrada_VALOR_962f286b==3) return (uint32_t)보드밀리초()-usuário_START_time[cargo_ÍNDICE];
    if (entrada_VALOR_962f286b==4) return 사용자누적시각[cargo_ÍNDICE]+(Estado_VALOR==1?(uint32_t)보드밀리초()-usuário_execução_time[cargo_ÍNDICE]:0);
    if (entrada_VALOR_962f286b==5) return ÍNDICE/4<sizeof(usuário_comando_nome[0])?usuário_comando_nome[cargo_ÍNDICE][ÍNDICE/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t entrada_CONT_NÚM_8f7753a1) {
    if (Ativo || entrada_CONT_NÚM_8f7753a1 > 8) return (uint32_t)-22;
    전달인수개수 = entrada_CONT_NÚM_8f7753a1;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t PROC_ÍNDICE, uintptr_t em_dia_cargo, uintptr_t byte_dados) {
    if (Ativo || PROC_ÍNDICE >= 전달인수개수 || em_dia_cargo >= 255 || em_dia_cargo != 전달인수길이[PROC_ÍNDICE] || !byte_dados || byte_dados > 255)
        return (uint32_t)-22;
    전달인수[PROC_ÍNDICE][em_dia_cargo] = byte_dados;
    전달인수길이[PROC_ÍNDICE] = em_dia_cargo + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Relógio_VALOR(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Pare_TEMPOLIMITE(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    computador_registro(IRQ_distribuidor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TEMPOLIMITE(void) {
    uint64_t 간격 = FREQÜÊNCIA * 2, ligar = 1;
    data_limite_time = Relógio_VALOR() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(ligar) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned bloco_de_dados = 0; bloco_de_dados < 4; bloco_de_dados++) {
        raiz_email[bloco_de_dados] = (uintptr_t)가운데[bloco_de_dados] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t Endereço = ((uintptr_t)bloco_de_dados << 30) | ((uintptr_t)순번 << 21);
            가운데[bloco_de_dados][순번] = Endereço | 1 | acesso_favorito | usuário_não_Executar;
            if (Endereço >= 0xfc000000ul) 가운데[bloco_de_dados][순번] |= não_Executar_Permissão; // Device-nGnRnE
            else 가운데[bloco_de_dados][순번] |= normal_Memória; // Normal, non-cacheable
        }
    }
    for (unsigned SEGUNDO_VALOR = 0; SEGUNDO_VALOR < usuário_página_CONT_NÚM / 512; SEGUNDO_VALOR++)
        가운데[0][(usuário_BASE >> 21) + SEGUNDO_VALOR] = (uintptr_t)(página_Lista + SEGUNDO_VALOR * 512) | 3;
    for (unsigned 순번 = 0; 순번 < usuário_página_CONT_NÚM; 순번++) página_Lista[순번] = (usuário_BASE + 순번 * tamanho_da_página) | kernel_página;
    uint64_t Memória_atributo_registro = 0x4400, email_Tradução_visual = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memória_atributo_registro), "r"(email_Tradução_visual), "r"((uintptr_t)raiz_email) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t ponto_flutuante_Estado = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(ponto_flutuante_Estado) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQÜÊNCIA));
    Pare_TEMPOLIMITE();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 ponto_de_entrada_VALOR 때만 Permitir_VALOR.
    computador_registro(IRQ_distribuidor) = 0;
    computador_registro(IRQ_distribuidor + 0x180) = 0xffffffff;
    computador_registro(IRQ_distribuidor + 0x80) = 0xffffffff;
    computador_registro(IRQ_distribuidor + 0x280) = 1u << 30;
    computador_registro(IRQ_distribuidor + 0x41c) = 0x80808080;
    computador_registro(IRQ_distribuidor + 0x100) = 1u << 30;
    computador_registro(IRQ_CPU_interface + 4) = 0xff;
    computador_registro(IRQ_CPU_interface + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 TI_normal 확인할 número 있다.
    int Segurança = (computador_registro(IRQ_distribuidor + 4) & (1u << 10)) != 0;
    computador_registro(IRQ_distribuidor) = Segurança ? 1 : 3;
    computador_registro(IRQ_CPU_interface) = Segurança ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TIPO_área, computador_TIPO; uint32_t número_de_versão;
    uint64_t ponto_de_entrada, app_Cabeçalho_DESLOC, cabeçalho_da_seção_DESLOC; uint32_t Configuração_BITS;
    uint16_t executável_Cabeçalho_dimensionar, app_Cabeçalho_entrada_dimensionar, app_Cabeçalho_CONT_NÚM, cabeçalho_da_seção_entrada_dimensionar, cabeçalho_da_seção_CONT_NÚM, seção_nome_tabela_ÍNDICE;
} 실행파일머리;
typedef struct { uint32_t TIPO_área, Configuração_BITS; uint64_t DESLOC_VALOR, Endereço, 물리주소, 파일영역크기, 기억영역크기, alinhar_limite; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(usuário_quadro) == 272, "exception assembly layout");
static int 포함된범위(uint64_t DESLOC_VALOR, uint64_t Tamanho, uint64_t encerrar_DESLOC) {
    return DESLOC_VALOR <= encerrar_DESLOC && Tamanho <= encerrar_DESLOC - DESLOC_VALOR;
}
static int 부가정보검사(const unsigned char *dados_cargo, size_t Tamanho) {
    size_t em_dia_cargo = 0;
    while (포함된범위(em_dia_cargo, 12, Tamanho)) {
        uint32_t 낱말들[3]; memcpy(낱말들, dados_cargo + em_dia_cargo, 12); em_dia_cargo += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(em_dia_cargo, 이름영역크기, Tamanho) || !포함된범위(em_dia_cargo + 이름영역크기, 설명크기, Tamanho)) return 0;
        const unsigned char Nome[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nome) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nome); 순번++) if (dados_cargo[em_dia_cargo + 순번] != Nome[순번]) 일치 = 0;
        uint32_t número_de_versão = 0;
        if (일치) memcpy(&número_de_versão, dados_cargo + em_dia_cargo + 이름영역크기, 4);
        if (일치 && número_de_versão == 1) return 1;
        em_dia_cargo += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *dados, size_t Tamanho, int 리눅스방식) {
    if (Tamanho < sizeof(실행파일머리)) return usuário_executável_erro;
    실행파일머리 executável_Cabeçalho; memcpy(&executável_Cabeçalho, dados, sizeof(executável_Cabeçalho));
    if (executável_Cabeçalho.형식식별[0] != 127 || executável_Cabeçalho.형식식별[1] != 'E' || executável_Cabeçalho.형식식별[2] != 'L' || executável_Cabeçalho.형식식별[3] != 'F' ||
        executável_Cabeçalho.형식식별[4] != 2 || executável_Cabeçalho.형식식별[5] != 1 || executável_Cabeçalho.형식식별[6] != 1 || (executável_Cabeçalho.형식식별[7] != 0 && (!리눅스방식 || executável_Cabeçalho.형식식별[7] != 3)) ||
        executável_Cabeçalho.TIPO_área != 2 || executável_Cabeçalho.computador_TIPO != 183 || executável_Cabeçalho.número_de_versão != 1 || executável_Cabeçalho.Configuração_BITS || executável_Cabeçalho.executável_Cabeçalho_dimensionar != sizeof(executável_Cabeçalho) ||
        executável_Cabeçalho.app_Cabeçalho_entrada_dimensionar != sizeof(실행파일구획) || !executável_Cabeçalho.app_Cabeçalho_CONT_NÚM || executável_Cabeçalho.app_Cabeçalho_CONT_NÚM > 16 ||
        executável_Cabeçalho.app_Cabeçalho_DESLOC < sizeof(executável_Cabeçalho) || !포함된범위(executável_Cabeçalho.app_Cabeçalho_DESLOC, (uint64_t)executável_Cabeçalho.app_Cabeçalho_CONT_NÚM * sizeof(실행파일구획), Tamanho)) return usuário_executável_erro;
    uint8_t 사용량[(usuário_foto_encerrar - usuário_BASE) / tamanho_da_página] = {0};
    int válido_ponto_de_entrada = 0, ABI_OK = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < executável_Cabeçalho.app_Cabeçalho_CONT_NÚM; 순번++) {
        실행파일구획 dados_cargo; memcpy(&dados_cargo, dados + executável_Cabeçalho.app_Cabeçalho_DESLOC + 순번 * sizeof(dados_cargo), sizeof(dados_cargo));
        if (dados_cargo.TIPO_área == 4) {
            if (!포함된범위(dados_cargo.DESLOC_VALOR, dados_cargo.파일영역크기, Tamanho)) return usuário_executável_erro;
            if (부가정보검사(dados + dados_cargo.DESLOC_VALOR, dados_cargo.파일영역크기)) ABI_OK = 1;
            continue;
        }
        if (dados_cargo.TIPO_área == 0 || dados_cargo.TIPO_área == 6 || (dados_cargo.TIPO_área == 0x6474e551 && !(dados_cargo.Configuração_BITS & 1))) continue;
        if (dados_cargo.TIPO_área != 1) return usuário_executável_erro; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!dados_cargo.기억영역크기) continue;
        if (dados_cargo.Configuração_BITS & ~7u || !(dados_cargo.Configuração_BITS & 4) || (dados_cargo.Configuração_BITS & 3) == 3 || dados_cargo.파일영역크기 > dados_cargo.기억영역크기 ||
            (dados_cargo.파일영역크기 && !포함된범위(dados_cargo.DESLOC_VALOR, dados_cargo.파일영역크기, Tamanho)) || dados_cargo.Endereço < usuário_BASE ||
            !포함된범위(dados_cargo.Endereço, dados_cargo.기억영역크기, usuário_foto_encerrar) ||
            (!리눅스방식 && ((dados_cargo.Endereço & (tamanho_da_página - 1)) || (dados_cargo.DESLOC_VALOR & (tamanho_da_página - 1)) || dados_cargo.alinhar_limite != tamanho_da_página)) ||
            (리눅스방식 && (((dados_cargo.Endereço ^ dados_cargo.DESLOC_VALOR) & (tamanho_da_página - 1)) || !dados_cargo.alinhar_limite ||
                (dados_cargo.alinhar_limite & (dados_cargo.alinhar_limite - 1)) || dados_cargo.alinhar_limite > 0x200000 || ((dados_cargo.Endereço ^ dados_cargo.DESLOC_VALOR) & (dados_cargo.alinhar_limite - 1))))) return usuário_executável_erro;
        unsigned 첫항목 = (dados_cargo.Endereço - usuário_BASE) / tamanho_da_página;
        unsigned entrada_CONT_NÚM_8f7753a1 = ((dados_cargo.Endereço & (tamanho_da_página - 1)) + dados_cargo.기억영역크기 + tamanho_da_página - 1) / tamanho_da_página;
        for (unsigned página_VALOR = 첫항목; página_VALOR < 첫항목 + entrada_CONT_NÚM_8f7753a1; página_VALOR++) {
            if (사용량[página_VALOR]) return usuário_executável_erro;
            사용량[página_VALOR] = 1;
        }
        if ((dados_cargo.Configuração_BITS & 1) && executável_Cabeçalho.ponto_de_entrada >= dados_cargo.Endereço && executável_Cabeçalho.ponto_de_entrada < dados_cargo.Endereço + dados_cargo.파일영역크기 && !(executável_Cabeçalho.ponto_de_entrada & 3)) válido_ponto_de_entrada = 1;
        적재구획++;
    }
    return válido_ponto_de_entrada && (리눅스방식 ? !ABI_OK : ABI_OK) && 적재구획 ? 0 : usuário_executável_erro;
}
int 사용자실행파일검사(const unsigned char *dados, size_t Tamanho) { return 실행파일검사(dados, Tamanho, 0); }
static void layout_da_página(uintptr_t Endereço, uint64_t Configuração_BITS, unsigned permissões) {
    unsigned PROC_ÍNDICE = (Endereço - usuário_BASE) / tamanho_da_página;
    página_Lista[PROC_ÍNDICE] = Endereço | Configuração_BITS;
    Permissões_Lista[PROC_ÍNDICE] = permissões;
}
static int usuário_alcance(uintptr_t Endereço, size_t entrada_CONT_NÚM_8f7753a1, int 쓰는중) {
    if (Endereço < usuário_BASE || !포함된범위(Endereço, entrada_CONT_NÚM_8f7753a1, usuário_encerrar)) return 0;
    if (!entrada_CONT_NÚM_8f7753a1) return 1;
    unsigned 첫항목 = (Endereço - usuário_BASE) / tamanho_da_página, 마지막 = (Endereço + entrada_CONT_NÚM_8f7753a1 - 1 - usuário_BASE) / tamanho_da_página;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Permissões_Lista[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int copiar_caminho(uintptr_t Endereço, char *caminho) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!usuário_alcance(Endereço, 1, 0)) return -14;
        caminho[순번] = *(const char *)Endereço++;
        if (!caminho[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_RC(intptr_t resultado) { return resultado < 0 ? -número_do_erro : resultado; }
static int 대응파일기술자(uint64_t identificador_de_arquivo) { return identificador_de_arquivo >= 3 && identificador_de_arquivo < 19 ? lista_de_arquivos[identificador_de_arquivo - 3] : -1; }
static int soquete_empresa_proprietário(uint64_t identificador_de_arquivo) { return identificador_de_arquivo >= 32 && identificador_de_arquivo < 56 && 통신끝점들[identificador_de_arquivo - 32]; }
static int email_entrada(uintptr_t 가리킴값, size_t duração_VALOR, struct pk_sockaddr_in *Endereço) {
    if (duração_VALOR != sizeof(*Endereço)) return -22;
    if (!usuário_alcance(가리킴값, duração_VALOR, 0)) return -14;
    memcpy(Endereço, (const void *)가리킴값, sizeof(*Endereço));
    return Endereço->sin_family == AF_INET ? 0 : -97;
}
static int email_saída_cheque(uintptr_t 가리킴값, uintptr_t duração_ponteiro, pk_socklen_t *buffer_capacidade) {
    if (!usuário_alcance(duração_ponteiro, sizeof(*buffer_capacidade), 1)) return -14;
    memcpy(buffer_capacidade, (const void *)duração_ponteiro, sizeof(*buffer_capacidade));
    if (*buffer_capacidade > sizeof(struct pk_sockaddr_in)) *buffer_capacidade = sizeof(struct pk_sockaddr_in);
    if (*buffer_capacidade && !usuário_alcance(가리킴값, *buffer_capacidade, 1)) return -14;
    return 0;
}
static void email_saída(uintptr_t 가리킴값, uintptr_t duração_ponteiro, pk_socklen_t buffer_capacidade, int Endereço, int número_da_porta) {
    struct pk_sockaddr_in VALOR; memset(&VALOR, 0, sizeof(VALOR));
    VALOR.sin_family = AF_INET; VALOR.sin_port = pk_htons(número_da_porta); VALOR.sin_addr.s_addr = pk_htonl(Endereço);
    if (buffer_capacidade) memcpy((void *)가리킴값, &VALOR, buffer_capacidade);
    pk_socklen_t duração_VALOR = sizeof(VALOR); memcpy((void *)duração_ponteiro, &duração_VALOR, sizeof(duração_VALOR));
}
extern uintptr_t Quadro_Canal(uintptr_t, uintptr_t);
static intptr_t nativo_Sistema_Ligar(usuário_quadro *Arquivo_entrada) {
    uintptr_t 첫째값 = Arquivo_entrada->registro_dados[0], SEGUNDO_VALOR = Arquivo_entrada->registro_dados[1], ponto_de_código = Arquivo_entrada->registro_dados[2];
    char caminho[65];
    int identificador_de_arquivo, resultado;
    switch (Arquivo_entrada->registro_dados[8]) {
    case 0: return 1; // nativo ABI 버전
    case 1: // write: ponteiro 전체를 검사한 BACK_VALOR saídaTexto/ficheiro alterar_VALOR
        if (ponto_de_código > 65536) return -22;
        if (!usuário_alcance(SEGUNDO_VALOR, ponto_de_código, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_saída=Relógio_VALOR();
            for (size_t 순번 = 0; 순번 < ponto_de_código; 순번++) Quadro_Canal(첫째값, ((const unsigned char *)SEGUNDO_VALOR)[순번]);
            /* 큰 tty를 그린 kernel_VALOR 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interativo){
                data_limite_time+=Relógio_VALOR()-START_saída;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(data_limite_time) : "memory");
            }
            return ponto_de_código;
        }
        if(첫째값>=40&&soquete_empresa_proprietário(첫째값)){
            size_t item_CONT_NÚM=ponto_de_código>512?512:ponto_de_código;for(size_t 순번=0;순번<item_CONT_NÚM;순번++)자바전문넣기(순번,((const unsigned char *)SEGUNDO_VALOR)[순번]);return 자바흐름쓰기(첫째값,item_CONT_NÚM);
        }
        identificador_de_arquivo = 대응파일기술자(첫째값); if (identificador_de_arquivo < 0) return -9;
        return kernel_RC(pk_write(identificador_de_arquivo, (const void *)SEGUNDO_VALOR, ponto_de_código));
    case 2:
        if (ponto_de_código > 65536) return -22;
        if (!usuário_alcance(SEGUNDO_VALOR, ponto_de_código, 1)) return -14;
        if (첫째값 == 0) {
            size_t item_CONT_NÚM = 0;
            while (item_CONT_NÚM < ponto_de_código) {
                int caractere_VALOR = (int32_t)보드글자읽기(); if (caractere_VALOR == -2) return item_CONT_NÚM; if (caractere_VALOR < 0) break;
                ((unsigned char *)SEGUNDO_VALOR)[item_CONT_NÚM++] = caractere_VALOR;
            }
            return item_CONT_NÚM ? (intptr_t)item_CONT_NÚM : (ponto_de_código ? -11 : 0);
        }
        if(첫째값>=40&&soquete_empresa_proprietário(첫째값)){
            resultado=자바흐름읽기(첫째값,ponto_de_código>512?512:ponto_de_código);if(resultado>0)for(int 순번=0;순번<resultado;순번++)((unsigned char *)SEGUNDO_VALOR)[순번]=자바전문얻기(순번);return resultado;
        }
        identificador_de_arquivo = 대응파일기술자(첫째값); if (identificador_de_arquivo < 0) return -9;
        return kernel_RC(pk_read(identificador_de_arquivo, (void *)SEGUNDO_VALOR, ponto_de_código));
    case 3:
        resultado = copiar_caminho(첫째값, caminho); if (resultado) return resultado;
        if (SEGUNDO_VALOR > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (lista_de_arquivos[순번] < 0) {
            identificador_de_arquivo = pk_open(caminho, (int)SEGUNDO_VALOR, 0600);
            if (identificador_de_arquivo < 0) return -número_do_erro;
            lista_de_arquivos[순번] = identificador_de_arquivo; return 순번 + 3;
        }
        return -24;
    case 4:
        if (soquete_empresa_proprietário(첫째값)) { resultado = Close_soquete_empresa(첫째값); if (!resultado) 통신끝점들[첫째값 - 32] = 0; return resultado; }
        identificador_de_arquivo = 대응파일기술자(첫째값); if (identificador_de_arquivo < 0) return -9;
        resultado = pk_close(identificador_de_arquivo); if (!resultado) lista_de_arquivos[첫째값 - 3] = -1;
        return kernel_RC(resultado);
    case 5:
        identificador_de_arquivo = 대응파일기술자(첫째값); if (identificador_de_arquivo < 0) return -9;
        if (ponto_de_código > 2) return -22;
        return kernel_RC(pk_lseek(identificador_de_arquivo, (int64_t)SEGUNDO_VALOR, ponto_de_código));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 espaço_do_utilizador RW/NX heap_VALOR, 새로 노출되는 페이지는 0으로 inicializar
        if (!첫째값) return heap_encerrar;
        if (첫째값 < usuário_foto_encerrar || 첫째값 > usuário_heap_encerrar) return -12;
        uintptr_t 이전쪽들 = (heap_encerrar + tamanho_da_página - 1) & ~(tamanho_da_página - 1);
        uintptr_t 새쪽들 = (첫째값 + tamanho_da_página - 1) & ~(tamanho_da_página - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t dados_cargo = 이전쪽들; dados_cargo < 새쪽들; dados_cargo += tamanho_da_página) layout_da_página(dados_cargo, kernel_página, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t dados_cargo = 이전쪽들; dados_cargo < 새쪽들; dados_cargo += tamanho_da_página) layout_da_página(dados_cargo, usuário_de_leitura_gravação, 3);
        } else {
            for (uintptr_t dados_cargo = 새쪽들; dados_cargo < 이전쪽들; dados_cargo += tamanho_da_página) {
                página_Lista[(dados_cargo - usuário_BASE) / tamanho_da_página] = 0; Permissões_Lista[(dados_cargo - usuário_BASE) / tamanho_da_página] = 0;
            }
        }
        heap_encerrar = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        identificador_de_arquivo = 대응파일기술자(첫째값); return identificador_de_arquivo < 0 ? -9 : kernel_RC(pk_size(identificador_de_arquivo));
    case 10:
        identificador_de_arquivo = 대응파일기술자(첫째값); return identificador_de_arquivo < 0 ? -9 : kernel_RC(pk_ftruncate(identificador_de_arquivo, (int64_t)SEGUNDO_VALOR));
    case 11:
        resultado = copiar_caminho(첫째값, caminho); return resultado ? resultado : kernel_RC(pk_unlink(caminho));
    case 12:
        identificador_de_arquivo = 대응파일기술자(첫째값); return identificador_de_arquivo < 0 ? -9 : kernel_RC(pk_fsync(identificador_de_arquivo));
    case 13: { // 그래픽 기초 API: espaço_do_utilizador 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Arquivo_entrada->registro_dados[3], solicitado_altura_VALOR = Arquivo_entrada->registro_dados[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), tela_duração = Quadro_tela_altura();
        if (첫째값 > 화면폭 || SEGUNDO_VALOR > tela_duração || 너비값 > 화면폭 - 첫째값 || solicitado_altura_VALOR > tela_duração - SEGUNDO_VALOR) return -22;
        for (uintptr_t Y_coordenada = SEGUNDO_VALOR; Y_coordenada < SEGUNDO_VALOR + solicitado_altura_VALOR; Y_coordenada++) for (uintptr_t coordenada_X = 첫째값; coordenada_X < 첫째값 + 너비값; coordenada_X++) Quadro_pixel(coordenada_X, Y_coordenada, ponto_de_código);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=item_CONT_NÚM; args(index,buffer,capacity)=UTF-8 duração_VALOR
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (ponto_de_código <= 전달인수길이[첫째값]) return -36;
        if (!usuário_alcance(SEGUNDO_VALOR, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEGUNDO_VALOR, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interativo=1;return Quadro_Terminal(13);}
        if(첫째값==2){interativo=0;return 0;}
        if(첫째값==3)return Quadro_Terminal(13);
        if(첫째값!=1||!interativo)return -22;
        resultado=(int32_t)보드글자읽기();
        if(resultado==-4096)return resultado;
        START_TEMPOLIMITE();return resultado<0?-11:resultado;
    case 17: { // 유한한 협력 aguarde_VALOR: comunicação 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t encerrar_time = Relógio_VALOR() + FREQÜÊNCIA * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Relógio_VALOR() < encerrar_time);
        START_TEMPOLIMITE(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 pai_VALOR·빈 폴더를 검사한다.
        if (SEGUNDO_VALOR > 2) return -22;
        resultado = copiar_caminho(첫째값, caminho); if (resultado) return resultado;
        unsigned duração_VALOR = 0; while (caminho[duração_VALOR]) duração_VALOR++;
        resultado = 자바경로시작(duração_VALOR); if (resultado < 0) return resultado;
        for (unsigned 순번 = 0; 순번 < duração_VALOR; 순번++) 자바경로바이트(순번, (unsigned char)caminho[순번]);
        return SEGUNDO_VALOR == 0 ? 자바항목종류() : SEGUNDO_VALOR == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int caractere_VALOR=(int32_t)보드글자읽기();if(caractere_VALOR==-4096)return caractere_VALOR;if(caractere_VALOR>=0)화면누름(proprietário_objeto,caractere_VALOR);START_TEMPOLIMITE();}
        if(첫째값==3&&ponto_de_código){if(!자바셸대화형())return -95;interativo=1;Quadro_Terminal(300);}
        return 화면호출(proprietário_objeto,첫째값,SEGUNDO_VALOR,ponto_de_código,Arquivo_entrada->registro_dados[3],Arquivo_entrada->registro_dados[4],Arquivo_entrada->registro_dados[5]);
    case 21:
        if(ponto_de_código>127)return -22;if(!usuário_alcance(SEGUNDO_VALOR,ponto_de_código*sizeof(uint32_t),0))return -14;
        return tela_SMS(proprietário_objeto,첫째값,(const uint32_t *)SEGUNDO_VALOR,ponto_de_código);
    case 22: // tela Tamanho consulta_VALOR: 0=너비, 1=altura_VALOR. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : Quadro_tela_altura();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEGUNDO_VALOR==SOCK_STREAM&&(ponto_de_código==0||ponto_de_código==6))resultado=자바흐름만들기();
        else if(SEGUNDO_VALOR==SOCK_DGRAM&&(ponto_de_código==0||ponto_de_código==IPPROTO_UDP))resultado=자바전문만들기(첫째값,SEGUNDO_VALOR,ponto_de_código);
        else return -93;
        if (resultado >= 32 && resultado < 56) 통신끝점들[resultado - 32] = 1;
        return resultado;
    case 33: {
        if (!soquete_empresa_proprietário(첫째값)) return -9;
        struct pk_sockaddr_in Endereço;
        resultado = email_entrada(SEGUNDO_VALOR, ponto_de_código, &Endereço); if (resultado) return resultado;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(Endereço.sin_addr.s_addr),pk_htons(Endereço.sin_port)):자바전문묶기(첫째값, pk_htonl(Endereço.sin_addr.s_addr), pk_htons(Endereço.sin_port));
    }
    case 34: {
        if (!soquete_empresa_proprietário(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Arquivo_entrada->registro_dados[3]) return -95;
        if (ponto_de_código > 512) return -90;
        if (ponto_de_código && !usuário_alcance(SEGUNDO_VALOR, ponto_de_código, 0)) return -14;
        struct pk_sockaddr_in Endereço;
        resultado = email_entrada(Arquivo_entrada->registro_dados[4], Arquivo_entrada->registro_dados[5], &Endereço); if (resultado) return resultado;
        for (unsigned 순번 = 0; 순번 < ponto_de_código; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEGUNDO_VALOR)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(Endereço.sin_addr.s_addr), pk_htons(Endereço.sin_port), ponto_de_código);
    }
    case 35: {
        if (!soquete_empresa_proprietário(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Arquivo_entrada->registro_dados[3]) return -95;
        if (ponto_de_código > 512) return -90;
        if (ponto_de_código && !usuário_alcance(SEGUNDO_VALOR, ponto_de_código, 1)) return -14;
        pk_socklen_t buffer_capacidade = 0;
        if (Arquivo_entrada->registro_dados[4]) { resultado = email_saída_cheque(Arquivo_entrada->registro_dados[4], Arquivo_entrada->registro_dados[5], &buffer_capacidade); if (resultado) return resultado; }
        resultado = 자바전문받기(첫째값, ponto_de_código); if (resultado < 0) return resultado;
        for (int 순번 = 0; 순번 < resultado; 순번++) ((unsigned char *)SEGUNDO_VALOR)[순번] = 자바전문얻기(순번);
        if (Arquivo_entrada->registro_dados[4]) email_saída(Arquivo_entrada->registro_dados[4], Arquivo_entrada->registro_dados[5], buffer_capacidade, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return resultado;
    }
    case 36: {
        if (!soquete_empresa_proprietário(첫째값)) return -9;
        pk_socklen_t buffer_capacidade;
        resultado = email_saída_cheque(SEGUNDO_VALOR, ponto_de_código, &buffer_capacidade); if (resultado) return resultado;
        email_saída(SEGUNDO_VALOR,ponto_de_código,buffer_capacidade,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!soquete_empresa_proprietário(첫째값))return -9;struct pk_sockaddr_in Endereço;
        resultado=email_entrada(SEGUNDO_VALOR,ponto_de_código,&Endereço);if(resultado)return resultado;
        return 자바흐름연결(첫째값,pk_htonl(Endereço.sin_addr.s_addr),pk_htons(Endereço.sin_port));
    }
    case 38: return 첫째값>=40&&soquete_empresa_proprietário(첫째값)?자바흐름듣기(첫째값,SEGUNDO_VALOR):-9;
    case 39:
        if(첫째값<40||!soquete_empresa_proprietário(첫째값))return -9;
        if(SEGUNDO_VALOR||ponto_de_código)return -95;resultado=자바흐름연결받기(첫째값);if(resultado>=40&&resultado<56)통신끝점들[resultado-32]=1;return resultado;
    case 40: return 첫째값>=40&&soquete_empresa_proprietário(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t chamada_ao_sistema(usuário_quadro *Arquivo_entrada) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Arquivo_entrada) : nativo_Sistema_Ligar(Arquivo_entrada);
}
static void devolver_kernel(usuário_quadro *Arquivo_entrada, int resultado) {
    Pare_TEMPOLIMITE();
    Arquivo_entrada->registro_dados[0] = (uint64_t)(int64_t)resultado;
    Arquivo_entrada->comando_cargo = (uintptr_t)usuário_devolver;
    Arquivo_entrada->código_de_estado = 0x3c5; // EL1h, DAIF masked
}
int exceção_de_usuário(usuário_quadro *Arquivo_entrada, unsigned interseção) {
    if (!Ativo || (Arquivo_entrada->código_de_estado & 15) != 0) return 0;
    if (interseção) {
        uint32_t reconhecimento_VALOR = computador_registro(IRQ_CPU_interface + 0xc), identificador_VALOR = reconhecimento_VALOR & 1023;
        if (identificador_VALOR == 30) { devolver_kernel(Arquivo_entrada, usuário_TEMPOLIMITE); computador_registro(IRQ_CPU_interface + 0x10) = reconhecimento_VALOR; return 1; }
        if (identificador_VALOR < 1020) computador_registro(IRQ_CPU_interface + 0x10) = reconhecimento_VALOR;
        return 1;
    }
    uint64_t exceção_Estado; __asm__ volatile("mrs %0, esr_el1" : "=r"(exceção_Estado));
    if (Relógio_VALOR() >= data_limite_time) { devolver_kernel(Arquivo_entrada, usuário_TEMPOLIMITE); return 1; }
    unsigned exceção_área = exceção_Estado >> 26;
    if (exceção_área == 0x15 && (exceção_Estado & 0xffff) == 0) {
        if (리눅스규약 ? Arquivo_entrada->registro_dados[8] == 93 || Arquivo_entrada->registro_dados[8] == 94 : Arquivo_entrada->registro_dados[8] == 6) devolver_kernel(Arquivo_entrada, (int)(Arquivo_entrada->registro_dados[0] & 255));
        else {
            intptr_t resultado=chamada_ao_sistema(Arquivo_entrada);
            if(resultado==-4096&&interativo){
                저장값[proprietário_objeto].execução_quadro=*Arquivo_entrada;저장값[proprietário_objeto].execução_quadro.comando_cargo-=4;
                사용자실수보관(저장값[proprietário_objeto].ponto_flutuante_Estado);devolver_kernel(Arquivo_entrada,사용자중단됨);
            }else Arquivo_entrada->registro_dados[0]=(uint64_t)resultado;
        }
    } else devolver_kernel(Arquivo_entrada, exceção_área == 0x24 ? usuário_dados_erro : exceção_área == 0x20 ? usuário_execução_erro : usuário_inválido_instrução);
    return 1;
}

// 생성된 const ELF Grupo_VALOR: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *dados; size_t Tamanho; unsigned 전달값; } app;
#include "programs.h"
static void *snapshot(unsigned cargo_ÍNDICE){return (void *)(0x04000000ul+cargo_ÍNDICE*(usuário_encerrar-usuário_BASE));}
static int fim_app(int resultado){
    사용자누적시각[proprietário_objeto]+=(uint32_t)보드밀리초()-usuário_execução_time[proprietário_objeto];
    Pare_TEMPOLIMITE();Ativo=0;
    if(resultado==사용자중단됨){
        저장된작업 *cadeia_dados=&저장값[proprietário_objeto];cadeia_dados->em_pausa_Estado=1;cadeia_dados->interativo=interativo;cadeia_dados->리눅스규약=리눅스규약;cadeia_dados->memória_dinâmica=heap_encerrar;cadeia_dados->인수개수=전달인수개수;
        memcpy(cadeia_dados->Permissões_Lista,Permissões_Lista,sizeof(Permissões_Lista));memcpy(cadeia_dados->lista_de_arquivos,lista_de_arquivos,sizeof(lista_de_arquivos));memcpy(cadeia_dados->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(cadeia_dados->argumento_MATRIZ,전달인수,sizeof(전달인수));memcpy(cadeia_dados->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<usuário_página_CONT_NÚM;순번++)if(Permissões_Lista[순번])memcpy((unsigned char *)snapshot(proprietário_objeto)+순번*tamanho_da_página,(void *)(usuário_BASE+순번*tamanho_da_página),tamanho_da_página);
    }else{
        저장값[proprietário_objeto].em_pausa_Estado=0;inicializar_tela(proprietário_objeto);
        for(unsigned 순번=0;순번<16;순번++)if(lista_de_arquivos[순번]>=0)pk_close(lista_de_arquivos[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])Close_soquete_empresa(순번+32);
    }
    for(unsigned 순번=0;순번<usuário_página_CONT_NÚM;순번++){página_Lista[순번]=0;Permissões_Lista[순번]=0;}변환표맞추기();return resultado;
}
uintptr_t Quadro_controle_de_usuário(uintptr_t Acção){
    unsigned cargo_ÍNDICE=Acção&15;if(cargo_ÍNDICE>=4||Ativo)return (uint32_t)-22;
    저장된작업 *cadeia_dados=&저장값[cargo_ÍNDICE];
    if(Acção>=32){if(cadeia_dados->em_pausa_Estado){for(unsigned 순번=0;순번<16;순번++)if(cadeia_dados->lista_de_arquivos[순번]>=0)pk_close(cadeia_dados->lista_de_arquivos[순번]);for(unsigned 순번=0;순번<24;순번++)if(cadeia_dados->통신끝점들[순번])Close_soquete_empresa(순번+32);}cadeia_dados->em_pausa_Estado=0;inicializar_tela(cargo_ÍNDICE);return 0;}
    if(Acção>=16)return cadeia_dados->em_pausa_Estado;
    if(!cadeia_dados->em_pausa_Estado)return (uint32_t)-22;
    proprietário_objeto=cargo_ÍNDICE;interativo=cadeia_dados->interativo;리눅스규약=cadeia_dados->리눅스규약;heap_encerrar=cadeia_dados->memória_dinâmica;전달인수개수=cadeia_dados->인수개수;
    memcpy(lista_de_arquivos,cadeia_dados->lista_de_arquivos,sizeof(lista_de_arquivos));memcpy(통신끝점들,cadeia_dados->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,cadeia_dados->argumento_MATRIZ,sizeof(전달인수));memcpy(전달인수길이,cadeia_dados->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<usuário_página_CONT_NÚM;순번++)página_Lista[순번]=(usuário_BASE+순번*tamanho_da_página)|kernel_página;변환표맞추기();
    memset((void *)usuário_BASE,0,usuário_encerrar-usuário_BASE);
    for(unsigned 순번=0;순번<usuário_página_CONT_NÚM;순번++)if(cadeia_dados->Permissões_Lista[순번])memcpy((void *)(usuário_BASE+순번*tamanho_da_página),(unsigned char *)snapshot(cargo_ÍNDICE)+순번*tamanho_da_página,tamanho_da_página);
    memcpy(Permissões_Lista,cadeia_dados->Permissões_Lista,sizeof(Permissões_Lista));
    for(unsigned 순번=0;순번<usuário_página_CONT_NÚM;순번++){unsigned dados_cargo=Permissões_Lista[순번];página_Lista[순번]=dados_cargo?(usuário_BASE+순번*tamanho_da_página)|(dados_cargo==3?usuário_de_leitura_gravação:dados_cargo==5?usuário_leitura_Executar:usuário_somente_leitura):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Ativo=1;cadeia_dados->em_pausa_Estado=0;START_TEMPOLIMITE();
    usuário_execução_time[proprietário_objeto]=보드밀리초();
    return (uint32_t)fim_app(usuário_CV(&cadeia_dados->execução_quadro,cadeia_dados->ponto_flutuante_Estado));
}
static int executar_app(const unsigned char *dados, size_t Tamanho, unsigned 전달값, int 리눅스방식, const char *Nome) {
    if (Ativo) return -16;
    proprietário_objeto=Quadro_Terminal(11);if(proprietário_objeto<0||proprietário_objeto>3||저장값[proprietário_objeto].em_pausa_Estado)return -16;interativo=0;
    int válido = 실행파일검사(dados, Tamanho, 리눅스방식); if (válido) return válido;
    리눅스규약 = 리눅스방식;
    unsigned nome_ÍNDICE=0;
    while (*Nome && nome_ÍNDICE<31) usuário_comando_nome[proprietário_objeto][nome_ÍNDICE++]=(unsigned char)*Nome++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nome_ÍNDICE) usuário_comando_nome[proprietário_objeto][nome_ÍNDICE++]=' ';
        for (unsigned cargo_ÍNDICE=0; cargo_ÍNDICE<전달인수길이[0]; cargo_ÍNDICE++) usuário_comando_nome[proprietário_objeto][nome_ÍNDICE++]=전달인수[0][cargo_ÍNDICE];
    }
    usuário_comando_nome[proprietário_objeto][nome_ÍNDICE]=0; número_do_usuário[proprietário_objeto]=Avançar_número_do_usuário++;
    if (Avançar_número_do_usuário>0x7fffffffu) Avançar_número_do_usuário=10;
    usuário_START_time[proprietário_objeto]=보드밀리초(); 사용자누적시각[proprietário_objeto]=0;
    for (unsigned 순번 = 0; 순번 < usuário_página_CONT_NÚM; 순번++) página_Lista[순번] = (usuário_BASE + 순번 * tamanho_da_página) | kernel_página;
    변환표맞추기();
    memset((void *)usuário_BASE, 0, usuário_encerrar - usuário_BASE);
    memset(Permissões_Lista, 0, sizeof(Permissões_Lista));
    실행파일머리 executável_Cabeçalho; memcpy(&executável_Cabeçalho, dados, sizeof(executável_Cabeçalho));
    for (unsigned 순번 = 0; 순번 < executável_Cabeçalho.app_Cabeçalho_CONT_NÚM; 순번++) {
        실행파일구획 dados_cargo; memcpy(&dados_cargo, dados + executável_Cabeçalho.app_Cabeçalho_DESLOC + 순번 * sizeof(dados_cargo), sizeof(dados_cargo));
        if (dados_cargo.TIPO_área != 1 || !dados_cargo.기억영역크기) continue;
        if (dados_cargo.파일영역크기) memcpy((void *)(uintptr_t)dados_cargo.Endereço, dados + dados_cargo.DESLOC_VALOR, dados_cargo.파일영역크기);
        for (uintptr_t em_dia_cargo = dados_cargo.Endereço & ~(tamanho_da_página - 1); em_dia_cargo < dados_cargo.Endereço + dados_cargo.기억영역크기; em_dia_cargo += tamanho_da_página) {
            Permissões_Lista[(em_dia_cargo - usuário_BASE) / tamanho_da_página] = (dados_cargo.Configuração_BITS & 2) ? 3 : ((dados_cargo.Configuração_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t em_dia_cargo = usuário_pilha_email; em_dia_cargo < usuário_encerrar; em_dia_cargo += tamanho_da_página) Permissões_Lista[(em_dia_cargo - usuário_BASE) / tamanho_da_página] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(executável_Cabeçalho.ponto_de_entrada) : usuário_encerrar;
    for (unsigned 순번 = 0; 순번 < usuário_página_CONT_NÚM; 순번++) {
        unsigned permissões = Permissões_Lista[순번];
        página_Lista[순번] = permissões ? (usuário_BASE + 순번 * tamanho_da_página) | (permissões == 3 ? usuário_de_leitura_gravação : permissões == 5 ? usuário_leitura_Executar : usuário_somente_leitura) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) lista_de_arquivos[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    heap_encerrar = usuário_foto_encerrar;
    Ativo = 1; START_TEMPOLIMITE();
    usuário_execução_time[proprietário_objeto]=보드밀리초();
    int resultado = usuário_inserir(executável_Cabeçalho.ponto_de_entrada, 초기쌓임공간, 전달값);
    return fim_app(resultado);
}
uintptr_t Quadro_usuário_executar(uintptr_t PROC_ÍNDICE) {
    if (PROC_ÍNDICE >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nome=PROC_ÍNDICE==10?"javac":PROC_ÍNDICE==11?"java":PROC_ÍNDICE==12?"python":PROC_ÍNDICE==13?"vi":PROC_ÍNDICE==14?"jar":PROC_ÍNDICE==15?"cc":PROC_ÍNDICE==16?"jaot":"ELF";
    return (uint32_t)executar_app(실행항목들[PROC_ÍNDICE].dados, 실행항목들[PROC_ÍNDICE].Tamanho, 실행항목들[PROC_ÍNDICE].전달값, 0, Nome);
}
static uintptr_t Executar_Arquivo(int 리눅스방식) {
    static unsigned char foto[16384];
    if (Ativo || !전달인수개수) return (uint32_t)-22;
    int identificador_de_arquivo = pk_open((const char *)전달인수[0], somente_leitura_VALOR, 0);
    if (identificador_de_arquivo < 0) return (uint32_t)-número_do_erro;
    int Tamanho = pk_size(identificador_de_arquivo);
    if (Tamanho < 0 || (unsigned)Tamanho > sizeof(foto)) { pk_close(identificador_de_arquivo); return (uint32_t)-27; }
    int RECEBER_CONT_NÚM = pk_read(identificador_de_arquivo, foto, Tamanho); pk_close(identificador_de_arquivo);
    if (RECEBER_CONT_NÚM != Tamanho) return (uint32_t)-5;
    return (uint32_t)executar_app(foto, Tamanho, 0, 리눅스방식, "");
}
uintptr_t Quadro_usuário_Arquivo(void) { return Executar_Arquivo(0); }
uintptr_t 보드사용자리눅스파일(void) { return Executar_Arquivo(1); }
uintptr_t Quadro_usuário_validar(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].dados, 잘못된실행항목들[순번].Tamanho) != usuário_executável_erro) return 순번 + 1;
    return 0;
}
