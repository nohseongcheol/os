// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.통신망;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ᏧᎾᏚᏓᎵ_ᏗᏰᎦᏟ {
    @FunctionalInterface
    public interface 자료처리기 {
        void ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(byte[] ᎦᏟᏌᏅᎯ, int ᎠᎢᏎᏍᏗ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ᎦᏘᏅᏛᏙᏗ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        if (!통신망도구.이더넷틀인가(ᎦᏘᏅᏛᏙᏗ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ)) {
            return false;
        }
        int 종류 = 통신망도구.이더넷상위규약(ᎦᏘᏅᏛᏙᏗ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(ᎦᏘᏅᏛᏙᏗ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, 14, ᎦᏘᏅᏛᏙᏗ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ᎦᏘᏅᏛᏙᏗ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, 14);
    }

    private boolean 상호통신망받기(byte[] ᎦᏟᏌᏅᎯ, int ᎠᎢᏎᏍᏗ) {
        if (!통신망도구.상호통신망규약사판인가(ᎦᏟᏌᏅᎯ, ᎠᎢᏎᏍᏗ)) {
            return false;
        }
        int ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏱᎦᏅᎯᏓ = (ᎦᏟᏌᏅᎯ[ᎠᎢᏎᏍᏗ] & 0x0f) * 4;
        int 전체길이 = 통신망도구.큰순서짧은정수(ᎦᏟᏌᏅᎯ, ᎠᎢᏎᏍᏗ + 2);
        if (전체길이 < ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏱᎦᏅᎯᏓ || ᎠᎢᏎᏍᏗ + 전체길이 > ᎦᏟᏌᏅᎯ.length) {
            return false;
        }
        int ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ = ᎦᏟᏌᏅᎯ[ᎠᎢᏎᏍᏗ + 9] & 0xff;
        int ᎦᎸᏛᎢ_ᎭᏂᎩᏍᏓ = ᎠᎢᏎᏍᏗ + ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏱᎦᏅᎯᏓ;
        int ᎦᎸᏛᎢ_ᏱᎦᏅᎯᏓ = 전체길이 - ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏱᎦᏅᎯᏓ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ));
        if (직접처리기 != null) {
            직접처리기.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(ᎦᏟᏌᏅᎯ, ᎦᎸᏛᎢ_ᎭᏂᎩᏍᏓ, ᎦᎸᏛᎢ_ᏱᎦᏅᎯᏓ);
            return true;
        }
        if (ᎦᎸᏛᎢ_ᏱᎦᏅᎯᏓ < 4) {
            return false;
        }
        int 목적포트 = 통신망도구.큰순서짧은정수(ᎦᏟᏌᏅᎯ, ᎦᎸᏛᎢ_ᎭᏂᎩᏍᏓ + 2);
        Map<Integer, 자료처리기> ᎫᏓᎸᏗ_ᏧᎾᎶᎢᏓ = ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ == 17 ? 사용자자료단위처리기 : ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ == 6 ? 전송제어처리기 : null;
        if (ᎫᏓᎸᏗ_ᏧᎾᎶᎢᏓ == null) {
            return false;
        }
        자료처리기 포트처리기 = ᎫᏓᎸᏗ_ᏧᎾᎶᎢᏓ.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(ᎦᏟᏌᏅᎯ, ᎦᎸᏛᎢ_ᎭᏂᎩᏍᏓ, ᎦᎸᏛᎢ_ᏱᎦᏅᎯᏓ);
        return true;
    }
}

