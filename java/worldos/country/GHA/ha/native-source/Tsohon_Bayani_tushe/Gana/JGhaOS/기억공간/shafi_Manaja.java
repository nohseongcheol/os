// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gana.JGhaOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB shafi_Daraja 연결과 Yi_Rubutu 시 복사를 제공한다. */
public final class shafi_Manaja {
    public static final int Girman_shafi = 4096;

    private static final class shafi_Daraja {
        private byte[] Tarin_bayani = new byte[Girman_shafi];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class imel_wuri {
        private final Map<Integer, shafi_Daraja> shafi_tebur = new HashMap<Integer, shafi_Daraja>();
    }

    public imel_wuri 새주소공간() {
        return new imel_wuri();
    }

    public void taswira_shafi(imel_wuri 공간, int Adireshi_mai_rumfa, boolean 쓰기가능) {
        int Indes = 쪽번호(Adireshi_mai_rumfa);
        shafi_Daraja 새쪽 = new shafi_Daraja();
        새쪽.쓰기가능 = 쓰기가능;
        공간.shafi_tebur.put(Integer.valueOf(Indes), 새쪽);
    }

    public imel_wuri 쓰기시복사복제(imel_wuri 원본) {
        imel_wuri 복제본 = new imel_wuri();
        for (Map.Entry<Integer, shafi_Daraja> Mashigar_bayanai_Daraja : 원본.shafi_tebur.entrySet()) {
            shafi_Daraja 공유쪽 = Mashigar_bayanai_Daraja.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.shafi_tebur.put(Mashigar_bayanai_Daraja.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(imel_wuri 공간, int Adireshi_mai_rumfa) {
        shafi_Daraja tageti = nema_shafi(공간, Adireshi_mai_rumfa);
        return tageti.Tarin_bayani[Math.floorMod(Adireshi_mai_rumfa, Girman_shafi)];
    }

    public void Rubuta_bayit_Daraja(imel_wuri 공간, int Adireshi_mai_rumfa, byte Daraja) {
        int Indes = 쪽번호(Adireshi_mai_rumfa);
        shafi_Daraja tageti = nema_shafi(공간, Adireshi_mai_rumfa);
        if (!tageti.쓰기가능) {
            if (!tageti.쓰기시복사) {
                throw new IllegalStateException("Yi_Karatu 전용 쪽입니다.");
            }
            tageti = ƙirƙíra_Ɓoyewa_shafi(공간, Indes, tageti);
        }
        tageti.Tarin_bayani[Math.floorMod(Adireshi_mai_rumfa, Girman_shafi)] = Daraja;
    }

    public void 범위개인쓰기(imel_wuri 공간, int Fara_imel, int Girma) {
        if (Girma < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int Ƙarshe_imel = Math.addExact(Fara_imel, Girma);
        for (int imel = Fara_imel; imel < Ƙarshe_imel; imel = (쪽번호(imel) + 1) * Girman_shafi) {
            int Indes = 쪽번호(imel);
            shafi_Daraja tageti = nema_shafi(공간, imel);
            if (tageti.쓰기시복사) {
                ƙirƙíra_Ɓoyewa_shafi(공간, Indes, tageti);
            } else {
                tageti.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(imel_wuri 공간, int Fara_imel, byte[] Tarin_bayani) {
        for (int Indes = 0; Indes < Tarin_bayani.length; Indes++) {
            Rubuta_bayit_Daraja(공간, Fara_imel + Indes, Tarin_bayani[Indes]);
        }
    }

    private shafi_Daraja ƙirƙíra_Ɓoyewa_shafi(imel_wuri 공간, int Indes, shafi_Daraja 공유쪽) {
        shafi_Daraja Ɓoyewa_shafi = new shafi_Daraja();
        Ɓoyewa_shafi.Tarin_bayani = Arrays.copyOf(공유쪽.Tarin_bayani, 공유쪽.Tarin_bayani.length);
        Ɓoyewa_shafi.쓰기가능 = true;
        Ɓoyewa_shafi.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.shafi_tebur.put(Integer.valueOf(Indes), Ɓoyewa_shafi);
        return Ɓoyewa_shafi;
    }

    private shafi_Daraja nema_shafi(imel_wuri 공간, int imel) {
        shafi_Daraja tageti = 공간.shafi_tebur.get(Integer.valueOf(쪽번호(imel)));
        if (tageti == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return tageti;
    }

    private int 쪽번호(int imel) {
        if (imel < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return imel / Girman_shafi;
    }
}

