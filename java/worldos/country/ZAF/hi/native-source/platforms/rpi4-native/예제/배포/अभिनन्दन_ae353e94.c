#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **तर्क_सूची) {
    if (인수개수 < 1 || !तर्क_सूची[0]) return 2;
    const char अभिनन्दन[] = "निज 커널의 C와 हिंदी POSIX\n";
    int 문서 = जारी_फ़ाइल("अभिनन्दन_ae353e94.txt", पठन_लेखन | 없으면만들기 | कम_करें_सामग्री, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = लिखना_फ़ाइल_डेटा(문서, अभिनन्दन, sizeof(अभिनन्दन) - 1);
    बंद_फ़ाइल(문서);
    लिखना_फ़ाइल_डेटा(1, अभिनन्दन, sizeof(अभिनन्दन) - 1);
    return 길이 == sizeof(अभिनन्दन) - 1 ? 0 : 3;
}
