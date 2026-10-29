// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Azərbaycan.JAzeOS.fayl_sistemi;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 FAYL 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final fayl_sistemi.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(fayl_sistemi.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final fayl_sistemi fayl_sistemi;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(fayl_sistemi fayl_sistemi) {
        this.fayl_sistemi = fayl_sistemi;
    }

    public int Aç(String Ad) {
        fayl_sistemi.열린파일 열린파일 = fayl_sistemi.Aç(Ad);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = boş_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Oxuma(int INDEX, byte[] 받을곳, int Böyüklük) {
        서술자 daxiletmə_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (daxiletmə_VALUE == null) {
            return -9;
        }
        if (Böyüklük < 0 || Böyüklük > 받을곳.length) {
            return -22;
        }
        int 남음 = daxiletmə_VALUE.열린파일.verilənlər.length - daxiletmə_VALUE.열린파일.yerinə_qoymaq;
        int 읽을크기 = Math.min(Böyüklük, Math.max(남음, 0));
        System.arraycopy(daxiletmə_VALUE.열린파일.verilənlər, daxiletmə_VALUE.열린파일.yerinə_qoymaq, 받을곳, 0, 읽을크기);
        daxiletmə_VALUE.열린파일.yerinə_qoymaq += 읽을크기;
        return 읽을크기;
    }

    public int hərəkət_etdir_yerinə_qoymaq(int INDEX, int 거리, int Project_kök) {
        서술자 daxiletmə_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (daxiletmə_VALUE == null) {
            return -9;
        }
        int Fon_VALUE;
        if (Project_kök == 0) {
            Fon_VALUE = 0;
        } else if (Project_kök == 1) {
            Fon_VALUE = daxiletmə_VALUE.열린파일.yerinə_qoymaq;
        } else if (Project_kök == 2) {
            Fon_VALUE = daxiletmə_VALUE.열린파일.verilənlər.length;
        } else {
            return -22;
        }
        int 새위치 = Fon_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        daxiletmə_VALUE.열린파일.yerinə_qoymaq = 새위치;
        return 새위치;
    }

    public int Bağla(int INDEX) {
        서술자 daxiletmə_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (daxiletmə_VALUE == null) {
            return -9;
        }
        daxiletmə_VALUE.열린파일.İstinad_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 daxiletmə_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (daxiletmə_VALUE == null) {
            return -9;
        }
        int 새번호 = boş_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        daxiletmə_VALUE.열린파일.İstinad_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(daxiletmə_VALUE.열린파일));
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
            Bağla(새번호);
        }
        원본.열린파일.İstinad_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 daxiletmə_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (daxiletmə_VALUE == null) {
            return -9;
        }
        daxiletmə_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 daxiletmə_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (daxiletmə_VALUE == null) {
            return -9;
        }
        return daxiletmə_VALUE.실행시닫기 ? 1 : 0;
    }

    public fayl_məlumat msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new fayl_məlumat(0, 0020666);
        }
        서술자 daxiletmə_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (daxiletmə_VALUE == null) {
            return null;
        }
        return new fayl_məlumat(daxiletmə_VALUE.열린파일.verilənlər.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 daxiletmə_VALUE = 서술자들.get(INDEX);
            if (daxiletmə_VALUE != null && daxiletmə_VALUE.실행시닫기) {
                Bağla(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 ölçü = new 파일서술자표(fayl_sistemi);
        for (Map.Entry<Integer, 서술자> daxiletmə_VALUE : 서술자들.entrySet()) {
            daxiletmə_VALUE.getValue().열린파일.İstinad_COUNT++;
            서술자 새서술자 = new 서술자(daxiletmə_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = daxiletmə_VALUE.getValue().실행시닫기;
            ölçü.서술자들.put(daxiletmə_VALUE.getKey(), 새서술자);
        }
        return ölçü;
    }

    private int boş_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
