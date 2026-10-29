// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.নেটৱৰ্ক_ষ্টেক;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class নেটৱৰ্ক_তৰপ {
    @FunctionalInterface
    public interface 자료처리기 {
        void প্ৰক্ৰিয়া_মান_প্রবিষ্ট(byte[] ডাটা, int সঞ্চালন, int দৈর্ঘ্য_মান);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void পঞ্জীয়ন_কৰক_ইথাৰনেট(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void পঞ্জীয়ন_কৰক_ইন্টাৰনেট_প্ৰ_ট_ক_ল(int কেছ_মান, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(কেছ_মান & 0xff), 처리기);
    }

    public void পঞ্জীয়ন_কৰক_ব্যৱহাৰকৰ্তা_ডাটা_পাঠ্য(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void পঞ্জীয়ন_কৰক_প্রচাৰণ_নিয়ন্ত্রণ(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ফ্ৰেম_ইনডেক্স) {
        if (!নেটৱৰ্ক_সঁজুলিসমূহ.이더넷틀인가(ফ্ৰেম_ইনডেক্স)) {
            return false;
        }
        int 종류 = নেটৱৰ্ক_সঁজুলিসমূহ.이더넷상위규약(ফ্ৰেম_ইনডেক্স);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.প্ৰক্ৰিয়া_মান_প্রবিষ্ট(ফ্ৰেম_ইনডেক্স, 14, ফ্ৰেম_ইনডেক্স.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ফ্ৰেম_ইনডেক্স, 14);
    }

    private boolean 상호통신망받기(byte[] ডাটা, int সঞ্চালন) {
        if (!নেটৱৰ্ক_সঁজুলিসমূহ.상호통신망규약사판인가(ডাটা, সঞ্চালন)) {
            return false;
        }
        int শিৰো_দৈর্ঘ্য = (ডাটা[সঞ্চালন] & 0x0f) * 4;
        int 전체길이 = নেটৱৰ্ক_সঁজুলিসমূহ.큰순서짧은정수(ডাটা, সঞ্চালন + 2);
        if (전체길이 < শিৰো_দৈর্ঘ্য || সঞ্চালন + 전체길이 > ডাটা.length) {
            return false;
        }
        int কেছ_মান = ডাটা[সঞ্চালন + 9] & 0xff;
        int সামগ্ৰী_আৰম্ভ = সঞ্চালন + শিৰো_দৈর্ঘ্য;
        int সামগ্ৰী_দৈর্ঘ্য = 전체길이 - শিৰো_দৈর্ঘ্য;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(কেছ_মান));
        if (직접처리기 != null) {
            직접처리기.প্ৰক্ৰিয়া_মান_প্রবিষ্ট(ডাটা, সামগ্ৰী_আৰম্ভ, সামগ্ৰী_দৈর্ঘ্য);
            return true;
        }
        if (সামগ্ৰী_দৈর্ঘ্য < 4) {
            return false;
        }
        int 목적포트 = নেটৱৰ্ক_সঁজুলিসমূহ.큰순서짧은정수(ডাটা, সামগ্ৰী_আৰম্ভ + 2);
        Map<Integer, 자료처리기> পৰ্ট_তালিকা = কেছ_মান == 17 ? 사용자자료단위처리기 : কেছ_মান == 6 ? 전송제어처리기 : null;
        if (পৰ্ট_তালিকা == null) {
            return false;
        }
        자료처리기 포트처리기 = পৰ্ট_তালিকা.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.প্ৰক্ৰিয়া_মান_প্রবিষ্ট(ডাটা, সামগ্ৰী_আৰম্ভ, সামগ্ৰী_দৈর্ঘ্য);
        return true;
    }
}

