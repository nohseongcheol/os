// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Словаччина.JSvkOS.переривання;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class 개입중단관리자 {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Активний;

    public void реєстр_запис(int індекс, 개입중단처리기 처리기) {
        번호확인(індекс);
        처리기들[індекс] = 처리기;
    }

    public void випуск_місце(int індекс) {
        번호확인(індекс);
        처리기들[індекс] = null;
    }

    public int поширювати_значення(int індекс, int 저장된쌓임주소) {
        번호확인(індекс);
        if (!Активний) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[індекс];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.процес_значення_запис(저장된쌓임주소);
    }

    public void вмикати() {
        Активний = true;
    }

    public void вимикати() {
        Активний = false;
    }

    public boolean ІТ_відділ_Активний() {
        return Активний;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int індекс) {
        if (індекс < 0 || індекс >= 처리기들.length) {
            throw new IllegalArgumentException("переривання 번호가 올바르지 않습니다.");
        }
    }
}

