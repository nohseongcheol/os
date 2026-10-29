// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.filsystem;

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

    public int Åpne(String Navn) {
        filsystem.열린파일 열린파일 = filsystem.Åpne(Navn);
        if (열린파일 == null) {
            return -2;
        }
        int INDEKS = tom_INDEKS(3);
        if (INDEKS < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEKS), new 서술자(열린파일));
        return INDEKS;
    }

    public int Les(int INDEKS, byte[] motta_mål, int Størrelse) {
        서술자 oppføring_VERDI = 서술자들.get(Integer.valueOf(INDEKS));
        if (oppføring_VERDI == null) {
            return -9;
        }
        if (Størrelse < 0 || Størrelse > motta_mål.length) {
            return -22;
        }
        int 남음 = oppføring_VERDI.열린파일.data.length - oppføring_VERDI.열린파일.Posisjon;
        int 읽을크기 = Math.min(Størrelse, Math.max(남음, 0));
        System.arraycopy(oppføring_VERDI.열린파일.data, oppføring_VERDI.열린파일.Posisjon, motta_mål, 0, 읽을크기);
        oppføring_VERDI.열린파일.Posisjon += 읽을크기;
        return 읽을크기;
    }

    public int flytte_plassere(int INDEKS, int 거리, int speile_rot) {
        서술자 oppføring_VERDI = 서술자들.get(Integer.valueOf(INDEKS));
        if (oppføring_VERDI == null) {
            return -9;
        }
        int bakgrunn_VERDI;
        if (speile_rot == 0) {
            bakgrunn_VERDI = 0;
        } else if (speile_rot == 1) {
            bakgrunn_VERDI = oppføring_VERDI.열린파일.Posisjon;
        } else if (speile_rot == 2) {
            bakgrunn_VERDI = oppføring_VERDI.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = bakgrunn_VERDI + 거리;
        if (새위치 < 0) {
            return -22;
        }
        oppføring_VERDI.열린파일.Posisjon = 새위치;
        return 새위치;
    }

    public int Lukk(int INDEKS) {
        서술자 oppføring_VERDI = 서술자들.remove(Integer.valueOf(INDEKS));
        if (oppføring_VERDI == null) {
            return -9;
        }
        oppføring_VERDI.열린파일.referere_ANTALL--;
        return 0;
    }

    public int 복제서술자(int INDEKS, int 최소번호) {
        서술자 oppføring_VERDI = 서술자들.get(Integer.valueOf(INDEKS));
        if (oppføring_VERDI == null) {
            return -9;
        }
        int 새번호 = tom_INDEKS(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        oppføring_VERDI.열린파일.referere_ANTALL++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(oppføring_VERDI.열린파일));
        return 새번호;
    }

    public int 지정복제(int INDEKS, int 새번호) {
        if (INDEKS == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(INDEKS)) ? INDEKS : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEKS));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Lukk(새번호);
        }
        원본.열린파일.referere_ANTALL++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEKS, boolean VERDI) {
        서술자 oppføring_VERDI = 서술자들.get(Integer.valueOf(INDEKS));
        if (oppføring_VERDI == null) {
            return -9;
        }
        oppføring_VERDI.실행시닫기 = VERDI;
        return 0;
    }

    public int 실행시닫기값(int INDEKS) {
        서술자 oppføring_VERDI = 서술자들.get(Integer.valueOf(INDEKS));
        if (oppføring_VERDI == null) {
            return -9;
        }
        return oppføring_VERDI.실행시닫기 ? 1 : 0;
    }

    public Fil_info msinfo32_exe(int INDEKS) {
        if (INDEKS >= 0 && INDEKS <= 2) {
            return new Fil_info(0, 0020666);
        }
        서술자 oppføring_VERDI = 서술자들.get(Integer.valueOf(INDEKS));
        if (oppføring_VERDI == null) {
            return null;
        }
        return new Fil_info(oppføring_VERDI.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] nummer_Liste = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEKS : nummer_Liste) {
            서술자 oppføring_VERDI = 서술자들.get(INDEKS);
            if (oppføring_VERDI != null && oppføring_VERDI.실행시닫기) {
                Lukk(INDEKS.intValue());
            }
        }
    }

    public boolean informasjonssystemer_åpen(int INDEKS) {
        return 서술자들.containsKey(Integer.valueOf(INDEKS));
    }

    public 파일서술자표 klon_VERDI() {
        파일서술자표 KR = new 파일서술자표(filsystem);
        for (Map.Entry<Integer, 서술자> oppføring_VERDI : 서술자들.entrySet()) {
            oppføring_VERDI.getValue().열린파일.referere_ANTALL++;
            서술자 새서술자 = new 서술자(oppføring_VERDI.getValue().열린파일);
            새서술자.실행시닫기 = oppføring_VERDI.getValue().실행시닫기;
            KR.서술자들.put(oppføring_VERDI.getKey(), 새서술자);
        }
        return KR;
    }

    private int tom_INDEKS(int 최소번호) {
        for (int INDEKS = Math.max(0, 최소번호); INDEKS < 최대서술자; INDEKS++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEKS))) {
                return INDEKS;
            }
        }
        return -1;
    }
}
