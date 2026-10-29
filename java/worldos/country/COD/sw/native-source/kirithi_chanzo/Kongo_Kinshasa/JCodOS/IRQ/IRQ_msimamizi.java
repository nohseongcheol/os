// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kongo_Kinshasa.JCodOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_msimamizi {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Amilifu;

    public void sajili_ingizo(int kielezo, 개입중단처리기 처리기) {
        번호확인(kielezo);
        처리기들[kielezo] = 처리기;
    }

    public void toleo_Hifadhi(int kielezo) {
        번호확인(kielezo);
        처리기들[kielezo] = null;
    }

    public int sambaza_thamani(int kielezo, int 저장된쌓임주소) {
        번호확인(kielezo);
        if (!Amilifu) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[kielezo];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Mchakato_thamani_ingizo(저장된쌓임주소);
    }

    public void washa() {
        Amilifu = true;
    }

    public void lemaza() {
        Amilifu = false;
    }

    public boolean teknolojia_ya_maelezo_Amilifu() {
        return Amilifu;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int kielezo) {
        if (kielezo < 0 || kielezo >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

