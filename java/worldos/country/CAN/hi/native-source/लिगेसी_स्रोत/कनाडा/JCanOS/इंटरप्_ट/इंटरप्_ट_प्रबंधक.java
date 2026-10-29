// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package कनाडा.JCanOS.इंटरप्_ट;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class इंटरप्_ट_प्रबंधक {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean सक्रिय;

    public void रजिस्टर_एन्ट्री(int इंडेक्स, 개입중단처리기 처리기) {
        번호확인(इंडेक्स);
        처리기들[इंडेक्स] = 처리기;
    }

    public void रिलीज़_संग्रहण(int इंडेक्स) {
        번호확인(इंडेक्स);
        처리기들[इंडेक्स] = null;
    }

    public int वितरित_करें_मान(int इंडेक्स, int 저장된쌓임주소) {
        번호확인(इंडेक्स);
        if (!सक्रिय) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[इंडेक्स];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.प्रक्रिया_मान_एन्ट्री(저장된쌓임주소);
    }

    public void चालू_करें() {
        सक्रिय = true;
    }

    public void निष्क्रिय_करें() {
        सक्रिय = false;
    }

    public boolean सूचना_प्रौद्योगिकी_सक्रिय() {
        return सक्रिय;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int इंडेक्स) {
        if (इंडेक्स < 0 || इंडेक्स >= 처리기들.length) {
            throw new IllegalArgumentException("इंटरप्_ट 번호가 올바르지 않습니다.");
        }
    }
}

