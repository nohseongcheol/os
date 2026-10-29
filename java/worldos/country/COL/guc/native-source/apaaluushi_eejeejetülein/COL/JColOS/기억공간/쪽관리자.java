// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ee_iyalaaya_ajutuu 연결과 ashajaa 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int 쪽크기 = 4096;

    private static final class ee_iyalaaya_ajutuu {
        private byte[] atijaaya = new byte[쪽크기];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ejepüsee_WAARAKATAJÜLÜ {
        private final Map<Integer, ee_iyalaaya_ajutuu> ee_iyalaaya_taapüla = new HashMap<Integer, ee_iyalaaya_ajutuu>();
    }

    public ejepüsee_WAARAKATAJÜLÜ 새주소공간() {
        return new ejepüsee_WAARAKATAJÜLÜ();
    }

    public void 쪽연결(ejepüsee_WAARAKATAJÜLÜ 공간, int ejepüsee_mepettujusalü, boolean 쓰기가능) {
        int ee_iyatialujuna = 쪽번호(ejepüsee_mepettujusalü);
        ee_iyalaaya_ajutuu 새쪽 = new ee_iyalaaya_ajutuu();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ee_iyalaaya_taapüla.put(Integer.valueOf(ee_iyatialujuna), 새쪽);
    }

    public ejepüsee_WAARAKATAJÜLÜ 쓰기시복사복제(ejepüsee_WAARAKATAJÜLÜ 원본) {
        ejepüsee_WAARAKATAJÜLÜ 복제본 = new ejepüsee_WAARAKATAJÜLÜ();
        for (Map.Entry<Integer, ee_iyalaaya_ajutuu> ekeroliaa_ajutuu : 원본.ee_iyalaaya_taapüla.entrySet()) {
            ee_iyalaaya_ajutuu 공유쪽 = ekeroliaa_ajutuu.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ee_iyalaaya_taapüla.put(ekeroliaa_ajutuu.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ejepüsee_WAARAKATAJÜLÜ 공간, int ejepüsee_mepettujusalü) {
        ee_iyalaaya_ajutuu 대상 = 쪽찾기(공간, ejepüsee_mepettujusalü);
        return 대상.atijaaya[Math.floorMod(ejepüsee_mepettujusalü, 쪽크기)];
    }

    public void ashajaa_waai_ajutuu(ejepüsee_WAARAKATAJÜLÜ 공간, int ejepüsee_mepettujusalü, byte ajutuu) {
        int ee_iyatialujuna = 쪽번호(ejepüsee_mepettujusalü);
        ee_iyalaaya_ajutuu 대상 = 쪽찾기(공간, ejepüsee_mepettujusalü);
        if (!대상.쓰기가능) {
            if (!대상.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            대상 = 개인쪽만들기(공간, ee_iyatialujuna, 대상);
        }
        대상.atijaaya[Math.floorMod(ejepüsee_mepettujusalü, 쪽크기)] = ajutuu;
    }

    public void 범위개인쓰기(ejepüsee_WAARAKATAJÜLÜ 공간, int achuwalaa_ejepüsee, int 크기) {
        if (크기 < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ajattiraa_ejepüsee = Math.addExact(achuwalaa_ejepüsee, 크기);
        for (int ejepüsee = achuwalaa_ejepüsee; ejepüsee < ajattiraa_ejepüsee; ejepüsee = (쪽번호(ejepüsee) + 1) * 쪽크기) {
            int ee_iyatialujuna = 쪽번호(ejepüsee);
            ee_iyalaaya_ajutuu 대상 = 쪽찾기(공간, ejepüsee);
            if (대상.쓰기시복사) {
                개인쪽만들기(공간, ee_iyatialujuna, 대상);
            } else {
                대상.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ejepüsee_WAARAKATAJÜLÜ 공간, int achuwalaa_ejepüsee, byte[] atijaaya) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < atijaaya.length; ee_iyatialujuna++) {
            ashajaa_waai_ajutuu(공간, achuwalaa_ejepüsee + ee_iyatialujuna, atijaaya[ee_iyatialujuna]);
        }
    }

    private ee_iyalaaya_ajutuu 개인쪽만들기(ejepüsee_WAARAKATAJÜLÜ 공간, int ee_iyatialujuna, ee_iyalaaya_ajutuu 공유쪽) {
        ee_iyalaaya_ajutuu kalaamainsü_ee_iyalaaya = new ee_iyalaaya_ajutuu();
        kalaamainsü_ee_iyalaaya.atijaaya = Arrays.copyOf(공유쪽.atijaaya, 공유쪽.atijaaya.length);
        kalaamainsü_ee_iyalaaya.쓰기가능 = true;
        kalaamainsü_ee_iyalaaya.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ee_iyalaaya_taapüla.put(Integer.valueOf(ee_iyatialujuna), kalaamainsü_ee_iyalaaya);
        return kalaamainsü_ee_iyalaaya;
    }

    private ee_iyalaaya_ajutuu 쪽찾기(ejepüsee_WAARAKATAJÜLÜ 공간, int ejepüsee) {
        ee_iyalaaya_ajutuu 대상 = 공간.ee_iyalaaya_taapüla.get(Integer.valueOf(쪽번호(ejepüsee)));
        if (대상 == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return 대상;
    }

    private int 쪽번호(int ejepüsee) {
        if (ejepüsee < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ejepüsee / 쪽크기;
    }
}

