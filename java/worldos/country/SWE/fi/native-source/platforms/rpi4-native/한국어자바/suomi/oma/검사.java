// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** 검사(檢査): Suorita_komento 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean ehto, String 까닭) {
        if (!ehto) throw new pätemätön_argumentti_poikkeus(까닭);
    }
}
