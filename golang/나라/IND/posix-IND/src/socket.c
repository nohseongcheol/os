/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <संचार_पता_परिवर्तन/अष्टक_क्रम.h>
#include <प्रणाली/syscall.h>
#include <प्रणाली/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_संचार_छोर_बनाना = 1, SC_स्थानीय_पता_बाँधना = 2, SC_दूसरे_छोर_से_जुड़ना = 3, SC_जुड़ाव_अनुरोध_के_लिए_तैयार_होना = 4,
    SC_जुड़ाव_स्वीकार_करना = 5, SC_स्थानीय_छोर_पता_पाना = 6, SC_दूसरे_छोर_का_पता_पाना = 7,
    SC_भेजना = 9, SC_प्राप्त_करना = 10, SC_गंतव्य_पर_भेजना = 11, SC_प्रेषक_पते_सहित_प्राप्त_करना = 12,
    SC_संचार_दिशा_बंद_करना = 13, SC_संचार_छोर_विकल्प_निर्धारित_करना = 14
};

static long socket_call(long call, unsigned long *तर्क_सूची)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)तर्क_सूची, 0, 0, 0, 0));
}

uint16_t _16_अंकों_को_संजाल_क्रम_में_बदलना(uint16_t मान) { return (uint16_t)((मान << 8) | (मान >> 8)); }
uint16_t _16_अंकों_को_यंत्र_क्रम_में_बदलना(uint16_t मान) { return _16_अंकों_को_संजाल_क्रम_में_बदलना(मान); }
uint32_t _32_अंकों_को_संजाल_क्रम_में_बदलना(uint32_t मान)
{
    return ((मान & 0x000000ffU) << 24) | ((मान & 0x0000ff00U) << 8) |
           ((मान & 0x00ff0000U) >> 8) | ((मान & 0xff000000U) >> 24);
}
uint32_t _32_अंकों_को_यंत्र_क्रम_में_बदलना(uint32_t मान) { return _32_अंकों_को_संजाल_क्रम_में_बदलना(मान); }

int संचार_छोर_बनाना(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_संचार_छोर_बनाना, a);
}

int स्थानीय_पता_बाँधना(int संचिका_विवरणक, const struct संचार_छोर_पता *address, पता_लंबाई_प्रकार लंबाई)
{
    unsigned long a[3] = {(unsigned long)संचिका_विवरणक, (unsigned long)address, लंबाई};
    return (int)socket_call(SC_स्थानीय_पता_बाँधना, a);
}

int दूसरे_छोर_से_जुड़ना(int संचिका_विवरणक, const struct संचार_छोर_पता *address, पता_लंबाई_प्रकार लंबाई)
{
    unsigned long a[3] = {(unsigned long)संचिका_विवरणक, (unsigned long)address, लंबाई};
    return (int)socket_call(SC_दूसरे_छोर_से_जुड़ना, a);
}

int जुड़ाव_अनुरोध_के_लिए_तैयार_होना(int संचिका_विवरणक, int backlog)
{
    unsigned long a[2] = {(unsigned long)संचिका_विवरणक, (unsigned long)backlog};
    return (int)socket_call(SC_जुड़ाव_अनुरोध_के_लिए_तैयार_होना, a);
}

int जुड़ाव_स्वीकार_करना(int संचिका_विवरणक, struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *लंबाई)
{
    unsigned long a[3] = {(unsigned long)संचिका_विवरणक, (unsigned long)address, (unsigned long)लंबाई};
    return (int)socket_call(SC_जुड़ाव_स्वीकार_करना, a);
}

int स्थानीय_छोर_पता_पाना(int संचिका_विवरणक, struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *लंबाई)
{
    unsigned long a[3] = {(unsigned long)संचिका_विवरणक, (unsigned long)address, (unsigned long)लंबाई};
    return (int)socket_call(SC_स्थानीय_छोर_पता_पाना, a);
}

int दूसरे_छोर_का_पता_पाना(int संचिका_विवरणक, struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *लंबाई)
{
    unsigned long a[3] = {(unsigned long)संचिका_विवरणक, (unsigned long)address, (unsigned long)लंबाई};
    return (int)socket_call(SC_दूसरे_छोर_का_पता_पाना, a);
}

ssize_t भेजना(int संचिका_विवरणक, const void *स्थानांतरण_का_अस्थायी_भंडार_2, size_t लंबाई, int flags)
{
    unsigned long a[4] = {(unsigned long)संचिका_विवरणक, (unsigned long)स्थानांतरण_का_अस्थायी_भंडार_2, लंबाई, (unsigned long)flags};
    return (ssize_t)socket_call(SC_भेजना, a);
}

ssize_t प्राप्त_करना(int संचिका_विवरणक, void *स्थानांतरण_का_अस्थायी_भंडार_2, size_t लंबाई, int flags)
{
    unsigned long a[4] = {(unsigned long)संचिका_विवरणक, (unsigned long)स्थानांतरण_का_अस्थायी_भंडार_2, लंबाई, (unsigned long)flags};
    return (ssize_t)socket_call(SC_प्राप्त_करना, a);
}

ssize_t गंतव्य_पर_भेजना(int संचिका_विवरणक, const void *स्थानांतरण_का_अस्थायी_भंडार_2, size_t लंबाई, int flags,
               const struct संचार_छोर_पता *address, पता_लंबाई_प्रकार address_length)
{
    unsigned long a[6] = {(unsigned long)संचिका_विवरणक, (unsigned long)स्थानांतरण_का_अस्थायी_भंडार_2, लंबाई,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_गंतव्य_पर_भेजना, a);
}

ssize_t प्रेषक_पते_सहित_प्राप्त_करना(int संचिका_विवरणक, void *स्थानांतरण_का_अस्थायी_भंडार_2, size_t लंबाई, int flags,
                 struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *address_length)
{
    unsigned long a[6] = {(unsigned long)संचिका_विवरणक, (unsigned long)स्थानांतरण_का_अस्थायी_भंडार_2, लंबाई,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_प्रेषक_पते_सहित_प्राप्त_करना, a);
}

int संचार_दिशा_बंद_करना(int संचिका_विवरणक, int how)
{
    unsigned long a[2] = {(unsigned long)संचिका_विवरणक, (unsigned long)how};
    return (int)socket_call(SC_संचार_दिशा_बंद_करना, a);
}

int संचार_छोर_विकल्प_निर्धारित_करना(int संचिका_विवरणक, int level, int option_name,
               const void *option_value, पता_लंबाई_प्रकार option_len)
{
    unsigned long a[5] = {(unsigned long)संचिका_विवरणक, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_संचार_छोर_विकल्प_निर्धारित_करना, a);
}
