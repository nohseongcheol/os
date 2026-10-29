// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.فائل_سسٹم;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 فائل 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final فائل_سسٹم.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(فائل_سسٹم.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final فائل_سسٹم فائل_سسٹم;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(فائل_سسٹم فائل_سسٹم) {
        this.فائل_سسٹم = فائل_سسٹم;
    }

    public int بنڑاؤ(String ناں) {
        فائل_سسٹم.열린파일 열린파일 = فائل_سسٹم.بنڑاؤ(ناں);
        if (열린파일 == null) {
            return -2;
        }
        int اشاریہ = خالی_اشاریہ(3);
        if (اشاریہ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(اشاریہ), new 서술자(열린파일));
        return اشاریہ;
    }

    public int 읽기(int اشاریہ, byte[] 받을곳, int سائز) {
        서술자 داخلہ_قدر = 서술자들.get(Integer.valueOf(اشاریہ));
        if (داخلہ_قدر == null) {
            return -9;
        }
        if (سائز < 0 || سائز > 받을곳.length) {
            return -22;
        }
        int 남음 = داخلہ_قدر.열린파일.کوائف.length - داخلہ_قدر.열린파일.위치;
        int 읽을크기 = Math.min(سائز, Math.max(남음, 0));
        System.arraycopy(داخلہ_قدر.열린파일.کوائف, داخلہ_قدر.열린파일.위치, 받을곳, 0, 읽을크기);
        داخلہ_قدر.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int اشاریہ, int 거리, int 기준) {
        서술자 داخلہ_قدر = 서술자들.get(Integer.valueOf(اشاریہ));
        if (داخلہ_قدر == null) {
            return -9;
        }
        int پس_منظر_قدر;
        if (기준 == 0) {
            پس_منظر_قدر = 0;
        } else if (기준 == 1) {
            پس_منظر_قدر = داخلہ_قدر.열린파일.위치;
        } else if (기준 == 2) {
            پس_منظر_قدر = داخلہ_قدر.열린파일.کوائف.length;
        } else {
            return -22;
        }
        int 새위치 = پس_منظر_قدر + 거리;
        if (새위치 < 0) {
            return -22;
        }
        داخلہ_قدر.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int بند_کرو(int اشاریہ) {
        서술자 داخلہ_قدر = 서술자들.remove(Integer.valueOf(اشاریہ));
        if (داخلہ_قدر == null) {
            return -9;
        }
        داخلہ_قدر.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int اشاریہ, int 최소번호) {
        서술자 داخلہ_قدر = 서술자들.get(Integer.valueOf(اشاریہ));
        if (داخلہ_قدر == null) {
            return -9;
        }
        int 새번호 = خالی_اشاریہ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        داخلہ_قدر.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(داخلہ_قدر.열린파일));
        return 새번호;
    }

    public int 지정복제(int اشاریہ, int 새번호) {
        if (اشاریہ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(اشاریہ)) ? اشاریہ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(اشاریہ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            بند_کرو(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int اشاریہ, boolean قدر) {
        서술자 داخلہ_قدر = 서술자들.get(Integer.valueOf(اشاریہ));
        if (داخلہ_قدر == null) {
            return -9;
        }
        داخلہ_قدر.실행시닫기 = قدر;
        return 0;
    }

    public int 실행시닫기값(int اشاریہ) {
        서술자 داخلہ_قدر = 서술자들.get(Integer.valueOf(اشاریہ));
        if (داخلہ_قدر == null) {
            return -9;
        }
        return داخلہ_قدر.실행시닫기 ? 1 : 0;
    }

    public فائل_معلومات سسٹم_دی_معلومات(int اشاریہ) {
        if (اشاریہ >= 0 && اشاریہ <= 2) {
            return new فائل_معلومات(0, 0020666);
        }
        서술자 داخلہ_قدر = 서술자들.get(Integer.valueOf(اشاریہ));
        if (داخلہ_قدر == null) {
            return null;
        }
        return new فائل_معلومات(داخلہ_قدر.열린파일.کوائف.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer اشاریہ : 번호들) {
            서술자 داخلہ_قدر = 서술자들.get(اشاریہ);
            if (داخلہ_قدر != null && داخلہ_قدر.실행시닫기) {
                بند_کرو(اشاریہ.intValue());
            }
        }
    }

    public boolean 열려있음(int اشاریہ) {
        return 서술자들.containsKey(Integer.valueOf(اشاریہ));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(فائل_سسٹم);
        for (Map.Entry<Integer, 서술자> داخلہ_قدر : 서술자들.entrySet()) {
            داخلہ_قدر.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(داخلہ_قدر.getValue().열린파일);
            새서술자.실행시닫기 = داخلہ_قدر.getValue().실행시닫기;
            결과.서술자들.put(داخلہ_قدر.getKey(), 새서술자);
        }
        return 결과;
    }

    private int خالی_اشاریہ(int 최소번호) {
        for (int اشاریہ = Math.max(0, 최소번호); اشاریہ < 최대서술자; اشاریہ++) {
            if (!서술자들.containsKey(Integer.valueOf(اشاریہ))) {
                return اشاریہ;
            }
        }
        return -1;
    }
}
