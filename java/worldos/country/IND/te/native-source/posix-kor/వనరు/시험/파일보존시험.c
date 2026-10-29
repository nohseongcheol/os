#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ప్రవేశం_జాబితా) {
    (void)개수; (void)ప్రవేశం_జాబితా;
    int దస్త్రం = తెరువు_ఫైలు("stored.txt", పఠన_లేఖన | 없으면만들기 | 내용비우기, 0600);
    if (దస్త్రం < 0 || వ్రాయి_ఫైలు_డేటా(దస్త్రం, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(దస్త్రం) < 0) return 2;
    if (మూసివేయి_ఫైలు(దస్త్రం) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
