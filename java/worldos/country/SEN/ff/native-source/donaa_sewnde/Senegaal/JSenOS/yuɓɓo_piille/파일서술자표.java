// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.yuɓɓo_piille;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 fiilde 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final yuɓɓo_piille.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(yuɓɓo_piille.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final yuɓɓo_piille yuɓɓo_piille;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(yuɓɓo_piille yuɓɓo_piille) {
        this.yuɓɓo_piille = yuɓɓo_piille;
    }

    public int udditde(String innde) {
        yuɓɓo_piille.열린파일 열린파일 = yuɓɓo_piille.udditde(innde);
        if (열린파일 == null) {
            return -2;
        }
        int joopirdu = 빈번호(3);
        if (joopirdu < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(joopirdu), new 서술자(열린파일));
        return joopirdu;
    }

    public int 읽기(int joopirdu, byte[] 받을곳, int waylude_etannde) {
        서술자 naatnugol_njaru = 서술자들.get(Integer.valueOf(joopirdu));
        if (naatnugol_njaru == null) {
            return -9;
        }
        if (waylude_etannde < 0 || waylude_etannde > 받을곳.length) {
            return -22;
        }
        int 남음 = naatnugol_njaru.열린파일.keɓe.length - naatnugol_njaru.열린파일.위치;
        int 읽을크기 = Math.min(waylude_etannde, Math.max(남음, 0));
        System.arraycopy(naatnugol_njaru.열린파일.keɓe, naatnugol_njaru.열린파일.위치, 받을곳, 0, 읽을크기);
        naatnugol_njaru.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int joopirdu, int 거리, int 기준) {
        서술자 naatnugol_njaru = 서술자들.get(Integer.valueOf(joopirdu));
        if (naatnugol_njaru == null) {
            return -9;
        }
        int cakkital_njaru;
        if (기준 == 0) {
            cakkital_njaru = 0;
        } else if (기준 == 1) {
            cakkital_njaru = naatnugol_njaru.열린파일.위치;
        } else if (기준 == 2) {
            cakkital_njaru = naatnugol_njaru.열린파일.keɓe.length;
        } else {
            return -22;
        }
        int 새위치 = cakkital_njaru + 거리;
        if (새위치 < 0) {
            return -22;
        }
        naatnugol_njaru.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int uddude(int joopirdu) {
        서술자 naatnugol_njaru = 서술자들.remove(Integer.valueOf(joopirdu));
        if (naatnugol_njaru == null) {
            return -9;
        }
        naatnugol_njaru.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int joopirdu, int 최소번호) {
        서술자 naatnugol_njaru = 서술자들.get(Integer.valueOf(joopirdu));
        if (naatnugol_njaru == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        naatnugol_njaru.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(naatnugol_njaru.열린파일));
        return 새번호;
    }

    public int 지정복제(int joopirdu, int 새번호) {
        if (joopirdu == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(joopirdu)) ? joopirdu : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(joopirdu));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            uddude(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int joopirdu, boolean njaru) {
        서술자 naatnugol_njaru = 서술자들.get(Integer.valueOf(joopirdu));
        if (naatnugol_njaru == null) {
            return -9;
        }
        naatnugol_njaru.실행시닫기 = njaru;
        return 0;
    }

    public int 실행시닫기값(int joopirdu) {
        서술자 naatnugol_njaru = 서술자들.get(Integer.valueOf(joopirdu));
        if (naatnugol_njaru == null) {
            return -9;
        }
        return naatnugol_njaru.실행시닫기 ? 1 : 0;
    }

    public fiilde_kumpital msinfo32_exe(int joopirdu) {
        if (joopirdu >= 0 && joopirdu <= 2) {
            return new fiilde_kumpital(0, 0020666);
        }
        서술자 naatnugol_njaru = 서술자들.get(Integer.valueOf(joopirdu));
        if (naatnugol_njaru == null) {
            return null;
        }
        return new fiilde_kumpital(naatnugol_njaru.열린파일.keɓe.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer joopirdu : 번호들) {
            서술자 naatnugol_njaru = 서술자들.get(joopirdu);
            if (naatnugol_njaru != null && naatnugol_njaru.실행시닫기) {
                uddude(joopirdu.intValue());
            }
        }
    }

    public boolean 열려있음(int joopirdu) {
        return 서술자들.containsKey(Integer.valueOf(joopirdu));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(yuɓɓo_piille);
        for (Map.Entry<Integer, 서술자> naatnugol_njaru : 서술자들.entrySet()) {
            naatnugol_njaru.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(naatnugol_njaru.getValue().열린파일);
            새서술자.실행시닫기 = naatnugol_njaru.getValue().실행시닫기;
            결과.서술자들.put(naatnugol_njaru.getKey(), 새서술자);
        }
        return 결과;
    }

    private int 빈번호(int 최소번호) {
        for (int joopirdu = Math.max(0, 최소번호); joopirdu < 최대서술자; joopirdu++) {
            if (!서술자들.containsKey(Integer.valueOf(joopirdu))) {
                return joopirdu;
            }
        }
        return -1;
    }
}
