// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_Valvoja {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktiivinen;

    public void rekisteri_merkintä(int INDEKSI, 개입중단처리기 처리기) {
        tarkistaa_numero(INDEKSI);
        처리기들[INDEKSI] = 처리기;
    }

    public void julkaista_Tallennus(int INDEKSI) {
        tarkistaa_numero(INDEKSI);
        처리기들[INDEKSI] = null;
    }

    public int jaa_ARVO(int INDEKSI, int 저장된쌓임주소) {
        tarkistaa_numero(INDEKSI);
        if (!Aktiivinen) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEKSI];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.prosessi_ARVO_merkintä(저장된쌓임주소);
    }

    public void ota_käyttöön() {
        Aktiivinen = true;
    }

    public void poistaa_aktivointi() {
        Aktiivinen = false;
    }

    public boolean tietojärjestelmät_Aktiivinen() {
        return Aktiivinen;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void tarkistaa_numero(int INDEKSI) {
        if (INDEKSI < 0 || INDEKSI >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

