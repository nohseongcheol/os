// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.ማቋረጥ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ማቋረጥ_አስተዳዳሪ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ንቁ;

    public void መዝግብ_ምዝግብ(int መረጃ_ጠቆመ, 개입중단처리기 처리기) {
        번호확인(መረጃ_ጠቆመ);
        처리기들[መረጃ_ጠቆመ] = 처리기;
    }

    public void ልቀቅ_ማከማቻ(int መረጃ_ጠቆመ) {
        번호확인(መረጃ_ጠቆመ);
        처리기들[መረጃ_ጠቆመ] = null;
    }

    public int አከፋፍል_እሴት(int መረጃ_ጠቆመ, int 저장된쌓임주소) {
        번호확인(መረጃ_ጠቆመ);
        if (!ንቁ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[መረጃ_ጠቆመ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ሂደት_እሴት_ምዝግብ(저장된쌓임주소);
    }

    public void አብራ() {
        ንቁ = true;
    }

    public void አቦዝን() {
        ንቁ = false;
    }

    public boolean የመረጃ_ቴክኖሎጂ_ንቁ() {
        return ንቁ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int መረጃ_ጠቆመ) {
        if (መረጃ_ጠቆመ < 0 || መረጃ_ጠቆመ >= 처리기들.length) {
            throw new IllegalArgumentException("ማቋረጥ 번호가 올바르지 않습니다.");
        }
    }
}

