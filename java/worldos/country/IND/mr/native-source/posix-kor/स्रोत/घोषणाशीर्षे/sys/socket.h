#ifndef JKOROS_SOCKET_H
#define JKOROS_SOCKET_H
#include <sys/types.h>
typedef unsigned int socklen_t;
typedef unsigned short sa_family_t;
struct sockaddr { sa_family_t sa_family; char sa_data[14]; };
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define MSG_DONTWAIT 64
#define SOL_SOCKET 1
#define SO_RCVTIMEO 20
int socket(int पत्ता_योजना, int संचारजाळे_प्रकार, int काम_संख्या);
int bind(int संचिका_विवरणक, const struct sockaddr *पत्ता, socklen_t पत्ता_लांबी);
ssize_t sendto(int संचिका_विवरणक, const void *डेटा, size_t बाइट_संख्या, int संयोजना,
               const struct sockaddr *पत्ता, socklen_t पत्ता_लांबी);
ssize_t recvfrom(int संचिका_विवरणक, void *डेटा, size_t बाइट_संख्या, int संयोजना,
                 struct sockaddr *पत्ता, socklen_t *पत्ता_लांबी);
int getsockname(int संचिका_विवरणक, struct sockaddr *पत्ता, socklen_t *पत्ता_लांबी);
int setsockopt(int संचिका_विवरणक, int थर_मूल्य, int सेटिंग्ज_नाव, const void *मूल्य, socklen_t मूल्य_लांबी);
#endif
