// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** 검사(檢査): Rith_ordú 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean coinníoll, String 까닭) {
        if (!coinníoll) throw new neamhbhailí_argóint_eisceacht(까닭);
    }
}
