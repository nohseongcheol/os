// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;

/** 검사(檢査): અમલ_કરો_આદેશ 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean શરત, String 까닭) {
        if (!શરત) throw new 잘못된인수예외(까닭);
    }
}
