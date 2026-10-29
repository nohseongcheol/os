// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** 검사(檢査): Izvedi_ukaz 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean pogoj, String 까닭) {
        if (!pogoj) throw new neveljaven_argument_izjema(까닭);
    }
}
