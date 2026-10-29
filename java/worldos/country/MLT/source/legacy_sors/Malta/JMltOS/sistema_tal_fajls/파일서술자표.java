// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.sistema_tal_fajls;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 fajl 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistema_tal_fajls.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistema_tal_fajls.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistema_tal_fajls sistema_tal_fajls;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistema_tal_fajls sistema_tal_fajls) {
        this.sistema_tal_fajls = sistema_tal_fajls;
    }

    public int fetaħ(String isem) {
        sistema_tal_fajls.열린파일 열린파일 = sistema_tal_fajls.fetaħ(isem);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = vojt_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int 읽기(int INDEX, byte[] 받을곳, int daqqas) {
        서술자 entrata_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entrata_VALUE == null) {
            return -9;
        }
        if (daqqas < 0 || daqqas > 받을곳.length) {
            return -22;
        }
        int 남음 = entrata_VALUE.열린파일.data.length - entrata_VALUE.열린파일.pożizzjoni;
        int 읽을크기 = Math.min(daqqas, Math.max(남음, 0));
        System.arraycopy(entrata_VALUE.열린파일.data, entrata_VALUE.열린파일.pożizzjoni, 받을곳, 0, 읽을크기);
        entrata_VALUE.열린파일.pożizzjoni += 읽을크기;
        return 읽을크기;
    }

    public int mexxi_pożizzjoni(int INDEX, int 거리, int pprojetta_għerq) {
        서술자 entrata_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entrata_VALUE == null) {
            return -9;
        }
        int Sfond_VALUE;
        if (pprojetta_għerq == 0) {
            Sfond_VALUE = 0;
        } else if (pprojetta_għerq == 1) {
            Sfond_VALUE = entrata_VALUE.열린파일.pożizzjoni;
        } else if (pprojetta_għerq == 2) {
            Sfond_VALUE = entrata_VALUE.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = Sfond_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        entrata_VALUE.열린파일.pożizzjoni = 새위치;
        return 새위치;
    }

    public int agħlaq(int INDEX) {
        서술자 entrata_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (entrata_VALUE == null) {
            return -9;
        }
        entrata_VALUE.열린파일.Referenza_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 entrata_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entrata_VALUE == null) {
            return -9;
        }
        int 새번호 = vojt_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        entrata_VALUE.열린파일.Referenza_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(entrata_VALUE.열린파일));
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
            agħlaq(새번호);
        }
        원본.열린파일.Referenza_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 entrata_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entrata_VALUE == null) {
            return -9;
        }
        entrata_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 entrata_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entrata_VALUE == null) {
            return -9;
        }
        return entrata_VALUE.실행시닫기 ? 1 : 0;
    }

    public fajl_informazzjoni msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new fajl_informazzjoni(0, 0020666);
        }
        서술자 entrata_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entrata_VALUE == null) {
            return null;
        }
        return new fajl_informazzjoni(entrata_VALUE.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 entrata_VALUE = 서술자들.get(INDEX);
            if (entrata_VALUE != null && entrata_VALUE.실행시닫기) {
                agħlaq(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 miżura = new 파일서술자표(sistema_tal_fajls);
        for (Map.Entry<Integer, 서술자> entrata_VALUE : 서술자들.entrySet()) {
            entrata_VALUE.getValue().열린파일.Referenza_COUNT++;
            서술자 새서술자 = new 서술자(entrata_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = entrata_VALUE.getValue().실행시닫기;
            miżura.서술자들.put(entrata_VALUE.getKey(), 새서술자);
        }
        return miżura;
    }

    private int vojt_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
