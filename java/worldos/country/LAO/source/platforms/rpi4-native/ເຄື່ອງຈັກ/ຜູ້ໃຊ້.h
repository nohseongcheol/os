#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ຜູ້ໃຊ້_ຮູບ_ຈົບ 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ຜູ້ໃຊ້_ກຸ່ມບັດ_ອີເມວ 0x02f00000ul
#define ຜູ້ໃຊ້_ຈົບ 0x03000000ul
#define 사용자쪽수 ((ຜູ້ໃຊ້_ຈົບ - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ຜູ້ໃຊ້_ຂໍ້ມູນ_ຂໍ້ຜິດພາດ (-1001)
#define 사용자실행오류 (-1002)
#define ຜູ້ໃຊ້_ໃຊ້ບໍ່ໄດ້_ຄໍາແນະນໍາ (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t ລົງທະບຽນ_ຂໍ້ມູນ[31], ຄໍາສັ່ງ_ຈັດຕໍາແຫນ່ງ, ສະຖານະ_ລະຫັດ, ກຸ່ມບັດ_ອີເມວ; } ຜູ້ໃຊ້_ກອບ;
void 사용자체계준비(void);
int ຜູ້ໃຊ້_ຂໍ້ຍົກເວັ້ນ(ຜູ້ໃຊ້_ກອບ *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ກະດານ_ຜູ້ໃຊ້_ແລ່ນ(uintptr_t);
uintptr_t ກະດານ_ຜູ້ໃຊ້_ຮັບ_ຮອງ(void);
uintptr_t ກະດານ_ຕົວຄວບຄຸມຜູ້ໃຊ້(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
