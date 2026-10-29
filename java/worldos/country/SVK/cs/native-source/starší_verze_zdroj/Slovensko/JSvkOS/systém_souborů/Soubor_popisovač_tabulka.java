// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.systém_souborů;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 název_souboru 설명을 유지한다. */
public final class Soubor_popisovač_tabulka {
    private static final int 최대서술자 = 32;

    private static final class popisovač_položka {
        private final systém_souborů.열린파일 열린파일;
        private boolean 실행시닫기;

        popisovač_položka(systém_souborů.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final systém_souborů systém_souborů;
    private final Map<Integer, popisovač_položka> 서술자들 = new HashMap<Integer, popisovač_položka>();

    public Soubor_popisovač_tabulka(systém_souborů systém_souborů) {
        this.systém_souborů = systém_souborů;
    }

    public int Otevřít(String Název) {
        systém_souborů.열린파일 열린파일 = systém_souborů.Otevřít(Název);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = 빈번호(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new popisovač_položka(열린파일));
        return INDEX;
    }

    public int Čtení(int INDEX, byte[] dostat_cíl, int Velikost) {
        popisovač_položka položka_HODNOTA = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_HODNOTA == null) {
            return -9;
        }
        if (Velikost < 0 || Velikost > dostat_cíl.length) {
            return -22;
        }
        int 남음 = položka_HODNOTA.열린파일.data.length - položka_HODNOTA.열린파일.pozice;
        int 읽을크기 = Math.min(Velikost, Math.max(남음, 0));
        System.arraycopy(položka_HODNOTA.열린파일.data, položka_HODNOTA.열린파일.pozice, dostat_cíl, 0, 읽을크기);
        položka_HODNOTA.열린파일.pozice += 읽을크기;
        return 읽을크기;
    }

    public int přesunout_pozice(int INDEX, int 거리, int akce_kořen) {
        popisovač_položka položka_HODNOTA = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_HODNOTA == null) {
            return -9;
        }
        int Pozadí_HODNOTA;
        if (akce_kořen == 0) {
            Pozadí_HODNOTA = 0;
        } else if (akce_kořen == 1) {
            Pozadí_HODNOTA = položka_HODNOTA.열린파일.pozice;
        } else if (akce_kořen == 2) {
            Pozadí_HODNOTA = položka_HODNOTA.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = Pozadí_HODNOTA + 거리;
        if (새위치 < 0) {
            return -22;
        }
        položka_HODNOTA.열린파일.pozice = 새위치;
        return 새위치;
    }

    public int Zavřené(int INDEX) {
        popisovač_položka položka_HODNOTA = 서술자들.remove(Integer.valueOf(INDEX));
        if (položka_HODNOTA == null) {
            return -9;
        }
        položka_HODNOTA.열린파일.odkaz_POČET--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        popisovač_položka položka_HODNOTA = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_HODNOTA == null) {
            return -9;
        }
        int Nové_číslo = 빈번호(최소번호);
        if (Nové_číslo < 0) {
            return -24;
        }
        položka_HODNOTA.열린파일.odkaz_POČET++;
        서술자들.put(Integer.valueOf(Nové_číslo), new popisovač_položka(položka_HODNOTA.열린파일));
        return Nové_číslo;
    }

    public int 지정복제(int INDEX, int Nové_číslo) {
        if (INDEX == Nové_číslo) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Nové_číslo < 0 || Nové_číslo >= 최대서술자) {
            return -9;
        }
        popisovač_položka 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nové_číslo))) {
            Zavřené(Nové_číslo);
        }
        원본.열린파일.odkaz_POČET++;
        서술자들.put(Integer.valueOf(Nové_číslo), new popisovač_položka(원본.열린파일));
        return Nové_číslo;
    }

    public int 실행시닫기설정(int INDEX, boolean HODNOTA) {
        popisovač_položka položka_HODNOTA = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_HODNOTA == null) {
            return -9;
        }
        položka_HODNOTA.실행시닫기 = HODNOTA;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        popisovač_položka položka_HODNOTA = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_HODNOTA == null) {
            return -9;
        }
        return položka_HODNOTA.실행시닫기 ? 1 : 0;
    }

    public Soubor_informace Informace_o_systému(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Soubor_informace(0, 0020666);
        }
        popisovač_položka položka_HODNOTA = 서술자들.get(Integer.valueOf(INDEX));
        if (položka_HODNOTA == null) {
            return null;
        }
        return new Soubor_informace(položka_HODNOTA.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] číslo_Seznam = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : číslo_Seznam) {
            popisovač_položka položka_HODNOTA = 서술자들.get(INDEX);
            if (položka_HODNOTA != null && položka_HODNOTA.실행시닫기) {
                Zavřené(INDEX.intValue());
            }
        }
    }

    public boolean informační_systémy_otevřít(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public Soubor_popisovač_tabulka klon_HODNOTA() {
        Soubor_popisovač_tabulka VÝSLEDEK = new Soubor_popisovač_tabulka(systém_souborů);
        for (Map.Entry<Integer, popisovač_položka> položka_HODNOTA : 서술자들.entrySet()) {
            položka_HODNOTA.getValue().열린파일.odkaz_POČET++;
            popisovač_položka 새서술자 = new popisovač_položka(položka_HODNOTA.getValue().열린파일);
            새서술자.실행시닫기 = položka_HODNOTA.getValue().실행시닫기;
            VÝSLEDEK.서술자들.put(položka_HODNOTA.getKey(), 새서술자);
        }
        return VÝSLEDEK;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
