#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void ກະ_ກຽມ_ເຄືອຂ່າຍ(void);
void 통신망살피기(void);
int 통신끝점만들기(int ພິມ_ຫມວດ);
int 망주소묶기(int ຟາຍ_ຈັດ_ການ, uint32_t ອີເມວ, unsigned ຫມາຍເລກພອດ);
int 연결기다리기(int ຟາຍ_ຈັດ_ການ);
void 통신주소재사용(int ຟາຍ_ຈັດ_ການ);
int 망연결하기(int ຟາຍ_ຈັດ_ການ, uint32_t ອີເມວ, unsigned ຫມາຍເລກພອດ);
int 망연결받기(int ຟາຍ_ຈັດ_ການ);
int 통신읽기(int ຟາຍ_ຈັດ_ການ, void *ຂໍ້ມູນ, unsigned 개수);
int 통신쓰기(int ຟາຍ_ຈັດ_ການ, const void *ຂໍ້ມູນ, unsigned 개수);
int 전문보내기(int ຟາຍ_ຈັດ_ການ, const void *ຂໍ້ມູນ, unsigned 개수, uint32_t ອີເມວ, unsigned ຫມາຍເລກພອດ);
int 전문받기(int ຟາຍ_ຈັດ_ການ, void *ຂໍ້ມູນ, unsigned 개수);
unsigned ເຄືອຂ່າຍ_ຫມາຍເລກພອດ(int ຟາຍ_ຈັດ_ການ);
unsigned ລຸ້ນດຽວກັນ_ຫມາຍເລກພອດ(int ຟາຍ_ຈັດ_ການ);
uint32_t 상대통신주소(int ຟາຍ_ຈັດ_ການ);
void ປິດ_ເຄືອຂ່າຍ(int ຟາຍ_ຈັດ_ການ);
int ຟາຍ_ໂອນ_ຄວບຄຸມ(int ຄໍາສັ່ງ);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ເຂົ້າໃນ_ຄ່າ, unsigned ດັດຊະນີ);
int ຕັ້ງຄ່າ_ເຄືອຂ່າຍ(unsigned ຄໍາສັ່ງ, uint32_t ອີເມວ, uint32_t ຫນ້າກາກ_ຄ່າ, uint32_t ເກດເວ_ຄ່າ);
int 응답시험시작(uint32_t ອີເມວ, unsigned ລໍາດັບ_ຄ່າ);
int 응답시험읽기(unsigned ເຂົ້າໃນ_ຄ່າ);
#endif
