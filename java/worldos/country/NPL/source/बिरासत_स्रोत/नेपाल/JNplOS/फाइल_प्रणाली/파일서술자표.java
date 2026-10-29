// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.फाइल_प्रणाली;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 फाइल 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final फाइल_प्रणाली.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(फाइल_प्रणाली.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final फाइल_प्रणाली फाइल_प्रणाली;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(फाइल_प्रणाली फाइल_प्रणाली) {
        this.फाइल_प्रणाली = फाइल_प्रणाली;
    }

    public int खोल्नुहोस्(String नाम) {
        फाइल_प्रणाली.열린파일 열린파일 = फाइल_प्रणाली.खोल्नुहोस्(नाम);
        if (열린파일 == null) {
            return -2;
        }
        int अनुक्रमणिका = रिक्त_अनुक्रमणिका(3);
        if (अनुक्रमणिका < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(अनुक्रमणिका), new 서술자(열린파일));
        return अनुक्रमणिका;
    }

    public int पढनुहोस्(int अनुक्रमणिका, byte[] 받을곳, int आकार) {
        서술자 प्रविष्टि_मान = 서술자들.get(Integer.valueOf(अनुक्रमणिका));
        if (प्रविष्टि_मान == null) {
            return -9;
        }
        if (आकार < 0 || आकार > 받을곳.length) {
            return -22;
        }
        int 남음 = प्रविष्टि_मान.열린파일.लगत.length - प्रविष्टि_मान.열린파일.स्थिति;
        int 읽을크기 = Math.min(आकार, Math.max(남음, 0));
        System.arraycopy(प्रविष्टि_मान.열린파일.लगत, प्रविष्टि_मान.열린파일.स्थिति, 받을곳, 0, 읽을크기);
        प्रविष्टि_मान.열린파일.स्थिति += 읽을크기;
        return 읽을크기;
    }

    public int लैजानुहोस्_राख्नुहोस्(int अनुक्रमणिका, int 거리, int परियोजना_रूट) {
        서술자 प्रविष्टि_मान = 서술자들.get(Integer.valueOf(अनुक्रमणिका));
        if (प्रविष्टि_मान == null) {
            return -9;
        }
        int वालपेपर_मान;
        if (परियोजना_रूट == 0) {
            वालपेपर_मान = 0;
        } else if (परियोजना_रूट == 1) {
            वालपेपर_मान = प्रविष्टि_मान.열린파일.स्थिति;
        } else if (परियोजना_रूट == 2) {
            वालपेपर_मान = प्रविष्टि_मान.열린파일.लगत.length;
        } else {
            return -22;
        }
        int 새위치 = वालपेपर_मान + 거리;
        if (새위치 < 0) {
            return -22;
        }
        प्रविष्टि_मान.열린파일.स्थिति = 새위치;
        return 새위치;
    }

    public int बन्दगर्नुहोस्(int अनुक्रमणिका) {
        서술자 प्रविष्टि_मान = 서술자들.remove(Integer.valueOf(अनुक्रमणिका));
        if (प्रविष्टि_मान == null) {
            return -9;
        }
        प्रविष्टि_मान.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int अनुक्रमणिका, int 최소번호) {
        서술자 प्रविष्टि_मान = 서술자들.get(Integer.valueOf(अनुक्रमणिका));
        if (प्रविष्टि_मान == null) {
            return -9;
        }
        int 새번호 = रिक्त_अनुक्रमणिका(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        प्रविष्टि_मान.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(प्रविष्टि_मान.열린파일));
        return 새번호;
    }

    public int 지정복제(int अनुक्रमणिका, int 새번호) {
        if (अनुक्रमणिका == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(अनुक्रमणिका)) ? अनुक्रमणिका : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(अनुक्रमणिका));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            बन्दगर्नुहोस्(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int अनुक्रमणिका, boolean मान) {
        서술자 प्रविष्टि_मान = 서술자들.get(Integer.valueOf(अनुक्रमणिका));
        if (प्रविष्टि_मान == null) {
            return -9;
        }
        प्रविष्टि_मान.실행시닫기 = मान;
        return 0;
    }

    public int 실행시닫기값(int अनुक्रमणिका) {
        서술자 प्रविष्टि_मान = 서술자들.get(Integer.valueOf(अनुक्रमणिका));
        if (प्रविष्टि_मान == null) {
            return -9;
        }
        return प्रविष्टि_मान.실행시닫기 ? 1 : 0;
    }

    public फाइल_जानकारी प्रणाली_जानकारी(int अनुक्रमणिका) {
        if (अनुक्रमणिका >= 0 && अनुक्रमणिका <= 2) {
            return new फाइल_जानकारी(0, 0020666);
        }
        서술자 प्रविष्टि_मान = 서술자들.get(Integer.valueOf(अनुक्रमणिका));
        if (प्रविष्टि_मान == null) {
            return null;
        }
        return new फाइल_जानकारी(प्रविष्टि_मान.열린파일.लगत.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer अनुक्रमणिका : 번호들) {
            서술자 प्रविष्टि_मान = 서술자들.get(अनुक्रमणिका);
            if (प्रविष्टि_मान != null && प्रविष्टि_मान.실행시닫기) {
                बन्दगर्नुहोस्(अनुक्रमणिका.intValue());
            }
        }
    }

    public boolean 열려있음(int अनुक्रमणिका) {
        return 서술자들.containsKey(Integer.valueOf(अनुक्रमणिका));
    }

    public 파일서술자표 복제() {
        파일서술자표 मापन = new 파일서술자표(फाइल_प्रणाली);
        for (Map.Entry<Integer, 서술자> प्रविष्टि_मान : 서술자들.entrySet()) {
            प्रविष्टि_मान.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(प्रविष्टि_मान.getValue().열린파일);
            새서술자.실행시닫기 = प्रविष्टि_मान.getValue().실행시닫기;
            मापन.서술자들.put(प्रविष्टि_मान.getKey(), 새서술자);
        }
        return मापन;
    }

    private int रिक्त_अनुक्रमणिका(int 최소번호) {
        for (int अनुक्रमणिका = Math.max(0, 최소번호); अनुक्रमणिका < 최대서술자; अनुक्रमणिका++) {
            if (!서술자들.containsKey(Integer.valueOf(अनुक्रमणिका))) {
                return अनुक्रमणिका;
            }
        }
        return -1;
    }
}
