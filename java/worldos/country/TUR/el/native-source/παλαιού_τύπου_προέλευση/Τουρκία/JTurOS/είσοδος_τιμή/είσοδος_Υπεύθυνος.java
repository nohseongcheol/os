// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Τουρκία.JTurOS.είσοδος_τιμή;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 κωδικός_τιμή 사이에서 είσοδος_τιμή 사건을 안전하게 넘긴다. */
public final class είσοδος_Υπεύθυνος {
    private final Queue<είσοδος_συμβάν> Εκδηλώσεις_Λίστα = new ArrayDeque<είσοδος_συμβάν>();
    private final int 최대사건수;
    private int 버린사건수;

    public είσοδος_Υπεύθυνος(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Συμβάν 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Κλειδί_εκτός_λειτουργίας(int Κλειδί_δεδομένα) {
        넣기(new είσοδος_συμβάν(είσοδος_συμβάν.종류.Κλειδί_εκτός_λειτουργίας, Κλειδί_δεδομένα & 0xff, 0));
    }

    public synchronized void 키놓음(int Κλειδί_δεδομένα) {
        넣기(new είσοδος_συμβάν(είσοδος_συμβάν.종류.키놓음, Κλειδί_δεδομένα & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int τομέας_θέση) {
        넣기(new είσοδος_συμβάν(είσοδος_συμβάν.종류.쥐이동, 가로, τομέας_θέση));
    }

    public synchronized είσοδος_συμβάν Επόμενο_συμβάν() {
        return Εκδηλώσεις_Λίστα.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(είσοδος_συμβάν Συμβάν) {
        if (Εκδηλώσεις_Λίστα.size() == 최대사건수) {
            Εκδηλώσεις_Λίστα.poll();
            버린사건수++;
        }
        Εκδηλώσεις_Λίστα.offer(Συμβάν);
    }
}

