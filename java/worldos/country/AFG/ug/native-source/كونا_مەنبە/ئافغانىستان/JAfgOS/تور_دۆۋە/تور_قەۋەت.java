// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.تور_دۆۋە;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class تور_قەۋەت {
    @FunctionalInterface
    public interface 자료처리기 {
        void جەريان_قىممىتى_كىرگۈزۈش(byte[] مەلۇمات, int ئىجرا_قىل_2, int ئۇزۇنلۇق_قىممىتى);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void تىزىملىتىش_ئىسېرنېت(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void تىزىملىتىش_ئىنتېرنېت_كېلىشىمى(int خىزمەت_قىممىتى, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(خىزمەت_قىممىتى & 0xff), 처리기);
    }

    public void تىزىملىتىش_ئىشلەتكۈچى_مەلۇمات_دەرس(int قاتتىق_دېتال_ئېغىز, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(قاتتىق_دېتال_ئېغىز & 0xffff), 처리기);
    }

    public void 전송제어등록(int قاتتىق_دېتال_ئېغىز, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(قاتتىق_دېتال_ئېغىز & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] رامكا_ئىندېكس) {
        if (!تور_قوراللار.이더넷틀인가(رامكا_ئىندېكس)) {
            return false;
        }
        int 종류 = تور_قوراللار.이더넷상위규약(رامكا_ئىندېكس);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.جەريان_قىممىتى_كىرگۈزۈش(رامكا_ئىندېكس, 14, رامكا_ئىندېكس.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(رامكا_ئىندېكس, 14);
    }

    private boolean 상호통신망받기(byte[] مەلۇمات, int ئىجرا_قىل_2) {
        if (!تور_قوراللار.상호통신망규약사판인가(مەلۇمات, ئىجرا_قىل_2)) {
            return false;
        }
        int بېشى_ئۇزۇنلۇق = (مەلۇمات[ئىجرا_قىل_2] & 0x0f) * 4;
        int 전체길이 = تور_قوراللار.큰순서짧은정수(مەلۇمات, ئىجرا_قىل_2 + 2);
        if (전체길이 < بېشى_ئۇزۇنلۇق || ئىجرا_قىل_2 + 전체길이 > مەلۇمات.length) {
            return false;
        }
        int خىزمەت_قىممىتى = مەلۇمات[ئىجرا_قىل_2 + 9] & 0xff;
        int مەزمۇن_باشلاش = ئىجرا_قىل_2 + بېشى_ئۇزۇنلۇق;
        int مەزمۇن_ئۇزۇنلۇق = 전체길이 - بېشى_ئۇزۇنلۇق;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(خىزمەت_قىممىتى));
        if (직접처리기 != null) {
            직접처리기.جەريان_قىممىتى_كىرگۈزۈش(مەلۇمات, مەزمۇن_باشلاش, مەزمۇن_ئۇزۇنلۇق);
            return true;
        }
        if (مەزمۇن_ئۇزۇنلۇق < 4) {
            return false;
        }
        int 목적포트 = تور_قوراللار.큰순서짧은정수(مەلۇمات, مەزمۇن_باشلاش + 2);
        Map<Integer, 자료처리기> ئېغىز_جەدۋەل = خىزمەت_قىممىتى == 17 ? 사용자자료단위처리기 : خىزمەت_قىممىتى == 6 ? 전송제어처리기 : null;
        if (ئېغىز_جەدۋەل == null) {
            return false;
        }
        자료처리기 포트처리기 = ئېغىز_جەدۋەل.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.جەريان_قىممىتى_كىرگۈزۈش(مەلۇمات, مەزمۇن_باشلاش, مەزمۇن_ئۇزۇنلۇق);
        return true;
    }
}

