#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Listë) {
    if (인수개수 < 1 || !argument_Listë[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = hap_skedar("인사.txt", lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 gjatësi_VALUE = shkruaj_skedar_të_dhëna(문서, 인사말, sizeof(인사말) - 1);
    mbyll_skedar(문서);
    shkruaj_skedar_të_dhëna(1, 인사말, sizeof(인사말) - 1);
    return gjatësi_VALUE == sizeof(인사말) - 1 ? 0 : 3;
}
