/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_النظام_socket
#define _include_النظام_socket

#include <التعريفات_الأساسية.h>
#include <النظام/أنواع_البيانات.h>

typedef unsigned short نوع_عائلة_العناوين;

struct عنوان_نقطة_الاتصال {
    نوع_عائلة_العناوين عائلة_عناوين_نقطة_الاتصال;
    char بيانات_العنوان[14];
};

#define عائلة_عناوين_غير_محددة 0
#define رمز_عائلة_عناوين_الشبكات_المترابطة 2
#define عائلة_بروتوكولات_الشبكات_المترابطة رمز_عائلة_عناوين_الشبكات_المترابطة

#define نقطة_تدفق_البيانات 1
#define نقطة_رزم_البيانات 2

#define إيقاف_الاستقبال 0
#define إيقاف_الإرسال 1
#define إيقاف_الاتجاهين 2

#ifdef __cplusplus
extern "C" {
#endif
int إنشاء_نقطة_اتصال(int domain, int type, int protocol);
int ربط_عنوان_محلي(int واصف_الملف, const struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان address_len);
int الاتصال_بالطرف_المقابل(int واصف_الملف, const struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان address_len);
int تهيئة_استقبال_الاتصالات(int واصف_الملف, int backlog);
int قبول_اتصال(int واصف_الملف, struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *address_len);
int جلب_عنوان_النقطة_المحلية(int واصف_الملف, struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *address_len);
int جلب_عنوان_الطرف_المقابل(int واصف_الملف, struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *address_len);
ssize_t إرسال(int واصف_الملف, const void *مخزن_النقل_المؤقت_2, size_t الطول, int flags);
ssize_t استقبال(int واصف_الملف, void *مخزن_النقل_المؤقت_2, size_t الطول, int flags);
ssize_t إرسال_إلى_وجهة(int واصف_الملف, const void *message, size_t الطول, int flags,
               const struct عنوان_نقطة_الاتصال *dest_addr, نوع_طول_العنوان dest_len);
ssize_t استقبال_مع_عنوان_المصدر(int واصف_الملف, void *مخزن_النقل_المؤقت_2, size_t الطول, int flags,
                 struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *address_len);
int إغلاق_اتجاه_الاتصال(int واصف_الملف, int how);
int ضبط_خيار_نقطة_الاتصال(int واصف_الملف, int level, int option_name,
               const void *option_value, نوع_طول_العنوان option_len);
#ifdef __cplusplus
}
#endif

#endif
