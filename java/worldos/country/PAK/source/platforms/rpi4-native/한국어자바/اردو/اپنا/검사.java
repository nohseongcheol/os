// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** 검사(檢査): نفاذ_کریں_حکم 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean شرط, String 까닭) {
        if (!شرط) throw new بے_جواز_دلائل_استثنا(까닭);
    }
}
