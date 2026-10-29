// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польшча.JPolOS.Сховішча_прылада;

import java.util.Arrays;

/** ATA 28비트 Загад 계층과 같은 512바이트 논리 секцыя_значэнне 장치다. */
public final class 고급기술결합장치 {
    public static final int секцыя_памер = 512;
    private final byte[] дадзеныя;
    private final boolean толькі_для_чытання_значэнне;

    public 고급기술결합장치(int 구역수, boolean толькі_для_чытання_значэнне) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("секцыя_значэнне 수가 올바르지 않습니다.");
        }
        дадзеныя = new byte[Math.multiplyExact(구역수, секцыя_памер)];
        this.толькі_для_чытання_значэнне = толькі_для_чытання_значэнне;
    }

    public int 구역수() {
        return дадзеныя.length / секцыя_памер;
    }

    public void Чытанне(int секцыя_індэкс, byte[] 받을곳) {
        범위확인(секцыя_індэкс, 받을곳);
        System.arraycopy(дадзеныя, секцыя_індэкс * секцыя_памер, 받을곳, 0, секцыя_памер);
    }

    public void Запіс(int секцыя_індэкс, byte[] 쓸자료) {
        if (толькі_для_чытання_значэнне) {
            throw new IllegalStateException("Чытанне 전용 장치입니다.");
        }
        범위확인(секцыя_індэкс, 쓸자료);
        System.arraycopy(쓸자료, 0, дадзеныя, секцыя_індэкс * секцыя_памер, секцыя_памер);
    }

    public void ачысціць_увядзенне() {
        if (толькі_для_чытання_значэнне) {
            throw new IllegalStateException("Чытанне 전용 장치입니다.");
        }
        Arrays.fill(дадзеныя, (byte) 0);
    }

    private void 범위확인(int секцыя_індэкс, byte[] 임시공간) {
        if (секцыя_індэкс < 0 || секцыя_індэкс >= 구역수() || 임시공간.length < секцыя_памер) {
            throw new IllegalArgumentException("ATA секцыя_значэнне 범위가 올바르지 않습니다.");
        }
    }
}

