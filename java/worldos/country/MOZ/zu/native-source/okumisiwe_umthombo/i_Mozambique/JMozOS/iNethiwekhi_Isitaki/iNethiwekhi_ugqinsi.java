// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Mozambique.JMozOS.iNethiwekhi_Isitaki;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class iNethiwekhi_ugqinsi {
    @FunctionalInterface
    public interface 자료처리기 {
        void Inqubo_inani_okufakwayo(byte[] imininingwane, int Sebenzisa, int ubude_inani);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void bhalisa_i_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void bhalisa_i_IP(int udaba_inani, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(udaba_inani & 0xff), 처리기);
    }

    public void bhalisa_umsebenzisi_imininingwane_isifundo(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void bhalisa_ukuthumela_isilawuli(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] uhlaka_thola_inkomba) {
        if (!iNethiwekhi_Amathuluzi.이더넷틀인가(uhlaka_thola_inkomba)) {
            return false;
        }
        int 종류 = iNethiwekhi_Amathuluzi.이더넷상위규약(uhlaka_thola_inkomba);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Inqubo_inani_okufakwayo(uhlaka_thola_inkomba, 14, uhlaka_thola_inkomba.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(uhlaka_thola_inkomba, 14);
    }

    private boolean 상호통신망받기(byte[] imininingwane, int Sebenzisa) {
        if (!iNethiwekhi_Amathuluzi.상호통신망규약사판인가(imininingwane, Sebenzisa)) {
            return false;
        }
        int Unhlokweni_ubude = (imininingwane[Sebenzisa] & 0x0f) * 4;
        int 전체길이 = iNethiwekhi_Amathuluzi.큰순서짧은정수(imininingwane, Sebenzisa + 2);
        if (전체길이 < Unhlokweni_ubude || Sebenzisa + 전체길이 > imininingwane.length) {
            return false;
        }
        int udaba_inani = imininingwane[Sebenzisa + 9] & 0xff;
        int Okuqukethwe_qala = Sebenzisa + Unhlokweni_ubude;
        int Okuqukethwe_ubude = 전체길이 - Unhlokweni_ubude;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(udaba_inani));
        if (직접처리기 != null) {
            직접처리기.Inqubo_inani_okufakwayo(imininingwane, Okuqukethwe_qala, Okuqukethwe_ubude);
            return true;
        }
        if (Okuqukethwe_ubude < 4) {
            return false;
        }
        int 목적포트 = iNethiwekhi_Amathuluzi.큰순서짧은정수(imininingwane, Okuqukethwe_qala + 2);
        Map<Integer, 자료처리기> intuba_ithebula = udaba_inani == 17 ? 사용자자료단위처리기 : udaba_inani == 6 ? 전송제어처리기 : null;
        if (intuba_ithebula == null) {
            return false;
        }
        자료처리기 포트처리기 = intuba_ithebula.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Inqubo_inani_okufakwayo(imininingwane, Okuqukethwe_qala, Okuqukethwe_ubude);
        return true;
    }
}

