// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਭਾਰਤ.JIndOS.ਨੈਟਵਰਕ_ਸਟੈਕ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ਨੈਟਵਰਕ_ਲੇਅਰ {
    @FunctionalInterface
    public interface 자료처리기 {
        void ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ(byte[] ਸਮੱਗਰੀ, int ਚਲਾਓ_2, int ਲੰਬਾਈ_ਕੀਮਤ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ਰਜਿਸਟਰ_ਕਰੋ_ਈਥਰਨੈਟ(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ਰਜਿਸਟਰ_ਕਰੋ_ਇੰਟਰਨੈਟ_ਪ੍ਰੋਟੋਕੋਲ(int ਕੰਮ_ਕੀਮਤ, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ਕੰਮ_ਕੀਮਤ & 0xff), 처리기);
    }

    public void ਰਜਿਸਟਰ_ਕਰੋ_ਉਪਭੋਗਤਾ_ਸਮੱਗਰੀ_ਪਾਠ(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void ਰਜਿਸਟਰ_ਕਰੋ_ਪ੍ਰਸਾਰਣ_ਨਿਯੰਤਰਣ(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ਖਾਕਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        if (!ਨੈਟਵਰਕ_ਸਾਧਨ.이더넷틀인가(ਖਾਕਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ)) {
            return false;
        }
        int 종류 = ਨੈਟਵਰਕ_ਸਾਧਨ.이더넷상위규약(ਖਾਕਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ(ਖਾਕਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ, 14, ਖਾਕਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ਖਾਕਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ, 14);
    }

    private boolean 상호통신망받기(byte[] ਸਮੱਗਰੀ, int ਚਲਾਓ_2) {
        if (!ਨੈਟਵਰਕ_ਸਾਧਨ.상호통신망규약사판인가(ਸਮੱਗਰੀ, ਚਲਾਓ_2)) {
            return false;
        }
        int ਸਿਰਲੇਖ_ਲੰਬਾਈ = (ਸਮੱਗਰੀ[ਚਲਾਓ_2] & 0x0f) * 4;
        int 전체길이 = ਨੈਟਵਰਕ_ਸਾਧਨ.큰순서짧은정수(ਸਮੱਗਰੀ, ਚਲਾਓ_2 + 2);
        if (전체길이 < ਸਿਰਲੇਖ_ਲੰਬਾਈ || ਚਲਾਓ_2 + 전체길이 > ਸਮੱਗਰੀ.length) {
            return false;
        }
        int ਕੰਮ_ਕੀਮਤ = ਸਮੱਗਰੀ[ਚਲਾਓ_2 + 9] & 0xff;
        int ਤਤਕਰਾ_ਸੁਰੂ = ਚਲਾਓ_2 + ਸਿਰਲੇਖ_ਲੰਬਾਈ;
        int ਤਤਕਰਾ_ਲੰਬਾਈ = 전체길이 - ਸਿਰਲੇਖ_ਲੰਬਾਈ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ਕੰਮ_ਕੀਮਤ));
        if (직접처리기 != null) {
            직접처리기.ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ(ਸਮੱਗਰੀ, ਤਤਕਰਾ_ਸੁਰੂ, ਤਤਕਰਾ_ਲੰਬਾਈ);
            return true;
        }
        if (ਤਤਕਰਾ_ਲੰਬਾਈ < 4) {
            return false;
        }
        int 목적포트 = ਨੈਟਵਰਕ_ਸਾਧਨ.큰순서짧은정수(ਸਮੱਗਰੀ, ਤਤਕਰਾ_ਸੁਰੂ + 2);
        Map<Integer, 자료처리기> ਪੋਰਟ_ਤਾਲਿਕਾ = ਕੰਮ_ਕੀਮਤ == 17 ? 사용자자료단위처리기 : ਕੰਮ_ਕੀਮਤ == 6 ? 전송제어처리기 : null;
        if (ਪੋਰਟ_ਤਾਲਿਕਾ == null) {
            return false;
        }
        자료처리기 포트처리기 = ਪੋਰਟ_ਤਾਲਿਕਾ.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ(ਸਮੱਗਰੀ, ਤਤਕਰਾ_ਸੁਰੂ, ਤਤਕਰਾ_ਲੰਬਾਈ);
        return true;
    }
}

