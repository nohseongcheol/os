#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **විස්තාරකය_ලැයිස්තුව) {
    if (인수개수 < 1 || !විස්තාරකය_ලැයිස්තුව[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = සාදන්න_ගොනුව("인사.txt", කියවීම්_ලිවීම් | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 දිග_අගය = ලියන්න_ගොනුව_දත්ත(문서, 인사말, sizeof(인사말) - 1);
    වසන්න_ගොනුව(문서);
    ලියන්න_ගොනුව_දත්ත(1, 인사말, sizeof(인사말) - 1);
    return දිග_අගය == sizeof(인사말) - 1 ? 0 : 3;
}
