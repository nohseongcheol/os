// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package இந்தியா.JIndOS.பிணையம்_அடுக்கு_49fba3da;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class பிணையம்_அடுக்கு {
    @FunctionalInterface
    public interface 자료처리기 {
        void செயலகம்_மதிப்பு_உள்ளீடு(byte[] தரவு, int செயல்படுத்துக, int நீளம்_மதிப்பு);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void பதிவு_செய்_ஈத்தர்நெட்(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void பதிவு_செய்_இன்டர்நெட்_புரோட்டோகால்(int வேலை_மதிப்பு_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(வேலை_மதிப்பு_102996da & 0xff), 처리기);
    }

    public void பதிவு_செய்_பயனர்_தரவு_பாடம்(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void பதிவு_செய்_தரவுப்பரிமாற்றம்_கட்டுப்பாடு(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ஃபிரேம்_அடைவு) {
        if (!பிணையம்_கருவிகள்.தகவல்_தொழில்நுட்பம்_ஈத்தர்நெட்_ஃபிரேம்(ஃபிரேம்_அடைவு)) {
            return false;
        }
        int 종류 = பிணையம்_கருவிகள்.이더넷상위규약(ஃபிரேம்_அடைவு);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.செயலகம்_மதிப்பு_உள்ளீடு(ஃபிரேம்_அடைவு, 14, ஃபிரேம்_அடைவு.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ஃபிரேம்_அடைவு, 14);
    }

    private boolean 상호통신망받기(byte[] தரவு, int செயல்படுத்துக) {
        if (!பிணையம்_கருவிகள்.상호통신망규약사판인가(தரவு, செயல்படுத்துக)) {
            return false;
        }
        int மேற்குறிப்பு_நீளம் = (தரவு[செயல்படுத்துக] & 0x0f) * 4;
        int 전체길이 = பிணையம்_கருவிகள்.큰순서짧은정수(தரவு, செயல்படுத்துக + 2);
        if (전체길이 < மேற்குறிப்பு_நீளம் || செயல்படுத்துக + 전체길이 > தரவு.length) {
            return false;
        }
        int வேலை_மதிப்பு_102996da = தரவு[செயல்படுத்துக + 9] & 0xff;
        int உள்ளடக்கம்_தொடங்கு = செயல்படுத்துக + மேற்குறிப்பு_நீளம்;
        int உள்ளடக்கம்_நீளம் = 전체길이 - மேற்குறிப்பு_நீளம்;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(வேலை_மதிப்பு_102996da));
        if (직접처리기 != null) {
            직접처리기.செயலகம்_மதிப்பு_உள்ளீடு(தரவு, உள்ளடக்கம்_தொடங்கு, உள்ளடக்கம்_நீளம்);
            return true;
        }
        if (உள்ளடக்கம்_நீளம் < 4) {
            return false;
        }
        int இலக்கு_முனைய_எண் = பிணையம்_கருவிகள்.큰순서짧은정수(தரவு, உள்ளடக்கம்_தொடங்கு + 2);
        Map<Integer, 자료처리기> முணையம்_அட்டவணை = வேலை_மதிப்பு_102996da == 17 ? 사용자자료단위처리기 : வேலை_மதிப்பு_102996da == 6 ? 전송제어처리기 : null;
        if (முணையம்_அட்டவணை == null) {
            return false;
        }
        자료처리기 포트처리기 = முணையம்_அட்டவணை.get(Integer.valueOf(இலக்கு_முனைய_எண்));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.செயலகம்_மதிப்பு_உள்ளீடு(தரவு, உள்ளடக்கம்_தொடங்கு, உள்ளடக்கம்_நீளம்);
        return true;
    }
}

