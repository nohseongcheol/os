// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.filsystem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fil 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final filsystem.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(filsystem.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final filsystem filsystem;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(filsystem filsystem) {
        this.filsystem = filsystem;
    }

    public int Opna(String Namn) {
        filsystem.열린파일 열린파일 = filsystem.Opna(Namn);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = tom_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Les(int INDEX, byte[] 받을곳, int Storleik) {
        서술자 oppføring_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (oppføring_VALUE == null) {
            return -9;
        }
        if (Storleik < 0 || Storleik > 받을곳.length) {
            return -22;
        }
        int 남음 = oppføring_VALUE.열린파일.data.length - oppføring_VALUE.열린파일.Posisjon;
        int 읽을크기 = Math.min(Storleik, Math.max(남음, 0));
        System.arraycopy(oppføring_VALUE.열린파일.data, oppføring_VALUE.열린파일.Posisjon, 받을곳, 0, 읽을크기);
        oppføring_VALUE.열린파일.Posisjon += 읽을크기;
        return 읽을크기;
    }

    public int flytte_plassere(int INDEX, int 거리, int spegle_rot) {
        서술자 oppføring_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (oppføring_VALUE == null) {
            return -9;
        }
        int bakgrunn_VALUE;
        if (spegle_rot == 0) {
            bakgrunn_VALUE = 0;
        } else if (spegle_rot == 1) {
            bakgrunn_VALUE = oppføring_VALUE.열린파일.Posisjon;
        } else if (spegle_rot == 2) {
            bakgrunn_VALUE = oppføring_VALUE.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = bakgrunn_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        oppføring_VALUE.열린파일.Posisjon = 새위치;
        return 새위치;
    }

    public int Lukk(int INDEX) {
        서술자 oppføring_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (oppføring_VALUE == null) {
            return -9;
        }
        oppføring_VALUE.열린파일.Oppslagsverk_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 oppføring_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (oppføring_VALUE == null) {
            return -9;
        }
        int Nytt_nummer = tom_INDEX(최소번호);
        if (Nytt_nummer < 0) {
            return -24;
        }
        oppføring_VALUE.열린파일.Oppslagsverk_COUNT++;
        서술자들.put(Integer.valueOf(Nytt_nummer), new 서술자(oppføring_VALUE.열린파일));
        return Nytt_nummer;
    }

    public int 지정복제(int INDEX, int Nytt_nummer) {
        if (INDEX == Nytt_nummer) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Nytt_nummer < 0 || Nytt_nummer >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nytt_nummer))) {
            Lukk(Nytt_nummer);
        }
        원본.열린파일.Oppslagsverk_COUNT++;
        서술자들.put(Integer.valueOf(Nytt_nummer), new 서술자(원본.열린파일));
        return Nytt_nummer;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 oppføring_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (oppføring_VALUE == null) {
            return -9;
        }
        oppføring_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 oppføring_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (oppføring_VALUE == null) {
            return -9;
        }
        return oppføring_VALUE.실행시닫기 ? 1 : 0;
    }

    public fil_informasjon msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new fil_informasjon(0, 0020666);
        }
        서술자 oppføring_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (oppføring_VALUE == null) {
            return null;
        }
        return new fil_informasjon(oppføring_VALUE.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 oppføring_VALUE = 서술자들.get(INDEX);
            if (oppføring_VALUE != null && oppføring_VALUE.실행시닫기) {
                Lukk(INDEX.intValue());
            }
        }
    }

    public boolean informasjonsteknologi_opne(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 forretningsmål = new 파일서술자표(filsystem);
        for (Map.Entry<Integer, 서술자> oppføring_VALUE : 서술자들.entrySet()) {
            oppføring_VALUE.getValue().열린파일.Oppslagsverk_COUNT++;
            서술자 새서술자 = new 서술자(oppføring_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = oppføring_VALUE.getValue().실행시닫기;
            forretningsmål.서술자들.put(oppføring_VALUE.getKey(), 새서술자);
        }
        return forretningsmål;
    }

    private int tom_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
