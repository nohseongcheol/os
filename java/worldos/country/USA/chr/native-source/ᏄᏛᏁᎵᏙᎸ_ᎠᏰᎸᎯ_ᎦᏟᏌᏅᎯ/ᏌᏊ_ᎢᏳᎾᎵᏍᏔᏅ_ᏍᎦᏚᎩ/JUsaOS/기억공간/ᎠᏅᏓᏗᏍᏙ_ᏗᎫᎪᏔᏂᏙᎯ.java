// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ᏗᏅᏅᏓᎦᏥᏃᏍᏓ_ᏗᎦᏅᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ 할당, 해제, 병합을 담당한다. */
public final class ᎠᏅᏓᏗᏍᏙ_ᏗᎫᎪᏔᏂᏙᎯ {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public ᎠᏅᏓᏗᏍᏙ_ᏗᎫᎪᏔᏂᏙᎯ(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int 할당(int ᎢᎩᏓ) {
        return 정렬할당(ᎢᎩᏓ, 1);
    }

    public synchronized int 정렬할당(int ᎢᎩᏓ, int ᏗᏅᏅᏓᎦᏥᏃᏍᏓ_ᏗᎦᏅᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ) {
        if (ᎢᎩᏓ <= 0 || ᏗᏅᏅᏓᎦᏥᏃᏍᏓ_ᏗᎦᏅᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ <= 0 || (ᏗᏅᏅᏓᎦᏥᏃᏍᏓ_ᏗᎦᏅᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ & (ᏗᏅᏅᏓᎦᏥᏃᏍᏓ_ᏗᎦᏅᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ : 빈영역.entrySet()) {
            int ᎠᎢᏎᏍᏗ = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getKey().intValue();
            int 영역크기 = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getValue().intValue();
            int 정렬시작 = (ᎠᎢᏎᏍᏗ + ᏗᏅᏅᏓᎦᏥᏃᏍᏓ_ᏗᎦᏅᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ - 1) & -ᏗᏅᏅᏓᎦᏥᏃᏍᏓ_ᏗᎦᏅᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ;
            int 앞크기 = 정렬시작 - ᎠᎢᏎᏍᏗ;
            int 끝크기 = 영역크기 - 앞크기 - ᎢᎩᏓ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ᎠᎢᏎᏍᏗ));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(ᎠᎢᏎᏍᏗ), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ᎢᎩᏓ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ᎢᎩᏓ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ᎢᎩᏓ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void 해제(int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
        Integer ᎢᎩᏓ_ᎪᎱᏍᏗ = 사용영역.remove(Integer.valueOf(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ));
        if (ᎢᎩᏓ_ᎪᎱᏍᏗ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ᎠᎢᏎᏍᏗ = ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
        int ᎢᎩᏓ = ᎢᎩᏓ_ᎪᎱᏍᏗ.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(ᎠᎢᏎᏍᏗ));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == ᎠᎢᏎᏍᏗ) {
            ᎠᎢᏎᏍᏗ = 앞.getKey().intValue();
            ᎢᎩᏓ += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ = 빈영역.ceilingEntry(Integer.valueOf(ᎠᎢᏎᏍᏗ));
        if (ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ != null && ᎠᎢᏎᏍᏗ + ᎢᎩᏓ == ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ.getKey().intValue()) {
            ᎢᎩᏓ += ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ.getValue().intValue();
            빈영역.remove(ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ.getKey());
        }
        빈영역.put(Integer.valueOf(ᎠᎢᏎᏍᏗ), Integer.valueOf(ᎢᎩᏓ));
    }

    public synchronized byte 바이트읽기(int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
        범위확인(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, 1);
        return 기억공간[ᎪᏪᎵ_ᏫᏗᎦᏅᏗ];
    }

    public synchronized void ᎪᏪᎶᏗ_byte_ᏧᎬᏩᎶᏗᏯ(int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, byte ᏧᎬᏩᎶᏗᏯ) {
        범위확인(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, 1);
        기억공간[ᎪᏪᎵ_ᏫᏗᎦᏅᏗ] = ᏧᎬᏩᎶᏗᏯ;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ᎢᎩᏓ : 사용영역.values()) {
            합계 += ᎢᎩᏓ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int ᎢᎩᏓ) {
        if (ᎪᏪᎵ_ᏫᏗᎦᏅᏗ < 0 || ᎢᎩᏓ < 0 || ᎪᏪᎵ_ᏫᏗᎦᏅᏗ > 기억공간.length - ᎢᎩᏓ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

