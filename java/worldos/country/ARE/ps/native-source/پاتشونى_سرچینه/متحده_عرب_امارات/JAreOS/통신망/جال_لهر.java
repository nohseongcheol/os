// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package متحده_عرب_امارات.JAreOS.통신망;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class جال_لهر {
    @FunctionalInterface
    public interface 자료처리기 {
        void 처리(byte[] اومتوک, int ځغلول, int اوږدوالى_ارزښت);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int کیس_ارزښت, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(کیس_ارزښت & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] چوکاټ_لړیال) {
        if (!통신망도구.이더넷틀인가(چوکاټ_لړیال)) {
            return false;
        }
        int 종류 = 통신망도구.이더넷상위규약(چوکاټ_لړیال);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.처리(چوکاټ_لړیال, 14, چوکاټ_لړیال.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(چوکاټ_لړیال, 14);
    }

    private boolean 상호통신망받기(byte[] اومتوک, int ځغلول) {
        if (!통신망도구.상호통신망규약사판인가(اومتوک, ځغلول)) {
            return false;
        }
        int سرۍ_اوږدوالى = (اومتوک[ځغلول] & 0x0f) * 4;
        int 전체길이 = 통신망도구.큰순서짧은정수(اومتوک, ځغلول + 2);
        if (전체길이 < سرۍ_اوږدوالى || ځغلول + 전체길이 > اومتوک.length) {
            return false;
        }
        int کیس_ارزښت = اومتوک[ځغلول + 9] & 0xff;
        int منځپانګه_پيل = ځغلول + سرۍ_اوږدوالى;
        int منځپانګه_اوږدوالى = 전체길이 - سرۍ_اوږدوالى;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(کیس_ارزښت));
        if (직접처리기 != null) {
            직접처리기.처리(اومتوک, منځپانګه_پيل, منځپانګه_اوږدوالى);
            return true;
        }
        if (منځپانګه_اوږدوالى < 4) {
            return false;
        }
        int 목적포트 = 통신망도구.큰순서짧은정수(اومتوک, منځپانګه_پيل + 2);
        Map<Integer, 자료처리기> درشل_لښتيال = کیس_ارزښت == 17 ? 사용자자료단위처리기 : کیس_ارزښت == 6 ? 전송제어처리기 : null;
        if (درشل_لښتيال == null) {
            return false;
        }
        자료처리기 포트처리기 = درشل_لښتيال.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.처리(اومتوک, منځپانګه_پيل, منځپانګه_اوږدوالى);
        return true;
    }
}

