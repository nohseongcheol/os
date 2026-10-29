// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mal_i_Zi.JMneOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB faqe_VALUE 연결과 Shkrimi 시 복사를 제공한다. */
public final class faqe_menaxher {
    public static final int përmasat_e_faqes = 4096;

    private static final class faqe_VALUE {
        private byte[] të_dhëna = new byte[përmasat_e_faqes];
        private int Referencë_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class email_HAPËSIRË {
        private final Map<Integer, faqe_VALUE> faqe_tabelë = new HashMap<Integer, faqe_VALUE>();
    }

    public email_HAPËSIRË 새주소공간() {
        return new email_HAPËSIRË();
    }

    public void MAP_faqe(email_HAPËSIRË 공간, int adresë_virtuale, boolean 쓰기가능) {
        int INDEX = 쪽번호(adresë_virtuale);
        faqe_VALUE 새쪽 = new faqe_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.faqe_tabelë.put(Integer.valueOf(INDEX), 새쪽);
    }

    public email_HAPËSIRË 쓰기시복사복제(email_HAPËSIRË 원본) {
        email_HAPËSIRË 복제본 = new email_HAPËSIRË();
        for (Map.Entry<Integer, faqe_VALUE> futje_VALUE : 원본.faqe_tabelë.entrySet()) {
            faqe_VALUE 공유쪽 = futje_VALUE.getValue();
            공유쪽.Referencë_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.faqe_tabelë.put(futje_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(email_HAPËSIRË 공간, int adresë_virtuale) {
        faqe_VALUE objektiv = FIND_faqe(공간, adresë_virtuale);
        return objektiv.të_dhëna[Math.floorMod(adresë_virtuale, përmasat_e_faqes)];
    }

    public void shkruaj_bajt_VALUE(email_HAPËSIRË 공간, int adresë_virtuale, byte VALUE) {
        int INDEX = 쪽번호(adresë_virtuale);
        faqe_VALUE objektiv = FIND_faqe(공간, adresë_virtuale);
        if (!objektiv.쓰기가능) {
            if (!objektiv.쓰기시복사) {
                throw new IllegalStateException("Leximi 전용 쪽입니다.");
            }
            objektiv = Krijo_Privat_faqe(공간, INDEX, objektiv);
        }
        objektiv.të_dhëna[Math.floorMod(adresë_virtuale, përmasat_e_faqes)] = VALUE;
    }

    public void 범위개인쓰기(email_HAPËSIRË 공간, int nis_email, int Madhësi) {
        if (Madhësi < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int mbaroj_email = Math.addExact(nis_email, Madhësi);
        for (int email = nis_email; email < mbaroj_email; email = (쪽번호(email) + 1) * përmasat_e_faqes) {
            int INDEX = 쪽번호(email);
            faqe_VALUE objektiv = FIND_faqe(공간, email);
            if (objektiv.쓰기시복사) {
                Krijo_Privat_faqe(공간, INDEX, objektiv);
            } else {
                objektiv.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(email_HAPËSIRË 공간, int nis_email, byte[] të_dhëna) {
        for (int INDEX = 0; INDEX < të_dhëna.length; INDEX++) {
            shkruaj_bajt_VALUE(공간, nis_email + INDEX, të_dhëna[INDEX]);
        }
    }

    private faqe_VALUE Krijo_Privat_faqe(email_HAPËSIRË 공간, int INDEX, faqe_VALUE 공유쪽) {
        faqe_VALUE Privat_faqe = new faqe_VALUE();
        Privat_faqe.të_dhëna = Arrays.copyOf(공유쪽.të_dhëna, 공유쪽.të_dhëna.length);
        Privat_faqe.쓰기가능 = true;
        Privat_faqe.쓰기시복사 = false;
        공유쪽.Referencë_COUNT--;
        공간.faqe_tabelë.put(Integer.valueOf(INDEX), Privat_faqe);
        return Privat_faqe;
    }

    private faqe_VALUE FIND_faqe(email_HAPËSIRË 공간, int email) {
        faqe_VALUE objektiv = 공간.faqe_tabelë.get(Integer.valueOf(쪽번호(email)));
        if (objektiv == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return objektiv;
    }

    private int 쪽번호(int email) {
        if (email < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return email / përmasat_e_faqes;
    }
}

