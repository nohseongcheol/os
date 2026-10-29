// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.מערכת_קבצים;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 קובץ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final מערכת_קבצים.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(מערכת_קבצים.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final מערכת_קבצים מערכת_קבצים;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(מערכת_קבצים מערכת_קבצים) {
        this.מערכת_קבצים = מערכת_קבצים;
    }

    public int פתח(String שם) {
        מערכת_קבצים.열린파일 열린파일 = מערכת_קבצים.פתח(שם);
        if (열린파일 == null) {
            return -2;
        }
        int מדד = ריק_מדד(3);
        if (מדד < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(מדד), new 서술자(열린파일));
        return מדד;
    }

    public int קרא(int מדד, byte[] לקבל_יעד, int גודל) {
        서술자 ערך_ערך = 서술자들.get(Integer.valueOf(מדד));
        if (ערך_ערך == null) {
            return -9;
        }
        if (גודל < 0 || גודל > לקבל_יעד.length) {
            return -22;
        }
        int 남음 = ערך_ערך.열린파일.נתונים.length - ערך_ערך.열린파일.מיקום;
        int 읽을크기 = Math.min(גודל, Math.max(남음, 0));
        System.arraycopy(ערך_ערך.열린파일.נתונים, ערך_ערך.열린파일.מיקום, לקבל_יעד, 0, 읽을크기);
        ערך_ערך.열린파일.מיקום += 읽을크기;
        return 읽을크기;
    }

    public int להעביר_עמדה(int מדד, int 거리, int לשקף_בסיס) {
        서술자 ערך_ערך = 서술자들.get(Integer.valueOf(מדד));
        if (ערך_ערך == null) {
            return -9;
        }
        int טפט_ערך;
        if (לשקף_בסיס == 0) {
            טפט_ערך = 0;
        } else if (לשקף_בסיס == 1) {
            טפט_ערך = ערך_ערך.열린파일.מיקום;
        } else if (לשקף_בסיס == 2) {
            טפט_ערך = ערך_ערך.열린파일.נתונים.length;
        } else {
            return -22;
        }
        int 새위치 = טפט_ערך + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ערך_ערך.열린파일.מיקום = 새위치;
        return 새위치;
    }

    public int סגירה(int מדד) {
        서술자 ערך_ערך = 서술자들.remove(Integer.valueOf(מדד));
        if (ערך_ערך == null) {
            return -9;
        }
        ערך_ערך.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int מדד, int 최소번호) {
        서술자 ערך_ערך = 서술자들.get(Integer.valueOf(מדד));
        if (ערך_ערך == null) {
            return -9;
        }
        int מספר_חדש = ריק_מדד(최소번호);
        if (מספר_חדש < 0) {
            return -24;
        }
        ערך_ערך.열린파일.참조수++;
        서술자들.put(Integer.valueOf(מספר_חדש), new 서술자(ערך_ערך.열린파일));
        return מספר_חדש;
    }

    public int 지정복제(int מדד, int מספר_חדש) {
        if (מדד == מספר_חדש) {
            return 서술자들.containsKey(Integer.valueOf(מדד)) ? מדד : -9;
        }
        if (מספר_חדש < 0 || מספר_חדש >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(מדד));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(מספר_חדש))) {
            סגירה(מספר_חדש);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(מספר_חדש), new 서술자(원본.열린파일));
        return מספר_חדש;
    }

    public int 실행시닫기설정(int מדד, boolean ערך) {
        서술자 ערך_ערך = 서술자들.get(Integer.valueOf(מדד));
        if (ערך_ערך == null) {
            return -9;
        }
        ערך_ערך.실행시닫기 = ערך;
        return 0;
    }

    public int 실행시닫기값(int מדד) {
        서술자 ערך_ערך = 서술자들.get(Integer.valueOf(מדד));
        if (ערך_ערך == null) {
            return -9;
        }
        return ערך_ערך.실행시닫기 ? 1 : 0;
    }

    public קובץ_מידע מידע_מערכת(int מדד) {
        if (מדד >= 0 && מדד <= 2) {
            return new קובץ_מידע(0, 0020666);
        }
        서술자 ערך_ערך = 서술자들.get(Integer.valueOf(מדד));
        if (ערך_ערך == null) {
            return null;
        }
        return new קובץ_מידע(ערך_ערך.열린파일.נתונים.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer מדד : 번호들) {
            서술자 ערך_ערך = 서술자들.get(מדד);
            if (ערך_ערך != null && ערך_ערך.실행시닫기) {
                סגירה(מדד.intValue());
            }
        }
    }

    public boolean מערכות_מידע_פתח(int מדד) {
        return 서술자들.containsKey(Integer.valueOf(מדד));
    }

    public 파일서술자표 לשכפל_ערך() {
        파일서술자표 תוצאה = new 파일서술자표(מערכת_קבצים);
        for (Map.Entry<Integer, 서술자> ערך_ערך : 서술자들.entrySet()) {
            ערך_ערך.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ערך_ערך.getValue().열린파일);
            새서술자.실행시닫기 = ערך_ערך.getValue().실행시닫기;
            תוצאה.서술자들.put(ערך_ערך.getKey(), 새서술자);
        }
        return תוצאה;
    }

    private int ריק_מדד(int 최소번호) {
        for (int מדד = Math.max(0, 최소번호); מדד < 최대서술자; מדד++) {
            if (!서술자들.containsKey(Integer.valueOf(מדד))) {
                return מדד;
            }
        }
        return -1;
    }
}
