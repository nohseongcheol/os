// 동일 ไทย 헤더를 사용하는 별도 EL0 ไลบรารี. เคอร์เนล_ค่า 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int รหัสข้อผิดพลาด;
int *pk_errno_location(void) { return &รหัสข้อผิดพลาด; }
static intptr_t 결과검사(intptr_t ผลลัพธ์) { if (ผลลัพธ์ < 0) { รหัสข้อผิดพลาด = -ผลลัพธ์; return -1; } return ผลลัพธ์; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
แฟ้ม_ออฟเซต_ชนิด pk_lseek(int fd, แฟ้ม_ออฟเซต_ชนิด offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, แฟ้ม_ออฟเซต_ชนิด size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* ไทย 공개 함수의 ค่าจริง_ข้อมูล EL0 구현. 구조체는 SVC에서 คัดลอก_ค่า·검증한다. */
int เปิด_ปลายทาง(int อีเมล_กลุ่ม,int 통신방식,int โอน_โพรโทคอล) {
    return 결과검사(사용자호출(32,อีเมล_กลุ่ม,통신방식,โอน_โพรโทคอล,0,0,0));
}
int ผูก_อีเมล(int ปลายทาง,const struct 통신주소 *อีเมล,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,ปลายทาง,(uintptr_t)อีเมล,길이,0,0,0));
}
intptr_t ส่ง_เดตาแกรม_ข้อมูล(int ปลายทาง,const void *ข้อมูล,size_t 개수,int การเลือก_ค่า,const struct 통신주소 *อีเมล,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,ปลายทาง,(uintptr_t)ข้อมูล,개수,การเลือก_ค่า,(uintptr_t)อีเมล,길이));
}
intptr_t รับ_เดตาแกรม_ข้อมูล(int ปลายทาง,void *ข้อมูล,size_t 개수,int การเลือก_ค่า,struct 통신주소 *อีเมล,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,ปลายทาง,(uintptr_t)ข้อมูล,개수,การเลือก_ค่า,(uintptr_t)อีเมล,(uintptr_t)길이));
}
int 통신주소읽기(int ปลายทาง,struct 통신주소 *อีเมล,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,ปลายทาง,(uintptr_t)อีเมล,(uintptr_t)길이,0,0,0));
}
int เชื่อมต่อ_เครือข่าย(int ปลายทาง,const struct 통신주소 *อีเมล,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,ปลายทาง,(uintptr_t)อีเมล,길이,0,0,0));
}
int 통신연결기다리기(int ปลายทาง,int 대기수) {
    return 결과검사(사용자호출(38,ปลายทาง,대기수,0,0,0,0));
}
int ยอมรับ_การเชื่อมต่อเครือข่าย(int ปลายทาง,struct 통신주소 *อีเมล,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,ปลายทาง,(uintptr_t)อีเมล,(uintptr_t)길이,0,0,0));
}

/* แฟ้ม 함수도 독립된 ไทย ฟังก์ชัน_ค่า 심볼로 제공한다. */
int เปิด_แฟ้ม(const char *เส้นทาง,int เมธอด_โหมด,...) { return 결과검사(사용자호출(3,(uintptr_t)เส้นทาง,เมธอด_โหมด,0,0,0,0)); }
입출력결과형 파일자료읽기(int แฟ้ม,void *ข้อมูล,size_t 개수) { return 결과검사(사용자호출(2,แฟ้ม,(uintptr_t)ข้อมูล,개수,0,0,0)); }
입출력결과형 파일자료쓰기(int แฟ้ม,const void *ข้อมูล,size_t 개수) { return 결과검사(사용자호출(1,แฟ้ม,(uintptr_t)ข้อมูล,개수,0,0,0)); }
int ปิด_แฟ้ม(int แฟ้ม) { return 결과검사(사용자호출(4,แฟ้ม,0,0,0,0,0)); }
แฟ้ม_ออฟเซต_ชนิด กรอ_แฟ้ม(int แฟ้ม,แฟ้ม_ออฟเซต_ชนิด 거리,int แสดง_ราก) { return 결과검사(사용자호출(5,แฟ้ม,거리,แสดง_ราก,0,0,0)); }
int นําออก_แฟ้ม_รายการ_ชื่อ(const char *เส้นทาง) { return 결과검사(사용자호출(11,(uintptr_t)เส้นทาง,0,0,0,0,0)); }
int 파일길이정하기(int แฟ้ม,แฟ้ม_ออฟเซต_ชนิด ขนาด) { return 결과검사(사용자호출(10,แฟ้ม,ขนาด,0,0,0,0)); }
int 파일저장확정(int แฟ้ม) { return 결과검사(사용자호출(12,แฟ้ม,0,0,0,0,0)); }
int ขนาดแฟ้ม(int แฟ้ม) { return 결과검사(사용자호출(9,แฟ้ม,0,0,0,0,0)); }
