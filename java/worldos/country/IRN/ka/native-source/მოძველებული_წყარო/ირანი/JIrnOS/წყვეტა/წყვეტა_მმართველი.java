// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ირანი.JIrnOS.წყვეტა;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class წყვეტა_მმართველი {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean აქტიური;

    public void დარეგისტრირება_შენატანი(int ინდექსი, 개입중단처리기 처리기) {
        번호확인(ინდექსი);
        처리기들[ინდექსი] = 처리기;
    }

    public void რელიზი_საცავი(int ინდექსი) {
        번호확인(ინდექსი);
        처리기들[ინდექსი] = null;
    }

    public int დისტრიბუცია_მნიშვნელობა(int ინდექსი, int 저장된쌓임주소) {
        번호확인(ინდექსი);
        if (!აქტიური) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ინდექსი];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.პროცესი_მნიშვნელობა_შენატანი(저장된쌓임주소);
    }

    public void ჩართვა() {
        აქტიური = true;
    }

    public void დეაქტივაცია() {
        აქტიური = false;
    }

    public boolean 활성인가() {
        return აქტიური;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ინდექსი) {
        if (ინდექსი < 0 || ინდექსი >= 처리기들.length) {
            throw new IllegalArgumentException("წყვეტა 번호가 올바르지 않습니다.");
        }
    }
}

