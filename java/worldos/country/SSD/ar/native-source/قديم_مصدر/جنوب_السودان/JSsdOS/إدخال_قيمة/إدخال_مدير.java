// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جنوب_السودان.JSsdOS.إدخال_قيمة;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 رمز_قيمة_f3cd31ee 사이에서 إدخال_قيمة 사건을 안전하게 넘긴다. */
public final class إدخال_مدير {
    private final Queue<إدخال_حدث> أحداث_قائمة = new ArrayDeque<إدخال_حدث>();
    private final int 최대사건수;
    private int 버린사건수;

    public إدخال_مدير(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("حدث 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void مفتاح_متوقف_عن_التشغيل(int مفتاح_بيانات) {
        넣기(new إدخال_حدث(إدخال_حدث.종류.مفتاح_متوقف_عن_التشغيل, مفتاح_بيانات & 0xff, 0));
    }

    public synchronized void 키놓음(int مفتاح_بيانات) {
        넣기(new إدخال_حدث(إدخال_حدث.종류.키놓음, مفتاح_بيانات & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int عمودي_منصب) {
        넣기(new إدخال_حدث(إدخال_حدث.종류.쥐이동, 가로, عمودي_منصب));
    }

    public synchronized إدخال_حدث التالي_حدث() {
        return أحداث_قائمة.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(إدخال_حدث حدث) {
        if (أحداث_قائمة.size() == 최대사건수) {
            أحداث_قائمة.poll();
            버린사건수++;
        }
        أحداث_قائمة.offer(حدث);
    }
}

