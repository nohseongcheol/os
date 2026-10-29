#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int ပေးအချက်များအရေအတွက်, char **ပေးအချက်စာရင်း) {
    if (ပေးအချက်များအရေအတွက် < 1 || !ပေးအချက်စာရင်း[0]) return 2;
    const char နှုတ်ဆက်စကား[] = "ကိုယ်ပိုင် 커널의 C와 မြန်မာ POSIX\n";
    int စာတမ်း = ဖိုင်ဖွင့်("နှုတ်ဆက်.txt", ဖတ်ရေး | 없으면만들기 | 내용비우기, 0600);
    if (စာတမ်း < 0) return 1;
    အဝင်အထွက်ရလဒ်အမျိုးပုံစံ အလျား = ဖိုင်ဒေတာရေး(စာတမ်း, နှုတ်ဆက်စကား, sizeof(နှုတ်ဆက်စကား) - 1);
    ဖိုင်ပိတ်(စာတမ်း);
    ဖိုင်ဒေတာရေး(1, နှုတ်ဆက်စကား, sizeof(နှုတ်ဆက်စကား) - 1);
    return အလျား == sizeof(နှုတ်ဆက်စကား) - 1 ? 0 : 3;
}
