// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** 검사(檢査): Izvrši_naredba 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean uvjet, String 까닭) {
        if (!uvjet) throw new nevaljan_argument_iznimka(까닭);
    }
}
