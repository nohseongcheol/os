#include <تحويل_عناوين_الاتصال/ترتيب_الثمانيات.h>
#include <النظام/syscall.h>
#include <النظام/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_إنشاء_نقطة_اتصال = 1, SC_ربط_عنوان_محلي = 2, SC_الاتصال_بالطرف_المقابل = 3, SC_تهيئة_استقبال_الاتصالات = 4,
    SC_قبول_اتصال = 5, SC_جلب_عنوان_النقطة_المحلية = 6, SC_جلب_عنوان_الطرف_المقابل = 7,
    SC_إرسال = 9, SC_استقبال = 10, SC_إرسال_إلى_وجهة = 11, SC_استقبال_مع_عنوان_المصدر = 12,
    SC_إغلاق_اتجاه_الاتصال = 13, SC_ضبط_خيار_نقطة_الاتصال = 14
};

static long socket_call(long call, unsigned long *المعاملات)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)المعاملات, 0, 0, 0, 0));
}

uint16_t تحويل_16_خانة_إلى_ترتيب_الشبكة(uint16_t القيمة) { return (uint16_t)((القيمة << 8) | (القيمة >> 8)); }
uint16_t تحويل_16_خانة_إلى_ترتيب_الآلة(uint16_t القيمة) { return تحويل_16_خانة_إلى_ترتيب_الشبكة(القيمة); }
uint32_t تحويل_32_خانة_إلى_ترتيب_الشبكة(uint32_t القيمة)
{
    return ((القيمة & 0x000000ffU) << 24) | ((القيمة & 0x0000ff00U) << 8) |
           ((القيمة & 0x00ff0000U) >> 8) | ((القيمة & 0xff000000U) >> 24);
}
uint32_t تحويل_32_خانة_إلى_ترتيب_الآلة(uint32_t القيمة) { return تحويل_32_خانة_إلى_ترتيب_الشبكة(القيمة); }

int إنشاء_نقطة_اتصال(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_إنشاء_نقطة_اتصال, a);
}

int ربط_عنوان_محلي(int واصف_الملف, const struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان الطول)
{
    unsigned long a[3] = {(unsigned long)واصف_الملف, (unsigned long)address, الطول};
    return (int)socket_call(SC_ربط_عنوان_محلي, a);
}

int الاتصال_بالطرف_المقابل(int واصف_الملف, const struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان الطول)
{
    unsigned long a[3] = {(unsigned long)واصف_الملف, (unsigned long)address, الطول};
    return (int)socket_call(SC_الاتصال_بالطرف_المقابل, a);
}

int تهيئة_استقبال_الاتصالات(int واصف_الملف, int backlog)
{
    unsigned long a[2] = {(unsigned long)واصف_الملف, (unsigned long)backlog};
    return (int)socket_call(SC_تهيئة_استقبال_الاتصالات, a);
}

int قبول_اتصال(int واصف_الملف, struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *الطول)
{
    unsigned long a[3] = {(unsigned long)واصف_الملف, (unsigned long)address, (unsigned long)الطول};
    return (int)socket_call(SC_قبول_اتصال, a);
}

int جلب_عنوان_النقطة_المحلية(int واصف_الملف, struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *الطول)
{
    unsigned long a[3] = {(unsigned long)واصف_الملف, (unsigned long)address, (unsigned long)الطول};
    return (int)socket_call(SC_جلب_عنوان_النقطة_المحلية, a);
}

int جلب_عنوان_الطرف_المقابل(int واصف_الملف, struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *الطول)
{
    unsigned long a[3] = {(unsigned long)واصف_الملف, (unsigned long)address, (unsigned long)الطول};
    return (int)socket_call(SC_جلب_عنوان_الطرف_المقابل, a);
}

ssize_t إرسال(int واصف_الملف, const void *مخزن_النقل_المؤقت_2, size_t الطول, int flags)
{
    unsigned long a[4] = {(unsigned long)واصف_الملف, (unsigned long)مخزن_النقل_المؤقت_2, الطول, (unsigned long)flags};
    return (ssize_t)socket_call(SC_إرسال, a);
}

ssize_t استقبال(int واصف_الملف, void *مخزن_النقل_المؤقت_2, size_t الطول, int flags)
{
    unsigned long a[4] = {(unsigned long)واصف_الملف, (unsigned long)مخزن_النقل_المؤقت_2, الطول, (unsigned long)flags};
    return (ssize_t)socket_call(SC_استقبال, a);
}

ssize_t إرسال_إلى_وجهة(int واصف_الملف, const void *مخزن_النقل_المؤقت_2, size_t الطول, int flags,
               const struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان address_length)
{
    unsigned long a[6] = {(unsigned long)واصف_الملف, (unsigned long)مخزن_النقل_المؤقت_2, الطول,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_إرسال_إلى_وجهة, a);
}

ssize_t استقبال_مع_عنوان_المصدر(int واصف_الملف, void *مخزن_النقل_المؤقت_2, size_t الطول, int flags,
                 struct عنوان_نقطة_الاتصال *address, نوع_طول_العنوان *address_length)
{
    unsigned long a[6] = {(unsigned long)واصف_الملف, (unsigned long)مخزن_النقل_المؤقت_2, الطول,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_استقبال_مع_عنوان_المصدر, a);
}

int إغلاق_اتجاه_الاتصال(int واصف_الملف, int how)
{
    unsigned long a[2] = {(unsigned long)واصف_الملف, (unsigned long)how};
    return (int)socket_call(SC_إغلاق_اتجاه_الاتصال, a);
}

int ضبط_خيار_نقطة_الاتصال(int واصف_الملف, int level, int option_name,
               const void *option_value, نوع_طول_العنوان option_len)
{
    unsigned long a[5] = {(unsigned long)واصف_الملف, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_ضبط_خيار_نقطة_الاتصال, a);
}
