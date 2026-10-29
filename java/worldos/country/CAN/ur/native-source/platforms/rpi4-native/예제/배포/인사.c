#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **دلائل_فہرست) {
    if (인수개수 < 1 || !دلائل_فہرست[0]) return 2;
    const char 인사말[] = "اپنا 커널의 C와 اردو POSIX\n";
    int 문서 = بنائیں_فائل("인사.txt", مطالعہ_تحریری | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 لمبا_ئی_قدر = لکھیں_فائل_کوائف(문서, 인사말, sizeof(인사말) - 1);
    بند_فائل(문서);
    لکھیں_فائل_کوائف(1, 인사말, sizeof(인사말) - 1);
    return لمبا_ئی_قدر == sizeof(인사말) - 1 ? 0 : 3;
}
