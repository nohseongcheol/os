#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **목록) {
    (void)개수; (void)목록;
    int COADAN = 파일열기("stored.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (COADAN < 0 || 파일자료쓰기(COADAN, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(COADAN) < 0) return 2;
    if (파일닫기(COADAN) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
