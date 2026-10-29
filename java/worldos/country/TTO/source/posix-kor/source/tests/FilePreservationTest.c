#include <FileABI.h>
#include <stdio.h>
int main(int itemCount, char **entryList) {
    (void)itemCount; (void)entryList;
    int file = openFile("stored.txt", ReadWrite | CreateIfMissing | TruncateContents, 0600);
    if (file < 0 || writeFileData(file, "saved-from-C", 12) != 12) return 1;
    if (commitFileStorage(file) < 0) return 2;
    if (closeFile(file) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
