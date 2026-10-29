// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Fichierssystem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fichier 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final Fichierssystem.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(Fichierssystem.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final Fichierssystem Fichierssystem;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(Fichierssystem Fichierssystem) {
        this.Fichierssystem = Fichierssystem;
    }

    public int ariichten(String Numm) {
        Fichierssystem.열린파일 열린파일 = Fichierssystem.ariichten(Numm);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = eidel_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int 읽기(int INDEX, byte[] 받을곳, int d_Gréisst_veränneren) {
        서술자 Agab_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (Agab_VALUE == null) {
            return -9;
        }
        if (d_Gréisst_veränneren < 0 || d_Gréisst_veränneren > 받을곳.length) {
            return -22;
        }
        int 남음 = Agab_VALUE.열린파일.Daten.length - Agab_VALUE.열린파일.positionéieren;
        int 읽을크기 = Math.min(d_Gréisst_veränneren, Math.max(남음, 0));
        System.arraycopy(Agab_VALUE.열린파일.Daten, Agab_VALUE.열린파일.positionéieren, 받을곳, 0, 읽을크기);
        Agab_VALUE.열린파일.positionéieren += 읽을크기;
        return 읽을크기;
    }

    public int verréckelen_positionéieren(int INDEX, int 거리, int projezéieren_Racinn) {
        서술자 Agab_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (Agab_VALUE == null) {
            return -9;
        }
        int Hannergrond_VALUE;
        if (projezéieren_Racinn == 0) {
            Hannergrond_VALUE = 0;
        } else if (projezéieren_Racinn == 1) {
            Hannergrond_VALUE = Agab_VALUE.열린파일.positionéieren;
        } else if (projezéieren_Racinn == 2) {
            Hannergrond_VALUE = Agab_VALUE.열린파일.Daten.length;
        } else {
            return -22;
        }
        int 새위치 = Hannergrond_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        Agab_VALUE.열린파일.positionéieren = 새위치;
        return 새위치;
    }

    public int Clôture(int INDEX) {
        서술자 Agab_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (Agab_VALUE == null) {
            return -9;
        }
        Agab_VALUE.열린파일.Referenzen_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 Agab_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (Agab_VALUE == null) {
            return -9;
        }
        int 새번호 = eidel_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        Agab_VALUE.열린파일.Referenzen_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(Agab_VALUE.열린파일));
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
            Clôture(새번호);
        }
        원본.열린파일.Referenzen_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 Agab_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (Agab_VALUE == null) {
            return -9;
        }
        Agab_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 Agab_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (Agab_VALUE == null) {
            return -9;
        }
        return Agab_VALUE.실행시닫기 ? 1 : 0;
    }

    public Fichier_Info msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Fichier_Info(0, 0020666);
        }
        서술자 Agab_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (Agab_VALUE == null) {
            return null;
        }
        return new Fichier_Info(Agab_VALUE.열린파일.Daten.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 Agab_VALUE = 서술자들.get(INDEX);
            if (Agab_VALUE != null && Agab_VALUE.실행시닫기) {
                Clôture(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 Mooss = new 파일서술자표(Fichierssystem);
        for (Map.Entry<Integer, 서술자> Agab_VALUE : 서술자들.entrySet()) {
            Agab_VALUE.getValue().열린파일.Referenzen_COUNT++;
            서술자 새서술자 = new 서술자(Agab_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = Agab_VALUE.getValue().실행시닫기;
            Mooss.서술자들.put(Agab_VALUE.getKey(), 새서술자);
        }
        return Mooss;
    }

    private int eidel_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
