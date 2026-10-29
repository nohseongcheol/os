// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Түркия.JTurOS.үзгіш;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class үзгіш_менеджер {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean желіде;

    public void тіркеу_енгізу(int индекс, 개입중단처리기 처리기) {
        번호확인(индекс);
        처리기들[индекс] = 처리기;
    }

    public void шығарылым_Жад(int индекс) {
        번호확인(индекс);
        처리기들[индекс] = null;
    }

    public int үлестіру_мән(int индекс, int 저장된쌓임주소) {
        번호확인(индекс);
        if (!желіде) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[индекс];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Процесс_мән_енгізу(저장된쌓임주소);
    }

    public void қосу_0b9ce0d7() {
        желіде = true;
    }

    public void ажырату_9fd8413e() {
        желіде = false;
    }

    public boolean ақпараттық_жүйелер_желіде() {
        return желіде;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int индекс) {
        if (индекс < 0 || индекс >= 처리기들.length) {
            throw new IllegalArgumentException("үзгіш 번호가 올바르지 않습니다.");
        }
    }
}

