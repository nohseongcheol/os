#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **arg_Saraksts) {
    if (인수개수 < 1 || !arg_Saraksts[0]) return 2;
    const char 인사말[] = "savs 커널의 C와 Latviešu POSIX\n";
    int 문서 = atvērt_Fails("인사.txt", 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = rakstīšana_Fails_dati(문서, 인사말, sizeof(인사말) - 1);
    Aizvērt_Fails(문서);
    rakstīšana_Fails_dati(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
