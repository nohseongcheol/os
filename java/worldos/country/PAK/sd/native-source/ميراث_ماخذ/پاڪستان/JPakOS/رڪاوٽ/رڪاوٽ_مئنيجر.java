// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.رڪاوٽ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class رڪاوٽ_مئنيجر {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean فعال;

    public void 등록(int ابتدائي, 개입중단처리기 처리기) {
        번호확인(ابتدائي);
        처리기들[ابتدائي] = 처리기;
    }

    public void جاري_ڪريو_ذخيرو(int ابتدائي) {
        번호확인(ابتدائي);
        처리기들[ابتدائي] = null;
    }

    public int ورهايو_قدر(int ابتدائي, int 저장된쌓임주소) {
        번호확인(ابتدائي);
        if (!فعال) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ابتدائي];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.عمل_قدر_داخلا(저장된쌓임주소);
    }

    public void اهل() {
        فعال = true;
    }

    public void غير_فعال_ڪريو() {
        فعال = false;
    }

    public boolean 활성인가() {
        return فعال;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ابتدائي) {
        if (ابتدائي < 0 || ابتدائي >= 처리기들.length) {
            throw new IllegalArgumentException("رڪاوٽ 번호가 올바르지 않습니다.");
        }
    }
}

