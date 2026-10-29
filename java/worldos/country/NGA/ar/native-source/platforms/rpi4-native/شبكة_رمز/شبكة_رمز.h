#ifndef أصلي_شبكة_عنوان
#define أصلي_شبكة_عنوان
#include <stdint.h>
#include <stddef.h>
void إعداد_شبكة(void);
void 통신망살피기(void);
int فتح_مأخذ_التوصيل_المشارك(int نوع_فئة);
int صافي_يربط(int ملف_مؤشر, uint32_t عنوان, unsigned رقم_المنفذ);
int صافي_انصات(int ملف_مؤشر);
void 통신주소재사용(int ملف_مؤشر);
int صافي_يتصل(int ملف_مؤشر, uint32_t عنوان, unsigned رقم_المنفذ);
int صافي_قبول(int ملف_مؤشر);
int صافي_يقرأ(int ملف_مؤشر, void *بيانات, unsigned 개수);
int صافي_كتابة(int ملف_مؤشر, const void *بيانات, unsigned 개수);
int يرسل_مخطط_بيانات(int ملف_مؤشر, const void *بيانات, unsigned 개수, uint32_t عنوان, unsigned رقم_المنفذ);
int يستلم_مخطط_بيانات(int ملف_مؤشر, void *بيانات, unsigned 개수);
unsigned شبكة_رقم_المنفذ(int ملف_مؤشر);
unsigned نظير_رقم_المنفذ(int ملف_مؤشر);
uint32_t صافي_نظير_عنوان(int ملف_مؤشر);
void يغلق_شبكة(int ملف_مؤشر);
int نقل_الملفات_تحكم(int إجراء);
void 파일전송살피기(void);
uint32_t يقرأ_شبكة_توفر(unsigned إدخال_قيمة_962f286b, unsigned فهرس);
int يكوّن_شبكة(unsigned إجراء, uint32_t عنوان, uint32_t قناع_قيمة, uint32_t بوابة_قيمة);
int بدء_رد_يختبر(uint32_t عنوان, unsigned أمر_قيمة);
int يقرأ_رد_يختبر(unsigned إدخال_قيمة_962f286b);
#endif
