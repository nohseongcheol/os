// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** 검사(檢査): Виконати_команда 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean умова, String 까닭) {
        if (!умова) throw new недійсний_аргумент_виняток(까닭);
    }
}
