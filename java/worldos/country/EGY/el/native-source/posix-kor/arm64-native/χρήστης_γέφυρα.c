// 동일 ελληνικά 헤더를 사용하는 별도 EL0 βιβλιοθήκη. πυρήνας_τιμή 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int κωδικός_σφάλματος;
int *pk_errno_location(void) { return &κωδικός_σφάλματος; }
static intptr_t 결과검사(intptr_t μέτρηση) { if (μέτρηση < 0) { κωδικός_σφάλματος = -μέτρηση; return -1; } return μέτρηση; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Αρχείο_Υπέρθεση_Τύπος pk_lseek(int fd, Αρχείο_Υπέρθεση_Τύπος offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Αρχείο_Υπέρθεση_Τύπος size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 결과검사(사용자호출(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 결과검사(사용자호출(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 결과검사(사용자호출(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 결과검사(사용자호출(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 결과검사(사용자호출(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 결과검사(사용자호출(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* ελληνικά 공개 함수의 πραγματικός_δεδομένα EL0 구현. 구조체는 SVC에서 παρουσία_τιμή·검증한다. */
int ανοίγω_τελικό_σημείο(int διεύθυνση_παιδικά,int 통신방식,int Μεταφορά_πρωτόκολλο) {
    return 결과검사(사용자호출(32,διεύθυνση_παιδικά,통신방식,Μεταφορά_πρωτόκολλο,0,0,0));
}
int συνδέω_διεύθυνση(int τελικό_σημείο,const struct υποδοχή_διεύθυνση *διεύθυνση,υποδοχή_διεύθυνση_διάρκεια_Τύπος διάρκεια_τιμή) {
    return 결과검사(사용자호출(33,τελικό_σημείο,(uintptr_t)διεύθυνση,διάρκεια_τιμή,0,0,0));
}
intptr_t στέλνω_αυτοδύναμο_πακέτο_δεδομένα(int τελικό_σημείο,const void *δεδομένα,size_t 개수,int επιλογή_τιμή,const struct υποδοχή_διεύθυνση *διεύθυνση,υποδοχή_διεύθυνση_διάρκεια_Τύπος διάρκεια_τιμή) {
    return 결과검사(사용자호출(34,τελικό_σημείο,(uintptr_t)δεδομένα,개수,επιλογή_τιμή,(uintptr_t)διεύθυνση,διάρκεια_τιμή));
}
intptr_t λαμβάνω_αυτοδύναμο_πακέτο_δεδομένα(int τελικό_σημείο,void *δεδομένα,size_t 개수,int επιλογή_τιμή,struct υποδοχή_διεύθυνση *διεύθυνση,υποδοχή_διεύθυνση_διάρκεια_Τύπος *διάρκεια_τιμή) {
    return 결과검사(사용자호출(35,τελικό_σημείο,(uintptr_t)δεδομένα,개수,επιλογή_τιμή,(uintptr_t)διεύθυνση,(uintptr_t)διάρκεια_τιμή));
}
int 통신주소읽기(int τελικό_σημείο,struct υποδοχή_διεύθυνση *διεύθυνση,υποδοχή_διεύθυνση_διάρκεια_Τύπος *διάρκεια_τιμή) {
    return 결과검사(사용자호출(36,τελικό_σημείο,(uintptr_t)διεύθυνση,(uintptr_t)διάρκεια_τιμή,0,0,0));
}
int συνδέω_δίκτυο(int τελικό_σημείο,const struct υποδοχή_διεύθυνση *διεύθυνση,υποδοχή_διεύθυνση_διάρκεια_Τύπος διάρκεια_τιμή) {
    return 결과검사(사용자호출(37,τελικό_σημείο,(uintptr_t)διεύθυνση,διάρκεια_τιμή,0,0,0));
}
int 통신연결기다리기(int τελικό_σημείο,int 대기수) {
    return 결과검사(사용자호출(38,τελικό_σημείο,대기수,0,0,0,0));
}
int αποδέχομαι_σύνδεση_δικτύου(int τελικό_σημείο,struct υποδοχή_διεύθυνση *διεύθυνση,υποδοχή_διεύθυνση_διάρκεια_Τύπος *διάρκεια_τιμή) {
    return 결과검사(사용자호출(39,τελικό_σημείο,(uintptr_t)διεύθυνση,(uintptr_t)διάρκεια_τιμή,0,0,0));
}

/* Αρχείο 함수도 독립된 ελληνικά συνάρτηση_τιμή 심볼로 제공한다. */
int ανοίγω_Αρχείο(const char *ΔΙΑΔΡΟΜΗ,int μέθοδος_λειτουργία,...) { return 결과검사(사용자호출(3,(uintptr_t)ΔΙΑΔΡΟΜΗ,μέθοδος_λειτουργία,0,0,0,0)); }
입출력결과형 파일자료읽기(int Αρχείο,void *δεδομένα,size_t 개수) { return 결과검사(사용자호출(2,Αρχείο,(uintptr_t)δεδομένα,개수,0,0,0)); }
입출력결과형 εγγράφω_Αρχείο_δεδομένα(int Αρχείο,const void *δεδομένα,size_t 개수) { return 결과검사(사용자호출(1,Αρχείο,(uintptr_t)δεδομένα,개수,0,0,0)); }
int κλείνω_Αρχείο(int Αρχείο) { return 결과검사(사용자호출(4,Αρχείο,0,0,0,0,0)); }
Αρχείο_Υπέρθεση_Τύπος αναζητώ_Αρχείο(int Αρχείο,Αρχείο_Υπέρθεση_Τύπος 거리,int έργο_ρίζα) { return 결과검사(사용자호출(5,Αρχείο,거리,έργο_ρίζα,0,0,0)); }
int καταργώ_Αρχείο_καταχώρηση_όνομα(const char *ΔΙΑΔΡΟΜΗ) { return 결과검사(사용자호출(11,(uintptr_t)ΔΙΑΔΡΟΜΗ,0,0,0,0,0)); }
int σύνολο_Αρχείο_διάρκεια(int Αρχείο,Αρχείο_Υπέρθεση_Τύπος Μέγεθος) { return 결과검사(사용자호출(10,Αρχείο,Μέγεθος,0,0,0,0)); }
int δέσμευση_Αρχεία(int Αρχείο) { return 결과검사(사용자호출(12,Αρχείο,0,0,0,0,0)); }
int μέγεθος_αρχείου(int Αρχείο) { return 결과검사(사용자호출(9,Αρχείο,0,0,0,0,0)); }
