#include <संचारजाळे_द्विमानजोडणी.h>
#include <errno.h>
#include "कॉल_सीमा.h"

int socket(int पत्ता_योजना, int संचारजाळे_प्रकार, int काम_संख्या) {
    return आवाहन_मोजमाप(jkoros_syscall(41, पत्ता_योजना, संचारजाळे_प्रकार, काम_संख्या, 0, 0));
}
int bind(int संचिका_विवरणक, const struct sockaddr *पत्ता, socklen_t पत्ता_लांबी) {
    return आवाहन_मोजमाप(jkoros_syscall(42, संचिका_विवरणक, (int)पत्ता, पत्ता_लांबी, 0, 0));
}
ssize_t sendto(int संचिका_विवरणक, const void *डेटा, size_t बाइट_संख्या, int संयोजना,
               const struct sockaddr *पत्ता, socklen_t पत्ता_लांबी) {
    int विनंती[2] = {(int)पत्ता, पत्ता_लांबी};
    return आवाहन_मोजमाप(jkoros_syscall(43, संचिका_विवरणक, (int)डेटा, बाइट_संख्या, संयोजना, (int)विनंती));
}
ssize_t recvfrom(int संचिका_विवरणक, void *डेटा, size_t बाइट_संख्या, int संयोजना,
                 struct sockaddr *पत्ता, socklen_t *पत्ता_लांबी) {
    int विनंती[2] = {(int)पत्ता, (int)पत्ता_लांबी};
    return आवाहन_मोजमाप(jkoros_syscall(44, संचिका_विवरणक, (int)डेटा, बाइट_संख्या, संयोजना, (int)विनंती));
}
int getsockname(int संचिका_विवरणक, struct sockaddr *पत्ता, socklen_t *पत्ता_लांबी) {
    return आवाहन_मोजमाप(jkoros_syscall(45, संचिका_विवरणक, (int)पत्ता, (int)पत्ता_लांबी, 0, 0));
}
int setsockopt(int संचिका_विवरणक, int थर_मूल्य, int सेटिंग्ज_नाव, const void *मूल्य, socklen_t मूल्य_लांबी) {
    if (थर_मूल्य != SOL_SOCKET || सेटिंग्ज_नाव != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!मूल्य) { errno = EFAULT; return -1; }
    if (मूल्य_लांबी != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *वेळ_मूल्य = मूल्य;
    if (वेळ_मूल्य->tv_sec < 0 || वेळ_मूल्य->tv_sec > 2 || वेळ_मूल्य->tv_usec < 0 || वेळ_मूल्य->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int मिलिसेकंद = वेळ_मूल्य->tv_sec * 1000 + (वेळ_मूल्य->tv_usec + 999) / 1000;
    return आवाहन_मोजमाप(jkoros_syscall(46, संचिका_विवरणक, मिलिसेकंद, 0, 0, 0));
}
uint16_t htons(uint16_t मूल्य) { return (मूल्य << 8) | (मूल्य >> 8); }
uint16_t ntohs(uint16_t मूल्य) { return htons(मूल्य); }
uint32_t htonl(uint32_t मूल्य) {
    return (मूल्य << 24) | ((मूल्य << 8) & 0xff0000U) | ((मूल्य >> 8) & 0xff00U) | (मूल्य >> 24);
}
uint32_t ntohl(uint32_t मूल्य) { return htonl(मूल्य); }
int inet_pton(int पत्ता_योजना, const char *स्ट्रींग_मूल्य, void *पत्ता) {
    if (पत्ता_योजना != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!स्ट्रींग_मूल्य || !पत्ता) { errno = EFAULT; return -1; }
    unsigned char तात्पुरते_मूल्य[4];
    for (int खाच_प्रविष्टी = 0; खाच_प्रविष्टी < 4; खाच_प्रविष्टी++) {
        int मूल्य = 0, अंक_90a88624 = 0;
        const char *सुरू_करा = स्ट्रींग_मूल्य;
        while (*स्ट्रींग_मूल्य >= '0' && *स्ट्रींग_मूल्य <= '9') {
            if (++अंक_90a88624 > 3) return 0;
            मूल्य = मूल्य * 10 + *स्ट्रींग_मूल्य++ - '0';
        }
        if (!अंक_90a88624 || मूल्य > 255 || (अंक_90a88624 > 1 && *सुरू_करा == '0')) return 0;
        तात्पुरते_मूल्य[खाच_प्रविष्टी] = मूल्य;
        if (खाच_प्रविष्टी < 3) { if (*स्ट्रींग_मूल्य++ != '.') return 0; }
        else if (*स्ट्रींग_मूल्य) return 0;
    }
    for (int खाच_प्रविष्टी = 0; खाच_प्रविष्टी < 4; खाच_प्रविष्टी++) ((unsigned char *)पत्ता)[खाच_प्रविष्टी] = तात्पुरते_मूल्य[खाच_प्रविष्टी];
    return 1;
}
const char *inet_ntop(int पत्ता_योजना, const void *पत्ता, char *स्ट्रींग_मूल्य, socklen_t धारणक्षमता_मूल्य) {
    if (पत्ता_योजना != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!पत्ता || !स्ट्रींग_मूल्य) { errno = EFAULT; return 0; }
    const unsigned char *संख्या = पत्ता;
    char तात्पुरते_मूल्य[16]; unsigned int लांबी_मूल्य = 0;
    for (int खाच_प्रविष्टी = 0; खाच_प्रविष्टी < 4; खाच_प्रविष्टी++) {
        unsigned int मूल्य = संख्या[खाच_प्रविष्टी];
        if (मूल्य >= 100) तात्पुरते_मूल्य[लांबी_मूल्य++] = '0' + मूल्य / 100;
        if (मूल्य >= 10) तात्पुरते_मूल्य[लांबी_मूल्य++] = '0' + मूल्य / 10 % 10;
        तात्पुरते_मूल्य[लांबी_मूल्य++] = '0' + मूल्य % 10;
        if (खाच_प्रविष्टी < 3) तात्पुरते_मूल्य[लांबी_मूल्य++] = '.';
    }
    तात्पुरते_मूल्य[लांबी_मूल्य++] = 0;
    if (धारणक्षमता_मूल्य < लांबी_मूल्य) { errno = ENOSPC; return 0; }
    for (unsigned int खाच_प्रविष्टी = 0; खाच_प्रविष्टी < लांबी_मूल्य; खाच_प्रविष्टी++) स्ट्रींग_मूल्य[खाच_प्रविष्टी] = तात्पुरते_मूल्य[खाच_प्रविष्टी];
    return स्ट्रींग_मूल्य;
}
