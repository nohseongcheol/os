// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 behandlingsprogram 등록과 분배를 담당한다. */
public final class IRQ_overordnet {
    private final IRQ_behandlingsprogram[] behandlingsprogram_Liste = new IRQ_behandlingsprogram[256];
    private boolean Aktiv;

    public void register_oppføring(int INDEKS, IRQ_behandlingsprogram behandlingsprogram) {
        bekrefte_nummer(INDEKS);
        behandlingsprogram_Liste[INDEKS] = behandlingsprogram;
    }

    public void frigi_lager(int INDEKS) {
        bekrefte_nummer(INDEKS);
        behandlingsprogram_Liste[INDEKS] = null;
    }

    public int distribuere_VERDI(int INDEKS, int 저장된쌓임주소) {
        bekrefte_nummer(INDEKS);
        if (!Aktiv) {
            return 저장된쌓임주소;
        }
        IRQ_behandlingsprogram behandlingsprogram = behandlingsprogram_Liste[INDEKS];
        return behandlingsprogram == null ? 저장된쌓임주소 : behandlingsprogram.Prosess_VERDI_oppføring(저장된쌓임주소);
    }

    public void aktivere() {
        Aktiv = true;
    }

    public void deaktivere() {
        Aktiv = false;
    }

    public boolean informasjonssystemer_Aktiv() {
        return Aktiv;
    }

    public void 모두해제() {
        Arrays.fill(behandlingsprogram_Liste, null);
    }

    private void bekrefte_nummer(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= behandlingsprogram_Liste.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

