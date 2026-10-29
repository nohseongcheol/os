// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.نیٹ_ورک_گٹھا;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class نیٹ_ورک_پرت {
    @FunctionalInterface
    public interface 자료처리기 {
        void عمل_قدر_داخلہ(byte[] کوائف, int چلاؤ, int لمبائی_قدر);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void رجسٹر_ایتھرنیٹ(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void رجسٹر_انٹرنیٹ_پروٹوکول(int حالت_قدر_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(حالت_قدر_102996da & 0xff), 처리기);
    }

    public void رجسٹر_صارف_کوائف_سبق(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] فریم_اشاریہ) {
        if (!نیٹ_ورک_اوزار.이더넷틀인가(فریم_اشاریہ)) {
            return false;
        }
        int 종류 = نیٹ_ورک_اوزار.이더넷상위규약(فریم_اشاریہ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.عمل_قدر_داخلہ(فریم_اشاریہ, 14, فریم_اشاریہ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(فریم_اشاریہ, 14);
    }

    private boolean 상호통신망받기(byte[] کوائف, int چلاؤ) {
        if (!نیٹ_ورک_اوزار.상호통신망규약사판인가(کوائف, چلاؤ)) {
            return false;
        }
        int سرتحریر_لمبائی = (کوائف[چلاؤ] & 0x0f) * 4;
        int 전체길이 = نیٹ_ورک_اوزار.큰순서짧은정수(کوائف, چلاؤ + 2);
        if (전체길이 < سرتحریر_لمبائی || چلاؤ + 전체길이 > کوائف.length) {
            return false;
        }
        int حالت_قدر_102996da = کوائف[چلاؤ + 9] & 0xff;
        int اجزاء_مکھ = چلاؤ + سرتحریر_لمبائی;
        int اجزاء_لمبائی = 전체길이 - سرتحریر_لمبائی;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(حالت_قدر_102996da));
        if (직접처리기 != null) {
            직접처리기.عمل_قدر_داخلہ(کوائف, اجزاء_مکھ, اجزاء_لمبائی);
            return true;
        }
        if (اجزاء_لمبائی < 4) {
            return false;
        }
        int 목적포트 = نیٹ_ورک_اوزار.큰순서짧은정수(کوائف, اجزاء_مکھ + 2);
        Map<Integer, 자료처리기> دہانہ_جدول = حالت_قدر_102996da == 17 ? 사용자자료단위처리기 : حالت_قدر_102996da == 6 ? 전송제어처리기 : null;
        if (دہانہ_جدول == null) {
            return false;
        }
        자료처리기 포트처리기 = دہانہ_جدول.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.عمل_قدر_داخلہ(کوائف, اجزاء_مکھ, اجزاء_لمبائی);
        return true;
    }
}

