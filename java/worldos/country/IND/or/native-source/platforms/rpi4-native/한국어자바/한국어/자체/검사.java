// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 검사(檢査): ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean ସର୍ତ୍ତ, String 까닭) {
        if (!ସର୍ତ୍ତ) throw new ଅବୈଧ_ଯୁକ୍ତି_ବ୍ୟତିକ୍ରମ(까닭);
    }
}
