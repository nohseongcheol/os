// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package फ़िजी.JFjiOS.नेटवर्क_स्टैक;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class नेटवर्क_लेयर {
    @FunctionalInterface
    public interface 자료처리기 {
        void प्रक्रिया_मान_एन्ट्री(byte[] आँकड़े, int चलाएँ, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void रजिस्टर_इंटरनेट_प्रोटोकॉल(int मामला_मान, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(मामला_मान & 0xff), 처리기);
    }

    public void रजिस्टर_उपयोगकर्ता_डेटा_इकाई(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] फ़्रेम_इंडेक्स) {
        if (!नेटवर्क_उपकरण.이더넷틀인가(फ़्रेम_इंडेक्स)) {
            return false;
        }
        int 종류 = नेटवर्क_उपकरण.이더넷상위규약(फ़्रेम_इंडेक्स);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.प्रक्रिया_मान_एन्ट्री(फ़्रेम_इंडेक्स, 14, फ़्रेम_इंडेक्स.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(फ़्रेम_इंडेक्स, 14);
    }

    private boolean 상호통신망받기(byte[] आँकड़े, int चलाएँ) {
        if (!नेटवर्क_उपकरण.상호통신망규약사판인가(आँकड़े, चलाएँ)) {
            return false;
        }
        int 머리길이 = (आँकड़े[चलाएँ] & 0x0f) * 4;
        int 전체길이 = नेटवर्क_उपकरण.큰순서짧은정수(आँकड़े, चलाएँ + 2);
        if (전체길이 < 머리길이 || चलाएँ + 전체길이 > आँकड़े.length) {
            return false;
        }
        int मामला_मान = आँकड़े[चलाएँ + 9] & 0xff;
        int सामग्री_प्रारंभ = चलाएँ + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(मामला_मान));
        if (직접처리기 != null) {
            직접처리기.प्रक्रिया_मान_एन्ट्री(आँकड़े, सामग्री_प्रारंभ, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int गंतव्य_पोर्ट_संख्या = नेटवर्क_उपकरण.큰순서짧은정수(आँकड़े, सामग्री_प्रारंभ + 2);
        Map<Integer, 자료처리기> पोर्ट_तालिका = मामला_मान == 17 ? 사용자자료단위처리기 : मामला_मान == 6 ? 전송제어처리기 : null;
        if (पोर्ट_तालिका == null) {
            return false;
        }
        자료처리기 포트처리기 = पोर्ट_तालिका.get(Integer.valueOf(गंतव्य_पोर्ट_संख्या));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.प्रक्रिया_मान_एन्ट्री(आँकड़े, सामग्री_प्रारंभ, 내용길이);
        return true;
    }
}

