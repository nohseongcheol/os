#include <Dosya_ABI.h>
#include "Ara_sınır.h"

int hata_numarası;
int çağrı_KR(int sonuç) {
    if (sonuç < 0) { hata_numarası = -sonuç; return -1; }
    return sonuç;
}
int open(const char *Dosya_girdi_ad, int açık_Ayarlar, ...) {
    mode_t izin_verme_izin = 0;
    if (açık_Ayarlar & O_CREAT) {
        __builtin_va_list bağımsız_değişkenler;
        __builtin_va_start(bağımsız_değişkenler, açık_Ayarlar);
        izin_verme_izin = __builtin_va_arg(bağımsız_değişkenler, mode_t);
        __builtin_va_end(bağımsız_değişkenler);
    }
    return çağrı_KR(jkoros_syscall(30, (int)Dosya_girdi_ad, açık_Ayarlar, izin_verme_izin, 0, 0));
}
int creat(const char *Dosya_girdi_ad, mode_t izin_verme_izin) { return open(Dosya_girdi_ad, O_WRONLY | O_CREAT | O_TRUNC, izin_verme_izin); }
ssize_t read(int Dosya_tanımlayıcı, void *veri, size_t bayt_BAĞ_DEĞ_SAY) {
    return çağrı_KR(jkoros_syscall(31, Dosya_tanımlayıcı, (int)veri, bayt_BAĞ_DEĞ_SAY, 0, 0));
}
ssize_t write(int Dosya_tanımlayıcı, const void *veri, size_t bayt_BAĞ_DEĞ_SAY) {
    return çağrı_KR(jkoros_syscall(32, Dosya_tanımlayıcı, (int)veri, bayt_BAĞ_DEĞ_SAY, 0, 0));
}
int close(int Dosya_tanımlayıcı) { return çağrı_KR(jkoros_syscall(33, Dosya_tanımlayıcı, 0, 0, 0, 0)); }
off_t lseek(int Dosya_tanımlayıcı, off_t Ofset_değer, int işlem_kök) {
    return çağrı_KR(jkoros_syscall(34, Dosya_tanımlayıcı, Ofset_değer, işlem_kök, 0, 0));
}
int dup(int Dosya_tanımlayıcı) { return çağrı_KR(jkoros_syscall(35, Dosya_tanımlayıcı, 0, 0, 0, 0)); }
int dup2(int Dosya_tanımlayıcı, int 새서술자) { return çağrı_KR(jkoros_syscall(36, Dosya_tanımlayıcı, 새서술자, 0, 0, 0)); }
int fstat(int Dosya_tanımlayıcı, struct stat *Durum_değer) { return çağrı_KR(jkoros_syscall(37, Dosya_tanımlayıcı, (int)Durum_değer, 0, 0, 0)); }
int unlink(const char *Dosya_girdi_ad) { return çağrı_KR(jkoros_syscall(38, (int)Dosya_girdi_ad, 0, 0, 0, 0)); }
int ftruncate(int Dosya_tanımlayıcı, off_t bayt_BAĞ_DEĞ_SAY) { return çağrı_KR(jkoros_syscall(39, Dosya_tanımlayıcı, bayt_BAĞ_DEĞ_SAY, 0, 0, 0)); }
int fsync(int Dosya_tanımlayıcı) { return çağrı_KR(jkoros_syscall(47, Dosya_tanımlayıcı, 0, 0, 0, 0)); }
int fcntl(int Dosya_tanımlayıcı, int komut, ...) {
    int değer = 0;
    if (komut == F_DUPFD || komut == F_DUPFD_CLOEXEC || komut == F_SETFD || komut == F_SETFL) {
        __builtin_va_list bağımsız_değişkenler;
        __builtin_va_start(bağımsız_değişkenler, komut); değer = __builtin_va_arg(bağımsız_değişkenler, int); __builtin_va_end(bağımsız_değişkenler);
    }
    return çağrı_KR(jkoros_syscall(40, Dosya_tanımlayıcı, komut, değer, 0, 0));
}
