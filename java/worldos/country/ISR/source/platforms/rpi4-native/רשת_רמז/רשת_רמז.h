#ifndef מקורי_רשת_כותרת
#define מקורי_רשת_כותרת
#include <stdint.h>
#include <stddef.h>
void להכין_רשת(void);
void 통신망살피기(void);
int 통신끝점만들기(int כתב_אזור);
int נטו_לאגד(int קובץ_נקודת_אחיזה, uint32_t למען, unsigned מספר_יציאה);
int נטו_להאזין(int קובץ_נקודת_אחיזה);
void 통신주소재사용(int קובץ_נקודת_אחיזה);
int נטו_לקשר(int קובץ_נקודת_אחיזה, uint32_t למען, unsigned מספר_יציאה);
int נטו_לקבל(int קובץ_נקודת_אחיזה);
int 통신읽기(int קובץ_נקודת_אחיזה, void *נתונים, unsigned 개수);
int נטו_כתיבה(int קובץ_נקודת_אחיזה, const void *נתונים, unsigned 개수);
int שלח_יחידת_נתונים(int קובץ_נקודת_אחיזה, const void *נתונים, unsigned 개수, uint32_t למען, unsigned מספר_יציאה);
int לקבל_יחידת_נתונים(int קובץ_נקודת_אחיזה, void *נתונים, unsigned 개수);
unsigned רשת_מספר_יציאה(int קובץ_נקודת_אחיזה);
unsigned עמית_מספר_יציאה(int קובץ_נקודת_אחיזה);
uint32_t נטו_עמית_למען(int קובץ_נקודת_אחיזה);
void סגור_רשת(int קובץ_נקודת_אחיזה);
int העברת_קבצים_פקד(int פעולה);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ערך_ערך, unsigned מדד);
int הגדר_רשת(unsigned פעולה, uint32_t למען, uint32_t מסיכה_ערך, uint32_t שער_ערך);
int התחל_תגובה_נסה(uint32_t למען, unsigned סדר_ערך);
int 응답시험읽기(unsigned ערך_ערך);
#endif
