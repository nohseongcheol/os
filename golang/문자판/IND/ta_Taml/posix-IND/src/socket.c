/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <தொடர்பு_முகவரி_மாற்றம்/எட்டு_இரும_இலக்கக்_குழு_வரிசை.h>
#include <அமைப்பு/syscall.h>
#include <அமைப்பு/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_தொடர்பு_முனையை_உருவாக்கு = 1, SC_உள்ளக_முகவரியைப்_பிணை = 2, SC_எதிர்_முனையுடன்_இணை = 3, SC_இணைப்புகளை_ஏற்கத்_தயாராகு = 4,
    SC_இணைப்பை_ஏற்றுக்கொள் = 5, SC_உள்ளக_முனையின்_முகவரியைப்_பெறு = 6, SC_எதிர்_முனையின்_முகவரியைப்_பெறு = 7,
    SC_அனுப்பு = 9, SC_பெறு = 10, SC_இலக்கிற்கு_அனுப்பு = 11, SC_அனுப்பிய_முகவரியுடன்_பெறு = 12,
    SC_தொடர்புத்_திசையை_மூடு = 13, SC_தொடர்பு_முனையின்_விருப்பத்தை_அமை = 14
};

static long socket_call(long call, unsigned long *செயலுருபுகள்)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)செயலுருபுகள், 0, 0, 0, 0));
}

uint16_t _16_இரும_இலக்கங்களை_வலை_வரிசைக்கு_மாற்று(uint16_t மதிப்பு) { return (uint16_t)((மதிப்பு << 8) | (மதிப்பு >> 8)); }
uint16_t _16_இரும_இலக்கங்களைப்_பொறி_வரிசைக்கு_மாற்று(uint16_t மதிப்பு) { return _16_இரும_இலக்கங்களை_வலை_வரிசைக்கு_மாற்று(மதிப்பு); }
uint32_t _32_இரும_இலக்கங்களை_வலை_வரிசைக்கு_மாற்று(uint32_t மதிப்பு)
{
    return ((மதிப்பு & 0x000000ffU) << 24) | ((மதிப்பு & 0x0000ff00U) << 8) |
           ((மதிப்பு & 0x00ff0000U) >> 8) | ((மதிப்பு & 0xff000000U) >> 24);
}
uint32_t _32_இரும_இலக்கங்களைப்_பொறி_வரிசைக்கு_மாற்று(uint32_t மதிப்பு) { return _32_இரும_இலக்கங்களை_வலை_வரிசைக்கு_மாற்று(மதிப்பு); }

int தொடர்பு_முனையை_உருவாக்கு(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_தொடர்பு_முனையை_உருவாக்கு, a);
}

int உள்ளக_முகவரியைப்_பிணை(int கோப்பு_விவரிப்பி, const struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை நீளம்)
{
    unsigned long a[3] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)address, நீளம்};
    return (int)socket_call(SC_உள்ளக_முகவரியைப்_பிணை, a);
}

int எதிர்_முனையுடன்_இணை(int கோப்பு_விவரிப்பி, const struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை நீளம்)
{
    unsigned long a[3] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)address, நீளம்};
    return (int)socket_call(SC_எதிர்_முனையுடன்_இணை, a);
}

int இணைப்புகளை_ஏற்கத்_தயாராகு(int கோப்பு_விவரிப்பி, int backlog)
{
    unsigned long a[2] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)backlog};
    return (int)socket_call(SC_இணைப்புகளை_ஏற்கத்_தயாராகு, a);
}

int இணைப்பை_ஏற்றுக்கொள்(int கோப்பு_விவரிப்பி, struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *நீளம்)
{
    unsigned long a[3] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)address, (unsigned long)நீளம்};
    return (int)socket_call(SC_இணைப்பை_ஏற்றுக்கொள், a);
}

int உள்ளக_முனையின்_முகவரியைப்_பெறு(int கோப்பு_விவரிப்பி, struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *நீளம்)
{
    unsigned long a[3] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)address, (unsigned long)நீளம்};
    return (int)socket_call(SC_உள்ளக_முனையின்_முகவரியைப்_பெறு, a);
}

int எதிர்_முனையின்_முகவரியைப்_பெறு(int கோப்பு_விவரிப்பி, struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *நீளம்)
{
    unsigned long a[3] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)address, (unsigned long)நீளம்};
    return (int)socket_call(SC_எதிர்_முனையின்_முகவரியைப்_பெறு, a);
}

ssize_t அனுப்பு(int கோப்பு_விவரிப்பி, const void *பரிமாற்ற_இடையகம்_2, size_t நீளம், int flags)
{
    unsigned long a[4] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)பரிமாற்ற_இடையகம்_2, நீளம், (unsigned long)flags};
    return (ssize_t)socket_call(SC_அனுப்பு, a);
}

ssize_t பெறு(int கோப்பு_விவரிப்பி, void *பரிமாற்ற_இடையகம்_2, size_t நீளம், int flags)
{
    unsigned long a[4] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)பரிமாற்ற_இடையகம்_2, நீளம், (unsigned long)flags};
    return (ssize_t)socket_call(SC_பெறு, a);
}

ssize_t இலக்கிற்கு_அனுப்பு(int கோப்பு_விவரிப்பி, const void *பரிமாற்ற_இடையகம்_2, size_t நீளம், int flags,
               const struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை address_length)
{
    unsigned long a[6] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)பரிமாற்ற_இடையகம்_2, நீளம்,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_இலக்கிற்கு_அனுப்பு, a);
}

ssize_t அனுப்பிய_முகவரியுடன்_பெறு(int கோப்பு_விவரிப்பி, void *பரிமாற்ற_இடையகம்_2, size_t நீளம், int flags,
                 struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *address_length)
{
    unsigned long a[6] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)பரிமாற்ற_இடையகம்_2, நீளம்,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_அனுப்பிய_முகவரியுடன்_பெறு, a);
}

int தொடர்புத்_திசையை_மூடு(int கோப்பு_விவரிப்பி, int how)
{
    unsigned long a[2] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)how};
    return (int)socket_call(SC_தொடர்புத்_திசையை_மூடு, a);
}

int தொடர்பு_முனையின்_விருப்பத்தை_அமை(int கோப்பு_விவரிப்பி, int level, int option_name,
               const void *option_value, முகவரி_நீள_வகை option_len)
{
    unsigned long a[5] = {(unsigned long)கோப்பு_விவரிப்பி, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_தொடர்பு_முனையின்_விருப்பத்தை_அமை, a);
}
