#ifndef _include_प्रणाली_socket
#define _include_प्रणाली_socket

#include <मूल_परिभाषाएँ.h>
#include <प्रणाली/आँकड़ा_प्रकार.h>

typedef unsigned short पता_परिवार_प्रकार;

struct संचार_छोर_पता {
    पता_परिवार_प्रकार छोर_पता_परिवार;
    char पता_आँकड़े[14];
};

#define अनिर्दिष्ट_पता_परिवार 0
#define अंतरजाल_पता_परिवार_संकेत 2
#define अंतरजाल_नियम_परिवार अंतरजाल_पता_परिवार_संकेत

#define आँकड़ा_प्रवाह_छोर 1
#define आँकड़ा_संदेश_छोर 2

#define प्राप्ति_रोकें 0
#define प्रेषण_रोकें 1
#define दोनों_दिशाएँ_रोकें 2

#ifdef __cplusplus
extern "C" {
#endif
int संचार_छोर_बनाना(int domain, int type, int protocol);
int स्थानीय_पता_बाँधना(int संचिका_विवरणक, const struct संचार_छोर_पता *address, पता_लंबाई_प्रकार address_len);
int दूसरे_छोर_से_जुड़ना(int संचिका_विवरणक, const struct संचार_छोर_पता *address, पता_लंबाई_प्रकार address_len);
int जुड़ाव_अनुरोध_के_लिए_तैयार_होना(int संचिका_विवरणक, int backlog);
int जुड़ाव_स्वीकार_करना(int संचिका_विवरणक, struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *address_len);
int स्थानीय_छोर_पता_पाना(int संचिका_विवरणक, struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *address_len);
int दूसरे_छोर_का_पता_पाना(int संचिका_विवरणक, struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *address_len);
ssize_t भेजना(int संचिका_विवरणक, const void *स्थानांतरण_का_अस्थायी_भंडार_2, size_t लंबाई, int flags);
ssize_t प्राप्त_करना(int संचिका_विवरणक, void *स्थानांतरण_का_अस्थायी_भंडार_2, size_t लंबाई, int flags);
ssize_t गंतव्य_पर_भेजना(int संचिका_विवरणक, const void *message, size_t लंबाई, int flags,
               const struct संचार_छोर_पता *dest_addr, पता_लंबाई_प्रकार dest_len);
ssize_t प्रेषक_पते_सहित_प्राप्त_करना(int संचिका_विवरणक, void *स्थानांतरण_का_अस्थायी_भंडार_2, size_t लंबाई, int flags,
                 struct संचार_छोर_पता *address, पता_लंबाई_प्रकार *address_len);
int संचार_दिशा_बंद_करना(int संचिका_विवरणक, int how);
int संचार_छोर_विकल्प_निर्धारित_करना(int संचिका_विवरणक, int level, int option_name,
               const void *option_value, पता_लंबाई_प्रकार option_len);
#ifdef __cplusplus
}
#endif

#endif
