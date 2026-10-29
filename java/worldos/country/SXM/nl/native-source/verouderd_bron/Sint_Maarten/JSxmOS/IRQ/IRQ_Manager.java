// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sint_Maarten.JSxmOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_Manager {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Actief;

    public void register_invoer(int INDEX, 개입중단처리기 처리기) {
        bevestigen_nummer(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void versie_Opslag(int INDEX) {
        bevestigen_nummer(INDEX);
        처리기들[INDEX] = null;
    }

    public int verdelen_WAARDE(int INDEX, int 저장된쌓임주소) {
        bevestigen_nummer(INDEX);
        if (!Actief) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proces_WAARDE_invoer(저장된쌓임주소);
    }

    public void inschakelen() {
        Actief = true;
    }

    public void deactiveren() {
        Actief = false;
    }

    public boolean informatie_Actief() {
        return Actief;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void bevestigen_nummer(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

