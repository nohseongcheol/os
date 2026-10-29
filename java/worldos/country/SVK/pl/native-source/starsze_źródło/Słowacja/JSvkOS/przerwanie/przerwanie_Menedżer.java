// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Słowacja.JSvkOS.przerwanie;

import java.util.Arrays;

/** IDT의 Java 관리 측 procedura_obsługi 등록과 분배를 담당한다. */
public final class przerwanie_Menedżer {
    private final przerwanie_procedura_obsługi[] procedura_obsługi_Lista = new przerwanie_procedura_obsługi[256];
    private boolean Aktywny;

    public void rejestr_wpis(int INDEKS, przerwanie_procedura_obsługi procedura_obsługi) {
        번호확인(INDEKS);
        procedura_obsługi_Lista[INDEKS] = procedura_obsługi;
    }

    public void wersja_Pamięć(int INDEKS) {
        번호확인(INDEKS);
        procedura_obsługi_Lista[INDEKS] = null;
    }

    public int rozproszony_WARTOŚĆ(int INDEKS, int 저장된쌓임주소) {
        번호확인(INDEKS);
        if (!Aktywny) {
            return 저장된쌓임주소;
        }
        przerwanie_procedura_obsługi procedura_obsługi = procedura_obsługi_Lista[INDEKS];
        return procedura_obsługi == null ? 저장된쌓임주소 : procedura_obsługi.Proces_WARTOŚĆ_wpis(저장된쌓임주소);
    }

    public void włączyć() {
        Aktywny = true;
    }

    public void dezaktywować() {
        Aktywny = false;
    }

    public boolean systemy_informacyjne_Aktywny() {
        return Aktywny;
    }

    public void 모두해제() {
        Arrays.fill(procedura_obsługi_Lista, null);
    }

    private void 번호확인(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= procedura_obsługi_Lista.length) {
            throw new IllegalArgumentException("przerwanie 번호가 올바르지 않습니다.");
        }
    }
}

