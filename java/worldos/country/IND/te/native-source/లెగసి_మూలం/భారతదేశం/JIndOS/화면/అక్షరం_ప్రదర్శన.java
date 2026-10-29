// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class అక్షరం_ప్రదర్శన {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int నిలువు_స్థాయి;

    public అక్షరం_ప్రదర్శన() {
        తుడిచివేయి_ప్రవేశం();
    }

    public void అవుట్పుట్(String విషయం_మూల్యం) {
        for (int సూచీ = 0; సూచీ < విషయం_మూల్యం.length(); సూచీ++) {
            char 문자 = విషయం_మూల్యం.charAt(సూచీ);
            if (문자 == '\n') {
                가로 = 0;
                నిలువు_స్థాయి++;
            } else {
                문자출력(가로++, నిలువు_స్థాయి, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                నిలువు_స్థాయి++;
            }
            if (నిలువు_స్థాయి >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int నిలువు_స్థాయి) {
        సరిచూడు_స్థాయి(가로, నిలువు_స్థాయి);
        return 문자들[నిలువు_స్థాయి * 너비 + 가로];
    }

    public void తుడిచివేయి_ప్రవేశం() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        నిలువు_స్థాయి = 0;
    }

    private void 문자출력(int 가로, int నిలువు_స్థాయి, char 문자) {
        సరిచూడు_స్థాయి(가로, నిలువు_స్థాయి);
        문자들[నిలువు_స్థాయి * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        నిలువు_స్థాయి = 높이 - 1;
    }

    private void సరిచూడు_స్థాయి(int 가로, int నిలువు_స్థాయి) {
        if (가로 < 0 || 가로 >= 너비 || నిలువు_స్థాయి < 0 || నిలువు_స్థాయి >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

