// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package নেপাল.JNplOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class অক্ষর_ডিসপ্লে {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int উল্লম্ব_পদ;

    public অক্ষর_ডিসপ্লে() {
        মুছুন_ভুক্তি();
    }

    public void নির্গম(String সামগ্রি_মান) {
        for (int সূচি = 0; সূচি < সামগ্রি_মান.length(); সূচি++) {
            char 문자 = সামগ্রি_মান.charAt(সূচি);
            if (문자 == '\n') {
                가로 = 0;
                উল্লম্ব_পদ++;
            } else {
                문자출력(가로++, উল্লম্ব_পদ, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                উল্লম্ব_পদ++;
            }
            if (উল্লম্ব_পদ >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int উল্লম্ব_পদ) {
        যাচাই_করা_পদ(가로, উল্লম্ব_পদ);
        return 문자들[উল্লম্ব_পদ * 너비 + 가로];
    }

    public void মুছুন_ভুক্তি() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        উল্লম্ব_পদ = 0;
    }

    private void 문자출력(int 가로, int উল্লম্ব_পদ, char 문자) {
        যাচাই_করা_পদ(가로, উল্লম্ব_পদ);
        문자들[উল্লম্ব_পদ * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        উল্লম্ব_পদ = 높이 - 1;
    }

    private void যাচাই_করা_পদ(int 가로, int উল্লম্ব_পদ) {
        if (가로 < 0 || 가로 >= 너비 || উল্লম্ব_পদ < 0 || উল্লম্ব_পদ >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

