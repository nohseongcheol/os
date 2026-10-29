// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** 검사(檢査): Wykonaj_polecenie 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean choroba, String 까닭) {
        if (!choroba) throw new nieważny_argument_wyjątek(까닭);
    }
}
