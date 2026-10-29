#ifndef स्वकीय_प्रयोक्ता_कॉल_शीर्षलेख
#define स्वकीय_प्रयोक्ता_कॉल_शीर्षलेख
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=आवाहन अनुक्रमणिका, x0..x5=बाबी, x0=मोजमाप/ऋण_मूल्य त्रुटी. Linux ABI 아님.
static inline intptr_t प्रयोक्ता_आवाहन(uintptr_t अनुक्रमणिका, uintptr_t पहिले_संकार्य, uintptr_t दुसरे_संकार्य, uintptr_t तिसरे_संकार्य,
                                uintptr_t चौथे_संकार्य, uintptr_t पाचवे_संकार्य, uintptr_t सहावे_संकार्य) {
    register uintptr_t रजिस्टर_शून्य __asm__("x0") = पहिले_संकार्य;
    register uintptr_t रजिस्टर_एक __asm__("x1") = दुसरे_संकार्य;
    register uintptr_t रजिस्टर_दोन __asm__("x2") = तिसरे_संकार्य;
    register uintptr_t रजिस्टर_तीन __asm__("x3") = चौथे_संकार्य;
    register uintptr_t रजिस्टर_चार __asm__("x4") = पाचवे_संकार्य;
    register uintptr_t रजिस्टर_पाच __asm__("x5") = सहावे_संकार्य;
    register uintptr_t रजिस्टर_आठ __asm__("x8") = अनुक्रमणिका;
    __asm__ volatile("svc #0" : "+r"(रजिस्टर_शून्य) : "r"(रजिस्टर_एक), "r"(रजिस्टर_दोन), "r"(रजिस्टर_तीन), "r"(रजिस्टर_चार), "r"(रजिस्टर_पाच), "r"(रजिस्टर_आठ) : "memory", "cc");
    return (intptr_t)रजिस्टर_शून्य;
}
static inline intptr_t पडदा_आयत(unsigned आडवे_समन्वयीत, unsigned उभे_समन्वयीत, unsigned मागितलेले_रुंदी_मूल्य, unsigned मागितलेले_उंची_मूल्य, unsigned रेड_ग्रीन_ब्ल्यू_रंग) {
    return प्रयोक्ता_आवाहन(13, आडवे_समन्वयीत, उभे_समन्वयीत, रेड_ग्रीन_ब्ल्यू_रंग, मागितलेले_रुंदी_मूल्य, मागितलेले_उंची_मूल्य, 0);
}
static inline intptr_t प्रयोक्ता_स्मृती_शेवट_करा(uintptr_t शेवट) { return प्रयोक्ता_आवाहन(8, शेवट, 0, 0, 0, 0, 0); }
static inline intptr_t पडदा_रुंदी_वाचा(void) { return प्रयोक्ता_आवाहन(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t पडदा_उंची_वाचा(void) { return प्रयोक्ता_आवाहन(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t प्रतीक्षा_करा_साठी_पडदा_कळ(void) {
    intptr_t मोजमाप = प्रयोक्ता_आवाहन(16, 0, 0, 0, 0, 0, 0);
    if (मोजमाप < 0) return मोजमाप;
    do { मोजमाप = प्रयोक्ता_आवाहन(16, 1, 0, 0, 0, 0, 0); } while (मोजमाप == -11);
    प्रयोक्ता_आवाहन(16, 2, 0, 0, 0, 0, 0);
    return मोजमाप;
}
static inline intptr_t प्रयोक्ता_वितर्क_संख्या(void) { return प्रयोक्ता_आवाहन(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t प्रयोक्ता_वितर्क(unsigned अनुक्रमणिका, char *सामुग्री_मूल्य, size_t आकार) {
    return प्रयोक्ता_आवाहन(15, अनुक्रमणिका, (uintptr_t)सामुग्री_मूल्य, आकार, 0, 0, 0);
}
#endif
