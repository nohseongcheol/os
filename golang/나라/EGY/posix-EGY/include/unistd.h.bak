#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <التعريفات_الأساسية.h>
#include <النظام/أنواع_البيانات.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void إنهاء_فوري(int الحالة) __attribute__((noreturn));
ssize_t قراءة(int واصف_الملف, void *مخزن_النقل_المؤقت, size_t count);
ssize_t كتابة(int واصف_الملف, const void *مخزن_النقل_المؤقت, size_t count);
int إغلاق(int واصف_الملف);
off_t نقل_موضع_الملف(int واصف_الملف, off_t offset, int whence);
pid_t إنشاء_عملية_فرعية(void);
int استبدال_البرنامج_الجاري(const char *المسار, char *const المعاملات_2[], char *const envp[]);
pid_t جلب_معرف_العملية(void);
pid_t جلب_معرف_العملية_الأم(void);
uid_t جلب_معرف_المستخدم(void);
uid_t جلب_معرف_المستخدم_الفعلي(void);
gid_t جلب_معرف_المجموعة(void);
gid_t جلب_معرف_المجموعة_الفعلي(void);
int فحص_صلاحيات_الوصول(const char *المسار, int mode);
int تغيير_دليل_العمل(const char *المسار);
char *جلب_مسار_دليل_العمل(char *مخزن_النقل_المؤقت, size_t عدد_الخانات);
int نسخ_مرجع_الملف_المفتوح(int واصف_الملف);
int نسخ_مرجع_الملف_إلى_رقم_محدد(int oldfd, int newfd);
int مزامنة_بيانات_الملف(int واصف_الملف);
void مزامنة_جميع_البيانات(void);
int فحص_كون_الوصف_طرفية(int واصف_الملف);
int تعيين_نهاية_الذاكرة_المتغيرة(void *address);
void *نقل_نهاية_الذاكرة_المتغيرة(int increment);
#ifdef __cplusplus
}
#endif

#endif
