#include "파일규약.h"
class doc_वेवस्थापक {
    int INDEX;
public:
    doc_वेवस्थापक(const char *नांव) : INDEX(उगडचें_फायल(नांव, वाचन_बरप | 없으면만들기 | 내용비우기, 0600)) {}
    ~doc_वेवस्थापक() { if (INDEX >= 0) शेवट_फायल(INDEX); }
    입출력결과형 बरोवचें(const char *डेटा, बायट_COUNT_TYPE आवाठ) { return बरोवचें_फायल_डेटा(INDEX, डेटा, आवाठ); }
};
extern "C" int Start_उपेगकर्तो_एप्लिकेशन(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    doc_वेवस्थापक 문서("C++인사.txt");
    बरोवचें_फायल_डेटा(1, 인사말, sizeof(인사말) - 1);
    return 문서.बरोवचें(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
