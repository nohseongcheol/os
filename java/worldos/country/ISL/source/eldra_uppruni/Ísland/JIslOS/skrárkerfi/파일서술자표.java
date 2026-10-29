// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.skrárkerfi;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Skrá 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final skrárkerfi.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(skrárkerfi.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final skrárkerfi skrárkerfi;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(skrárkerfi skrárkerfi) {
        this.skrárkerfi = skrárkerfi;
    }

    public int Opna(String Heiti) {
        skrárkerfi.열린파일 열린파일 = skrárkerfi.Opna(Heiti);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = autt_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Lestur(int INDEX, byte[] 받을곳, int Stærð) {
        서술자 færsla_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (færsla_VALUE == null) {
            return -9;
        }
        if (Stærð < 0 || Stærð > 받을곳.length) {
            return -22;
        }
        int 남음 = færsla_VALUE.열린파일.gögn.length - færsla_VALUE.열린파일.Staðsetning;
        int 읽을크기 = Math.min(Stærð, Math.max(남음, 0));
        System.arraycopy(færsla_VALUE.열린파일.gögn, færsla_VALUE.열린파일.Staðsetning, 받을곳, 0, 읽을크기);
        færsla_VALUE.열린파일.Staðsetning += 읽을크기;
        return 읽을크기;
    }

    public int færa_staða(int INDEX, int 거리, int verk_rót) {
        서술자 færsla_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (færsla_VALUE == null) {
            return -9;
        }
        int veggfóður_VALUE;
        if (verk_rót == 0) {
            veggfóður_VALUE = 0;
        } else if (verk_rót == 1) {
            veggfóður_VALUE = færsla_VALUE.열린파일.Staðsetning;
        } else if (verk_rót == 2) {
            veggfóður_VALUE = færsla_VALUE.열린파일.gögn.length;
        } else {
            return -22;
        }
        int 새위치 = veggfóður_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        færsla_VALUE.열린파일.Staðsetning = 새위치;
        return 새위치;
    }

    public int Loka(int INDEX) {
        서술자 færsla_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (færsla_VALUE == null) {
            return -9;
        }
        færsla_VALUE.열린파일.tilvísun_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 færsla_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (færsla_VALUE == null) {
            return -9;
        }
        int 새번호 = autt_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        færsla_VALUE.열린파일.tilvísun_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(færsla_VALUE.열린파일));
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
            Loka(새번호);
        }
        원본.열린파일.tilvísun_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 færsla_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (færsla_VALUE == null) {
            return -9;
        }
        færsla_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 færsla_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (færsla_VALUE == null) {
            return -9;
        }
        return færsla_VALUE.실행시닫기 ? 1 : 0;
    }

    public skrá_uppl msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new skrá_uppl(0, 0020666);
        }
        서술자 færsla_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (færsla_VALUE == null) {
            return null;
        }
        return new skrá_uppl(færsla_VALUE.열린파일.gögn.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] númer_Listi = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : númer_Listi) {
            서술자 færsla_VALUE = 서술자들.get(INDEX);
            if (færsla_VALUE != null && færsla_VALUE.실행시닫기) {
                Loka(INDEX.intValue());
            }
        }
    }

    public boolean upplýsingatækni_opið(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 NIÐURSTAÐA = new 파일서술자표(skrárkerfi);
        for (Map.Entry<Integer, 서술자> færsla_VALUE : 서술자들.entrySet()) {
            færsla_VALUE.getValue().열린파일.tilvísun_COUNT++;
            서술자 새서술자 = new 서술자(færsla_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = færsla_VALUE.getValue().실행시닫기;
            NIÐURSTAÐA.서술자들.put(færsla_VALUE.getKey(), 새서술자);
        }
        return NIÐURSTAÐA;
    }

    private int autt_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
