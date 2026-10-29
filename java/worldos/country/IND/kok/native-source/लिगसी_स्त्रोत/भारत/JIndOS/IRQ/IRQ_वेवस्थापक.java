// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_वेवस्थापक {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean क्रियाशील;

    public void नोंदणी_प्रवेश(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void रिलीज_सांठवण(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int वितरण_मोल(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!क्रियाशील) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.प्रक्रिया_मोल_प्रवेश(저장된쌓임주소);
    }

    public void सक्षम_करचें() {
        क्रियाशील = true;
    }

    public void निश्क्रीय_करा() {
        क्रियाशील = false;
    }

    public boolean 활성인가() {
        return क्रियाशील;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

