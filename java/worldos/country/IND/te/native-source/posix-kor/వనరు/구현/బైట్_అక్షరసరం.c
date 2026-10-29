#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *అక్షరసరం_మూల్యం) { size_t పొడవు_మూల్యం = 0; while (అక్షరసరం_మూల్యం[పొడవు_మూల్యం]) పొడవు_మూల్యం++; return పొడవు_మూల్యం; }
int strcmp(const char *ముందు_మూల్యం, const char *వెనుకకు_మూల్యం) {
    while (*ముందు_మూల్యం && *ముందు_మూల్యం == *వెనుకకు_మూల్యం) { ముందు_మూల్యం++; వెనుకకు_మూల్యం++; }
    return (unsigned char)*ముందు_మూల్యం - (unsigned char)*వెనుకకు_మూల్యం;
}
int memcmp(const void *ముందు_మూల్యం, const void *వెనుకకు_మూల్యం, size_t 바이트수) {
    const unsigned char *가 = ముందు_మూల్యం, *나 = వెనుకకు_మూల్యం;
    for (size_t స్లాట్_ప్రవేశం = 0; స్లాట్_ప్రవేశం < 바이트수; స్లాట్_ప్రవేశం++) if (가[స్లాట్_ప్రవేశం] != 나[స్లాట్_ప్రవేశం]) return 가[స్లాట్_ప్రవేశం] - 나[స్లాట్_ప్రవేశం];
    return 0;
}
void *memcpy(void *గమ్యం_మూల్యం, const void *원본, size_t 바이트수) {
    unsigned char *가 = గమ్యం_మూల్యం; const unsigned char *나 = 원본;
    for (size_t స్లాట్_ప్రవేశం = 0; స్లాట్_ప్రవేశం < 바이트수; స్లాట్_ప్రవేశం++) 가[స్లాట్_ప్రవేశం] = 나[స్లాట్_ప్రవేశం];
    return గమ్యం_మూల్యం;
}
void *memset(void *గమ్యం_మూల్యం, int మూల్యం, size_t 바이트수) {
    unsigned char *డేటా = గమ్యం_మూల్యం;
    for (size_t స్లాట్_ప్రవేశం = 0; స్లాట్_ప్రవేశం < 바이트수; స్లాట్_ప్రవేశం++) డేటా[స్లాట్_ప్రవేశం] = మూల్యం;
    return గమ్యం_మూల్యం;
}
int putchar(int 문자) { unsigned char మూల్యం = 문자; return write(1, &మూల్యం, 1) == 1 ? మూల్యం : EOF; }
int puts(const char *అక్షరసరం_మూల్యం) {
    size_t పొడవు_మూల్యం = strlen(అక్షరసరం_మూల్యం), స్థానము = 0;
    while (స్థానము < పొడవు_మూల్యం) { ssize_t ప్రమాణం = write(1, అక్షరసరం_మూల్యం + స్థానము, పొడవు_మూల్యం - స్థానము); if (ప్రమాణం <= 0) return EOF; స్థానము += ప్రమాణం; }
    return putchar('\n') == EOF ? EOF : 0;
}
