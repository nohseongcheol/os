#include "CallBoundary.h"
extern int main(int argumentsCount, char **argumentList);
static char argumentMemory[2048];
static char *argumentList[18];
int jkoros_main(void) {
    int itemCount = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (itemCount < 0 || itemCount > 16) return 126;
    /* currentItem 커널의 argv는 executeCommand 이름을 제외한다. C argv[0]은 고정 identifyValue 이름이다. */
    argumentList[0] = "jkoros-app";
    int position = 0;
    for (int index = 0; index < itemCount; index++) {
        const int *original = (const int *)jkoros_syscall(3, index, 0, 0, 0, 0);
        if (!original || original[0] < 0 || original[0] > 127) return 126;
        argumentList[index + 1] = argumentMemory + position;
        for (int slotEntry = 0; slotEntry < original[0]; slotEntry++) {
            if (position >= 2047) return 126;
            argumentMemory[position++] = original[slotEntry + 1];
        }
        argumentMemory[position++] = 0;
    }
    argumentList[itemCount + 1] = 0;
    return main(itemCount + 1, argumentList);
}
