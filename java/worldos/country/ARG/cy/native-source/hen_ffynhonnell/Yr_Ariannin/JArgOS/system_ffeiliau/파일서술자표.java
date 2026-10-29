// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.system_ffeiliau;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Ffeil 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final system_ffeiliau.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(system_ffeiliau.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final system_ffeiliau system_ffeiliau;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(system_ffeiliau system_ffeiliau) {
        this.system_ffeiliau = system_ffeiliau;
    }

    public int Agor(String Enw) {
        system_ffeiliau.열린파일 열린파일 = system_ffeiliau.Agor(Enw);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = gwag_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Darllen(int INDEX, byte[] 받을곳, int Maint) {
        서술자 cofnod_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (cofnod_VALUE == null) {
            return -9;
        }
        if (Maint < 0 || Maint > 받을곳.length) {
            return -22;
        }
        int 남음 = cofnod_VALUE.열린파일.data.length - cofnod_VALUE.열린파일.safle;
        int 읽을크기 = Math.min(Maint, Math.max(남음, 0));
        System.arraycopy(cofnod_VALUE.열린파일.data, cofnod_VALUE.열린파일.safle, 받을곳, 0, 읽을크기);
        cofnod_VALUE.열린파일.safle += 읽을크기;
        return 읽을크기;
    }

    public int symud_safle(int INDEX, int 거리, int prosiect_gwraidd) {
        서술자 cofnod_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (cofnod_VALUE == null) {
            return -9;
        }
        int Cefndir_VALUE;
        if (prosiect_gwraidd == 0) {
            Cefndir_VALUE = 0;
        } else if (prosiect_gwraidd == 1) {
            Cefndir_VALUE = cofnod_VALUE.열린파일.safle;
        } else if (prosiect_gwraidd == 2) {
            Cefndir_VALUE = cofnod_VALUE.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = Cefndir_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        cofnod_VALUE.열린파일.safle = 새위치;
        return 새위치;
    }

    public int Cau(int INDEX) {
        서술자 cofnod_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (cofnod_VALUE == null) {
            return -9;
        }
        cofnod_VALUE.열린파일.cyfeiriad_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 cofnod_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (cofnod_VALUE == null) {
            return -9;
        }
        int 새번호 = gwag_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        cofnod_VALUE.열린파일.cyfeiriad_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(cofnod_VALUE.열린파일));
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
            Cau(새번호);
        }
        원본.열린파일.cyfeiriad_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 cofnod_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (cofnod_VALUE == null) {
            return -9;
        }
        cofnod_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 cofnod_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (cofnod_VALUE == null) {
            return -9;
        }
        return cofnod_VALUE.실행시닫기 ? 1 : 0;
    }

    public ffeil_gwybodaeth msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new ffeil_gwybodaeth(0, 0020666);
        }
        서술자 cofnod_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (cofnod_VALUE == null) {
            return null;
        }
        return new ffeil_gwybodaeth(cofnod_VALUE.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 cofnod_VALUE = 서술자들.get(INDEX);
            if (cofnod_VALUE != null && cofnod_VALUE.실행시닫기) {
                Cau(INDEX.intValue());
            }
        }
    }

    public boolean technoleg_gwybodaeth_agor(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 mesur = new 파일서술자표(system_ffeiliau);
        for (Map.Entry<Integer, 서술자> cofnod_VALUE : 서술자들.entrySet()) {
            cofnod_VALUE.getValue().열린파일.cyfeiriad_COUNT++;
            서술자 새서술자 = new 서술자(cofnod_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = cofnod_VALUE.getValue().실행시닫기;
            mesur.서술자들.put(cofnod_VALUE.getKey(), 새서술자);
        }
        return mesur;
    }

    private int gwag_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
