// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ماریشس.JMusOS.مداخلت_کریں;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class مداخلت_کریں_مینیجر {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean فعال;

    public void رجسٹر_کریں_اندراج(int اشاریہ, 개입중단처리기 처리기) {
        번호확인(اشاریہ);
        처리기들[اشاریہ] = 처리기;
    }

    public void ریلیز_ذخیرہ(int اشاریہ) {
        번호확인(اشاریہ);
        처리기들[اشاریہ] = null;
    }

    public int بانٹیں_قدر(int اشاریہ, int 저장된쌓임주소) {
        번호확인(اشاریہ);
        if (!فعال) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[اشاریہ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.عمل_قدر_اندراج(저장된쌓임주소);
    }

    public void آف_کریں() {
        فعال = true;
    }

    public void بے_عمل_کریں() {
        فعال = false;
    }

    public boolean معلومات_ٹیکنالوجی_فعال() {
        return فعال;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int اشاریہ) {
        if (اشاریہ < 0 || اشاریہ >= 처리기들.length) {
            throw new IllegalArgumentException("مداخلت_کریں 번호가 올바르지 않습니다.");
        }
    }
}

