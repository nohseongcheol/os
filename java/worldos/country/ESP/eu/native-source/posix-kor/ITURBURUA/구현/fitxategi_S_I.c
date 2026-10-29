#include <파일규약.h>
#include "호출경계.h"

int errorearen_zenbaki;
int 호출결과(int EMAITZA) {
    if (EMAITZA < 0) { errorearen_zenbaki = -EMAITZA; return -1; }
    return EMAITZA;
}
int open(const char *fitxategi_sarrera_izen, int ireki_Ezarpenak, ...) {
    mode_t 허가 = 0;
    if (ireki_Ezarpenak & O_CREAT) {
        __builtin_va_list Argumentuak;
        __builtin_va_start(Argumentuak, ireki_Ezarpenak);
        허가 = __builtin_va_arg(Argumentuak, mode_t);
        __builtin_va_end(Argumentuak);
    }
    return 호출결과(jkoros_syscall(30, (int)fitxategi_sarrera_izen, ireki_Ezarpenak, 허가, 0, 0));
}
int creat(const char *fitxategi_sarrera_izen, mode_t 허가) { return open(fitxategi_sarrera_izen, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *datuak, size_t byte_ZENBATU) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)datuak, byte_ZENBATU, 0, 0));
}
ssize_t write(int 파일서술자, const void *datuak, size_t byte_ZENBATU) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)datuak, byte_ZENBATU, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Geruzak_balio, int Project_erro) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Geruzak_balio, Project_erro, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Egoera_balio) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Egoera_balio, 0, 0, 0)); }
int unlink(const char *fitxategi_sarrera_izen) { return 호출결과(jkoros_syscall(38, (int)fitxategi_sarrera_izen, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_ZENBATU) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_ZENBATU, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Komandoa, ...) {
    int balio = 0;
    if (Komandoa == F_DUPFD || Komandoa == F_DUPFD_CLOEXEC || Komandoa == F_SETFD || Komandoa == F_SETFL) {
        __builtin_va_list Argumentuak;
        __builtin_va_start(Argumentuak, Komandoa); balio = __builtin_va_arg(Argumentuak, int); __builtin_va_end(Argumentuak);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Komandoa, balio, 0, 0));
}
