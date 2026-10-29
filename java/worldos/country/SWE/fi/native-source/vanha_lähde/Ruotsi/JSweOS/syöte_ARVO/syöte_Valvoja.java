// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ruotsi.JSweOS.syöte_ARVO;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KOODI_ARVO 사이에서 syöte_ARVO 사건을 안전하게 넘긴다. */
public final class syöte_Valvoja {
    private final Queue<syöte_tapahtuma> Tapahtumat_luettelo = new ArrayDeque<syöte_tapahtuma>();
    private final int 최대사건수;
    private int 버린사건수;

    public syöte_Valvoja(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Tapahtuma 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Avain_ei_toiminnassa(int Avain_data) {
        넣기(new syöte_tapahtuma(syöte_tapahtuma.종류.Avain_ei_toiminnassa, Avain_data & 0xff, 0));
    }

    public synchronized void 키놓음(int Avain_data) {
        넣기(new syöte_tapahtuma(syöte_tapahtuma.종류.키놓음, Avain_data & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int toimiala_toimi) {
        넣기(new syöte_tapahtuma(syöte_tapahtuma.종류.쥐이동, 가로, toimiala_toimi));
    }

    public synchronized syöte_tapahtuma Seuraava_tapahtuma() {
        return Tapahtumat_luettelo.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(syöte_tapahtuma Tapahtuma) {
        if (Tapahtumat_luettelo.size() == 최대사건수) {
            Tapahtumat_luettelo.poll();
            버린사건수++;
        }
        Tapahtumat_luettelo.offer(Tapahtuma);
    }
}

