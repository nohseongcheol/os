// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republica_Moldova.JMdaOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class 개입중단관리자 {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Activ;

    public void registru_intrare(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void lansa_Stocare(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int distribui_VALUE(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!Activ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proces_VALUE_intrare(저장된쌓임주소);
    }

    public void activa() {
        Activ = true;
    }

    public void deactiva() {
        Activ = false;
    }

    public boolean sisteme_de_informații_Activ() {
        return Activ;
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

