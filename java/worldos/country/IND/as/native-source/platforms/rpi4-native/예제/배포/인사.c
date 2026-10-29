#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **যুক্তি_সূচী) {
    if (인수개수 < 1 || !যুক্তি_সূচী[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = খোলক_ফাইল("인사.txt", পঢ়িব_লিখিব_পৰা | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 দৈর্ঘ্য_মান = লিখক_ফাইল_ডাটা(문서, 인사말, sizeof(인사말) - 1);
    বন্ধ_কৰক_ফাইল(문서);
    লিখক_ফাইল_ডাটা(1, 인사말, sizeof(인사말) - 1);
    return দৈর্ঘ্য_মান == sizeof(인사말) - 1 ? 0 : 3;
}
