#include <ABITệp.h>
#include "RanhGiớiGọi.h"

int sốLỗi;
int kếtQuảLờiGọi(int kếtQuả) {
    if (kếtQuả < 0) { sốLỗi = -kếtQuả; return -1; }
    return kếtQuả;
}
int open(const char *tênMụcTệp, int mởCácThiếtLập, ...) {
    mode_t cấpQuyềnQuyền = 0;
    if (mởCácThiếtLập & O_CREAT) {
        __builtin_va_list cácĐốiSố;
        __builtin_va_start(cácĐốiSố, mởCácThiếtLập);
        cấpQuyềnQuyền = __builtin_va_arg(cácĐốiSố, mode_t);
        __builtin_va_end(cácĐốiSố);
    }
    return kếtQuảLờiGọi(jkoros_syscall(30, (int)tênMụcTệp, mởCácThiếtLập, cấpQuyềnQuyền, 0, 0));
}
int creat(const char *tênMụcTệp, mode_t cấpQuyềnQuyền) { return open(tênMụcTệp, O_WRONLY | O_CREAT | O_TRUNC, cấpQuyềnQuyền); }
ssize_t read(int bộMôTảTệp, void *DữLiệu, size_t sốLượngByte) {
    return kếtQuảLờiGọi(jkoros_syscall(31, bộMôTảTệp, (int)DữLiệu, sốLượngByte, 0, 0));
}
ssize_t write(int bộMôTảTệp, const void *DữLiệu, size_t sốLượngByte) {
    return kếtQuảLờiGọi(jkoros_syscall(32, bộMôTảTệp, (int)DữLiệu, sốLượngByte, 0, 0));
}
int close(int bộMôTảTệp) { return kếtQuảLờiGọi(jkoros_syscall(33, bộMôTảTệp, 0, 0, 0, 0)); }
off_t lseek(int bộMôTảTệp, off_t giáTrịĐộLệch, int gốcCâyDựÁn) {
    return kếtQuảLờiGọi(jkoros_syscall(34, bộMôTảTệp, giáTrịĐộLệch, gốcCâyDựÁn, 0, 0));
}
int dup(int bộMôTảTệp) { return kếtQuảLờiGọi(jkoros_syscall(35, bộMôTảTệp, 0, 0, 0, 0)); }
int dup2(int bộMôTảTệp, int bộMôTảMới) { return kếtQuảLờiGọi(jkoros_syscall(36, bộMôTảTệp, bộMôTảMới, 0, 0, 0)); }
int fstat(int bộMôTảTệp, struct stat *giáTrịTrạngThái) { return kếtQuảLờiGọi(jkoros_syscall(37, bộMôTảTệp, (int)giáTrịTrạngThái, 0, 0, 0)); }
int unlink(const char *tênMụcTệp) { return kếtQuảLờiGọi(jkoros_syscall(38, (int)tênMụcTệp, 0, 0, 0, 0)); }
int ftruncate(int bộMôTảTệp, off_t sốLượngByte) { return kếtQuảLờiGọi(jkoros_syscall(39, bộMôTảTệp, sốLượngByte, 0, 0, 0)); }
int fsync(int bộMôTảTệp) { return kếtQuảLờiGọi(jkoros_syscall(47, bộMôTảTệp, 0, 0, 0, 0)); }
int fcntl(int bộMôTảTệp, int lệnh, ...) {
    int giáTrị = 0;
    if (lệnh == F_DUPFD || lệnh == F_DUPFD_CLOEXEC || lệnh == F_SETFD || lệnh == F_SETFL) {
        __builtin_va_list cácĐốiSố;
        __builtin_va_start(cácĐốiSố, lệnh); giáTrị = __builtin_va_arg(cácĐốiSố, int); __builtin_va_end(cácĐốiSố);
    }
    return kếtQuảLờiGọi(jkoros_syscall(40, bộMôTảTệp, lệnh, giáTrị, 0, 0));
}
