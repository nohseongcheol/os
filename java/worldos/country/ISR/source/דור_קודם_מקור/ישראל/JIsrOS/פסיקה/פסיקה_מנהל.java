// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.פסיקה;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class פסיקה_מנהל {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean זמין;

    public void אוגר_ערך_bb216f10(int מדד, 개입중단처리기 처리기) {
        번호확인(מדד);
        처리기들[מדד] = 처리기;
    }

    public void לשחרר_אחסון(int מדד) {
        번호확인(מדד);
        처리기들[מדד] = null;
    }

    public int להפיץ_ערך(int מדד, int 저장된쌓임주소) {
        번호확인(מדד);
        if (!זמין) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[מדד];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.תהליך_ערך_ערך(저장된쌓임주소);
    }

    public void הפעלה_0b9ce0d7() {
        זמין = true;
    }

    public void בטל_הפעלה() {
        זמין = false;
    }

    public boolean מערכות_מידע_זמין() {
        return זמין;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int מדד) {
        if (מדד < 0 || מדד >= 처리기들.length) {
            throw new IllegalArgumentException("פסיקה 번호가 올바르지 않습니다.");
        }
    }
}

