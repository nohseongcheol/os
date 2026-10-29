// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** 검사(檢査): இயக்கு_கட்டளை 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean நிபந்தனை, String 까닭) {
        if (!நிபந்தனை) throw new செல்லுபடியாகாத_மதிப்புரு_விதிவிலக்கு(까닭);
    }
}
