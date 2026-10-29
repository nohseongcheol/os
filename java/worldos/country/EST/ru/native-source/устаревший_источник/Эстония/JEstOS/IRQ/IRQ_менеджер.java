// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Эстония.JEstOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 обработчик 등록과 분배를 담당한다. */
public final class IRQ_менеджер {
    private final IRQ_обработчик[] обработчик_Список = new IRQ_обработчик[256];
    private boolean В_сети;

    public void регистр_ввод(int ИНДЕКС, IRQ_обработчик обработчик) {
        번호확인(ИНДЕКС);
        обработчик_Список[ИНДЕКС] = обработчик;
    }

    public void выпуск_Память_293182ec(int ИНДЕКС) {
        번호확인(ИНДЕКС);
        обработчик_Список[ИНДЕКС] = null;
    }

    public int распределять_ЗНАЧЕН(int ИНДЕКС, int 저장된쌓임주소) {
        번호확인(ИНДЕКС);
        if (!В_сети) {
            return 저장된쌓임주소;
        }
        IRQ_обработчик обработчик = обработчик_Список[ИНДЕКС];
        return обработчик == null ? 저장된쌓임주소 : обработчик.Процесс_ЗНАЧЕН_ввод(저장된쌓임주소);
    }

    public void включить() {
        В_сети = true;
    }

    public void отключить_9fd8413e() {
        В_сети = false;
    }

    public boolean ИТ_службы_В_сети() {
        return В_сети;
    }

    public void 모두해제() {
        Arrays.fill(обработчик_Список, null);
    }

    private void 번호확인(int ИНДЕКС) {
        if (ИНДЕКС < 0 || ИНДЕКС >= обработчик_Список.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

