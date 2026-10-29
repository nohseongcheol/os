// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Τουρκία.JTurOS.διακοπή;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class διακοπή_Υπεύθυνος {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ενεργή;

    public void δήλωση_καταχώρηση(int Ευρετήριο, 개입중단처리기 처리기) {
        번호확인(Ευρετήριο);
        처리기들[Ευρετήριο] = 처리기;
    }

    public void έκδοση_Χώρος_αποθήκευσης(int Ευρετήριο) {
        번호확인(Ευρετήριο);
        처리기들[Ευρετήριο] = null;
    }

    public int διανέμω_τιμή(int Ευρετήριο, int 저장된쌓임주소) {
        번호확인(Ευρετήριο);
        if (!ενεργή) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[Ευρετήριο];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.διεργασία_τιμή_καταχώρηση(저장된쌓임주소);
    }

    public void ενεργοποιώ() {
        ενεργή = true;
    }

    public void απενεργοποιώ() {
        ενεργή = false;
    }

    public boolean πληροφοριακά_συστήματα_ενεργή() {
        return ενεργή;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int Ευρετήριο) {
        if (Ευρετήριο < 0 || Ευρετήριο >= 처리기들.length) {
            throw new IllegalArgumentException("διακοπή 번호가 올바르지 않습니다.");
        }
    }
}

