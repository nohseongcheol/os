// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عراق.JIrqOS.شبکه_پشته;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class شبکه_لایه {
    @FunctionalInterface
    public interface 자료처리기 {
        void فرآیند_مقدار_ورودی(byte[] داده_ها, int اجرا_2, int طول_مقدار);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ثبت_نام_اترنت(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ثبت_نام_پروتکل_اینترنتی(int شغل_مقدار, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(شغل_مقدار & 0xff), 처리기);
    }

    public void ثبت_نام_کاربر_داده_ها_درس(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void ثبت_نام_مخابره_کنترل(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] قاب_فهرست) {
        if (!شبکه_ابزارها.فناوری_اطلاعات_اترنت_قاب(قاب_فهرست)) {
            return false;
        }
        int 종류 = شبکه_ابزارها.이더넷상위규약(قاب_فهرست);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.فرآیند_مقدار_ورودی(قاب_فهرست, 14, قاب_فهرست.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(قاب_فهرست, 14);
    }

    private boolean 상호통신망받기(byte[] داده_ها, int اجرا_2) {
        if (!شبکه_ابزارها.상호통신망규약사판인가(داده_ها, اجرا_2)) {
            return false;
        }
        int سرصفحه_طول = (داده_ها[اجرا_2] & 0x0f) * 4;
        int 전체길이 = شبکه_ابزارها.큰순서짧은정수(داده_ها, اجرا_2 + 2);
        if (전체길이 < سرصفحه_طول || اجرا_2 + 전체길이 > داده_ها.length) {
            return false;
        }
        int شغل_مقدار = داده_ها[اجرا_2 + 9] & 0xff;
        int محتوا_شروع = اجرا_2 + سرصفحه_طول;
        int محتوا_طول = 전체길이 - سرصفحه_طول;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(شغل_مقدار));
        if (직접처리기 != null) {
            직접처리기.فرآیند_مقدار_ورودی(داده_ها, محتوا_شروع, محتوا_طول);
            return true;
        }
        if (محتوا_طول < 4) {
            return false;
        }
        int مقصد_شماره_درگاه = شبکه_ابزارها.큰순서짧은정수(داده_ها, محتوا_شروع + 2);
        Map<Integer, 자료처리기> تبدیل_جدول = شغل_مقدار == 17 ? 사용자자료단위처리기 : شغل_مقدار == 6 ? 전송제어처리기 : null;
        if (تبدیل_جدول == null) {
            return false;
        }
        자료처리기 포트처리기 = تبدیل_جدول.get(Integer.valueOf(مقصد_شماره_درگاه));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.فرآیند_مقدار_ورودی(داده_ها, محتوا_شروع, محتوا_طول);
        return true;
    }
}

