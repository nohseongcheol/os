#include "../नामकरण/मशीन_लिंक_नावे.h"
#include "आवाहन.h"
typedef void (*आरंभक_पद्धत)(void);
extern आरंभक_पद्धत __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int प्रारंभ_प्रयोक्ता_अनुप्रयोग(int);
int प्रयोक्ता_प्रारंभ(int अग्रेषित_मूल्य) {
    for (आरंभक_पद्धत *डेटा_स्थान = __init_array_start; डेटा_स्थान < __init_array_end; डेटा_स्थान++) (*डेटा_स्थान)();
    int मोजमाप = प्रारंभ_प्रयोक्ता_अनुप्रयोग(अग्रेषित_मूल्य);
    for (आरंभक_पद्धत *डेटा_स्थान = __fini_array_end; डेटा_स्थान != __fini_array_start;) (*--डेटा_स्थान)();
    return मोजमाप;
}
void *memset(void *डेटा_स्थान, int मूल्य, size_t प्रविष्टी_संख्या) { unsigned char *गंतव्यस्थान_डेटा = डेटा_स्थान; while (प्रविष्टी_संख्या--) *गंतव्यस्थान_डेटा++ = मूल्य; return डेटा_स्थान; }
void *memcpy(void *गंतव्यस्थान_डेटा, const void *स्ट्रींग_डेटा, size_t प्रविष्टी_संख्या) { unsigned char *पहिले_मूल्य = गंतव्यस्थान_डेटा; const unsigned char *दुसरे_मूल्य = स्ट्रींग_डेटा; while (प्रविष्टी_संख्या--) *पहिले_मूल्य++ = *दुसरे_मूल्य++; return गंतव्यस्थान_डेटा; }
