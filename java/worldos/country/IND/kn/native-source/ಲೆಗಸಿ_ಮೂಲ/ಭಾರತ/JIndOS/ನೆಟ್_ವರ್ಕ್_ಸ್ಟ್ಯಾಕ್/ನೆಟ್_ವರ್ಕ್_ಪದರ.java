// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ನೆಟ್_ವರ್ಕ್_ಪದರ {
    @FunctionalInterface
    public interface 자료처리기 {
        void ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು(byte[] ಡೇಟಾ, int ಚಲಾಯಿಸು_2, int ಉದ್ದ_ಮೌಲ್ಯ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ನೋಂದಾಯಿಸು_ಇಥರ್ನೆಟ್(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ನೋಂದಾಯಿಸು_ಇಂಟರ್ನೆಟ್_ಪ್ರೊಟೋಕಾಲ್(int ಕೆಲಸ_ಮೌಲ್ಯ, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ಕೆಲಸ_ಮೌಲ್ಯ & 0xff), 처리기);
    }

    public void ನೋಂದಾಯಿಸು_ಬಳಕೆದಾರ_ಡೇಟಾ_ಅಧ್ಯಯನ(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void ನೋಂದಾಯಿಸು_ಪ್ರಸಾರ_ನಿಯಂತ್ರಣ(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ಫ್ರೇಮ್_ಪದಸೂಚಿ) {
        if (!ನೆಟ್_ವರ್ಕ್_ಪರಿಕರಗಳು.ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಇಥರ್ನೆಟ್_ಫ್ರೇಮ್(ಫ್ರೇಮ್_ಪದಸೂಚಿ)) {
            return false;
        }
        int 종류 = ನೆಟ್_ವರ್ಕ್_ಪರಿಕರಗಳು.이더넷상위규약(ಫ್ರೇಮ್_ಪದಸೂಚಿ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು(ಫ್ರೇಮ್_ಪದಸೂಚಿ, 14, ಫ್ರೇಮ್_ಪದಸೂಚಿ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ಫ್ರೇಮ್_ಪದಸೂಚಿ, 14);
    }

    private boolean 상호통신망받기(byte[] ಡೇಟಾ, int ಚಲಾಯಿಸು_2) {
        if (!ನೆಟ್_ವರ್ಕ್_ಪರಿಕರಗಳು.상호통신망규약사판인가(ಡೇಟಾ, ಚಲಾಯಿಸು_2)) {
            return false;
        }
        int ಶಿರೋಲೇಖ_ಉದ್ದ = (ಡೇಟಾ[ಚಲಾಯಿಸು_2] & 0x0f) * 4;
        int 전체길이 = ನೆಟ್_ವರ್ಕ್_ಪರಿಕರಗಳು.큰순서짧은정수(ಡೇಟಾ, ಚಲಾಯಿಸು_2 + 2);
        if (전체길이 < ಶಿರೋಲೇಖ_ಉದ್ದ || ಚಲಾಯಿಸು_2 + 전체길이 > ಡೇಟಾ.length) {
            return false;
        }
        int ಕೆಲಸ_ಮೌಲ್ಯ = ಡೇಟಾ[ಚಲಾಯಿಸು_2 + 9] & 0xff;
        int ವಿಷಯ_ಆರಂಭಿಸು = ಚಲಾಯಿಸು_2 + ಶಿರೋಲೇಖ_ಉದ್ದ;
        int ವಿಷಯ_ಉದ್ದ = 전체길이 - ಶಿರೋಲೇಖ_ಉದ್ದ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ಕೆಲಸ_ಮೌಲ್ಯ));
        if (직접처리기 != null) {
            직접처리기.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು(ಡೇಟಾ, ವಿಷಯ_ಆರಂಭಿಸು, ವಿಷಯ_ಉದ್ದ);
            return true;
        }
        if (ವಿಷಯ_ಉದ್ದ < 4) {
            return false;
        }
        int ಗಮ್ಯಸ್ಥಾನ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = ನೆಟ್_ವರ್ಕ್_ಪರಿಕರಗಳು.큰순서짧은정수(ಡೇಟಾ, ವಿಷಯ_ಆರಂಭಿಸು + 2);
        Map<Integer, 자료처리기> ಪೋರ್ಟ್_ಕೋಷ್ಟಕ = ಕೆಲಸ_ಮೌಲ್ಯ == 17 ? 사용자자료단위처리기 : ಕೆಲಸ_ಮೌಲ್ಯ == 6 ? 전송제어처리기 : null;
        if (ಪೋರ್ಟ್_ಕೋಷ್ಟಕ == null) {
            return false;
        }
        자료처리기 포트처리기 = ಪೋರ್ಟ್_ಕೋಷ್ಟಕ.get(Integer.valueOf(ಗಮ್ಯಸ್ಥಾನ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು(ಡೇಟಾ, ವಿಷಯ_ಆರಂಭಿಸು, ವಿಷಯ_ಉದ್ದ);
        return true;
    }
}

