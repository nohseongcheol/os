// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੀਨੀਆ.JKenOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class ਵਰਣ_ਪ੍ਰਦਰਸ਼ਨ {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ;

    public ਵਰਣ_ਪ੍ਰਦਰਸ਼ਨ() {
        지우기();
    }

    public void ਆਉਟਪੁੱਟ(String ਤਤਕਰਾ_ਕੀਮਤ) {
        for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਅਨੁਕ੍ਰਮਣਿਕਾ < ਤਤਕਰਾ_ਕੀਮਤ.length(); ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
            char 문자 = ਤਤਕਰਾ_ਕੀਮਤ.charAt(ਅਨੁਕ੍ਰਮਣਿਕਾ);
            if (문자 == '\n') {
                가로 = 0;
                ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ++;
            } else {
                문자출력(가로++, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ++;
            }
            if (ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ) {
        ਤਸਦੀਕ_ਸਥਿਤੀ_ਬਦਲੋ(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ);
        return 문자들[ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ = 0;
    }

    private void 문자출력(int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, char 문자) {
        ਤਸਦੀਕ_ਸਥਿਤੀ_ਬਦਲੋ(가로, ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ);
        문자들[ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ = 높이 - 1;
    }

    private void ਤਸਦੀਕ_ਸਥਿਤੀ_ਬਦਲੋ(int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ) {
        if (가로 < 0 || 가로 >= 너비 || ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ < 0 || ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

