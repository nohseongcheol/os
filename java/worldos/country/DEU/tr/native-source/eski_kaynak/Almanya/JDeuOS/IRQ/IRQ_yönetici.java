// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Almanya.JDeuOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 işleyici 등록과 분배를 담당한다. */
public final class IRQ_yönetici {
    private final IRQ_işleyici[] işleyici_Liste = new IRQ_işleyici[256];
    private boolean Aktif;

    public void yazmaç_girdi(int Dizin, IRQ_işleyici işleyici) {
        번호확인(Dizin);
        işleyici_Liste[Dizin] = işleyici;
    }

    public void sürüm_Depolama(int Dizin) {
        번호확인(Dizin);
        işleyici_Liste[Dizin] = null;
    }

    public int dağıtmak_değer(int Dizin, int 저장된쌓임주소) {
        번호확인(Dizin);
        if (!Aktif) {
            return 저장된쌓임주소;
        }
        IRQ_işleyici işleyici = işleyici_Liste[Dizin];
        return işleyici == null ? 저장된쌓임주소 : işleyici.işlem_değer_girdi(저장된쌓임주소);
    }

    public void açmak() {
        Aktif = true;
    }

    public void devre_dışı_bırakmak() {
        Aktif = false;
    }

    public boolean bilgi_teknolojisi_Aktif() {
        return Aktif;
    }

    public void 모두해제() {
        Arrays.fill(işleyici_Liste, null);
    }

    private void 번호확인(int Dizin) {
        if (Dizin < 0 || Dizin >= işleyici_Liste.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

