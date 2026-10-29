// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aruba.JAbwOS.bestandssysteem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 bestand 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final bestandssysteem.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(bestandssysteem.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final bestandssysteem bestandssysteem;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(bestandssysteem bestandssysteem) {
        this.bestandssysteem = bestandssysteem;
    }

    public int Openen(String Naam) {
        bestandssysteem.열린파일 열린파일 = bestandssysteem.Openen(Naam);
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

    public int Lezen(int INDEX, byte[] ontvangen_doel, int Grootte) {
        서술자 invoer_WAARDE_962f286b = 서술자들.get(Integer.valueOf(INDEX));
        if (invoer_WAARDE_962f286b == null) {
            return -9;
        }
        if (Grootte < 0 || Grootte > ontvangen_doel.length) {
            return -22;
        }
        int 남음 = invoer_WAARDE_962f286b.열린파일.gegevens.length - invoer_WAARDE_962f286b.열린파일.positie;
        int 읽을크기 = Math.min(Grootte, Math.max(남음, 0));
        System.arraycopy(invoer_WAARDE_962f286b.열린파일.gegevens, invoer_WAARDE_962f286b.열린파일.positie, ontvangen_doel, 0, 읽을크기);
        invoer_WAARDE_962f286b.열린파일.positie += 읽을크기;
        return 읽을크기;
    }

    public int verplaatsen_functie(int INDEX, int 거리, int Taken_wortel) {
        서술자 invoer_WAARDE_962f286b = 서술자들.get(Integer.valueOf(INDEX));
        if (invoer_WAARDE_962f286b == null) {
            return -9;
        }
        int Achtergrond_WAARDE;
        if (Taken_wortel == 0) {
            Achtergrond_WAARDE = 0;
        } else if (Taken_wortel == 1) {
            Achtergrond_WAARDE = invoer_WAARDE_962f286b.열린파일.positie;
        } else if (Taken_wortel == 2) {
            Achtergrond_WAARDE = invoer_WAARDE_962f286b.열린파일.gegevens.length;
        } else {
            return -22;
        }
        int 새위치 = Achtergrond_WAARDE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        invoer_WAARDE_962f286b.열린파일.positie = 새위치;
        return 새위치;
    }

    public int Sluiten(int INDEX) {
        서술자 invoer_WAARDE_962f286b = 서술자들.remove(Integer.valueOf(INDEX));
        if (invoer_WAARDE_962f286b == null) {
            return -9;
        }
        invoer_WAARDE_962f286b.열린파일.verwijzen_AANTAL--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 invoer_WAARDE_962f286b = 서술자들.get(Integer.valueOf(INDEX));
        if (invoer_WAARDE_962f286b == null) {
            return -9;
        }
        int Nieuw_nummer = leeg_INDEX(최소번호);
        if (Nieuw_nummer < 0) {
            return -24;
        }
        invoer_WAARDE_962f286b.열린파일.verwijzen_AANTAL++;
        서술자들.put(Integer.valueOf(Nieuw_nummer), new 서술자(invoer_WAARDE_962f286b.열린파일));
        return Nieuw_nummer;
    }

    public int 지정복제(int INDEX, int Nieuw_nummer) {
        if (INDEX == Nieuw_nummer) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Nieuw_nummer < 0 || Nieuw_nummer >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nieuw_nummer))) {
            Sluiten(Nieuw_nummer);
        }
        원본.열린파일.verwijzen_AANTAL++;
        서술자들.put(Integer.valueOf(Nieuw_nummer), new 서술자(원본.열린파일));
        return Nieuw_nummer;
    }

    public int 실행시닫기설정(int INDEX, boolean WAARDE) {
        서술자 invoer_WAARDE_962f286b = 서술자들.get(Integer.valueOf(INDEX));
        if (invoer_WAARDE_962f286b == null) {
            return -9;
        }
        invoer_WAARDE_962f286b.실행시닫기 = WAARDE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 invoer_WAARDE_962f286b = 서술자들.get(Integer.valueOf(INDEX));
        if (invoer_WAARDE_962f286b == null) {
            return -9;
        }
        return invoer_WAARDE_962f286b.실행시닫기 ? 1 : 0;
    }

    public Bestand_info msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Bestand_info(0, 0020666);
        }
        서술자 invoer_WAARDE_962f286b = 서술자들.get(Integer.valueOf(INDEX));
        if (invoer_WAARDE_962f286b == null) {
            return null;
        }
        return new Bestand_info(invoer_WAARDE_962f286b.열린파일.gegevens.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] nummer_Lijst = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : nummer_Lijst) {
            서술자 invoer_WAARDE_962f286b = 서술자들.get(INDEX);
            if (invoer_WAARDE_962f286b != null && invoer_WAARDE_962f286b.실행시닫기) {
                Sluiten(INDEX.intValue());
            }
        }
    }

    public boolean informatie_open(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 kloon_WAARDE() {
        파일서술자표 resultaat = new 파일서술자표(bestandssysteem);
        for (Map.Entry<Integer, 서술자> invoer_WAARDE_962f286b : 서술자들.entrySet()) {
            invoer_WAARDE_962f286b.getValue().열린파일.verwijzen_AANTAL++;
            서술자 새서술자 = new 서술자(invoer_WAARDE_962f286b.getValue().열린파일);
            새서술자.실행시닫기 = invoer_WAARDE_962f286b.getValue().실행시닫기;
            resultaat.서술자들.put(invoer_WAARDE_962f286b.getKey(), 새서술자);
        }
        return resultaat;
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
