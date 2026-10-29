// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.lêerstelsel;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Lêer 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final lêerstelsel.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(lêerstelsel.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final lêerstelsel lêerstelsel;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(lêerstelsel lêerstelsel) {
        this.lêerstelsel = lêerstelsel;
    }

    public int skep(String Naam) {
        lêerstelsel.열린파일 열린파일 = lêerstelsel.skep(Naam);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = leeg_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Lees(int INDEX, byte[] 받을곳, int Grootte) {
        서술자 inskrywing_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (inskrywing_VALUE == null) {
            return -9;
        }
        if (Grootte < 0 || Grootte > 받을곳.length) {
            return -22;
        }
        int 남음 = inskrywing_VALUE.열린파일.data.length - inskrywing_VALUE.열린파일.Posisie;
        int 읽을크기 = Math.min(Grootte, Math.max(남음, 0));
        System.arraycopy(inskrywing_VALUE.열린파일.data, inskrywing_VALUE.열린파일.Posisie, 받을곳, 0, 읽을크기);
        inskrywing_VALUE.열린파일.Posisie += 읽을크기;
        return 읽을크기;
    }

    public int skuif_plaas(int INDEX, int 거리, int Project_wortel) {
        서술자 inskrywing_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (inskrywing_VALUE == null) {
            return -9;
        }
        int muur_VALUE;
        if (Project_wortel == 0) {
            muur_VALUE = 0;
        } else if (Project_wortel == 1) {
            muur_VALUE = inskrywing_VALUE.열린파일.Posisie;
        } else if (Project_wortel == 2) {
            muur_VALUE = inskrywing_VALUE.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = muur_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        inskrywing_VALUE.열린파일.Posisie = 새위치;
        return 새위치;
    }

    public int Sluit(int INDEX) {
        서술자 inskrywing_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (inskrywing_VALUE == null) {
            return -9;
        }
        inskrywing_VALUE.열린파일.Naslaan_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 inskrywing_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (inskrywing_VALUE == null) {
            return -9;
        }
        int 새번호 = leeg_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        inskrywing_VALUE.열린파일.Naslaan_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(inskrywing_VALUE.열린파일));
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
            Sluit(새번호);
        }
        원본.열린파일.Naslaan_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 inskrywing_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (inskrywing_VALUE == null) {
            return -9;
        }
        inskrywing_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 inskrywing_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (inskrywing_VALUE == null) {
            return -9;
        }
        return inskrywing_VALUE.실행시닫기 ? 1 : 0;
    }

    public lêer_inligting Stelselinfo(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new lêer_inligting(0, 0020666);
        }
        서술자 inskrywing_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (inskrywing_VALUE == null) {
            return null;
        }
        return new lêer_inligting(inskrywing_VALUE.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 inskrywing_VALUE = 서술자들.get(INDEX);
            if (inskrywing_VALUE != null && inskrywing_VALUE.실행시닫기) {
                Sluit(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 maatreël = new 파일서술자표(lêerstelsel);
        for (Map.Entry<Integer, 서술자> inskrywing_VALUE : 서술자들.entrySet()) {
            inskrywing_VALUE.getValue().열린파일.Naslaan_COUNT++;
            서술자 새서술자 = new 서술자(inskrywing_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = inskrywing_VALUE.getValue().실행시닫기;
            maatreël.서술자들.put(inskrywing_VALUE.getKey(), 새서술자);
        }
        return maatreël;
    }

    private int leeg_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
