// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.faýl_ulgamy;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Faýl 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final faýl_ulgamy.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(faýl_ulgamy.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final faýl_ulgamy faýl_ulgamy;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(faýl_ulgamy faýl_ulgamy) {
        this.faýl_ulgamy = faýl_ulgamy;
    }

    public int Aç(String Ad) {
        faýl_ulgamy.열린파일 열린파일 = faýl_ulgamy.Aç(Ad);
        if (열린파일 == null) {
            return -2;
        }
        int indeks = boş_indeks(3);
        if (indeks < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(indeks), new 서술자(열린파일));
        return indeks;
    }

    public int Oka(int indeks, byte[] 받을곳, int Ululyk) {
        서술자 girizmeklik_baha = 서술자들.get(Integer.valueOf(indeks));
        if (girizmeklik_baha == null) {
            return -9;
        }
        if (Ululyk < 0 || Ululyk > 받을곳.length) {
            return -22;
        }
        int 남음 = girizmeklik_baha.열린파일.maglumat.length - girizmeklik_baha.열린파일.위치;
        int 읽을크기 = Math.min(Ululyk, Math.max(남음, 0));
        System.arraycopy(girizmeklik_baha.열린파일.maglumat, girizmeklik_baha.열린파일.위치, 받을곳, 0, 읽을크기);
        girizmeklik_baha.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int indeks, int 거리, int 기준) {
        서술자 girizmeklik_baha = 서술자들.get(Integer.valueOf(indeks));
        if (girizmeklik_baha == null) {
            return -9;
        }
        int Fon_baha;
        if (기준 == 0) {
            Fon_baha = 0;
        } else if (기준 == 1) {
            Fon_baha = girizmeklik_baha.열린파일.위치;
        } else if (기준 == 2) {
            Fon_baha = girizmeklik_baha.열린파일.maglumat.length;
        } else {
            return -22;
        }
        int 새위치 = Fon_baha + 거리;
        if (새위치 < 0) {
            return -22;
        }
        girizmeklik_baha.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Ýap(int indeks) {
        서술자 girizmeklik_baha = 서술자들.remove(Integer.valueOf(indeks));
        if (girizmeklik_baha == null) {
            return -9;
        }
        girizmeklik_baha.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int indeks, int 최소번호) {
        서술자 girizmeklik_baha = 서술자들.get(Integer.valueOf(indeks));
        if (girizmeklik_baha == null) {
            return -9;
        }
        int 새번호 = boş_indeks(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        girizmeklik_baha.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(girizmeklik_baha.열린파일));
        return 새번호;
    }

    public int 지정복제(int indeks, int 새번호) {
        if (indeks == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(indeks)) ? indeks : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(indeks));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Ýap(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int indeks, boolean baha) {
        서술자 girizmeklik_baha = 서술자들.get(Integer.valueOf(indeks));
        if (girizmeklik_baha == null) {
            return -9;
        }
        girizmeklik_baha.실행시닫기 = baha;
        return 0;
    }

    public int 실행시닫기값(int indeks) {
        서술자 girizmeklik_baha = 서술자들.get(Integer.valueOf(indeks));
        if (girizmeklik_baha == null) {
            return -9;
        }
        return girizmeklik_baha.실행시닫기 ? 1 : 0;
    }

    public faýl_maglumat msinfo32_exe(int indeks) {
        if (indeks >= 0 && indeks <= 2) {
            return new faýl_maglumat(0, 0020666);
        }
        서술자 girizmeklik_baha = 서술자들.get(Integer.valueOf(indeks));
        if (girizmeklik_baha == null) {
            return null;
        }
        return new faýl_maglumat(girizmeklik_baha.열린파일.maglumat.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer indeks : 번호들) {
            서술자 girizmeklik_baha = 서술자들.get(indeks);
            if (girizmeklik_baha != null && girizmeklik_baha.실행시닫기) {
                Ýap(indeks.intValue());
            }
        }
    }

    public boolean 열려있음(int indeks) {
        return 서술자들.containsKey(Integer.valueOf(indeks));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(faýl_ulgamy);
        for (Map.Entry<Integer, 서술자> girizmeklik_baha : 서술자들.entrySet()) {
            girizmeklik_baha.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(girizmeklik_baha.getValue().열린파일);
            새서술자.실행시닫기 = girizmeklik_baha.getValue().실행시닫기;
            결과.서술자들.put(girizmeklik_baha.getKey(), 새서술자);
        }
        return 결과;
    }

    private int boş_indeks(int 최소번호) {
        for (int indeks = Math.max(0, 최소번호); indeks < 최대서술자; indeks++) {
            if (!서술자들.containsKey(Integer.valueOf(indeks))) {
                return indeks;
            }
        }
        return -1;
    }
}
