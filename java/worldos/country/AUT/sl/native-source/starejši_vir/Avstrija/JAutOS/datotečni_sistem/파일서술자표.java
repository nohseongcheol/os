// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Avstrija.JAutOS.datotečni_sistem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Datoteka 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final datotečni_sistem.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(datotečni_sistem.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final datotečni_sistem datotečni_sistem;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(datotečni_sistem datotečni_sistem) {
        this.datotečni_sistem = datotečni_sistem;
    }

    public int Odpri(String Ime) {
        datotečni_sistem.열린파일 열린파일 = datotečni_sistem.Odpri(Ime);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = prazen_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Branje(int INDEX, byte[] sprejeti_sprejemati_prejeti_prejemati_cilj, int Velikost) {
        서술자 vnos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (vnos_VALUE == null) {
            return -9;
        }
        if (Velikost < 0 || Velikost > sprejeti_sprejemati_prejeti_prejemati_cilj.length) {
            return -22;
        }
        int 남음 = vnos_VALUE.열린파일.podatki.length - vnos_VALUE.열린파일.Položaj;
        int 읽을크기 = Math.min(Velikost, Math.max(남음, 0));
        System.arraycopy(vnos_VALUE.열린파일.podatki, vnos_VALUE.열린파일.Položaj, sprejeti_sprejemati_prejeti_prejemati_cilj, 0, 읽을크기);
        vnos_VALUE.열린파일.Položaj += 읽을크기;
        return 읽을크기;
    }

    public int premikati_položaj(int INDEX, int 거리, int pobuda_koren) {
        서술자 vnos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (vnos_VALUE == null) {
            return -9;
        }
        int Ozadje_VALUE;
        if (pobuda_koren == 0) {
            Ozadje_VALUE = 0;
        } else if (pobuda_koren == 1) {
            Ozadje_VALUE = vnos_VALUE.열린파일.Položaj;
        } else if (pobuda_koren == 2) {
            Ozadje_VALUE = vnos_VALUE.열린파일.podatki.length;
        } else {
            return -22;
        }
        int 새위치 = Ozadje_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        vnos_VALUE.열린파일.Položaj = 새위치;
        return 새위치;
    }

    public int Zapri(int INDEX) {
        서술자 vnos_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (vnos_VALUE == null) {
            return -9;
        }
        vnos_VALUE.열린파일.Gradiva_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 vnos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (vnos_VALUE == null) {
            return -9;
        }
        int Nova_številka = prazen_INDEX(최소번호);
        if (Nova_številka < 0) {
            return -24;
        }
        vnos_VALUE.열린파일.Gradiva_COUNT++;
        서술자들.put(Integer.valueOf(Nova_številka), new 서술자(vnos_VALUE.열린파일));
        return Nova_številka;
    }

    public int 지정복제(int INDEX, int Nova_številka) {
        if (INDEX == Nova_številka) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Nova_številka < 0 || Nova_številka >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nova_številka))) {
            Zapri(Nova_številka);
        }
        원본.열린파일.Gradiva_COUNT++;
        서술자들.put(Integer.valueOf(Nova_številka), new 서술자(원본.열린파일));
        return Nova_številka;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 vnos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (vnos_VALUE == null) {
            return -9;
        }
        vnos_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 vnos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (vnos_VALUE == null) {
            return -9;
        }
        return vnos_VALUE.실행시닫기 ? 1 : 0;
    }

    public Datoteka_informacije msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Datoteka_informacije(0, 0020666);
        }
        서술자 vnos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (vnos_VALUE == null) {
            return null;
        }
        return new Datoteka_informacije(vnos_VALUE.열린파일.podatki.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 vnos_VALUE = 서술자들.get(INDEX);
            if (vnos_VALUE != null && vnos_VALUE.실행시닫기) {
                Zapri(INDEX.intValue());
            }
        }
    }

    public boolean informacijska_tehnologija_odprto(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klon_VALUE() {
        파일서술자표 REZULTAT = new 파일서술자표(datotečni_sistem);
        for (Map.Entry<Integer, 서술자> vnos_VALUE : 서술자들.entrySet()) {
            vnos_VALUE.getValue().열린파일.Gradiva_COUNT++;
            서술자 새서술자 = new 서술자(vnos_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = vnos_VALUE.getValue().실행시닫기;
            REZULTAT.서술자들.put(vnos_VALUE.getKey(), 새서술자);
        }
        return REZULTAT;
    }

    private int prazen_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
