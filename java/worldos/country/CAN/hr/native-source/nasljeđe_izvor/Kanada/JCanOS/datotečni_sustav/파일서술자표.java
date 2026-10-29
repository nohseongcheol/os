// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.datotečni_sustav;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Datoteka 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final datotečni_sustav.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(datotečni_sustav.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final datotečni_sustav datotečni_sustav;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(datotečni_sustav datotečni_sustav) {
        this.datotečni_sustav = datotečni_sustav;
    }

    public int Otvori(String Ime) {
        datotečni_sustav.열린파일 열린파일 = datotečni_sustav.Otvori(Ime);
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

    public int Čitaj(int INDEX, byte[] primiti_odredište, int Veličina) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        if (Veličina < 0 || Veličina > primiti_odredište.length) {
            return -22;
        }
        int 남음 = unos_VALUE.열린파일.podaci.length - unos_VALUE.열린파일.Položaj;
        int 읽을크기 = Math.min(Veličina, Math.max(남음, 0));
        System.arraycopy(unos_VALUE.열린파일.podaci, unos_VALUE.열린파일.Položaj, primiti_odredište, 0, 읽을크기);
        unos_VALUE.열린파일.Položaj += 읽을크기;
        return 읽을크기;
    }

    public int pomicati_se_položaj(int INDEX, int 거리, int akcija_korijen) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        int podloga_VALUE;
        if (akcija_korijen == 0) {
            podloga_VALUE = 0;
        } else if (akcija_korijen == 1) {
            podloga_VALUE = unos_VALUE.열린파일.Položaj;
        } else if (akcija_korijen == 2) {
            podloga_VALUE = unos_VALUE.열린파일.podaci.length;
        } else {
            return -22;
        }
        int 새위치 = podloga_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        unos_VALUE.열린파일.Položaj = 새위치;
        return 새위치;
    }

    public int Zatvori(int INDEX) {
        서술자 unos_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        unos_VALUE.열린파일.Reference_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        int Novi_broj = 빈번호(최소번호);
        if (Novi_broj < 0) {
            return -24;
        }
        unos_VALUE.열린파일.Reference_COUNT++;
        서술자들.put(Integer.valueOf(Novi_broj), new 서술자(unos_VALUE.열린파일));
        return Novi_broj;
    }

    public int 지정복제(int INDEX, int Novi_broj) {
        if (INDEX == Novi_broj) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Novi_broj < 0 || Novi_broj >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Novi_broj))) {
            Zatvori(Novi_broj);
        }
        원본.열린파일.Reference_COUNT++;
        서술자들.put(Integer.valueOf(Novi_broj), new 서술자(원본.열린파일));
        return Novi_broj;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        unos_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return -9;
        }
        return unos_VALUE.실행시닫기 ? 1 : 0;
    }

    public Datoteka_informacija Podaci_o_sustavu(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Datoteka_informacija(0, 0020666);
        }
        서술자 unos_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (unos_VALUE == null) {
            return null;
        }
        return new Datoteka_informacija(unos_VALUE.열린파일.podaci.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 unos_VALUE = 서술자들.get(INDEX);
            if (unos_VALUE != null && unos_VALUE.실행시닫기) {
                Zatvori(INDEX.intValue());
            }
        }
    }

    public boolean odjel_informacijske_tehnologije_otvoreno(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klon_VALUE() {
        파일서술자표 REZULTAT = new 파일서술자표(datotečni_sustav);
        for (Map.Entry<Integer, 서술자> unos_VALUE : 서술자들.entrySet()) {
            unos_VALUE.getValue().열린파일.Reference_COUNT++;
            서술자 새서술자 = new 서술자(unos_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = unos_VALUE.getValue().실행시닫기;
            REZULTAT.서술자들.put(unos_VALUE.getKey(), 새서술자);
        }
        return REZULTAT;
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
