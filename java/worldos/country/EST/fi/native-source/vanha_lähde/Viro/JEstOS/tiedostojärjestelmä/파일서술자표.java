// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Viro.JEstOS.tiedostojärjestelmä;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 tiedoston_nimi 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final tiedostojärjestelmä.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(tiedostojärjestelmä.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final tiedostojärjestelmä tiedostojärjestelmä;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(tiedostojärjestelmä tiedostojärjestelmä) {
        this.tiedostojärjestelmä = tiedostojärjestelmä;
    }

    public int Avaa(String Nimi) {
        tiedostojärjestelmä.열린파일 열린파일 = tiedostojärjestelmä.Avaa(Nimi);
        if (열린파일 == null) {
            return -2;
        }
        int INDEKSI = 빈번호(3);
        if (INDEKSI < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEKSI), new 서술자(열린파일));
        return INDEKSI;
    }

    public int Luku(int INDEKSI, byte[] saada_kohde, int Koko) {
        서술자 merkintä_ARVO_962f286b = 서술자들.get(Integer.valueOf(INDEKSI));
        if (merkintä_ARVO_962f286b == null) {
            return -9;
        }
        if (Koko < 0 || Koko > saada_kohde.length) {
            return -22;
        }
        int 남음 = merkintä_ARVO_962f286b.열린파일.data.length - merkintä_ARVO_962f286b.열린파일.paikka;
        int lukea_muuttaa_kokoa = Math.min(Koko, Math.max(남음, 0));
        System.arraycopy(merkintä_ARVO_962f286b.열린파일.data, merkintä_ARVO_962f286b.열린파일.paikka, saada_kohde, 0, lukea_muuttaa_kokoa);
        merkintä_ARVO_962f286b.열린파일.paikka += lukea_muuttaa_kokoa;
        return lukea_muuttaa_kokoa;
    }

    public int siirrä_toimi(int INDEKSI, int 거리, int aloite_juuri) {
        서술자 merkintä_ARVO_962f286b = 서술자들.get(Integer.valueOf(INDEKSI));
        if (merkintä_ARVO_962f286b == null) {
            return -9;
        }
        int Tausta_ARVO;
        if (aloite_juuri == 0) {
            Tausta_ARVO = 0;
        } else if (aloite_juuri == 1) {
            Tausta_ARVO = merkintä_ARVO_962f286b.열린파일.paikka;
        } else if (aloite_juuri == 2) {
            Tausta_ARVO = merkintä_ARVO_962f286b.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = Tausta_ARVO + 거리;
        if (새위치 < 0) {
            return -22;
        }
        merkintä_ARVO_962f286b.열린파일.paikka = 새위치;
        return 새위치;
    }

    public int Sulje(int INDEKSI) {
        서술자 merkintä_ARVO_962f286b = 서술자들.remove(Integer.valueOf(INDEKSI));
        if (merkintä_ARVO_962f286b == null) {
            return -9;
        }
        merkintä_ARVO_962f286b.열린파일.viite_LASKE--;
        return 0;
    }

    public int 복제서술자(int INDEKSI, int 최소번호) {
        서술자 merkintä_ARVO_962f286b = 서술자들.get(Integer.valueOf(INDEKSI));
        if (merkintä_ARVO_962f286b == null) {
            return -9;
        }
        int Uusi_numero = 빈번호(최소번호);
        if (Uusi_numero < 0) {
            return -24;
        }
        merkintä_ARVO_962f286b.열린파일.viite_LASKE++;
        서술자들.put(Integer.valueOf(Uusi_numero), new 서술자(merkintä_ARVO_962f286b.열린파일));
        return Uusi_numero;
    }

    public int 지정복제(int INDEKSI, int Uusi_numero) {
        if (INDEKSI == Uusi_numero) {
            return 서술자들.containsKey(Integer.valueOf(INDEKSI)) ? INDEKSI : -9;
        }
        if (Uusi_numero < 0 || Uusi_numero >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEKSI));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Uusi_numero))) {
            Sulje(Uusi_numero);
        }
        원본.열린파일.viite_LASKE++;
        서술자들.put(Integer.valueOf(Uusi_numero), new 서술자(원본.열린파일));
        return Uusi_numero;
    }

    public int 실행시닫기설정(int INDEKSI, boolean ARVO) {
        서술자 merkintä_ARVO_962f286b = 서술자들.get(Integer.valueOf(INDEKSI));
        if (merkintä_ARVO_962f286b == null) {
            return -9;
        }
        merkintä_ARVO_962f286b.실행시닫기 = ARVO;
        return 0;
    }

    public int 실행시닫기값(int INDEKSI) {
        서술자 merkintä_ARVO_962f286b = 서술자들.get(Integer.valueOf(INDEKSI));
        if (merkintä_ARVO_962f286b == null) {
            return -9;
        }
        return merkintä_ARVO_962f286b.실행시닫기 ? 1 : 0;
    }

    public Tiedosto_info msinfo32_exe(int INDEKSI) {
        if (INDEKSI >= 0 && INDEKSI <= 2) {
            return new Tiedosto_info(0, 0020666);
        }
        서술자 merkintä_ARVO_962f286b = 서술자들.get(Integer.valueOf(INDEKSI));
        if (merkintä_ARVO_962f286b == null) {
            return null;
        }
        return new Tiedosto_info(merkintä_ARVO_962f286b.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] numero_luettelo = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEKSI : numero_luettelo) {
            서술자 merkintä_ARVO_962f286b = 서술자들.get(INDEKSI);
            if (merkintä_ARVO_962f286b != null && merkintä_ARVO_962f286b.실행시닫기) {
                Sulje(INDEKSI.intValue());
            }
        }
    }

    public boolean tietojärjestelmät_avata(int INDEKSI) {
        return 서술자들.containsKey(Integer.valueOf(INDEKSI));
    }

    public 파일서술자표 klooni_ARVO() {
        파일서술자표 TULOS = new 파일서술자표(tiedostojärjestelmä);
        for (Map.Entry<Integer, 서술자> merkintä_ARVO_962f286b : 서술자들.entrySet()) {
            merkintä_ARVO_962f286b.getValue().열린파일.viite_LASKE++;
            서술자 새서술자 = new 서술자(merkintä_ARVO_962f286b.getValue().열린파일);
            새서술자.실행시닫기 = merkintä_ARVO_962f286b.getValue().실행시닫기;
            TULOS.서술자들.put(merkintä_ARVO_962f286b.getKey(), 새서술자);
        }
        return TULOS;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEKSI = Math.max(0, 최소번호); INDEKSI < 최대서술자; INDEKSI++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEKSI))) {
                return INDEKSI;
            }
        }
        return -1;
    }
}
