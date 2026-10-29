// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_aulattiji {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean pigiaqtisimajuq;

    public void 등록(int nalunaiqsimavik, 개입중단처리기 처리기) {
        번호확인(nalunaiqsimavik);
        처리기들[nalunaiqsimavik] = 처리기;
    }

    public void 해제(int nalunaiqsimavik) {
        번호확인(nalunaiqsimavik);
        처리기들[nalunaiqsimavik] = null;
    }

    public int 분배(int nalunaiqsimavik, int 저장된쌓임주소) {
        번호확인(nalunaiqsimavik);
        if (!pigiaqtisimajuq) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[nalunaiqsimavik];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Pivallianiq_atuutilik_Iliniku(저장된쌓임주소);
    }

    public void ikilli() {
        pigiaqtisimajuq = true;
    }

    public void 비활성화() {
        pigiaqtisimajuq = false;
    }

    public boolean 활성인가() {
        return pigiaqtisimajuq;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int nalunaiqsimavik) {
        if (nalunaiqsimavik < 0 || nalunaiqsimavik >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

