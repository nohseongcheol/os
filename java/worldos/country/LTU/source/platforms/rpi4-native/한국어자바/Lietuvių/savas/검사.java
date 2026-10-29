// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 검사(檢査): Vykdyti_komanda 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean sąlyga, String 까닭) {
        if (!sąlyga) throw new neleistinas_argumentas_išimtis(까닭);
    }
}
