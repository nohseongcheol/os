// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 검사(檢査): Executar_comando 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean doença, String 까닭) {
        if (!doença) throw new inválido_argumento_exceção(까닭);
    }
}
