// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.Paměť_oblast;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB stránka_HODNOTA 연결과 Zápis 시 복사를 제공한다. */
public final class stránka_Správce {
    public static final int velikost_stránky = 4096;

    private static final class stránka_HODNOTA {
        private byte[] data = new byte[velikost_stránky];
        private int odkaz_POČET = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresní_prostor {
        private final Map<Integer, stránka_HODNOTA> stránka_tabulka = new HashMap<Integer, stránka_HODNOTA>();
    }

    public adresní_prostor 새주소공간() {
        return new adresní_prostor();
    }

    public void MAP_stránka(adresní_prostor ODKAZ_oblast, int virtuální_adresa, boolean 쓰기가능) {
        int INDEX = stránka_číslo(virtuální_adresa);
        stránka_HODNOTA 새쪽 = new stránka_HODNOTA();
        새쪽.쓰기가능 = 쓰기가능;
        ODKAZ_oblast.stránka_tabulka.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adresní_prostor 쓰기시복사복제(adresní_prostor 원본) {
        adresní_prostor 복제본 = new adresní_prostor();
        for (Map.Entry<Integer, stránka_HODNOTA> položka_HODNOTA : 원본.stránka_tabulka.entrySet()) {
            stránka_HODNOTA Shared_stránka = položka_HODNOTA.getValue();
            Shared_stránka.odkaz_POČET++;
            if (Shared_stránka.쓰기가능) {
                Shared_stránka.쓰기가능 = false;
                Shared_stránka.쓰기시복사 = true;
            }
            복제본.stránka_tabulka.put(položka_HODNOTA.getKey(), Shared_stránka);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresní_prostor ODKAZ_oblast, int virtuální_adresa) {
        stránka_HODNOTA cílová_úroveň = NAJÍT_stránka(ODKAZ_oblast, virtuální_adresa);
        return cílová_úroveň.data[Math.floorMod(virtuální_adresa, velikost_stránky)];
    }

    public void zápis_bajt_HODNOTA(adresní_prostor ODKAZ_oblast, int virtuální_adresa, byte HODNOTA) {
        int INDEX = stránka_číslo(virtuální_adresa);
        stránka_HODNOTA cílová_úroveň = NAJÍT_stránka(ODKAZ_oblast, virtuální_adresa);
        if (!cílová_úroveň.쓰기가능) {
            if (!cílová_úroveň.쓰기시복사) {
                throw new IllegalStateException("Čtení 전용 쪽입니다.");
            }
            cílová_úroveň = Create_soukromý_stránka(ODKAZ_oblast, INDEX, cílová_úroveň);
        }
        cílová_úroveň.data[Math.floorMod(virtuální_adresa, velikost_stránky)] = HODNOTA;
    }

    public void soukromý_oblast_zápis(adresní_prostor ODKAZ_oblast, int START_ODKAZ, int Velikost) {
        if (Velikost < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int konec_ODKAZ = Math.addExact(START_ODKAZ, Velikost);
        for (int Adresa = START_ODKAZ; Adresa < konec_ODKAZ; Adresa = (stránka_číslo(Adresa) + 1) * velikost_stránky) {
            int INDEX = stránka_číslo(Adresa);
            stránka_HODNOTA cílová_úroveň = NAJÍT_stránka(ODKAZ_oblast, Adresa);
            if (cílová_úroveň.쓰기시복사) {
                Create_soukromý_stránka(ODKAZ_oblast, INDEX, cílová_úroveň);
            } else {
                cílová_úroveň.쓰기가능 = true;
            }
        }
    }

    public void oblast_zápis(adresní_prostor ODKAZ_oblast, int START_ODKAZ, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            zápis_bajt_HODNOTA(ODKAZ_oblast, START_ODKAZ + INDEX, data[INDEX]);
        }
    }

    private stránka_HODNOTA Create_soukromý_stránka(adresní_prostor ODKAZ_oblast, int INDEX, stránka_HODNOTA Shared_stránka) {
        stránka_HODNOTA soukromý_stránka = new stránka_HODNOTA();
        soukromý_stránka.data = Arrays.copyOf(Shared_stránka.data, Shared_stránka.data.length);
        soukromý_stránka.쓰기가능 = true;
        soukromý_stránka.쓰기시복사 = false;
        Shared_stránka.odkaz_POČET--;
        ODKAZ_oblast.stránka_tabulka.put(Integer.valueOf(INDEX), soukromý_stránka);
        return soukromý_stránka;
    }

    private stránka_HODNOTA NAJÍT_stránka(adresní_prostor ODKAZ_oblast, int Adresa) {
        stránka_HODNOTA cílová_úroveň = ODKAZ_oblast.stránka_tabulka.get(Integer.valueOf(stránka_číslo(Adresa)));
        if (cílová_úroveň == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return cílová_úroveň;
    }

    private int stránka_číslo(int Adresa) {
        if (Adresa < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return Adresa / velikost_stránky;
    }
}

