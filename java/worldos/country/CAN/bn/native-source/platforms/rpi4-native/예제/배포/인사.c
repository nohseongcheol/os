#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **যুক্তি_তালিকা) {
    if (인수개수 < 1 || !যুক্তি_তালিকা[0]) return 2;
    const char 인사말[] = "নিজ 커널의 C와 বাংলা POSIX\n";
    int 문서 = খোলা_ফাইল("인사.txt", পঠন_লিখন | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 দৈর্ঘ্য_মান = লেখা_ফাইল_ডাটা(문서, 인사말, sizeof(인사말) - 1);
    বন্ধ_ফাইল(문서);
    লেখা_ফাইল_ডাটা(1, 인사말, sizeof(인사말) - 1);
    return দৈর্ঘ্য_মান == sizeof(인사말) - 1 ? 0 : 3;
}
