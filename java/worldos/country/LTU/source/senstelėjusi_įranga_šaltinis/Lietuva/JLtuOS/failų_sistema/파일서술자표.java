// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuva.JLtuOS.failų_sistema;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Failas 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final failų_sistema.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(failų_sistema.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final failų_sistema failų_sistema;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(failų_sistema failų_sistema) {
        this.failų_sistema = failų_sistema;
    }

    public int Atverti(String Pavadinimas_2) {
        failų_sistema.열린파일 열린파일 = failų_sistema.Atverti(Pavadinimas_2);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = 빈번호(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Skaitymas(int INDEX, byte[] gauti_vieta, int Dydis) {
        서술자 įrašas_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (įrašas_VALUE == null) {
            return -9;
        }
        if (Dydis < 0 || Dydis > gauti_vieta.length) {
            return -22;
        }
        int 남음 = įrašas_VALUE.열린파일.duomenys.length - įrašas_VALUE.열린파일.Pozicija;
        int 읽을크기 = Math.min(Dydis, Math.max(남음, 0));
        System.arraycopy(įrašas_VALUE.열린파일.duomenys, įrašas_VALUE.열린파일.Pozicija, gauti_vieta, 0, 읽을크기);
        įrašas_VALUE.열린파일.Pozicija += 읽을크기;
        return 읽을크기;
    }

    public int judėti_padėtis(int INDEX, int 거리, int Project_šaknis) {
        서술자 įrašas_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (įrašas_VALUE == null) {
            return -9;
        }
        int Fonas_VALUE;
        if (Project_šaknis == 0) {
            Fonas_VALUE = 0;
        } else if (Project_šaknis == 1) {
            Fonas_VALUE = įrašas_VALUE.열린파일.Pozicija;
        } else if (Project_šaknis == 2) {
            Fonas_VALUE = įrašas_VALUE.열린파일.duomenys.length;
        } else {
            return -22;
        }
        int 새위치 = Fonas_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        įrašas_VALUE.열린파일.Pozicija = 새위치;
        return 새위치;
    }

    public int Užverti(int INDEX) {
        서술자 įrašas_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (įrašas_VALUE == null) {
            return -9;
        }
        įrašas_VALUE.열린파일.nuoroda_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 įrašas_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (įrašas_VALUE == null) {
            return -9;
        }
        int Naujas_numeris = 빈번호(최소번호);
        if (Naujas_numeris < 0) {
            return -24;
        }
        įrašas_VALUE.열린파일.nuoroda_COUNT++;
        서술자들.put(Integer.valueOf(Naujas_numeris), new 서술자(įrašas_VALUE.열린파일));
        return Naujas_numeris;
    }

    public int 지정복제(int INDEX, int Naujas_numeris) {
        if (INDEX == Naujas_numeris) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Naujas_numeris < 0 || Naujas_numeris >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Naujas_numeris))) {
            Užverti(Naujas_numeris);
        }
        원본.열린파일.nuoroda_COUNT++;
        서술자들.put(Integer.valueOf(Naujas_numeris), new 서술자(원본.열린파일));
        return Naujas_numeris;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 įrašas_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (įrašas_VALUE == null) {
            return -9;
        }
        įrašas_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 įrašas_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (įrašas_VALUE == null) {
            return -9;
        }
        return įrašas_VALUE.실행시닫기 ? 1 : 0;
    }

    public Failas_informacija msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Failas_informacija(0, 0020666);
        }
        서술자 įrašas_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (įrašas_VALUE == null) {
            return null;
        }
        return new Failas_informacija(įrašas_VALUE.열린파일.duomenys.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] numeris_Sąrašas = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : numeris_Sąrašas) {
            서술자 įrašas_VALUE = 서술자들.get(INDEX);
            if (įrašas_VALUE != null && įrašas_VALUE.실행시닫기) {
                Užverti(INDEX.intValue());
            }
        }
    }

    public boolean informacinės_technologijos_kurti(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klonas_VALUE() {
        파일서술자표 REZULTATAS = new 파일서술자표(failų_sistema);
        for (Map.Entry<Integer, 서술자> įrašas_VALUE : 서술자들.entrySet()) {
            įrašas_VALUE.getValue().열린파일.nuoroda_COUNT++;
            서술자 새서술자 = new 서술자(įrašas_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = įrašas_VALUE.getValue().실행시닫기;
            REZULTATAS.서술자들.put(įrašas_VALUE.getKey(), 새서술자);
        }
        return REZULTATAS;
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
