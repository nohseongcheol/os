#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **արգումենտ_Ցուցակ) {
    if (인수개수 < 1 || !արգումենտ_Ցուցակ[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = բացել_նիշք("인사.txt", կարդալ_գրել | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 տեւողություն_արժեք = գրել_նիշք_տվյալ(문서, 인사말, sizeof(인사말) - 1);
    փակել_նիշք(문서);
    գրել_նիշք_տվյալ(1, 인사말, sizeof(인사말) - 1);
    return տեւողություն_արժեք == sizeof(인사말) - 1 ? 0 : 3;
}
