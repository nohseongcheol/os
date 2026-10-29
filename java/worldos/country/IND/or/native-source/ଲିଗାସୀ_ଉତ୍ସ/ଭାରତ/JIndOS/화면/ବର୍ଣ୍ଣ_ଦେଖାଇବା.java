// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class ବର୍ଣ୍ଣ_ଦେଖାଇବା {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int ଅନୁଲମ୍ବ_ସ୍ଥିତି;

    public ବର୍ଣ୍ଣ_ଦେଖାଇବା() {
        지우기();
    }

    public void ନିର୍ଗମ(String ବିଷୟ_ମୂଲ୍ୟ) {
        for (int ଅନୁକ୍ରମଣିକା = 0; ଅନୁକ୍ରମଣିକା < ବିଷୟ_ମୂଲ୍ୟ.length(); ଅନୁକ୍ରମଣିକା++) {
            char 문자 = ବିଷୟ_ମୂଲ୍ୟ.charAt(ଅନୁକ୍ରମଣିକା);
            if (문자 == '\n') {
                가로 = 0;
                ଅନୁଲମ୍ବ_ସ୍ଥିତି++;
            } else {
                문자출력(가로++, ଅନୁଲମ୍ବ_ସ୍ଥିତି, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                ଅନୁଲମ୍ବ_ସ୍ଥିତି++;
            }
            if (ଅନୁଲମ୍ବ_ସ୍ଥିତି >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି) {
        ଯାଞ୍ଚ୍_କରିବା_ସ୍ଥିତି(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି);
        return 문자들[ଅନୁଲମ୍ବ_ସ୍ଥିତି * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        ଅନୁଲମ୍ବ_ସ୍ଥିତି = 0;
    }

    private void 문자출력(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି, char 문자) {
        ଯାଞ୍ଚ୍_କରିବା_ସ୍ଥିତି(가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି);
        문자들[ଅନୁଲମ୍ବ_ସ୍ଥିତି * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        ଅନୁଲମ୍ବ_ସ୍ଥିତି = 높이 - 1;
    }

    private void ଯାଞ୍ଚ୍_କରିବା_ସ୍ଥିତି(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି) {
        if (가로 < 0 || 가로 >= 너비 || ଅନୁଲମ୍ବ_ସ୍ଥିତି < 0 || ଅନୁଲମ୍ବ_ସ୍ଥିତି >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

