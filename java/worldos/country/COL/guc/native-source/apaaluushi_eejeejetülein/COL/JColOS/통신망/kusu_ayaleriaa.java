// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.통신망;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class kusu_ayaleriaa {
    @FunctionalInterface
    public interface 자료처리기 {
        void 처리(byte[] atijaaya, int 시작, int akaliaa_ajutuu);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int achikii_ajutuu, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(achikii_ajutuu & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] otpünaa_ee_iyatialujuna) {
        if (!통신망도구.이더넷틀인가(otpünaa_ee_iyatialujuna)) {
            return false;
        }
        int 종류 = 통신망도구.이더넷상위규약(otpünaa_ee_iyatialujuna);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.처리(otpünaa_ee_iyatialujuna, 14, otpünaa_ee_iyatialujuna.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(otpünaa_ee_iyatialujuna, 14);
    }

    private boolean 상호통신망받기(byte[] atijaaya, int 시작) {
        if (!통신망도구.상호통신망규약사판인가(atijaaya, 시작)) {
            return false;
        }
        int o_ttiakii_akaliaa = (atijaaya[시작] & 0x0f) * 4;
        int 전체길이 = 통신망도구.큰순서짧은정수(atijaaya, 시작 + 2);
        if (전체길이 < o_ttiakii_akaliaa || 시작 + 전체길이 > atijaaya.length) {
            return false;
        }
        int achikii_ajutuu = atijaaya[시작 + 9] & 0xff;
        int alu_ujatüü_achuwalaa = 시작 + o_ttiakii_akaliaa;
        int alu_ujatüü_akaliaa = 전체길이 - o_ttiakii_akaliaa;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(achikii_ajutuu));
        if (직접처리기 != null) {
            직접처리기.처리(atijaaya, alu_ujatüü_achuwalaa, alu_ujatüü_akaliaa);
            return true;
        }
        if (alu_ujatüü_akaliaa < 4) {
            return false;
        }
        int 목적포트 = 통신망도구.큰순서짧은정수(atijaaya, alu_ujatüü_achuwalaa + 2);
        Map<Integer, 자료처리기> outtülee_taapüla = achikii_ajutuu == 17 ? 사용자자료단위처리기 : achikii_ajutuu == 6 ? 전송제어처리기 : null;
        if (outtülee_taapüla == null) {
            return false;
        }
        자료처리기 포트처리기 = outtülee_taapüla.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.처리(atijaaya, alu_ujatüü_achuwalaa, alu_ujatüü_akaliaa);
        return true;
    }
}

