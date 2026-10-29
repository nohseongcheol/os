#include "../naming/machineLinkNames.h"
#include "screenInformation.h"
#include <stdint.h>
#include <stddef.h>
#include "User.h"
#include "../networkStack/networkStack.h"
typedef uintptr_t machineWord;
#define machineRegister(firstValue) (*(volatile uint32_t *)(uintptr_t)(firstValue))
#define serialDevice 0xfe201000u
#define generalPurposeIo 0xfe200000u
#define mailboxAddress 0xfe00b880u
static inline void memoryBarrier(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t clockCount(void) { uint64_t temporaryData; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(temporaryData)); return temporaryData; }
static uint64_t frequency;
static volatile uint32_t mailboxData[64] __attribute__((aligned(16)));
static unsigned screenReady;
static uint32_t armMemoryKiB;

void *memset(void *dataPosition, int characterCode, size_t itemCount) { unsigned char *nextOffset = dataPosition; while (itemCount--) *nextOffset++ = characterCode; return dataPosition; }
void *memcpy(void *destinationData, const void *stringData, size_t itemCount) { unsigned char *firstValue = destinationData; const unsigned char *secondValue = stringData; while (itemCount--) *firstValue++ = *secondValue++; return destinationData; }

static int mailbox(void) {
    uint32_t request = (uint32_t)(uintptr_t)mailboxData | 8;
    uint64_t run = clockCount();
    memoryBarrier();
    while (machineRegister(mailboxAddress + 0x38) & 0x80000000u)
        if (clockCount() - run > frequency) return 0;
    machineRegister(mailboxAddress + 0x20) = request;
    for (;;) {
        if (!(machineRegister(mailboxAddress + 0x18) & 0x40000000u)) {
            uint32_t reply = machineRegister(mailboxAddress);
            if (reply == request) { memoryBarrier(); return mailboxData[1] == 0x80000000u; }
        }
        if (clockCount() - run > frequency) return 0;
    }
}

extern int32_t jshellOutput(int32_t, int32_t), jshellInput(void);
extern void terminalByte(unsigned);
extern int terminalPending(void);
extern void terminalPointer(unsigned,int,int),terminalHotkey(unsigned);
extern void terminalInputMode(unsigned);
#include "../remoteValue/remoteValue.h"
static int streams;
static unsigned uartPrevious;
machineWord boardStreams(machineWord isUsed) { streams=isUsed!=0; return 0; }
machineWord boardChannel(machineWord channel, machineWord characterCode) {
    if(streams && jshellOutput((int32_t)channel,(int32_t)(characterCode&255))) return 0;
    terminalByte(characterCode&255);
    remoteOutput(characterCode&255);
    if ((characterCode&255)==10 && uartPrevious!=13) {
        while (machineRegister(serialDevice + 0x18) & 0x20) __asm__ volatile("yield");
        machineRegister(serialDevice)=13;
    }
    uartPrevious=characterCode&255;
    while (machineRegister(serialDevice + 0x18) & 0x20) __asm__ volatile("yield");
    machineRegister(serialDevice) = (uint32_t)characterCode & 255;
    return 0;
}
machineWord boardPutc(machineWord characterCode) { return boardChannel(1,characterCode); }
machineWord boardRawGetc(void) {
    int remoteCharacter=remoteInput();if(remoteCharacter>=0)return remoteCharacter;
    if (machineRegister(serialDevice + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t value = machineRegister(serialDevice);
    if (value & 0xf00) { machineRegister(serialDevice + 4) = 0; return (uint32_t)-1; }
    return value & 255;
}
machineWord boardGetc(void) {
    network_poll();
    static unsigned inPacket,usedCapacity; static unsigned char packetData[6];
    if(terminalPending())return (uint32_t)-4096;
    if(streams){int32_t characterCode=jshellInput();if(characterCode!=-3)return (uint32_t)characterCode;}
    for(;;){
        int characterCode=(int32_t)boardRawGetc();if(characterCode<0)return (uint32_t)characterCode;
        if(!inPacket){if(characterCode!=30)return characterCode;inPacket=1;usedCapacity=0;continue;}
        packetData[usedCapacity++]=characterCode;if(usedCapacity<6)continue;inPacket=0;
        if(packetData[0]==1)terminalPointer(packetData[1],packetData[2]+packetData[3]*256,packetData[4]+packetData[5]*256);
        if(packetData[0]==2)terminalHotkey(packetData[1]);
        if(packetData[0]==3)terminalInputMode(packetData[1]);
        if(terminalPending())return (uint32_t)-4096;
    }
}
machineWord boardMillis(void) { return (uint32_t)(clockCount() / (frequency / 1000)); }
machineWord boardEl(void) { uint64_t temporaryData; __asm__ volatile("mrs %0, CurrentEL" : "=r"(temporaryData)); return temporaryData >> 2; }
static void putsUart(const char *stringData) { while (*stringData) boardPutc((unsigned char)*stringData++); }
static void hexUart(machineWord itemCount) { const char *hexadecimalDigits = "0123456789abcdef"; for (int stringData = 60; stringData >= 0; stringData -= 4) boardPutc(hexadecimalDigits[(itemCount >> stringData) & 15]); }
machineWord boardStop(machineWord stateValue) {
    putsUart("\r\nHALTED "); hexUart(stateValue); putsUart("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void kernelPanic(const char *causeValue) __attribute__((noreturn));
void kernelPanic(const char *causeValue) { putsUart("\r\nPANIC: "); putsUart(causeValue); boardStop(1); __builtin_unreachable(); }
void boardException(machineWord exceptionState, machineWord commandPosition, machineWord invalidAddress) {
    putsUart("\r\nEXCEPTION ESR="); hexUart(exceptionState);
    putsUart(" PC="); hexUart(commandPosition); putsUart(" FAR="); hexUart(invalidAddress);
    boardStop(2);
}
int boardPhysicalHardware(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    mailboxData[0]=32;mailboxData[1]=0;mailboxData[2]=0x10004;mailboxData[3]=8;mailboxData[4]=0;
    mailboxData[5]=mailboxData[6]=mailboxData[7]=0;
    return mailbox()&&mailboxData[4]==0x80000008u&&(mailboxData[5]||mailboxData[6]);
}
int boardMachineAddress(unsigned char *address) {
    mailboxData[0]=32;mailboxData[1]=0;mailboxData[2]=0x10003;mailboxData[3]=8;mailboxData[4]=0;
    mailboxData[5]=mailboxData[6]=mailboxData[7]=0;
    if(!mailbox()||(mailboxData[4]&0x80000000u)==0||(mailboxData[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&mailboxData[5];unsigned sumValue=0;
    for(unsigned ordinalIndex=0;ordinalIndex<6;ordinalIndex++){address[ordinalIndex]=data[ordinalIndex];sumValue|=data[ordinalIndex];}return sumValue&&!(address[0]&1);
}
void boardInit(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(frequency));
    machineRegister(serialDevice + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    machineRegister(generalPurposeIo + 4) = (machineRegister(generalPurposeIo + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    machineRegister(generalPurposeIo + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. failureValue 시 config.txt의 48MHz를 사용한다.
    mailboxData[0] = 36; mailboxData[1] = 0; mailboxData[2] = 0x38002; mailboxData[3] = 12;
    mailboxData[4] = 0; mailboxData[5] = 2; mailboxData[6] = 48000000; mailboxData[7] = 0; mailboxData[8] = 0;
    int clockHealthy = mailbox();
    uint32_t speedValue = clockHealthy && mailboxData[6] >= 1843200 ? mailboxData[6] : 48000000;
    mailboxData[0]=32; mailboxData[1]=0; mailboxData[2]=0x10005; mailboxData[3]=8; mailboxData[4]=0;
    mailboxData[5]=mailboxData[6]=mailboxData[7]=0;
    if (mailbox() && mailboxData[4]==0x80000008u) armMemoryKiB=mailboxData[6]/1024;
    uint32_t divisor64 = (uint32_t)(((uint64_t)speedValue * 4 + 57600) / 115200);
    machineRegister(serialDevice + 0x44) = 0x7ff;
    machineRegister(serialDevice + 0x24) = divisor64 / 64;
    machineRegister(serialDevice + 0x28) = divisor64 % 64;
    machineRegister(serialDevice + 0x2c) = (3u << 5) | (1u << 4);
    machineRegister(serialDevice + 0x38) = 0;
    machineRegister(serialDevice + 0x30) = 0x301;
    memoryBarrier();
    putsUart("JKOROS AARCH64 BARE METAL\r\n");
    userSystemInit();
    network_init();
}
machineWord boardFtp(machineWord action) { return (uint32_t)ftp_control((int)action); }
machineWord boardNetworkStatus(machineWord entryValue, machineWord index) { return readNetworkStatus(entryValue, index); }
machineWord boardNetworkSettings(machineWord action, machineWord address, machineWord maskValue, machineWord gatewayValue) { return (uint32_t)configureNetwork(action, address, maskValue, gatewayValue); }
machineWord boardSendResponse(machineWord address, machineWord orderValue) { return (uint32_t)startResponseTest(address, orderValue); }
machineWord boardReadResponse(machineWord entryValue) { return (uint32_t)readResponseTest(entryValue); }
machineWord boardPowerOff(void) {
    ftp_control(0);
    for (unsigned index=0; index<32; index++) closeNetwork(index);
    for (unsigned index=0; index<4; index++) boardUserControl(32+index);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    putsUart("\r\nPOWER OFF\r\n");
    while (machineRegister(serialDevice+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    machineRegister(0xfe100020ul)=0x5a000000u | (machineRegister(0xfe100020ul)&~0xfffu) | 0x555;
    machineRegister(0xfe100024ul)=0x5a000000u | 10;
    machineRegister(0xfe10001cul)=0x5a000000u | (machineRegister(0xfe10001cul)&~0x30u) | 0x20;
    memoryBarrier();
    for (;;) __asm__ volatile("wfe");
}

machineWord boardFramebuffer(void) {
    if (screenReady) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 currentItem 크기를 읽는다. */
    const uint32_t queryValue[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t requestedWidth = 640, requestedHeight = 480;
    for (size_t ordinalIndex = 0; ordinalIndex < sizeof(queryValue)/4; ordinalIndex++) mailboxData[ordinalIndex] = queryValue[ordinalIndex];
    if (mailbox() && mailboxData[4] == 0x80000008u &&
        mailboxData[5] >= 640 && mailboxData[5] <= 1920 &&
        mailboxData[6] >= 480 && mailboxData[6] <= 1080) {
        requestedWidth = mailboxData[5]; requestedHeight = mailboxData[6];
    }
    const uint32_t request[] = {
        35 * 4, 0,
        0x48003, 8, 0, requestedWidth, requestedHeight,
        0x48004, 8, 0, requestedWidth, requestedHeight,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t ordinalIndex = 0; ordinalIndex < sizeof(request)/4; ordinalIndex++) mailboxData[ordinalIndex] = request[ordinalIndex];
    // topValue 메시지의 actualData 길이를 useValue: 태그 appendEntry 시 lengthValue 불일치를 방지한다.
    mailboxData[0] = sizeof(request);
    if (!mailbox()) return 0;
    const unsigned responses[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned responseLength[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned ordinalIndex = 0; ordinalIndex < sizeof(responses)/sizeof(responses[0]); ordinalIndex++)
        if (mailboxData[responses[ordinalIndex]] != (0x80000000u | responseLength[ordinalIndex])) return 0;
    uint32_t backgroundValue = mailboxData[28] & 0x3fffffffu;
    uint32_t size = mailboxData[29];
    uint32_t receivedWidth = mailboxData[5], receivedHeight = mailboxData[6], receivedLineSpacing = mailboxData[33];
    if (mailboxData[15] != 32 || mailboxData[19] != 1 ||
        receivedWidth < 640 || receivedWidth > 1920 || receivedHeight < 480 || receivedHeight > 1080 ||
        mailboxData[10] < receivedWidth || mailboxData[11] < receivedHeight || mailboxData[23] || mailboxData[24] ||
        !backgroundValue || backgroundValue < 0x1000000 || (backgroundValue & 3) || receivedLineSpacing < receivedWidth * 4 || (receivedLineSpacing & 3) ||
        (uint64_t)receivedLineSpacing * receivedHeight > size || (uint64_t)backgroundValue + size > 0x40000000u)
        return 0;
    boardPrepareDrawing((volatile uint32_t *)(uintptr_t)backgroundValue, receivedWidth, receivedHeight, receivedLineSpacing);
    screenReady = 1;
    return 1;
}

// 단일 코어의 협력식 threadValue. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t saved[13]; } context;
static context contexts[3];
static unsigned char stacks[2][65536] __attribute__((aligned(16)));
static int isRunning[3] = {1, 0, 0};
static int currentTask;
extern void contextSwitch(context *, context *);
extern void javaTask(int32_t);
machineWord boardYield(void) {
    network_poll();
    int previousItem = currentTask, nextItem = (previousItem + 1) % 3;
    while (nextItem != previousItem && !isRunning[nextItem]) nextItem = (nextItem + 1) % 3;
    if (nextItem != previousItem) {
        for (unsigned ordinalIndex = 0; ordinalIndex < 2; ordinalIndex++)
            if (isRunning[ordinalIndex + 1] && *(uint64_t *)stacks[ordinalIndex] != 0x6b6f726f7373746bull)
                kernelPanic("task stack guard");
        currentTask = nextItem;
        contextSwitch(&contexts[previousItem], &contexts[nextItem]);
    }
    return 0;
}
static void taskBootstrap(void) {
    javaTask(currentTask);
    isRunning[currentTask] = 0;
    boardYield();
    kernelPanic("finished task resumed");
}
machineWord boardTaskCreate(machineWord identifierValue) {
    if (identifierValue < 1 || identifierValue > 2 || isRunning[identifierValue]) return (uint32_t)-1;
    memset(&contexts[identifierValue], 0, sizeof(context));
    *(uint64_t *)stacks[identifierValue - 1] = 0x6b6f726f7373746bull;
    contexts[identifierValue].saved[11] = (uintptr_t)taskBootstrap;
    contexts[identifierValue].saved[12] = (uintptr_t)(stacks[identifierValue - 1] + sizeof(stacks[0]));
    isRunning[identifierValue] = 1;
    return 0;
}
machineWord boardTaskState(machineWord identifierValue) { return identifierValue < 3 ? isRunning[identifierValue] : (uint32_t)-1; }
extern machineWord aotMemoryLookup(machineWord);
extern uint32_t readUserState(unsigned, unsigned);
extern unsigned char StackTop[];
machineWord boardQuerySystem(machineWord entryValue, machineWord index) {
    if (entryValue==0) return armMemoryKiB;
    if (entryValue==1) return ((uintptr_t)StackTop-0x80000+1023)/1024;
    if (entryValue==2 || entryValue==3) return aotMemoryLookup(entryValue==3);
    if (entryValue==4) return screenReady ? (boardScreenWidth()*boardScreenHeight()*4+1023)/1024 : 0;
    if (entryValue==5) return 80*1024; /* executeCommand addressRegion 16 MiB + 네 세션 preserveValue addressRegion. */
    if (entryValue>=20) return readUserState(entryValue-20, index);
    return 0;
}
int *pk_errno_location(void) { static int errors[3]; return &errors[currentTask]; }
