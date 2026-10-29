// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int ಚಲಾಯಿಸು_2() {
        ಬಳಕೆದಾರ.ಬರೆ("Hello from a separate Java ELF!\n");
        ಬಳಕೆದಾರ.ಬರೆ(ಬಳಕೆದಾರ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ಪದಸೂಚಿ = 0; ಪದಸೂಚಿ < ಬಳಕೆದಾರ.인수개수(); ಪದಸೂಚಿ++) {
            ಬಳಕೆದಾರ.ಬರೆ("arg: "); ಬಳಕೆದಾರ.ಬರೆ(ಬಳಕೆದಾರ.인수(ಪದಸೂಚಿ)); ಬಳಕೆದಾರ.ಬರೆ("\n");
        }
        return ಬಳಕೆದಾರ.실행권한() == 3 ? 0 : 1;
    }
}
