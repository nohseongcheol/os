// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederland.JNldOS.invoer_WAARDE;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 CODE_WAARDE 사이에서 invoer_WAARDE 사건을 안전하게 넘긴다. */
public final class invoer_Manager {
    private final Queue<invoergebeurtenis> Evenementen_Lijst = new ArrayDeque<invoergebeurtenis>();
    private final int 최대사건수;
    private int 버린사건수;

    public invoer_Manager(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Gebeurtenis 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void toets_offline(int toets_gegevens) {
        넣기(new invoergebeurtenis(invoergebeurtenis.soort_WAARDE.toets_offline, toets_gegevens & 0xff, 0));
    }

    public synchronized void 키놓음(int toets_gegevens) {
        넣기(new invoergebeurtenis(invoergebeurtenis.soort_WAARDE.키놓음, toets_gegevens & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Verticaal_functie) {
        넣기(new invoergebeurtenis(invoergebeurtenis.soort_WAARDE.쥐이동, 가로, Verticaal_functie));
    }

    public synchronized invoergebeurtenis Volgende_gebeurtenis() {
        return Evenementen_Lijst.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(invoergebeurtenis Gebeurtenis) {
        if (Evenementen_Lijst.size() == 최대사건수) {
            Evenementen_Lijst.poll();
            버린사건수++;
        }
        Evenementen_Lijst.offer(Gebeurtenis);
    }
}

