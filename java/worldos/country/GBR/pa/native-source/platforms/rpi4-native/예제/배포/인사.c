#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ਦਲੀਲ_ਸੂਚੀ) {
    if (인수개수 < 1 || !ਦਲੀਲ_ਸੂਚੀ[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 ਪੰਜਾਬੀ POSIX\n";
    int 문서 = ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ("인사.txt", ਪੜ੍ਹਨ_ਲਿਖਣ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ਲੰਬਾਈ_ਕੀਮਤ = ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(문서, 인사말, sizeof(인사말) - 1);
    ਬੰਦ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ(문서);
    ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(1, 인사말, sizeof(인사말) - 1);
    return ਲੰਬਾਈ_ਕੀਮਤ == sizeof(인사말) - 1 ? 0 : 3;
}
