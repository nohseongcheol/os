// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.córas_comhad;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Comhad 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final córas_comhad.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(córas_comhad.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final córas_comhad córas_comhad;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(córas_comhad córas_comhad) {
        this.córas_comhad = córas_comhad;
    }

    public int Oscail(String Ainm) {
        córas_comhad.열린파일 열린파일 = córas_comhad.Oscail(Ainm);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = folamh_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Léigh(int INDEX, byte[] 받을곳, int Méid) {
        서술자 iontráil_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (iontráil_VALUE == null) {
            return -9;
        }
        if (Méid < 0 || Méid > 받을곳.length) {
            return -22;
        }
        int 남음 = iontráil_VALUE.열린파일.sonraí.length - iontráil_VALUE.열린파일.suíomh;
        int 읽을크기 = Math.min(Méid, Math.max(남음, 0));
        System.arraycopy(iontráil_VALUE.열린파일.sonraí, iontráil_VALUE.열린파일.suíomh, 받을곳, 0, 읽을크기);
        iontráil_VALUE.열린파일.suíomh += 읽을크기;
        return 읽을크기;
    }

    public int bog_suíomh(int INDEX, int 거리, int teilgean_fréamh) {
        서술자 iontráil_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (iontráil_VALUE == null) {
            return -9;
        }
        int Cúlra_VALUE;
        if (teilgean_fréamh == 0) {
            Cúlra_VALUE = 0;
        } else if (teilgean_fréamh == 1) {
            Cúlra_VALUE = iontráil_VALUE.열린파일.suíomh;
        } else if (teilgean_fréamh == 2) {
            Cúlra_VALUE = iontráil_VALUE.열린파일.sonraí.length;
        } else {
            return -22;
        }
        int 새위치 = Cúlra_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        iontráil_VALUE.열린파일.suíomh = 새위치;
        return 새위치;
    }

    public int Dún(int INDEX) {
        서술자 iontráil_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (iontráil_VALUE == null) {
            return -9;
        }
        iontráil_VALUE.열린파일.Leabhair_thagartha_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 iontráil_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (iontráil_VALUE == null) {
            return -9;
        }
        int 새번호 = folamh_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        iontráil_VALUE.열린파일.Leabhair_thagartha_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(iontráil_VALUE.열린파일));
        return 새번호;
    }

    public int 지정복제(int INDEX, int 새번호) {
        if (INDEX == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Dún(새번호);
        }
        원본.열린파일.Leabhair_thagartha_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 iontráil_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (iontráil_VALUE == null) {
            return -9;
        }
        iontráil_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 iontráil_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (iontráil_VALUE == null) {
            return -9;
        }
        return iontráil_VALUE.실행시닫기 ? 1 : 0;
    }

    public comhad_faisnéis msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new comhad_faisnéis(0, 0020666);
        }
        서술자 iontráil_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (iontráil_VALUE == null) {
            return null;
        }
        return new comhad_faisnéis(iontráil_VALUE.열린파일.sonraí.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 iontráil_VALUE = 서술자들.get(INDEX);
            if (iontráil_VALUE != null && iontráil_VALUE.실행시닫기) {
                Dún(INDEX.intValue());
            }
        }
    }

    public boolean teicneolaíocht_faisnéise_oscail(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 tomhas = new 파일서술자표(córas_comhad);
        for (Map.Entry<Integer, 서술자> iontráil_VALUE : 서술자들.entrySet()) {
            iontráil_VALUE.getValue().열린파일.Leabhair_thagartha_COUNT++;
            서술자 새서술자 = new 서술자(iontráil_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = iontráil_VALUE.getValue().실행시닫기;
            tomhas.서술자들.put(iontráil_VALUE.getKey(), 새서술자);
        }
        return tomhas;
    }

    private int folamh_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
