// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 검사(檢査): Mag_execute_utos 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean kondisyon, String 까닭) {
        if (!kondisyon) throw new hindi_tama_argumento_pagbubukod(까닭);
    }
}
