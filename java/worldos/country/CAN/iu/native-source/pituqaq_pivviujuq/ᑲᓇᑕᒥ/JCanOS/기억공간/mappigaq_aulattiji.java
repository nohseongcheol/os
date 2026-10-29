// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB mappigaq_atuutilik 연결과 titiraq 시 복사를 제공한다. */
public final class mappigaq_aulattiji {
    public static final int mappigap_angininga = 4096;

    private static final class mappigaq_atuutilik {
        private byte[] titiqqat = new byte[mappigap_angininga];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class turaarut_SPACEBAR {
        private final Map<Integer, mappigaq_atuutilik> mappigaq_kipu = new HashMap<Integer, mappigaq_atuutilik>();
    }

    public turaarut_SPACEBAR 새주소공간() {
        return new turaarut_SPACEBAR();
    }

    public void nunannguarurli_mappigaq(turaarut_SPACEBAR 공간, int saqqijaanganngittuq_turaarut, boolean 쓰기가능) {
        int nalunaiqsimavik = 쪽번호(saqqijaanganngittuq_turaarut);
        mappigaq_atuutilik 새쪽 = new mappigaq_atuutilik();
        새쪽.쓰기가능 = 쓰기가능;
        공간.mappigaq_kipu.put(Integer.valueOf(nalunaiqsimavik), 새쪽);
    }

    public turaarut_SPACEBAR 쓰기시복사복제(turaarut_SPACEBAR 원본) {
        turaarut_SPACEBAR 복제본 = new turaarut_SPACEBAR();
        for (Map.Entry<Integer, mappigaq_atuutilik> Iliniku_atuutilik : 원본.mappigaq_kipu.entrySet()) {
            mappigaq_atuutilik 공유쪽 = Iliniku_atuutilik.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.mappigaq_kipu.put(Iliniku_atuutilik.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(turaarut_SPACEBAR 공간, int saqqijaanganngittuq_turaarut) {
        mappigaq_atuutilik turaagaq = nanili_mappigaq(공간, saqqijaanganngittuq_turaarut);
        return turaagaq.titiqqat[Math.floorMod(saqqijaanganngittuq_turaarut, mappigap_angininga)];
    }

    public void titiraq_byte_atuutilik(turaarut_SPACEBAR 공간, int saqqijaanganngittuq_turaarut, byte atuutilik) {
        int nalunaiqsimavik = 쪽번호(saqqijaanganngittuq_turaarut);
        mappigaq_atuutilik turaagaq = nanili_mappigaq(공간, saqqijaanganngittuq_turaarut);
        if (!turaagaq.쓰기가능) {
            if (!turaagaq.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            turaagaq = 개인쪽만들기(공간, nalunaiqsimavik, turaagaq);
        }
        turaagaq.titiqqat[Math.floorMod(saqqijaanganngittuq_turaarut, mappigap_angininga)] = atuutilik;
    }

    public void 범위개인쓰기(turaarut_SPACEBAR 공간, int pigiarli_turaarut, int anininga) {
        if (anininga < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int isulittuq_turaarut = Math.addExact(pigiarli_turaarut, anininga);
        for (int turaarut = pigiarli_turaarut; turaarut < isulittuq_turaarut; turaarut = (쪽번호(turaarut) + 1) * mappigap_angininga) {
            int nalunaiqsimavik = 쪽번호(turaarut);
            mappigaq_atuutilik turaagaq = nanili_mappigaq(공간, turaarut);
            if (turaagaq.쓰기시복사) {
                개인쪽만들기(공간, nalunaiqsimavik, turaagaq);
            } else {
                turaagaq.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(turaarut_SPACEBAR 공간, int pigiarli_turaarut, byte[] titiqqat) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < titiqqat.length; nalunaiqsimavik++) {
            titiraq_byte_atuutilik(공간, pigiarli_turaarut + nalunaiqsimavik, titiqqat[nalunaiqsimavik]);
        }
    }

    private mappigaq_atuutilik 개인쪽만들기(turaarut_SPACEBAR 공간, int nalunaiqsimavik, mappigaq_atuutilik 공유쪽) {
        mappigaq_atuutilik kikkutuinnanuunngittuq_mappigaq = new mappigaq_atuutilik();
        kikkutuinnanuunngittuq_mappigaq.titiqqat = Arrays.copyOf(공유쪽.titiqqat, 공유쪽.titiqqat.length);
        kikkutuinnanuunngittuq_mappigaq.쓰기가능 = true;
        kikkutuinnanuunngittuq_mappigaq.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.mappigaq_kipu.put(Integer.valueOf(nalunaiqsimavik), kikkutuinnanuunngittuq_mappigaq);
        return kikkutuinnanuunngittuq_mappigaq;
    }

    private mappigaq_atuutilik nanili_mappigaq(turaarut_SPACEBAR 공간, int turaarut) {
        mappigaq_atuutilik turaagaq = 공간.mappigaq_kipu.get(Integer.valueOf(쪽번호(turaarut)));
        if (turaagaq == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return turaagaq;
    }

    private int 쪽번호(int turaarut) {
        if (turaarut < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return turaarut / mappigap_angininga;
    }
}

