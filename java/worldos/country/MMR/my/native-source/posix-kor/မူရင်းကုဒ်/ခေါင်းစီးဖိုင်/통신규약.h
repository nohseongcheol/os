#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define အဆုံးမှတ်ဖန်တီး socket
#define လိပ်စာချည်နှောင် bind
#define ဒေတာစာဒေတာပို့ sendto
#define ဒေတာစာဒေတာလက်ခံရယူ recvfrom
#define ကွန်ရက်ပေါက်လိပ်စာဖတ် getsockname
#define ကွန်ရက်သတ်မှတ်ချက်ပြောင်း setsockopt
#define ကွန်ရက်လိပ်စာသဒ္ဒါခွဲခြမ်း inet_pton
#define ပုံစံကွန်ရက်လိပ်စာ inet_ntop
#define ကွန်ရက်တို htons
#define ကွန်ရက်ကိန်းပြည့် htonl
#define ကိရိယာအစဉ်တို ntohs
#define ကိရိယာအစဉ်ကိန်းပြည့် ntohl
#endif
