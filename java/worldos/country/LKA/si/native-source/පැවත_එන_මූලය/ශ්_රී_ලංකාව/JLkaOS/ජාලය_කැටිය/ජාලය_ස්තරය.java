// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ජාලය_කැටිය;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ජාලය_ස්තරය {
    @FunctionalInterface
    public interface 자료처리기 {
        void ක්_රියාවලිය_අගය_පිවිසුම(byte[] දත්ත, int ක්_රියාත්මක_කරන්න_2, int දිග_අගය);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ලියාපදිංචිය_ඊතර්නෙට්(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ලියාපදිංචිය_අන්තර්ජාල_ප්_රොටොකෝලය(int කාරණය_අගය, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(කාරණය_අගය & 0xff), 처리기);
    }

    public void ලියාපදිංචිය_පරිශීලක_දත්ත_ඒකක(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void ලියාපදිංචිය_සම්ප්_රේෂණය_පාලකය(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] රාමුව_සූචිය) {
        if (!ජාලය_මෙවලම්.이더넷틀인가(රාමුව_සූචිය)) {
            return false;
        }
        int 종류 = ජාලය_මෙවලම්.이더넷상위규약(රාමුව_සූචිය);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ක්_රියාවලිය_අගය_පිවිසුම(රාමුව_සූචිය, 14, රාමුව_සූචිය.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(රාමුව_සූචිය, 14);
    }

    private boolean 상호통신망받기(byte[] දත්ත, int ක්_රියාත්මක_කරන්න_2) {
        if (!ජාලය_මෙවලම්.상호통신망규약사판인가(දත්ත, ක්_රියාත්මක_කරන්න_2)) {
            return false;
        }
        int ශීර්ෂය_දිග = (දත්ත[ක්_රියාත්මක_කරන්න_2] & 0x0f) * 4;
        int 전체길이 = ජාලය_මෙවලම්.큰순서짧은정수(දත්ත, ක්_රියාත්මක_කරන්න_2 + 2);
        if (전체길이 < ශීර්ෂය_දිග || ක්_රියාත්මක_කරන්න_2 + 전체길이 > දත්ත.length) {
            return false;
        }
        int කාරණය_අගය = දත්ත[ක්_රියාත්මක_කරන්න_2 + 9] & 0xff;
        int අන්තර්ගතය_ඇරඹුම = ක්_රියාත්මක_කරන්න_2 + ශීර්ෂය_දිග;
        int අන්තර්ගතය_දිග = 전체길이 - ශීර්ෂය_දිග;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(කාරණය_අගය));
        if (직접처리기 != null) {
            직접처리기.ක්_රියාවලිය_අගය_පිවිසුම(දත්ත, අන්තර්ගතය_ඇරඹුම, අන්තර්ගතය_දිග);
            return true;
        }
        if (අන්තර්ගතය_දිග < 4) {
            return false;
        }
        int 목적포트 = ජාලය_මෙවලම්.큰순서짧은정수(දත්ත, අන්තර්ගතය_ඇරඹුම + 2);
        Map<Integer, 자료처리기> තොට_වගුව = කාරණය_අගය == 17 ? 사용자자료단위처리기 : කාරණය_අගය == 6 ? 전송제어처리기 : null;
        if (තොට_වගුව == null) {
            return false;
        }
        자료처리기 포트처리기 = තොට_වගුව.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ක්_රියාවලිය_අගය_පිවිසුම(දත්ත, අන්තර්ගතය_ඇරඹුම, අන්තර්ගතය_දිග);
        return true;
    }
}

