// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** 검사(檢査): কার্যকর_করুন_আদেশ 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean শর্ত, String 까닭) {
        if (!শর্ত) throw new অবৈধ_যুক্তি_ব্যতিক্রম(까닭);
    }
}
