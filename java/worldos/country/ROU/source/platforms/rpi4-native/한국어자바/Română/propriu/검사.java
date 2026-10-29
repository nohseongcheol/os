// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;

/** 검사(檢査): executa_comandă 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean condiție, String 까닭) {
        if (!condiție) throw new nul_argument_excepție(까닭);
    }
}
