#include "../naming/machineLinkNames.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "networkStack.h"
#include "string.h"
#include "FileABI.h"
extern uintptr_t boardMillis(void);
extern int32_t jfsEntryLength(int32_t), jfsEntryByte(int32_t,int32_t), jfsEntrySize(int32_t);
extern int32_t jfsEntryCount(void);
static int receivePort = -1, control = -1, manualConnection = -1, data = -1;
static unsigned isLoggedIn, userOk, lineSize, lineBad, quitProgram, executingTask, usedCapacity, sentCount, hasFailed;
static unsigned replySize, replySent, nextPortNumber;
static uint32_t activity;
static char line[256], replies[2048], fileEntryName[64], transferName[64];
static unsigned char transferState[16384];
static int equal(const char *firstValue, const char *secondValue) { while (*firstValue && *firstValue == *secondValue) { firstValue++; secondValue++; } return *firstValue == *secondValue; }
static void reply(const char *stringData) {
    size_t itemCount = strlen(stringData);
    if (replySent) { memmove(replies, replies + replySent, replySize - replySent); replySize -= replySent; replySent = 0; }
    if (itemCount > sizeof(replies) - replySize) { quitProgram = 1; return; }
    memcpy(replies + replySize, stringData, itemCount); replySize += itemCount;
}
static void numericValue(unsigned value, char *resultData, unsigned *itemCount) {
    char digitCount[10]; unsigned entryCount = 0;
    do { digitCount[entryCount++] = '0' + value % 10; value /= 10; } while (value);
    while (entryCount) resultData[(*itemCount)++] = digitCount[--entryCount];
}
static void stopTransfer(void) {
    if (data >= 0) closeNetwork(data); if (manualConnection >= 0) closeNetwork(manualConnection);
    data = manualConnection = -1; executingTask = usedCapacity = sentCount = hasFailed = 0;
}
static void disconnect(void) {
    stopTransfer(); if (control >= 0) closeNetwork(control); control = -1;
    isLoggedIn = userOk = lineSize = lineBad = replySize = replySent = quitProgram = 0;
}
int fileTransferControl(int action) {
    if (action == 2) return receivePort >= 0;
    if (action == 0) { disconnect(); if (receivePort >= 0) closeNetwork(receivePort); receivePort = -1; return 0; }
    if (action != 1) return -22; if (receivePort >= 0) return 0;
    receivePort = createSocketEndpoint(1); if (receivePort < 0) return receivePort;
    int returnedValue = netBind(receivePort, readNetworkStatus(0,0), 21); if (!returnedValue) returnedValue = netListen(receivePort);
    if (returnedValue < 0) { closeNetwork(receivePort); receivePort = -1; } return returnedValue;
}
static int path(const char *name) {
    unsigned itemCount = 0; if (*name == '/') name++;
    if (!*name || equal(name, ".") || equal(name, "..")) return 0;
    fileEntryName[itemCount++] = '/';
    while (*name) {
        unsigned char characterCode = *name++;
        if (itemCount >= 63 || characterCode < 32 || characterCode == 127 || characterCode == '/' || characterCode == '\\') return 0;
        fileEntryName[itemCount++] = characterCode;
    }
    fileEntryName[itemCount] = 0; return 1;
}
static void sendList(int detail) {
    usedCapacity = sentCount = 0;
    for (int ordinalIndex = 0; ordinalIndex < jfsEntryCount(); ordinalIndex++) {
        int itemCount = jfsEntryLength(ordinalIndex); if (itemCount <= 0) continue;
        const char *leadingPart = detail == 2 ? "type=file;size=" : detail == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned entryCount = strlen(leadingPart); memcpy(transferState + usedCapacity, leadingPart, entryCount); usedCapacity += entryCount;
        if (detail) numericValue(jfsEntrySize(ordinalIndex), (char *)transferState, &usedCapacity);
        const char *suffixValue = detail == 2 ? "; " : detail == 1 ? " Jan 01 00:00 " : "";
        entryCount = strlen(suffixValue); memcpy(transferState + usedCapacity, suffixValue, entryCount); usedCapacity += entryCount;
        for (int innerOrdinal = 0; innerOrdinal < itemCount; innerOrdinal++) transferState[usedCapacity++] = jfsEntryByte(ordinalIndex,innerOrdinal);
        transferState[usedCapacity++] = '\r'; transferState[usedCapacity++] = '\n';
    }
}
static void prepareManualConnection(int extended) {
    if (executingTask) { reply("450 Transfer in progress\r\n"); return; }
    stopTransfer(); manualConnection = createSocketEndpoint(1);
    if (manualConnection >= 0) reuseSocketAddress(manualConnection);
    unsigned portNumber = 50000 + nextPortNumber++ % 8;
    if (manualConnection < 0 || netBind(manualConnection, readNetworkStatus(0,0), portNumber) || netListen(manualConnection)) {
        stopTransfer(); reply("425 Cannot open passive listener\r\n"); return;
    }
    char response[96]; const char *leadingPart = extended ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned itemCount = strlen(leadingPart); memcpy(response, leadingPart, itemCount);
    if (extended) { numericValue(portNumber, response, &itemCount); response[itemCount++] = '|'; }
    else {
        uint32_t address=readNetworkStatus(0,0);
        for (int positionIndex=24;positionIndex>=0;positionIndex-=8) { numericValue((address>>positionIndex)&255,response,&itemCount);response[itemCount++]=','; }
        numericValue(portNumber / 256, response, &itemCount); response[itemCount++] = ','; numericValue(portNumber % 256, response, &itemCount);
    }
    response[itemCount++] = ')'; response[itemCount++] = '\r'; response[itemCount++] = '\n'; response[itemCount] = 0; reply(response);
}
static void command(void) {
    line[lineSize] = 0;
    char *additionalArguments = line; while (*additionalArguments && *additionalArguments != ' ') { if (*additionalArguments >= 'a' && *additionalArguments <= 'z') *additionalArguments -= 32; additionalArguments++; }
    if (*additionalArguments) *additionalArguments++ = 0; while (*additionalArguments == ' ') additionalArguments++;
    if (equal(line, "QUIT")) { stopTransfer(); reply("221 Goodbye\r\n"); quitProgram = 1; return; }
    if (equal(line, "NOOP")) { reply("200 OK\r\n"); return; }
    if (equal(line, "SYST")) { reply("215 UNIX Type: L8\r\n"); return; }
    if (equal(line, "FEAT")) { reply("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (equal(line, "USER")) { isLoggedIn = 0; userOk = equal(additionalArguments, "anonymous") || equal(additionalArguments, "jkoros"); reply(userOk ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (equal(line, "PASS")) { isLoggedIn = userOk; reply(isLoggedIn ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!isLoggedIn) { reply("530 Login first\r\n"); return; }
    if (equal(line, "PWD")) reply("257 \"/\"\r\n");
    else if (equal(line, "CWD")) reply(equal(additionalArguments, "/") || equal(additionalArguments, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (equal(line, "TYPE")) reply(equal(additionalArguments, "I") || equal(additionalArguments, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (equal(line, "OPTS")) reply(equal(additionalArguments, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (equal(line, "PASV")) prepareManualConnection(0);
    else if (equal(line, "EPSV")) { if (*additionalArguments && !equal(additionalArguments, "1")) reply("522 IPv4 only\r\n"); else prepareManualConnection(1); }
    else if (equal(line, "ABOR")) { stopTransfer(); reply("226 Transfer aborted\r\n"); }
    else if (equal(line, "DELE")) { reply(path(additionalArguments) && pk_unlink(fileEntryName) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (equal(line, "LIST") || equal(line, "NLST") || equal(line, "MLSD")) {
        if (executingTask) { reply("450 Transfer in progress\r\n"); return; }
        if (manualConnection < 0 && data < 0) { reply("425 Use PASV or EPSV\r\n"); return; }
        if (*additionalArguments && !equal(additionalArguments,"/") && !equal(additionalArguments,".") && !equal(additionalArguments,"-a") && !equal(additionalArguments,"-l") && !equal(additionalArguments,"-la")) { reply("550 Root listing only\r\n"); return; }
        sendList(equal(line,"MLSD") ? 2 : equal(line,"LIST") ? 1 : 0); executingTask = 2;
        reply("150 Opening directory listing\r\n");
    }
    else if (equal(line, "SIZE")) {
        if (!path(additionalArguments)) { reply("550 Invalid filename\r\n"); return; }
        int fileHandle = pk_open(fileEntryName, readOnlyValue, 0); if (fileHandle < 0) { reply("550 File unavailable\r\n"); return; }
        int size = pk_size(fileHandle); pk_close(fileHandle); char response[32] = "213 "; unsigned itemCount = 4;
        numericValue(size, response, &itemCount); response[itemCount++] = '\r'; response[itemCount++] = '\n'; response[itemCount] = 0; reply(response);
    } else if (equal(line, "STOR") || equal(line, "RETR")) {
        if (executingTask) { reply("450 Transfer in progress\r\n"); return; }
        if (manualConnection < 0 && data < 0) { reply("425 Use PASV or EPSV\r\n"); return; }
        if (!path(additionalArguments)) { reply("550 Invalid filename\r\n"); return; }
        executingTask = equal(line, "STOR") ? 1 : 2; usedCapacity = sentCount = hasFailed = 0;
        memcpy(transferName, fileEntryName, strlen(fileEntryName) + 1);
        if (executingTask == 2) {
            int fileHandle = pk_open(fileEntryName, readOnlyValue, 0);
            if (fileHandle < 0) { executingTask = 0; reply("550 File unavailable\r\n"); return; }
            int itemCount = pk_read(fileHandle, transferState, sizeof(transferState)); pk_close(fileHandle);
            if (itemCount < 0) { executingTask = 0; reply("451 Read failed\r\n"); return; } usedCapacity = itemCount;
        }
        reply("150 Opening binary data connection\r\n");
    } else reply("502 Command not implemented\r\n");
}
void inspectFileTransfer(void) {
    if (receivePort < 0) return;
    int incomingConnection = netAccept(receivePort);
    if (incomingConnection >= 0) {
        if (control >= 0) { netWrite(incomingConnection, "421 One session at a time\r\n", 27); closeNetwork(incomingConnection); }
        else { control = incomingConnection; activity = boardMillis(); reply("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (control < 0) return;
    if ((uint32_t)(boardMillis() - activity) > 60000) { disconnect(); return; }
    if (!quitProgram) for (unsigned budget = 0; budget < 256; budget++) {
        unsigned char characterCode; int returnedValue = netRead(control, &characterCode, 1);
        if (returnedValue == -11) break; if (returnedValue <= 0) { disconnect(); return; } activity = boardMillis();
        if (characterCode == '\n') { if (lineBad) reply("500 Command too long or invalid\r\n"); else command(); lineSize = lineBad = 0; if (quitProgram) break; }
        else if (characterCode != '\r') { if (!characterCode || lineSize >= sizeof(line) - 1) lineBad = 1; else line[lineSize++] = characterCode; }
    }
    if (manualConnection >= 0 && data < 0) {
        int returnedValue = netAccept(manualConnection);
        if (returnedValue >= 0) {
            if (netPeerAddress(returnedValue) != netPeerAddress(control)) closeNetwork(returnedValue);
            else { data = returnedValue; closeNetwork(manualConnection); manualConnection = -1; activity = boardMillis(); }
        }
    }
    if (executingTask == 1 && data >= 0) for (unsigned budget = 0; budget < 8; budget++) {
        unsigned char dataBlock[512]; int itemCount = netRead(data, dataBlock, sizeof(dataBlock));
        if (itemCount == -11) break;
        if (itemCount < 0) { stopTransfer(); reply("426 Data connection failed\r\n"); break; }
        activity = boardMillis();
        if (itemCount == 0) {
            int result = -1;
            if (!hasFailed) {
                int fileHandle = pk_open(transferName, writeOnlyValue | CreateIfMissing | TruncateContents, 0600);
                if (fileHandle >= 0) { result = pk_write(fileHandle, transferState, usedCapacity); pk_close(fileHandle); }
            }
            int isSuccessful = !hasFailed && result == (int)usedCapacity; stopTransfer(); reply(isSuccessful ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)itemCount > sizeof(transferState) - usedCapacity) hasFailed = 1;
        if (!hasFailed) { memcpy(transferState + usedCapacity, dataBlock, itemCount); usedCapacity += itemCount; }
    }
    if (executingTask == 2 && data >= 0) {
        int itemCount = netWrite(data, transferState + sentCount, usedCapacity - sentCount);
        if (itemCount >= 0) { sentCount += itemCount; activity = boardMillis(); if (sentCount == usedCapacity) { stopTransfer(); reply("226 Transfer complete\r\n"); } }
        else if (itemCount != -11) { stopTransfer(); reply("426 Data connection failed\r\n"); }
    }
    if (replySent < replySize) {
        int itemCount = netWrite(control, replies + replySent, replySize - replySent);
        if (itemCount > 0) replySent += itemCount; else if (itemCount != -11) { disconnect(); return; }
    }
    if (replySent == replySize) { replySize = replySent = 0; if (quitProgram) disconnect(); }
}
