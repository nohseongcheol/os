#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 वास्तविक_डेटा RGB32 화면 आकार. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: छुपा_हुआ_मान, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void बोर्ड_सूचक(int 가로, int अनुलंब_पद, unsigned आकृति_मान);
/* 한 번에 32줄을 완성한 वापस_मान, 달라진 화소만 वास्तविक_डेटा 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *आँकड़े, unsigned 폭, unsigned 길이, unsigned लीडिंग_मान);
int 보드그림범위(int *가로, int *अनुलंब_पद, int *폭, int *길이);
int बोर्ड_प्रारंभ_ड्रॉइंग(int 가로, int अनुलंब_पद, int 폭, int 길이);
void बोर्ड_पूर्ण_ड्रॉइंग(void);
void बोर्ड_रेक्_टेंगल_भरण(int 가로, int अनुलंब_पद, int 폭, int 길이, uint32_t 색);
/* वास्तविक_डेटा शो_मान 메모리에 기록한 पिक्सेल 수. सूचक 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned अनुलंब_पद);
#endif
