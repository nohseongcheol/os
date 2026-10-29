#include <FileABI.h>
#include <NetworkABI.h>
#include <string.h>
#include <stdio.h>

static int checkedItemCount;
static void Checks(int condition, int line) {
    checkedItemCount++;
    if (!condition) {
        puts("POSIX CHECK FAILED");
        char digitValue[12]; int lengthValue = 0;
        do { digitValue[lengthValue++] = '0' + line % 10; line /= 10; } while (line);
        while (lengthValue) putchar(digitValue[--lengthValue]);
        putchar('\n'); _exit(1);
    }
}
#define verify(condition) Checks((condition), __LINE__)

int main(int argumentsCount, char **argumentList) {
    char data[32]; struct stat stateValue;
    verify(argumentsCount == 2 && strcmp(argumentList[1], "check") == 0 && argumentList[2] == 0);
    verify(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    verify(openFile("absent", readOnlyValue) == -1 && errorNumber == ENOENT);
    int file = openFile("/posix.txt", ReadWrite | createNewFile, 0640);
    verify(file == 3);
    verify(writeFileData(file, "abcd", 4) == 4);
    verify(openFile("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    verify(readFileStatus(file, &stateValue) == 0 && stateValue.st_size == 4 && S_ISREG(stateValue.st_mode));
    verify((stateValue.st_mode & 0777) == 0640 && stateValue.st_nlink == 1);
    verify(seekFile(file, 0, FromBeginning) == 0);
    int cloneValue = duplicateFileDescriptor(file);
    verify(cloneValue == 4);
    verify(readFileData(cloneValue, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    verify(readFileData(file, data, 2) == 2 && memcmp(data, "cd", 2) == 0);
    verify(readFileData(file, data, 1) == 0);
    verify(fcntl(file, F_SETFD, FD_CLOEXEC) == 0 && fcntl(file, F_GETFD) == 1);
    verify(fcntl(cloneValue, F_GETFD) == 0);
    verify(dup2(file, file) == file && fcntl(file, F_GETFD) == 1);
    verify(dup2(-1, cloneValue) == -1 && errno == EBADF && fcntl(cloneValue, F_GETFD) == 0);
    verify(fcntl(cloneValue, F_SETFL, O_APPEND) == 0 && (fcntl(file, F_GETFL) & O_APPEND));
    verify(lseek(file, 0, SEEK_SET) == 0 && write(cloneValue, "e", 1) == 1 && lseek(file, 0, SEEK_CUR) == 5);
    verify(fcntl(file, F_SETFL, 0) == 0);
    verify(lseek(file, 8, SEEK_SET) == 8 && write(file, "Z", 1) == 1);
    verify(lseek(cloneValue, 5, SEEK_SET) == 5 && read(file, data, 4) == 4);
    verify(data[0] == 0 && data[1] == 0 && data[2] == 0 && data[3] == 'Z');
    verify(ftruncate(file, 2) == 0 && lseek(file, 0, SEEK_CUR) == 9);
    verify(ftruncate(file, 6) == 0 && lseek(file, 2, SEEK_SET) == 2 && read(file, data, 4) == 4);
    verify(!data[0] && !data[1] && !data[2] && !data[3]);
    verify(lseek(file, 2147483647, SEEK_SET) == 2147483647);
    verify(lseek(file, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    verify(lseek(file, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    verify(write(file, "!", 1) == -1 && errno == EFBIG);
    verify(lseek(file, 0, SEEK_SET) == 0);
    verify(read(file, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verify(read(file, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    verify(write(file, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    verify(read(file, data, (size_t)-1) == -1 && errno == EINVAL);
    verify(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    verify(fstat(file, (void *)0x00100000) == -1 && errno == EFAULT);
    verify(lseek(file, 0, SEEK_CUR) == 0);
    verify(read(file, NULL, 0) == 0 && write(file, NULL, 0) == 0);
    verify(removeFileEntryName("posix.txt") == 0);
    verify(fstat(file, &stateValue) == 0 && stateValue.st_nlink == 0 && stateValue.st_size == 6);
    int newFile = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    verify(newFile == 5 && fstat(newFile, &stateValue) == 0 && stateValue.st_size == 0);
    verify(read(file, data, 2) == 2 && memcmp(data, "ab", 2) == 0);
    verify(close(file) == 0 && close(cloneValue) == 0 && close(newFile) == 0);
    verify(close(newFile) == -1 && errno == EBADF);
    verify(unlink("posix.txt") == 0);
    file = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    verify(file == 3 && fcntl(file, F_GETFD) == 1);
    verify(read(file, data, 1) == -1 && errno == EBADF);
    verify(write(file, "keep", 4) == 4);
    for (int index = 4; index < 32; index++) verify(dup(file) == index);
    verify(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    verify(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    verify(fstat(file, &stateValue) == 0 && stateValue.st_size == 4);
    for (int index = 3; index < 32; index++) verify(close(index) == 0);
    verify(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    file = open("posix.txt", O_RDONLY);
    verify(file == 3 && write(file, data, 1) == -1 && errno == EBADF);
    verify(fcntl(file, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    verify(close(8) == 0 && close(file) == 0 && unlink("posix.txt") == 0);
    verify(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    verify(fstat(1, &stateValue) == 0 && S_ISCHR(stateValue.st_mode));
    verify(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    verify(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr address; char addressText[16];
    verify(inet_pton(AF_INET, "10.0.2.2", &address) == 1 && ntohl(address.s_addr) == 0x0a000202U);
    verify(inet_ntop(AF_INET, &address, addressText, sizeof addressText) == addressText && strcmp(addressText, "10.0.2.2") == 0);
    verify(inet_pton(AF_INET, "256.0.0.1", &address) == 0 && ntohl(address.s_addr) == 0x0a000202U);
    verify(inet_pton(AF_INET, "01.0.0.1", &address) == 0);
    verify(inet_ntop(AF_INET, &address, addressText, 3) == NULL && errno == ENOSPC);
    verify(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int preserveValue[8], itemCount = 0; char name[] = "slot0";
    for (int index = 0; index < 8; index++) {
        name[4] = '0' + index;
        int openedFile = open(name, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (openedFile < 0) { verify(errno == ENOSPC); break; }
        preserveValue[itemCount++] = openedFile;
    }
    verify(itemCount > 0 && itemCount < 8);
    verify(unlink("slot0") == 0);
    verify(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    verify(close(preserveValue[0]) == 0);
    file = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    verify(file >= 0 && close(file) == 0 && unlink("held-slot") == 0);
    for (int index = 1; index < itemCount; index++) {
        name[4] = '0' + index;
        verify(close(preserveValue[index]) == 0 && unlink(name) == 0);
    }
    verify(fsync(-1) == -1 && errno == EBADF);
    verify(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
