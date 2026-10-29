// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB letlakala_boleng 연결과 Ngwala 시 복사를 제공한다. */
public final class letlakala_molaodi {
    public static final int bogolo_bja_letlakala = 4096;

    private static final class letlakala_boleng {
        private byte[] data = new byte[bogolo_bja_letlakala];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class atrese_sekgoba {
        private final Map<Integer, letlakala_boleng> letlakala_tafola = new HashMap<Integer, letlakala_boleng>();
    }

    public atrese_sekgoba 새주소공간() {
        return new atrese_sekgoba();
    }

    public void mmepe_letlakala(atrese_sekgoba 공간, int atrese_ya_sethalwa, boolean 쓰기가능) {
        int lokela = 쪽번호(atrese_ya_sethalwa);
        letlakala_boleng 새쪽 = new letlakala_boleng();
        새쪽.쓰기가능 = 쓰기가능;
        공간.letlakala_tafola.put(Integer.valueOf(lokela), 새쪽);
    }

    public atrese_sekgoba 쓰기시복사복제(atrese_sekgoba 원본) {
        atrese_sekgoba 복제본 = new atrese_sekgoba();
        for (Map.Entry<Integer, letlakala_boleng> go_tsenya_tshedimošo_boleng : 원본.letlakala_tafola.entrySet()) {
            letlakala_boleng 공유쪽 = go_tsenya_tshedimošo_boleng.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.letlakala_tafola.put(go_tsenya_tshedimošo_boleng.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(atrese_sekgoba 공간, int atrese_ya_sethalwa) {
        letlakala_boleng nepo = hwetša_letlakala(공간, atrese_ya_sethalwa);
        return nepo.data[Math.floorMod(atrese_ya_sethalwa, bogolo_bja_letlakala)];
    }

    public void ngwala_paete_boleng(atrese_sekgoba 공간, int atrese_ya_sethalwa, byte boleng) {
        int lokela = 쪽번호(atrese_ya_sethalwa);
        letlakala_boleng nepo = hwetša_letlakala(공간, atrese_ya_sethalwa);
        if (!nepo.쓰기가능) {
            if (!nepo.쓰기시복사) {
                throw new IllegalStateException("Bala 전용 쪽입니다.");
            }
            nepo = 개인쪽만들기(공간, lokela, nepo);
        }
        nepo.data[Math.floorMod(atrese_ya_sethalwa, bogolo_bja_letlakala)] = boleng;
    }

    public void 범위개인쓰기(atrese_sekgoba 공간, int Thomišo_atrese, int Bogolo) {
        if (Bogolo < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int fetša_atrese = Math.addExact(Thomišo_atrese, Bogolo);
        for (int atrese = Thomišo_atrese; atrese < fetša_atrese; atrese = (쪽번호(atrese) + 1) * bogolo_bja_letlakala) {
            int lokela = 쪽번호(atrese);
            letlakala_boleng nepo = hwetša_letlakala(공간, atrese);
            if (nepo.쓰기시복사) {
                개인쪽만들기(공간, lokela, nepo);
            } else {
                nepo.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(atrese_sekgoba 공간, int Thomišo_atrese, byte[] data) {
        for (int lokela = 0; lokela < data.length; lokela++) {
            ngwala_paete_boleng(공간, Thomišo_atrese + lokela, data[lokela]);
        }
    }

    private letlakala_boleng 개인쪽만들기(atrese_sekgoba 공간, int lokela, letlakala_boleng 공유쪽) {
        letlakala_boleng ya_phraebete_letlakala = new letlakala_boleng();
        ya_phraebete_letlakala.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        ya_phraebete_letlakala.쓰기가능 = true;
        ya_phraebete_letlakala.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.letlakala_tafola.put(Integer.valueOf(lokela), ya_phraebete_letlakala);
        return ya_phraebete_letlakala;
    }

    private letlakala_boleng hwetša_letlakala(atrese_sekgoba 공간, int atrese) {
        letlakala_boleng nepo = 공간.letlakala_tafola.get(Integer.valueOf(쪽번호(atrese)));
        if (nepo == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return nepo;
    }

    private int 쪽번호(int atrese) {
        if (atrese < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return atrese / bogolo_bja_letlakala;
    }
}

