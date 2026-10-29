// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.fitxategi_sistema;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fitxategia 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final fitxategi_sistema.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(fitxategi_sistema.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final fitxategi_sistema fitxategi_sistema;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(fitxategi_sistema fitxategi_sistema) {
        this.fitxategi_sistema = fitxategi_sistema;
    }

    public int Ireki(String Izena) {
        fitxategi_sistema.열린파일 열린파일 = fitxategi_sistema.Ireki(Izena);
        if (열린파일 == null) {
            return -2;
        }
        int INDIZE = 빈번호(3);
        if (INDIZE < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDIZE), new 서술자(열린파일));
        return INDIZE;
    }

    public int Irakurri(int INDIZE, byte[] 받을곳, int Tamaina) {
        서술자 sarrera_balio = 서술자들.get(Integer.valueOf(INDIZE));
        if (sarrera_balio == null) {
            return -9;
        }
        if (Tamaina < 0 || Tamaina > 받을곳.length) {
            return -22;
        }
        int 남음 = sarrera_balio.열린파일.datuak.length - sarrera_balio.열린파일.Posizioa;
        int 읽을크기 = Math.min(Tamaina, Math.max(남음, 0));
        System.arraycopy(sarrera_balio.열린파일.datuak, sarrera_balio.열린파일.Posizioa, 받을곳, 0, 읽을크기);
        sarrera_balio.열린파일.Posizioa += 읽을크기;
        return 읽을크기;
    }

    public int eraman_kargu(int INDIZE, int 거리, int Project_erro) {
        서술자 sarrera_balio = 서술자들.get(Integer.valueOf(INDIZE));
        if (sarrera_balio == null) {
            return -9;
        }
        int horma_paper_balio;
        if (Project_erro == 0) {
            horma_paper_balio = 0;
        } else if (Project_erro == 1) {
            horma_paper_balio = sarrera_balio.열린파일.Posizioa;
        } else if (Project_erro == 2) {
            horma_paper_balio = sarrera_balio.열린파일.datuak.length;
        } else {
            return -22;
        }
        int 새위치 = horma_paper_balio + 거리;
        if (새위치 < 0) {
            return -22;
        }
        sarrera_balio.열린파일.Posizioa = 새위치;
        return 새위치;
    }

    public int Itxi(int INDIZE) {
        서술자 sarrera_balio = 서술자들.remove(Integer.valueOf(INDIZE));
        if (sarrera_balio == null) {
            return -9;
        }
        sarrera_balio.열린파일.Erreferentzia_materiala_ZENBATU--;
        return 0;
    }

    public int 복제서술자(int INDIZE, int 최소번호) {
        서술자 sarrera_balio = 서술자들.get(Integer.valueOf(INDIZE));
        if (sarrera_balio == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        sarrera_balio.열린파일.Erreferentzia_materiala_ZENBATU++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(sarrera_balio.열린파일));
        return 새번호;
    }

    public int 지정복제(int INDIZE, int 새번호) {
        if (INDIZE == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(INDIZE)) ? INDIZE : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDIZE));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Itxi(새번호);
        }
        원본.열린파일.Erreferentzia_materiala_ZENBATU++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDIZE, boolean balio) {
        서술자 sarrera_balio = 서술자들.get(Integer.valueOf(INDIZE));
        if (sarrera_balio == null) {
            return -9;
        }
        sarrera_balio.실행시닫기 = balio;
        return 0;
    }

    public int 실행시닫기값(int INDIZE) {
        서술자 sarrera_balio = 서술자들.get(Integer.valueOf(INDIZE));
        if (sarrera_balio == null) {
            return -9;
        }
        return sarrera_balio.실행시닫기 ? 1 : 0;
    }

    public fitxategi_info msinfo32_exe(int INDIZE) {
        if (INDIZE >= 0 && INDIZE <= 2) {
            return new fitxategi_info(0, 0020666);
        }
        서술자 sarrera_balio = 서술자들.get(Integer.valueOf(INDIZE));
        if (sarrera_balio == null) {
            return null;
        }
        return new fitxategi_info(sarrera_balio.열린파일.datuak.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDIZE : 번호들) {
            서술자 sarrera_balio = 서술자들.get(INDIZE);
            if (sarrera_balio != null && sarrera_balio.실행시닫기) {
                Itxi(INDIZE.intValue());
            }
        }
    }

    public boolean informatika_ireki(int INDIZE) {
        return 서술자들.containsKey(Integer.valueOf(INDIZE));
    }

    public 파일서술자표 klon_balio() {
        파일서술자표 EMAITZA = new 파일서술자표(fitxategi_sistema);
        for (Map.Entry<Integer, 서술자> sarrera_balio : 서술자들.entrySet()) {
            sarrera_balio.getValue().열린파일.Erreferentzia_materiala_ZENBATU++;
            서술자 새서술자 = new 서술자(sarrera_balio.getValue().열린파일);
            새서술자.실행시닫기 = sarrera_balio.getValue().실행시닫기;
            EMAITZA.서술자들.put(sarrera_balio.getKey(), 새서술자);
        }
        return EMAITZA;
    }

    private int 빈번호(int 최소번호) {
        for (int INDIZE = Math.max(0, 최소번호); INDIZE < 최대서술자; INDIZE++) {
            if (!서술자들.containsKey(Integer.valueOf(INDIZE))) {
                return INDIZE;
            }
        }
        return -1;
    }
}
