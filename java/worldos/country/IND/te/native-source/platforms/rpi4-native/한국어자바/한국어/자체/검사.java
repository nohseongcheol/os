// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 검사(檢査): అమలు_చేయి_ఆదేశం 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean నిబంధన, String 까닭) {
        if (!నిబంధన) throw new చెల్లని_కారకం_మినహాయింపు(까닭);
    }
}
