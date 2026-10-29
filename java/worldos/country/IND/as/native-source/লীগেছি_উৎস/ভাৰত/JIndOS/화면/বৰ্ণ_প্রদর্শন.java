// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class বৰ্ণ_প্রদর্শন {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int উলম্ব_স্থান_সলনি_কৰক;

    public বৰ্ণ_প্রদর্শন() {
        지우기();
    }

    public void নিৰ্গম(String সামগ্ৰী_মান) {
        for (int ইনডেক্স = 0; ইনডেক্স < সামগ্ৰী_মান.length(); ইনডেক্স++) {
            char 문자 = সামগ্ৰী_মান.charAt(ইনডেক্স);
            if (문자 == '\n') {
                가로 = 0;
                উলম্ব_স্থান_সলনি_কৰক++;
            } else {
                문자출력(가로++, উলম্ব_স্থান_সলনি_কৰক, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                উলম্ব_স্থান_সলনি_কৰক++;
            }
            if (উলম্ব_স্থান_সলনি_কৰক >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int উলম্ব_স্থান_সলনি_কৰক) {
        প্ৰমাণিত_কৰক_স্থান_সলনি_কৰক(가로, উলম্ব_স্থান_সলনি_কৰক);
        return 문자들[উলম্ব_স্থান_সলনি_কৰক * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        উলম্ব_স্থান_সলনি_কৰক = 0;
    }

    private void 문자출력(int 가로, int উলম্ব_স্থান_সলনি_কৰক, char 문자) {
        প্ৰমাণিত_কৰক_স্থান_সলনি_কৰক(가로, উলম্ব_স্থান_সলনি_কৰক);
        문자들[উলম্ব_স্থান_সলনি_কৰক * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        উলম্ব_স্থান_সলনি_কৰক = 높이 - 1;
    }

    private void প্ৰমাণিত_কৰক_স্থান_সলনি_কৰক(int 가로, int উলম্ব_স্থান_সলনি_কৰক) {
        if (가로 < 0 || 가로 >= 너비 || উলম্ব_স্থান_সলনি_কৰক < 0 || উলম্ব_স্থান_সলনি_কৰক >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

