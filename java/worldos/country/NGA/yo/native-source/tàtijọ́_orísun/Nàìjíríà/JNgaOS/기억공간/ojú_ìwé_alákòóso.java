// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ojú_ìwé_iye 연결과 Kọ 시 복사를 제공한다. */
public final class ojú_ìwé_alákòóso {
    public static final int ìwọ̀n_ojú_ìwé = 4096;

    private static final class ojú_ìwé_iye {
        private byte[] détà = new byte[ìwọ̀n_ojú_ìwé];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class àdírẹ́ẹ̀sì_àlàfo {
        private final Map<Integer, ojú_ìwé_iye> ojú_ìwé_atọ́ka = new HashMap<Integer, ojú_ìwé_iye>();
    }

    public àdírẹ́ẹ̀sì_àlàfo 새주소공간() {
        return new àdírẹ́ẹ̀sì_àlàfo();
    }

    public void máàpù_ojú_ìwé(àdírẹ́ẹ̀sì_àlàfo 공간, int àdírẹ́ẹ̀sì_àfojúinúní, boolean 쓰기가능) {
        int wá_atọ̀ka_àkóónú = 쪽번호(àdírẹ́ẹ̀sì_àfojúinúní);
        ojú_ìwé_iye 새쪽 = new ojú_ìwé_iye();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ojú_ìwé_atọ́ka.put(Integer.valueOf(wá_atọ̀ka_àkóónú), 새쪽);
    }

    public àdírẹ́ẹ̀sì_àlàfo 쓰기시복사복제(àdírẹ́ẹ̀sì_àlàfo 원본) {
        àdírẹ́ẹ̀sì_àlàfo 복제본 = new àdírẹ́ẹ̀sì_àlàfo();
        for (Map.Entry<Integer, ojú_ìwé_iye> ìgbéwọlé_iye : 원본.ojú_ìwé_atọ́ka.entrySet()) {
            ojú_ìwé_iye 공유쪽 = ìgbéwọlé_iye.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ojú_ìwé_atọ́ka.put(ìgbéwọlé_iye.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(àdírẹ́ẹ̀sì_àlàfo 공간, int àdírẹ́ẹ̀sì_àfojúinúní) {
        ojú_ìwé_iye àfojúsùn = wá_ojú_ìwé(공간, àdírẹ́ẹ̀sì_àfojúinúní);
        return àfojúsùn.détà[Math.floorMod(àdírẹ́ẹ̀sì_àfojúinúní, ìwọ̀n_ojú_ìwé)];
    }

    public void kọ_báìtì_iye(àdírẹ́ẹ̀sì_àlàfo 공간, int àdírẹ́ẹ̀sì_àfojúinúní, byte iye) {
        int wá_atọ̀ka_àkóónú = 쪽번호(àdírẹ́ẹ̀sì_àfojúinúní);
        ojú_ìwé_iye àfojúsùn = wá_ojú_ìwé(공간, àdírẹ́ẹ̀sì_àfojúinúní);
        if (!àfojúsùn.쓰기가능) {
            if (!àfojúsùn.쓰기시복사) {
                throw new IllegalStateException("Kàá 전용 쪽입니다.");
            }
            àfojúsùn = Ṣẹ̀dá_àdáni_ojú_ìwé(공간, wá_atọ̀ka_àkóónú, àfojúsùn);
        }
        àfojúsùn.détà[Math.floorMod(àdírẹ́ẹ̀sì_àfojúinúní, ìwọ̀n_ojú_ìwé)] = iye;
    }

    public void 범위개인쓰기(àdírẹ́ẹ̀sì_àlàfo 공간, int bẹ̀rẹ̀_àdírẹ́ẹ̀sì, int Ìwọ̀n) {
        if (Ìwọ̀n < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int parí_àdírẹ́ẹ̀sì = Math.addExact(bẹ̀rẹ̀_àdírẹ́ẹ̀sì, Ìwọ̀n);
        for (int àdírẹ́ẹ̀sì = bẹ̀rẹ̀_àdírẹ́ẹ̀sì; àdírẹ́ẹ̀sì < parí_àdírẹ́ẹ̀sì; àdírẹ́ẹ̀sì = (쪽번호(àdírẹ́ẹ̀sì) + 1) * ìwọ̀n_ojú_ìwé) {
            int wá_atọ̀ka_àkóónú = 쪽번호(àdírẹ́ẹ̀sì);
            ojú_ìwé_iye àfojúsùn = wá_ojú_ìwé(공간, àdírẹ́ẹ̀sì);
            if (àfojúsùn.쓰기시복사) {
                Ṣẹ̀dá_àdáni_ojú_ìwé(공간, wá_atọ̀ka_àkóónú, àfojúsùn);
            } else {
                àfojúsùn.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(àdírẹ́ẹ̀sì_àlàfo 공간, int bẹ̀rẹ̀_àdírẹ́ẹ̀sì, byte[] détà) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < détà.length; wá_atọ̀ka_àkóónú++) {
            kọ_báìtì_iye(공간, bẹ̀rẹ̀_àdírẹ́ẹ̀sì + wá_atọ̀ka_àkóónú, détà[wá_atọ̀ka_àkóónú]);
        }
    }

    private ojú_ìwé_iye Ṣẹ̀dá_àdáni_ojú_ìwé(àdírẹ́ẹ̀sì_àlàfo 공간, int wá_atọ̀ka_àkóónú, ojú_ìwé_iye 공유쪽) {
        ojú_ìwé_iye àdáni_ojú_ìwé = new ojú_ìwé_iye();
        àdáni_ojú_ìwé.détà = Arrays.copyOf(공유쪽.détà, 공유쪽.détà.length);
        àdáni_ojú_ìwé.쓰기가능 = true;
        àdáni_ojú_ìwé.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ojú_ìwé_atọ́ka.put(Integer.valueOf(wá_atọ̀ka_àkóónú), àdáni_ojú_ìwé);
        return àdáni_ojú_ìwé;
    }

    private ojú_ìwé_iye wá_ojú_ìwé(àdírẹ́ẹ̀sì_àlàfo 공간, int àdírẹ́ẹ̀sì) {
        ojú_ìwé_iye àfojúsùn = 공간.ojú_ìwé_atọ́ka.get(Integer.valueOf(쪽번호(àdírẹ́ẹ̀sì)));
        if (àfojúsùn == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return àfojúsùn;
    }

    private int 쪽번호(int àdírẹ́ẹ̀sì) {
        if (àdírẹ́ẹ̀sì < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return àdírẹ́ẹ̀sì / ìwọ̀n_ojú_ìwé;
    }
}

