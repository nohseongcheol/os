// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.Geheugen_regio;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB page_WAARDE 연결과 Schrijven 시 복사를 제공한다. */
public final class Paginabeheer {
    public static final int paginaformaat = 4096;

    private static final class page_WAARDE {
        private byte[] gegevens = new byte[paginaformaat];
        private int verwijzen_AANTAL = 1;
        private boolean 쓰기가능 = true;
        private boolean kopiëren_bij_schrijven;
    }

    public static final class adresruimte {
        private final Map<Integer, page_WAARDE> page_tabel = new HashMap<Integer, page_WAARDE>();
    }

    public adresruimte 새주소공간() {
        return new adresruimte();
    }

    public void MAP_page(adresruimte ADRES_regio, int virtueel_adres, boolean 쓰기가능) {
        int INDEX = page_nummer(virtueel_adres);
        page_WAARDE 새쪽 = new page_WAARDE();
        새쪽.쓰기가능 = 쓰기가능;
        ADRES_regio.page_tabel.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adresruimte kloon_kopiëren_bij_schrijven(adresruimte 원본) {
        adresruimte 복제본 = new adresruimte();
        for (Map.Entry<Integer, page_WAARDE> invoer_WAARDE_962f286b : 원본.page_tabel.entrySet()) {
            page_WAARDE Gedeeld_page = invoer_WAARDE_962f286b.getValue();
            Gedeeld_page.verwijzen_AANTAL++;
            if (Gedeeld_page.쓰기가능) {
                Gedeeld_page.쓰기가능 = false;
                Gedeeld_page.kopiëren_bij_schrijven = true;
            }
            복제본.page_tabel.put(invoer_WAARDE_962f286b.getKey(), Gedeeld_page);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresruimte ADRES_regio, int virtueel_adres) {
        page_WAARDE doel = Zoeken_page(ADRES_regio, virtueel_adres);
        return doel.gegevens[Math.floorMod(virtueel_adres, paginaformaat)];
    }

    public void schrijven_byte_WAARDE(adresruimte ADRES_regio, int virtueel_adres, byte WAARDE) {
        int INDEX = page_nummer(virtueel_adres);
        page_WAARDE doel = Zoeken_page(ADRES_regio, virtueel_adres);
        if (!doel.쓰기가능) {
            if (!doel.kopiëren_bij_schrijven) {
                throw new IllegalStateException("Lezen 전용 쪽입니다.");
            }
            doel = maken_Privé_page(ADRES_regio, INDEX, doel);
        }
        doel.gegevens[Math.floorMod(virtueel_adres, paginaformaat)] = WAARDE;
    }

    public void Privé_bereik_schrijven(adresruimte ADRES_regio, int START_ADRES, int Grootte) {
        if (Grootte < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int eindadres = Math.addExact(START_ADRES, Grootte);
        for (int ADRES = START_ADRES; ADRES < eindadres; ADRES = (page_nummer(ADRES) + 1) * paginaformaat) {
            int INDEX = page_nummer(ADRES);
            page_WAARDE doel = Zoeken_page(ADRES_regio, ADRES);
            if (doel.kopiëren_bij_schrijven) {
                maken_Privé_page(ADRES_regio, INDEX, doel);
            } else {
                doel.쓰기가능 = true;
            }
        }
    }

    public void bereik_schrijven(adresruimte ADRES_regio, int START_ADRES, byte[] gegevens) {
        for (int INDEX = 0; INDEX < gegevens.length; INDEX++) {
            schrijven_byte_WAARDE(ADRES_regio, START_ADRES + INDEX, gegevens[INDEX]);
        }
    }

    private page_WAARDE maken_Privé_page(adresruimte ADRES_regio, int INDEX, page_WAARDE Gedeeld_page) {
        page_WAARDE Privé_page = new page_WAARDE();
        Privé_page.gegevens = Arrays.copyOf(Gedeeld_page.gegevens, Gedeeld_page.gegevens.length);
        Privé_page.쓰기가능 = true;
        Privé_page.kopiëren_bij_schrijven = false;
        Gedeeld_page.verwijzen_AANTAL--;
        ADRES_regio.page_tabel.put(Integer.valueOf(INDEX), Privé_page);
        return Privé_page;
    }

    private page_WAARDE Zoeken_page(adresruimte ADRES_regio, int ADRES) {
        page_WAARDE doel = ADRES_regio.page_tabel.get(Integer.valueOf(page_nummer(ADRES)));
        if (doel == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return doel;
    }

    private int page_nummer(int ADRES) {
        if (ADRES < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADRES / paginaformaat;
    }
}

