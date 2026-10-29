#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 בפועל_נתונים RGB32 화면 גודל. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: מוסתר_ערך, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void לוח_מצביע(int 가로, int אנכי_עמדה, unsigned צורה_ערך);
/* 한 번에 32줄을 완성한 הקודם_ערך, 달라진 화소만 בפועל_נתונים 화면에 옮긴다. */
void לוח_להכין_ציור(volatile uint32_t *נתונים, unsigned 폭, unsigned 길이, unsigned מוביל_ערך);
int 보드그림범위(int *가로, int *אנכי_עמדה, int *폭, int *길이);
int לוח_התחל_ציור(int 가로, int אנכי_עמדה, int 폭, int 길이);
void לוח_סיום_ציור(void);
void לוח_מלבן_למלא(int 가로, int אנכי_עמדה, int 폭, int 길이, uint32_t 색);
/* בפועל_נתונים הופעה_ערך 메모리에 기록한 פיקסל 수. מצביע 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned אנכי_עמדה);
#endif
