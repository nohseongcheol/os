#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define संचिका_उघडा open
#define संचिका_तयार_करा creat
#define संचिका_डेटा_वाचा read
#define संचिका_डेटा_लिहा write
#define संचिका_मिटवा close
#define शोधा_संचिका lseek
#define प्रतिरूप_संचिका_विवरणक dup
#define प्रतिरूप_संचिका_विवरणक_येथे dup2
#define संचिका_प्रविष्टी_नाव_काढणे unlink
#define संचिका_लांबी_संच ftruncate
#define स्थिरकरा_फाईल_संग्रहण fsync
#define संचिका_राज्य_वाचा fstat
#define नियंत्रण_संचिका_विवरणक fcntl
#define केवळ_मूल्य_वाचा O_RDONLY
#define केवळ_मूल्य_लिहा O_WRONLY
#define वाचणे_लिहिणे O_RDWR
#define जर_अनुपस्थित_तयार_करा O_CREAT
#define नवे_संचिका_तयार_करा (O_CREAT | O_EXCL)
#define छाटूनरिकामेकरा_सामुग्री O_TRUNC
#define शेवटीजोडा_येथे_शेवट_करा O_APPEND
#define करा_नाही_प्रतीक्षा_करा O_NONBLOCK
#define पासून_आरंभ SEEK_SET
#define सध्याचे_मूळ SEEK_CUR
#define शेवट_करा_उगम SEEK_END
#define संचिका_राज्य stat
typedef size_t बाइट_संख्या_टाइप_करा;
typedef ssize_t आदानप्रदान_मोजमाप_टाइप_करा;
typedef off_t संचिका_ऑफसेट_टाइप_करा;
#endif
