// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ڀارت.JIndOS.نيٽ_ورڪ_اڀرڻ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class نيٽ_ورڪ_پرت {
    @FunctionalInterface
    public interface 자료처리기 {
        void عمل_قدر_داخلا(byte[] ڪوائف, int هلائڻ, int لمبائي_قدر);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int حالت_قدر_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(حالت_قدر_102996da & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] فريم_ابتدائي) {
        if (!نيٽ_ورڪ_اوزار.이더넷틀인가(فريم_ابتدائي)) {
            return false;
        }
        int 종류 = نيٽ_ورڪ_اوزار.이더넷상위규약(فريم_ابتدائي);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.عمل_قدر_داخلا(فريم_ابتدائي, 14, فريم_ابتدائي.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(فريم_ابتدائي, 14);
    }

    private boolean 상호통신망받기(byte[] ڪوائف, int هلائڻ) {
        if (!نيٽ_ورڪ_اوزار.상호통신망규약사판인가(ڪوائف, هلائڻ)) {
            return false;
        }
        int هيڊر_لمبائي = (ڪوائف[هلائڻ] & 0x0f) * 4;
        int 전체길이 = نيٽ_ورڪ_اوزار.큰순서짧은정수(ڪوائف, هلائڻ + 2);
        if (전체길이 < هيڊر_لمبائي || هلائڻ + 전체길이 > ڪوائف.length) {
            return false;
        }
        int حالت_قدر_102996da = ڪوائف[هلائڻ + 9] & 0xff;
        int مواد_شروع = هلائڻ + هيڊر_لمبائي;
        int مواد_لمبائي = 전체길이 - هيڊر_لمبائي;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(حالت_قدر_102996da));
        if (직접처리기 != null) {
            직접처리기.عمل_قدر_داخلا(ڪوائف, مواد_شروع, مواد_لمبائي);
            return true;
        }
        if (مواد_لمبائي < 4) {
            return false;
        }
        int 목적포트 = نيٽ_ورڪ_اوزار.큰순서짧은정수(ڪوائف, مواد_شروع + 2);
        Map<Integer, 자료처리기> پورٽ_جدول = حالت_قدر_102996da == 17 ? 사용자자료단위처리기 : حالت_قدر_102996da == 6 ? 전송제어처리기 : null;
        if (پورٽ_جدول == null) {
            return false;
        }
        자료처리기 포트처리기 = پورٽ_جدول.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.عمل_قدر_داخلا(ڪوائف, مواد_شروع, مواد_لمبائي);
        return true;
    }
}

