// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] 인수) throws Exception {
        int 합 = 0;
        int 수 = 1;
        while (수 <= 10) {
            합 = 합 + 수;
            수 = 수 + 1;
        }
        ಕನ್ನಡ.자체.ಔಟ್_ಪುಟ್.수쓰기(합);
        ಕನ್ನಡ.자체.ಕಡತ.ಬರೆ("aot.txt", "한글 AOT ಕಡತ 😀");
        ಕನ್ನಡ.자체.ಔಟ್_ಪುಟ್.ಬರೆ_ಸಾಲು(ಕನ್ನಡ.자체.ಕಡತ.ಓದು("aot.txt"));
    }
}
