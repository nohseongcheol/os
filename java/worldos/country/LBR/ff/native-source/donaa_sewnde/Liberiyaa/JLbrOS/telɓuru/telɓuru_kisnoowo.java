// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Liberiyaa.JLbrOS.telɓuru;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class telɓuru_kisnoowo {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean gonaa;

    public void 등록(int joopirdu, 개입중단처리기 처리기) {
        번호확인(joopirdu);
        처리기들[joopirdu] = 처리기;
    }

    public void 해제(int joopirdu) {
        번호확인(joopirdu);
        처리기들[joopirdu] = null;
    }

    public int 분배(int joopirdu, int 저장된쌓임주소) {
        번호확인(joopirdu);
        if (!gonaa) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[joopirdu];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Yuɓɓo_golle_njaru_naatnugol(저장된쌓임주소);
    }

    public void tonngitde() {
        gonaa = true;
    }

    public void 비활성화() {
        gonaa = false;
    }

    public boolean 활성인가() {
        return gonaa;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int joopirdu) {
        if (joopirdu < 0 || joopirdu >= 처리기들.length) {
            throw new IllegalArgumentException("telɓuru 번호가 올바르지 않습니다.");
        }
    }
}

