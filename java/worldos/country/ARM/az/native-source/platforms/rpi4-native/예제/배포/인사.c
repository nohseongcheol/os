#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **arqument_Siyahı) {
    if (인수개수 < 1 || !arqument_Siyahı[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = açmaq_fayl("인사.txt", oxunan_yazılan | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 uzunluq_VALUE = yazmaq_fayl_verilənlər(문서, 인사말, sizeof(인사말) - 1);
    bağlamaq_fayl(문서);
    yazmaq_fayl_verilənlər(1, 인사말, sizeof(인사말) - 1);
    return uzunluq_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
