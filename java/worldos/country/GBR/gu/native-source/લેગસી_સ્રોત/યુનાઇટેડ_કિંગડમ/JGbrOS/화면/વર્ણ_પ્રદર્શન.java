// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package યુનાઇટેડ_કિંગડમ.JGbrOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class વર્ણ_પ્રદર્શન {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int ઊભી_સ્થિતિ;

    public વર્ણ_પ્રદર્શન() {
        지우기();
    }

    public void આઉટપુટ(String સામગ્રી_મૂલ્ય) {
        for (int અનુક્રમણિકા = 0; અનુક્રમણિકા < સામગ્રી_મૂલ્ય.length(); અનુક્રમણિકા++) {
            char 문자 = સામગ્રી_મૂલ્ય.charAt(અનુક્રમણિકા);
            if (문자 == '\n') {
                가로 = 0;
                ઊભી_સ્થિતિ++;
            } else {
                문자출력(가로++, ઊભી_સ્થિતિ, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                ઊભી_સ્થિતિ++;
            }
            if (ઊભી_સ્થિતિ >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int ઊભી_સ્થિતિ) {
        ચકાસવું_સ્થિતિ(가로, ઊભી_સ્થિતિ);
        return 문자들[ઊભી_સ્થિતિ * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        ઊભી_સ્થિતિ = 0;
    }

    private void 문자출력(int 가로, int ઊભી_સ્થિતિ, char 문자) {
        ચકાસવું_સ્થિતિ(가로, ઊભી_સ્થિતિ);
        문자들[ઊભી_સ્થિતિ * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        ઊભી_સ્થિતિ = 높이 - 1;
    }

    private void ચકાસવું_સ્થિતિ(int 가로, int ઊભી_સ્થિતિ) {
        if (가로 < 0 || 가로 >= 너비 || ઊભી_સ્થિતિ < 0 || ઊભી_સ્થિતિ >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

