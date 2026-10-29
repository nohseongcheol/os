#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int आयटम_COUNT, char **प्रवेश_सुची) {
    (void)आयटम_COUNT; (void)प्रवेश_सुची;
    char डेटा[6]; int लांबाय_मोल = 0;
    puts("POSIX INPUT READY");
    while (लांबाय_मोल < 6) {
        int मेजप = 파일자료읽기(0, डेटा + लांबाय_मोल, 6 - लांबाय_मोल);
        if (मेजप <= 0) return 1;
        लांबाय_मोल += मेजप;
    }
    if (memcmp(डेटा, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
