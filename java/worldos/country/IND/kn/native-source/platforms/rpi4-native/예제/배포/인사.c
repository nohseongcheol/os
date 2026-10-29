#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ವಾದ_ಪಟ್ಟಿ) {
    if (인수개수 < 1 || !ವಾದ_ಪಟ್ಟಿ[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 ಕನ್ನಡ POSIX\n";
    int 문서 = ರಚಿಸು_ಫೈಲ್("인사.txt", ಓದು_ಬರೆ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ಉದ್ದ_ಮೌಲ್ಯ = ಬರೆ_ಫೈಲ್_ಡೇಟಾ(문서, 인사말, sizeof(인사말) - 1);
    ಮುಚ್ಚು_ಫೈಲ್(문서);
    ಬರೆ_ಫೈಲ್_ಡೇಟಾ(1, 인사말, sizeof(인사말) - 1);
    return ಉದ್ದ_ಮೌಲ್ಯ == sizeof(인사말) - 1 ? 0 : 3;
}
