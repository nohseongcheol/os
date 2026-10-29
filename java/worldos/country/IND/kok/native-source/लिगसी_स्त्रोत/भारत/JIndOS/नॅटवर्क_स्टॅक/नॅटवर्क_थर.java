// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.नॅटवर्क_स्टॅक;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class नॅटवर्क_थर {
    @FunctionalInterface
    public interface 자료처리기 {
        void प्रक्रिया_मोल_प्रवेश(byte[] डेटा, int चलोवप, int लांबाय_मोल);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void नोंदणी_इथरनॅट(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void नोंदणी_IP(int काम_मोल, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(काम_मोल & 0xff), 처리기);
    }

    public void नोंदणी_उपेगकर्तो_डेटा_एकक(int हार्डवॅर_पोर्ट, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(हार्डवॅर_पोर्ट & 0xffff), 처리기);
    }

    public void नोंदणी_प्रसारण_नियंत्रण(int हार्डवॅर_पोर्ट, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(हार्डवॅर_पोर्ट & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] फ्रेम_INDEX) {
        if (!नॅटवर्क_साधनां.이더넷틀인가(फ्रेम_INDEX)) {
            return false;
        }
        int 종류 = नॅटवर्क_साधनां.इथरनॅट_UPPER_प्रोटोकॉल(फ्रेम_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.प्रक्रिया_मोल_प्रवेश(फ्रेम_INDEX, 14, फ्रेम_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(फ्रेम_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] डेटा, int चलोवप) {
        if (!नॅटवर्क_साधनां.상호통신망규약사판인가(डेटा, चलोवप)) {
            return false;
        }
        int माथाळो_लांबाय = (डेटा[चलोवप] & 0x0f) * 4;
        int 전체길이 = नॅटवर्क_साधनां.큰순서짧은정수(डेटा, चलोवप + 2);
        if (전체길이 < माथाळो_लांबाय || चलोवप + 전체길이 > डेटा.length) {
            return false;
        }
        int काम_मोल = डेटा[चलोवप + 9] & 0xff;
        int अनुक्रमणिका_Start = चलोवप + माथाळो_लांबाय;
        int अनुक्रमणिका_लांबाय = 전체길이 - माथाळो_लांबाय;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(काम_मोल));
        if (직접처리기 != null) {
            직접처리기.प्रक्रिया_मोल_प्रवेश(डेटा, अनुक्रमणिका_Start, अनुक्रमणिका_लांबाय);
            return true;
        }
        if (अनुक्रमणिका_लांबाय < 4) {
            return false;
        }
        int 목적포트 = नॅटवर्क_साधनां.큰순서짧은정수(डेटा, अनुक्रमणिका_Start + 2);
        Map<Integer, 자료처리기> पोर्ट_तकटो = काम_मोल == 17 ? 사용자자료단위처리기 : काम_मोल == 6 ? 전송제어처리기 : null;
        if (पोर्ट_तकटो == null) {
            return false;
        }
        자료처리기 포트처리기 = पोर्ट_तकटो.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.प्रक्रिया_मोल_प्रवेश(डेटा, अनुक्रमणिका_Start, अनुक्रमणिका_लांबाय);
        return true;
    }
}

