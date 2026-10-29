// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.רשת_רמז;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP לקבל_ערך_cef4d8ab 분배를 한곳에서 관리한다. */
public final class שכבת_רשת {
    @FunctionalInterface
    public interface 자료처리기 {
        void תהליך_ערך_ערך(byte[] נתונים, int הפעלה, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void אוגר_פרוטוקול_אינטרנט(int ערך_חוזה, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ערך_חוזה & 0xff), 처리기);
    }

    public void אוגר_משתמש_נתונים_יחידה(int חומרה_הסב, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(חומרה_הסב & 0xffff), 처리기);
    }

    public void 전송제어등록(int חומרה_הסב, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(חומרה_הסב & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] למסגר_מדד) {
        if (!רשת_כלים.이더넷틀인가(למסגר_מדד)) {
            return false;
        }
        int 종류 = רשת_כלים.이더넷상위규약(למסגר_מדד);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.תהליך_ערך_ערך(למסגר_מדד, 14, למסגר_מדד.length - 14);
            return true;
        }
        return 종류 == 0x0800 && לקבל_ענן_מנה(למסגר_מדד, 14);
    }

    private boolean לקבל_ענן_מנה(byte[] נתונים, int הפעלה) {
        if (!רשת_כלים.מערכות_מידע_חיסון_נגד_פוליו_4_פרוטוקול(נתונים, הפעלה)) {
            return false;
        }
        int 머리길이 = (נתונים[הפעלה] & 0x0f) * 4;
        int 전체길이 = רשת_כלים.큰순서짧은정수(נתונים, הפעלה + 2);
        if (전체길이 < 머리길이 || הפעלה + 전체길이 > נתונים.length) {
            return false;
        }
        int ערך_חוזה = נתונים[הפעלה + 9] & 0xff;
        int תוכן_התחל = הפעלה + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ערך_חוזה));
        if (직접처리기 != null) {
            직접처리기.תהליך_ערך_ערך(נתונים, תוכן_התחל, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int יעד_מספר_יציאה = רשת_כלים.큰순서짧은정수(נתונים, תוכן_התחל + 2);
        Map<Integer, 자료처리기> הסב_טבלה = ערך_חוזה == 17 ? 사용자자료단위처리기 : ערך_חוזה == 6 ? 전송제어처리기 : null;
        if (הסב_טבלה == null) {
            return false;
        }
        자료처리기 포트처리기 = הסב_טבלה.get(Integer.valueOf(יעד_מספר_יציאה));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.תהליך_ערך_ערך(נתונים, תוכן_התחל, 내용길이);
        return true;
    }
}

