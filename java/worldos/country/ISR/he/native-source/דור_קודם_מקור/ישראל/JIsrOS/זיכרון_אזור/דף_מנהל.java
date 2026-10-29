// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.זיכרון_אזור;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB דף_ערך 연결과 כתוב 시 복사를 제공한다. */
public final class דף_מנהל {
    public static final int גודל_עמוד = 4096;

    private static final class דף_ערך {
        private byte[] נתונים = new byte[גודל_עמוד];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean העתקה_בכתיבה;
    }

    public static final class למען_חלל {
        private final Map<Integer, דף_ערך> דף_טבלה = new HashMap<Integer, דף_ערך>();
    }

    public למען_חלל 새주소공간() {
        return new למען_חלל();
    }

    public void מפה_דף(למען_חלל למען_אזור, int כתובת_וירטואלית, boolean 쓰기가능) {
        int מדד = 쪽번호(כתובת_וירטואלית);
        דף_ערך 새쪽 = new דף_ערך();
        새쪽.쓰기가능 = 쓰기가능;
        למען_אזור.דף_טבלה.put(Integer.valueOf(מדד), 새쪽);
    }

    public למען_חלל לשכפל_העתקה_בכתיבה(למען_חלל 원본) {
        למען_חלל 복제본 = new למען_חלל();
        for (Map.Entry<Integer, דף_ערך> ערך_ערך : 원본.דף_טבלה.entrySet()) {
            דף_ערך 공유쪽 = ערך_ערך.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.העתקה_בכתיבה = true;
            }
            복제본.דף_טבלה.put(ערך_ערך.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(למען_חלל למען_אזור, int כתובת_וירטואלית) {
        דף_ערך יעד = חפש_דף(למען_אזור, כתובת_וירטואלית);
        return יעד.נתונים[Math.floorMod(כתובת_וירטואלית, גודל_עמוד)];
    }

    public void כתיבה_בית_ערך(למען_חלל למען_אזור, int כתובת_וירטואלית, byte ערך) {
        int מדד = 쪽번호(כתובת_וירטואלית);
        דף_ערך יעד = חפש_דף(למען_אזור, כתובת_וירטואלית);
        if (!יעד.쓰기가능) {
            if (!יעד.העתקה_בכתיבה) {
                throw new IllegalStateException("קרא 전용 쪽입니다.");
            }
            יעד = ליצור_חסוי_דף(למען_אזור, מדד, יעד);
        }
        יעד.נתונים[Math.floorMod(כתובת_וירטואלית, גודל_עמוד)] = ערך;
    }

    public void חסוי_טווח_כתיבה(למען_חלל למען_אזור, int התחל_למען, int גודל) {
        if (גודל < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int כתובת_קצה = Math.addExact(התחל_למען, גודל);
        for (int למען = התחל_למען; למען < כתובת_קצה; למען = (쪽번호(למען) + 1) * גודל_עמוד) {
            int מדד = 쪽번호(למען);
            דף_ערך יעד = חפש_דף(למען_אזור, למען);
            if (יעד.העתקה_בכתיבה) {
                ליצור_חסוי_דף(למען_אזור, מדד, יעד);
            } else {
                יעד.쓰기가능 = true;
            }
        }
    }

    public void טווח_כתיבה(למען_חלל למען_אזור, int התחל_למען, byte[] נתונים) {
        for (int מדד = 0; מדד < נתונים.length; מדד++) {
            כתיבה_בית_ערך(למען_אזור, התחל_למען + מדד, נתונים[מדד]);
        }
    }

    private דף_ערך ליצור_חסוי_דף(למען_חלל למען_אזור, int מדד, דף_ערך 공유쪽) {
        דף_ערך חסוי_דף = new דף_ערך();
        חסוי_דף.נתונים = Arrays.copyOf(공유쪽.נתונים, 공유쪽.נתונים.length);
        חסוי_דף.쓰기가능 = true;
        חסוי_דף.העתקה_בכתיבה = false;
        공유쪽.참조수--;
        למען_אזור.דף_טבלה.put(Integer.valueOf(מדד), חסוי_דף);
        return חסוי_דף;
    }

    private דף_ערך חפש_דף(למען_חלל למען_אזור, int למען) {
        דף_ערך יעד = למען_אזור.דף_טבלה.get(Integer.valueOf(쪽번호(למען)));
        if (יעד == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return יעד;
    }

    private int 쪽번호(int למען) {
        if (למען < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return למען / גודל_עמוד;
    }
}

