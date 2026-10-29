#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 තථ්_ය_දත්ත RGB32 화면 ප්_රමාණය. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: සැඟවුණු_අගය, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 보드포인터(int 가로, int 세로, unsigned හැඩය_අගය);
/* 한 번에 32줄을 완성한 ආපසු_අගය, 달라진 화소만 තථ්_ය_දත්ත 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *දත්ත, unsigned 폭, unsigned දිග_අගය, unsigned පේළි_පරතරය_අගය);
int 보드그림범위(int *가로, int *세로, int *폭, int *දිග_අගය);
int 보드그림시작(int 가로, int 세로, int 폭, int දිග_අගය);
void 보드그림마침(void);
void 보드사각그림(int 가로, int 세로, int 폭, int දිග_අගය, uint32_t 색);
/* තථ්_ය_දත්ත දර්ශනය_අගය 메모리에 기록한 පික්සලය 수. පොයින්ටරය 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned 세로);
#endif
