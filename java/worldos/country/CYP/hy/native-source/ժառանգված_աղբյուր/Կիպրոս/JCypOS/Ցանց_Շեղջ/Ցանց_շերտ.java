// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Կիպրոս.JCypOS.Ցանց_Շեղջ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Ցանց_շերտ {
    @FunctionalInterface
    public interface 자료처리기 {
        void Ընթացք_արժեք_մուտքագրում(byte[] տվյալ, int Գործարկել, int տեւողություն_արժեք);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void գրանցվել_համացանցի_հաղորդակարգ(int գործ_արժեք, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(գործ_արժեք & 0xff), 처리기);
    }

    public void գրանցվել_օգտվող_տվյալ_դասընթաց(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void գրանցվել_փոխանցում_հսկում(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] կադր_դասիչ) {
        if (!Ցանց_Գործիքներ.이더넷틀인가(կադր_դասիչ)) {
            return false;
        }
        int 종류 = Ցանց_Գործիքներ.이더넷상위규약(կադր_դասիչ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Ընթացք_արժեք_մուտքագրում(կադր_դասիչ, 14, կադր_դասիչ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(կադր_դասիչ, 14);
    }

    private boolean 상호통신망받기(byte[] տվյալ, int Գործարկել) {
        if (!Ցանց_Գործիքներ.상호통신망규약사판인가(տվյալ, Գործարկել)) {
            return false;
        }
        int Վերնագիր_տեւողություն = (տվյալ[Գործարկել] & 0x0f) * 4;
        int 전체길이 = Ցանց_Գործիքներ.큰순서짧은정수(տվյալ, Գործարկել + 2);
        if (전체길이 < Վերնագիր_տեւողություն || Գործարկել + 전체길이 > տվյալ.length) {
            return false;
        }
        int գործ_արժեք = տվյալ[Գործարկել + 9] & 0xff;
        int Բովանդակություն_Մեկնարկ = Գործարկել + Վերնագիր_տեւողություն;
        int Բովանդակություն_տեւողություն = 전체길이 - Վերնագիր_տեւողություն;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(գործ_արժեք));
        if (직접처리기 != null) {
            직접처리기.Ընթացք_արժեք_մուտքագրում(տվյալ, Բովանդակություն_Մեկնարկ, Բովանդակություն_տեւողություն);
            return true;
        }
        if (Բովանդակություն_տեւողություն < 4) {
            return false;
        }
        int 목적포트 = Ցանց_Գործիքներ.큰순서짧은정수(տվյալ, Բովանդակություն_Մեկնարկ + 2);
        Map<Integer, 자료처리기> միացք_աղյուսակ = գործ_արժեք == 17 ? 사용자자료단위처리기 : գործ_արժեք == 6 ? 전송제어처리기 : null;
        if (միացք_աղյուսակ == null) {
            return false;
        }
        자료처리기 포트처리기 = միացք_աղյուսակ.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Ընթացք_արժեք_մուտքագրում(տվյալ, Բովանդակություն_Մեկնարկ, Բովանդակություն_տեւողություն);
        return true;
    }
}

