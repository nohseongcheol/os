#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argument_Lista) {
    if (인수개수 < 1 || !argument_Lista[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = otvoren_Datoteka("인사.txt", za_čitanje_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = 파일자료쓰기(문서, 인사말, sizeof(인사말) - 1);
    Zatvori_Datoteka(문서);
    파일자료쓰기(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
