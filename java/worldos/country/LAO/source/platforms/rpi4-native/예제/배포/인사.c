#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ຂໍ້ພິສູດ_ລາຍຊື່) {
    if (인수개수 < 1 || !ຂໍ້ພິສູດ_ລາຍຊື່[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = ສ້າງ_ຟາຍ("인사.txt", ອ່ານ_ຂຽນ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ຄວາມຍາວ_ຄ່າ = ຂຽນ_ຟາຍ_ຂໍ້ມູນ(문서, 인사말, sizeof(인사말) - 1);
    ປິດ_ຟາຍ(문서);
    ຂຽນ_ຟາຍ_ຂໍ້ມູນ(1, 인사말, sizeof(인사말) - 1);
    return ຄວາມຍາວ_ຄ່າ == sizeof(인사말) - 1 ? 0 : 3;
}
