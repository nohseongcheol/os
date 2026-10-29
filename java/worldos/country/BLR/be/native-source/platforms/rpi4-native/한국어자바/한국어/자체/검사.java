// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 검사(檢査): выканаць_каманда 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean умова, String 까닭) {
        if (!умова) throw new памылковы_аргумент_выключэнне(까닭);
    }
}
