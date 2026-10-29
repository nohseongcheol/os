// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Maďarsko.JHunOS.systém_súborov;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Súbor 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final systém_súborov.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(systém_súborov.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final systém_súborov systém_súborov;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(systém_súborov systém_súborov) {
        this.systém_súborov = systém_súborov;
    }

    public int Otvoriť(String Názov) {
        systém_súborov.열린파일 열린파일 = systém_súborov.Otvoriť(Názov);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = prázdny_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Čítanie(int INDEX, byte[] dostať_cieľ, int Veľkosť) {
        서술자 položka_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_VALUE == null) {
            return -9;
        }
        if (Veľkosť < 0 || Veľkosť > dostať_cieľ.length) {
            return -22;
        }
        int 남음 = položka_VALUE.열린파일.údaje.length - položka_VALUE.열린파일.Pozícia;
        int 읽을크기 = Math.min(Veľkosť, Math.max(남음, 0));
        System.arraycopy(položka_VALUE.열린파일.údaje, položka_VALUE.열린파일.Pozícia, dostať_cieľ, 0, 읽을크기);
        položka_VALUE.열린파일.Pozícia += 읽을크기;
        return 읽을크기;
    }

    public int premiestniť_pozícia(int INDEX, int 거리, int akcia_koreň) {
        서술자 položka_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_VALUE == null) {
            return -9;
        }
        int tapeta_VALUE;
        if (akcia_koreň == 0) {
            tapeta_VALUE = 0;
        } else if (akcia_koreň == 1) {
            tapeta_VALUE = položka_VALUE.열린파일.Pozícia;
        } else if (akcia_koreň == 2) {
            tapeta_VALUE = položka_VALUE.열린파일.údaje.length;
        } else {
            return -22;
        }
        int 새위치 = tapeta_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        položka_VALUE.열린파일.Pozícia = 새위치;
        return 새위치;
    }

    public int Zatvoriť(int INDEX) {
        서술자 položka_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (položka_VALUE == null) {
            return -9;
        }
        položka_VALUE.열린파일.zdroj_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 položka_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_VALUE == null) {
            return -9;
        }
        int Nové_číslo = prázdny_INDEX(최소번호);
        if (Nové_číslo < 0) {
            return -24;
        }
        položka_VALUE.열린파일.zdroj_COUNT++;
        서술자들.put(Integer.valueOf(Nové_číslo), new 서술자(položka_VALUE.열린파일));
        return Nové_číslo;
    }

    public int 지정복제(int INDEX, int Nové_číslo) {
        if (INDEX == Nové_číslo) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Nové_číslo < 0 || Nové_číslo >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nové_číslo))) {
            Zatvoriť(Nové_číslo);
        }
        원본.열린파일.zdroj_COUNT++;
        서술자들.put(Integer.valueOf(Nové_číslo), new 서술자(원본.열린파일));
        return Nové_číslo;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 položka_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_VALUE == null) {
            return -9;
        }
        položka_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 položka_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_VALUE == null) {
            return -9;
        }
        return položka_VALUE.실행시닫기 ? 1 : 0;
    }

    public Súbor_informácia Systémové_informácie(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Súbor_informácia(0, 0020666);
        }
        서술자 položka_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_VALUE == null) {
            return null;
        }
        return new Súbor_informácia(položka_VALUE.열린파일.údaje.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 položka_VALUE = 서술자들.get(INDEX);
            if (položka_VALUE != null && položka_VALUE.실행시닫기) {
                Zatvoriť(INDEX.intValue());
            }
        }
    }

    public boolean Informačné_systémy_otvoriť(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klon_VALUE() {
        파일서술자표 KR = new 파일서술자표(systém_súborov);
        for (Map.Entry<Integer, 서술자> položka_VALUE : 서술자들.entrySet()) {
            položka_VALUE.getValue().열린파일.zdroj_COUNT++;
            서술자 새서술자 = new 서술자(položka_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = položka_VALUE.getValue().실행시닫기;
            KR.서술자들.put(položka_VALUE.getKey(), 새서술자);
        }
        return KR;
    }

    private int prázdny_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
