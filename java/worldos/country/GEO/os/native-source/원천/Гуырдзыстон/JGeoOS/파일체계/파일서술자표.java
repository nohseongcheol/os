// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Гуырдзыстон.JGeoOS.파일체계;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 파일 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final 파일체계.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(파일체계.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final 파일체계 파일체계;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(파일체계 파일체계) {
        this.파일체계 = 파일체계;
    }

    public int 열기(String 이름) {
        파일체계.열린파일 열린파일 = 파일체계.열기(이름);
        if (열린파일 == null) {
            return -2;
        }
        int 번호 = 빈번호(3);
        if (번호 < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(번호), new 서술자(열린파일));
        return 번호;
    }

    public int 읽기(int 번호, byte[] 받을곳, int 크기) {
        서술자 항목 = 서술자들.get(Integer.valueOf(번호));
        if (항목 == null) {
            return -9;
        }
        if (크기 < 0 || 크기 > 받을곳.length) {
            return -22;
        }
        int 남음 = 항목.열린파일.자료.length - 항목.열린파일.위치;
        int 읽을크기 = Math.min(크기, Math.max(남음, 0));
        System.arraycopy(항목.열린파일.자료, 항목.열린파일.위치, 받을곳, 0, 읽을크기);
        항목.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int 번호, int 거리, int 기준) {
        서술자 항목 = 서술자들.get(Integer.valueOf(번호));
        if (항목 == null) {
            return -9;
        }
        int 바탕;
        if (기준 == 0) {
            바탕 = 0;
        } else if (기준 == 1) {
            바탕 = 항목.열린파일.위치;
        } else if (기준 == 2) {
            바탕 = 항목.열린파일.자료.length;
        } else {
            return -22;
        }
        int 새위치 = 바탕 + 거리;
        if (새위치 < 0) {
            return -22;
        }
        항목.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int 닫기(int 번호) {
        서술자 항목 = 서술자들.remove(Integer.valueOf(번호));
        if (항목 == null) {
            return -9;
        }
        항목.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int 번호, int 최소번호) {
        서술자 항목 = 서술자들.get(Integer.valueOf(번호));
        if (항목 == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        항목.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(항목.열린파일));
        return 새번호;
    }

    public int 지정복제(int 번호, int 새번호) {
        if (번호 == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(번호)) ? 번호 : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(번호));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            닫기(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int 번호, boolean 값) {
        서술자 항목 = 서술자들.get(Integer.valueOf(번호));
        if (항목 == null) {
            return -9;
        }
        항목.실행시닫기 = 값;
        return 0;
    }

    public int 실행시닫기값(int 번호) {
        서술자 항목 = 서술자들.get(Integer.valueOf(번호));
        if (항목 == null) {
            return -9;
        }
        return 항목.실행시닫기 ? 1 : 0;
    }

    public 파일정보 정보(int 번호) {
        if (번호 >= 0 && 번호 <= 2) {
            return new 파일정보(0, 0020666);
        }
        서술자 항목 = 서술자들.get(Integer.valueOf(번호));
        if (항목 == null) {
            return null;
        }
        return new 파일정보(항목.열린파일.자료.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer 번호 : 번호들) {
            서술자 항목 = 서술자들.get(번호);
            if (항목 != null && 항목.실행시닫기) {
                닫기(번호.intValue());
            }
        }
    }

    public boolean 열려있음(int 번호) {
        return 서술자들.containsKey(Integer.valueOf(번호));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(파일체계);
        for (Map.Entry<Integer, 서술자> 항목 : 서술자들.entrySet()) {
            항목.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(항목.getValue().열린파일);
            새서술자.실행시닫기 = 항목.getValue().실행시닫기;
            결과.서술자들.put(항목.getKey(), 새서술자);
        }
        return 결과;
    }

    private int 빈번호(int 최소번호) {
        for (int 번호 = Math.max(0, 최소번호); 번호 < 최대서술자; 번호++) {
            if (!서술자들.containsKey(Integer.valueOf(번호))) {
                return 번호;
            }
        }
        return -1;
    }
}
