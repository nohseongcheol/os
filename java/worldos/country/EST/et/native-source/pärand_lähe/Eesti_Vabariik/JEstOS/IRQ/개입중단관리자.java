// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class 개입중단관리자 {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktiivne;

    public void register_kirje(int INDEX, 개입중단처리기 처리기) {
        kinnitama_number(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void vabastama_salvesti(int INDEX) {
        kinnitama_number(INDEX);
        처리기들[INDEX] = null;
    }

    public int laiali_jagama_VALUE(int INDEX, int 저장된쌓임주소) {
        kinnitama_number(INDEX);
        if (!Aktiivne) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Joonis_VALUE_kirje(저장된쌓임주소);
    }

    public void lubama() {
        Aktiivne = true;
    }

    public void inaktiveerima() {
        Aktiivne = false;
    }

    public boolean infotehnoloogia_Aktiivne() {
        return Aktiivne;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void kinnitama_number(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

