// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeriyaa.JNgaOS.통신망;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class laylaytol_tekkeendi {
    @FunctionalInterface
    public interface 자료처리기 {
        void Yuɓɓo_golle_njaru_naatnugol(byte[] keɓe, int huutoraade, int njuuteendi_njaru);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int haaju_njaru, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(haaju_njaru & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] taƴtinnde_joopirdu) {
        if (!통신망도구.이더넷틀인가(taƴtinnde_joopirdu)) {
            return false;
        }
        int 종류 = 통신망도구.이더넷상위규약(taƴtinnde_joopirdu);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Yuɓɓo_golle_njaru_naatnugol(taƴtinnde_joopirdu, 14, taƴtinnde_joopirdu.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(taƴtinnde_joopirdu, 14);
    }

    private boolean 상호통신망받기(byte[] keɓe, int huutoraade) {
        if (!통신망도구.상호통신망규약사판인가(keɓe, huutoraade)) {
            return false;
        }
        int meetalol_hello_njuuteendi = (keɓe[huutoraade] & 0x0f) * 4;
        int 전체길이 = 통신망도구.큰순서짧은정수(keɓe, huutoraade + 2);
        if (전체길이 < meetalol_hello_njuuteendi || huutoraade + 전체길이 > keɓe.length) {
            return false;
        }
        int haaju_njaru = keɓe[huutoraade + 9] & 0xff;
        int loowdi_huɓɓude = huutoraade + meetalol_hello_njuuteendi;
        int loowdi_njuuteendi = 전체길이 - meetalol_hello_njuuteendi;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(haaju_njaru));
        if (직접처리기 != null) {
            직접처리기.Yuɓɓo_golle_njaru_naatnugol(keɓe, loowdi_huɓɓude, loowdi_njuuteendi);
            return true;
        }
        if (loowdi_njuuteendi < 4) {
            return false;
        }
        int 목적포트 = 통신망도구.큰순서짧은정수(keɓe, loowdi_huɓɓude + 2);
        Map<Integer, 자료처리기> poor_taabal = haaju_njaru == 17 ? 사용자자료단위처리기 : haaju_njaru == 6 ? 전송제어처리기 : null;
        if (poor_taabal == null) {
            return false;
        }
        자료처리기 포트처리기 = poor_taabal.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Yuɓɓo_golle_njaru_naatnugol(keɓe, loowdi_huɓɓude, loowdi_njuuteendi);
        return true;
    }
}

