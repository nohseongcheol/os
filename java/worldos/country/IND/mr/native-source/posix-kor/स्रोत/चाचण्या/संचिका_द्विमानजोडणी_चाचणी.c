#include <संचिका_द्विमानजोडणी.h>
#include <संचारजाळे_द्विमानजोडणी.h>
#include <string.h>
#include <stdio.h>

static int पडताळलेले_आयटम_संख्या;
static void पडताळण्या(int सशर्त, int ओळ) {
    पडताळलेले_आयटम_संख्या++;
    if (!सशर्त) {
        puts("POSIX CHECK FAILED");
        char अंक_मूल्य[12]; int लांबी_मूल्य = 0;
        do { अंक_मूल्य[लांबी_मूल्य++] = '0' + ओळ % 10; ओळ /= 10; } while (ओळ);
        while (लांबी_मूल्य) putchar(अंक_मूल्य[--लांबी_मूल्य]);
        putchar('\n'); _exit(1);
    }
}
#define पडताळा(सशर्त) पडताळण्या((सशर्त), __LINE__)

int main(int वितर्क_संख्या_e5e1cf1c, char **वितर्क_यादी) {
    char डेटा[32]; struct stat राज्य_मूल्य;
    पडताळा(वितर्क_संख्या_e5e1cf1c == 2 && strcmp(वितर्क_यादी[1], "check") == 0 && वितर्क_यादी[2] == 0);
    पडताळा(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    पडताळा(संचिका_उघडा("absent", केवळ_मूल्य_वाचा) == -1 && त्रुटी_संख्या == ENOENT);
    int फाइल = संचिका_उघडा("/posix.txt", वाचणे_लिहिणे | नवे_संचिका_तयार_करा, 0640);
    पडताळा(फाइल == 3);
    पडताळा(संचिका_डेटा_लिहा(फाइल, "abcd", 4) == 4);
    पडताळा(संचिका_उघडा("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    पडताळा(संचिका_राज्य_वाचा(फाइल, &राज्य_मूल्य) == 0 && राज्य_मूल्य.st_size == 4 && S_ISREG(राज्य_मूल्य.st_mode));
    पडताळा((राज्य_मूल्य.st_mode & 0777) == 0640 && राज्य_मूल्य.st_nlink == 1);
    पडताळा(शोधा_संचिका(फाइल, 0, पासून_आरंभ) == 0);
    int प्रतबनवा_मूल्य = प्रतिरूप_संचिका_विवरणक(फाइल);
    पडताळा(प्रतबनवा_मूल्य == 4);
    पडताळा(संचिका_डेटा_वाचा(प्रतबनवा_मूल्य, डेटा, 2) == 2 && memcmp(डेटा, "ab", 2) == 0);
    पडताळा(संचिका_डेटा_वाचा(फाइल, डेटा, 2) == 2 && memcmp(डेटा, "cd", 2) == 0);
    पडताळा(संचिका_डेटा_वाचा(फाइल, डेटा, 1) == 0);
    पडताळा(fcntl(फाइल, F_SETFD, FD_CLOEXEC) == 0 && fcntl(फाइल, F_GETFD) == 1);
    पडताळा(fcntl(प्रतबनवा_मूल्य, F_GETFD) == 0);
    पडताळा(dup2(फाइल, फाइल) == फाइल && fcntl(फाइल, F_GETFD) == 1);
    पडताळा(dup2(-1, प्रतबनवा_मूल्य) == -1 && errno == EBADF && fcntl(प्रतबनवा_मूल्य, F_GETFD) == 0);
    पडताळा(fcntl(प्रतबनवा_मूल्य, F_SETFL, O_APPEND) == 0 && (fcntl(फाइल, F_GETFL) & O_APPEND));
    पडताळा(lseek(फाइल, 0, SEEK_SET) == 0 && write(प्रतबनवा_मूल्य, "e", 1) == 1 && lseek(फाइल, 0, SEEK_CUR) == 5);
    पडताळा(fcntl(फाइल, F_SETFL, 0) == 0);
    पडताळा(lseek(फाइल, 8, SEEK_SET) == 8 && write(फाइल, "Z", 1) == 1);
    पडताळा(lseek(प्रतबनवा_मूल्य, 5, SEEK_SET) == 5 && read(फाइल, डेटा, 4) == 4);
    पडताळा(डेटा[0] == 0 && डेटा[1] == 0 && डेटा[2] == 0 && डेटा[3] == 'Z');
    पडताळा(ftruncate(फाइल, 2) == 0 && lseek(फाइल, 0, SEEK_CUR) == 9);
    पडताळा(ftruncate(फाइल, 6) == 0 && lseek(फाइल, 2, SEEK_SET) == 2 && read(फाइल, डेटा, 4) == 4);
    पडताळा(!डेटा[0] && !डेटा[1] && !डेटा[2] && !डेटा[3]);
    पडताळा(lseek(फाइल, 2147483647, SEEK_SET) == 2147483647);
    पडताळा(lseek(फाइल, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    पडताळा(lseek(फाइल, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    पडताळा(write(फाइल, "!", 1) == -1 && errno == EFBIG);
    पडताळा(lseek(फाइल, 0, SEEK_SET) == 0);
    पडताळा(read(फाइल, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    पडताळा(read(फाइल, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    पडताळा(write(फाइल, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    पडताळा(read(फाइल, डेटा, (size_t)-1) == -1 && errno == EINVAL);
    पडताळा(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    पडताळा(fstat(फाइल, (void *)0x00100000) == -1 && errno == EFAULT);
    पडताळा(lseek(फाइल, 0, SEEK_CUR) == 0);
    पडताळा(read(फाइल, NULL, 0) == 0 && write(फाइल, NULL, 0) == 0);
    पडताळा(संचिका_प्रविष्टी_नाव_काढणे("posix.txt") == 0);
    पडताळा(fstat(फाइल, &राज्य_मूल्य) == 0 && राज्य_मूल्य.st_nlink == 0 && राज्य_मूल्य.st_size == 6);
    int नवे_संचिका = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    पडताळा(नवे_संचिका == 5 && fstat(नवे_संचिका, &राज्य_मूल्य) == 0 && राज्य_मूल्य.st_size == 0);
    पडताळा(read(फाइल, डेटा, 2) == 2 && memcmp(डेटा, "ab", 2) == 0);
    पडताळा(close(फाइल) == 0 && close(प्रतबनवा_मूल्य) == 0 && close(नवे_संचिका) == 0);
    पडताळा(close(नवे_संचिका) == -1 && errno == EBADF);
    पडताळा(unlink("posix.txt") == 0);
    फाइल = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    पडताळा(फाइल == 3 && fcntl(फाइल, F_GETFD) == 1);
    पडताळा(read(फाइल, डेटा, 1) == -1 && errno == EBADF);
    पडताळा(write(फाइल, "keep", 4) == 4);
    for (int अनुक्रमणिका = 4; अनुक्रमणिका < 32; अनुक्रमणिका++) पडताळा(dup(फाइल) == अनुक्रमणिका);
    पडताळा(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    पडताळा(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    पडताळा(fstat(फाइल, &राज्य_मूल्य) == 0 && राज्य_मूल्य.st_size == 4);
    for (int अनुक्रमणिका = 3; अनुक्रमणिका < 32; अनुक्रमणिका++) पडताळा(close(अनुक्रमणिका) == 0);
    पडताळा(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    फाइल = open("posix.txt", O_RDONLY);
    पडताळा(फाइल == 3 && write(फाइल, डेटा, 1) == -1 && errno == EBADF);
    पडताळा(fcntl(फाइल, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    पडताळा(close(8) == 0 && close(फाइल) == 0 && unlink("posix.txt") == 0);
    पडताळा(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    पडताळा(fstat(1, &राज्य_मूल्य) == 0 && S_ISCHR(राज्य_मूल्य.st_mode));
    पडताळा(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    पडताळा(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr पत्ता; char पत्ता_मजकूर[16];
    पडताळा(inet_pton(AF_INET, "10.0.2.2", &पत्ता) == 1 && ntohl(पत्ता.s_addr) == 0x0a000202U);
    पडताळा(inet_ntop(AF_INET, &पत्ता, पत्ता_मजकूर, sizeof पत्ता_मजकूर) == पत्ता_मजकूर && strcmp(पत्ता_मजकूर, "10.0.2.2") == 0);
    पडताळा(inet_pton(AF_INET, "256.0.0.1", &पत्ता) == 0 && ntohl(पत्ता.s_addr) == 0x0a000202U);
    पडताळा(inet_pton(AF_INET, "01.0.0.1", &पत्ता) == 0);
    पडताळा(inet_ntop(AF_INET, &पत्ता, पत्ता_मजकूर, 3) == NULL && errno == ENOSPC);
    पडताळा(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int जतनकरा_मूल्य[8], आयटम_संख्या = 0; char नाव[] = "slot0";
    for (int अनुक्रमणिका = 0; अनुक्रमणिका < 8; अनुक्रमणिका++) {
        नाव[4] = '0' + अनुक्रमणिका;
        int उघडलेले_संचिका = open(नाव, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (उघडलेले_संचिका < 0) { पडताळा(errno == ENOSPC); break; }
        जतनकरा_मूल्य[आयटम_संख्या++] = उघडलेले_संचिका;
    }
    पडताळा(आयटम_संख्या > 0 && आयटम_संख्या < 8);
    पडताळा(unlink("slot0") == 0);
    पडताळा(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    पडताळा(close(जतनकरा_मूल्य[0]) == 0);
    फाइल = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    पडताळा(फाइल >= 0 && close(फाइल) == 0 && unlink("held-slot") == 0);
    for (int अनुक्रमणिका = 1; अनुक्रमणिका < आयटम_संख्या; अनुक्रमणिका++) {
        नाव[4] = '0' + अनुक्रमणिका;
        पडताळा(close(जतनकरा_मूल्य[अनुक्रमणिका]) == 0 && unlink(नाव) == 0);
    }
    पडताळा(fsync(-1) == -1 && errno == EBADF);
    पडताळा(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
