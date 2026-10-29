// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;

/** 검사(檢査): laksanakan_perintah 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean syarat, String 까닭) {
        if (!syarat) throw new tak_sah_argumen_pengecualian(까닭);
    }
}
