// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.ליבה;

import ישראל.JIsrOS.זיכרון_אזור.זיכרון_מנהל;
import ישראל.JIsrOS.זיכרון_אזור.דף_מנהל;
import ישראל.JIsrOS.קלט_ערך.קלט_מנהל;
import ישראל.JIsrOS.작업.תהליך_ערך;
import ישראל.JIsrOS.작업.מתזמן;
import ישראל.JIsrOS.체계호출.체계호출;
import ישראל.JIsrOS.מערכת_קבצים.파일서술자표;
import ישראל.JIsrOS.מערכת_קבצים.מערכת_קבצים;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ליבה {
    private final חומרה_ערך_9591fb0a התקן_ערך_e13f0cd9;
    private final זיכרון_מנהל זיכרון_אזור = new זיכרון_מנהל(32 * 1024 * 1024);
    private final דף_מנהל 쪽관리 = new דף_מנהל();
    private final מערכת_קבצים מערכת_קבצים = new מערכת_קבצים();
    private final מתזמן מתזמן = new מתזמן(쪽관리);
    private final קלט_מנהל 입력관리 = new קלט_מנהל(256);
    private final תהליך_ערך 첫과정;
    private final 체계호출 체계호출;

    public ליבה(חומרה_ערך_9591fb0a התקן_ערך_e13f0cd9) {
        this.התקן_ערך_e13f0cd9 = התקן_ערך_e13f0cd9;
        첫과정 = מתזמן.첫과정(new 파일서술자표(מערכת_קבצים));
        체계호출 = new 체계호출(מערכת_קבצים, 쪽관리, מתזמן, התקן_ערך_e13f0cd9, 입력관리);
    }

    public void הפעלה() {
        התקן_ערך_e13f0cd9.직렬출력("=== JIsrOS 관리 ליבה_ערך ===\n");
    }

    public void לבצע_צעד() {
        התקן_ערך_e13f0cd9.중앙처리장치멈춤();
    }

    public זיכרון_מנהל זיכרון_אזור() {
        return זיכרון_אזור;
    }

    public דף_מנהל 쪽관리() {
        return 쪽관리;
    }

    public מערכת_קבצים מערכת_קבצים() {
        return מערכת_קבצים;
    }

    public מתזמן מתזמן() {
        return מתזמן;
    }

    public קלט_מנהל 입력관리() {
        return 입력관리;
    }

    public תהליך_ערך 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
