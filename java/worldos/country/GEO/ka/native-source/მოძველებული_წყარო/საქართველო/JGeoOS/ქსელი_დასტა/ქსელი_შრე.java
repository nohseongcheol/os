// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package საქართველო.JGeoOS.ქსელი_დასტა;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ქსელი_შრე {
    @FunctionalInterface
    public interface 자료처리기 {
        void პროცესი_მნიშვნელობა_შენატანი(byte[] მონაცემები, int გაშვება, int სიგრძე_მნიშვნელობა);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void დარეგისტრირება_ეთერნეთი(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void დარეგისტრირება_ინტერნეტ_პროტოკოლი(int დავალება_მნიშვნელობა, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(დავალება_მნიშვნელობა & 0xff), 처리기);
    }

    public void დარეგისტრირება_მომხმარებელი_მონაცემები_გაკვეთილი(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void დარეგისტრირება_გადაცემა_მართვა(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ჩარჩო_ინდექსი) {
        if (!ქსელი_ხელსაწყოები.이더넷틀인가(ჩარჩო_ინდექსი)) {
            return false;
        }
        int 종류 = ქსელი_ხელსაწყოები.이더넷상위규약(ჩარჩო_ინდექსი);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.პროცესი_მნიშვნელობა_შენატანი(ჩარჩო_ინდექსი, 14, ჩარჩო_ინდექსი.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ჩარჩო_ინდექსი, 14);
    }

    private boolean 상호통신망받기(byte[] მონაცემები, int გაშვება) {
        if (!ქსელი_ხელსაწყოები.상호통신망규약사판인가(მონაცემები, გაშვება)) {
            return false;
        }
        int ზედა_კოლონტიტული_სიგრძე = (მონაცემები[გაშვება] & 0x0f) * 4;
        int 전체길이 = ქსელი_ხელსაწყოები.큰순서짧은정수(მონაცემები, გაშვება + 2);
        if (전체길이 < ზედა_კოლონტიტული_სიგრძე || გაშვება + 전체길이 > მონაცემები.length) {
            return false;
        }
        int დავალება_მნიშვნელობა = მონაცემები[გაშვება + 9] & 0xff;
        int შიგთავსი_დაწყება = გაშვება + ზედა_კოლონტიტული_სიგრძე;
        int შიგთავსი_სიგრძე = 전체길이 - ზედა_კოლონტიტული_სიგრძე;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(დავალება_მნიშვნელობა));
        if (직접처리기 != null) {
            직접처리기.პროცესი_მნიშვნელობა_შენატანი(მონაცემები, შიგთავსი_დაწყება, შიგთავსი_სიგრძე);
            return true;
        }
        if (შიგთავსი_სიგრძე < 4) {
            return false;
        }
        int 목적포트 = ქსელი_ხელსაწყოები.큰순서짧은정수(მონაცემები, შიგთავსი_დაწყება + 2);
        Map<Integer, 자료처리기> პორტი_ცხრილი = დავალება_მნიშვნელობა == 17 ? 사용자자료단위처리기 : დავალება_მნიშვნელობა == 6 ? 전송제어처리기 : null;
        if (პორტი_ცხრილი == null) {
            return false;
        }
        자료처리기 포트처리기 = პორტი_ცხრილი.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.პროცესი_მნიშვნელობა_შენატანი(მონაცემები, შიგთავსი_დაწყება, შიგთავსი_სიგრძე);
        return true;
    }
}

