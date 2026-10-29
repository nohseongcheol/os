#ifndef ดั้งเดิม_แบบผ่านสาย_เครือข่าย_ส่วนหัว
#define ดั้งเดิม_แบบผ่านสาย_เครือข่าย_ส่วนหัว
#include "lwip/netif.h"
int 유선장치있음(void);
err_t จัดเตรียม_แบบผ่านสาย_เครือข่าย(struct netif *);
void 유선망살피기(struct netif *);
uint32_t 유선망집계(unsigned);
#endif
