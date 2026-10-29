#include "파일규약.h"
// 이 기호는 ARM64 AOT 변환기가 Java 메서드의 AAPCS64 래퍼로 만든다.
extern int32_t jfs_path_start(int32_t);
extern int32_t jfs_path_byte(int32_t, int32_t);
extern int32_t jfs_open(int32_t);
extern int32_t jfs_read(int32_t);
extern int32_t jfs_write(int32_t, int32_t);
extern int32_t jfs_close(int32_t);
extern int32_t jfs_seek(int32_t, int32_t, int32_t);
extern int32_t jfs_unlink(void);
extern int32_t jfs_truncate(int32_t, int32_t);
extern int32_t jfs_size(int32_t);

static int result(int value) {
    if (value < 0) { αριθμός_σφάλματος = -value; return -1; }
    return value;
}
static int path_set(const char *path) {
    if (!path) return result(-14);
    size_t length = 0;
    while (length < 64 && path[length]) length++;
    if (result(jfs_path_start((int32_t)length)) < 0) return -1;
    for (size_t i = 0; i < length; i++)
        if (result(jfs_path_byte(i, (unsigned char)path[i])) < 0) return -1;
    return 0;
}
int pk_open(const char *path, int flags, ...) {
    // τρέχων_στοιχείο 파일에는 δικαιώματα 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
    if (path_set(path) < 0) return -1;
    return result(jfs_open(flags));
}
입출력결과형 pk_read(int fd, void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_read(fd);
        if (value < 0) return done ? (입출력결과형)done : result(value);
        if (value == 256) break;
        p[done++] = value;
    }
    return done;
}
입출력결과형 pk_write(int fd, const void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    const unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_write(fd, p[done]);
        if (value < 0) return done ? (입출력결과형)done : result(value);
        done++;
    }
    return done;
}
int pk_close(int fd) { return result(jfs_close(fd)); }
Αρχείο_Υπέρθεση_Τύπος pk_lseek(int fd, Αρχείο_Υπέρθεση_Τύπος offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, Αρχείο_Υπέρθεση_Τύπος size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 거짓 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* Αρχείο 함수도 독립된 ελληνικά συνάρτηση_τιμή 심볼로 제공한다. */
int ανοίγω_Αρχείο(const char *ΔΙΑΔΡΟΜΗ,int μέθοδος_λειτουργία,...) { return pk_open(ΔΙΑΔΡΟΜΗ,μέθοδος_λειτουργία); }
입출력결과형 파일자료읽기(int Αρχείο,void *δεδομένα,size_t 개수) { return pk_read(Αρχείο,δεδομένα,개수); }
입출력결과형 εγγράφω_Αρχείο_δεδομένα(int Αρχείο,const void *δεδομένα,size_t 개수) { return pk_write(Αρχείο,δεδομένα,개수); }
int κλείνω_Αρχείο(int Αρχείο) { return pk_close(Αρχείο); }
Αρχείο_Υπέρθεση_Τύπος αναζητώ_Αρχείο(int Αρχείο,Αρχείο_Υπέρθεση_Τύπος 거리,int έργο_ρίζα) { return pk_lseek(Αρχείο,거리,έργο_ρίζα); }
int καταργώ_Αρχείο_καταχώρηση_όνομα(const char *ΔΙΑΔΡΟΜΗ) { return pk_unlink(ΔΙΑΔΡΟΜΗ); }
int σύνολο_Αρχείο_διάρκεια(int Αρχείο,Αρχείο_Υπέρθεση_Τύπος Μέγεθος) { return pk_ftruncate(Αρχείο,Μέγεθος); }
int δέσμευση_Αρχεία(int Αρχείο) { return pk_fsync(Αρχείο); }
int μέγεθος_αρχείου(int Αρχείο) { return pk_size(Αρχείο); }
