#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *स्ट्रिंग_मोल) { size_t लांबाय_मोल = 0; while (स्ट्रिंग_मोल[लांबाय_मोल]) लांबाय_मोल++; return लांबाय_मोल; }
int strcmp(const char *앞, const char *फाटीं_मोल) {
    while (*앞 && *앞 == *फाटीं_मोल) { 앞++; फाटीं_मोल++; }
    return (unsigned char)*앞 - (unsigned char)*फाटीं_मोल;
}
int memcmp(const void *앞, const void *फाटीं_मोल, size_t बायट_COUNT) {
    const unsigned char *가 = 앞, *나 = फाटीं_मोल;
    for (size_t स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < बायट_COUNT; स्लॉट_प्रवेश++) if (가[स्लॉट_प्रवेश] != 나[स्लॉट_प्रवेश]) return 가[स्लॉट_प्रवेश] - 나[स्लॉट_प्रवेश];
    return 0;
}
void *memcpy(void *नियुक्त_स्थान_मोल, const void *원본, size_t बायट_COUNT) {
    unsigned char *가 = नियुक्त_स्थान_मोल; const unsigned char *나 = 원본;
    for (size_t स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < बायट_COUNT; स्लॉट_प्रवेश++) 가[स्लॉट_प्रवेश] = 나[स्लॉट_प्रवेश];
    return नियुक्त_स्थान_मोल;
}
void *memset(void *नियुक्त_स्थान_मोल, int मोल, size_t बायट_COUNT) {
    unsigned char *डेटा = नियुक्त_स्थान_मोल;
    for (size_t स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < बायट_COUNT; स्लॉट_प्रवेश++) डेटा[स्लॉट_प्रवेश] = मोल;
    return नियुक्त_स्थान_मोल;
}
int putchar(int 문자) { unsigned char मोल = 문자; return write(1, &मोल, 1) == 1 ? मोल : EOF; }
int puts(const char *स्ट्रिंग_मोल) {
    size_t लांबाय_मोल = strlen(स्ट्रिंग_मोल), स्थिती = 0;
    while (स्थिती < लांबाय_मोल) { ssize_t मेजप = write(1, स्ट्रिंग_मोल + स्थिती, लांबाय_मोल - स्थिती); if (मेजप <= 0) return EOF; स्थिती += मेजप; }
    return putchar('\n') == EOF ? EOF : 0;
}
