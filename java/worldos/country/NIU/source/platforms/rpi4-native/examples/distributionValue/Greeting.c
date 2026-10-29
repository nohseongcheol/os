#include <FileABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int argumentsCount, char **argumentList) {
    if (argumentsCount < 1 || !argumentList[0]) return 2;
    const char greeting[] = "Native 커널의 C와 English POSIX\n";
    int guides = openFile("Greeting.txt", ReadWrite | CreateIfMissing | TruncateContents, 0600);
    if (guides < 0) return 1;
    ioResultType lengthValue = writeFileData(guides, greeting, sizeof(greeting) - 1);
    closeFile(guides);
    writeFileData(1, greeting, sizeof(greeting) - 1);
    return lengthValue == sizeof(greeting) - 1 ? 0 : 3;
}
