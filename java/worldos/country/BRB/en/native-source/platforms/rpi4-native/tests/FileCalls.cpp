#include "../naming/machineLinkNames.h"
#include "FileABI.h"
// 표준 C++ library 없는 freestanding C++11 Program. 커널에 staticValue 링크한다.
extern "C" uintptr_t testCppPrograms(void) {
    const char contentValue[] = "C++ → Java kernelValue · 한글 😀";
    unsigned char readValue[sizeof(contentValue)] = {};
    int file = openFile("tests.txt", ReadWrite | CreateIfMissing | TruncateContents, 0600);
    if (file < 0) return 1;
    if (writeFileData(file, contentValue, sizeof(contentValue)) != sizeof(contentValue)) return 2;
    if (seekFile(file, 0, FromBeginning) != 0) return 3;
    if (readFileData(file, readValue, sizeof(readValue)) != sizeof(readValue)) return 4;
    for (size_t ordinalIndex = 0; ordinalIndex < sizeof(contentValue); ordinalIndex++) if (readValue[ordinalIndex] != (unsigned char)contentValue[ordinalIndex]) return 5;
    if (readFileData(file, readValue, 1) != 0) return 6;
    if (commitFileStorage(file) != -1 || errorNumber != 38) return 7;
    if (closeFile(file) || closeFile(file) != -1 || errorNumber != 9) return 8;
    file = openFile("tests.txt", readOnlyValue);
    if (file < 0 || writeFileData(file, contentValue, 1) != -1 || errorNumber != 9) return 9;
    if (closeFile(file)) return 10;
    file = openFile("tests.txt", ReadWrite | appendAtEnd);
    if (file < 0 || seekFile(file, 0, FromBeginning) != 0 || writeFileData(file, "!", 1) != 1 || fileSize(file) != sizeof(contentValue) + 1) return 11;
    if (setFileLength(file, 2) || seekFile(file, 4, FromBeginning) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (writeFileData(file, "x", 1) != 1 || fileSize(file) != 3 || closeFile(file)) return 13;
    file = openFile("구멍.bin", ReadWrite | CreateIfMissing | TruncateContents, 0600);
    if (file < 0 || seekFile(file, 3, FromBeginning) != 3 || writeFileData(file, "z", 1) != 1) return 14;
    if (seekFile(file, 0, FromBeginning) != 0 || readFileData(file, readValue, 4) != 4 || readValue[0] || readValue[1] || readValue[2] || readValue[3] != 'z') return 15;
    if (removeFileEntryName("구멍.bin") || fileSize(file) != 4 || closeFile(file)) return 16;
    if (openFile("구멍.bin", readOnlyValue) != -1 || errorNumber != 2) return 17;
    if (openFile("tests.txt", ReadWrite | createNewFile, 0600) != -1 || errorNumber != 17) return 18;
    if (openFile("../prohibitedValue", readOnlyValue) != -1) return 19;
    return 0;
}
