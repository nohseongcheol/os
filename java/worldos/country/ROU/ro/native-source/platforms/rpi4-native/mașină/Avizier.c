#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "utilizator.h"
#include "../rețea_Teanc/rețea_Teanc.h"
typedef uintptr_t mașină_Word;
#define mașină_registru(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define cutie_poștală_adresa 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Ceas_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t cutie_poștală_date[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *date_poziție, int cod_caracter, size_t element_COUNT) { unsigned char *Următorul_OFFSET = date_poziție; while (element_COUNT--) *Următorul_OFFSET++ = cod_caracter; return date_poziție; }
void *memcpy(void *destinație_date, const void *șir_date, size_t element_COUNT) { unsigned char *첫째값 = destinație_date; const unsigned char *SECOND_VALUE = șir_date; while (element_COUNT--) *첫째값++ = *SECOND_VALUE++; return destinație_date; }

static int cutie_poștală(void) {
    uint32_t cerere = (uint32_t)(uintptr_t)cutie_poștală_date | 8;
    uint64_t Pornește = Ceas_COUNT();
    기억장벽();
    while (mașină_registru(cutie_poștală_adresa + 0x38) & 0x80000000u)
        if (Ceas_COUNT() - Pornește > FREQUENCY) return 0;
    mașină_registru(cutie_poștală_adresa + 0x20) = cerere;
    for (;;) {
        if (!(mașină_registru(cutie_poștală_adresa + 0x18) & 0x40000000u)) {
            uint32_t replică = mașină_registru(cutie_poștală_adresa);
            if (replică == cerere) { 기억장벽(); return cutie_poștală_date[1] == 0x80000000u; }
        }
        if (Ceas_COUNT() - Pornește > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_în_așteptare(void);
extern void Terminal_cursor(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../la_distanță_VALUE/la_distanță_VALUE.h"
static int Fluxuri;
static unsigned 직렬이전글자;
mașină_Word Avizier_Fluxuri(mașină_Word 사용여부) { Fluxuri=사용여부!=0; return 0; }
mașină_Word Avizier_Canal(mașină_Word Canal, mașină_Word cod_caracter) {
    if(Fluxuri && 자바셸출력((int32_t)Canal,(int32_t)(cod_caracter&255))) return 0;
    Terminal_byte(cod_caracter&255);
    원격출력(cod_caracter&255);
    if ((cod_caracter&255)==10 && 직렬이전글자!=13) {
        while (mașină_registru(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        mașină_registru(직렬장치)=13;
    }
    직렬이전글자=cod_caracter&255;
    while (mașină_registru(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    mașină_registru(직렬장치) = (uint32_t)cod_caracter & 255;
    return 0;
}
mașină_Word 보드글자쓰기(mașină_Word cod_caracter) { return Avizier_Canal(1,cod_caracter); }
mașină_Word 보드원시글자읽기(void) {
    int la_distanță_caracter=원격입력();if(la_distanță_caracter>=0)return la_distanță_caracter;
    if (mașină_registru(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = mașină_registru(직렬장치);
    if (VALUE & 0xf00) { mașină_registru(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
mașină_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pachet_date[6];
    if(Terminal_în_așteptare())return (uint32_t)-4096;
    if(Fluxuri){int32_t cod_caracter=자바셸입력();if(cod_caracter!=-3)return (uint32_t)cod_caracter;}
    for(;;){
        int cod_caracter=(int32_t)보드원시글자읽기();if(cod_caracter<0)return (uint32_t)cod_caracter;
        if(!꾸러미안쪽){if(cod_caracter!=30)return cod_caracter;꾸러미안쪽=1;사용량=0;continue;}
        pachet_date[사용량++]=cod_caracter;if(사용량<6)continue;꾸러미안쪽=0;
        if(pachet_date[0]==1)Terminal_cursor(pachet_date[1],pachet_date[2]+pachet_date[3]*256,pachet_date[4]+pachet_date[5]*256);
        if(pachet_date[0]==2)터미널바로가기키(pachet_date[1]);
        if(pachet_date[0]==3)터미널입력방식(pachet_date[1]);
        if(Terminal_în_așteptare())return (uint32_t)-4096;
    }
}
mașină_Word 보드밀리초(void) { return (uint32_t)(Ceas_COUNT() / (FREQUENCY / 1000)); }
mașină_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *șir_date) { while (*șir_date) 보드글자쓰기((unsigned char)*șir_date++); }
static void 직렬열여섯진출력(mașină_Word element_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int șir_date = 60; șir_date >= 0; șir_date -= 4) 보드글자쓰기(열여섯진숫자[(element_COUNT >> șir_date) & 15]); }
mașină_Word Avizier_Stop(mașină_Word Stare_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Stare_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Avizier_Stop(1); __builtin_unreachable(); }
void Avizier_excepție(mașină_Word excepție_Stare, mașină_Word comandă_poziție, mașină_Word nul_adresa) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(excepție_Stare);
    직렬글출력(" PC="); 직렬열여섯진출력(comandă_poziție); 직렬글출력(" FAR="); 직렬열여섯진출력(nul_adresa);
    Avizier_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    cutie_poștală_date[0]=32;cutie_poștală_date[1]=0;cutie_poștală_date[2]=0x10004;cutie_poștală_date[3]=8;cutie_poștală_date[4]=0;
    cutie_poștală_date[5]=cutie_poștală_date[6]=cutie_poștală_date[7]=0;
    return cutie_poștală()&&cutie_poștală_date[4]==0x80000008u&&(cutie_poștală_date[5]||cutie_poștală_date[6]);
}
int Avizier_adresă_reală(unsigned char *adresa) {
    cutie_poștală_date[0]=32;cutie_poștală_date[1]=0;cutie_poștală_date[2]=0x10003;cutie_poștală_date[3]=8;cutie_poștală_date[4]=0;
    cutie_poștală_date[5]=cutie_poștală_date[6]=cutie_poștală_date[7]=0;
    if(!cutie_poștală()||(cutie_poștală_date[4]&0x80000000u)==0||(cutie_poștală_date[4]&0xffff)!=6)return 0;
    const unsigned char *date=(const unsigned char*)&cutie_poștală_date[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){adresa[순번]=date[순번];SUM_VALUE|=date[순번];}return SUM_VALUE&&!(adresa[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    mașină_registru(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    mașină_registru(범용입출력 + 4) = (mașină_registru(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    mașină_registru(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. eroare_VALUE 시 config.txt의 48MHz를 사용한다.
    cutie_poștală_date[0] = 36; cutie_poștală_date[1] = 0; cutie_poștală_date[2] = 0x38002; cutie_poștală_date[3] = 12;
    cutie_poștală_date[4] = 0; cutie_poștală_date[5] = 2; cutie_poștală_date[6] = 48000000; cutie_poștală_date[7] = 0; cutie_poștală_date[8] = 0;
    int 시계정상 = cutie_poștală();
    uint32_t 속도 = 시계정상 && cutie_poștală_date[6] >= 1843200 ? cutie_poștală_date[6] : 48000000;
    cutie_poștală_date[0]=32; cutie_poștală_date[1]=0; cutie_poștală_date[2]=0x10005; cutie_poștală_date[3]=8; cutie_poștală_date[4]=0;
    cutie_poștală_date[5]=cutie_poștală_date[6]=cutie_poștală_date[7]=0;
    if (cutie_poștală() && cutie_poștală_date[4]==0x80000008u) 팔기억킬로바이트=cutie_poștală_date[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    mașină_registru(직렬장치 + 0x44) = 0x7ff;
    mașină_registru(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    mașină_registru(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    mașină_registru(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    mașină_registru(직렬장치 + 0x38) = 0;
    mașină_registru(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
mașină_Word Avizier_FTP(mașină_Word Acțiuni) { return (uint32_t)ftp_control((int)Acțiuni); }
mașină_Word Avizier_rețea_stare(mașină_Word intrare_VALUE, mașină_Word INDEX) { return 망상태읽기(intrare_VALUE, INDEX); }
mașină_Word Avizier_rețea_Setări(mașină_Word Acțiuni, mașină_Word adresa, mașină_Word mască_VALUE, mașină_Word gateway_VALUE) { return (uint32_t)configura_rețea(Acțiuni, adresa, mască_VALUE, gateway_VALUE); }
mașină_Word Avizier_trimite_răspuns(mașină_Word adresa, mașină_Word ordine_VALUE) { return (uint32_t)응답시험시작(adresa, ordine_VALUE); }
mașină_Word 보드응답읽기(mașină_Word intrare_VALUE) { return (uint32_t)응답시험읽기(intrare_VALUE); }
mașină_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) închide_rețea(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Avizier_control_utilizator(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (mașină_registru(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    mașină_registru(0xfe100020ul)=0x5a000000u | (mașină_registru(0xfe100020ul)&~0xfffu) | 0x555;
    mașină_registru(0xfe100024ul)=0x5a000000u | 10;
    mașină_registru(0xfe10001cul)=0x5a000000u | (mașină_registru(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

mașină_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 curent_element 크기를 읽는다. */
    const uint32_t interoga_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(interoga_VALUE)/4; 순번++) cutie_poștală_date[순번] = interoga_VALUE[순번];
    if (cutie_poștală() && cutie_poștală_date[4] == 0x80000008u &&
        cutie_poștală_date[5] >= 640 && cutie_poștală_date[5] <= 1920 &&
        cutie_poștală_date[6] >= 480 && cutie_poștală_date[6] <= 1080) {
        요청너비 = cutie_poștală_date[5]; 요청높이 = cutie_poștală_date[6];
    }
    const uint32_t cerere[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(cerere)/4; 순번++) cutie_poștală_date[순번] = cerere[순번];
    // 위 메시지의 real_date 길이를 utiliza_VALUE: 태그 adăuga_intrare 시 lungime_VALUE 불일치를 방지한다.
    cutie_poștală_date[0] = sizeof(cerere);
    if (!cutie_poștală()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned răspuns_lungime[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (cutie_poștală_date[응답들[순번]] != (0x80000000u | răspuns_lungime[순번])) return 0;
    uint32_t tapet_VALUE = cutie_poștală_date[28] & 0x3fffffffu;
    uint32_t Mărime = cutie_poștală_date[29];
    uint32_t 받은너비 = cutie_poștală_date[5], 받은높이 = cutie_poștală_date[6], RECEIVED_spațiere = cutie_poștală_date[33];
    if (cutie_poștală_date[15] != 32 || cutie_poștală_date[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        cutie_poștală_date[10] < 받은너비 || cutie_poștală_date[11] < 받은높이 || cutie_poștală_date[23] || cutie_poștală_date[24] ||
        !tapet_VALUE || tapet_VALUE < 0x1000000 || (tapet_VALUE & 3) || RECEIVED_spațiere < 받은너비 * 4 || (RECEIVED_spațiere & 3) ||
        (uint64_t)RECEIVED_spațiere * 받은높이 > Mărime || (uint64_t)tapet_VALUE + Mărime > 0x40000000u)
        return 0;
    Avizier_Pregătiți_desen((volatile uint32_t *)(uintptr_t)tapet_VALUE, 받은너비, 받은높이, RECEIVED_spațiere);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 fir_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } context;
static context 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int sisteme_de_informații_Alergare[3] = {1, 0, 0};
static int curent_sarcină;
extern void comutator_de_context(context *, context *);
extern void 자바작업(int32_t);
mașină_Word Avizier_YIELD(void) {
    network_poll();
    int Anteriorul_element = curent_sarcină, Următorul_element = (Anteriorul_element + 1) % 3;
    while (Următorul_element != Anteriorul_element && !sisteme_de_informații_Alergare[Următorul_element]) Următorul_element = (Următorul_element + 1) % 3;
    if (Următorul_element != Anteriorul_element) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (sisteme_de_informații_Alergare[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        curent_sarcină = Următorul_element;
        comutator_de_context(&작업문맥들[Anteriorul_element], &작업문맥들[Următorul_element]);
    }
    return 0;
}
static void sarcină_boot(void) {
    자바작업(curent_sarcină);
    sisteme_de_informații_Alergare[curent_sarcină] = 0;
    Avizier_YIELD();
    커널중단("finished task resumed");
}
mașină_Word Avizier_sarcină_crea(mașină_Word identificator_VALUE) {
    if (identificator_VALUE < 1 || identificator_VALUE > 2 || sisteme_de_informații_Alergare[identificator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identificator_VALUE], 0, sizeof(context));
    *(uint64_t *)쌓임공간들[identificator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identificator_VALUE].저장값[11] = (uintptr_t)sarcină_boot;
    작업문맥들[identificator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identificator_VALUE - 1] + sizeof(쌓임공간들[0]));
    sisteme_de_informații_Alergare[identificator_VALUE] = 1;
    return 0;
}
mașină_Word Avizier_sarcină_Stare(mașină_Word identificator_VALUE) { return identificator_VALUE < 3 ? sisteme_de_informații_Alergare[identificator_VALUE] : (uint32_t)-1; }
extern mașină_Word 미리번역기억조회(mașină_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
mașină_Word Avizier_interoga_sistem(mașină_Word intrare_VALUE, mașină_Word INDEX) {
    if (intrare_VALUE==0) return 팔기억킬로바이트;
    if (intrare_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (intrare_VALUE==2 || intrare_VALUE==3) return 미리번역기억조회(intrare_VALUE==3);
    if (intrare_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (intrare_VALUE==5) return 80*1024; /* executa_comandă adresa_regiune 16 MiB + 네 세션 보관 adresa_regiune. */
    if (intrare_VALUE>=20) return 사용자상태읽기(intrare_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[curent_sarcină]; }
