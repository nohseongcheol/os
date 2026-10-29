// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.a_yatawaajiraaya_anaajaalaairua;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 anaajaalaa 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final a_yatawaajiraaya_anaajaalaairua.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(a_yatawaajiraaya_anaajaalaairua.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final a_yatawaajiraaya_anaajaalaairua a_yatawaajiraaya_anaajaalaairua;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(a_yatawaajiraaya_anaajaalaairua a_yatawaajiraaya_anaajaalaairua) {
        this.a_yatawaajiraaya_anaajaalaairua = a_yatawaajiraaya_anaajaalaairua;
    }

    public int 열기(String 이름) {
        a_yatawaajiraaya_anaajaalaairua.열린파일 열린파일 = a_yatawaajiraaya_anaajaalaairua.열기(이름);
        if (열린파일 == null) {
            return -2;
        }
        int ee_iyatialujuna = 빈번호(3);
        if (ee_iyatialujuna < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ee_iyatialujuna), new 서술자(열린파일));
        return ee_iyatialujuna;
    }

    public int 읽기(int ee_iyatialujuna, byte[] 받을곳, int 크기) {
        서술자 ekeroliaa_ajutuu = 서술자들.get(Integer.valueOf(ee_iyatialujuna));
        if (ekeroliaa_ajutuu == null) {
            return -9;
        }
        if (크기 < 0 || 크기 > 받을곳.length) {
            return -22;
        }
        int 남음 = ekeroliaa_ajutuu.열린파일.atijaaya.length - ekeroliaa_ajutuu.열린파일.위치;
        int 읽을크기 = Math.min(크기, Math.max(남음, 0));
        System.arraycopy(ekeroliaa_ajutuu.열린파일.atijaaya, ekeroliaa_ajutuu.열린파일.위치, 받을곳, 0, 읽을크기);
        ekeroliaa_ajutuu.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int ee_iyatialujuna, int 거리, int 기준) {
        서술자 ekeroliaa_ajutuu = 서술자들.get(Integer.valueOf(ee_iyatialujuna));
        if (ekeroliaa_ajutuu == null) {
            return -9;
        }
        int apa_ajanaa_ajutuu;
        if (기준 == 0) {
            apa_ajanaa_ajutuu = 0;
        } else if (기준 == 1) {
            apa_ajanaa_ajutuu = ekeroliaa_ajutuu.열린파일.위치;
        } else if (기준 == 2) {
            apa_ajanaa_ajutuu = ekeroliaa_ajutuu.열린파일.atijaaya.length;
        } else {
            return -22;
        }
        int 새위치 = apa_ajanaa_ajutuu + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ekeroliaa_ajutuu.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int asürülaa(int ee_iyatialujuna) {
        서술자 ekeroliaa_ajutuu = 서술자들.remove(Integer.valueOf(ee_iyatialujuna));
        if (ekeroliaa_ajutuu == null) {
            return -9;
        }
        ekeroliaa_ajutuu.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ee_iyatialujuna, int 최소번호) {
        서술자 ekeroliaa_ajutuu = 서술자들.get(Integer.valueOf(ee_iyatialujuna));
        if (ekeroliaa_ajutuu == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ekeroliaa_ajutuu.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ekeroliaa_ajutuu.열린파일));
        return 새번호;
    }

    public int 지정복제(int ee_iyatialujuna, int 새번호) {
        if (ee_iyatialujuna == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ee_iyatialujuna)) ? ee_iyatialujuna : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ee_iyatialujuna));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            asürülaa(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ee_iyatialujuna, boolean ajutuu) {
        서술자 ekeroliaa_ajutuu = 서술자들.get(Integer.valueOf(ee_iyatialujuna));
        if (ekeroliaa_ajutuu == null) {
            return -9;
        }
        ekeroliaa_ajutuu.실행시닫기 = ajutuu;
        return 0;
    }

    public int 실행시닫기값(int ee_iyatialujuna) {
        서술자 ekeroliaa_ajutuu = 서술자들.get(Integer.valueOf(ee_iyatialujuna));
        if (ekeroliaa_ajutuu == null) {
            return -9;
        }
        return ekeroliaa_ajutuu.실행시닫기 ? 1 : 0;
    }

    public 파일정보 정보(int ee_iyatialujuna) {
        if (ee_iyatialujuna >= 0 && ee_iyatialujuna <= 2) {
            return new 파일정보(0, 0020666);
        }
        서술자 ekeroliaa_ajutuu = 서술자들.get(Integer.valueOf(ee_iyatialujuna));
        if (ekeroliaa_ajutuu == null) {
            return null;
        }
        return new 파일정보(ekeroliaa_ajutuu.열린파일.atijaaya.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ee_iyatialujuna : 번호들) {
            서술자 ekeroliaa_ajutuu = 서술자들.get(ee_iyatialujuna);
            if (ekeroliaa_ajutuu != null && ekeroliaa_ajutuu.실행시닫기) {
                asürülaa(ee_iyatialujuna.intValue());
            }
        }
    }

    public boolean 열려있음(int ee_iyatialujuna) {
        return 서술자들.containsKey(Integer.valueOf(ee_iyatialujuna));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(a_yatawaajiraaya_anaajaalaairua);
        for (Map.Entry<Integer, 서술자> ekeroliaa_ajutuu : 서술자들.entrySet()) {
            ekeroliaa_ajutuu.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ekeroliaa_ajutuu.getValue().열린파일);
            새서술자.실행시닫기 = ekeroliaa_ajutuu.getValue().실행시닫기;
            결과.서술자들.put(ekeroliaa_ajutuu.getKey(), 새서술자);
        }
        return 결과;
    }

    private int 빈번호(int 최소번호) {
        for (int ee_iyatialujuna = Math.max(0, 최소번호); ee_iyatialujuna < 최대서술자; ee_iyatialujuna++) {
            if (!서술자들.containsKey(Integer.valueOf(ee_iyatialujuna))) {
                return ee_iyatialujuna;
            }
        }
        return -1;
    }
}
