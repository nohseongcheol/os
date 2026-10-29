// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovákia.JSvkOS.megszakítás;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class megszakítás_kezelő {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktív;

    public void jegyzék_bejegyzés(int INDEX, 개입중단처리기 처리기) {
        igazol_szám(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void kiad_tár(int INDEX) {
        igazol_szám(INDEX);
        처리기들[INDEX] = null;
    }

    public int eloszt_ÉRTÉK(int INDEX, int 저장된쌓임주소) {
        igazol_szám(INDEX);
        if (!Aktív) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.folyamat_ÉRTÉK_bejegyzés(저장된쌓임주소);
    }

    public void bekapcsol() {
        Aktív = true;
    }

    public void inaktivál() {
        Aktív = false;
    }

    public boolean informatikai_részleg_Aktív() {
        return Aktív;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void igazol_szám(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("megszakítás 번호가 올바르지 않습니다.");
        }
    }
}

