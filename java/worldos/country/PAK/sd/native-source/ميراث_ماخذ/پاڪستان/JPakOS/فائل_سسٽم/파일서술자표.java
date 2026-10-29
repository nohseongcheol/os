// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.فائل_سسٽم;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 فائل 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final فائل_سسٽم.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(فائل_سسٽم.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final فائل_سسٽم فائل_سسٽم;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(فائل_سسٽم فائل_سسٽم) {
        this.فائل_سسٽم = فائل_سسٽم;
    }

    public int ٺاھيو(String نالو) {
        فائل_سسٽم.열린파일 열린파일 = فائل_سسٽم.ٺاھيو(نالو);
        if (열린파일 == null) {
            return -2;
        }
        int ابتدائي = خالي_ابتدائي(3);
        if (ابتدائي < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ابتدائي), new 서술자(열린파일));
        return ابتدائي;
    }

    public int 읽기(int ابتدائي, byte[] 받을곳, int سائيز) {
        서술자 داخلا_قدر = 서술자들.get(Integer.valueOf(ابتدائي));
        if (داخلا_قدر == null) {
            return -9;
        }
        if (سائيز < 0 || سائيز > 받을곳.length) {
            return -22;
        }
        int 남음 = داخلا_قدر.열린파일.ڪوائف.length - داخلا_قدر.열린파일.위치;
        int 읽을크기 = Math.min(سائيز, Math.max(남음, 0));
        System.arraycopy(داخلا_قدر.열린파일.ڪوائف, داخلا_قدر.열린파일.위치, 받을곳, 0, 읽을크기);
        داخلا_قدر.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int ابتدائي, int 거리, int 기준) {
        서술자 داخلا_قدر = 서술자들.get(Integer.valueOf(ابتدائي));
        if (داخلا_قدر == null) {
            return -9;
        }
        int پس_منظر_قدر;
        if (기준 == 0) {
            پس_منظر_قدر = 0;
        } else if (기준 == 1) {
            پس_منظر_قدر = داخلا_قدر.열린파일.위치;
        } else if (기준 == 2) {
            پس_منظر_قدر = داخلا_قدر.열린파일.ڪوائف.length;
        } else {
            return -22;
        }
        int 새위치 = پس_منظر_قدر + 거리;
        if (새위치 < 0) {
            return -22;
        }
        داخلا_قدر.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int بند_ڪرڻ(int ابتدائي) {
        서술자 داخلا_قدر = 서술자들.remove(Integer.valueOf(ابتدائي));
        if (داخلا_قدر == null) {
            return -9;
        }
        داخلا_قدر.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ابتدائي, int 최소번호) {
        서술자 داخلا_قدر = 서술자들.get(Integer.valueOf(ابتدائي));
        if (داخلا_قدر == null) {
            return -9;
        }
        int 새번호 = خالي_ابتدائي(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        داخلا_قدر.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(داخلا_قدر.열린파일));
        return 새번호;
    }

    public int 지정복제(int ابتدائي, int 새번호) {
        if (ابتدائي == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ابتدائي)) ? ابتدائي : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ابتدائي));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            بند_ڪرڻ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ابتدائي, boolean قدر) {
        서술자 داخلا_قدر = 서술자들.get(Integer.valueOf(ابتدائي));
        if (داخلا_قدر == null) {
            return -9;
        }
        داخلا_قدر.실행시닫기 = قدر;
        return 0;
    }

    public int 실행시닫기값(int ابتدائي) {
        서술자 داخلا_قدر = 서술자들.get(Integer.valueOf(ابتدائي));
        if (داخلا_قدر == null) {
            return -9;
        }
        return داخلا_قدر.실행시닫기 ? 1 : 0;
    }

    public فائل_معلومات سسٽم_معلومات(int ابتدائي) {
        if (ابتدائي >= 0 && ابتدائي <= 2) {
            return new فائل_معلومات(0, 0020666);
        }
        서술자 داخلا_قدر = 서술자들.get(Integer.valueOf(ابتدائي));
        if (داخلا_قدر == null) {
            return null;
        }
        return new فائل_معلومات(داخلا_قدر.열린파일.ڪوائف.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ابتدائي : 번호들) {
            서술자 داخلا_قدر = 서술자들.get(ابتدائي);
            if (داخلا_قدر != null && داخلا_قدر.실행시닫기) {
                بند_ڪرڻ(ابتدائي.intValue());
            }
        }
    }

    public boolean 열려있음(int ابتدائي) {
        return 서술자들.containsKey(Integer.valueOf(ابتدائي));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(فائل_سسٽم);
        for (Map.Entry<Integer, 서술자> داخلا_قدر : 서술자들.entrySet()) {
            داخلا_قدر.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(داخلا_قدر.getValue().열린파일);
            새서술자.실행시닫기 = داخلا_قدر.getValue().실행시닫기;
            결과.서술자들.put(داخلا_قدر.getKey(), 새서술자);
        }
        return 결과;
    }

    private int خالي_ابتدائي(int 최소번호) {
        for (int ابتدائي = Math.max(0, 최소번호); ابتدائي < 최대서술자; ابتدائي++) {
            if (!서술자들.containsKey(Integer.valueOf(ابتدائي))) {
                return ابتدائي;
            }
        }
        return -1;
    }
}
