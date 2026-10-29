// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package কানাডা.JCanOS.নেটওয়ার্ক_গাদা;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class নেটওয়ার্ক_স্তর {
    @FunctionalInterface
    public interface 자료처리기 {
        void প্রসেসর_মান_ভুক্তি(byte[] ডাটা, int চালনা, int দৈর্ঘ্য_মান);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void নিবন্ধন_করুন_ইথারনেট(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void নিবন্ধন_করুন_ইন্টারনেট_প্রটোকল(int কাজ_মান, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(কাজ_মান & 0xff), 처리기);
    }

    public void নিবন্ধন_করুন_ব্যবহারকারী_ডাটা_একক(int হার্ডওয়্যার_পোর্ট, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(হার্ডওয়্যার_পোর্ট & 0xffff), 처리기);
    }

    public void নিবন্ধন_করুন_সঞ্চালন_নিয়ন্ত্রণ(int হার্ডওয়্যার_পোর্ট, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(হার্ডওয়্যার_পোর্ট & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ফ্রেম_সূচি) {
        if (!নেটওয়ার্ক_সরঞ্জামগুলি.তথ্য_প্রযুক্তি_ইথারনেট_ফ্রেম(ফ্রেম_সূচি)) {
            return false;
        }
        int 종류 = নেটওয়ার্ক_সরঞ্জামগুলি.이더넷상위규약(ফ্রেম_সূচি);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.প্রসেসর_মান_ভুক্তি(ফ্রেম_সূচি, 14, ফ্রেম_সূচি.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ফ্রেম_সূচি, 14);
    }

    private boolean 상호통신망받기(byte[] ডাটা, int চালনা) {
        if (!নেটওয়ার্ক_সরঞ্জামগুলি.상호통신망규약사판인가(ডাটা, চালনা)) {
            return false;
        }
        int হেডার_দৈর্ঘ্য = (ডাটা[চালনা] & 0x0f) * 4;
        int 전체길이 = নেটওয়ার্ক_সরঞ্জামগুলি.큰순서짧은정수(ডাটা, চালনা + 2);
        if (전체길이 < হেডার_দৈর্ঘ্য || চালনা + 전체길이 > ডাটা.length) {
            return false;
        }
        int কাজ_মান = ডাটা[চালনা + 9] & 0xff;
        int সামগ্রি_শুরু = চালনা + হেডার_দৈর্ঘ্য;
        int সামগ্রি_দৈর্ঘ্য = 전체길이 - হেডার_দৈর্ঘ্য;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(কাজ_মান));
        if (직접처리기 != null) {
            직접처리기.প্রসেসর_মান_ভুক্তি(ডাটা, সামগ্রি_শুরু, সামগ্রি_দৈর্ঘ্য);
            return true;
        }
        if (সামগ্রি_দৈর্ঘ্য < 4) {
            return false;
        }
        int গন্তব্য_পোর্ট_নম্বর = নেটওয়ার্ক_সরঞ্জামগুলি.큰순서짧은정수(ডাটা, সামগ্রি_শুরু + 2);
        Map<Integer, 자료처리기> পোর্ট_সারণি = কাজ_মান == 17 ? 사용자자료단위처리기 : কাজ_মান == 6 ? 전송제어처리기 : null;
        if (পোর্ট_সারণি == null) {
            return false;
        }
        자료처리기 포트처리기 = পোর্ট_সারণি.get(Integer.valueOf(গন্তব্য_পোর্ট_নম্বর));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.প্রসেসর_মান_ভুক্তি(ডাটা, সামগ্রি_শুরু, সামগ্রি_দৈর্ঘ্য);
        return true;
    }
}

