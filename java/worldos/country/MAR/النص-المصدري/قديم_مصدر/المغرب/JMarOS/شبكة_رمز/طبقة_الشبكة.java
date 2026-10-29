// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package المغرب.JMarOS.شبكة_رمز;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP يستلم_قيمة 분배를 한곳에서 관리한다. */
public final class طبقة_الشبكة {
    @FunctionalInterface
    public interface 자료처리기 {
        void عملية_قيمة_إدخال(byte[] بيانات, int تشغيل, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void سجل_بروتوكول_الإنترنت(int قيمة_العقد, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(قيمة_العقد & 0xff), 처리기);
    }

    public void سجل_مستخدم_بيانات_درس(int أجهزة_منفذ, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(أجهزة_منفذ & 0xffff), 처리기);
    }

    public void 전송제어등록(int أجهزة_منفذ, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(أجهزة_منفذ & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] شكل_فهرس) {
        if (!شبكة_أدوات.이더넷틀인가(شكل_فهرس)) {
            return false;
        }
        int 종류 = شبكة_أدوات.이더넷상위규약(شكل_فهرس);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.عملية_قيمة_إدخال(شكل_فهرس, 14, شكل_فهرس.length - 14);
            return true;
        }
        return 종류 == 0x0800 && يستلم_سحابة_حزمة(شكل_فهرس, 14);
    }

    private boolean يستلم_سحابة_حزمة(byte[] بيانات, int تشغيل) {
        if (!شبكة_أدوات.أنظمة_المعلومات_لقاح_شلل_الأطفال_4_بروتوكول(بيانات, تشغيل)) {
            return false;
        }
        int 머리길이 = (بيانات[تشغيل] & 0x0f) * 4;
        int 전체길이 = شبكة_أدوات.큰순서짧은정수(بيانات, تشغيل + 2);
        if (전체길이 < 머리길이 || تشغيل + 전체길이 > بيانات.length) {
            return false;
        }
        int قيمة_العقد = بيانات[تشغيل + 9] & 0xff;
        int محتوى_بدء = تشغيل + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(قيمة_العقد));
        if (직접처리기 != null) {
            직접처리기.عملية_قيمة_إدخال(بيانات, محتوى_بدء, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int وجهة_رقم_المنفذ = شبكة_أدوات.큰순서짧은정수(بيانات, محتوى_بدء + 2);
        Map<Integer, 자료처리기> منفذ_جدول = قيمة_العقد == 17 ? 사용자자료단위처리기 : قيمة_العقد == 6 ? 전송제어처리기 : null;
        if (منفذ_جدول == null) {
            return false;
        }
        자료처리기 포트처리기 = منفذ_جدول.get(Integer.valueOf(وجهة_رقم_المنفذ));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.عملية_قيمة_إدخال(بيانات, محتوى_بدء, 내용길이);
        return true;
    }
}

