// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.fajl_sistem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fajl 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final fajl_sistem.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(fajl_sistem.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final fajl_sistem fajl_sistem;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(fajl_sistem fajl_sistem) {
        this.fajl_sistem = fajl_sistem;
    }

    public int Otvori(String Naziv) {
        fajl_sistem.열린파일 열린파일 = fajl_sistem.Otvori(Naziv);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = prazno_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Čitaj(int INDEX, byte[] 받을곳, int Veličina) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        if (Veličina < 0 || Veličina > 받을곳.length) {
            return -22;
        }
        int 남음 = unos_VALUE.열린파일.podaci.length - unos_VALUE.열린파일.Pozicija;
        int 읽을크기 = Math.min(Veličina, Math.max(남음, 0));
        System.arraycopy(unos_VALUE.열린파일.podaci, unos_VALUE.열린파일.Pozicija, 받을곳, 0, 읽을크기);
        unos_VALUE.열린파일.Pozicija += 읽을크기;
        return 읽을크기;
    }

    public int pomaći_položaj(int INDEX, int 거리, int projicirati_koijen) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        int poster_VALUE;
        if (projicirati_koijen == 0) {
            poster_VALUE = 0;
        } else if (projicirati_koijen == 1) {
            poster_VALUE = unos_VALUE.열린파일.Pozicija;
        } else if (projicirati_koijen == 2) {
            poster_VALUE = unos_VALUE.열린파일.podaci.length;
        } else {
            return -22;
        }
        int 새위치 = poster_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        unos_VALUE.열린파일.Pozicija = 새위치;
        return 새위치;
    }

    public int Zatvori(int INDEX) {
        서술자 unos_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        unos_VALUE.열린파일.Reference_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        int 새번호 = prazno_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        unos_VALUE.열린파일.Reference_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(unos_VALUE.열린파일));
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
            Zatvori(새번호);
        }
        원본.열린파일.Reference_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        unos_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        return unos_VALUE.실행시닫기 ? 1 : 0;
    }

    public fajl_informacija msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new fajl_informacija(0, 0020666);
        }
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return null;
        }
        return new fajl_informacija(unos_VALUE.열린파일.podaci.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 unos_VALUE = 서술자들.get(INDEX);
            if (unos_VALUE != null && unos_VALUE.실행시닫기) {
                Zatvori(INDEX.intValue());
            }
        }
    }

    public boolean odjel_za_informacijske_tehnologije_kreirati(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 mjera = new 파일서술자표(fajl_sistem);
        for (Map.Entry<Integer, 서술자> unos_VALUE : 서술자들.entrySet()) {
            unos_VALUE.getValue().열린파일.Reference_COUNT++;
            서술자 새서술자 = new 서술자(unos_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = unos_VALUE.getValue().실행시닫기;
            mjera.서술자들.put(unos_VALUE.getKey(), 새서술자);
        }
        return mjera;
    }

    private int prazno_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
