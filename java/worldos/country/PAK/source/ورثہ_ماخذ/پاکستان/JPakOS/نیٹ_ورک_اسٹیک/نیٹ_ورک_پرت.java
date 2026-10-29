// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.نیٹ_ورک_اسٹیک;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class نیٹ_ورک_پرت {
    @FunctionalInterface
    public interface 자료처리기 {
        void عمل_قدر_اندراج(byte[] کوائف, int چلائیں, int لمبا_ئی_قدر);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void رجسٹر_کریں_ایتھرنیٹ(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void رجسٹر_کریں_انٹرنیٹ_پروٹوکول(int جاب_قدر, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(جاب_قدر & 0xff), 처리기);
    }

    public void رجسٹر_کریں_صارف_کوائف_سبق(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void رجسٹر_کریں_ترسیل_کنٹرول(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] فریم_اشاریہ) {
        if (!نیٹ_ورک_ٹولز.معلومات_ٹیکنالوجی_ایتھرنیٹ_فریم(فریم_اشاریہ)) {
            return false;
        }
        int 종류 = نیٹ_ورک_ٹولز.이더넷상위규약(فریم_اشاریہ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.عمل_قدر_اندراج(فریم_اشاریہ, 14, فریم_اشاریہ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(فریم_اشاریہ, 14);
    }

    private boolean 상호통신망받기(byte[] کوائف, int چلائیں) {
        if (!نیٹ_ورک_ٹولز.상호통신망규약사판인가(کوائف, چلائیں)) {
            return false;
        }
        int سرصفحہ_لمبا_ئی = (کوائف[چلائیں] & 0x0f) * 4;
        int 전체길이 = نیٹ_ورک_ٹولز.큰순서짧은정수(کوائف, چلائیں + 2);
        if (전체길이 < سرصفحہ_لمبا_ئی || چلائیں + 전체길이 > کوائف.length) {
            return false;
        }
        int جاب_قدر = کوائف[چلائیں + 9] & 0xff;
        int مشمول_ابتدا = چلائیں + سرصفحہ_لمبا_ئی;
        int مشمول_لمبا_ئی = 전체길이 - سرصفحہ_لمبا_ئی;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(جاب_قدر));
        if (직접처리기 != null) {
            직접처리기.عمل_قدر_اندراج(کوائف, مشمول_ابتدا, مشمول_لمبا_ئی);
            return true;
        }
        if (مشمول_لمبا_ئی < 4) {
            return false;
        }
        int منزل_مقصود_دہانہ_نمبر = نیٹ_ورک_ٹولز.큰순서짧은정수(کوائف, مشمول_ابتدا + 2);
        Map<Integer, 자료처리기> پورٹ_جدول = جاب_قدر == 17 ? 사용자자료단위처리기 : جاب_قدر == 6 ? 전송제어처리기 : null;
        if (پورٹ_جدول == null) {
            return false;
        }
        자료처리기 포트처리기 = پورٹ_جدول.get(Integer.valueOf(منزل_مقصود_دہانہ_نمبر));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.عمل_قدر_اندراج(کوائف, مشمول_ابتدا, مشمول_لمبا_ئی);
        return true;
    }
}

