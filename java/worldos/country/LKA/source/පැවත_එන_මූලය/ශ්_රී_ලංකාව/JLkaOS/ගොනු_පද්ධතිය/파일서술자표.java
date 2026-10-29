// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ගොනු_පද්ධතිය;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ගොනු 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ගොනු_පද්ධතිය.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ගොනු_පද්ධතිය.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ගොනු_පද්ධතිය ගොනු_පද්ධතිය;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ගොනු_පද්ධතිය ගොනු_පද්ධතිය) {
        this.ගොනු_පද්ධතිය = ගොනු_පද්ධතිය;
    }

    public int විවෘත_කරන්න(String නම) {
        ගොනු_පද්ධතිය.열린파일 열린파일 = ගොනු_පද්ධතිය.විවෘත_කරන්න(නම);
        if (열린파일 == null) {
            return -2;
        }
        int සූචිය = ශූන්_ය_සූචිය(3);
        if (සූචිය < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(සූචිය), new 서술자(열린파일));
        return සූචිය;
    }

    public int කියවීම(int සූචිය, byte[] 받을곳, int ප්_රමාණය) {
        서술자 පිවිසුම_අගය = 서술자들.get(Integer.valueOf(සූචිය));
        if (පිවිසුම_අගය == null) {
            return -9;
        }
        if (ප්_රමාණය < 0 || ප්_රමාණය > 받을곳.length) {
            return -22;
        }
        int 남음 = පිවිසුම_අගය.열린파일.දත්ත.length - පිවිසුම_අගය.열린파일.පිහිටීම;
        int 읽을크기 = Math.min(ප්_රමාණය, Math.max(남음, 0));
        System.arraycopy(පිවිසුම_අගය.열린파일.දත්ත, පිවිසුම_අගය.열린파일.පිහිටීම, 받을곳, 0, 읽을크기);
        පිවිසුම_අගය.열린파일.පිහිටීම += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int සූචිය, int 거리, int 기준) {
        서술자 පිවිසුම_අගය = 서술자들.get(Integer.valueOf(සූචිය));
        if (පිවිසුම_අගය == null) {
            return -9;
        }
        int පසුබිම_අගය;
        if (기준 == 0) {
            පසුබිම_අගය = 0;
        } else if (기준 == 1) {
            පසුබිම_අගය = පිවිසුම_අගය.열린파일.පිහිටීම;
        } else if (기준 == 2) {
            පසුබිම_අගය = පිවිසුම_අගය.열린파일.දත්ත.length;
        } else {
            return -22;
        }
        int 새위치 = පසුබිම_අගය + 거리;
        if (새위치 < 0) {
            return -22;
        }
        පිවිසුම_අගය.열린파일.පිහිටීම = 새위치;
        return 새위치;
    }

    public int වසන්න(int සූචිය) {
        서술자 පිවිසුම_අගය = 서술자들.remove(Integer.valueOf(සූචිය));
        if (පිවිසුම_අගය == null) {
            return -9;
        }
        පිවිසුම_අගය.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int සූචිය, int 최소번호) {
        서술자 පිවිසුම_අගය = 서술자들.get(Integer.valueOf(සූචිය));
        if (පිවිසුම_අගය == null) {
            return -9;
        }
        int 새번호 = ශූන්_ය_සූචිය(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        පිවිසුම_අගය.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(පිවිසුම_අගය.열린파일));
        return 새번호;
    }

    public int 지정복제(int සූචිය, int 새번호) {
        if (සූචිය == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(සූචිය)) ? සූචිය : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(සූචිය));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            වසන්න(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int සූචිය, boolean අගය) {
        서술자 පිවිසුම_අගය = 서술자들.get(Integer.valueOf(සූචිය));
        if (පිවිසුම_අගය == null) {
            return -9;
        }
        පිවිසුම_අගය.실행시닫기 = අගය;
        return 0;
    }

    public int 실행시닫기값(int සූචිය) {
        서술자 පිවිසුම_අගය = 서술자들.get(Integer.valueOf(සූචිය));
        if (පිවිසුම_අගය == null) {
            return -9;
        }
        return පිවිසුම_අගය.실행시닫기 ? 1 : 0;
    }

    public ගොනුව_තතු පද්ධති_තොරතුරු(int සූචිය) {
        if (සූචිය >= 0 && සූචිය <= 2) {
            return new ගොනුව_තතු(0, 0020666);
        }
        서술자 පිවිසුම_අගය = 서술자들.get(Integer.valueOf(සූචිය));
        if (පිවිසුම_අගය == null) {
            return null;
        }
        return new ගොනුව_තතු(පිවිසුම_අගය.열린파일.දත්ත.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer සූචිය : 번호들) {
            서술자 පිවිසුම_අගය = 서술자들.get(සූචිය);
            if (පිවිසුම_අගය != null && පිවිසුම_අගය.실행시닫기) {
                වසන්න(සූචිය.intValue());
            }
        }
    }

    public boolean 열려있음(int සූචිය) {
        return 서술자들.containsKey(Integer.valueOf(සූචිය));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(ගොනු_පද්ධතිය);
        for (Map.Entry<Integer, 서술자> පිවිසුම_අගය : 서술자들.entrySet()) {
            පිවිසුම_අගය.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(පිවිසුම_අගය.getValue().열린파일);
            새서술자.실행시닫기 = පිවිසුම_අගය.getValue().실행시닫기;
            결과.서술자들.put(පිවිසුම_අගය.getKey(), 새서술자);
        }
        return 결과;
    }

    private int ශූන්_ය_සූචිය(int 최소번호) {
        for (int සූචිය = Math.max(0, 최소번호); සූචිය < 최대서술자; සූචිය++) {
            if (!서술자들.containsKey(Integer.valueOf(සූචිය))) {
                return සූචිය;
            }
        }
        return -1;
    }
}
