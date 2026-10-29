// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Słowacja.JSvkOS.system_plików;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 nazwa_pliku 설명을 유지한다. */
public final class Plik_deskryptor_tabela {
    private static final int 최대서술자 = 32;

    private static final class deskryptor_wpis {
        private final system_plików.열린파일 열린파일;
        private boolean 실행시닫기;

        deskryptor_wpis(system_plików.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final system_plików system_plików;
    private final Map<Integer, deskryptor_wpis> 서술자들 = new HashMap<Integer, deskryptor_wpis>();

    public Plik_deskryptor_tabela(system_plików system_plików) {
        this.system_plików = system_plików;
    }

    public int Otwórz(String Nazwa) {
        system_plików.열린파일 열린파일 = system_plików.Otwórz(Nazwa);
        if (열린파일 == null) {
            return -2;
        }
        int INDEKS = 빈번호(3);
        if (INDEKS < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEKS), new deskryptor_wpis(열린파일));
        return INDEKS;
    }

    public int Odczyt(int INDEKS, byte[] odbierać_cel, int Rozmiar) {
        deskryptor_wpis wpis_WARTOŚĆ = 서술자들.get(Integer.valueOf(INDEKS));
        if (wpis_WARTOŚĆ == null) {
            return -9;
        }
        if (Rozmiar < 0 || Rozmiar > odbierać_cel.length) {
            return -22;
        }
        int 남음 = wpis_WARTOŚĆ.열린파일.dane.length - wpis_WARTOŚĆ.열린파일.pozycja;
        int 읽을크기 = Math.min(Rozmiar, Math.max(남음, 0));
        System.arraycopy(wpis_WARTOŚĆ.열린파일.dane, wpis_WARTOŚĆ.열린파일.pozycja, odbierać_cel, 0, 읽을크기);
        wpis_WARTOŚĆ.열린파일.pozycja += 읽을크기;
        return 읽을크기;
    }

    public int przenosić_stanowisko(int INDEKS, int 거리, int Project_korzeń) {
        deskryptor_wpis wpis_WARTOŚĆ = 서술자들.get(Integer.valueOf(INDEKS));
        if (wpis_WARTOŚĆ == null) {
            return -9;
        }
        int Tło_WARTOŚĆ;
        if (Project_korzeń == 0) {
            Tło_WARTOŚĆ = 0;
        } else if (Project_korzeń == 1) {
            Tło_WARTOŚĆ = wpis_WARTOŚĆ.열린파일.pozycja;
        } else if (Project_korzeń == 2) {
            Tło_WARTOŚĆ = wpis_WARTOŚĆ.열린파일.dane.length;
        } else {
            return -22;
        }
        int 새위치 = Tło_WARTOŚĆ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        wpis_WARTOŚĆ.열린파일.pozycja = 새위치;
        return 새위치;
    }

    public int Zamknięte(int INDEKS) {
        deskryptor_wpis wpis_WARTOŚĆ = 서술자들.remove(Integer.valueOf(INDEKS));
        if (wpis_WARTOŚĆ == null) {
            return -9;
        }
        wpis_WARTOŚĆ.열린파일.odwołanie_ILE_LICZB--;
        return 0;
    }

    public int 복제서술자(int INDEKS, int 최소번호) {
        deskryptor_wpis wpis_WARTOŚĆ = 서술자들.get(Integer.valueOf(INDEKS));
        if (wpis_WARTOŚĆ == null) {
            return -9;
        }
        int Nowy_numer = 빈번호(최소번호);
        if (Nowy_numer < 0) {
            return -24;
        }
        wpis_WARTOŚĆ.열린파일.odwołanie_ILE_LICZB++;
        서술자들.put(Integer.valueOf(Nowy_numer), new deskryptor_wpis(wpis_WARTOŚĆ.열린파일));
        return Nowy_numer;
    }

    public int 지정복제(int INDEKS, int Nowy_numer) {
        if (INDEKS == Nowy_numer) {
            return 서술자들.containsKey(Integer.valueOf(INDEKS)) ? INDEKS : -9;
        }
        if (Nowy_numer < 0 || Nowy_numer >= 최대서술자) {
            return -9;
        }
        deskryptor_wpis 원본 = 서술자들.get(Integer.valueOf(INDEKS));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nowy_numer))) {
            Zamknięte(Nowy_numer);
        }
        원본.열린파일.odwołanie_ILE_LICZB++;
        서술자들.put(Integer.valueOf(Nowy_numer), new deskryptor_wpis(원본.열린파일));
        return Nowy_numer;
    }

    public int 실행시닫기설정(int INDEKS, boolean WARTOŚĆ) {
        deskryptor_wpis wpis_WARTOŚĆ = 서술자들.get(Integer.valueOf(INDEKS));
        if (wpis_WARTOŚĆ == null) {
            return -9;
        }
        wpis_WARTOŚĆ.실행시닫기 = WARTOŚĆ;
        return 0;
    }

    public int 실행시닫기값(int INDEKS) {
        deskryptor_wpis wpis_WARTOŚĆ = 서술자들.get(Integer.valueOf(INDEKS));
        if (wpis_WARTOŚĆ == null) {
            return -9;
        }
        return wpis_WARTOŚĆ.실행시닫기 ? 1 : 0;
    }

    public Plik_informacje msinfo32_exe(int INDEKS) {
        if (INDEKS >= 0 && INDEKS <= 2) {
            return new Plik_informacje(0, 0020666);
        }
        deskryptor_wpis wpis_WARTOŚĆ = 서술자들.get(Integer.valueOf(INDEKS));
        if (wpis_WARTOŚĆ == null) {
            return null;
        }
        return new Plik_informacje(wpis_WARTOŚĆ.열린파일.dane.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] identyfikator_Lista = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEKS : identyfikator_Lista) {
            deskryptor_wpis wpis_WARTOŚĆ = 서술자들.get(INDEKS);
            if (wpis_WARTOŚĆ != null && wpis_WARTOŚĆ.실행시닫기) {
                Zamknięte(INDEKS.intValue());
            }
        }
    }

    public boolean systemy_informacyjne_otwarty(int INDEKS) {
        return 서술자들.containsKey(Integer.valueOf(INDEKS));
    }

    public Plik_deskryptor_tabela klon_WARTOŚĆ() {
        Plik_deskryptor_tabela WYNIK = new Plik_deskryptor_tabela(system_plików);
        for (Map.Entry<Integer, deskryptor_wpis> wpis_WARTOŚĆ : 서술자들.entrySet()) {
            wpis_WARTOŚĆ.getValue().열린파일.odwołanie_ILE_LICZB++;
            deskryptor_wpis 새서술자 = new deskryptor_wpis(wpis_WARTOŚĆ.getValue().열린파일);
            새서술자.실행시닫기 = wpis_WARTOŚĆ.getValue().실행시닫기;
            WYNIK.서술자들.put(wpis_WARTOŚĆ.getKey(), 새서술자);
        }
        return WYNIK;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEKS = Math.max(0, 최소번호); INDEKS < 최대서술자; INDEKS++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEKS))) {
                return INDEKS;
            }
        }
        return -1;
    }
}
