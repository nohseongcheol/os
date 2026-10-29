// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.מערכת_קבצים;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ערך_ברירת_מחדל 분할 영역을 읽는다. */
public final class מחיצה_ראשית_טבלה {
    public static final class מחיצה_ערך {
        private final int 종류;
        private final long התחל_מקטע;
        private final long 구역수;

        מחיצה_ערך(int 종류, long התחל_מקטע, long 구역수) {
            this.종류 = 종류;
            this.התחל_מקטע = התחל_מקטע;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long התחל_מקטע() { return התחל_מקטע; }
        public long 구역수() { return 구역수; }
    }

    public List<מחיצה_ערך> קרא(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<מחיצה_ערך> תוצאה = new ArrayList<מחיצה_ערך>();
        for (int מדד = 0; מדד < 4; מדד++) {
            int מיקום = 446 + מדד * 16;
            int 종류 = 첫구역[מיקום + 4] & 0xff;
            long הפעלה = 작은순서정수(첫구역, מיקום + 8);
            long גודל = 작은순서정수(첫구역, מיקום + 12);
            if (종류 != 0 && גודל != 0) {
                תוצאה.add(new מחיצה_ערך(종류, הפעלה, גודל));
            }
        }
        return Collections.unmodifiableList(תוצאה);
    }

    private long 작은순서정수(byte[] נתונים, int מיקום) {
        return (נתונים[מיקום] & 0xffL)
                | ((נתונים[מיקום + 1] & 0xffL) << 8)
                | ((נתונים[מיקום + 2] & 0xffL) << 16)
                | ((נתונים[מיקום + 3] & 0xffL) << 24);
    }
}

