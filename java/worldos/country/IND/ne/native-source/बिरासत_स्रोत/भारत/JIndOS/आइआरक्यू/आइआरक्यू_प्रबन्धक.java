// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.आइआरक्यू;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class आइआरक्यू_प्रबन्धक {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean सक्रिय;

    public void दर्ता_प्रविष्टि(int अनुक्रमणिका, 개입중단처리기 처리기) {
        번호확인(अनुक्रमणिका);
        처리기들[अनुक्रमणिका] = 처리기;
    }

    public void जारी_भण्डारण(int अनुक्रमणिका) {
        번호확인(अनुक्रमणिका);
        처리기들[अनुक्रमणिका] = null;
    }

    public int वितरण_गर्नुहोस्_मान(int अनुक्रमणिका, int 저장된쌓임주소) {
        번호확인(अनुक्रमणिका);
        if (!सक्रिय) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[अनुक्रमणिका];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.प्रक्रिया_मान_प्रविष्टि(저장된쌓임주소);
    }

    public void खोल्नुहोस्_0b9ce0d7() {
        सक्रिय = true;
    }

    public void निष्क्रिय_गर्नुहोस्() {
        सक्रिय = false;
    }

    public boolean 활성인가() {
        return सक्रिय;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int अनुक्रमणिका) {
        if (अनुक्रमणिका < 0 || अनुक्रमणिका >= 처리기들.length) {
            throw new IllegalArgumentException("आइआरक्यू 번호가 올바르지 않습니다.");
        }
    }
}

