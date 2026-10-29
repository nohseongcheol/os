// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.failu_sistēma;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fails 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final failu_sistēma.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(failu_sistēma.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final failu_sistēma failu_sistēma;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(failu_sistēma failu_sistēma) {
        this.failu_sistēma = failu_sistēma;
    }

    public int Atvērt(String Nosaukums) {
        failu_sistēma.열린파일 열린파일 = failu_sistēma.Atvērt(Nosaukums);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = 빈번호(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Lasīt(int INDEX, byte[] saņemt_mērķis, int Izmērs) {
        서술자 ievade_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (ievade_VALUE == null) {
            return -9;
        }
        if (Izmērs < 0 || Izmērs > saņemt_mērķis.length) {
            return -22;
        }
        int 남음 = ievade_VALUE.열린파일.dati.length - ievade_VALUE.열린파일.Novietojums;
        int 읽을크기 = Math.min(Izmērs, Math.max(남음, 0));
        System.arraycopy(ievade_VALUE.열린파일.dati, ievade_VALUE.열린파일.Novietojums, saņemt_mērķis, 0, 읽을크기);
        ievade_VALUE.열린파일.Novietojums += 읽을크기;
        return 읽을크기;
    }

    public int pārvietot_amats(int INDEX, int 거리, int Project_sakne) {
        서술자 ievade_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (ievade_VALUE == null) {
            return -9;
        }
        int Fons_VALUE;
        if (Project_sakne == 0) {
            Fons_VALUE = 0;
        } else if (Project_sakne == 1) {
            Fons_VALUE = ievade_VALUE.열린파일.Novietojums;
        } else if (Project_sakne == 2) {
            Fons_VALUE = ievade_VALUE.열린파일.dati.length;
        } else {
            return -22;
        }
        int 새위치 = Fons_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ievade_VALUE.열린파일.Novietojums = 새위치;
        return 새위치;
    }

    public int Aizvērt(int INDEX) {
        서술자 ievade_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (ievade_VALUE == null) {
            return -9;
        }
        ievade_VALUE.열린파일.Uzziņas_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 ievade_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (ievade_VALUE == null) {
            return -9;
        }
        int Jauns_numurs = 빈번호(최소번호);
        if (Jauns_numurs < 0) {
            return -24;
        }
        ievade_VALUE.열린파일.Uzziņas_COUNT++;
        서술자들.put(Integer.valueOf(Jauns_numurs), new 서술자(ievade_VALUE.열린파일));
        return Jauns_numurs;
    }

    public int 지정복제(int INDEX, int Jauns_numurs) {
        if (INDEX == Jauns_numurs) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Jauns_numurs < 0 || Jauns_numurs >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Jauns_numurs))) {
            Aizvērt(Jauns_numurs);
        }
        원본.열린파일.Uzziņas_COUNT++;
        서술자들.put(Integer.valueOf(Jauns_numurs), new 서술자(원본.열린파일));
        return Jauns_numurs;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 ievade_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (ievade_VALUE == null) {
            return -9;
        }
        ievade_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 ievade_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (ievade_VALUE == null) {
            return -9;
        }
        return ievade_VALUE.실행시닫기 ? 1 : 0;
    }

    public Fails_informācija msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Fails_informācija(0, 0020666);
        }
        서술자 ievade_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (ievade_VALUE == null) {
            return null;
        }
        return new Fails_informācija(ievade_VALUE.열린파일.dati.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] numurs_Saraksts = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : numurs_Saraksts) {
            서술자 ievade_VALUE = 서술자들.get(INDEX);
            if (ievade_VALUE != null && ievade_VALUE.실행시닫기) {
                Aizvērt(INDEX.intValue());
            }
        }
    }

    public boolean informācijas_tehnoloģija_atvērt(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klons_VALUE() {
        파일서술자표 mērs = new 파일서술자표(failu_sistēma);
        for (Map.Entry<Integer, 서술자> ievade_VALUE : 서술자들.entrySet()) {
            ievade_VALUE.getValue().열린파일.Uzziņas_COUNT++;
            서술자 새서술자 = new 서술자(ievade_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = ievade_VALUE.getValue().실행시닫기;
            mērs.서술자들.put(ievade_VALUE.getKey(), 새서술자);
        }
        return mērs;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
