#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "gumagamit.h"
#include "../Network_Stack/Network_Stack.h"
typedef uintptr_t machine_Word;
#define machine_magrehistro(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define mailbox_email 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Orasan_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t mailbox_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_posisyon, int character_code, size_t item_COUNT) { unsigned char *Susunod_OFFSET = data_posisyon; while (item_COUNT--) *Susunod_OFFSET++ = character_code; return data_posisyon; }
void *memcpy(void *patutunguhan_data, const void *string_data, size_t item_COUNT) { unsigned char *첫째값 = patutunguhan_data; const unsigned char *SECOND_VALUE = string_data; while (item_COUNT--) *첫째값++ = *SECOND_VALUE++; return patutunguhan_data; }

static int mailbox(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)mailbox_data | 8;
    uint64_t run = Orasan_COUNT();
    기억장벽();
    while (machine_magrehistro(mailbox_email + 0x38) & 0x80000000u)
        if (Orasan_COUNT() - run > FREQUENCY) return 0;
    machine_magrehistro(mailbox_email + 0x20) = 요청;
    for (;;) {
        if (!(machine_magrehistro(mailbox_email + 0x18) & 0x40000000u)) {
            uint32_t tumugon = machine_magrehistro(mailbox_email);
            if (tumugon == 요청) { 기억장벽(); return mailbox_data[1] == 0x80000000u; }
        }
        if (Orasan_COUNT() - run > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_pending(void);
extern void Terminal_pointer(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../malayuan_VALUE/malayuan_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
machine_Word 보드흐름설정(machine_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
machine_Word board_channel(machine_Word channel, machine_Word character_code) {
    if(흐름목록 && 자바셸출력((int32_t)channel,(int32_t)(character_code&255))) return 0;
    Terminal_byte(character_code&255);
    원격출력(character_code&255);
    if ((character_code&255)==10 && 직렬이전글자!=13) {
        while (machine_magrehistro(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        machine_magrehistro(직렬장치)=13;
    }
    직렬이전글자=character_code&255;
    while (machine_magrehistro(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    machine_magrehistro(직렬장치) = (uint32_t)character_code & 255;
    return 0;
}
machine_Word 보드글자쓰기(machine_Word character_code) { return board_channel(1,character_code); }
machine_Word 보드원시글자읽기(void) {
    int malayuan_karakter=원격입력();if(malayuan_karakter>=0)return malayuan_karakter;
    if (machine_magrehistro(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = machine_magrehistro(직렬장치);
    if (VALUE & 0xf00) { machine_magrehistro(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
machine_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char packet_data[6];
    if(Terminal_pending())return (uint32_t)-4096;
    if(흐름목록){int32_t character_code=자바셸입력();if(character_code!=-3)return (uint32_t)character_code;}
    for(;;){
        int character_code=(int32_t)보드원시글자읽기();if(character_code<0)return (uint32_t)character_code;
        if(!꾸러미안쪽){if(character_code!=30)return character_code;꾸러미안쪽=1;사용량=0;continue;}
        packet_data[사용량++]=character_code;if(사용량<6)continue;꾸러미안쪽=0;
        if(packet_data[0]==1)Terminal_pointer(packet_data[1],packet_data[2]+packet_data[3]*256,packet_data[4]+packet_data[5]*256);
        if(packet_data[0]==2)터미널바로가기키(packet_data[1]);
        if(packet_data[0]==3)터미널입력방식(packet_data[1]);
        if(Terminal_pending())return (uint32_t)-4096;
    }
}
machine_Word 보드밀리초(void) { return (uint32_t)(Orasan_COUNT() / (FREQUENCY / 1000)); }
machine_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *string_data) { while (*string_data) 보드글자쓰기((unsigned char)*string_data++); }
static void 직렬열여섯진출력(machine_Word item_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int string_data = 60; string_data >= 0; string_data -= 4) 보드글자쓰기(열여섯진숫자[(item_COUNT >> string_data) & 15]); }
machine_Word board_Hinto(machine_Word katayuan_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(katayuan_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); board_Hinto(1); __builtin_unreachable(); }
void board_pagbubukod(machine_Word pagbubukod_katayuan, machine_Word utos_posisyon, machine_Word hindi_tama_email) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(pagbubukod_katayuan);
    직렬글출력(" PC="); 직렬열여섯진출력(utos_posisyon); 직렬글출력(" FAR="); 직렬열여섯진출력(hindi_tama_email);
    board_Hinto(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    mailbox_data[0]=32;mailbox_data[1]=0;mailbox_data[2]=0x10004;mailbox_data[3]=8;mailbox_data[4]=0;
    mailbox_data[5]=mailbox_data[6]=mailbox_data[7]=0;
    return mailbox()&&mailbox_data[4]==0x80000008u&&(mailbox_data[5]||mailbox_data[6]);
}
int board_machine_email(unsigned char *email) {
    mailbox_data[0]=32;mailbox_data[1]=0;mailbox_data[2]=0x10003;mailbox_data[3]=8;mailbox_data[4]=0;
    mailbox_data[5]=mailbox_data[6]=mailbox_data[7]=0;
    if(!mailbox()||(mailbox_data[4]&0x80000000u)==0||(mailbox_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&mailbox_data[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){email[순번]=data[순번];SUM_VALUE|=data[순번];}return SUM_VALUE&&!(email[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    machine_magrehistro(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    machine_magrehistro(범용입출력 + 4) = (machine_magrehistro(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    machine_magrehistro(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. pagpalya_VALUE 시 config.txt의 48MHz를 사용한다.
    mailbox_data[0] = 36; mailbox_data[1] = 0; mailbox_data[2] = 0x38002; mailbox_data[3] = 12;
    mailbox_data[4] = 0; mailbox_data[5] = 2; mailbox_data[6] = 48000000; mailbox_data[7] = 0; mailbox_data[8] = 0;
    int 시계정상 = mailbox();
    uint32_t 속도 = 시계정상 && mailbox_data[6] >= 1843200 ? mailbox_data[6] : 48000000;
    mailbox_data[0]=32; mailbox_data[1]=0; mailbox_data[2]=0x10005; mailbox_data[3]=8; mailbox_data[4]=0;
    mailbox_data[5]=mailbox_data[6]=mailbox_data[7]=0;
    if (mailbox() && mailbox_data[4]==0x80000008u) 팔기억킬로바이트=mailbox_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    machine_magrehistro(직렬장치 + 0x44) = 0x7ff;
    machine_magrehistro(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    machine_magrehistro(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    machine_magrehistro(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    machine_magrehistro(직렬장치 + 0x38) = 0;
    machine_magrehistro(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
machine_Word board_FTP(machine_Word aksyon) { return (uint32_t)ftp_control((int)aksyon); }
machine_Word board_Network_katayuan(machine_Word pagpasok_VALUE, machine_Word INDEX) { return 망상태읽기(pagpasok_VALUE, INDEX); }
machine_Word board_Network_Mga_Setting(machine_Word aksyon, machine_Word email, machine_Word mask_VALUE, machine_Word entrada_VALUE) { return (uint32_t)magkompigura_Network(aksyon, email, mask_VALUE, entrada_VALUE); }
machine_Word 보드응답보내기(machine_Word email, machine_Word pagkakasunud_sunod_VALUE) { return (uint32_t)응답시험시작(email, pagkakasunud_sunod_VALUE); }
machine_Word 보드응답읽기(machine_Word pagpasok_VALUE) { return (uint32_t)응답시험읽기(pagpasok_VALUE); }
machine_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) isara_Network(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) board_user_control(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (machine_magrehistro(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    machine_magrehistro(0xfe100020ul)=0x5a000000u | (machine_magrehistro(0xfe100020ul)&~0xfffu) | 0x555;
    machine_magrehistro(0xfe100024ul)=0x5a000000u | 10;
    machine_magrehistro(0xfe10001cul)=0x5a000000u | (machine_magrehistro(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

machine_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t query_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(query_VALUE)/4; 순번++) mailbox_data[순번] = query_VALUE[순번];
    if (mailbox() && mailbox_data[4] == 0x80000008u &&
        mailbox_data[5] >= 640 && mailbox_data[5] <= 1920 &&
        mailbox_data[6] >= 480 && mailbox_data[6] <= 1080) {
        요청너비 = mailbox_data[5]; 요청높이 = mailbox_data[6];
    }
    const uint32_t 요청[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) mailbox_data[순번] = 요청[순번];
    // 위 메시지의 totoo_data 길이를 사용: 태그 추가 시 haba_VALUE 불일치를 방지한다.
    mailbox_data[0] = sizeof(요청);
    if (!mailbox()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (mailbox_data[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t wallpaper_VALUE = mailbox_data[28] & 0x3fffffffu;
    uint32_t sukat_82232621 = mailbox_data[29];
    uint32_t 받은너비 = mailbox_data[5], 받은높이 = mailbox_data[6], RECEIVED_pagitan_ng_linya = mailbox_data[33];
    if (mailbox_data[15] != 32 || mailbox_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        mailbox_data[10] < 받은너비 || mailbox_data[11] < 받은높이 || mailbox_data[23] || mailbox_data[24] ||
        !wallpaper_VALUE || wallpaper_VALUE < 0x1000000 || (wallpaper_VALUE & 3) || RECEIVED_pagitan_ng_linya < 받은너비 * 4 || (RECEIVED_pagitan_ng_linya & 3) ||
        (uint64_t)RECEIVED_pagitan_ng_linya * 받은높이 > sukat_82232621 || (uint64_t)wallpaper_VALUE + sukat_82232621 > 0x40000000u)
        return 0;
    board_Ihanda_iginuhit((volatile uint32_t *)(uintptr_t)wallpaper_VALUE, 받은너비, 받은높이, RECEIVED_pagitan_ng_linya);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 thread_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Konteksto;
static Konteksto 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int information_technology_Tumatakbo[3] = {1, 0, 0};
static int 현재작업;
extern void Konteksto_SWITCH(Konteksto *, Konteksto *);
extern void 자바작업(int32_t);
machine_Word board_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Susunod_item = (이전 + 1) % 3;
    while (Susunod_item != 이전 && !information_technology_Tumatakbo[Susunod_item]) Susunod_item = (Susunod_item + 1) % 3;
    if (Susunod_item != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (information_technology_Tumatakbo[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Susunod_item;
        Konteksto_SWITCH(&작업문맥들[이전], &작업문맥들[Susunod_item]);
    }
    return 0;
}
static void gawain_magbukas(void) {
    자바작업(현재작업);
    information_technology_Tumatakbo[현재작업] = 0;
    board_YIELD();
    커널중단("finished task resumed");
}
machine_Word board_gawain_Create(machine_Word tagakilala_VALUE) {
    if (tagakilala_VALUE < 1 || tagakilala_VALUE > 2 || information_technology_Tumatakbo[tagakilala_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[tagakilala_VALUE], 0, sizeof(Konteksto));
    *(uint64_t *)쌓임공간들[tagakilala_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[tagakilala_VALUE].저장값[11] = (uintptr_t)gawain_magbukas;
    작업문맥들[tagakilala_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[tagakilala_VALUE - 1] + sizeof(쌓임공간들[0]));
    information_technology_Tumatakbo[tagakilala_VALUE] = 1;
    return 0;
}
machine_Word board_gawain_katayuan(machine_Word tagakilala_VALUE) { return tagakilala_VALUE < 3 ? information_technology_Tumatakbo[tagakilala_VALUE] : (uint32_t)-1; }
extern machine_Word 미리번역기억조회(machine_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
machine_Word board_query_system(machine_Word pagpasok_VALUE, machine_Word INDEX) {
    if (pagpasok_VALUE==0) return 팔기억킬로바이트;
    if (pagpasok_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (pagpasok_VALUE==2 || pagpasok_VALUE==3) return 미리번역기억조회(pagpasok_VALUE==3);
    if (pagpasok_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (pagpasok_VALUE==5) return 80*1024; /* Mag_execute_utos 공간 16 MiB + 네 세션 보관 공간. */
    if (pagpasok_VALUE>=20) return 사용자상태읽기(pagpasok_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
