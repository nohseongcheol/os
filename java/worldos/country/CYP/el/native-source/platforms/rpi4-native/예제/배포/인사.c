#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **όρισμα_Λίστα) {
    if (인수개수 < 1 || !όρισμα_Λίστα[0]) return 2;
    const char 인사말[] = "ίδιο 커널의 C와 ελληνικά POSIX\n";
    int 문서 = ανοίγω_Αρχείο("인사.txt", 읽고쓰기 | 없으면만들기 | περικοπή_Περιεχόμενα, 0600);
    if (문서 < 0) return 1;
    입출력결과형 διάρκεια_τιμή = εγγράφω_Αρχείο_δεδομένα(문서, 인사말, sizeof(인사말) - 1);
    κλείνω_Αρχείο(문서);
    εγγράφω_Αρχείο_δεδομένα(1, 인사말, sizeof(인사말) - 1);
    return διάρκεια_τιμή == sizeof(인사말) - 1 ? 0 : 3;
}
