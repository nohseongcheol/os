// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.prekinitev;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class prekinitev_Upravitelj {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Dejaven;

    public void register_vnos(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void izdaja_Senzor_prostora(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int distribuirati_VALUE(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!Dejaven) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proces_VALUE_vnos(저장된쌓임주소);
    }

    public void vklopiti() {
        Dejaven = true;
    }

    public void dezaktivirati() {
        Dejaven = false;
    }

    public boolean informacijska_tehnologija_Dejaven() {
        return Dejaven;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("prekinitev 번호가 올바르지 않습니다.");
        }
    }
}

