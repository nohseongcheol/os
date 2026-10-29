#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **목록) {
    (void)개수; (void)목록;
    int Besjtandj = 파일열기("stored.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (Besjtandj < 0 || 파일자료쓰기(Besjtandj, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Besjtandj) < 0) return 2;
    if (파일닫기(Besjtandj) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
