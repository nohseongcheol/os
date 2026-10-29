// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ 연결과 ᎪᏪᎶᏗ 시 복사를 제공한다. */
public final class ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ {
    public static final int ᎤᎦᏅᏓᏛᎢ_ᎢᎩᏓ = 4096;

    private static final class ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ {
        private byte[] ᎦᏟᏌᏅᎯ = new byte[ᎤᎦᏅᏓᏛᎢ_ᎢᎩᏓ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE {
        private final Map<Integer, ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ> ᎤᎦᏅᏓᏛᎢ_ᏧᎾᎶᎢᏓ = new HashMap<Integer, ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ>();
    }

    public ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 새주소공간() {
        return new ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE();
    }

    public void 쪽연결(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 공간, int ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, boolean 쓰기가능) {
        int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 쪽번호(ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);
        ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ 새쪽 = new ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ᎤᎦᏅᏓᏛᎢ_ᏧᎾᎶᎢᏓ.put(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ), 새쪽);
    }

    public ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 쓰기시복사복제(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 원본) {
        ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 복제본 = new ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE();
        for (Map.Entry<Integer, ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ : 원본.ᎤᎦᏅᏓᏛᎢ_ᏧᎾᎶᎢᏓ.entrySet()) {
            ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ 공유쪽 = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ᎤᎦᏅᏓᏛᎢ_ᏧᎾᎶᎢᏓ.put(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 공간, int ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
        ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ ᎠᏉᏅᏗᎢ = ᎯᏩᏔ_ᎤᎦᏅᏓᏛᎢ(공간, ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);
        return ᎠᏉᏅᏗᎢ.ᎦᏟᏌᏅᎯ[Math.floorMod(ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎤᎦᏅᏓᏛᎢ_ᎢᎩᏓ)];
    }

    public void ᎪᏪᎶᏗ_byte_ᏧᎬᏩᎶᏗᏯ(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 공간, int ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, byte ᏧᎬᏩᎶᏗᏯ) {
        int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 쪽번호(ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);
        ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ ᎠᏉᏅᏗᎢ = ᎯᏩᏔ_ᎤᎦᏅᏓᏛᎢ(공간, ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);
        if (!ᎠᏉᏅᏗᎢ.쓰기가능) {
            if (!ᎠᏉᏅᏗᎢ.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            ᎠᏉᏅᏗᎢ = 개인쪽만들기(공간, ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, ᎠᏉᏅᏗᎢ);
        }
        ᎠᏉᏅᏗᎢ.ᎦᏟᏌᏅᎯ[Math.floorMod(ᎠᏓᏅᏙ_ᎢᏳᏍᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎤᎦᏅᏓᏛᎢ_ᎢᎩᏓ)] = ᏧᎬᏩᎶᏗᏯ;
    }

    public void 범위개인쓰기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 공간, int ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᎢᎩᏓ) {
        if (ᎢᎩᏓ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ᎠᏍᏆᏗᏍᏙᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = Math.addExact(ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎢᎩᏓ);
        for (int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ; ᎪᏪᎵ_ᏫᏗᎦᏅᏗ < ᎠᏍᏆᏗᏍᏙᏗ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ; ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = (쪽번호(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) + 1) * ᎤᎦᏅᏓᏛᎢ_ᎢᎩᏓ) {
            int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 쪽번호(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);
            ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ ᎠᏉᏅᏗᎢ = ᎯᏩᏔ_ᎤᎦᏅᏓᏛᎢ(공간, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ);
            if (ᎠᏉᏅᏗᎢ.쓰기시복사) {
                개인쪽만들기(공간, ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, ᎠᏉᏅᏗᎢ);
            } else {
                ᎠᏉᏅᏗᎢ.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 공간, int ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, byte[] ᎦᏟᏌᏅᎯ) {
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < ᎦᏟᏌᏅᎯ.length; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            ᎪᏪᎶᏗ_byte_ᏧᎬᏩᎶᏗᏯ(공간, ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, ᎦᏟᏌᏅᎯ[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ]);
        }
    }

    private ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ 개인쪽만들기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 공간, int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ 공유쪽) {
        ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ ᎬᏍᎦᏟ_ᎤᎦᏅᏓᏛᎢ = new ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ();
        ᎬᏍᎦᏟ_ᎤᎦᏅᏓᏛᎢ.ᎦᏟᏌᏅᎯ = Arrays.copyOf(공유쪽.ᎦᏟᏌᏅᎯ, 공유쪽.ᎦᏟᏌᏅᎯ.length);
        ᎬᏍᎦᏟ_ᎤᎦᏅᏓᏛᎢ.쓰기가능 = true;
        ᎬᏍᎦᏟ_ᎤᎦᏅᏓᏛᎢ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ᎤᎦᏅᏓᏛᎢ_ᏧᎾᎶᎢᏓ.put(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ), ᎬᏍᎦᏟ_ᎤᎦᏅᏓᏛᎢ);
        return ᎬᏍᎦᏟ_ᎤᎦᏅᏓᏛᎢ;
    }

    private ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ ᎯᏩᏔ_ᎤᎦᏅᏓᏛᎢ(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE 공간, int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
        ᎤᎦᏅᏓᏛᎢ_ᏧᎬᏩᎶᏗᏯ ᎠᏉᏅᏗᎢ = 공간.ᎤᎦᏅᏓᏛᎢ_ᏧᎾᎶᎢᏓ.get(Integer.valueOf(쪽번호(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)));
        if (ᎠᏉᏅᏗᎢ == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ᎠᏉᏅᏗᎢ;
    }

    private int 쪽번호(int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
        if (ᎪᏪᎵ_ᏫᏗᎦᏅᏗ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ᎪᏪᎵ_ᏫᏗᎦᏅᏗ / ᎤᎦᏅᏓᏛᎢ_ᎢᎩᏓ;
    }
}

