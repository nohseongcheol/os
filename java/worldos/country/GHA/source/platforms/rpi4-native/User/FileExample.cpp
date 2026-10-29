#include "FileABI.h"
#include "invoke.h"
static int initializerValue;
static volatile int initializerSeed = 72;
static volatile double floatingPointSeed = 1.25;
static int destructionCount;
struct testInitialization { testInitialization() { initializerValue = initializerSeed + 1; } } initializeStatics;
class automaticFile {
    int index;
public:
    explicit automaticFile(const char *name) : index(openFile(name, ReadWrite | CreateIfMissing | TruncateContents, 0600)) {}
    ~automaticFile() { if (index >= 0) closeFile(index); destructionCount++; }
    int descriptorEntry() const { return index; }
};
extern "C" int startUserProgram(int) {
    if (initializerValue != 73 || userInvoke(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double floatingPointValue = floatingPointSeed * 2.0 + 0.5;
    if (userInvoke(0, 0, 0, 0, 0, 0, 0) != 1 || floatingPointValue != 3.0) return 16;
    static const char contentValue[] = "EL0 C++ → posix-kor → Java file · 안녕하세요 😀\n";
    char readValue[sizeof(contentValue)] = {};
    {
        automaticFile file("User.txt");
        int index = file.descriptorEntry();
        if (index < 0 || writeFileData(index, contentValue, sizeof(contentValue)) != sizeof(contentValue)) return 2;
        if (seekFile(index, 0, FromBeginning) || readFileData(index, readValue, sizeof(readValue)) != sizeof(readValue)) return 3;
        for (unsigned ordinalIndex = 0; ordinalIndex < sizeof(contentValue); ordinalIndex++) if (readValue[ordinalIndex] != contentValue[ordinalIndex]) return 4;
    }
    if (destructionCount != 1) return 5;
    if (writeFileData(1, contentValue, sizeof(contentValue) - 1) != sizeof(contentValue) - 1) return 6;
    uintptr_t bottomEntry = userMemoryEnd(0);
    if (bottomEntry != 0x02c00000 || userMemoryEnd(bottomEntry + 8192) != (intptr_t)(bottomEntry + 8192)) return 7;
    volatile unsigned char *memoryValue = (volatile unsigned char *)bottomEntry;
    if (memoryValue[0] || memoryValue[8191]) return 8;
    memoryValue[8191] = 137;
    if (userMemoryEnd(bottomEntry) != (intptr_t)bottomEntry || userMemoryEnd(bottomEntry + 8192) != (intptr_t)(bottomEntry + 8192) || memoryValue[8191]) return 9;
    // 잘못된 User pointer/번호는 오류이며 커널을 중단하지 않는다.
    if (writeFileData(1, (const void *)0x80000, 8) != -1 || errorNumber != 14) return 10;
    if (readFileData(0, (void *)contentValue, 1) != -1 || errorNumber != 14) return 11;
    if (userInvoke(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t screenSpan = readScreenWidth(), screenLength = readScreenHeight();
    if (screenSpan <= 0 || screenLength <= 0 || userInvoke(13, screenSpan-1, screenLength-1, 0, 2, 2, 0) != -22) return 13;
    if (screenRectangle(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 exitProgram 시 열린 서술자가 자동 정리되어야 한다.
    if (openFile("User.txt", readOnlyValue) < 0) return 15;
    return 0;
}
