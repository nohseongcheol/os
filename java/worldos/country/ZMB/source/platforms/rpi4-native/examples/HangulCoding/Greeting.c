#include "FileABI.h"
int startUserProgram(int arguments) {
    (void)arguments;
    const char greeting[] = "C에서 한글 이름과 posix-kor invoke\n";
    int guides = openFile("C인사.txt", ReadWrite | CreateIfMissing | TruncateContents, 0600);
    if (guides < 0) return 1;
    ioResultType recordedCount = writeFileData(guides, greeting, sizeof(greeting) - 1);
    closeFile(guides);
    writeFileData(1, greeting, sizeof(greeting) - 1);
    return recordedCount == sizeof(greeting) - 1 ? 0 : 2;
}
