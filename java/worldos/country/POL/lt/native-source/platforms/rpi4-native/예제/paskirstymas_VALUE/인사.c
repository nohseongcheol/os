#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argumentas_Sąrašas) {
    if (인수개수 < 1 || !argumentas_Sąrašas[0]) return 2;
    const char 인사말[] = "savas 커널의 C와 Lietuvių POSIX\n";
    int 문서 = kurti_Failas("인사.txt", 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = rašymas_Failas_duomenys(문서, 인사말, sizeof(인사말) - 1);
    Uždaryti_Failas(문서);
    rašymas_Failas_duomenys(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
