// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gine_Bisaawo.JGnbOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB hello_njaru 연결과 winndude 시 복사를 제공한다. */
public final class hello_kisnoowo {
    public static final int hello_waylude_etannde = 4096;

    private static final class hello_njaru {
        private byte[] keɓe = new byte[hello_waylude_etannde];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ñiiɓirde_wonorde {
        private final Map<Integer, hello_njaru> hello_taabal = new HashMap<Integer, hello_njaru>();
    }

    public ñiiɓirde_wonorde 새주소공간() {
        return new ñiiɓirde_wonorde();
    }

    public void 쪽연결(ñiiɓirde_wonorde 공간, int paayaalo_ñiiɓirde, boolean 쓰기가능) {
        int joopirdu = 쪽번호(paayaalo_ñiiɓirde);
        hello_njaru 새쪽 = new hello_njaru();
        새쪽.쓰기가능 = 쓰기가능;
        공간.hello_taabal.put(Integer.valueOf(joopirdu), 새쪽);
    }

    public ñiiɓirde_wonorde 쓰기시복사복제(ñiiɓirde_wonorde 원본) {
        ñiiɓirde_wonorde 복제본 = new ñiiɓirde_wonorde();
        for (Map.Entry<Integer, hello_njaru> naatnugol_njaru : 원본.hello_taabal.entrySet()) {
            hello_njaru 공유쪽 = naatnugol_njaru.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.hello_taabal.put(naatnugol_njaru.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ñiiɓirde_wonorde 공간, int paayaalo_ñiiɓirde) {
        hello_njaru faandaare = yiylaade_hello(공간, paayaalo_ñiiɓirde);
        return faandaare.keɓe[Math.floorMod(paayaalo_ñiiɓirde, hello_waylude_etannde)];
    }

    public void winndude_oktee_njaru(ñiiɓirde_wonorde 공간, int paayaalo_ñiiɓirde, byte njaru) {
        int joopirdu = 쪽번호(paayaalo_ñiiɓirde);
        hello_njaru faandaare = yiylaade_hello(공간, paayaalo_ñiiɓirde);
        if (!faandaare.쓰기가능) {
            if (!faandaare.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            faandaare = 개인쪽만들기(공간, joopirdu, faandaare);
        }
        faandaare.keɓe[Math.floorMod(paayaalo_ñiiɓirde, hello_waylude_etannde)] = njaru;
    }

    public void 범위개인쓰기(ñiiɓirde_wonorde 공간, int huɓɓude_ñiiɓirde, int waylude_etannde) {
        if (waylude_etannde < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int taƴde_ñiiɓirde = Math.addExact(huɓɓude_ñiiɓirde, waylude_etannde);
        for (int ñiiɓirde = huɓɓude_ñiiɓirde; ñiiɓirde < taƴde_ñiiɓirde; ñiiɓirde = (쪽번호(ñiiɓirde) + 1) * hello_waylude_etannde) {
            int joopirdu = 쪽번호(ñiiɓirde);
            hello_njaru faandaare = yiylaade_hello(공간, ñiiɓirde);
            if (faandaare.쓰기시복사) {
                개인쪽만들기(공간, joopirdu, faandaare);
            } else {
                faandaare.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ñiiɓirde_wonorde 공간, int huɓɓude_ñiiɓirde, byte[] keɓe) {
        for (int joopirdu = 0; joopirdu < keɓe.length; joopirdu++) {
            winndude_oktee_njaru(공간, huɓɓude_ñiiɓirde + joopirdu, keɓe[joopirdu]);
        }
    }

    private hello_njaru 개인쪽만들기(ñiiɓirde_wonorde 공간, int joopirdu, hello_njaru 공유쪽) {
        hello_njaru heerii_hello = new hello_njaru();
        heerii_hello.keɓe = Arrays.copyOf(공유쪽.keɓe, 공유쪽.keɓe.length);
        heerii_hello.쓰기가능 = true;
        heerii_hello.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.hello_taabal.put(Integer.valueOf(joopirdu), heerii_hello);
        return heerii_hello;
    }

    private hello_njaru yiylaade_hello(ñiiɓirde_wonorde 공간, int ñiiɓirde) {
        hello_njaru faandaare = 공간.hello_taabal.get(Integer.valueOf(쪽번호(ñiiɓirde)));
        if (faandaare == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return faandaare;
    }

    private int 쪽번호(int ñiiɓirde) {
        if (ñiiɓirde < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ñiiɓirde / hello_waylude_etannde;
    }
}

