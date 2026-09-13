#ifndef _include_प्रणाली_संतान_प्रतीक्षा
#define _include_प्रणाली_संतान_प्रतीक्षा

#include <प्रणाली/आँकड़ा_प्रकार.h>

#define WNOHANG 1
#define WEXITSTATUS(स्थिति) (((स्थिति) >> 8) & 0xff)
#define WIFEXITED(स्थिति) (((स्थिति) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t संतान_की_प्रतीक्षा_करना(int *स्थिति);
pid_t नियत_संतान_की_प्रतीक्षा_करना(pid_t pid, int *स्थिति, int options);
#ifdef __cplusplus
}
#endif

#endif
