#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 الفعلي_بيانات RGB32 화면 حجم. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: مخفية_قيمة, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void لوحة_مؤشر(int 가로, int عمودي_منصب, unsigned شكل_قيمة);
/* 한 번에 32줄을 완성한 عودة_قيمة, 달라진 화소만 الفعلي_بيانات 화면에 옮긴다. */
void لوحة_إعداد_رسم(volatile uint32_t *بيانات, unsigned 폭, unsigned 길이, unsigned بادئة_قيمة);
int 보드그림범위(int *가로, int *عمودي_منصب, int *폭, int *길이);
int لوحة_بدء_رسم(int 가로, int عمودي_منصب, int 폭, int 길이);
void لوحة_إنهاء_رسم(void);
void لوحة_مستطيل_يملأ(int 가로, int عمودي_منصب, int 폭, int 길이, uint32_t 색);
/* الفعلي_بيانات عرض_قيمة_487749b8 메모리에 기록한 عنصر_صورة رقم. مؤشر 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned عمودي_منصب);
#endif
