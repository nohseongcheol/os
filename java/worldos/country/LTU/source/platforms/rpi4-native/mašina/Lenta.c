#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "naudotojas.h"
#include "../tinklas_eilė/tinklas_eilė.h"
typedef uintptr_t mašina_Word;
#define mašina_registras(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define pašto_dėžutė_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t laikrodis_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t dažnis;
static volatile uint32_t pašto_dėžutė_duomenys[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *duomenys_padėtis, int simbolio_kodas, size_t prekė_COUNT) { unsigned char *toliau_OFFSET = duomenys_padėtis; while (prekė_COUNT--) *toliau_OFFSET++ = simbolio_kodas; return duomenys_padėtis; }
void *memcpy(void *vieta_duomenys, const void *eilutė_duomenys, size_t prekė_COUNT) { unsigned char *첫째값 = vieta_duomenys; const unsigned char *SECOND_VALUE = eilutė_duomenys; while (prekė_COUNT--) *첫째값++ = *SECOND_VALUE++; return vieta_duomenys; }

static int pašto_dėžutė(void) {
    uint32_t užklausa = (uint32_t)(uintptr_t)pašto_dėžutė_duomenys | 8;
    uint64_t Paleisti = laikrodis_COUNT();
    기억장벽();
    while (mašina_registras(pašto_dėžutė_ADDRESS + 0x38) & 0x80000000u)
        if (laikrodis_COUNT() - Paleisti > dažnis) return 0;
    mašina_registras(pašto_dėžutė_ADDRESS + 0x20) = užklausa;
    for (;;) {
        if (!(mašina_registras(pašto_dėžutė_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t atsakyti = mašina_registras(pašto_dėžutė_ADDRESS);
            if (atsakyti == užklausa) { 기억장벽(); return pašto_dėžutė_duomenys[1] == 0x80000000u; }
        }
        if (laikrodis_COUNT() - Paleisti > dažnis) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminalas_baitas(unsigned);
extern int Terminalas_laukiama(void);
extern void Terminalas_rodyklė(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../nuotolinis_VALUE/nuotolinis_VALUE.h"
static int srautai;
static unsigned 직렬이전글자;
mašina_Word Lenta_srautai(mašina_Word 사용여부) { srautai=사용여부!=0; return 0; }
mašina_Word Lenta_kanalas(mašina_Word kanalas, mašina_Word simbolio_kodas) {
    if(srautai && 자바셸출력((int32_t)kanalas,(int32_t)(simbolio_kodas&255))) return 0;
    Terminalas_baitas(simbolio_kodas&255);
    nuotolinis_išeiga(simbolio_kodas&255);
    if ((simbolio_kodas&255)==10 && 직렬이전글자!=13) {
        while (mašina_registras(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        mašina_registras(직렬장치)=13;
    }
    직렬이전글자=simbolio_kodas&255;
    while (mašina_registras(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    mašina_registras(직렬장치) = (uint32_t)simbolio_kodas & 255;
    return 0;
}
mašina_Word 보드글자쓰기(mašina_Word simbolio_kodas) { return Lenta_kanalas(1,simbolio_kodas); }
mašina_Word 보드원시글자읽기(void) {
    int nuotolinis_simbolis=원격입력();if(nuotolinis_simbolis>=0)return nuotolinis_simbolis;
    if (mašina_registras(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = mašina_registras(직렬장치);
    if (VALUE & 0xf00) { mašina_registras(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
mašina_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paketas_duomenys[6];
    if(Terminalas_laukiama())return (uint32_t)-4096;
    if(srautai){int32_t simbolio_kodas=자바셸입력();if(simbolio_kodas!=-3)return (uint32_t)simbolio_kodas;}
    for(;;){
        int simbolio_kodas=(int32_t)보드원시글자읽기();if(simbolio_kodas<0)return (uint32_t)simbolio_kodas;
        if(!꾸러미안쪽){if(simbolio_kodas!=30)return simbolio_kodas;꾸러미안쪽=1;사용량=0;continue;}
        paketas_duomenys[사용량++]=simbolio_kodas;if(사용량<6)continue;꾸러미안쪽=0;
        if(paketas_duomenys[0]==1)Terminalas_rodyklė(paketas_duomenys[1],paketas_duomenys[2]+paketas_duomenys[3]*256,paketas_duomenys[4]+paketas_duomenys[5]*256);
        if(paketas_duomenys[0]==2)터미널바로가기키(paketas_duomenys[1]);
        if(paketas_duomenys[0]==3)터미널입력방식(paketas_duomenys[1]);
        if(Terminalas_laukiama())return (uint32_t)-4096;
    }
}
mašina_Word 보드밀리초(void) { return (uint32_t)(laikrodis_COUNT() / (dažnis / 1000)); }
mašina_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *eilutė_duomenys) { while (*eilutė_duomenys) 보드글자쓰기((unsigned char)*eilutė_duomenys++); }
static void 직렬열여섯진출력(mašina_Word prekė_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int eilutė_duomenys = 60; eilutė_duomenys >= 0; eilutė_duomenys -= 4) 보드글자쓰기(열여섯진숫자[(prekė_COUNT >> eilutė_duomenys) & 15]); }
mašina_Word Lenta_Stok(mašina_Word Būsena_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Būsena_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Lenta_Stok(1); __builtin_unreachable(); }
void Lenta_išimtis(mašina_Word išimtis_Būsena, mašina_Word komanda_padėtis, mašina_Word neleistinas_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(išimtis_Būsena);
    직렬글출력(" PC="); 직렬열여섯진출력(komanda_padėtis); 직렬글출력(" FAR="); 직렬열여섯진출력(neleistinas_ADDRESS);
    Lenta_Stok(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    pašto_dėžutė_duomenys[0]=32;pašto_dėžutė_duomenys[1]=0;pašto_dėžutė_duomenys[2]=0x10004;pašto_dėžutė_duomenys[3]=8;pašto_dėžutė_duomenys[4]=0;
    pašto_dėžutė_duomenys[5]=pašto_dėžutė_duomenys[6]=pašto_dėžutė_duomenys[7]=0;
    return pašto_dėžutė()&&pašto_dėžutė_duomenys[4]==0x80000008u&&(pašto_dėžutė_duomenys[5]||pašto_dėžutė_duomenys[6]);
}
int Lenta_absoliutusis_adresas(unsigned char *ADDRESS) {
    pašto_dėžutė_duomenys[0]=32;pašto_dėžutė_duomenys[1]=0;pašto_dėžutė_duomenys[2]=0x10003;pašto_dėžutė_duomenys[3]=8;pašto_dėžutė_duomenys[4]=0;
    pašto_dėžutė_duomenys[5]=pašto_dėžutė_duomenys[6]=pašto_dėžutė_duomenys[7]=0;
    if(!pašto_dėžutė()||(pašto_dėžutė_duomenys[4]&0x80000000u)==0||(pašto_dėžutė_duomenys[4]&0xffff)!=6)return 0;
    const unsigned char *duomenys=(const unsigned char*)&pašto_dėžutė_duomenys[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=duomenys[순번];SUM_VALUE|=duomenys[순번];}return SUM_VALUE&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(dažnis));
    mašina_registras(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    mašina_registras(범용입출력 + 4) = (mašina_registras(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    mašina_registras(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. triktis_VALUE 시 config.txt의 48MHz를 사용한다.
    pašto_dėžutė_duomenys[0] = 36; pašto_dėžutė_duomenys[1] = 0; pašto_dėžutė_duomenys[2] = 0x38002; pašto_dėžutė_duomenys[3] = 12;
    pašto_dėžutė_duomenys[4] = 0; pašto_dėžutė_duomenys[5] = 2; pašto_dėžutė_duomenys[6] = 48000000; pašto_dėžutė_duomenys[7] = 0; pašto_dėžutė_duomenys[8] = 0;
    int 시계정상 = pašto_dėžutė();
    uint32_t 속도 = 시계정상 && pašto_dėžutė_duomenys[6] >= 1843200 ? pašto_dėžutė_duomenys[6] : 48000000;
    pašto_dėžutė_duomenys[0]=32; pašto_dėžutė_duomenys[1]=0; pašto_dėžutė_duomenys[2]=0x10005; pašto_dėžutė_duomenys[3]=8; pašto_dėžutė_duomenys[4]=0;
    pašto_dėžutė_duomenys[5]=pašto_dėžutė_duomenys[6]=pašto_dėžutė_duomenys[7]=0;
    if (pašto_dėžutė() && pašto_dėžutė_duomenys[4]==0x80000008u) 팔기억킬로바이트=pašto_dėžutė_duomenys[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    mašina_registras(직렬장치 + 0x44) = 0x7ff;
    mašina_registras(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    mašina_registras(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    mašina_registras(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    mašina_registras(직렬장치 + 0x38) = 0;
    mašina_registras(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
mašina_Word Lenta_FTP(mašina_Word Veiksmas) { return (uint32_t)ftp_control((int)Veiksmas); }
mašina_Word Lenta_tinklas_būsena(mašina_Word įrašas_VALUE, mašina_Word INDEX) { return 망상태읽기(įrašas_VALUE, INDEX); }
mašina_Word Lenta_tinklas_Parametrai(mašina_Word Veiksmas, mašina_Word ADDRESS, mašina_Word šablonas_VALUE, mašina_Word šliuzas_VALUE) { return (uint32_t)konfigūruoti_tinklas(Veiksmas, ADDRESS, šablonas_VALUE, šliuzas_VALUE); }
mašina_Word Lenta_siųsti_atsakas(mašina_Word ADDRESS, mašina_Word tvarka_VALUE) { return (uint32_t)응답시험시작(ADDRESS, tvarka_VALUE); }
mašina_Word 보드응답읽기(mašina_Word įrašas_VALUE) { return (uint32_t)응답시험읽기(įrašas_VALUE); }
mašina_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Uždaryti_tinklas(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Lenta_vartotojo_valdiklis(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (mašina_registras(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    mašina_registras(0xfe100020ul)=0x5a000000u | (mašina_registras(0xfe100020ul)&~0xfffu) | 0x555;
    mašina_registras(0xfe100024ul)=0x5a000000u | 10;
    mašina_registras(0xfe10001cul)=0x5a000000u | (mašina_registras(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

mašina_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 dabartinis_prekė 크기를 읽는다. */
    const uint32_t užklausa_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(užklausa_VALUE)/4; 순번++) pašto_dėžutė_duomenys[순번] = užklausa_VALUE[순번];
    if (pašto_dėžutė() && pašto_dėžutė_duomenys[4] == 0x80000008u &&
        pašto_dėžutė_duomenys[5] >= 640 && pašto_dėžutė_duomenys[5] <= 1920 &&
        pašto_dėžutė_duomenys[6] >= 480 && pašto_dėžutė_duomenys[6] <= 1080) {
        요청너비 = pašto_dėžutė_duomenys[5]; 요청높이 = pašto_dėžutė_duomenys[6];
    }
    const uint32_t užklausa[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(užklausa)/4; 순번++) pašto_dėžutė_duomenys[순번] = užklausa[순번];
    // 위 메시지의 faktinis_duomenys 길이를 naudoti_VALUE: 태그 sujungti_įrašas 시 길이 불일치를 방지한다.
    pašto_dėžutė_duomenys[0] = sizeof(užklausa);
    if (!pašto_dėžutė()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (pašto_dėžutė_duomenys[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Fonas_VALUE = pašto_dėžutė_duomenys[28] & 0x3fffffffu;
    uint32_t Dydis = pašto_dėžutė_duomenys[29];
    uint32_t 받은너비 = pašto_dėžutė_duomenys[5], 받은높이 = pašto_dėžutė_duomenys[6], RECEIVED_eilučių_intervalas = pašto_dėžutė_duomenys[33];
    if (pašto_dėžutė_duomenys[15] != 32 || pašto_dėžutė_duomenys[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        pašto_dėžutė_duomenys[10] < 받은너비 || pašto_dėžutė_duomenys[11] < 받은높이 || pašto_dėžutė_duomenys[23] || pašto_dėžutė_duomenys[24] ||
        !Fonas_VALUE || Fonas_VALUE < 0x1000000 || (Fonas_VALUE & 3) || RECEIVED_eilučių_intervalas < 받은너비 * 4 || (RECEIVED_eilučių_intervalas & 3) ||
        (uint64_t)RECEIVED_eilučių_intervalas * 받은높이 > Dydis || (uint64_t)Fonas_VALUE + Dydis > 0x40000000u)
        return 0;
    Lenta_Parengti_piešinys((volatile uint32_t *)(uintptr_t)Fonas_VALUE, 받은너비, 받은높이, RECEIVED_eilučių_intervalas);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 gija_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informacinės_technologijos_Bėgimas[3] = {1, 0, 0};
static int dabartinis_užduotis;
extern void konteksto_jungiklis(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
mašina_Word Lenta_YIELD(void) {
    network_poll();
    int 이전 = dabartinis_užduotis, toliau_prekė = (이전 + 1) % 3;
    while (toliau_prekė != 이전 && !informacinės_technologijos_Bėgimas[toliau_prekė]) toliau_prekė = (toliau_prekė + 1) % 3;
    if (toliau_prekė != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informacinės_technologijos_Bėgimas[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        dabartinis_užduotis = toliau_prekė;
        konteksto_jungiklis(&작업문맥들[이전], &작업문맥들[toliau_prekė]);
    }
    return 0;
}
static void užduotis_perkrovimas(void) {
    자바작업(dabartinis_užduotis);
    informacinės_technologijos_Bėgimas[dabartinis_užduotis] = 0;
    Lenta_YIELD();
    커널중단("finished task resumed");
}
mašina_Word Lenta_užduotis_kurti(mašina_Word identifikatorius_VALUE) {
    if (identifikatorius_VALUE < 1 || identifikatorius_VALUE > 2 || informacinės_technologijos_Bėgimas[identifikatorius_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikatorius_VALUE], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[identifikatorius_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikatorius_VALUE].저장값[11] = (uintptr_t)užduotis_perkrovimas;
    작업문맥들[identifikatorius_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikatorius_VALUE - 1] + sizeof(쌓임공간들[0]));
    informacinės_technologijos_Bėgimas[identifikatorius_VALUE] = 1;
    return 0;
}
mašina_Word Lenta_užduotis_Būsena(mašina_Word identifikatorius_VALUE) { return identifikatorius_VALUE < 3 ? informacinės_technologijos_Bėgimas[identifikatorius_VALUE] : (uint32_t)-1; }
extern mašina_Word AOT_atmintis_LOOKUP(mašina_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
mašina_Word Lenta_užklausa_sistema(mašina_Word įrašas_VALUE, mašina_Word INDEX) {
    if (įrašas_VALUE==0) return 팔기억킬로바이트;
    if (įrašas_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (įrašas_VALUE==2 || įrašas_VALUE==3) return AOT_atmintis_LOOKUP(įrašas_VALUE==3);
    if (įrašas_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (įrašas_VALUE==5) return 80*1024; /* Vykdyti_komanda ADDRESS_sritis 16 MiB + 네 세션 보관 ADDRESS_sritis. */
    if (įrašas_VALUE>=20) return 사용자상태읽기(įrašas_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[dabartinis_užduotis]; }
