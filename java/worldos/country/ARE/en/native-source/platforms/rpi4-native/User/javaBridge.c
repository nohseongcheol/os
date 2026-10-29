#include "../naming/machineLinkNames.h"
// AOT 슬롯은 uintptr_t. Java 도구의 file/Output/인수는 buildAll EL0 SVC를 거친다.
#include "invoke.h"
#include "java-resources.h"
#include "Bundle.h"
typedef uintptr_t machineWord;
static int categoryValue;
static int jarActive, jarShift;
static machineWord forwardedArgument[8][257];
static unsigned pendingSurrogate;
extern int32_t javaEntry(void);
static intptr_t invoke(unsigned itemCount, machineWord firstValue, machineWord secondValue, machineWord characterCode) {
    return userInvoke(itemCount, firstValue, secondValue, characterCode, 0, 0, 0);
}
static void byteValues(const char *dataPosition, size_t itemCount) { invoke(1, 1, (machineWord)dataPosition, itemCount); }
static void character(unsigned characterCode) {
    unsigned char data[4]; unsigned itemCount = 0;
    if (characterCode < 128) data[itemCount++] = characterCode;
    else if (characterCode < 2048) { data[itemCount++] = 0xc0 | (characterCode >> 6); data[itemCount++] = 0x80 | (characterCode & 63); }
    else if (characterCode < 65536) { data[itemCount++] = 0xe0 | (characterCode >> 12); data[itemCount++] = 0x80 | ((characterCode >> 6) & 63); data[itemCount++] = 0x80 | (characterCode & 63); }
    else { data[itemCount++] = 0xf0 | (characterCode >> 18); data[itemCount++] = 0x80 | ((characterCode >> 12) & 63); data[itemCount++] = 0x80 | ((characterCode >> 6) & 63); data[itemCount++] = 0x80 | (characterCode & 63); }
    byteValues((const char *)data, itemCount);
}
machineWord toolCharacter(machineWord value) {
    unsigned characterCode = value;
    if (pendingSurrogate) {
        unsigned highPart = pendingSurrogate; pendingSurrogate = 0;
        if (characterCode >= 0xdc00 && characterCode <= 0xdfff) { character(0x10000 + ((highPart - 0xd800) << 10) + characterCode - 0xdc00); return 1; }
        character(0xfffd);
    }
    if (characterCode >= 0xd800 && characterCode <= 0xdbff) pendingSurrogate = characterCode;
    else character(characterCode > 0x10ffff || (characterCode >= 0xdc00 && characterCode <= 0xdfff) ? 0xfffd : characterCode);
    return 1;
}
machineWord toolPrint(machineWord value) {
    const machineWord *stringData = (const machineWord *)value;
    for (machineWord ordinalIndex = 0; ordinalIndex < stringData[0]; ordinalIndex++) toolCharacter(stringData[ordinalIndex + 1]);
    return stringData[0];
}
static int path(machineWord objectReference, char resultData[512]) {
    const machineWord *firstValue = (const machineWord *)objectReference;
    unsigned usedCapacity = 0;
    for (machineWord ordinalIndex = 1; ordinalIndex <= firstValue[0] && firstValue[ordinalIndex]; ordinalIndex++) {
        unsigned characterCode = firstValue[ordinalIndex];
        // UTF-16 -> UTF-8. 기존 도구의 char[] methodMode 경로와 호환한다.
        if (characterCode >= 0xd800 && characterCode <= 0xdbff && ordinalIndex < firstValue[0] && firstValue[ordinalIndex + 1] >= 0xdc00 && firstValue[ordinalIndex + 1] <= 0xdfff)
            { unsigned lowValue = firstValue[++ordinalIndex]; characterCode = 0x10000 + ((characterCode - 0xd800) << 10) + lowValue - 0xdc00; }
        else if (characterCode >= 0xd800 && characterCode <= 0xdfff) return -22;
        unsigned itemCount = characterCode < 128 ? 1 : characterCode < 2048 ? 2 : characterCode < 65536 ? 3 : 4;
        if (usedCapacity + itemCount > 511) return -36;
        if (itemCount == 1) resultData[usedCapacity++] = characterCode;
        else {
            resultData[usedCapacity++] = (itemCount == 2 ? 0xc0 : itemCount == 3 ? 0xe0 : 0xf0) | (characterCode >> (6 * (itemCount - 1)));
            for (unsigned innerOrdinal = itemCount - 1; innerOrdinal; innerOrdinal--) resultData[usedCapacity++] = 0x80 | ((characterCode >> (6 * (innerOrdinal - 1))) & 63);
        }
    }
    resultData[usedCapacity] = 0; return usedCapacity ? 0 : -22;
}
machineWord toolOpen(machineWord name, machineWord configurationBits) {
    char dataPosition[512]; int error = path(name, dataPosition);
    return (uint32_t)(error ? error : invoke(3, (machineWord)dataPosition, configurationBits, 0));
}
machineWord toolClose(machineWord fileHandle) { return (uint32_t)invoke(4, fileHandle, 0, 0); }
machineWord toolReadByte(machineWord fileHandle) {
    unsigned char secondValue; intptr_t itemCount = invoke(2, fileHandle, (machineWord)&secondValue, 1);
    return (uint32_t)(itemCount == 1 ? secondValue : itemCount == 0 ? 256 : itemCount);
}
machineWord toolWriteByte(machineWord fileHandle, machineWord value) {
    unsigned char secondValue = value; return (uint32_t)invoke(1, fileHandle, (machineWord)&secondValue, 1);
}
machineWord toolRead(machineWord name, machineWord destinationDataAddress) {
    if (jarActive) {
        char dataPosition[512]; int error = path(name, dataPosition); if (error) return (uint32_t)error;
        unsigned itemCount = 0; while (dataPosition[itemCount]) itemCount++;
        if (itemCount >= 6) for (unsigned ordinalIndex = 0; ordinalIndex < itemCount - 6; ordinalIndex++) if (dataPosition[ordinalIndex] == '.') dataPosition[ordinalIndex] = '/';
        unsigned char byteValues[16384]; machineWord *destinationValuePosition = (machineWord *)destinationDataAddress;
        int receivedCount = jarRead(dataPosition, byteValues, destinationValuePosition[0] < sizeof(byteValues) ? destinationValuePosition[0] : sizeof(byteValues));
        if (receivedCount >= 0) { for (int ordinalIndex = 0; ordinalIndex < receivedCount; ordinalIndex++) destinationValuePosition[ordinalIndex + 1] = byteValues[ordinalIndex]; return receivedCount; }
        if (receivedCount != -2) return (uint32_t)receivedCount;
    }
    int fileHandle = jarActive ? -2 : (int32_t)toolOpen(name, 0);
    if (fileHandle < 0) {
        char dataPosition[512]; int error = path(name, dataPosition); if (error) return (uint32_t)error;
        for (unsigned ordinalIndex = 0; ordinalIndex < sizeof(javaClassList) / sizeof(javaClassList[0]); ordinalIndex++) {
            const char *nextOffset = javaClassList[ordinalIndex].name; unsigned innerOrdinal = 0;
            while (dataPosition[innerOrdinal] && dataPosition[innerOrdinal] == nextOffset[innerOrdinal]) innerOrdinal++;
            if (dataPosition[innerOrdinal] || nextOffset[innerOrdinal]) continue;
            machineWord *destinationValuePosition = (machineWord *)destinationDataAddress;
            if (destinationValuePosition[0] < javaClassList[ordinalIndex].size) return (uint32_t)-27;
            for (innerOrdinal = 0; innerOrdinal < javaClassList[ordinalIndex].size; innerOrdinal++) destinationValuePosition[innerOrdinal + 1] = javaClassList[ordinalIndex].data[innerOrdinal];
            return javaClassList[ordinalIndex].size;
        }
        return (uint32_t)fileHandle;
    }
    machineWord *firstValue = (machineWord *)destinationDataAddress;
    intptr_t size = invoke(9, fileHandle, 0, 0), completedAmount = 0;
    if (size < 0 || (machineWord)size > firstValue[0]) { toolClose(fileHandle); return (uint32_t)(size < 0 ? size : -27); }
    unsigned char dataBlock[256];
    while (completedAmount < size) {
        intptr_t itemCount = invoke(2, fileHandle, (machineWord)dataBlock, size - completedAmount < 256 ? size - completedAmount : 256);
        if (itemCount <= 0) { toolClose(fileHandle); return (uint32_t)(itemCount ? itemCount : -5); }
        for (intptr_t ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) firstValue[1 + completedAmount + ordinalIndex] = dataBlock[ordinalIndex];
        completedAmount += itemCount;
    }
    toolClose(fileHandle); return completedAmount;
}
machineWord toolWrite(machineWord name, machineWord originalData, machineWord entryCount) {
    const machineWord *firstValue = (const machineWord *)originalData;
    if (entryCount > firstValue[0] || entryCount > 16384) return (uint32_t)-27;
    int fileHandle = (int32_t)toolOpen(name, 577); if (fileHandle < 0) return (uint32_t)fileHandle;
    unsigned char dataBlock[256]; machineWord completedAmount = 0;
    while (completedAmount < entryCount) {
        machineWord itemCount = entryCount - completedAmount < 256 ? entryCount - completedAmount : 256;
        for (machineWord ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) dataBlock[ordinalIndex] = firstValue[1 + completedAmount + ordinalIndex];
        intptr_t result = invoke(1, fileHandle, (machineWord)dataBlock, itemCount);
        if (result <= 0) { toolClose(fileHandle); return (uint32_t)(result ? result : -5); }
        completedAmount += result;
    }
    toolClose(fileHandle); return entryCount;
}
machineWord toolArgc(void) { return invoke(15, UINTPTR_MAX, 0, 0) - (jarActive ? jarShift : 0); }
machineWord toolArgument(machineWord lookupIndex) {
    static const machineWord emptyValue[1] = {0};
    if (lookupIndex >= 8) return (machineWord)emptyValue;
    unsigned char input[256]; intptr_t itemCount;
    if (jarActive && lookupIndex == 0) { const char *dataPosition = jarMain(); itemCount = 0; while (dataPosition[itemCount] && itemCount < 255) { input[itemCount] = dataPosition[itemCount]; itemCount++; } }
    else itemCount = invoke(15, lookupIndex + (jarActive ? jarShift : 0), (machineWord)input, sizeof(input));
    if (itemCount < 0) return (machineWord)emptyValue;
    machineWord *resultData = forwardedArgument[lookupIndex]; unsigned entryCount = 0;
    for (intptr_t ordinalIndex = 0; ordinalIndex < itemCount;) {
        unsigned characterCode = input[ordinalIndex++], hasMore = characterCode < 128 ? 0 : characterCode >= 0xc2 && characterCode < 0xe0 ? 1 : characterCode < 0xf0 && characterCode >= 0xe0 ? 2 : characterCode >= 0xf0 && characterCode <= 0xf4 ? 3 : 4;
        if (hasMore == 4 || ordinalIndex + hasMore > itemCount) { resultData[++entryCount] = 0xfffd; continue; }
        unsigned minimumData = hasMore == 1 ? 128 : hasMore == 2 ? 2048 : hasMore == 3 ? 65536 : 0;
        if (hasMore) characterCode &= (1u << (6 - hasMore)) - 1;
        unsigned innerOrdinal = 0;
        while (innerOrdinal < hasMore && (input[ordinalIndex] & 0xc0) == 0x80) { characterCode = (characterCode << 6) | (input[ordinalIndex++] & 63); innerOrdinal++; }
        if (innerOrdinal != hasMore || characterCode < minimumData || characterCode > 0x10ffff || (characterCode >= 0xd800 && characterCode <= 0xdfff)) characterCode = 0xfffd;
        if (characterCode >= 65536) { characterCode -= 65536; resultData[++entryCount] = 0xd800 | (characterCode >> 10); resultData[++entryCount] = 0xdc00 | (characterCode & 1023); }
        else resultData[++entryCount] = characterCode;
    }
    resultData[0] = entryCount; return (machineWord)resultData;
}
machineWord toolKind(void) { return categoryValue; }
void kernelPanic(const char *noticeText) {
    const char *dataPosition = noticeText; while (*dataPosition) dataPosition++;
    byteValues("Java tool runtime error: ", 25); byteValues(noticeText, dataPosition - noticeText); character(10);
    invoke(6, 1, 0, 0); for (;;) {}
}
int startUserProgram(int methodMode) {
    categoryValue = methodMode;
    unsigned char firstEntry[256]; intptr_t itemCount = invoke(15, 0, (machineWord)firstEntry, sizeof(firstEntry));
    if (methodMode == 2 || (methodMode == 1 && itemCount == 4 && firstEntry[0] == '-' && firstEntry[1] == 'j' && firstEntry[2] == 'a' && firstEntry[3] == 'r')) {
        jarShift = methodMode == 2 ? 0 : 1;
        char fileEntryName[256]; intptr_t lengthData = invoke(15, jarShift, (machineWord)fileEntryName, sizeof(fileEntryName));
        if (lengthData <= 0 || jarOpen(fileEntryName) < 0) {
            static const char error[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            byteValues(error, sizeof(error) - 1); return 1;
        }
        jarActive = 1;
    }
    int result = javaEntry();
    if (pendingSurrogate) character(0xfffd);
    return result;
}

// UDP는 Native 커널의 SVC를 통과하며 currentItem 127.0.0.1만 제공한다.
struct javaAddress { uint16_t family, portNumber; uint32_t address; unsigned char zeroValue[8]; };
static struct javaAddress udpAddress(unsigned portNumber) {
    struct javaAddress firstValue = {2, (uint16_t)((portNumber << 8) | (portNumber >> 8)), 0x0100007f, {0}}; return firstValue;
}
machineWord toolUdpOpen(machineWord portNumber) {
    intptr_t fileHandle = invoke(32, 2, 2, 17); if (fileHandle < 0) return (uint32_t)fileHandle;
    struct javaAddress firstValue = udpAddress(portNumber);
    firstValue.address = 0;
    intptr_t stateValue = invoke(33, fileHandle, (machineWord)&firstValue, sizeof(firstValue));
    if (stateValue < 0) { toolClose(fileHandle); return (uint32_t)stateValue; }
    return fileHandle;
}
machineWord toolUdpSend(machineWord fileHandle, machineWord portNumber, machineWord arrayValue, machineWord lengthValue) {
    const machineWord *originalAddress = (const machineWord *)arrayValue; unsigned char data[512];
    if (lengthValue > 512 || lengthValue > originalAddress[0]) return (uint32_t)-90;
    for (machineWord ordinalIndex = 0; ordinalIndex < lengthValue; ordinalIndex++) data[ordinalIndex] = originalAddress[ordinalIndex + 1];
    struct javaAddress firstValue = udpAddress(portNumber);
    return (uint32_t)userInvoke(34, fileHandle, (machineWord)data, lengthValue, 0, (machineWord)&firstValue, sizeof(firstValue));
}
static uint32_t reverseByteOrder(uint32_t itemCount) { return (itemCount>>24)|((itemCount>>8)&0xff00)|((itemCount<<8)&0xff0000)|(itemCount<<24); }
machineWord toolUdpSendAddress(machineWord fileHandle, machineWord address, machineWord portNumber, machineWord arrayValue, machineWord lengthValue) {
    const machineWord *originalAddress = (const machineWord *)arrayValue; unsigned char data[512];
    if (lengthValue > 512 || lengthValue > originalAddress[0]) return (uint32_t)-90;
    for (machineWord ordinalIndex = 0; ordinalIndex < lengthValue; ordinalIndex++) data[ordinalIndex] = originalAddress[ordinalIndex + 1];
    struct javaAddress firstValue = udpAddress(portNumber); firstValue.address = reverseByteOrder(address);
    return (uint32_t)userInvoke(34, fileHandle, (machineWord)data, lengthValue, 0, (machineWord)&firstValue, sizeof(firstValue));
}
machineWord toolConnect(machineWord fileHandle, machineWord address, machineWord portNumber) {
    struct javaAddress firstValue = udpAddress(portNumber); firstValue.address = reverseByteOrder(address);
    uint32_t run = invoke(7, 0, 0, 0);
    for (;;) {
        intptr_t result = invoke(37, fileHandle, (machineWord)&firstValue, sizeof(firstValue));
        if (result != -115) return (uint32_t)result;
        if ((uint32_t)(invoke(7, 0, 0, 0) - run) >= 1000) return (uint32_t)-110;
    }
}
machineWord toolUdpRecv(machineWord fileHandle, machineWord arrayValue, machineWord bufferCapacity) {
    machineWord *destinationAddress = (machineWord *)arrayValue; unsigned char data[512];
    if (bufferCapacity > 512 || destinationAddress[0] < 514) return (uint32_t)-90;
    struct javaAddress firstValue; unsigned lengthData = sizeof(firstValue);
    intptr_t itemCount = userInvoke(35, fileHandle, (machineWord)data, bufferCapacity, 0, (machineWord)&firstValue, (machineWord)&lengthData);
    if (itemCount >= 0) { for (intptr_t ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) destinationAddress[ordinalIndex + 1] = data[ordinalIndex]; destinationAddress[513] = (firstValue.portNumber << 8 | firstValue.portNumber >> 8) & 65535; destinationAddress[514] = reverseByteOrder(firstValue.address); }
    return (uint32_t)itemCount;
}
machineWord toolUdpPort(machineWord fileHandle) {
    struct javaAddress firstValue; unsigned lengthData = sizeof(firstValue);
    intptr_t returnedValue = invoke(36, fileHandle, (machineWord)&firstValue, (machineWord)&lengthData);
    return (uint32_t)(returnedValue < 0 ? returnedValue : (firstValue.portNumber << 8 | firstValue.portNumber >> 8) & 65535);
}
machineWord toolMillis(void) { return (uint32_t)invoke(7, 0, 0, 0); }
machineWord toolScreenWidth(void) { return (uint32_t)readScreenWidth(); }
machineWord toolScreenHeight(void) { return (uint32_t)readScreenHeight(); }
machineWord toolGraphicsWait(void) { return (uint32_t)waitForScreenKey(); }
machineWord toolRectangle(machineWord xCoordinate, machineWord yCoordinate, machineWord requestedWidthValue, machineWord requestedHeightValue, machineWord pixelColour) {
    return (uint32_t)userInvoke(13, xCoordinate, yCoordinate, pixelColour, requestedWidthValue, requestedHeightValue, 0);
}

machineWord toolStream(machineWord action,machineWord fileHandle,machineWord value){
    if(action==0)return (uint32_t)invoke(32,2,1,6);
    struct javaAddress firstValue=udpAddress(value);
    if(action==1){firstValue.address=0;intptr_t returnedValue=invoke(33,fileHandle,(machineWord)&firstValue,sizeof(firstValue));return (uint32_t)(returnedValue<0?returnedValue:invoke(38,fileHandle,4,0));}
    if(action==2)return (uint32_t)invoke(37,fileHandle,(machineWord)&firstValue,sizeof(firstValue));
    if(action==3)return (uint32_t)invoke(39,fileHandle,0,0);
    if(action==4)return toolUdpPort(fileHandle);
    if(action==5)return (uint32_t)invoke(40,fileHandle,0,0);
    return (uint32_t)-22;
}
machineWord toolGui(machineWord action,machineWord identifierValue,machineWord firstValue,machineWord secondValue,machineWord characterCode,machineWord destinationData){return (uint32_t)userInvoke(20,action,identifierValue,firstValue,secondValue,characterCode,destinationData);}
machineWord toolGuiText(machineWord identifierValue,machineWord arrayValue,machineWord itemCount){
    const machineWord *originalAddress=(const machineWord *)arrayValue;uint32_t data[127];unsigned entryCount=0;
    if(itemCount>originalAddress[0])return (uint32_t)-22;
    for(machineWord ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++){unsigned characterEncoding=originalAddress[ordinalIndex+1];if(characterEncoding>=0xd800&&characterEncoding<=0xdbff&&ordinalIndex+1<itemCount){unsigned lowValue=originalAddress[++ordinalIndex+1];if(lowValue<0xdc00||lowValue>0xdfff)return (uint32_t)-22;characterEncoding=0x10000+((characterEncoding-0xd800)<<10)+lowValue-0xdc00;}if(entryCount==127)return (uint32_t)-22;data[entryCount++]=characterEncoding;}
    return (uint32_t)userInvoke(21,identifierValue,(machineWord)data,entryCount,0,0,0);
}
