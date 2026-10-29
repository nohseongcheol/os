#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **arg_Zerrenda) {
    if (인수개수 < 1 || !arg_Zerrenda[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 Euskara POSIX\n";
    int 문서 = ireki_fitxategi("인사.txt", irakurri_idatzi | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 luzera_balio = idatzi_fitxategi_datuak(문서, 인사말, sizeof(인사말) - 1);
    itxi_fitxategi(문서);
    idatzi_fitxategi_datuak(1, 인사말, sizeof(인사말) - 1);
    return luzera_balio == sizeof(인사말) - 1 ? 0 : 3;
}
