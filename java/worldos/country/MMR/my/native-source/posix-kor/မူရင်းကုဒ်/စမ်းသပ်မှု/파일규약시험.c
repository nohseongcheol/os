#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

static int 검사항목수;
static void စစ်ဆေးချက်(int အခြေအနေစည်းကမ်း, int စာကြောင်း) {
    검사항목수++;
    if (!အခြေအနေစည်းကမ်း) {
        puts("POSIX CHECK FAILED");
        char ဂဏန်းတန်ဖိုး[12]; int အလျား = 0;
        do { ဂဏန်းတန်ဖိုး[အလျား++] = '0' + စာကြောင်း % 10; စာကြောင်း /= 10; } while (စာကြောင်း);
        while (အလျား) putchar(ဂဏန်းတန်ဖိုး[--အလျား]);
        putchar('\n'); _exit(1);
    }
}
#define အတည်ပြု(အခြေအနေစည်းကမ်း) စစ်ဆေးချက်((အခြေအနေစည်းကမ်း), __LINE__)

int main(int ပေးအချက်များအရေအတွက်, char **ပေးအချက်စာရင်း) {
    char ဒေတာ[32]; struct stat အခြေအနေတန်ဖိုး;
    အတည်ပြု(ပေးအချက်များအရေအတွက် == 2 && strcmp(ပေးအချက်စာရင်း[1], "check") == 0 && ပေးအချက်စာရင်း[2] == 0);
    အတည်ပြု(sizeof(struct stat) == 48 && sizeof(struct sockaddr_in) == 16);
    အတည်ပြု(ဖိုင်ဖွင့်("absent", သာတန်ဖိုးဖတ်) == -1 && အမှားကိန်း == ENOENT);
    int ဖိုင် = ဖိုင်ဖွင့်("/posix.txt", ဖတ်ရေး | အသစ်ဖိုင်ဖန်တီး, 0640);
    အတည်ပြု(ဖိုင် == 3);
    အတည်ပြု(ဖိုင်ဒေတာရေး(ဖိုင်, "abcd", 4) == 4);
    အတည်ပြု(ဖိုင်ဖွင့်("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600) == -1 && errno == EEXIST);
    အတည်ပြု(ဖိုင်လက်ရှိအခြေအနေဖတ်(ဖိုင်, &အခြေအနေတန်ဖိုး) == 0 && အခြေအနေတန်ဖိုး.st_size == 4 && S_ISREG(အခြေအနေတန်ဖိုး.st_mode));
    အတည်ပြု((အခြေအနေတန်ဖိုး.st_mode & 0777) == 0640 && အခြေအနေတန်ဖိုး.st_nlink == 1);
    အတည်ပြု(ဖိုင်နေရာရွှေ့(ဖိုင်, 0, 처음기준) == 0);
    int ပုံတူပွားတန်ဖိုး = မိတ္တူဖိုင်အညွှန်း(ဖိုင်);
    အတည်ပြု(ပုံတူပွားတန်ဖိုး == 4);
    အတည်ပြု(ဖိုင်ဒေတာဖတ်(ပုံတူပွားတန်ဖိုး, ဒေတာ, 2) == 2 && memcmp(ဒေတာ, "ab", 2) == 0);
    အတည်ပြု(ဖိုင်ဒေတာဖတ်(ဖိုင်, ဒေတာ, 2) == 2 && memcmp(ဒေတာ, "cd", 2) == 0);
    အတည်ပြု(ဖိုင်ဒေတာဖတ်(ဖိုင်, ဒေတာ, 1) == 0);
    အတည်ပြု(fcntl(ဖိုင်, F_SETFD, FD_CLOEXEC) == 0 && fcntl(ဖိုင်, F_GETFD) == 1);
    အတည်ပြု(fcntl(ပုံတူပွားတန်ဖိုး, F_GETFD) == 0);
    အတည်ပြု(dup2(ဖိုင်, ဖိုင်) == ဖိုင် && fcntl(ဖိုင်, F_GETFD) == 1);
    အတည်ပြု(dup2(-1, ပုံတူပွားတန်ဖိုး) == -1 && errno == EBADF && fcntl(ပုံတူပွားတန်ဖိုး, F_GETFD) == 0);
    အတည်ပြု(fcntl(ပုံတူပွားတန်ဖိုး, F_SETFL, O_APPEND) == 0 && (fcntl(ဖိုင်, F_GETFL) & O_APPEND));
    အတည်ပြု(lseek(ဖိုင်, 0, SEEK_SET) == 0 && write(ပုံတူပွားတန်ဖိုး, "e", 1) == 1 && lseek(ဖိုင်, 0, SEEK_CUR) == 5);
    အတည်ပြု(fcntl(ဖိုင်, F_SETFL, 0) == 0);
    အတည်ပြု(lseek(ဖိုင်, 8, SEEK_SET) == 8 && write(ဖိုင်, "Z", 1) == 1);
    အတည်ပြု(lseek(ပုံတူပွားတန်ဖိုး, 5, SEEK_SET) == 5 && read(ဖိုင်, ဒေတာ, 4) == 4);
    အတည်ပြု(ဒေတာ[0] == 0 && ဒေတာ[1] == 0 && ဒေတာ[2] == 0 && ဒေတာ[3] == 'Z');
    အတည်ပြု(ftruncate(ဖိုင်, 2) == 0 && lseek(ဖိုင်, 0, SEEK_CUR) == 9);
    အတည်ပြု(ftruncate(ဖိုင်, 6) == 0 && lseek(ဖိုင်, 2, SEEK_SET) == 2 && read(ဖိုင်, ဒေတာ, 4) == 4);
    အတည်ပြု(!ဒေတာ[0] && !ဒေတာ[1] && !ဒေတာ[2] && !ဒေတာ[3]);
    အတည်ပြု(lseek(ဖိုင်, 2147483647, SEEK_SET) == 2147483647);
    အတည်ပြု(lseek(ဖိုင်, 1, SEEK_CUR) == -1 && errno == EOVERFLOW);
    အတည်ပြု(lseek(ဖိုင်, -2147483647 - 1, SEEK_CUR) == -1 && errno == EINVAL);
    အတည်ပြု(write(ဖိုင်, "!", 1) == -1 && errno == EFBIG);
    အတည်ပြု(lseek(ဖိုင်, 0, SEEK_SET) == 0);
    အတည်ပြု(read(ဖိုင်, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    အတည်ပြု(read(ဖိုင်, (void *)0x043fffff, 2) == -1 && errno == EFAULT);
    အတည်ပြု(write(ဖိုင်, (void *)0x00100000, 1) == -1 && errno == EFAULT);
    အတည်ပြု(read(ဖိုင်, ဒေတာ, (size_t)-1) == -1 && errno == EINVAL);
    အတည်ပြု(open((const char *)0x00100000, O_CREAT, 0600) == -1 && errno == EFAULT);
    အတည်ပြု(fstat(ဖိုင်, (void *)0x00100000) == -1 && errno == EFAULT);
    အတည်ပြု(lseek(ဖိုင်, 0, SEEK_CUR) == 0);
    အတည်ပြု(read(ဖိုင်, NULL, 0) == 0 && write(ဖိုင်, NULL, 0) == 0);
    အတည်ပြု(ဖိုင်အချက်အမည်ဖယ်ရှား("posix.txt") == 0);
    အတည်ပြု(fstat(ဖိုင်, &အခြေအနေတန်ဖိုး) == 0 && အခြေအနေတန်ဖိုး.st_nlink == 0 && အခြေအနေတန်ဖိုး.st_size == 6);
    int အသစ်ဖိုင် = open("posix.txt", O_RDWR | O_CREAT | O_EXCL, 0600);
    အတည်ပြု(အသစ်ဖိုင် == 5 && fstat(အသစ်ဖိုင်, &အခြေအနေတန်ဖိုး) == 0 && အခြေအနေတန်ဖိုး.st_size == 0);
    အတည်ပြု(read(ဖိုင်, ဒေတာ, 2) == 2 && memcmp(ဒေတာ, "ab", 2) == 0);
    အတည်ပြု(close(ဖိုင်) == 0 && close(ပုံတူပွားတန်ဖိုး) == 0 && close(အသစ်ဖိုင်) == 0);
    အတည်ပြု(close(အသစ်ဖိုင်) == -1 && errno == EBADF);
    အတည်ပြု(unlink("posix.txt") == 0);
    ဖိုင် = open("posix.txt", O_WRONLY | O_CREAT | O_CLOEXEC, 0600);
    အတည်ပြု(ဖိုင် == 3 && fcntl(ဖိုင်, F_GETFD) == 1);
    အတည်ပြု(read(ဖိုင်, ဒေတာ, 1) == -1 && errno == EBADF);
    အတည်ပြု(write(ဖိုင်, "keep", 4) == 4);
    for (int နံပါတ် = 4; နံပါတ် < 32; နံပါတ်++) အတည်ပြု(dup(ဖိုင်) == နံပါတ်);
    အတည်ပြု(open("posix.txt", O_WRONLY | O_TRUNC) == -1 && errno == EMFILE);
    အတည်ပြု(open("no-side", O_CREAT | O_RDWR, 0600) == -1 && errno == EMFILE);
    အတည်ပြု(fstat(ဖိုင်, &အခြေအနေတန်ဖိုး) == 0 && အခြေအနေတန်ဖိုး.st_size == 4);
    for (int နံပါတ် = 3; နံပါတ် < 32; နံပါတ်++) အတည်ပြု(close(နံပါတ်) == 0);
    အတည်ပြု(open("no-side", O_RDONLY) == -1 && errno == ENOENT);
    ဖိုင် = open("posix.txt", O_RDONLY);
    အတည်ပြု(ဖိုင် == 3 && write(ဖိုင်, ဒေတာ, 1) == -1 && errno == EBADF);
    အတည်ပြု(fcntl(ဖိုင်, F_DUPFD_CLOEXEC, 8) == 8 && fcntl(8, F_GETFD) == 1);
    အတည်ပြု(close(8) == 0 && close(ဖိုင်) == 0 && unlink("posix.txt") == 0);
    အတည်ပြု(lseek(1, 0, SEEK_SET) == -1 && errno == ESPIPE);
    အတည်ပြု(fstat(1, &အခြေအနေတန်ဖိုး) == 0 && S_ISCHR(အခြေအနေတန်ဖိုး.st_mode));
    အတည်ပြု(socket(AF_INET, SOCK_STREAM, 0) == -1 && errno == EPROTONOSUPPORT);
    အတည်ပြု(socket(99, SOCK_DGRAM, 0) == -1 && errno == EAFNOSUPPORT);
    struct in_addr လိပ်စာ; char လိပ်စာစာသား[16];
    အတည်ပြု(inet_pton(AF_INET, "10.0.2.2", &လိပ်စာ) == 1 && ntohl(လိပ်စာ.s_addr) == 0x0a000202U);
    အတည်ပြု(inet_ntop(AF_INET, &လိပ်စာ, လိပ်စာစာသား, sizeof လိပ်စာစာသား) == လိပ်စာစာသား && strcmp(လိပ်စာစာသား, "10.0.2.2") == 0);
    အတည်ပြု(inet_pton(AF_INET, "256.0.0.1", &လိပ်စာ) == 0 && ntohl(လိပ်စာ.s_addr) == 0x0a000202U);
    အတည်ပြု(inet_pton(AF_INET, "01.0.0.1", &လိပ်စာ) == 0);
    အတည်ပြု(inet_ntop(AF_INET, &လိပ်စာ, လိပ်စာစာသား, 3) == NULL && errno == ENOSPC);
    အတည်ပြု(ntohs(htons(12345)) == 12345 && ntohl(htonl(0x89abcdef)) == 0x89abcdef);
    int တန်ဖိုးထိန်းသိမ်း[8], အရေအတွက် = 0; char အမည်[] = "slot0";
    for (int နံပါတ် = 0; နံပါတ် < 8; နံပါတ်++) {
        အမည်[4] = '0' + နံပါတ်;
        int ဖွင့်ထားဖိုင် = open(အမည်, O_RDWR | O_CREAT | O_EXCL, 0600);
        if (ဖွင့်ထားဖိုင် < 0) { အတည်ပြု(errno == ENOSPC); break; }
        တန်ဖိုးထိန်းသိမ်း[အရေအတွက်++] = ဖွင့်ထားဖိုင်;
    }
    အတည်ပြု(အရေအတွက် > 0 && အရေအတွက် < 8);
    အတည်ပြု(unlink("slot0") == 0);
    အတည်ပြု(open("held-slot", O_RDWR | O_CREAT, 0600) == -1 && errno == ENOSPC);
    အတည်ပြု(close(တန်ဖိုးထိန်းသိမ်း[0]) == 0);
    ဖိုင် = open("held-slot", O_RDWR | O_CREAT | O_EXCL, 0600);
    အတည်ပြု(ဖိုင် >= 0 && close(ဖိုင်) == 0 && unlink("held-slot") == 0);
    for (int နံပါတ် = 1; နံပါတ် < အရေအတွက်; နံပါတ်++) {
        အမည်[4] = '0' + နံပါတ်;
        အတည်ပြု(close(တန်ဖိုးထိန်းသိမ်း[နံပါတ်]) == 0 && unlink(အမည်) == 0);
    }
    အတည်ပြု(fsync(-1) == -1 && errno == EBADF);
    အတည်ပြု(fsync(1) == -1 && errno == EINVAL);
    puts("POSIX FILE CHECK PASS");
    puts("Korean identifiers and C ABI PASS");
    return 0;
}
