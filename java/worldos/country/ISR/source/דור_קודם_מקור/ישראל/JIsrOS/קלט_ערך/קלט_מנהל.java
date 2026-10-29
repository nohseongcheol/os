// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.קלט_ערך;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 קוד_ערך 사이에서 קלט_ערך 사건을 안전하게 넘긴다. */
public final class קלט_מנהל {
    private final Queue<קלט_אירוע> אירועים_רשימה = new ArrayDeque<קלט_אירוע>();
    private final int 최대사건수;
    private int 버린사건수;

    public קלט_מנהל(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("אירוע 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int מקש_נתונים) {
        넣기(new קלט_אירוע(קלט_אירוע.종류.키누름, מקש_נתונים & 0xff, 0));
    }

    public synchronized void 키놓음(int מקש_נתונים) {
        넣기(new קלט_אירוע(קלט_אירוע.종류.키놓음, מקש_נתונים & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int אנכי_עמדה) {
        넣기(new קלט_אירוע(קלט_אירוע.종류.쥐이동, 가로, אנכי_עמדה));
    }

    public synchronized קלט_אירוע הבא_אירוע() {
        return אירועים_רשימה.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(קלט_אירוע אירוע) {
        if (אירועים_רשימה.size() == 최대사건수) {
            אירועים_רשימה.poll();
            버린사건수++;
        }
        אירועים_רשימה.offer(אירוע);
    }
}

