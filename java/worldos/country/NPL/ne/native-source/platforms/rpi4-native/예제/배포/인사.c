#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **तर्क_सूची) {
    if (인수개수 < 1 || !तर्क_सूची[0]) return 2;
    const char 인사말[] = "निज 커널의 C와 नेपाली POSIX\n";
    int 문서 = सिर्जना_फाइल("인사.txt", पढ्न_लेख्_न | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 लम्बाइ_मान = लेख्नुहोस्_फाइल_लगत(문서, 인사말, sizeof(인사말) - 1);
    बन्द_गर्नुहोस्_फाइल(문서);
    लेख्नुहोस्_फाइल_लगत(1, 인사말, sizeof(인사말) - 1);
    return लम्बाइ_मान == sizeof(인사말) - 1 ? 0 : 3;
}
