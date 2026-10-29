#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ(int);
int ຜູ້ໃຊ້_ເລີ່ມ(int 전달값) {
    for (초기화함수 *ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ = __init_array_start; ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ < __init_array_end; ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ++) (*ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ)();
    int ມາດຕະການ = ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ(전달값);
    for (초기화함수 *ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ = __fini_array_end; ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ != __fini_array_start;) (*--ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ)();
    return ມາດຕະການ;
}
void *memset(void *ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ, int ຄ່າ, size_t 항목수) { unsigned char *ປາຍທາງ_ຂໍ້ມູນ = ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ; while (항목수--) *ປາຍທາງ_ຂໍ້ມູນ++ = ຄ່າ; return ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ; }
void *memcpy(void *ປາຍທາງ_ຂໍ້ມູນ, const void *ສະຕຣິງ_ຂໍ້ມູນ, size_t 항목수) { unsigned char *첫째값 = ປາຍທາງ_ຂໍ້ມູນ; const unsigned char *둘째값 = ສະຕຣິງ_ຂໍ້ມູນ; while (항목수--) *첫째값++ = *둘째값++; return ປາຍທາງ_ຂໍ້ມູນ; }
