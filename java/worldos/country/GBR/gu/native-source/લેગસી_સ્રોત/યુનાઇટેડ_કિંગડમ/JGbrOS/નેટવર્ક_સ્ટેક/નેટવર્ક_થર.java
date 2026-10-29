// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package યુનાઇટેડ_કિંગડમ.JGbrOS.નેટવર્ક_સ્ટેક;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class નેટવર્ક_થર {
    @FunctionalInterface
    public interface 자료처리기 {
        void પ્રક્રિયા_મૂલ્ય_પ્રવેશ(byte[] ડેટા, int ચલાવો_2, int લંબાઈ_મૂલ્ય);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void રજિસ્ટર_કરો_ઇથરનેટ(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void રજિસ્ટર_કરો_ઇંટરનેટ_પ્રોટોકૉલ(int કામ_મૂલ્ય, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(કામ_મૂલ્ય & 0xff), 처리기);
    }

    public void રજિસ્ટર_કરો_ઉપયોગકર્તા_ડેટા_એકમ(int હાર્ડવેર_પૉર્ટ, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(હાર્ડવેર_પૉર્ટ & 0xffff), 처리기);
    }

    public void રજિસ્ટર_કરો_પ્રસારણ_નિયંત્રણ(int હાર્ડવેર_પૉર્ટ, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(હાર્ડવેર_પૉર્ટ & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ફ્રેમ_અનુક્રમણિકા) {
        if (!નેટવર્ક_ઉપકરણો.ઇન્ટરમિટેંટ_ઇથરનેટ_ફ્રેમ(ફ્રેમ_અનુક્રમણિકા)) {
            return false;
        }
        int 종류 = નેટવર્ક_ઉપકરણો.이더넷상위규약(ફ્રેમ_અનુક્રમણિકા);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.પ્રક્રિયા_મૂલ્ય_પ્રવેશ(ફ્રેમ_અનુક્રમણિકા, 14, ફ્રેમ_અનુક્રમણિકા.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ફ્રેમ_અનુક્રમણિકા, 14);
    }

    private boolean 상호통신망받기(byte[] ડેટા, int ચલાવો_2) {
        if (!નેટવર્ક_ઉપકરણો.상호통신망규약사판인가(ડેટા, ચલાવો_2)) {
            return false;
        }
        int શીર્ષલેખ_લંબાઈ = (ડેટા[ચલાવો_2] & 0x0f) * 4;
        int 전체길이 = નેટવર્ક_ઉપકરણો.큰순서짧은정수(ડેટા, ચલાવો_2 + 2);
        if (전체길이 < શીર્ષલેખ_લંબાઈ || ચલાવો_2 + 전체길이 > ડેટા.length) {
            return false;
        }
        int કામ_મૂલ્ય = ડેટા[ચલાવો_2 + 9] & 0xff;
        int સામગ્રી_પ્રારંભ = ચલાવો_2 + શીર્ષલેખ_લંબાઈ;
        int સામગ્રી_લંબાઈ = 전체길이 - શીર્ષલેખ_લંબાઈ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(કામ_મૂલ્ય));
        if (직접처리기 != null) {
            직접처리기.પ્રક્રિયા_મૂલ્ય_પ્રવેશ(ડેટા, સામગ્રી_પ્રારંભ, સામગ્રી_લંબાઈ);
            return true;
        }
        if (સામગ્રી_લંબાઈ < 4) {
            return false;
        }
        int ગંતવ્ય_પોર્ટ_નંબર = નેટવર્ક_ઉપકરણો.큰순서짧은정수(ડેટા, સામગ્રી_પ્રારંભ + 2);
        Map<Integer, 자료처리기> પૉર્ટ_કોષ્ટક = કામ_મૂલ્ય == 17 ? 사용자자료단위처리기 : કામ_મૂલ્ય == 6 ? 전송제어처리기 : null;
        if (પૉર્ટ_કોષ્ટક == null) {
            return false;
        }
        자료처리기 포트처리기 = પૉર્ટ_કોષ્ટક.get(Integer.valueOf(ગંતવ્ય_પોર્ટ_નંબર));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.પ્રક્રિયા_મૂલ્ય_પ્રવેશ(ડેટા, સામગ્રી_પ્રારંભ, સામગ્રી_લંબાઈ);
        return true;
    }
}

