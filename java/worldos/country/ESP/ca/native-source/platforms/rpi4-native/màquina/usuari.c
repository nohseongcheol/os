#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Executa_ordre màquina capa_VALOR. Fitxer dades/정책은 기존 AOT Java 커널에 위임한다.
#include "usuari.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../xarxa_Pila/xarxa_Pila.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define màquina_registrar_se(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define interrupció_distribuïdor 0xff841000ul
#define interrupció_CPU_interfície 0xff842000ul
#define mida_de_la_pàgina 4096ul
#define 접근표시 (1ul << 10)
#define No_Executa_permís (1ul << 53)
#define usuari_No_Executa (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define nucli_pàgina (3ul | 보통기억 | No_Executa_permís | usuari_No_Executa)
#define usuari_lectura_escriptura (3ul | 보통기억 | (1ul << 6) | No_Executa_permís | usuari_No_Executa)
#define usuari_només_de_lectura (3ul | 보통기억 | (3ul << 6) | No_Executa_permís | usuari_No_Executa)
#define usuari_tancar_Executa (3ul | 보통기억 | (3ul << 6) | No_Executa_permís)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tauler_píxel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tauler_Terminal(uintptr_t);
extern int Terminal_pendent(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int usuari_reprendre(usuari_marc *,void *);
extern void 사용자실수보관(void *);
extern int usuari_introduir(uintptr_t introducció_p, uintptr_t Pila_Emmagatzematge, uintptr_t 전달값);
extern void usuari_tornar_les_tasques(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rel_ADREÇA[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t pàgina_Llista[usuari_pàgina_COMPT] __attribute__((aligned(4096)));
static uint8_t Permisos_Llista[usuari_pàgina_COMPT];
static int Actiu, arxiu_Llista[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned arxiu_control_7f4cdfd5){return arxiu_control_7f4cdfd5<40?자바전문닫기(arxiu_control_7f4cdfd5):자바흐름닫기(arxiu_control_7f4cdfd5);}
static uint64_t FREQUENCIA, 마감시각;
static uintptr_t 동적기억끝;
// nucli_VALOR 셸이 준비한 UTF-8 인수. EL0에는 copiar_VALOR 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interactiu,리눅스규약,arxiu_Llista[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char arg_MATRIU[8][256],Permisos_Llista[usuari_pàgina_COMPT];
    uintptr_t 동적기억공간; usuari_marc 실행틀;
    unsigned char flotant_p_Estat[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int propietari_objecte,interactiu;
static uint32_t número_d_usuari[4], usuari_Inici_Hora[4], 사용자누적시각[4], 사용자실행시각[4], Següent_número_d_usuari=10;
static unsigned char usuari_ordre_nom[4][288];
uint32_t tancar_usuari_Estat(unsigned introducció_VALOR, unsigned INDEX) {
    unsigned càrrec_INDEX=INDEX&3;
    int Estat_VALOR=(Actiu && propietari_objecte==(int)càrrec_INDEX) ? 1 : 저장값[càrrec_INDEX].멈춤상태 ? 2 : 0;
    if (introducció_VALOR==0) return Estat_VALOR;
    if (!Estat_VALOR) return 0;
    if (introducció_VALOR==1) return número_d_usuari[càrrec_INDEX];
    if (introducció_VALOR==2) {
        unsigned char *쪽들=Estat_VALOR==1?Permisos_Llista:저장값[càrrec_INDEX].Permisos_Llista;
        unsigned pàgina_COMPT=0; for (unsigned 순번=0; 순번<usuari_pàgina_COMPT; 순번++) if(쪽들[순번]) pàgina_COMPT++;
        return pàgina_COMPT*4;
    }
    if (introducció_VALOR==3) return (uint32_t)보드밀리초()-usuari_Inici_Hora[càrrec_INDEX];
    if (introducció_VALOR==4) return 사용자누적시각[càrrec_INDEX]+(Estat_VALOR==1?(uint32_t)보드밀리초()-사용자실행시각[càrrec_INDEX]:0);
    if (introducció_VALOR==5) return INDEX/4<sizeof(usuari_ordre_nom[0])?usuari_ordre_nom[càrrec_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t introducció_COMPT) {
    if (Actiu || introducció_COMPT > 8) return (uint32_t)-22;
    전달인수개수 = introducció_COMPT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t Cerca_INDEX, uintptr_t 현재위치, uintptr_t byte_dades) {
    if (Actiu || Cerca_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[Cerca_INDEX] || !byte_dades || byte_dades > 255)
        return (uint32_t)-22;
    전달인수[Cerca_INDEX][현재위치] = byte_dades;
    전달인수길이[Cerca_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Rellotge_VALOR(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void aturar_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    màquina_registrar_se(interrupció_distribuïdor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Inici_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCIA * 2, activar = 1;
    마감시각 = Rellotge_VALOR() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(activar) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned dades_bloquejar = 0; dades_bloquejar < 4; dades_bloquejar++) {
        rel_ADREÇA[dades_bloquejar] = (uintptr_t)가운데[dades_bloquejar] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t Adreça = ((uintptr_t)dades_bloquejar << 30) | ((uintptr_t)순번 << 21);
            가운데[dades_bloquejar][순번] = Adreça | 1 | 접근표시 | usuari_No_Executa;
            if (Adreça >= 0xfc000000ul) 가운데[dades_bloquejar][순번] |= No_Executa_permís; // Device-nGnRnE
            else 가운데[dades_bloquejar][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SEGON_VALOR = 0; SEGON_VALOR < usuari_pàgina_COMPT / 512; SEGON_VALOR++)
        가운데[0][(usuari_BASE >> 21) + SEGON_VALOR] = (uintptr_t)(pàgina_Llista + SEGON_VALOR * 512) | 3;
    for (unsigned 순번 = 0; 순번 < usuari_pàgina_COMPT; 순번++) pàgina_Llista[순번] = (usuari_BASE + 순번 * mida_de_la_pàgina) | nucli_pàgina;
    uint64_t Memòria_atribut_registrar_se = 0x4400, ADREÇA_Traducció_control = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memòria_atribut_registrar_se), "r"(ADREÇA_Traducció_control), "r"((uintptr_t)rel_ADREÇA) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t flotant_p_Estat = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(flotant_p_Estat) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCIA));
    aturar_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 introducció_p_VALOR 때만 Permet_VALOR.
    màquina_registrar_se(interrupció_distribuïdor) = 0;
    màquina_registrar_se(interrupció_distribuïdor + 0x180) = 0xffffffff;
    màquina_registrar_se(interrupció_distribuïdor + 0x80) = 0xffffffff;
    màquina_registrar_se(interrupció_distribuïdor + 0x280) = 1u << 30;
    màquina_registrar_se(interrupció_distribuïdor + 0x41c) = 0x80808080;
    màquina_registrar_se(interrupció_distribuïdor + 0x100) = 1u << 30;
    màquina_registrar_se(interrupció_CPU_interfície + 4) = 0xff;
    màquina_registrar_se(interrupció_CPU_interfície + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Seguretat = (màquina_registrar_se(interrupció_distribuïdor + 4) & (1u << 10)) != 0;
    màquina_registrar_se(interrupció_distribuïdor) = Seguretat ? 1 : 3;
    màquina_registrar_se(interrupció_CPU_interfície) = Seguretat ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TIPUS_Categoria, màquina_TIPUS; uint32_t 판번호;
    uint64_t introducció_p, programa_Capçalera_DESPLAÇAMENT, capçalera_de_la_secció_DESPLAÇAMENT; uint32_t configuració_Servei_de_transferència_intel_ligent_en_segon_terme;
    uint16_t 실행머리크기, programa_Capçalera_introducció_canviar_la_mida, programa_Capçalera_COMPT, capçalera_de_la_secció_introducció_canviar_la_mida, capçalera_de_la_secció_COMPT, secció_nom_taula_INDEX;
} 실행파일머리;
typedef struct { uint32_t TIPUS_Categoria, configuració_Servei_de_transferència_intel_ligent_en_segon_terme; uint64_t DESPLAÇAMENT_VALOR, Adreça, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(usuari_marc) == 272, "exception assembly layout");
static int 포함된범위(uint64_t DESPLAÇAMENT_VALOR, uint64_t Mida, uint64_t finalitzar_DESPLAÇAMENT) {
    return DESPLAÇAMENT_VALOR <= finalitzar_DESPLAÇAMENT && Mida <= finalitzar_DESPLAÇAMENT - DESPLAÇAMENT_VALOR;
}
static int 부가정보검사(const unsigned char *dades_càrrec, size_t Mida) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Mida)) {
        uint32_t 낱말들[3]; memcpy(낱말들, dades_càrrec + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Mida) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Mida)) return 0;
        const unsigned char Nom[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nom) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nom); 순번++) if (dades_càrrec[현재위치 + 순번] != Nom[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, dades_càrrec + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *dades, size_t Mida, int 리눅스방식) {
    if (Mida < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, dades, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TIPUS_Categoria != 2 || 실행머리.màquina_TIPUS != 183 || 실행머리.판번호 != 1 || 실행머리.configuració_Servei_de_transferència_intel_ligent_en_segon_terme || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.programa_Capçalera_introducció_canviar_la_mida != sizeof(실행파일구획) || !실행머리.programa_Capçalera_COMPT || 실행머리.programa_Capçalera_COMPT > 16 ||
        실행머리.programa_Capçalera_DESPLAÇAMENT < sizeof(실행머리) || !포함된범위(실행머리.programa_Capçalera_DESPLAÇAMENT, (uint64_t)실행머리.programa_Capçalera_COMPT * sizeof(실행파일구획), Mida)) return 사용자실행파일오류;
    uint8_t 사용량[(usuari_IMATGE_finalitzar - usuari_BASE) / mida_de_la_pàgina] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.programa_Capçalera_COMPT; 순번++) {
        실행파일구획 dades_càrrec; memcpy(&dades_càrrec, dades + 실행머리.programa_Capçalera_DESPLAÇAMENT + 순번 * sizeof(dades_càrrec), sizeof(dades_càrrec));
        if (dades_càrrec.TIPUS_Categoria == 4) {
            if (!포함된범위(dades_càrrec.DESPLAÇAMENT_VALOR, dades_càrrec.파일영역크기, Mida)) return 사용자실행파일오류;
            if (부가정보검사(dades + dades_càrrec.DESPLAÇAMENT_VALOR, dades_càrrec.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (dades_càrrec.TIPUS_Categoria == 0 || dades_càrrec.TIPUS_Categoria == 6 || (dades_càrrec.TIPUS_Categoria == 0x6474e551 && !(dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme & 1))) continue;
        if (dades_càrrec.TIPUS_Categoria != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!dades_càrrec.기억영역크기) continue;
        if (dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme & ~7u || !(dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme & 4) || (dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme & 3) == 3 || dades_càrrec.파일영역크기 > dades_càrrec.기억영역크기 ||
            (dades_càrrec.파일영역크기 && !포함된범위(dades_càrrec.DESPLAÇAMENT_VALOR, dades_càrrec.파일영역크기, Mida)) || dades_càrrec.Adreça < usuari_BASE ||
            !포함된범위(dades_càrrec.Adreça, dades_càrrec.기억영역크기, usuari_IMATGE_finalitzar) ||
            (!리눅스방식 && ((dades_càrrec.Adreça & (mida_de_la_pàgina - 1)) || (dades_càrrec.DESPLAÇAMENT_VALOR & (mida_de_la_pàgina - 1)) || dades_càrrec.맞춤 != mida_de_la_pàgina)) ||
            (리눅스방식 && (((dades_càrrec.Adreça ^ dades_càrrec.DESPLAÇAMENT_VALOR) & (mida_de_la_pàgina - 1)) || !dades_càrrec.맞춤 ||
                (dades_càrrec.맞춤 & (dades_càrrec.맞춤 - 1)) || dades_càrrec.맞춤 > 0x200000 || ((dades_càrrec.Adreça ^ dades_càrrec.DESPLAÇAMENT_VALOR) & (dades_càrrec.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (dades_càrrec.Adreça - usuari_BASE) / mida_de_la_pàgina;
        unsigned introducció_COMPT = ((dades_càrrec.Adreça & (mida_de_la_pàgina - 1)) + dades_càrrec.기억영역크기 + mida_de_la_pàgina - 1) / mida_de_la_pàgina;
        for (unsigned pàgina_VALOR = 첫항목; pàgina_VALOR < 첫항목 + introducció_COMPT; pàgina_VALOR++) {
            if (사용량[pàgina_VALOR]) return 사용자실행파일오류;
            사용량[pàgina_VALOR] = 1;
        }
        if ((dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme & 1) && 실행머리.introducció_p >= dades_càrrec.Adreça && 실행머리.introducció_p < dades_càrrec.Adreça + dades_càrrec.파일영역크기 && !(실행머리.introducció_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *dades, size_t Mida) { return 실행파일검사(dades, Mida, 0); }
static void disposició_de_la_pàgina(uintptr_t Adreça, uint64_t configuració_Servei_de_transferència_intel_ligent_en_segon_terme, unsigned permisos) {
    unsigned Cerca_INDEX = (Adreça - usuari_BASE) / mida_de_la_pàgina;
    pàgina_Llista[Cerca_INDEX] = Adreça | configuració_Servei_de_transferència_intel_ligent_en_segon_terme;
    Permisos_Llista[Cerca_INDEX] = permisos;
}
static int usuari_interval(uintptr_t Adreça, size_t introducció_COMPT, int 쓰는중) {
    if (Adreça < usuari_BASE || !포함된범위(Adreça, introducció_COMPT, usuari_finalitzar)) return 0;
    if (!introducció_COMPT) return 1;
    unsigned 첫항목 = (Adreça - usuari_BASE) / mida_de_la_pàgina, 마지막 = (Adreça + introducció_COMPT - 1 - usuari_BASE) / mida_de_la_pàgina;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Permisos_Llista[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int copiar_camí(uintptr_t Adreça, char *Camí) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!usuari_interval(Adreça, 1, 0)) return -14;
        Camí[순번] = *(const char *)Adreça++;
        if (!Camí[순번]) return 0;
    }
    return -36;
}
static intptr_t nucli_mesura(intptr_t RESULTAT) { return RESULTAT < 0 ? -número_d_error : RESULTAT; }
static int 대응파일기술자(uint64_t arxiu_control_7f4cdfd5) { return arxiu_control_7f4cdfd5 >= 3 && arxiu_control_7f4cdfd5 < 19 ? arxiu_Llista[arxiu_control_7f4cdfd5 - 3] : -1; }
static int 통신끝점소유(uint64_t arxiu_control_7f4cdfd5) { return arxiu_control_7f4cdfd5 >= 32 && arxiu_control_7f4cdfd5 < 56 && 통신끝점들[arxiu_control_7f4cdfd5 - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t durada_VALOR, struct pk_sockaddr_in *Adreça) {
    if (durada_VALOR != sizeof(*Adreça)) return -22;
    if (!usuari_interval(가리킴값, durada_VALOR, 0)) return -14;
    memcpy(Adreça, (const void *)가리킴값, sizeof(*Adreça));
    return Adreça->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t durada_punter, pk_socklen_t *memòria_intermèdia_capacitat) {
    if (!usuari_interval(durada_punter, sizeof(*memòria_intermèdia_capacitat), 1)) return -14;
    memcpy(memòria_intermèdia_capacitat, (const void *)durada_punter, sizeof(*memòria_intermèdia_capacitat));
    if (*memòria_intermèdia_capacitat > sizeof(struct pk_sockaddr_in)) *memòria_intermèdia_capacitat = sizeof(struct pk_sockaddr_in);
    if (*memòria_intermèdia_capacitat && !usuari_interval(가리킴값, *memòria_intermèdia_capacitat, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t durada_punter, pk_socklen_t memòria_intermèdia_capacitat, int Adreça, int número_de_port) {
    struct pk_sockaddr_in VALOR; memset(&VALOR, 0, sizeof(VALOR));
    VALOR.sin_family = AF_INET; VALOR.sin_port = pk_htons(número_de_port); VALOR.sin_addr.s_addr = pk_htonl(Adreça);
    if (memòria_intermèdia_capacitat) memcpy((void *)가리킴값, &VALOR, memòria_intermèdia_capacitat);
    pk_socklen_t durada_VALOR = sizeof(VALOR); memcpy((void *)durada_punter, &durada_VALOR, sizeof(durada_VALOR));
}
extern uintptr_t Tauler_Canal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(usuari_marc *arxiu_introducció) {
    uintptr_t 첫째값 = arxiu_introducció->registrar_se_dades[0], SEGON_VALOR = arxiu_introducció->registrar_se_dades[1], codi_de_caràcter = arxiu_introducció->registrar_se_dades[2];
    char Camí[65];
    int arxiu_control_7f4cdfd5, RESULTAT;
    switch (arxiu_introducció->registrar_se_dades[8]) {
    case 0: return 1; // propi ABI 버전
    case 1: // write: punter 전체를 검사한 ENRERE_VALOR Sortida/Fitxer canviar_VALOR
        if (codi_de_caràcter > 65536) return -22;
        if (!usuari_interval(SEGON_VALOR, codi_de_caràcter, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Rellotge_VALOR();
            for (size_t 순번 = 0; 순번 < codi_de_caràcter; 순번++) Tauler_Canal(첫째값, ((const unsigned char *)SEGON_VALOR)[순번]);
            /* 큰 tty를 그린 nucli_VALOR 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interactiu){
                마감시각+=Rellotge_VALOR()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return codi_de_caràcter;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t element_COMPT=codi_de_caràcter>512?512:codi_de_caràcter;for(size_t 순번=0;순번<element_COMPT;순번++)자바전문넣기(순번,((const unsigned char *)SEGON_VALOR)[순번]);return 자바흐름쓰기(첫째값,element_COMPT);
        }
        arxiu_control_7f4cdfd5 = 대응파일기술자(첫째값); if (arxiu_control_7f4cdfd5 < 0) return -9;
        return nucli_mesura(pk_write(arxiu_control_7f4cdfd5, (const void *)SEGON_VALOR, codi_de_caràcter));
    case 2:
        if (codi_de_caràcter > 65536) return -22;
        if (!usuari_interval(SEGON_VALOR, codi_de_caràcter, 1)) return -14;
        if (첫째값 == 0) {
            size_t element_COMPT = 0;
            while (element_COMPT < codi_de_caràcter) {
                int caràcter_VALOR = (int32_t)보드글자읽기(); if (caràcter_VALOR == -2) return element_COMPT; if (caràcter_VALOR < 0) break;
                ((unsigned char *)SEGON_VALOR)[element_COMPT++] = caràcter_VALOR;
            }
            return element_COMPT ? (intptr_t)element_COMPT : (codi_de_caràcter ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            RESULTAT=자바흐름읽기(첫째값,codi_de_caràcter>512?512:codi_de_caràcter);if(RESULTAT>0)for(int 순번=0;순번<RESULTAT;순번++)((unsigned char *)SEGON_VALOR)[순번]=자바전문얻기(순번);return RESULTAT;
        }
        arxiu_control_7f4cdfd5 = 대응파일기술자(첫째값); if (arxiu_control_7f4cdfd5 < 0) return -9;
        return nucli_mesura(pk_read(arxiu_control_7f4cdfd5, (void *)SEGON_VALOR, codi_de_caràcter));
    case 3:
        RESULTAT = copiar_camí(첫째값, Camí); if (RESULTAT) return RESULTAT;
        if (SEGON_VALOR > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (arxiu_Llista[순번] < 0) {
            arxiu_control_7f4cdfd5 = pk_open(Camí, (int)SEGON_VALOR, 0600);
            if (arxiu_control_7f4cdfd5 < 0) return -número_d_error;
            arxiu_Llista[순번] = arxiu_control_7f4cdfd5; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { RESULTAT = 통신끝점닫기(첫째값); if (!RESULTAT) 통신끝점들[첫째값 - 32] = 0; return RESULTAT; }
        arxiu_control_7f4cdfd5 = 대응파일기술자(첫째값); if (arxiu_control_7f4cdfd5 < 0) return -9;
        RESULTAT = pk_close(arxiu_control_7f4cdfd5); if (!RESULTAT) arxiu_Llista[첫째값 - 3] = -1;
        return nucli_mesura(RESULTAT);
    case 5:
        arxiu_control_7f4cdfd5 = 대응파일기술자(첫째값); if (arxiu_control_7f4cdfd5 < 0) return -9;
        if (codi_de_caràcter > 2) return -22;
        return nucli_mesura(pk_lseek(arxiu_control_7f4cdfd5, (int64_t)SEGON_VALOR, codi_de_caràcter));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 usuari RW/NX 힙, 새로 노출되는 페이지는 0으로 inicialitzar
        if (!첫째값) return 동적기억끝;
        if (첫째값 < usuari_IMATGE_finalitzar || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + mida_de_la_pàgina - 1) & ~(mida_de_la_pàgina - 1);
        uintptr_t 새쪽들 = (첫째값 + mida_de_la_pàgina - 1) & ~(mida_de_la_pàgina - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t dades_càrrec = 이전쪽들; dades_càrrec < 새쪽들; dades_càrrec += mida_de_la_pàgina) disposició_de_la_pàgina(dades_càrrec, nucli_pàgina, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t dades_càrrec = 이전쪽들; dades_càrrec < 새쪽들; dades_càrrec += mida_de_la_pàgina) disposició_de_la_pàgina(dades_càrrec, usuari_lectura_escriptura, 3);
        } else {
            for (uintptr_t dades_càrrec = 새쪽들; dades_càrrec < 이전쪽들; dades_càrrec += mida_de_la_pàgina) {
                pàgina_Llista[(dades_càrrec - usuari_BASE) / mida_de_la_pàgina] = 0; Permisos_Llista[(dades_càrrec - usuari_BASE) / mida_de_la_pàgina] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        arxiu_control_7f4cdfd5 = 대응파일기술자(첫째값); return arxiu_control_7f4cdfd5 < 0 ? -9 : nucli_mesura(pk_size(arxiu_control_7f4cdfd5));
    case 10:
        arxiu_control_7f4cdfd5 = 대응파일기술자(첫째값); return arxiu_control_7f4cdfd5 < 0 ? -9 : nucli_mesura(pk_ftruncate(arxiu_control_7f4cdfd5, (int64_t)SEGON_VALOR));
    case 11:
        RESULTAT = copiar_camí(첫째값, Camí); return RESULTAT ? RESULTAT : nucli_mesura(pk_unlink(Camí));
    case 12:
        arxiu_control_7f4cdfd5 = 대응파일기술자(첫째값); return arxiu_control_7f4cdfd5 < 0 ? -9 : nucli_mesura(pk_fsync(arxiu_control_7f4cdfd5));
    case 13: { // 그래픽 기초 API: usuari 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = arxiu_introducció->registrar_se_dades[3], 높이값 = arxiu_introducció->registrar_se_dades[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SEGON_VALOR > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SEGON_VALOR) return -22;
        for (uintptr_t Y_coordenada = SEGON_VALOR; Y_coordenada < SEGON_VALOR + 높이값; Y_coordenada++) for (uintptr_t X_coordenada = 첫째값; X_coordenada < 첫째값 + 너비값; X_coordenada++) Tauler_píxel(X_coordenada, Y_coordenada, codi_de_caràcter);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=element_COMPT; args(index,buffer,capacity)=UTF-8 durada_VALOR
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (codi_de_caràcter <= 전달인수길이[첫째값]) return -36;
        if (!usuari_interval(SEGON_VALOR, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SEGON_VALOR, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interactiu=1;return Tauler_Terminal(13);}
        if(첫째값==2){interactiu=0;return 0;}
        if(첫째값==3)return Tauler_Terminal(13);
        if(첫째값!=1||!interactiu)return -22;
        RESULTAT=(int32_t)보드글자읽기();
        if(RESULTAT==-4096)return RESULTAT;
        Inici_TIMEOUT();return RESULTAT<0?-11:RESULTAT;
    case 17: { // 유한한 협력 Espera_VALOR: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t finalitzar_Hora = Rellotge_VALOR() + FREQUENCIA * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Rellotge_VALOR() < finalitzar_Hora);
        Inici_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SEGON_VALOR > 2) return -22;
        RESULTAT = copiar_camí(첫째값, Camí); if (RESULTAT) return RESULTAT;
        unsigned durada_VALOR = 0; while (Camí[durada_VALOR]) durada_VALOR++;
        RESULTAT = 자바경로시작(durada_VALOR); if (RESULTAT < 0) return RESULTAT;
        for (unsigned 순번 = 0; 순번 < durada_VALOR; 순번++) 자바경로바이트(순번, (unsigned char)Camí[순번]);
        return SEGON_VALOR == 0 ? 자바항목종류() : SEGON_VALOR == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int caràcter_VALOR=(int32_t)보드글자읽기();if(caràcter_VALOR==-4096)return caràcter_VALOR;if(caràcter_VALOR>=0)화면누름(propietari_objecte,caràcter_VALOR);Inici_TIMEOUT();}
        if(첫째값==3&&codi_de_caràcter){if(!자바셸대화형())return -95;interactiu=1;Tauler_Terminal(300);}
        return 화면호출(propietari_objecte,첫째값,SEGON_VALOR,codi_de_caràcter,arxiu_introducció->registrar_se_dades[3],arxiu_introducció->registrar_se_dades[4],arxiu_introducció->registrar_se_dades[5]);
    case 21:
        if(codi_de_caràcter>127)return -22;if(!usuari_interval(SEGON_VALOR,codi_de_caràcter*sizeof(uint32_t),0))return -14;
        return 화면글(propietari_objecte,첫째값,(const uint32_t *)SEGON_VALOR,codi_de_caràcter);
    case 22: // 화면 Mida cerca_VALOR: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SEGON_VALOR==SOCK_STREAM&&(codi_de_caràcter==0||codi_de_caràcter==6))RESULTAT=자바흐름만들기();
        else if(SEGON_VALOR==SOCK_DGRAM&&(codi_de_caràcter==0||codi_de_caràcter==IPPROTO_UDP))RESULTAT=자바전문만들기(첫째값,SEGON_VALOR,codi_de_caràcter);
        else return -93;
        if (RESULTAT >= 32 && RESULTAT < 56) 통신끝점들[RESULTAT - 32] = 1;
        return RESULTAT;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in Adreça;
        RESULTAT = 주소입력(SEGON_VALOR, codi_de_caràcter, &Adreça); if (RESULTAT) return RESULTAT;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(Adreça.sin_addr.s_addr),pk_htons(Adreça.sin_port)):자바전문묶기(첫째값, pk_htonl(Adreça.sin_addr.s_addr), pk_htons(Adreça.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (arxiu_introducció->registrar_se_dades[3]) return -95;
        if (codi_de_caràcter > 512) return -90;
        if (codi_de_caràcter && !usuari_interval(SEGON_VALOR, codi_de_caràcter, 0)) return -14;
        struct pk_sockaddr_in Adreça;
        RESULTAT = 주소입력(arxiu_introducció->registrar_se_dades[4], arxiu_introducció->registrar_se_dades[5], &Adreça); if (RESULTAT) return RESULTAT;
        for (unsigned 순번 = 0; 순번 < codi_de_caràcter; 순번++) 자바전문넣기(순번, ((const unsigned char *)SEGON_VALOR)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(Adreça.sin_addr.s_addr), pk_htons(Adreça.sin_port), codi_de_caràcter);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (arxiu_introducció->registrar_se_dades[3]) return -95;
        if (codi_de_caràcter > 512) return -90;
        if (codi_de_caràcter && !usuari_interval(SEGON_VALOR, codi_de_caràcter, 1)) return -14;
        pk_socklen_t memòria_intermèdia_capacitat = 0;
        if (arxiu_introducció->registrar_se_dades[4]) { RESULTAT = 주소출력검사(arxiu_introducció->registrar_se_dades[4], arxiu_introducció->registrar_se_dades[5], &memòria_intermèdia_capacitat); if (RESULTAT) return RESULTAT; }
        RESULTAT = 자바전문받기(첫째값, codi_de_caràcter); if (RESULTAT < 0) return RESULTAT;
        for (int 순번 = 0; 순번 < RESULTAT; 순번++) ((unsigned char *)SEGON_VALOR)[순번] = 자바전문얻기(순번);
        if (arxiu_introducció->registrar_se_dades[4]) 주소출력(arxiu_introducció->registrar_se_dades[4], arxiu_introducció->registrar_se_dades[5], memòria_intermèdia_capacitat, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return RESULTAT;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t memòria_intermèdia_capacitat;
        RESULTAT = 주소출력검사(SEGON_VALOR, codi_de_caràcter, &memòria_intermèdia_capacitat); if (RESULTAT) return RESULTAT;
        주소출력(SEGON_VALOR,codi_de_caràcter,memòria_intermèdia_capacitat,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in Adreça;
        RESULTAT=주소입력(SEGON_VALOR,codi_de_caràcter,&Adreça);if(RESULTAT)return RESULTAT;
        return 자바흐름연결(첫째값,pk_htonl(Adreça.sin_addr.s_addr),pk_htons(Adreça.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SEGON_VALOR):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SEGON_VALOR||codi_de_caràcter)return -95;RESULTAT=자바흐름연결받기(첫째값);if(RESULTAT>=40&&RESULTAT<56)통신끝점들[RESULTAT-32]=1;return RESULTAT;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(usuari_marc *arxiu_introducció) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(arxiu_introducció) : 자체체계호출(arxiu_introducció);
}
static void tornar_les_tasques_nucli(usuari_marc *arxiu_introducció, int RESULTAT) {
    aturar_TIMEOUT();
    arxiu_introducció->registrar_se_dades[0] = (uint64_t)(int64_t)RESULTAT;
    arxiu_introducció->ordre_càrrec = (uintptr_t)usuari_tornar_les_tasques;
    arxiu_introducció->Estat_CODI = 0x3c5; // EL1h, DAIF masked
}
int usuari_excepció(usuari_marc *arxiu_introducció, unsigned INTERSECCIO) {
    if (!Actiu || (arxiu_introducció->Estat_CODI & 15) != 0) return 0;
    if (INTERSECCIO) {
        uint32_t reconeixement_VALOR = màquina_registrar_se(interrupció_CPU_interfície + 0xc), identificador_VALOR = reconeixement_VALOR & 1023;
        if (identificador_VALOR == 30) { tornar_les_tasques_nucli(arxiu_introducció, usuari_TIMEOUT); màquina_registrar_se(interrupció_CPU_interfície + 0x10) = reconeixement_VALOR; return 1; }
        if (identificador_VALOR < 1020) màquina_registrar_se(interrupció_CPU_interfície + 0x10) = reconeixement_VALOR;
        return 1;
    }
    uint64_t excepció_Estat; __asm__ volatile("mrs %0, esr_el1" : "=r"(excepció_Estat));
    if (Rellotge_VALOR() >= 마감시각) { tornar_les_tasques_nucli(arxiu_introducció, usuari_TIMEOUT); return 1; }
    unsigned excepció_Categoria = excepció_Estat >> 26;
    if (excepció_Categoria == 0x15 && (excepció_Estat & 0xffff) == 0) {
        if (리눅스규약 ? arxiu_introducció->registrar_se_dades[8] == 93 || arxiu_introducció->registrar_se_dades[8] == 94 : arxiu_introducció->registrar_se_dades[8] == 6) tornar_les_tasques_nucli(arxiu_introducció, (int)(arxiu_introducció->registrar_se_dades[0] & 255));
        else {
            intptr_t RESULTAT=체계호출(arxiu_introducció);
            if(RESULTAT==-4096&&interactiu){
                저장값[propietari_objecte].실행틀=*arxiu_introducció;저장값[propietari_objecte].실행틀.ordre_càrrec-=4;
                사용자실수보관(저장값[propietari_objecte].flotant_p_Estat);tornar_les_tasques_nucli(arxiu_introducció,사용자중단됨);
            }else arxiu_introducció->registrar_se_dades[0]=(uint64_t)RESULTAT;
        }
    } else tornar_les_tasques_nucli(arxiu_introducció, excepció_Categoria == 0x24 ? usuari_dades_error : excepció_Categoria == 0x20 ? 사용자실행오류 : usuari_invàlid_instrucció);
    return 1;
}

// 생성된 const ELF Grup_VALOR: 실행은 반드시 programa_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *dades; size_t Mida; unsigned 전달값; } programa;
#include "programs.h"
static void *instantània(unsigned càrrec_INDEX){return (void *)(0x04000000ul+càrrec_INDEX*(usuari_finalitzar-usuari_BASE));}
static int fi_programa(int RESULTAT){
    사용자누적시각[propietari_objecte]+=(uint32_t)보드밀리초()-사용자실행시각[propietari_objecte];
    aturar_TIMEOUT();Actiu=0;
    if(RESULTAT==사용자중단됨){
        저장된작업 *cadena_dades=&저장값[propietari_objecte];cadena_dades->멈춤상태=1;cadena_dades->interactiu=interactiu;cadena_dades->리눅스규약=리눅스규약;cadena_dades->동적기억공간=동적기억끝;cadena_dades->인수개수=전달인수개수;
        memcpy(cadena_dades->Permisos_Llista,Permisos_Llista,sizeof(Permisos_Llista));memcpy(cadena_dades->arxiu_Llista,arxiu_Llista,sizeof(arxiu_Llista));memcpy(cadena_dades->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(cadena_dades->arg_MATRIU,전달인수,sizeof(전달인수));memcpy(cadena_dades->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<usuari_pàgina_COMPT;순번++)if(Permisos_Llista[순번])memcpy((unsigned char *)instantània(propietari_objecte)+순번*mida_de_la_pàgina,(void *)(usuari_BASE+순번*mida_de_la_pàgina),mida_de_la_pàgina);
    }else{
        저장값[propietari_objecte].멈춤상태=0;화면초기화(propietari_objecte);
        for(unsigned 순번=0;순번<16;순번++)if(arxiu_Llista[순번]>=0)pk_close(arxiu_Llista[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<usuari_pàgina_COMPT;순번++){pàgina_Llista[순번]=0;Permisos_Llista[순번]=0;}변환표맞추기();return RESULTAT;
}
uintptr_t Tauler_control_d_usuari(uintptr_t Acció){
    unsigned càrrec_INDEX=Acció&15;if(càrrec_INDEX>=4||Actiu)return (uint32_t)-22;
    저장된작업 *cadena_dades=&저장값[càrrec_INDEX];
    if(Acció>=32){if(cadena_dades->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(cadena_dades->arxiu_Llista[순번]>=0)pk_close(cadena_dades->arxiu_Llista[순번]);for(unsigned 순번=0;순번<24;순번++)if(cadena_dades->통신끝점들[순번])통신끝점닫기(순번+32);}cadena_dades->멈춤상태=0;화면초기화(càrrec_INDEX);return 0;}
    if(Acció>=16)return cadena_dades->멈춤상태;
    if(!cadena_dades->멈춤상태)return (uint32_t)-22;
    propietari_objecte=càrrec_INDEX;interactiu=cadena_dades->interactiu;리눅스규약=cadena_dades->리눅스규약;동적기억끝=cadena_dades->동적기억공간;전달인수개수=cadena_dades->인수개수;
    memcpy(arxiu_Llista,cadena_dades->arxiu_Llista,sizeof(arxiu_Llista));memcpy(통신끝점들,cadena_dades->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,cadena_dades->arg_MATRIU,sizeof(전달인수));memcpy(전달인수길이,cadena_dades->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<usuari_pàgina_COMPT;순번++)pàgina_Llista[순번]=(usuari_BASE+순번*mida_de_la_pàgina)|nucli_pàgina;변환표맞추기();
    memset((void *)usuari_BASE,0,usuari_finalitzar-usuari_BASE);
    for(unsigned 순번=0;순번<usuari_pàgina_COMPT;순번++)if(cadena_dades->Permisos_Llista[순번])memcpy((void *)(usuari_BASE+순번*mida_de_la_pàgina),(unsigned char *)instantània(càrrec_INDEX)+순번*mida_de_la_pàgina,mida_de_la_pàgina);
    memcpy(Permisos_Llista,cadena_dades->Permisos_Llista,sizeof(Permisos_Llista));
    for(unsigned 순번=0;순번<usuari_pàgina_COMPT;순번++){unsigned dades_càrrec=Permisos_Llista[순번];pàgina_Llista[순번]=dades_càrrec?(usuari_BASE+순번*mida_de_la_pàgina)|(dades_càrrec==3?usuari_lectura_escriptura:dades_càrrec==5?usuari_tancar_Executa:usuari_només_de_lectura):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Actiu=1;cadena_dades->멈춤상태=0;Inici_TIMEOUT();
    사용자실행시각[propietari_objecte]=보드밀리초();
    return (uint32_t)fi_programa(usuari_reprendre(&cadena_dades->실행틀,cadena_dades->flotant_p_Estat));
}
static int execució_programa(const unsigned char *dades, size_t Mida, unsigned 전달값, int 리눅스방식, const char *Nom) {
    if (Actiu) return -16;
    propietari_objecte=Tauler_Terminal(11);if(propietari_objecte<0||propietari_objecte>3||저장값[propietari_objecte].멈춤상태)return -16;interactiu=0;
    int 유효함 = 실행파일검사(dades, Mida, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned nom_INDEX=0;
    while (*Nom && nom_INDEX<31) usuari_ordre_nom[propietari_objecte][nom_INDEX++]=(unsigned char)*Nom++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nom_INDEX) usuari_ordre_nom[propietari_objecte][nom_INDEX++]=' ';
        for (unsigned càrrec_INDEX=0; càrrec_INDEX<전달인수길이[0]; càrrec_INDEX++) usuari_ordre_nom[propietari_objecte][nom_INDEX++]=전달인수[0][càrrec_INDEX];
    }
    usuari_ordre_nom[propietari_objecte][nom_INDEX]=0; número_d_usuari[propietari_objecte]=Següent_número_d_usuari++;
    if (Següent_número_d_usuari>0x7fffffffu) Següent_número_d_usuari=10;
    usuari_Inici_Hora[propietari_objecte]=보드밀리초(); 사용자누적시각[propietari_objecte]=0;
    for (unsigned 순번 = 0; 순번 < usuari_pàgina_COMPT; 순번++) pàgina_Llista[순번] = (usuari_BASE + 순번 * mida_de_la_pàgina) | nucli_pàgina;
    변환표맞추기();
    memset((void *)usuari_BASE, 0, usuari_finalitzar - usuari_BASE);
    memset(Permisos_Llista, 0, sizeof(Permisos_Llista));
    실행파일머리 실행머리; memcpy(&실행머리, dades, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.programa_Capçalera_COMPT; 순번++) {
        실행파일구획 dades_càrrec; memcpy(&dades_càrrec, dades + 실행머리.programa_Capçalera_DESPLAÇAMENT + 순번 * sizeof(dades_càrrec), sizeof(dades_càrrec));
        if (dades_càrrec.TIPUS_Categoria != 1 || !dades_càrrec.기억영역크기) continue;
        if (dades_càrrec.파일영역크기) memcpy((void *)(uintptr_t)dades_càrrec.Adreça, dades + dades_càrrec.DESPLAÇAMENT_VALOR, dades_càrrec.파일영역크기);
        for (uintptr_t 현재위치 = dades_càrrec.Adreça & ~(mida_de_la_pàgina - 1); 현재위치 < dades_càrrec.Adreça + dades_càrrec.기억영역크기; 현재위치 += mida_de_la_pàgina) {
            Permisos_Llista[(현재위치 - usuari_BASE) / mida_de_la_pàgina] = (dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme & 2) ? 3 : ((dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = usuari_Pila_ADREÇA; 현재위치 < usuari_finalitzar; 현재위치 += mida_de_la_pàgina) Permisos_Llista[(현재위치 - usuari_BASE) / mida_de_la_pàgina] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.introducció_p) : usuari_finalitzar;
    for (unsigned 순번 = 0; 순번 < usuari_pàgina_COMPT; 순번++) {
        unsigned permisos = Permisos_Llista[순번];
        pàgina_Llista[순번] = permisos ? (usuari_BASE + 순번 * mida_de_la_pàgina) | (permisos == 3 ? usuari_lectura_escriptura : permisos == 5 ? usuari_tancar_Executa : usuari_només_de_lectura) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) arxiu_Llista[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = usuari_IMATGE_finalitzar;
    Actiu = 1; Inici_TIMEOUT();
    사용자실행시각[propietari_objecte]=보드밀리초();
    int RESULTAT = usuari_introduir(실행머리.introducció_p, 초기쌓임공간, 전달값);
    return fi_programa(RESULTAT);
}
uintptr_t Tauler_usuari_execució(uintptr_t Cerca_INDEX) {
    if (Cerca_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nom=Cerca_INDEX==10?"javac":Cerca_INDEX==11?"java":Cerca_INDEX==12?"python":Cerca_INDEX==13?"vi":Cerca_INDEX==14?"jar":Cerca_INDEX==15?"cc":Cerca_INDEX==16?"jaot":"ELF";
    return (uint32_t)execució_programa(실행항목들[Cerca_INDEX].dades, 실행항목들[Cerca_INDEX].Mida, 실행항목들[Cerca_INDEX].전달값, 0, Nom);
}
static uintptr_t Executa_arxiu(int 리눅스방식) {
    static unsigned char IMATGE[16384];
    if (Actiu || !전달인수개수) return (uint32_t)-22;
    int arxiu_control_7f4cdfd5 = pk_open((const char *)전달인수[0], només_de_lectura_VALOR, 0);
    if (arxiu_control_7f4cdfd5 < 0) return (uint32_t)-número_d_error;
    int Mida = pk_size(arxiu_control_7f4cdfd5);
    if (Mida < 0 || (unsigned)Mida > sizeof(IMATGE)) { pk_close(arxiu_control_7f4cdfd5); return (uint32_t)-27; }
    int CANTIDAD_RECIBIDA_COMPT = pk_read(arxiu_control_7f4cdfd5, IMATGE, Mida); pk_close(arxiu_control_7f4cdfd5);
    if (CANTIDAD_RECIBIDA_COMPT != Mida) return (uint32_t)-5;
    return (uint32_t)execució_programa(IMATGE, Mida, 0, 리눅스방식, "");
}
uintptr_t Tauler_usuari_arxiu(void) { return Executa_arxiu(0); }
uintptr_t 보드사용자리눅스파일(void) { return Executa_arxiu(1); }
uintptr_t Tauler_usuari_validar(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].dades, 잘못된실행항목들[순번].Mida) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
