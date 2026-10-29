#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ארגומנט_רשימה) {
    if (인수개수 < 1 || !ארגומנט_רשימה[0]) return 2;
    const char 인사말[] = "עצמי 커널의 C와 עברית POSIX\n";
    int 문서 = פתח_קובץ("인사.txt", קריאה_כתיבה | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = כתיבה_קובץ_נתונים(문서, 인사말, sizeof(인사말) - 1);
    סגור_קובץ(문서);
    כתיבה_קובץ_נתונים(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
