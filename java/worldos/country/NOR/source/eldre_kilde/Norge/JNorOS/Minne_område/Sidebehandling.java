// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.Minne_område;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB page_VERDI 연결과 Skriv 시 복사를 제공한다. */
public final class Sidebehandling {
    public static final int sidestørrelse = 4096;

    private static final class page_VERDI {
        private byte[] data = new byte[sidestørrelse];
        private int referere_ANTALL = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresseområde {
        private final Map<Integer, page_VERDI> page_tabell = new HashMap<Integer, page_VERDI>();
    }

    public adresseområde 새주소공간() {
        return new adresseområde();
    }

    public void kart_page(adresseområde e_post_område, int virtuell_adresse, boolean 쓰기가능) {
        int INDEKS = page_nummer(virtuell_adresse);
        page_VERDI 새쪽 = new page_VERDI();
        새쪽.쓰기가능 = 쓰기가능;
        e_post_område.page_tabell.put(Integer.valueOf(INDEKS), 새쪽);
    }

    public adresseområde 쓰기시복사복제(adresseområde 원본) {
        adresseområde 복제본 = new adresseområde();
        for (Map.Entry<Integer, page_VERDI> oppføring_VERDI : 원본.page_tabell.entrySet()) {
            page_VERDI 공유쪽 = oppføring_VERDI.getValue();
            공유쪽.referere_ANTALL++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.page_tabell.put(oppføring_VERDI.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresseområde e_post_område, int virtuell_adresse) {
        page_VERDI mål = Søk_page(e_post_område, virtuell_adresse);
        return mål.data[Math.floorMod(virtuell_adresse, sidestørrelse)];
    }

    public void skrive_byte_VERDI(adresseområde e_post_område, int virtuell_adresse, byte VERDI) {
        int INDEKS = page_nummer(virtuell_adresse);
        page_VERDI mål = Søk_page(e_post_område, virtuell_adresse);
        if (!mål.쓰기가능) {
            if (!mål.쓰기시복사) {
                throw new IllegalStateException("Les 전용 쪽입니다.");
            }
            mål = åpne_privat_page(e_post_område, INDEKS, mål);
        }
        mål.data[Math.floorMod(virtuell_adresse, sidestørrelse)] = VERDI;
    }

    public void privat_område_skrive(adresseområde e_post_område, int START_e_post, int Størrelse) {
        if (Størrelse < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int avslutte_en_samtale_e_post = Math.addExact(START_e_post, Størrelse);
        for (int e_post = START_e_post; e_post < avslutte_en_samtale_e_post; e_post = (page_nummer(e_post) + 1) * sidestørrelse) {
            int INDEKS = page_nummer(e_post);
            page_VERDI mål = Søk_page(e_post_område, e_post);
            if (mål.쓰기시복사) {
                åpne_privat_page(e_post_område, INDEKS, mål);
            } else {
                mål.쓰기가능 = true;
            }
        }
    }

    public void område_skrive(adresseområde e_post_område, int START_e_post, byte[] data) {
        for (int INDEKS = 0; INDEKS < data.length; INDEKS++) {
            skrive_byte_VERDI(e_post_område, START_e_post + INDEKS, data[INDEKS]);
        }
    }

    private page_VERDI åpne_privat_page(adresseområde e_post_område, int INDEKS, page_VERDI 공유쪽) {
        page_VERDI privat_page = new page_VERDI();
        privat_page.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        privat_page.쓰기가능 = true;
        privat_page.쓰기시복사 = false;
        공유쪽.referere_ANTALL--;
        e_post_område.page_tabell.put(Integer.valueOf(INDEKS), privat_page);
        return privat_page;
    }

    private page_VERDI Søk_page(adresseområde e_post_område, int e_post) {
        page_VERDI mål = e_post_område.page_tabell.get(Integer.valueOf(page_nummer(e_post)));
        if (mål == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return mål;
    }

    private int page_nummer(int e_post) {
        if (e_post < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return e_post / sidestørrelse;
    }
}

