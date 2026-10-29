// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
/** ਪੰਜਾਬੀ 화면 구성요소를 만드는 편의 ਫੰਗਸ਼ਨ_ਕੀਮਤ. */
public final class ਵਿਜੇਟ {
    private ਵਿਜੇਟ() {}
    public static void 나중에실행(실행할일 ਕਾਰਜ_ਕਿਰਿਆ) { ਇਵੈਂਟ_ਕਤਾਰ.나중에실행(ਕਾਰਜ_ਕਿਰਿਆ); }
    public static ਲੇਬਲ ਟੈਗ_ਕੀਮਤ(String ਟੈਕਸਟ, int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, int 폭, int 높이) {
        return new ਲੇਬਲ(ਟੈਕਸਟ, 가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 폭, 높이);
    }
    public static ਬਟਨ ਬਟਨ(String ਟੈਕਸਟ, int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, int 폭, int 높이, 동작받이 받이) {
        return new ਬਟਨ(ਟੈਕਸਟ, 가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 폭, 높이, 받이);
    }
    public static ਟੈਕਸਟ_ਖੇਤਰ ਟੈਕਸਟ_ਖੇਤਰ(String ਟੈਕਸਟ, int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, int 폭, int 높이) {
        return new ਟੈਕਸਟ_ਖੇਤਰ(ਟੈਕਸਟ, 가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 폭, 높이);
    }
}
