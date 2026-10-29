// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB xët_xëyma 연결과 biir 시 복사를 제공한다. */
public final class xët_doxalkat {
    public static final int dayob_xët = 4096;

    private static final class xët_xëyma {
        private byte[] mbir = new byte[dayob_xët];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class dëkkuwaay_Espace {
        private final Map<Integer, xët_xëyma> xët_àlluwa = new HashMap<Integer, xët_xëyma>();
    }

    public dëkkuwaay_Espace 새주소공간() {
        return new dëkkuwaay_Espace();
    }

    public void fésal_dëkkuwaay_bi_ciw_kart_xët(dëkkuwaay_Espace 공간, int dëkkuwaay_bu_jëmmadi, boolean 쓰기가능) {
        int àlluwa_tur = 쪽번호(dëkkuwaay_bu_jëmmadi);
        xët_xëyma 새쪽 = new xët_xëyma();
        새쪽.쓰기가능 = 쓰기가능;
        공간.xët_àlluwa.put(Integer.valueOf(àlluwa_tur), 새쪽);
    }

    public dëkkuwaay_Espace 쓰기시복사복제(dëkkuwaay_Espace 원본) {
        dëkkuwaay_Espace 복제본 = new dëkkuwaay_Espace();
        for (Map.Entry<Integer, xët_xëyma> dugal_xabaar_xëyma : 원본.xët_àlluwa.entrySet()) {
            xët_xëyma 공유쪽 = dugal_xabaar_xëyma.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.xët_àlluwa.put(dugal_xabaar_xëyma.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(dëkkuwaay_Espace 공간, int dëkkuwaay_bu_jëmmadi) {
        xët_xëyma luñu_name = seet_xët(공간, dëkkuwaay_bu_jëmmadi);
        return luñu_name.mbir[Math.floorMod(dëkkuwaay_bu_jëmmadi, dayob_xët)];
    }

    public void biir_okte_xëyma(dëkkuwaay_Espace 공간, int dëkkuwaay_bu_jëmmadi, byte xëyma) {
        int àlluwa_tur = 쪽번호(dëkkuwaay_bu_jëmmadi);
        xët_xëyma luñu_name = seet_xët(공간, dëkkuwaay_bu_jëmmadi);
        if (!luñu_name.쓰기가능) {
            if (!luñu_name.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            luñu_name = sos_lol_jambur_xët(공간, àlluwa_tur, luñu_name);
        }
        luñu_name.mbir[Math.floorMod(dëkkuwaay_bu_jëmmadi, dayob_xët)] = xëyma;
    }

    public void 범위개인쓰기(dëkkuwaay_Espace 공간, int Door_dëkkuwaay, int tolluwaay) {
        if (tolluwaay < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int jeexal_dëkkuwaay = Math.addExact(Door_dëkkuwaay, tolluwaay);
        for (int dëkkuwaay = Door_dëkkuwaay; dëkkuwaay < jeexal_dëkkuwaay; dëkkuwaay = (쪽번호(dëkkuwaay) + 1) * dayob_xët) {
            int àlluwa_tur = 쪽번호(dëkkuwaay);
            xët_xëyma luñu_name = seet_xët(공간, dëkkuwaay);
            if (luñu_name.쓰기시복사) {
                sos_lol_jambur_xët(공간, àlluwa_tur, luñu_name);
            } else {
                luñu_name.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(dëkkuwaay_Espace 공간, int Door_dëkkuwaay, byte[] mbir) {
        for (int àlluwa_tur = 0; àlluwa_tur < mbir.length; àlluwa_tur++) {
            biir_okte_xëyma(공간, Door_dëkkuwaay + àlluwa_tur, mbir[àlluwa_tur]);
        }
    }

    private xët_xëyma sos_lol_jambur_xët(dëkkuwaay_Espace 공간, int àlluwa_tur, xët_xëyma 공유쪽) {
        xët_xëyma lol_jambur_xët = new xët_xëyma();
        lol_jambur_xët.mbir = Arrays.copyOf(공유쪽.mbir, 공유쪽.mbir.length);
        lol_jambur_xët.쓰기가능 = true;
        lol_jambur_xët.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.xët_àlluwa.put(Integer.valueOf(àlluwa_tur), lol_jambur_xët);
        return lol_jambur_xët;
    }

    private xët_xëyma seet_xët(dëkkuwaay_Espace 공간, int dëkkuwaay) {
        xët_xëyma luñu_name = 공간.xët_àlluwa.get(Integer.valueOf(쪽번호(dëkkuwaay)));
        if (luñu_name == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return luñu_name;
    }

    private int 쪽번호(int dëkkuwaay) {
        if (dëkkuwaay < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return dëkkuwaay / dayob_xët;
    }
}

