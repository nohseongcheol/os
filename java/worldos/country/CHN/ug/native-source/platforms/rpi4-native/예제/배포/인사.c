#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **دەلىل_تىزىم) {
    if (인수개수 < 1 || !دەلىل_تىزىم[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = قۇرۇش_ھۆججەت("인사.txt", ئوقۇش_يېزىش | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ئۇزۇنلۇق_قىممىتى = يازماق_ھۆججەت_مەلۇمات(문서, 인사말, sizeof(인사말) - 1);
    ئاياغ_ھۆججەت(문서);
    يازماق_ھۆججەت_مەلۇمات(1, 인사말, sizeof(인사말) - 1);
    return ئۇزۇنلۇق_قىممىتى == sizeof(인사말) - 1 ? 0 : 3;
}
