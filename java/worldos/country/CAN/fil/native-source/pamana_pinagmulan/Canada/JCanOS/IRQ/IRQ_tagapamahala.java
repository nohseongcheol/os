// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_tagapamahala {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktibo;

    public void magrehistro_pagpasok(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void release_Storage(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int ipamahagi_VALUE(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!Aktibo) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proseso_VALUE_pagpasok(저장된쌓임주소);
    }

    public void i_on() {
        Aktibo = true;
    }

    public void ideaktibo() {
        Aktibo = false;
    }

    public boolean information_technology_Aktibo() {
        return Aktibo;
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

