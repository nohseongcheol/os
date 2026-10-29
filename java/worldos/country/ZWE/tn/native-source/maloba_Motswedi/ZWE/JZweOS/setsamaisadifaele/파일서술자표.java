// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ZWE.JZweOS.setsamaisadifaele;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 faele 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final setsamaisadifaele.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(setsamaisadifaele.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final setsamaisadifaele setsamaisadifaele;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(setsamaisadifaele setsamaisadifaele) {
        this.setsamaisadifaele = setsamaisadifaele;
    }

    public int bula(String leina) {
        setsamaisadifaele.열린파일 열린파일 = setsamaisadifaele.bula(leina);
        if (열린파일 == null) {
            return -2;
        }
        int tshupane = lolea_tshupane(3);
        if (tshupane < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(tshupane), new 서술자(열린파일));
        return tshupane;
    }

    public int 읽기(int tshupane, byte[] 받을곳, int lekanya) {
        서술자 tsenyo_Boleng = 서술자들.get(Integer.valueOf(tshupane));
        if (tsenyo_Boleng == null) {
            return -9;
        }
        if (lekanya < 0 || lekanya > 받을곳.length) {
            return -22;
        }
        int 남음 = tsenyo_Boleng.열린파일.tshedimosetso.length - tsenyo_Boleng.열린파일.위치;
        int 읽을크기 = Math.min(lekanya, Math.max(남음, 0));
        System.arraycopy(tsenyo_Boleng.열린파일.tshedimosetso, tsenyo_Boleng.열린파일.위치, 받을곳, 0, 읽을크기);
        tsenyo_Boleng.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int tshupane, int 거리, int 기준) {
        서술자 tsenyo_Boleng = 서술자들.get(Integer.valueOf(tshupane));
        if (tsenyo_Boleng == null) {
            return -9;
        }
        int Lemorago_Boleng;
        if (기준 == 0) {
            Lemorago_Boleng = 0;
        } else if (기준 == 1) {
            Lemorago_Boleng = tsenyo_Boleng.열린파일.위치;
        } else if (기준 == 2) {
            Lemorago_Boleng = tsenyo_Boleng.열린파일.tshedimosetso.length;
        } else {
            return -22;
        }
        int 새위치 = Lemorago_Boleng + 거리;
        if (새위치 < 0) {
            return -22;
        }
        tsenyo_Boleng.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int tswala(int tshupane) {
        서술자 tsenyo_Boleng = 서술자들.remove(Integer.valueOf(tshupane));
        if (tsenyo_Boleng == null) {
            return -9;
        }
        tsenyo_Boleng.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int tshupane, int 최소번호) {
        서술자 tsenyo_Boleng = 서술자들.get(Integer.valueOf(tshupane));
        if (tsenyo_Boleng == null) {
            return -9;
        }
        int 새번호 = lolea_tshupane(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        tsenyo_Boleng.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(tsenyo_Boleng.열린파일));
        return 새번호;
    }

    public int 지정복제(int tshupane, int 새번호) {
        if (tshupane == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(tshupane)) ? tshupane : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(tshupane));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            tswala(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int tshupane, boolean Boleng) {
        서술자 tsenyo_Boleng = 서술자들.get(Integer.valueOf(tshupane));
        if (tsenyo_Boleng == null) {
            return -9;
        }
        tsenyo_Boleng.실행시닫기 = Boleng;
        return 0;
    }

    public int 실행시닫기값(int tshupane) {
        서술자 tsenyo_Boleng = 서술자들.get(Integer.valueOf(tshupane));
        if (tsenyo_Boleng == null) {
            return -9;
        }
        return tsenyo_Boleng.실행시닫기 ? 1 : 0;
    }

    public faele_tshedimosetso msinfo32_exe(int tshupane) {
        if (tshupane >= 0 && tshupane <= 2) {
            return new faele_tshedimosetso(0, 0020666);
        }
        서술자 tsenyo_Boleng = 서술자들.get(Integer.valueOf(tshupane));
        if (tsenyo_Boleng == null) {
            return null;
        }
        return new faele_tshedimosetso(tsenyo_Boleng.열린파일.tshedimosetso.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer tshupane : 번호들) {
            서술자 tsenyo_Boleng = 서술자들.get(tshupane);
            if (tsenyo_Boleng != null && tsenyo_Boleng.실행시닫기) {
                tswala(tshupane.intValue());
            }
        }
    }

    public boolean 열려있음(int tshupane) {
        return 서술자들.containsKey(Integer.valueOf(tshupane));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(setsamaisadifaele);
        for (Map.Entry<Integer, 서술자> tsenyo_Boleng : 서술자들.entrySet()) {
            tsenyo_Boleng.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(tsenyo_Boleng.getValue().열린파일);
            새서술자.실행시닫기 = tsenyo_Boleng.getValue().실행시닫기;
            결과.서술자들.put(tsenyo_Boleng.getKey(), 새서술자);
        }
        return 결과;
    }

    private int lolea_tshupane(int 최소번호) {
        for (int tshupane = Math.max(0, 최소번호); tshupane < 최대서술자; tshupane++) {
            if (!서술자들.containsKey(Integer.valueOf(tshupane))) {
                return tshupane;
            }
        }
        return -1;
    }
}
