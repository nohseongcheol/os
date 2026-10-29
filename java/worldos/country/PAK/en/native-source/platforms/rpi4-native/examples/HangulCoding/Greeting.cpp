#include "FileABI.h"
class DocumentManager {
    int index;
public:
    DocumentManager(const char *name) : index(openFile(name, ReadWrite | CreateIfMissing | TruncateContents, 0600)) {}
    ~DocumentManager() { if (index >= 0) closeFile(index); }
    ioResultType write(const char *data, byteCountType size) { return writeFileData(index, data, size); }
};
extern "C" int startUserProgram(int arguments) {
    (void)arguments;
    const char greeting[] = "C++에서 한글 클래스와 posix-kor invoke\n";
    DocumentManager guides("C++Greeting.txt");
    writeFileData(1, greeting, sizeof(greeting) - 1);
    return guides.write(greeting, sizeof(greeting) - 1) == sizeof(greeting) - 1 ? 0 : 1;
}
