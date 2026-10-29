#include <파일규약.h>
#include <stdio.h>
int main(int आयटम_COUNT, char **प्रवेश_सुची) {
    (void)आयटम_COUNT; (void)प्रवेश_सुची;
    int फायल = उगडचें_फायल("stored.txt", वाचन_बरप | 없으면만들기 | 내용비우기, 0600);
    if (फायल < 0 || बरोवचें_फायल_डेटा(फायल, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(फायल) < 0) return 2;
    if (शेवट_फायल(फायल) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
