#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t 바이트수형;
typedef int64_t ຟາຍ_ອອບເຊັດ_ພິມ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ຟາຍ_ອອບເຊັດ_ພິມ pk_lseek(int fd, ຟາຍ_ອອບເຊັດ_ພິມ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ຟາຍ_ອອບເຊັດ_ພິມ size);
int pk_fsync(int fd);
int pk_size(int fd);
int ສ້າງ_ຟາຍ(const char *ທາງໂຄຈອນ, int ວິ_ທີ_ໂຫມດ, ...);
입출력결과형 파일자료읽기(int ຟາຍ, void *ຂໍ້ມູນ, size_t 개수);
입출력결과형 ຂຽນ_ຟາຍ_ຂໍ້ມູນ(int ຟາຍ, const void *ຂໍ້ມູນ, size_t 개수);
int ປິດ_ຟາຍ(int ຟາຍ);
ຟາຍ_ອອບເຊັດ_ພິມ ຊອກຫາ_ຟາຍ(int ຟາຍ, ຟາຍ_ອອບເຊັດ_ພິມ 거리, int ໂຄງ_ການ_ເລກຮາກ);
int 파일이름지우기(const char *ທາງໂຄຈອນ);
int ຊຸດ_ຟາຍ_ຄວາມຍາວ(int ຟາຍ, ຟາຍ_ອອບເຊັດ_ພິມ ຂະ_ຫນາດ);
int 파일저장확정(int ຟາຍ);
int ຟາຍ_ຂະ_ຫນາດ(int ຟາຍ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ 0
#define 쓰기전용 1
#define ອ່ານ_ຂຽນ 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
