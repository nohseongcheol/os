// 동일 한국어 헤더를 사용하는 별도 EL0 ຫໍສະຫມຸດ. ແກນກາງ_ຄ່າ 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ລະຫັດຂັດຂ້ອງ;
int *pk_errno_location(void) { return &ລະຫັດຂັດຂ້ອງ; }
static intptr_t 결과검사(intptr_t ມາດຕະການ) { if (ມາດຕະການ < 0) { ລະຫັດຂັດຂ້ອງ = -ມາດຕະການ; return -1; } return ມາດຕະການ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ຟາຍ_ອອບເຊັດ_ພິມ pk_lseek(int fd, ຟາຍ_ອອບເຊັດ_ພິມ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ຟາຍ_ອອບເຊັດ_ພິມ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 ຕົວ_ຈິງ_ຂໍ້ມູນ EL0 구현. 구조체는 SVC에서 ກ່າຍ_ຄ່າ·검증한다. */
int 통신종단점만들기(int ອີເມວ_ຄອບຄົວ,int 통신방식,int ໂອນ_ຫຼັກການ) {
    return 결과검사(사용자호출(32,ອີເມວ_ຄອບຄົວ,통신방식,ໂອນ_ຫຼັກການ,0,0,0));
}
int ຜູກ_ມັດ_ອີເມວ(int 종단,const struct 통신주소 *ອີເມວ,통신주소길이형 ຄວາມຍາວ_ຄ່າ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ອີເມວ,ຄວາມຍາວ_ຄ່າ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ຂໍ້ມູນ,size_t 개수,int ການ_ເລືອກ_ຄ່າ,const struct 통신주소 *ອີເມວ,통신주소길이형 ຄວາມຍາວ_ຄ່າ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ຂໍ້ມູນ,개수,ການ_ເລືອກ_ຄ່າ,(uintptr_t)ອີເມວ,ຄວາມຍາວ_ຄ່າ));
}
intptr_t 자료전문받기(int 종단,void *ຂໍ້ມູນ,size_t 개수,int ການ_ເລືອກ_ຄ່າ,struct 통신주소 *ອີເມວ,통신주소길이형 *ຄວາມຍາວ_ຄ່າ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ຂໍ້ມູນ,개수,ການ_ເລືອກ_ຄ່າ,(uintptr_t)ອີເມວ,(uintptr_t)ຄວາມຍາວ_ຄ່າ));
}
int 통신주소읽기(int 종단,struct 통신주소 *ອີເມວ,통신주소길이형 *ຄວາມຍາວ_ຄ່າ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ອີເມວ,(uintptr_t)ຄວາມຍາວ_ຄ່າ,0,0,0));
}
int ເຊື່ອມຕໍ່_ເຄືອຂ່າຍ(int 종단,const struct 통신주소 *ອີເມວ,통신주소길이형 ຄວາມຍາວ_ຄ່າ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ອີເມວ,ຄວາມຍາວ_ຄ່າ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ຕອບຮັບ_ການ_ເຊື່ອມ_ຕໍ່_ເຄືອ_ຂ່າຍ(int 종단,struct 통신주소 *ອີເມວ,통신주소길이형 *ຄວາມຍາວ_ຄ່າ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ອີເມວ,(uintptr_t)ຄວາມຍາວ_ຄ່າ,0,0,0));
}

/* ຟາຍ 함수도 독립된 한국어 ຟັງ_ຄ໌_ຊັນ_ຄ່າ 심볼로 제공한다. */
int ສ້າງ_ຟາຍ(const char *ທາງໂຄຈອນ,int ວິ_ທີ_ໂຫມດ,...) { return 결과검사(사용자호출(3,(uintptr_t)ທາງໂຄຈອນ,ວິ_ທີ_ໂຫມດ,0,0,0,0)); }
입출력결과형 파일자료읽기(int ຟາຍ,void *ຂໍ້ມູນ,size_t 개수) { return 결과검사(사용자호출(2,ຟາຍ,(uintptr_t)ຂໍ້ມູນ,개수,0,0,0)); }
입출력결과형 ຂຽນ_ຟາຍ_ຂໍ້ມູນ(int ຟາຍ,const void *ຂໍ້ມູນ,size_t 개수) { return 결과검사(사용자호출(1,ຟາຍ,(uintptr_t)ຂໍ້ມູນ,개수,0,0,0)); }
int ປິດ_ຟາຍ(int ຟາຍ) { return 결과검사(사용자호출(4,ຟາຍ,0,0,0,0,0)); }
ຟາຍ_ອອບເຊັດ_ພິມ ຊອກຫາ_ຟາຍ(int ຟາຍ,ຟາຍ_ອອບເຊັດ_ພິມ 거리,int ໂຄງ_ການ_ເລກຮາກ) { return 결과검사(사용자호출(5,ຟາຍ,거리,ໂຄງ_ການ_ເລກຮາກ,0,0,0)); }
int 파일이름지우기(const char *ທາງໂຄຈອນ) { return 결과검사(사용자호출(11,(uintptr_t)ທາງໂຄຈອນ,0,0,0,0,0)); }
int ຊຸດ_ຟາຍ_ຄວາມຍາວ(int ຟາຍ,ຟາຍ_ອອບເຊັດ_ພິມ ຂະ_ຫນາດ) { return 결과검사(사용자호출(10,ຟາຍ,ຂະ_ຫນາດ,0,0,0,0)); }
int 파일저장확정(int ຟາຍ) { return 결과검사(사용자호출(12,ຟາຍ,0,0,0,0,0)); }
int ຟາຍ_ຂະ_ຫນາດ(int ຟາຍ) { return 결과검사(사용자호출(9,ຟາຍ,0,0,0,0,0)); }
