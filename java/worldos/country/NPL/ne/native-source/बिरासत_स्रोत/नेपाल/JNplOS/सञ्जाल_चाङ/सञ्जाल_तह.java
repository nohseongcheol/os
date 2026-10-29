// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.सञ्जाल_चाङ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class सञ्जाल_तह {
    @FunctionalInterface
    public interface 자료처리기 {
        void प्रक्रिया_मान_प्रविष्टि(byte[] लगत, int चलाउनुहोस्, int लम्बाइ_मान);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void दर्ता_इथरनेट(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void दर्ता_आइपी(int केस_मान, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(केस_मान & 0xff), 처리기);
    }

    public void दर्ता_प्रयोगकर्ता_लगत_शिक्षा(int हार्डवेयर_पोर्ट, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(हार्डवेयर_पोर्ट & 0xffff), 처리기);
    }

    public void दर्ता_प्रसारण_नियन्त्रण(int हार्डवेयर_पोर्ट, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(हार्डवेयर_पोर्ट & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] फ्रेम_अनुक्रमणिका) {
        if (!सञ्जाल_उपकरणहरू.이더넷틀인가(फ्रेम_अनुक्रमणिका)) {
            return false;
        }
        int 종류 = सञ्जाल_उपकरणहरू.이더넷상위규약(फ्रेम_अनुक्रमणिका);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.प्रक्रिया_मान_प्रविष्टि(फ्रेम_अनुक्रमणिका, 14, फ्रेम_अनुक्रमणिका.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(फ्रेम_अनुक्रमणिका, 14);
    }

    private boolean 상호통신망받기(byte[] लगत, int चलाउनुहोस्) {
        if (!सञ्जाल_उपकरणहरू.상호통신망규약사판인가(लगत, चलाउनुहोस्)) {
            return false;
        }
        int हेडर_लम्बाइ = (लगत[चलाउनुहोस्] & 0x0f) * 4;
        int 전체길이 = सञ्जाल_उपकरणहरू.큰순서짧은정수(लगत, चलाउनुहोस् + 2);
        if (전체길이 < हेडर_लम्बाइ || चलाउनुहोस् + 전체길이 > लगत.length) {
            return false;
        }
        int केस_मान = लगत[चलाउनुहोस् + 9] & 0xff;
        int सामग्री_सुरु = चलाउनुहोस् + हेडर_लम्बाइ;
        int सामग्री_लम्बाइ = 전체길이 - हेडर_लम्बाइ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(केस_मान));
        if (직접처리기 != null) {
            직접처리기.प्रक्रिया_मान_प्रविष्टि(लगत, सामग्री_सुरु, सामग्री_लम्बाइ);
            return true;
        }
        if (सामग्री_लम्बाइ < 4) {
            return false;
        }
        int 목적포트 = सञ्जाल_उपकरणहरू.큰순서짧은정수(लगत, सामग्री_सुरु + 2);
        Map<Integer, 자료처리기> पोर्ट_तालिका = केस_मान == 17 ? 사용자자료단위처리기 : केस_मान == 6 ? 전송제어처리기 : null;
        if (पोर्ट_तालिका == null) {
            return false;
        }
        자료처리기 포트처리기 = पोर्ट_तालिका.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.प्रक्रिया_मान_प्रविष्टि(लगत, सामग्री_सुरु, सामग्री_लम्बाइ);
        return true;
    }
}

