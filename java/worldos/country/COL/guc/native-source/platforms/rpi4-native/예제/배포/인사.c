#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **인수목록) {
    if (인수개수 < 1 || !인수목록[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = 파일열기("인사.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 akaliaa_ajutuu = ashajaa_anaajaalaa_atijaaya(문서, 인사말, sizeof(인사말) - 1);
    asürülaa_anaajaalaa(문서);
    ashajaa_anaajaalaa_atijaaya(1, 인사말, sizeof(인사말) - 1);
    return akaliaa_ajutuu == sizeof(인사말) - 1 ? 0 : 3;
}
