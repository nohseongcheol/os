// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جۇڭگو.JChnOS.ئۈزۈلۈش;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ئۈزۈلۈش_باشقۇرغۇچى {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ئاكتىپ;

    public void تىزىملىتىش_كىرگۈزۈش(int ئىندېكس, 개입중단처리기 처리기) {
        번호확인(ئىندېكس);
        처리기들[ئىندېكس] = 처리기;
    }

    public void تارقىتىش_بوشلۇق(int ئىندېكس) {
        번호확인(ئىندېكس);
        처리기들[ئىندېكس] = null;
    }

    public int تارقىتىش_قىممىتى_51743f48(int ئىندېكس, int 저장된쌓임주소) {
        번호확인(ئىندېكس);
        if (!ئاكتىپ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ئىندېكس];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.جەريان_قىممىتى_كىرگۈزۈش(저장된쌓임주소);
    }

    public void ئىشلەتمەك() {
        ئاكتىپ = true;
    }

    public void ئىشلىتىشتىن_توختاتماق() {
        ئاكتىپ = false;
    }

    public boolean 활성인가() {
        return ئاكتىپ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ئىندېكس) {
        if (ئىندېكس < 0 || ئىندېكس >= 처리기들.length) {
            throw new IllegalArgumentException("ئۈزۈلۈش 번호가 올바르지 않습니다.");
        }
    }
}

