// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package फ़िजी.JFjiOS.फ़ाइल_सिस्टम;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 संचिका 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final फ़ाइल_सिस्टम.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(फ़ाइल_सिस्टम.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final फ़ाइल_सिस्टम फ़ाइल_सिस्टम;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(फ़ाइल_सिस्टम फ़ाइल_सिस्टम) {
        this.फ़ाइल_सिस्टम = फ़ाइल_सिस्टम;
    }

    public int खोलें(String नाम) {
        फ़ाइल_सिस्टम.열린파일 열린파일 = फ़ाइल_सिस्टम.खोलें(नाम);
        if (열린파일 == null) {
            return -2;
        }
        int इंडेक्स = 빈번호(3);
        if (इंडेक्स < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(इंडेक्स), new 서술자(열린파일));
        return इंडेक्स;
    }

    public int पढ़ें(int इंडेक्स, byte[] 받을곳, int आकार) {
        서술자 एन्ट्री_मान = 서술자들.get(Integer.valueOf(इंडेक्स));
        if (एन्ट्री_मान == null) {
            return -9;
        }
        if (आकार < 0 || आकार > 받을곳.length) {
            return -22;
        }
        int 남음 = एन्ट्री_मान.열린파일.आँकड़े.length - एन्ट्री_मान.열린파일.स्थान;
        int पढें_आकार = Math.min(आकार, Math.max(남음, 0));
        System.arraycopy(एन्ट्री_मान.열린파일.आँकड़े, एन्ट्री_मान.열린파일.स्थान, 받을곳, 0, पढें_आकार);
        एन्ट्री_मान.열린파일.स्थान += पढें_आकार;
        return पढें_आकार;
    }

    public int ले_जाएँ_पद(int इंडेक्स, int 거리, int प्रोजेक्ट_करें_मूल) {
        서술자 एन्ट्री_मान = 서술자들.get(Integer.valueOf(इंडेक्स));
        if (एन्ट्री_मान == null) {
            return -9;
        }
        int वॉलपेपर_मान;
        if (प्रोजेक्ट_करें_मूल == 0) {
            वॉलपेपर_मान = 0;
        } else if (प्रोजेक्ट_करें_मूल == 1) {
            वॉलपेपर_मान = एन्ट्री_मान.열린파일.स्थान;
        } else if (प्रोजेक्ट_करें_मूल == 2) {
            वॉलपेपर_मान = एन्ट्री_मान.열린파일.आँकड़े.length;
        } else {
            return -22;
        }
        int 새위치 = वॉलपेपर_मान + 거리;
        if (새위치 < 0) {
            return -22;
        }
        एन्ट्री_मान.열린파일.स्थान = 새위치;
        return 새위치;
    }

    public int बंदकरें(int इंडेक्स) {
        서술자 एन्ट्री_मान = 서술자들.remove(Integer.valueOf(इंडेक्स));
        if (एन्ट्री_मान == null) {
            return -9;
        }
        एन्ट्री_मान.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int इंडेक्स, int 최소번호) {
        서술자 एन्ट्री_मान = 서술자들.get(Integer.valueOf(इंडेक्स));
        if (एन्ट्री_मान == null) {
            return -9;
        }
        int नया_नंबर = 빈번호(최소번호);
        if (नया_नंबर < 0) {
            return -24;
        }
        एन्ट्री_मान.열린파일.참조수++;
        서술자들.put(Integer.valueOf(नया_नंबर), new 서술자(एन्ट्री_मान.열린파일));
        return नया_नंबर;
    }

    public int 지정복제(int इंडेक्स, int नया_नंबर) {
        if (इंडेक्स == नया_नंबर) {
            return 서술자들.containsKey(Integer.valueOf(इंडेक्स)) ? इंडेक्स : -9;
        }
        if (नया_नंबर < 0 || नया_नंबर >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(इंडेक्स));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(नया_नंबर))) {
            बंदकरें(नया_नंबर);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(नया_नंबर), new 서술자(원본.열린파일));
        return नया_नंबर;
    }

    public int 실행시닫기설정(int इंडेक्स, boolean मान) {
        서술자 एन्ट्री_मान = 서술자들.get(Integer.valueOf(इंडेक्स));
        if (एन्ट्री_मान == null) {
            return -9;
        }
        एन्ट्री_मान.실행시닫기 = मान;
        return 0;
    }

    public int 실행시닫기값(int इंडेक्स) {
        서술자 एन्ट्री_मान = 서술자들.get(Integer.valueOf(इंडेक्स));
        if (एन्ट्री_मान == null) {
            return -9;
        }
        return एन्ट्री_मान.실행시닫기 ? 1 : 0;
    }

    public फ़ाइल_जानकारी सिस्टम_जानकारी(int इंडेक्स) {
        if (इंडेक्स >= 0 && इंडेक्स <= 2) {
            return new फ़ाइल_जानकारी(0, 0020666);
        }
        서술자 एन्ट्री_मान = 서술자들.get(Integer.valueOf(इंडेक्स));
        if (एन्ट्री_मान == null) {
            return null;
        }
        return new फ़ाइल_जानकारी(एन्ट्री_मान.열린파일.आँकड़े.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer इंडेक्स : 번호들) {
            서술자 एन्ट्री_मान = 서술자들.get(इंडेक्स);
            if (एन्ट्री_मान != null && एन्ट्री_मान.실행시닫기) {
                बंदकरें(इंडेक्स.intValue());
            }
        }
    }

    public boolean सूचना_प्रौद्योगिकी_जारी(int इंडेक्स) {
        return 서술자들.containsKey(Integer.valueOf(इंडेक्स));
    }

    public 파일서술자표 क्लोन_मान() {
        파일서술자표 परिणाम = new 파일서술자표(फ़ाइल_सिस्टम);
        for (Map.Entry<Integer, 서술자> एन्ट्री_मान : 서술자들.entrySet()) {
            एन्ट्री_मान.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(एन्ट्री_मान.getValue().열린파일);
            새서술자.실행시닫기 = एन्ट्री_मान.getValue().실행시닫기;
            परिणाम.서술자들.put(एन्ट्री_मान.getKey(), 새서술자);
        }
        return परिणाम;
    }

    private int 빈번호(int 최소번호) {
        for (int इंडेक्स = Math.max(0, 최소번호); इंडेक्स < 최대서술자; इंडेक्स++) {
            if (!서술자들.containsKey(Integer.valueOf(इंडेक्स))) {
                return इंडेक्स;
            }
        }
        return -1;
    }
}
