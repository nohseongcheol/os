#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **อาร์กิวเมนต์_รายการ) {
    if (인수개수 < 1 || !อาร์กิวเมนต์_รายการ[0]) return 2;
    const char 인사말[] = "เอง 커널의 C와 ไทย POSIX\n";
    int 문서 = เปิด_แฟ้ม("인사.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 길이 = 파일자료쓰기(문서, 인사말, sizeof(인사말) - 1);
    ปิด_แฟ้ม(문서);
    파일자료쓰기(1, 인사말, sizeof(인사말) - 1);
    return 길이 == sizeof(인사말) - 1 ? 0 : 3;
}
