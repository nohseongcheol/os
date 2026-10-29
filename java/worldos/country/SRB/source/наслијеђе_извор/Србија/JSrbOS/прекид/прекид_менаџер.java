// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.прекид;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class прекид_менаџер {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Активан;

    public void регистровати_унос(int индекс, 개입중단처리기 처리기) {
        번호확인(индекс);
        처리기들[индекс] = 처리기;
    }

    public void издање_похрана(int индекс) {
        번호확인(индекс);
        처리기들[индекс] = null;
    }

    public int дистрибуирати_вриједност(int индекс, int 저장된쌓임주소) {
        번호확인(индекс);
        if (!Активан) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[индекс];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Процес_вриједност_унос(저장된쌓임주소);
    }

    public void укључити() {
        Активан = true;
    }

    public void деактивирати() {
        Активан = false;
    }

    public boolean информатичко_одељење_Активан() {
        return Активан;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int индекс) {
        if (индекс < 0 || индекс >= 처리기들.length) {
            throw new IllegalArgumentException("прекид 번호가 올바르지 않습니다.");
        }
    }
}

