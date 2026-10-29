// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.Hukommelse_område;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB side_VÆRDI 연결과 Skrive 시 복사를 제공한다. */
public final class Sidestyring {
    public static final int sidestørrelse = 4096;

    private static final class side_VÆRDI {
        private byte[] data = new byte[sidestørrelse];
        private int referere_TÆL = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresseinterval {
        private final Map<Integer, side_VÆRDI> side_tabel = new HashMap<Integer, side_VÆRDI>();
    }

    public adresseinterval 새주소공간() {
        return new adresseinterval();
    }

    public void MAP_side(adresseinterval mail_område, int virtuel_adresse, boolean 쓰기가능) {
        int INDEKS = side_tal(virtuel_adresse);
        side_VÆRDI 새쪽 = new side_VÆRDI();
        새쪽.쓰기가능 = 쓰기가능;
        mail_område.side_tabel.put(Integer.valueOf(INDEKS), 새쪽);
    }

    public adresseinterval 쓰기시복사복제(adresseinterval 원본) {
        adresseinterval 복제본 = new adresseinterval();
        for (Map.Entry<Integer, side_VÆRDI> post_VÆRDI_962f286b : 원본.side_tabel.entrySet()) {
            side_VÆRDI 공유쪽 = post_VÆRDI_962f286b.getValue();
            공유쪽.referere_TÆL++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.side_tabel.put(post_VÆRDI_962f286b.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresseinterval mail_område, int virtuel_adresse) {
        side_VÆRDI mål = Søg_side(mail_område, virtuel_adresse);
        return mål.data[Math.floorMod(virtuel_adresse, sidestørrelse)];
    }

    public void skrive_byte_VÆRDI(adresseinterval mail_område, int virtuel_adresse, byte VÆRDI) {
        int INDEKS = side_tal(virtuel_adresse);
        side_VÆRDI mål = Søg_side(mail_område, virtuel_adresse);
        if (!mål.쓰기가능) {
            if (!mål.쓰기시복사) {
                throw new IllegalStateException("Læse 전용 쪽입니다.");
            }
            mål = åbne_privat_side(mail_område, INDEKS, mål);
        }
        mål.data[Math.floorMod(virtuel_adresse, sidestørrelse)] = VÆRDI;
    }

    public void privat_område_skrive(adresseinterval mail_område, int START_mail, int Størrelse) {
        if (Størrelse < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int afslutte_et_opkald_mail = Math.addExact(START_mail, Størrelse);
        for (int mail = START_mail; mail < afslutte_et_opkald_mail; mail = (side_tal(mail) + 1) * sidestørrelse) {
            int INDEKS = side_tal(mail);
            side_VÆRDI mål = Søg_side(mail_område, mail);
            if (mål.쓰기시복사) {
                åbne_privat_side(mail_område, INDEKS, mål);
            } else {
                mål.쓰기가능 = true;
            }
        }
    }

    public void område_skrive(adresseinterval mail_område, int START_mail, byte[] data) {
        for (int INDEKS = 0; INDEKS < data.length; INDEKS++) {
            skrive_byte_VÆRDI(mail_område, START_mail + INDEKS, data[INDEKS]);
        }
    }

    private side_VÆRDI åbne_privat_side(adresseinterval mail_område, int INDEKS, side_VÆRDI 공유쪽) {
        side_VÆRDI privat_side = new side_VÆRDI();
        privat_side.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        privat_side.쓰기가능 = true;
        privat_side.쓰기시복사 = false;
        공유쪽.referere_TÆL--;
        mail_område.side_tabel.put(Integer.valueOf(INDEKS), privat_side);
        return privat_side;
    }

    private side_VÆRDI Søg_side(adresseinterval mail_område, int mail) {
        side_VÆRDI mål = mail_område.side_tabel.get(Integer.valueOf(side_tal(mail)));
        if (mål == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return mål;
    }

    private int side_tal(int mail) {
        if (mail < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return mail / sidestørrelse;
    }
}

