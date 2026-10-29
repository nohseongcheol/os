#include "../naming/machineLinkNames.h"
#include "screenInformation.h"
// EL0 executeCommand machine layerValue. file data/정책은 기존 AOT Java 커널에 위임한다.
#include "User.h"
#include "FileABI.h"
#include "NetworkABI.h"
#include "../networkStack/networkStack.h"
extern int32_t jnetRemote(int32_t), jstreamAddress(int32_t);
#define machineRegister(firstValue) (*(volatile uint32_t *)(uintptr_t)(firstValue))
#define interruptDistributor 0xff841000ul
#define interruptCpuInterface 0xff842000ul
#define pageSize 4096ul
#define accessMarker (1ul << 10)
#define noExecutePermission (1ul << 53)
#define userNoExecute (1ul << 54)
#define normalMemory ((1ul << 2) | (3ul << 8) | accessMarker)
#define kernelPage (3ul | normalMemory | noExecutePermission | userNoExecute)
#define userReadWrite (3ul | normalMemory | (1ul << 6) | noExecutePermission | userNoExecute)
#define userReadOnly (3ul | normalMemory | (3ul << 6) | noExecutePermission | userNoExecute)
#define userReadExecute (3ul | normalMemory | (3ul << 6) | noExecutePermission)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t boardPutc(uintptr_t), boardGetc(void), boardMillis(void);
extern uintptr_t boardPixel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t boardFramebuffer(void);
extern uintptr_t boardTerminal(uintptr_t);
extern int terminalPending(void);
extern int32_t jshellInteractive(void);
extern int32_t javaPathStart(int32_t), javaPathByte(int32_t,int32_t);
extern int32_t javaCreateDirectory(void), javaRemoveDirectory(void), javaEntryKind(void);
extern int invokeScreen(int,unsigned,int,int,int,int,int),screenText(int,int,const uint32_t *,unsigned);
extern void initializeScreen(int),screenPress(int,unsigned);
extern int userResume(userFrame *,void *);
extern void userFpSave(void *);
extern int userEnter(uintptr_t entryPoint, uintptr_t stackStorage, uintptr_t forwardedValue);
extern void userReturn(void);
extern void kernelPanic(const char *) __attribute__((noreturn));
static uint64_t rootAddress[512] __attribute__((aligned(4096)));
static uint64_t middle[4][512] __attribute__((aligned(4096)));
static uint64_t pageList[userPageCount] __attribute__((aligned(4096)));
static uint8_t permissionsList[userPageCount];
static int active, fileList[16], linuxAbi;
static unsigned socketEndpoints[24];
extern int32_t jnetSocket(int32_t, int32_t, int32_t), jnetBind(int32_t, int32_t, int32_t);
extern int32_t jnetPut(int32_t, int32_t), jnetGet(int32_t), jnetSend(int32_t, int32_t, int32_t, int32_t);
extern int32_t jnetRecv(int32_t, int32_t), jnetPort(int32_t), jnetAddress(int32_t), jnetPeer(int32_t), jnetClose(int32_t);
extern int32_t jstreamCreate(void),jstreamBind(int32_t,int32_t,int32_t),jstreamListen(int32_t,int32_t),jstreamConnect(int32_t,int32_t,int32_t),jstreamAccept(int32_t),jstreamRead(int32_t,int32_t),jstreamWrite(int32_t,int32_t),jstreamPort(int32_t),jstreamPeer(int32_t),jstreamClose(int32_t);
static int closeSocketEndpoint(unsigned fileHandle){return fileHandle<40?jnetClose(fileHandle):jstreamClose(fileHandle);}
static uint64_t frequency, deadlineTime;
static uintptr_t heapEnd;
// kernelValue 셸이 준비한 UTF-8 arguments. EL0에는 copyValue 호출만 제공한다.
static unsigned forwardedArgumentCount, forwardedArgumentLength[8];
static unsigned char forwardedArgument[8][256];
typedef struct {
    int pausedState,interactive,linuxAbi,fileList[16]; unsigned socketEndpoints[24],argumentsCount,arglen[8];
    unsigned char argumentArray[8][256],permissionsList[userPageCount];
    uintptr_t heapStorage; userFrame executionFrame;
    unsigned char floatingPointState[528] __attribute__((aligned(16)));
} savedProcess;
static savedProcess saved[4];
static int ownerObject,interactive;
static uint32_t userNumber[4], userStartTime[4], userAccumulatedTime[4], userExecutionTime[4], nextUserNumber=10;
static unsigned char userCommandName[4][288];
uint32_t readUserState(unsigned entryValue, unsigned index) {
    unsigned positionIndex=index&3;
    int stateValue=(active && ownerObject==(int)positionIndex) ? 1 : saved[positionIndex].pausedState ? 2 : 0;
    if (entryValue==0) return stateValue;
    if (!stateValue) return 0;
    if (entryValue==1) return userNumber[positionIndex];
    if (entryValue==2) {
        unsigned char *pagesList=stateValue==1?permissionsList:saved[positionIndex].permissionsList;
        unsigned pageCount=0; for (unsigned ordinalIndex=0; ordinalIndex<userPageCount; ordinalIndex++) if(pagesList[ordinalIndex]) pageCount++;
        return pageCount*4;
    }
    if (entryValue==3) return (uint32_t)boardMillis()-userStartTime[positionIndex];
    if (entryValue==4) return userAccumulatedTime[positionIndex]+(stateValue==1?(uint32_t)boardMillis()-userExecutionTime[positionIndex]:0);
    if (entryValue==5) return index/4<sizeof(userCommandName[0])?userCommandName[positionIndex][index/4]:0;
    return 0;
}
uintptr_t boardArgsBegin(uintptr_t entryCount) {
    if (active || entryCount > 8) return (uint32_t)-22;
    forwardedArgumentCount = entryCount;
    memset(forwardedArgumentLength, 0, sizeof(forwardedArgumentLength));
    memset(forwardedArgument, 0, sizeof(forwardedArgument));
    return 0;
}
uintptr_t boardArgsByte(uintptr_t lookupIndex, uintptr_t currentPosition, uintptr_t byteData) {
    if (active || lookupIndex >= forwardedArgumentCount || currentPosition >= 255 || currentPosition != forwardedArgumentLength[lookupIndex] || !byteData || byteData > 255)
        return (uint32_t)-22;
    forwardedArgument[lookupIndex][currentPosition] = byteData;
    forwardedArgumentLength[lookupIndex] = currentPosition + 1;
    return 0;
}
static void syncTables(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t clockValue(void) { uint64_t temporaryData; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(temporaryData)); return temporaryData; }
static void stopTimeout(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    machineRegister(interruptDistributor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void startTimeout(void) {
    uint64_t spacingValue = frequency * 2, enable = 1;
    deadlineTime = clockValue() + spacingValue;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(spacingValue), "r"(enable) : "memory");
}
void userSystemInit(void) {
    for (unsigned dataBlock = 0; dataBlock < 4; dataBlock++) {
        rootAddress[dataBlock] = (uintptr_t)middle[dataBlock] | 3;
        for (unsigned ordinalIndex = 0; ordinalIndex < 512; ordinalIndex++) {
            uintptr_t address = ((uintptr_t)dataBlock << 30) | ((uintptr_t)ordinalIndex << 21);
            middle[dataBlock][ordinalIndex] = address | 1 | accessMarker | userNoExecute;
            if (address >= 0xfc000000ul) middle[dataBlock][ordinalIndex] |= noExecutePermission; // Device-nGnRnE
            else middle[dataBlock][ordinalIndex] |= normalMemory; // Normal, non-cacheable
        }
    }
    for (unsigned secondValue = 0; secondValue < userPageCount / 512; secondValue++)
        middle[0][(userBase >> 21) + secondValue] = (uintptr_t)(pageList + secondValue * 512) | 3;
    for (unsigned ordinalIndex = 0; ordinalIndex < userPageCount; ordinalIndex++) pageList[ordinalIndex] = (userBase + ordinalIndex * pageSize) | kernelPage;
    uint64_t memoryAttributeRegister = 0x4400, addressTranslationControl = 32 | (3ul << 12) | (1ul << 23), sctlr;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(memoryAttributeRegister), "r"(addressTranslationControl), "r"((uintptr_t)rootAddress) : "memory");
    syncTables();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(sctlr));
    sctlr = (sctlr & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(sctlr) : "memory");
    uint64_t floatingPointState = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(floatingPointState) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(frequency));
    stopTimeout();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 entryPointValue 때만 allowValue.
    machineRegister(interruptDistributor) = 0;
    machineRegister(interruptDistributor + 0x180) = 0xffffffff;
    machineRegister(interruptDistributor + 0x80) = 0xffffffff;
    machineRegister(interruptDistributor + 0x280) = 1u << 30;
    machineRegister(interruptDistributor + 0x41c) = 0x80808080;
    machineRegister(interruptDistributor + 0x100) = 1u << 30;
    machineRegister(interruptCpuInterface + 4) = 0xff;
    machineRegister(interruptCpuInterface + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 isNormal 확인할 number 있다.
    int security = (machineRegister(interruptDistributor + 4) & (1u << 10)) != 0;
    machineRegister(interruptDistributor) = security ? 1 : 3;
    machineRegister(interruptCpuInterface) = security ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char ident[16]; uint16_t typeCategory, machineType; uint32_t versionNumber;
    uint64_t entryPoint, programHeaderOffset, sectionHeaderOffset; uint32_t configurationBits;
    uint16_t executableHeaderSize, programHeaderEntrySize, programHeaderCount, sectionHeaderEntrySize, sectionHeaderCount, sectionNameTableIndex;
} elfHeader;
typedef struct { uint32_t typeCategory, configurationBits; uint64_t offsetValue, address, physicalAddress, filesz, memsz, alignBoundary; } elfProgram;
_Static_assert(sizeof(elfHeader) == 64 && sizeof(elfProgram) == 56, "ELF layout");
_Static_assert(sizeof(userFrame) == 272, "exception assembly layout");
static int contained(uint64_t offsetValue, uint64_t size, uint64_t endOffset) {
    return offsetValue <= endOffset && size <= endOffset - offsetValue;
}
static int checkAuxiliaryInformation(const unsigned char *dataPosition, size_t size) {
    size_t currentPosition = 0;
    while (contained(currentPosition, 12, size)) {
        uint32_t lexicalWords[3]; memcpy(lexicalWords, dataPosition + currentPosition, 12); currentPosition += 12;
        uint64_t namesz = ((uint64_t)lexicalWords[0] + 3) & ~3ul;
        uint64_t descsz = ((uint64_t)lexicalWords[1] + 3) & ~3ul;
        if (!contained(currentPosition, namesz, size) || !contained(currentPosition + namesz, descsz, size)) return 0;
        const unsigned char name[] = {'J','K','O','R','O','S',0};
        int isEqual = lexicalWords[0] == sizeof(name) && lexicalWords[1] == 4 && lexicalWords[2] == 1;
        if (isEqual) for (unsigned ordinalIndex = 0; ordinalIndex < sizeof(name); ordinalIndex++) if (dataPosition[currentPosition + ordinalIndex] != name[ordinalIndex]) isEqual = 0;
        uint32_t versionNumber = 0;
        if (isEqual) memcpy(&versionNumber, dataPosition + currentPosition + namesz, 4);
        if (isEqual && versionNumber == 1) return 1;
        currentPosition += namesz + descsz;
    }
    return 0;
}
static int validateElf(const unsigned char *data, size_t size, int linuxMode) {
    if (size < sizeof(elfHeader)) return userExecutableError;
    elfHeader executableHeader; memcpy(&executableHeader, data, sizeof(executableHeader));
    if (executableHeader.ident[0] != 127 || executableHeader.ident[1] != 'E' || executableHeader.ident[2] != 'L' || executableHeader.ident[3] != 'F' ||
        executableHeader.ident[4] != 2 || executableHeader.ident[5] != 1 || executableHeader.ident[6] != 1 || (executableHeader.ident[7] != 0 && (!linuxMode || executableHeader.ident[7] != 3)) ||
        executableHeader.typeCategory != 2 || executableHeader.machineType != 183 || executableHeader.versionNumber != 1 || executableHeader.configurationBits || executableHeader.executableHeaderSize != sizeof(executableHeader) ||
        executableHeader.programHeaderEntrySize != sizeof(elfProgram) || !executableHeader.programHeaderCount || executableHeader.programHeaderCount > 16 ||
        executableHeader.programHeaderOffset < sizeof(executableHeader) || !contained(executableHeader.programHeaderOffset, (uint64_t)executableHeader.programHeaderCount * sizeof(elfProgram), size)) return userExecutableError;
    uint8_t usedCapacity[(userImageEnd - userBase) / pageSize] = {0};
    int validEntryPoint = 0, abiOk = 0, loads = 0;
    for (unsigned ordinalIndex = 0; ordinalIndex < executableHeader.programHeaderCount; ordinalIndex++) {
        elfProgram dataPosition; memcpy(&dataPosition, data + executableHeader.programHeaderOffset + ordinalIndex * sizeof(dataPosition), sizeof(dataPosition));
        if (dataPosition.typeCategory == 4) {
            if (!contained(dataPosition.offsetValue, dataPosition.filesz, size)) return userExecutableError;
            if (checkAuxiliaryInformation(data + dataPosition.offsetValue, dataPosition.filesz)) abiOk = 1;
            continue;
        }
        if (dataPosition.typeCategory == 0 || dataPosition.typeCategory == 6 || (dataPosition.typeCategory == 0x6474e551 && !(dataPosition.configurationBits & 1))) continue;
        if (dataPosition.typeCategory != 1) return userExecutableError; // PT_INTERP, DYNAMIC, TLS isUnsupported
        if (!dataPosition.memsz) continue;
        if (dataPosition.configurationBits & ~7u || !(dataPosition.configurationBits & 4) || (dataPosition.configurationBits & 3) == 3 || dataPosition.filesz > dataPosition.memsz ||
            (dataPosition.filesz && !contained(dataPosition.offsetValue, dataPosition.filesz, size)) || dataPosition.address < userBase ||
            !contained(dataPosition.address, dataPosition.memsz, userImageEnd) ||
            (!linuxMode && ((dataPosition.address & (pageSize - 1)) || (dataPosition.offsetValue & (pageSize - 1)) || dataPosition.alignBoundary != pageSize)) ||
            (linuxMode && (((dataPosition.address ^ dataPosition.offsetValue) & (pageSize - 1)) || !dataPosition.alignBoundary ||
                (dataPosition.alignBoundary & (dataPosition.alignBoundary - 1)) || dataPosition.alignBoundary > 0x200000 || ((dataPosition.address ^ dataPosition.offsetValue) & (dataPosition.alignBoundary - 1))))) return userExecutableError;
        unsigned firstEntry = (dataPosition.address - userBase) / pageSize;
        unsigned entryCount = ((dataPosition.address & (pageSize - 1)) + dataPosition.memsz + pageSize - 1) / pageSize;
        for (unsigned pageValue = firstEntry; pageValue < firstEntry + entryCount; pageValue++) {
            if (usedCapacity[pageValue]) return userExecutableError;
            usedCapacity[pageValue] = 1;
        }
        if ((dataPosition.configurationBits & 1) && executableHeader.entryPoint >= dataPosition.address && executableHeader.entryPoint < dataPosition.address + dataPosition.filesz && !(executableHeader.entryPoint & 3)) validEntryPoint = 1;
        loads++;
    }
    return validEntryPoint && (linuxMode ? !abiOk : abiOk) && loads ? 0 : userExecutableError;
}
int userValidateElf(const unsigned char *data, size_t size) { return validateElf(data, size, 0); }
static void pageLayout(uintptr_t address, uint64_t configurationBits, unsigned accessPermissions) {
    unsigned lookupIndex = (address - userBase) / pageSize;
    pageList[lookupIndex] = address | configurationBits;
    permissionsList[lookupIndex] = accessPermissions;
}
static int userRange(uintptr_t address, size_t entryCount, int writing) {
    if (address < userBase || !contained(address, entryCount, userEnd)) return 0;
    if (!entryCount) return 1;
    unsigned firstEntry = (address - userBase) / pageSize, lastItem = (address + entryCount - 1 - userBase) / pageSize;
    for (unsigned ordinalIndex = firstEntry; ordinalIndex <= lastItem; ordinalIndex++) if (!(permissionsList[ordinalIndex] & (writing ? 2 : 1))) return 0;
    return 1;
}
static int copyPath(uintptr_t address, char *path) {
    for (unsigned ordinalIndex = 0; ordinalIndex < 65; ordinalIndex++) {
        if (!userRange(address, 1, 0)) return -14;
        path[ordinalIndex] = *(const char *)address++;
        if (!path[ordinalIndex]) return 0;
    }
    return -36;
}
static intptr_t kernelResult(intptr_t result) { return result < 0 ? -errorNumber : result; }
static int mappedFd(uint64_t fileHandle) { return fileHandle >= 3 && fileHandle < 19 ? fileList[fileHandle - 3] : -1; }
static int socketEndpointOwner(uint64_t fileHandle) { return fileHandle >= 32 && fileHandle < 56 && socketEndpoints[fileHandle - 32]; }
static int addressInput(uintptr_t pointingValue, size_t lengthValue, struct pk_sockaddr_in *address) {
    if (lengthValue != sizeof(*address)) return -22;
    if (!userRange(pointingValue, lengthValue, 0)) return -14;
    memcpy(address, (const void *)pointingValue, sizeof(*address));
    return address->sin_family == AF_INET ? 0 : -97;
}
static int addressOutputCheck(uintptr_t pointingValue, uintptr_t lengthPointer, pk_socklen_t *bufferCapacity) {
    if (!userRange(lengthPointer, sizeof(*bufferCapacity), 1)) return -14;
    memcpy(bufferCapacity, (const void *)lengthPointer, sizeof(*bufferCapacity));
    if (*bufferCapacity > sizeof(struct pk_sockaddr_in)) *bufferCapacity = sizeof(struct pk_sockaddr_in);
    if (*bufferCapacity && !userRange(pointingValue, *bufferCapacity, 1)) return -14;
    return 0;
}
static void addressOutput(uintptr_t pointingValue, uintptr_t lengthPointer, pk_socklen_t bufferCapacity, int address, int portNumber) {
    struct pk_sockaddr_in value; memset(&value, 0, sizeof(value));
    value.sin_family = AF_INET; value.sin_port = pk_htons(portNumber); value.sin_addr.s_addr = pk_htonl(address);
    if (bufferCapacity) memcpy((void *)pointingValue, &value, bufferCapacity);
    pk_socklen_t lengthValue = sizeof(value); memcpy((void *)lengthPointer, &lengthValue, sizeof(lengthValue));
}
extern uintptr_t boardChannel(uintptr_t, uintptr_t);
static intptr_t nativeSystemCall(userFrame *fileEntry) {
    uintptr_t firstValue = fileEntry->registerData[0], secondValue = fileEntry->registerData[1], characterCode = fileEntry->registerData[2];
    char path[65];
    int fileHandle, result;
    switch (fileEntry->registerData[8]) {
    case 0: return 1; // Native ABI 버전
    case 1: // write: pointer 전체를 검사한 backValue Output/file changeValue
        if (characterCode > 65536) return -22;
        if (!userRange(secondValue, characterCode, 0)) return -14;
        if (firstValue == 1 || firstValue == 2) {
            uint64_t startOutput=clockValue();
            for (size_t ordinalIndex = 0; ordinalIndex < characterCode; ordinalIndex++) boardChannel(firstValue, ((const unsigned char *)secondValue)[ordinalIndex]);
            /* 큰 tty를 그린 kernelValue 시간만 돌려준다. EL0 calculation 기한은 늘리지 않는다. */
            if(interactive){
                deadlineTime+=clockValue()-startOutput;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(deadlineTime) : "memory");
            }
            return characterCode;
        }
        if(firstValue>=40&&socketEndpointOwner(firstValue)){
            size_t itemCount=characterCode>512?512:characterCode;for(size_t ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)jnetPut(ordinalIndex,((const unsigned char *)secondValue)[ordinalIndex]);return jstreamWrite(firstValue,itemCount);
        }
        fileHandle = mappedFd(firstValue); if (fileHandle < 0) return -9;
        return kernelResult(pk_write(fileHandle, (const void *)secondValue, characterCode));
    case 2:
        if (characterCode > 65536) return -22;
        if (!userRange(secondValue, characterCode, 1)) return -14;
        if (firstValue == 0) {
            size_t itemCount = 0;
            while (itemCount < characterCode) {
                int characterValue = (int32_t)boardGetc(); if (characterValue == -2) return itemCount; if (characterValue < 0) break;
                ((unsigned char *)secondValue)[itemCount++] = characterValue;
            }
            return itemCount ? (intptr_t)itemCount : (characterCode ? -11 : 0);
        }
        if(firstValue>=40&&socketEndpointOwner(firstValue)){
            result=jstreamRead(firstValue,characterCode>512?512:characterCode);if(result>0)for(int ordinalIndex=0;ordinalIndex<result;ordinalIndex++)((unsigned char *)secondValue)[ordinalIndex]=jnetGet(ordinalIndex);return result;
        }
        fileHandle = mappedFd(firstValue); if (fileHandle < 0) return -9;
        return kernelResult(pk_read(fileHandle, (void *)secondValue, characterCode));
    case 3:
        result = copyPath(firstValue, path); if (result) return result;
        if (secondValue > 0x7ff) return -22;
        for (unsigned ordinalIndex = 0; ordinalIndex < 16; ordinalIndex++) if (fileList[ordinalIndex] < 0) {
            fileHandle = pk_open(path, (int)secondValue, 0600);
            if (fileHandle < 0) return -errorNumber;
            fileList[ordinalIndex] = fileHandle; return ordinalIndex + 3;
        }
        return -24;
    case 4:
        if (socketEndpointOwner(firstValue)) { result = closeSocketEndpoint(firstValue); if (!result) socketEndpoints[firstValue - 32] = 0; return result; }
        fileHandle = mappedFd(firstValue); if (fileHandle < 0) return -9;
        result = pk_close(fileHandle); if (!result) fileList[firstValue - 3] = -1;
        return kernelResult(result);
    case 5:
        fileHandle = mappedFd(firstValue); if (fileHandle < 0) return -9;
        if (characterCode > 2) return -22;
        return kernelResult(pk_lseek(fileHandle, (int64_t)secondValue, characterCode));
    case 7: return boardMillis();
    case 8: { // brk: 별도 User RW/NX heapValue, 새로 노출되는 페이지는 0으로 initialize
        if (!firstValue) return heapEnd;
        if (firstValue < userImageEnd || firstValue > userHeapEnd) return -12;
        uintptr_t oldPages = (heapEnd + pageSize - 1) & ~(pageSize - 1);
        uintptr_t newPages = (firstValue + pageSize - 1) & ~(pageSize - 1);
        if (newPages > oldPages) {
            for (uintptr_t dataPosition = oldPages; dataPosition < newPages; dataPosition += pageSize) pageLayout(dataPosition, kernelPage, 0);
            syncTables();
            memset((void *)oldPages, 0, newPages - oldPages);
            for (uintptr_t dataPosition = oldPages; dataPosition < newPages; dataPosition += pageSize) pageLayout(dataPosition, userReadWrite, 3);
        } else {
            for (uintptr_t dataPosition = newPages; dataPosition < oldPages; dataPosition += pageSize) {
                pageList[(dataPosition - userBase) / pageSize] = 0; permissionsList[(dataPosition - userBase) / pageSize] = 0;
            }
        }
        heapEnd = firstValue; syncTables(); return firstValue;
    }
    case 9:
        fileHandle = mappedFd(firstValue); return fileHandle < 0 ? -9 : kernelResult(pk_size(fileHandle));
    case 10:
        fileHandle = mappedFd(firstValue); return fileHandle < 0 ? -9 : kernelResult(pk_ftruncate(fileHandle, (int64_t)secondValue));
    case 11:
        result = copyPath(firstValue, path); return result ? result : kernelResult(pk_unlink(path));
    case 12:
        fileHandle = mappedFd(firstValue); return fileHandle < 0 ? -9 : kernelResult(pk_fsync(fileHandle));
    case 13: { // 그래픽 기초 API: User 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t requestedWidthValue = fileEntry->registerData[3], requestedHeightValue = fileEntry->registerData[4];
        if (!boardFramebuffer()) return -19;
        uintptr_t screenSpan = boardScreenWidth(), screenLength = boardScreenHeight();
        if (firstValue > screenSpan || secondValue > screenLength || requestedWidthValue > screenSpan - firstValue || requestedHeightValue > screenLength - secondValue) return -22;
        for (uintptr_t yCoordinate = secondValue; yCoordinate < secondValue + requestedHeightValue; yCoordinate++) for (uintptr_t xCoordinate = firstValue; xCoordinate < firstValue + requestedWidthValue; xCoordinate++) boardPixel(xCoordinate, yCoordinate, characterCode);
        return 0;
    }
    case 14: return (int32_t)boardGetc();
    case 15: // args(-1,0,0)=itemCount; args(index,buffer,capacity)=UTF-8 lengthValue
        if (firstValue == UINTPTR_MAX) return forwardedArgumentCount;
        if (firstValue >= forwardedArgumentCount) return -22;
        if (characterCode <= forwardedArgumentLength[firstValue]) return -36;
        if (!userRange(secondValue, forwardedArgumentLength[firstValue] + 1, 1)) return -14;
        memcpy((void *)secondValue, forwardedArgument[firstValue], forwardedArgumentLength[firstValue] + 1);
        return forwardedArgumentLength[firstValue];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(firstValue==0){if(!jshellInteractive())return -95;interactive=1;return boardTerminal(13);}
        if(firstValue==2){interactive=0;return 0;}
        if(firstValue==3)return boardTerminal(13);
        if(firstValue!=1||!interactive)return -22;
        result=(int32_t)boardGetc();
        if(result==-4096)return result;
        startTimeout();return result<0?-11:result;
    case 17: { // 유한한 협력 waitValue: communication 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (firstValue > 100) return -22;
        uint64_t endTime = clockValue() + frequency * firstValue / 1000;
        do { inspectNetwork(); inspectFileTransfer(); __asm__ volatile("yield"); } while (clockValue() < endTime);
        startTimeout(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 parentValue·빈 폴더를 검사한다.
        if (secondValue > 2) return -22;
        result = copyPath(firstValue, path); if (result) return result;
        unsigned lengthValue = 0; while (path[lengthValue]) lengthValue++;
        result = javaPathStart(lengthValue); if (result < 0) return result;
        for (unsigned ordinalIndex = 0; ordinalIndex < lengthValue; ordinalIndex++) javaPathByte(ordinalIndex, (unsigned char)path[ordinalIndex]);
        return secondValue == 0 ? javaEntryKind() : secondValue == 1 ? javaCreateDirectory() : javaRemoveDirectory();
    }
    case 20:
        if(firstValue==5){int characterValue=(int32_t)boardGetc();if(characterValue==-4096)return characterValue;if(characterValue>=0)screenPress(ownerObject,characterValue);startTimeout();}
        if(firstValue==3&&characterCode){if(!jshellInteractive())return -95;interactive=1;boardTerminal(300);}
        return invokeScreen(ownerObject,firstValue,secondValue,characterCode,fileEntry->registerData[3],fileEntry->registerData[4],fileEntry->registerData[5]);
    case 21:
        if(characterCode>127)return -22;if(!userRange(secondValue,characterCode*sizeof(uint32_t),0))return -14;
        return screenText(ownerObject,firstValue,(const uint32_t *)secondValue,characterCode);
    case 22: // Screen size queryValue: 0=widthValue, 1=heightValue. 사용자에게 주소를 노출하지 않는다.
        if (firstValue > 1) return -22;
        if (!boardFramebuffer()) return -19;
        return firstValue == 0 ? boardScreenWidth() : boardScreenHeight();
    case 32:
        if (firstValue != AF_INET) return -97;
        if(secondValue==SOCK_STREAM&&(characterCode==0||characterCode==6))result=jstreamCreate();
        else if(secondValue==SOCK_DGRAM&&(characterCode==0||characterCode==IPPROTO_UDP))result=jnetSocket(firstValue,secondValue,characterCode);
        else return -93;
        if (result >= 32 && result < 56) socketEndpoints[result - 32] = 1;
        return result;
    case 33: {
        if (!socketEndpointOwner(firstValue)) return -9;
        struct pk_sockaddr_in address;
        result = addressInput(secondValue, characterCode, &address); if (result) return result;
        return firstValue>=40?jstreamBind(firstValue,pk_htonl(address.sin_addr.s_addr),pk_htons(address.sin_port)):jnetBind(firstValue, pk_htonl(address.sin_addr.s_addr), pk_htons(address.sin_port));
    }
    case 34: {
        if (!socketEndpointOwner(firstValue)) return -9;
        if(firstValue>=40)return -95;
        if (fileEntry->registerData[3]) return -95;
        if (characterCode > 512) return -90;
        if (characterCode && !userRange(secondValue, characterCode, 0)) return -14;
        struct pk_sockaddr_in address;
        result = addressInput(fileEntry->registerData[4], fileEntry->registerData[5], &address); if (result) return result;
        for (unsigned ordinalIndex = 0; ordinalIndex < characterCode; ordinalIndex++) jnetPut(ordinalIndex, ((const unsigned char *)secondValue)[ordinalIndex]);
        return jnetSend(firstValue, pk_htonl(address.sin_addr.s_addr), pk_htons(address.sin_port), characterCode);
    }
    case 35: {
        if (!socketEndpointOwner(firstValue)) return -9;
        if(firstValue>=40)return -95;
        if (fileEntry->registerData[3]) return -95;
        if (characterCode > 512) return -90;
        if (characterCode && !userRange(secondValue, characterCode, 1)) return -14;
        pk_socklen_t bufferCapacity = 0;
        if (fileEntry->registerData[4]) { result = addressOutputCheck(fileEntry->registerData[4], fileEntry->registerData[5], &bufferCapacity); if (result) return result; }
        result = jnetRecv(firstValue, characterCode); if (result < 0) return result;
        for (int ordinalIndex = 0; ordinalIndex < result; ordinalIndex++) ((unsigned char *)secondValue)[ordinalIndex] = jnetGet(ordinalIndex);
        if (fileEntry->registerData[4]) addressOutput(fileEntry->registerData[4], fileEntry->registerData[5], bufferCapacity, jnetRemote(firstValue), jnetPeer(firstValue));
        return result;
    }
    case 36: {
        if (!socketEndpointOwner(firstValue)) return -9;
        pk_socklen_t bufferCapacity;
        result = addressOutputCheck(secondValue, characterCode, &bufferCapacity); if (result) return result;
        addressOutput(secondValue,characterCode,bufferCapacity,firstValue>=40?jstreamAddress(firstValue):jnetAddress(firstValue),firstValue>=40?jstreamPort(firstValue):jnetPort(firstValue)); return 0;
    }
    case 37: {
        if(firstValue<40||!socketEndpointOwner(firstValue))return -9;struct pk_sockaddr_in address;
        result=addressInput(secondValue,characterCode,&address);if(result)return result;
        return jstreamConnect(firstValue,pk_htonl(address.sin_addr.s_addr),pk_htons(address.sin_port));
    }
    case 38: return firstValue>=40&&socketEndpointOwner(firstValue)?jstreamListen(firstValue,secondValue):-9;
    case 39:
        if(firstValue<40||!socketEndpointOwner(firstValue))return -9;
        if(secondValue||characterCode)return -95;result=jstreamAccept(firstValue);if(result>=40&&result<56)socketEndpoints[result-32]=1;return result;
    case 40: return firstValue>=40&&socketEndpointOwner(firstValue)?jstreamPeer(firstValue):-9;
    default: return -38; // isUnsupported 기능을 성공으로 가장하지 않음
    }
}
#include "linuxCompatibility.inc"
static intptr_t invokeSystemCall(userFrame *fileEntry) {
    network_poll();
    return linuxAbi ? linuxSystemCall(fileEntry) : nativeSystemCall(fileEntry);
}
static void returnKernel(userFrame *fileEntry, int result) {
    stopTimeout();
    fileEntry->registerData[0] = (uint64_t)(int64_t)result;
    fileEntry->commandPosition = (uintptr_t)userReturn;
    fileEntry->stateCode = 0x3c5; // EL1h, DAIF masked
}
int userException(userFrame *fileEntry, unsigned intercept) {
    if (!active || (fileEntry->stateCode & 15) != 0) return 0;
    if (intercept) {
        uint32_t acknowledgementValue = machineRegister(interruptCpuInterface + 0xc), identifierValue = acknowledgementValue & 1023;
        if (identifierValue == 30) { returnKernel(fileEntry, userTimeout); machineRegister(interruptCpuInterface + 0x10) = acknowledgementValue; return 1; }
        if (identifierValue < 1020) machineRegister(interruptCpuInterface + 0x10) = acknowledgementValue;
        return 1;
    }
    uint64_t exceptionState; __asm__ volatile("mrs %0, esr_el1" : "=r"(exceptionState));
    if (clockValue() >= deadlineTime) { returnKernel(fileEntry, userTimeout); return 1; }
    unsigned exceptionCategory = exceptionState >> 26;
    if (exceptionCategory == 0x15 && (exceptionState & 0xffff) == 0) {
        if (linuxAbi ? fileEntry->registerData[8] == 93 || fileEntry->registerData[8] == 94 : fileEntry->registerData[8] == 6) returnKernel(fileEntry, (int)(fileEntry->registerData[0] & 255));
        else {
            intptr_t result=invokeSystemCall(fileEntry);
            if(result==-4096&&interactive){
                saved[ownerObject].executionFrame=*fileEntry;saved[ownerObject].executionFrame.commandPosition-=4;
                userFpSave(saved[ownerObject].floatingPointState);returnKernel(fileEntry,userInterrupted);
            }else fileEntry->registerData[0]=(uint64_t)result;
        }
    } else returnKernel(fileEntry, exceptionCategory == 0x24 ? userDataError : exceptionCategory == 0x20 ? userExecutionError : userInvalidInstruction);
    return 1;
}

// 생성된 const ELF groupValue: 실행은 반드시 Program 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t size; unsigned forwardedValue; } program;
#include "programs.h"
static void *snapshot(unsigned positionIndex){return (void *)(0x04000000ul+positionIndex*(userEnd-userBase));}
static int finishProgram(int result){
    userAccumulatedTime[ownerObject]+=(uint32_t)boardMillis()-userExecutionTime[ownerObject];
    stopTimeout();active=0;
    if(result==userInterrupted){
        savedProcess *stringData=&saved[ownerObject];stringData->pausedState=1;stringData->interactive=interactive;stringData->linuxAbi=linuxAbi;stringData->heapStorage=heapEnd;stringData->argumentsCount=forwardedArgumentCount;
        memcpy(stringData->permissionsList,permissionsList,sizeof(permissionsList));memcpy(stringData->fileList,fileList,sizeof(fileList));memcpy(stringData->socketEndpoints,socketEndpoints,sizeof(socketEndpoints));
        memcpy(stringData->argumentArray,forwardedArgument,sizeof(forwardedArgument));memcpy(stringData->arglen,forwardedArgumentLength,sizeof(forwardedArgumentLength));
        for(unsigned ordinalIndex=0;ordinalIndex<userPageCount;ordinalIndex++)if(permissionsList[ordinalIndex])memcpy((unsigned char *)snapshot(ownerObject)+ordinalIndex*pageSize,(void *)(userBase+ordinalIndex*pageSize),pageSize);
    }else{
        saved[ownerObject].pausedState=0;initializeScreen(ownerObject);
        for(unsigned ordinalIndex=0;ordinalIndex<16;ordinalIndex++)if(fileList[ordinalIndex]>=0)pk_close(fileList[ordinalIndex]);
        for(unsigned ordinalIndex=0;ordinalIndex<24;ordinalIndex++)if(socketEndpoints[ordinalIndex])closeSocketEndpoint(ordinalIndex+32);
    }
    for(unsigned ordinalIndex=0;ordinalIndex<userPageCount;ordinalIndex++){pageList[ordinalIndex]=0;permissionsList[ordinalIndex]=0;}syncTables();return result;
}
uintptr_t boardUserControl(uintptr_t action){
    unsigned positionIndex=action&15;if(positionIndex>=4||active)return (uint32_t)-22;
    savedProcess *stringData=&saved[positionIndex];
    if(action>=32){if(stringData->pausedState){for(unsigned ordinalIndex=0;ordinalIndex<16;ordinalIndex++)if(stringData->fileList[ordinalIndex]>=0)pk_close(stringData->fileList[ordinalIndex]);for(unsigned ordinalIndex=0;ordinalIndex<24;ordinalIndex++)if(stringData->socketEndpoints[ordinalIndex])closeSocketEndpoint(ordinalIndex+32);}stringData->pausedState=0;initializeScreen(positionIndex);return 0;}
    if(action>=16)return stringData->pausedState;
    if(!stringData->pausedState)return (uint32_t)-22;
    ownerObject=positionIndex;interactive=stringData->interactive;linuxAbi=stringData->linuxAbi;heapEnd=stringData->heapStorage;forwardedArgumentCount=stringData->argumentsCount;
    memcpy(fileList,stringData->fileList,sizeof(fileList));memcpy(socketEndpoints,stringData->socketEndpoints,sizeof(socketEndpoints));memcpy(forwardedArgument,stringData->argumentArray,sizeof(forwardedArgument));memcpy(forwardedArgumentLength,stringData->arglen,sizeof(forwardedArgumentLength));
    for(unsigned ordinalIndex=0;ordinalIndex<userPageCount;ordinalIndex++)pageList[ordinalIndex]=(userBase+ordinalIndex*pageSize)|kernelPage;syncTables();
    memset((void *)userBase,0,userEnd-userBase);
    for(unsigned ordinalIndex=0;ordinalIndex<userPageCount;ordinalIndex++)if(stringData->permissionsList[ordinalIndex])memcpy((void *)(userBase+ordinalIndex*pageSize),(unsigned char *)snapshot(positionIndex)+ordinalIndex*pageSize,pageSize);
    memcpy(permissionsList,stringData->permissionsList,sizeof(permissionsList));
    for(unsigned ordinalIndex=0;ordinalIndex<userPageCount;ordinalIndex++){unsigned dataPosition=permissionsList[ordinalIndex];pageList[ordinalIndex]=dataPosition?(userBase+ordinalIndex*pageSize)|(dataPosition==3?userReadWrite:dataPosition==5?userReadExecute:userReadOnly):0;}
    syncTables();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");active=1;stringData->pausedState=0;startTimeout();
    userExecutionTime[ownerObject]=boardMillis();
    return (uint32_t)finishProgram(userResume(&stringData->executionFrame,stringData->floatingPointState));
}
static int runProgram(const unsigned char *data, size_t size, unsigned forwardedValue, int linuxMode, const char *name) {
    if (active) return -16;
    ownerObject=boardTerminal(11);if(ownerObject<0||ownerObject>3||saved[ownerObject].pausedState)return -16;interactive=0;
    int valid = validateElf(data, size, linuxMode); if (valid) return valid;
    linuxAbi = linuxMode;
    unsigned nameIndex=0;
    while (*name && nameIndex<31) userCommandName[ownerObject][nameIndex++]=(unsigned char)*name++;
    if (forwardedArgumentCount && forwardedArgumentLength[0]) {
        if (nameIndex) userCommandName[ownerObject][nameIndex++]=' ';
        for (unsigned positionIndex=0; positionIndex<forwardedArgumentLength[0]; positionIndex++) userCommandName[ownerObject][nameIndex++]=forwardedArgument[0][positionIndex];
    }
    userCommandName[ownerObject][nameIndex]=0; userNumber[ownerObject]=nextUserNumber++;
    if (nextUserNumber>0x7fffffffu) nextUserNumber=10;
    userStartTime[ownerObject]=boardMillis(); userAccumulatedTime[ownerObject]=0;
    for (unsigned ordinalIndex = 0; ordinalIndex < userPageCount; ordinalIndex++) pageList[ordinalIndex] = (userBase + ordinalIndex * pageSize) | kernelPage;
    syncTables();
    memset((void *)userBase, 0, userEnd - userBase);
    memset(permissionsList, 0, sizeof(permissionsList));
    elfHeader executableHeader; memcpy(&executableHeader, data, sizeof(executableHeader));
    for (unsigned ordinalIndex = 0; ordinalIndex < executableHeader.programHeaderCount; ordinalIndex++) {
        elfProgram dataPosition; memcpy(&dataPosition, data + executableHeader.programHeaderOffset + ordinalIndex * sizeof(dataPosition), sizeof(dataPosition));
        if (dataPosition.typeCategory != 1 || !dataPosition.memsz) continue;
        if (dataPosition.filesz) memcpy((void *)(uintptr_t)dataPosition.address, data + dataPosition.offsetValue, dataPosition.filesz);
        for (uintptr_t currentPosition = dataPosition.address & ~(pageSize - 1); currentPosition < dataPosition.address + dataPosition.memsz; currentPosition += pageSize) {
            permissionsList[(currentPosition - userBase) / pageSize] = (dataPosition.configurationBits & 2) ? 3 : ((dataPosition.configurationBits & 1) ? 5 : 1);
        }
    }
    for (uintptr_t currentPosition = userStackAddress; currentPosition < userEnd; currentPosition += pageSize) permissionsList[(currentPosition - userBase) / pageSize] = 3;
    uintptr_t initialStack = linuxMode ? linuxStartStack(executableHeader.entryPoint) : userEnd;
    for (unsigned ordinalIndex = 0; ordinalIndex < userPageCount; ordinalIndex++) {
        unsigned accessPermissions = permissionsList[ordinalIndex];
        pageList[ordinalIndex] = accessPermissions ? (userBase + ordinalIndex * pageSize) | (accessPermissions == 3 ? userReadWrite : accessPermissions == 5 ? userReadExecute : userReadOnly) : 0;
    }
    syncTables();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned ordinalIndex = 0; ordinalIndex < 16; ordinalIndex++) fileList[ordinalIndex] = -1;
    memset(socketEndpoints, 0, sizeof(socketEndpoints));
    heapEnd = userImageEnd;
    active = 1; startTimeout();
    userExecutionTime[ownerObject]=boardMillis();
    int result = userEnter(executableHeader.entryPoint, initialStack, forwardedValue);
    return finishProgram(result);
}
uintptr_t boardUserRun(uintptr_t lookupIndex) {
    if (lookupIndex >= sizeof(executableEntries) / sizeof(executableEntries[0])) return (uint32_t)-22;
    const char *name=lookupIndex==10?"javac":lookupIndex==11?"java":lookupIndex==12?"python":lookupIndex==13?"vi":lookupIndex==14?"jar":lookupIndex==15?"cc":lookupIndex==16?"jaot":"ELF";
    return (uint32_t)runProgram(executableEntries[lookupIndex].data, executableEntries[lookupIndex].size, executableEntries[lookupIndex].forwardedValue, 0, name);
}
static uintptr_t executeFile(int linuxMode) {
    static unsigned char image[16384];
    if (active || !forwardedArgumentCount) return (uint32_t)-22;
    int fileHandle = pk_open((const char *)forwardedArgument[0], readOnlyValue, 0);
    if (fileHandle < 0) return (uint32_t)-errorNumber;
    int size = pk_size(fileHandle);
    if (size < 0 || (unsigned)size > sizeof(image)) { pk_close(fileHandle); return (uint32_t)-27; }
    int receivedCount = pk_read(fileHandle, image, size); pk_close(fileHandle);
    if (receivedCount != size) return (uint32_t)-5;
    return (uint32_t)runProgram(image, size, 0, linuxMode, "");
}
uintptr_t boardUserFile(void) { return executeFile(0); }
uintptr_t boardUserLinuxFile(void) { return executeFile(1); }
uintptr_t boardUserValidate(void) {
    for (unsigned ordinalIndex = 0; ordinalIndex < sizeof(invalidExecutables) / sizeof(invalidExecutables[0]); ordinalIndex++)
        if (userValidateElf(invalidExecutables[ordinalIndex].data, invalidExecutables[ordinalIndex].size) != userExecutableError) return ordinalIndex + 1;
    return 0;
}
