// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republica_Moldova.JMdaOS.sistem_de_fișiere;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fișier 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistem_de_fișiere.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistem_de_fișiere.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistem_de_fișiere sistem_de_fișiere;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistem_de_fișiere sistem_de_fișiere) {
        this.sistem_de_fișiere = sistem_de_fișiere;
    }

    public int Deschide(String Nume) {
        sistem_de_fișiere.열린파일 열린파일 = sistem_de_fișiere.Deschide(Nume);
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

    public int Citire(int INDEX, byte[] primi_destinație, int Mărime) {
        서술자 intrare_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (intrare_VALUE == null) {
            return -9;
        }
        if (Mărime < 0 || Mărime > primi_destinație.length) {
            return -22;
        }
        int 남음 = intrare_VALUE.열린파일.date.length - intrare_VALUE.열린파일.Poziție;
        int 읽을크기 = Math.min(Mărime, Math.max(남음, 0));
        System.arraycopy(intrare_VALUE.열린파일.date, intrare_VALUE.열린파일.Poziție, primi_destinație, 0, 읽을크기);
        intrare_VALUE.열린파일.Poziție += 읽을크기;
        return 읽을크기;
    }

    public int muta_poziție(int INDEX, int 거리, int Project_rădăcină) {
        서술자 intrare_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (intrare_VALUE == null) {
            return -9;
        }
        int tapet_VALUE;
        if (Project_rădăcină == 0) {
            tapet_VALUE = 0;
        } else if (Project_rădăcină == 1) {
            tapet_VALUE = intrare_VALUE.열린파일.Poziție;
        } else if (Project_rădăcină == 2) {
            tapet_VALUE = intrare_VALUE.열린파일.date.length;
        } else {
            return -22;
        }
        int 새위치 = tapet_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        intrare_VALUE.열린파일.Poziție = 새위치;
        return 새위치;
    }

    public int Închide(int INDEX) {
        서술자 intrare_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (intrare_VALUE == null) {
            return -9;
        }
        intrare_VALUE.열린파일.referință_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 intrare_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (intrare_VALUE == null) {
            return -9;
        }
        int Număr_nou = 빈번호(최소번호);
        if (Număr_nou < 0) {
            return -24;
        }
        intrare_VALUE.열린파일.referință_COUNT++;
        서술자들.put(Integer.valueOf(Număr_nou), new 서술자(intrare_VALUE.열린파일));
        return Număr_nou;
    }

    public int 지정복제(int INDEX, int Număr_nou) {
        if (INDEX == Număr_nou) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Număr_nou < 0 || Număr_nou >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Număr_nou))) {
            Închide(Număr_nou);
        }
        원본.열린파일.referință_COUNT++;
        서술자들.put(Integer.valueOf(Număr_nou), new 서술자(원본.열린파일));
        return Număr_nou;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 intrare_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (intrare_VALUE == null) {
            return -9;
        }
        intrare_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 intrare_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (intrare_VALUE == null) {
            return -9;
        }
        return intrare_VALUE.실행시닫기 ? 1 : 0;
    }

    public Fișier_info msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Fișier_info(0, 0020666);
        }
        서술자 intrare_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (intrare_VALUE == null) {
            return null;
        }
        return new Fișier_info(intrare_VALUE.열린파일.date.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 intrare_VALUE = 서술자들.get(INDEX);
            if (intrare_VALUE != null && intrare_VALUE.실행시닫기) {
                Închide(INDEX.intValue());
            }
        }
    }

    public boolean sisteme_de_informații_crea(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 clona_VALUE() {
        파일서술자표 KR = new 파일서술자표(sistem_de_fișiere);
        for (Map.Entry<Integer, 서술자> intrare_VALUE : 서술자들.entrySet()) {
            intrare_VALUE.getValue().열린파일.referință_COUNT++;
            서술자 새서술자 = new 서술자(intrare_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = intrare_VALUE.getValue().실행시닫기;
            KR.서술자들.put(intrare_VALUE.getKey(), 새서술자);
        }
        return KR;
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
