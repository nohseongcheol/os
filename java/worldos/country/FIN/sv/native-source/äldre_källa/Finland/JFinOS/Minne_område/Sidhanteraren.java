// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finland.JFinOS.Minne_område;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB page_värde 연결과 Skriv 시 복사를 제공한다. */
public final class Sidhanteraren {
    public static final int sidstorlek = 4096;

    private static final class page_värde {
        private byte[] data = new byte[sidstorlek];
        private int referens_ANTAL = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adressutrymme {
        private final Map<Integer, page_värde> page_tabell = new HashMap<Integer, page_värde>();
    }

    public adressutrymme 새주소공간() {
        return new adressutrymme();
    }

    public void MAP_page(adressutrymme ADRESS_område, int virtuell_adress, boolean 쓰기가능) {
        int INDEX = page_nummer(virtuell_adress);
        page_värde 새쪽 = new page_värde();
        새쪽.쓰기가능 = 쓰기가능;
        ADRESS_område.page_tabell.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adressutrymme 쓰기시복사복제(adressutrymme 원본) {
        adressutrymme 복제본 = new adressutrymme();
        for (Map.Entry<Integer, page_värde> post_värde : 원본.page_tabell.entrySet()) {
            page_värde Delad_page = post_värde.getValue();
            Delad_page.referens_ANTAL++;
            if (Delad_page.쓰기가능) {
                Delad_page.쓰기가능 = false;
                Delad_page.쓰기시복사 = true;
            }
            복제본.page_tabell.put(post_värde.getKey(), Delad_page);
        }
        return 복제본;
    }

    public byte läsa_byte_värde(adressutrymme ADRESS_område, int virtuell_adress) {
        page_värde mål = Sök_page(ADRESS_område, virtuell_adress);
        return mål.data[Math.floorMod(virtuell_adress, sidstorlek)];
    }

    public void skriva_byte_värde(adressutrymme ADRESS_område, int virtuell_adress, byte värde) {
        int INDEX = page_nummer(virtuell_adress);
        page_värde mål = Sök_page(ADRESS_område, virtuell_adress);
        if (!mål.쓰기가능) {
            if (!mål.쓰기시복사) {
                throw new IllegalStateException("Läs 전용 쪽입니다.");
            }
            mål = Skapa_Privat_page(ADRESS_område, INDEX, mål);
        }
        mål.data[Math.floorMod(virtuell_adress, sidstorlek)] = värde;
    }

    public void Privat_område_skriva(adressutrymme ADRESS_område, int START_ADRESS, int Storlek) {
        if (Storlek < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int avsluta_ADRESS = Math.addExact(START_ADRESS, Storlek);
        for (int Adress = START_ADRESS; Adress < avsluta_ADRESS; Adress = (page_nummer(Adress) + 1) * sidstorlek) {
            int INDEX = page_nummer(Adress);
            page_värde mål = Sök_page(ADRESS_område, Adress);
            if (mål.쓰기시복사) {
                Skapa_Privat_page(ADRESS_område, INDEX, mål);
            } else {
                mål.쓰기가능 = true;
            }
        }
    }

    public void område_skriva(adressutrymme ADRESS_område, int START_ADRESS, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            skriva_byte_värde(ADRESS_område, START_ADRESS + INDEX, data[INDEX]);
        }
    }

    private page_värde Skapa_Privat_page(adressutrymme ADRESS_område, int INDEX, page_värde Delad_page) {
        page_värde Privat_page = new page_värde();
        Privat_page.data = Arrays.copyOf(Delad_page.data, Delad_page.data.length);
        Privat_page.쓰기가능 = true;
        Privat_page.쓰기시복사 = false;
        Delad_page.referens_ANTAL--;
        ADRESS_område.page_tabell.put(Integer.valueOf(INDEX), Privat_page);
        return Privat_page;
    }

    private page_värde Sök_page(adressutrymme ADRESS_område, int Adress) {
        page_värde mål = ADRESS_område.page_tabell.get(Integer.valueOf(page_nummer(Adress)));
        if (mål == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return mål;
    }

    private int page_nummer(int Adress) {
        if (Adress < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return Adress / sidstorlek;
    }
}

