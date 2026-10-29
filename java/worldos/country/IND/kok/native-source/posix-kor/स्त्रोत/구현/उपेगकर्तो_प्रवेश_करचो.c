#include "호출경계.h"
extern int main(int 인수개수, char **युक्तीवाद_सुची);
static char युक्तीवाद_मेमरी[2048];
static char *युक्तीवाद_सुची[18];
int jkoros_main(void) {
    int आयटम_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (आयटम_COUNT < 0 || आयटम_COUNT > 16) return 126;
    /* 현재 커널의 argv는 पाळो_दिवचो_आदेश 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    युक्तीवाद_सुची[0] = "jkoros-app";
    int स्थिती = 0;
    for (int INDEX = 0; INDEX < आयटम_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        युक्तीवाद_सुची[INDEX + 1] = युक्तीवाद_मेमरी + स्थिती;
        for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < 원본[0]; स्लॉट_प्रवेश++) {
            if (स्थिती >= 2047) return 126;
            युक्तीवाद_मेमरी[स्थिती++] = 원본[स्लॉट_प्रवेश + 1];
        }
        युक्तीवाद_मेमरी[स्थिती++] = 0;
    }
    युक्तीवाद_सुची[आयटम_COUNT + 1] = 0;
    return main(आयटम_COUNT + 1, युक्तीवाद_सुची);
}
