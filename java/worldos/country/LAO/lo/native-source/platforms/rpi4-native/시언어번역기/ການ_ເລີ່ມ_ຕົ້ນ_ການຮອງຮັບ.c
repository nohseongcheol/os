#include "../명명/기계연결이름.h"
#include "호출.h"
extern int main(int,char **);
static char ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[8][256];
int ຜູ້ໃຊ້_ເລີ່ມ(int 미사용값){
    (void)미사용값;char *ຂໍ້ພິສູດ_ລາຍຊື່[9];int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수<0||인수개수>8)return 126;
    for(int 순번=0;순번<인수개수;순번++){if(사용자호출(15,순번,(uintptr_t)ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[순번],256,0,0,0)<0)return 126;ຂໍ້ພິສູດ_ລາຍຊື່[순번]=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ[순번];}ຂໍ້ພິສູດ_ລາຍຊື່[인수개수]=0;
    return main(인수개수,ຂໍ້ພິສູດ_ລາຍຊື່);
}
void *memset(void*ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ,int ຈຸດ_ລະ_ຫັດ,size_t 개수){unsigned char*ປາຍທາງ_ຂໍ້ມູນ=ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ;while(개수--)*ປາຍທາງ_ຂໍ້ມູນ++=ຈຸດ_ລະ_ຫັດ;return ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ;}
void *memcpy(void*ປາຍທາງ_ຂໍ້ມູນ,const void*ສະຕຣິງ_ຂໍ້ມູນ,size_t 개수){unsigned char*첫째값=ປາຍທາງ_ຂໍ້ມູນ;const unsigned char*둘째값=ສະຕຣິງ_ຂໍ້ມູນ;while(개수--)*첫째값++=*둘째값++;return ປາຍທາງ_ຂໍ້ມູນ;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned ຈຸດ_ພິ_ກັດ_x,unsigned ປຸ່ມ_Y_ຈຸດປະສານ,unsigned 너비,unsigned 높이,unsigned 색상){return 화면사각형(ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ,너비,높이,색상);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return 사용자호출(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return 화면키기다리기();}
int 네모그리기(unsigned 가로,unsigned ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ,unsigned 너비,unsigned 높이,unsigned 색상){return pk_rectangle(가로,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ,너비,높이,색상);}
unsigned 밀리초(void){return pk_ticks_ms();}
int 그림기다리기(void){return pk_graphics_wait();}
int 화면너비(void){return 화면너비읽기();}
int 화면높이(void){return 화면높이읽기();}
