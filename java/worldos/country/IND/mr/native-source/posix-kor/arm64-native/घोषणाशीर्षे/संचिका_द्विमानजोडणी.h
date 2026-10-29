#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t आदानप्रदान_मोजमाप_टाइप_करा;
typedef size_t बाइट_संख्या_टाइप_करा;
typedef int64_t संचिका_ऑफसेट_टाइप_करा;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
आदानप्रदान_मोजमाप_टाइप_करा pk_read(int fd, void *buffer, size_t count);
आदानप्रदान_मोजमाप_टाइप_करा pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
संचिका_ऑफसेट_टाइप_करा pk_lseek(int fd, संचिका_ऑफसेट_टाइप_करा offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, संचिका_ऑफसेट_टाइप_करा size);
int pk_fsync(int fd);
int pk_size(int fd);
int संचिका_उघडा(const char *मार्ग, int पद्धत_मोड, ...);
आदानप्रदान_मोजमाप_टाइप_करा संचिका_डेटा_वाचा(int फाइल, void *डेटा, size_t आयटम_संख्या);
आदानप्रदान_मोजमाप_टाइप_करा संचिका_डेटा_लिहा(int फाइल, const void *डेटा, size_t आयटम_संख्या);
int संचिका_मिटवा(int फाइल);
संचिका_ऑफसेट_टाइप_करा शोधा_संचिका(int फाइल, संचिका_ऑफसेट_टाइप_करा अंतर_मूल्य, int प्रोजेक्ट_मूळ);
int संचिका_प्रविष्टी_नाव_काढणे(const char *मार्ग);
int संचिका_लांबी_संच(int फाइल, संचिका_ऑफसेट_टाइप_करा आकार);
int स्थिरकरा_फाईल_संग्रहण(int फाइल);
int संचिका_आकारा(int फाइल);
#ifdef __cplusplus
}
#endif
#define त्रुटी_संख्या (*pk_errno_location())
#define केवळ_मूल्य_वाचा 0
#define केवळ_मूल्य_लिहा 1
#define वाचणे_लिहिणे 2
#define जर_अनुपस्थित_तयार_करा 0x40
#define नवे_संचिका_तयार_करा 0xc0
#define छाटूनरिकामेकरा_सामुग्री 0x200
#define शेवटीजोडा_येथे_शेवट_करा 0x400
#define पासून_आरंभ 0
#define सध्याचे_मूळ 1
#define शेवट_करा_उगम 2
#endif
