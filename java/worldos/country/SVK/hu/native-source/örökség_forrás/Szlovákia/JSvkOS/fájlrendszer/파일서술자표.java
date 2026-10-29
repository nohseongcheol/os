// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovákia.JSvkOS.fájlrendszer;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fájl 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final fájlrendszer.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(fájlrendszer.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final fájlrendszer fájlrendszer;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(fájlrendszer fájlrendszer) {
        this.fájlrendszer = fájlrendszer;
    }

    public int Megnyitás(String Név) {
        fájlrendszer.열린파일 열린파일 = fájlrendszer.Megnyitás(Név);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = üres_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Olvasás(int INDEX, byte[] fogad_cél, int Méret) {
        서술자 bejegyzés_ÉRTÉK = 서술자들.get(Integer.valueOf(INDEX));
        if (bejegyzés_ÉRTÉK == null) {
            return -9;
        }
        if (Méret < 0 || Méret > fogad_cél.length) {
            return -22;
        }
        int 남음 = bejegyzés_ÉRTÉK.열린파일.adat.length - bejegyzés_ÉRTÉK.열린파일.Pozíció;
        int 읽을크기 = Math.min(Méret, Math.max(남음, 0));
        System.arraycopy(bejegyzés_ÉRTÉK.열린파일.adat, bejegyzés_ÉRTÉK.열린파일.Pozíció, fogad_cél, 0, 읽을크기);
        bejegyzés_ÉRTÉK.열린파일.Pozíció += 읽을크기;
        return 읽을크기;
    }

    public int áthelyez_pozíció(int INDEX, int 거리, int teendő_gyök) {
        서술자 bejegyzés_ÉRTÉK = 서술자들.get(Integer.valueOf(INDEX));
        if (bejegyzés_ÉRTÉK == null) {
            return -9;
        }
        int Háttér_ÉRTÉK;
        if (teendő_gyök == 0) {
            Háttér_ÉRTÉK = 0;
        } else if (teendő_gyök == 1) {
            Háttér_ÉRTÉK = bejegyzés_ÉRTÉK.열린파일.Pozíció;
        } else if (teendő_gyök == 2) {
            Háttér_ÉRTÉK = bejegyzés_ÉRTÉK.열린파일.adat.length;
        } else {
            return -22;
        }
        int 새위치 = Háttér_ÉRTÉK + 거리;
        if (새위치 < 0) {
            return -22;
        }
        bejegyzés_ÉRTÉK.열린파일.Pozíció = 새위치;
        return 새위치;
    }

    public int Bezárás(int INDEX) {
        서술자 bejegyzés_ÉRTÉK = 서술자들.remove(Integer.valueOf(INDEX));
        if (bejegyzés_ÉRTÉK == null) {
            return -9;
        }
        bejegyzés_ÉRTÉK.열린파일.hivatkozik_DARAB--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 bejegyzés_ÉRTÉK = 서술자들.get(Integer.valueOf(INDEX));
        if (bejegyzés_ÉRTÉK == null) {
            return -9;
        }
        int Új_telefonszám = üres_INDEX(최소번호);
        if (Új_telefonszám < 0) {
            return -24;
        }
        bejegyzés_ÉRTÉK.열린파일.hivatkozik_DARAB++;
        서술자들.put(Integer.valueOf(Új_telefonszám), new 서술자(bejegyzés_ÉRTÉK.열린파일));
        return Új_telefonszám;
    }

    public int 지정복제(int INDEX, int Új_telefonszám) {
        if (INDEX == Új_telefonszám) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Új_telefonszám < 0 || Új_telefonszám >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Új_telefonszám))) {
            Bezárás(Új_telefonszám);
        }
        원본.열린파일.hivatkozik_DARAB++;
        서술자들.put(Integer.valueOf(Új_telefonszám), new 서술자(원본.열린파일));
        return Új_telefonszám;
    }

    public int 실행시닫기설정(int INDEX, boolean ÉRTÉK) {
        서술자 bejegyzés_ÉRTÉK = 서술자들.get(Integer.valueOf(INDEX));
        if (bejegyzés_ÉRTÉK == null) {
            return -9;
        }
        bejegyzés_ÉRTÉK.실행시닫기 = ÉRTÉK;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 bejegyzés_ÉRTÉK = 서술자들.get(Integer.valueOf(INDEX));
        if (bejegyzés_ÉRTÉK == null) {
            return -9;
        }
        return bejegyzés_ÉRTÉK.실행시닫기 ? 1 : 0;
    }

    public Fájl_infó msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Fájl_infó(0, 0020666);
        }
        서술자 bejegyzés_ÉRTÉK = 서술자들.get(Integer.valueOf(INDEX));
        if (bejegyzés_ÉRTÉK == null) {
            return null;
        }
        return new Fájl_infó(bejegyzés_ÉRTÉK.열린파일.adat.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] szám_Lista = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : szám_Lista) {
            서술자 bejegyzés_ÉRTÉK = 서술자들.get(INDEX);
            if (bejegyzés_ÉRTÉK != null && bejegyzés_ÉRTÉK.실행시닫기) {
                Bezárás(INDEX.intValue());
            }
        }
    }

    public boolean informatikai_részleg_készít(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klón_ÉRTÉK() {
        파일서술자표 KR = new 파일서술자표(fájlrendszer);
        for (Map.Entry<Integer, 서술자> bejegyzés_ÉRTÉK : 서술자들.entrySet()) {
            bejegyzés_ÉRTÉK.getValue().열린파일.hivatkozik_DARAB++;
            서술자 새서술자 = new 서술자(bejegyzés_ÉRTÉK.getValue().열린파일);
            새서술자.실행시닫기 = bejegyzés_ÉRTÉK.getValue().실행시닫기;
            KR.서술자들.put(bejegyzés_ÉRTÉK.getKey(), 새서술자);
        }
        return KR;
    }

    private int üres_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
