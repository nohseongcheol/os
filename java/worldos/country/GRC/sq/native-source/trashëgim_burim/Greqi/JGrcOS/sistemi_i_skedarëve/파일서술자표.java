// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Greqi.JGrcOS.sistemi_i_skedarëve;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Kartelë 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistemi_i_skedarëve.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistemi_i_skedarëve.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistemi_i_skedarëve sistemi_i_skedarëve;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistemi_i_skedarëve sistemi_i_skedarëve) {
        this.sistemi_i_skedarëve = sistemi_i_skedarëve;
    }

    public int Hap(String Emër) {
        sistemi_i_skedarëve.열린파일 열린파일 = sistemi_i_skedarëve.Hap(Emër);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = bosh_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Leximi(int INDEX, byte[] 받을곳, int Madhësi) {
        서술자 futje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (futje_VALUE == null) {
            return -9;
        }
        if (Madhësi < 0 || Madhësi > 받을곳.length) {
            return -22;
        }
        int 남음 = futje_VALUE.열린파일.të_dhëna.length - futje_VALUE.열린파일.Pozicioni;
        int 읽을크기 = Math.min(Madhësi, Math.max(남음, 0));
        System.arraycopy(futje_VALUE.열린파일.të_dhëna, futje_VALUE.열린파일.Pozicioni, 받을곳, 0, 읽을크기);
        futje_VALUE.열린파일.Pozicioni += 읽을크기;
        return 읽을크기;
    }

    public int lëviz_pozicioni(int INDEX, int 거리, int Project_rrënjë) {
        서술자 futje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (futje_VALUE == null) {
            return -9;
        }
        int Sfond_VALUE;
        if (Project_rrënjë == 0) {
            Sfond_VALUE = 0;
        } else if (Project_rrënjë == 1) {
            Sfond_VALUE = futje_VALUE.열린파일.Pozicioni;
        } else if (Project_rrënjë == 2) {
            Sfond_VALUE = futje_VALUE.열린파일.të_dhëna.length;
        } else {
            return -22;
        }
        int 새위치 = Sfond_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        futje_VALUE.열린파일.Pozicioni = 새위치;
        return 새위치;
    }

    public int Mbyll(int INDEX) {
        서술자 futje_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (futje_VALUE == null) {
            return -9;
        }
        futje_VALUE.열린파일.Referencë_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 futje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (futje_VALUE == null) {
            return -9;
        }
        int 새번호 = bosh_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        futje_VALUE.열린파일.Referencë_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(futje_VALUE.열린파일));
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
            Mbyll(새번호);
        }
        원본.열린파일.Referencë_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 futje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (futje_VALUE == null) {
            return -9;
        }
        futje_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 futje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (futje_VALUE == null) {
            return -9;
        }
        return futje_VALUE.실행시닫기 ? 1 : 0;
    }

    public skedar_informacion msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new skedar_informacion(0, 0020666);
        }
        서술자 futje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (futje_VALUE == null) {
            return null;
        }
        return new skedar_informacion(futje_VALUE.열린파일.të_dhëna.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 futje_VALUE = 서술자들.get(INDEX);
            if (futje_VALUE != null && futje_VALUE.실행시닫기) {
                Mbyll(INDEX.intValue());
            }
        }
    }

    public boolean teknologjia_e_informacionit_hap(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 llogaritje = new 파일서술자표(sistemi_i_skedarëve);
        for (Map.Entry<Integer, 서술자> futje_VALUE : 서술자들.entrySet()) {
            futje_VALUE.getValue().열린파일.Referencë_COUNT++;
            서술자 새서술자 = new 서술자(futje_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = futje_VALUE.getValue().실행시닫기;
            llogaritje.서술자들.put(futje_VALUE.getKey(), 새서술자);
        }
        return llogaritje;
    }

    private int bosh_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
