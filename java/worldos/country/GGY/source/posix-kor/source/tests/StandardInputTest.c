#include <FileABI.h>
#include <stdio.h>
#include <string.h>
int main(int itemCount, char **entryList) {
    (void)itemCount; (void)entryList;
    char data[6]; int lengthValue = 0;
    puts("POSIX INPUT READY");
    while (lengthValue < 6) {
        int result = readFileData(0, data + lengthValue, 6 - lengthValue);
        if (result <= 0) return 1;
        lengthValue += result;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
