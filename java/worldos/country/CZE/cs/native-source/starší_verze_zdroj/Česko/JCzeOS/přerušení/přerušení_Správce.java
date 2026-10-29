// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.přerušení;

import java.util.Arrays;

/** IDT의 Java 관리 측 obslužná_rutina 등록과 분배를 담당한다. */
public final class přerušení_Správce {
    private final přerušení_obslužná_rutina[] obslužná_rutina_Seznam = new přerušení_obslužná_rutina[256];
    private boolean Aktivní;

    public void registr_položka(int INDEX, přerušení_obslužná_rutina obslužná_rutina) {
        ověřit_číslo(INDEX);
        obslužná_rutina_Seznam[INDEX] = obslužná_rutina;
    }

    public void verze_Storage(int INDEX) {
        ověřit_číslo(INDEX);
        obslužná_rutina_Seznam[INDEX] = null;
    }

    public int distribuovat_HODNOTA(int INDEX, int 저장된쌓임주소) {
        ověřit_číslo(INDEX);
        if (!Aktivní) {
            return 저장된쌓임주소;
        }
        přerušení_obslužná_rutina obslužná_rutina = obslužná_rutina_Seznam[INDEX];
        return obslužná_rutina == null ? 저장된쌓임주소 : obslužná_rutina.Proces_HODNOTA_položka(저장된쌓임주소);
    }

    public void povolit() {
        Aktivní = true;
    }

    public void pozastavit() {
        Aktivní = false;
    }

    public boolean informační_systémy_Aktivní() {
        return Aktivní;
    }

    public void 모두해제() {
        Arrays.fill(obslužná_rutina_Seznam, null);
    }

    private void ověřit_číslo(int INDEX) {
        if (INDEX < 0 || INDEX >= obslužná_rutina_Seznam.length) {
            throw new IllegalArgumentException("přerušení 번호가 올바르지 않습니다.");
        }
    }
}

