// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جنوب_السودان.JSsdOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class حرف_يعرض {
    public static final int 너비 = 80;
    public static final int ارتفاع_قيمة = 25;
    private final char[] 문자들 = new char[너비 * ارتفاع_قيمة];
    private int 가로;
    private int عمودي_منصب;

    public حرف_يعرض() {
        مسح_إدخال();
    }

    public void مخرجات(String محتوى_قيمة) {
        for (int فهرس = 0; فهرس < محتوى_قيمة.length(); فهرس++) {
            char 문자 = محتوى_قيمة.charAt(فهرس);
            if (문자 == '\n') {
                가로 = 0;
                عمودي_منصب++;
            } else {
                يطبع_حرف(가로++, عمودي_منصب, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                عمودي_منصب++;
            }
            if (عمودي_منصب >= ارتفاع_قيمة) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int عمودي_منصب) {
        يتحقق_منصب(가로, عمودي_منصب);
        return 문자들[عمودي_منصب * 너비 + 가로];
    }

    public void مسح_إدخال() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        عمودي_منصب = 0;
    }

    private void يطبع_حرف(int 가로, int عمودي_منصب, char 문자) {
        يتحقق_منصب(가로, عمودي_منصب);
        문자들[عمودي_منصب * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (ارتفاع_قيمة - 1));
        Arrays.fill(문자들, 너비 * (ارتفاع_قيمة - 1), 문자들.length, ' ');
        عمودي_منصب = ارتفاع_قيمة - 1;
    }

    private void يتحقق_منصب(int 가로, int عمودي_منصب) {
        if (가로 < 0 || 가로 >= 너비 || عمودي_منصب < 0 || عمودي_منصب >= ارتفاع_قيمة) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

