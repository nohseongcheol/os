// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.መረብ_ክምር;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class መረብ_ንብርብር {
    @FunctionalInterface
    public interface 자료처리기 {
        void ሂደት_እሴት_ምዝግብ(byte[] ውሂብ, int ማስኬጃ, int ርዝመት_እሴት);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void መዝግብ_ኢተርኔት(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void መዝግብ_የበይነመረብ_ፕሮቶኮል(int ስራ_እሴት_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ስራ_እሴት_102996da & 0xff), 처리기);
    }

    public void መዝግብ_ተጠቃሚ_ውሂብ_አሀዶች(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void መዝግብ_ትልልፍ_ቁጥጥር(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ማዕቀፍ_መረጃ_ጠቆመ) {
        if (!መረብ_መሳሪያዎች.የመረጃ_ቴክኖሎጂ_ኢተርኔት_ማዕቀፍ(ማዕቀፍ_መረጃ_ጠቆመ)) {
            return false;
        }
        int 종류 = መረብ_መሳሪያዎች.이더넷상위규약(ማዕቀፍ_መረጃ_ጠቆመ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ሂደት_እሴት_ምዝግብ(ማዕቀፍ_መረጃ_ጠቆመ, 14, ማዕቀፍ_መረጃ_ጠቆመ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ማዕቀፍ_መረጃ_ጠቆመ, 14);
    }

    private boolean 상호통신망받기(byte[] ውሂብ, int ማስኬጃ) {
        if (!መረብ_መሳሪያዎች.상호통신망규약사판인가(ውሂብ, ማስኬጃ)) {
            return false;
        }
        int ርእስ_ርዝመት = (ውሂብ[ማስኬጃ] & 0x0f) * 4;
        int 전체길이 = መረብ_መሳሪያዎች.큰순서짧은정수(ውሂብ, ማስኬጃ + 2);
        if (전체길이 < ርእስ_ርዝመት || ማስኬጃ + 전체길이 > ውሂብ.length) {
            return false;
        }
        int ስራ_እሴት_102996da = ውሂብ[ማስኬጃ + 9] & 0xff;
        int ይዘት_ጀምር = ማስኬጃ + ርእስ_ርዝመት;
        int ይዘት_ርዝመት = 전체길이 - ርእስ_ርዝመት;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ስራ_እሴት_102996da));
        if (직접처리기 != null) {
            직접처리기.ሂደት_እሴት_ምዝግብ(ውሂብ, ይዘት_ጀምር, ይዘት_ርዝመት);
            return true;
        }
        if (ይዘት_ርዝመት < 4) {
            return false;
        }
        int መድረሻ_የወደብ_ቁጥር = መረብ_መሳሪያዎች.큰순서짧은정수(ውሂብ, ይዘት_ጀምር + 2);
        Map<Integer, 자료처리기> ወደብ_ሰንጠረዥ = ስራ_እሴት_102996da == 17 ? 사용자자료단위처리기 : ስራ_እሴት_102996da == 6 ? 전송제어처리기 : null;
        if (ወደብ_ሰንጠረዥ == null) {
            return false;
        }
        자료처리기 포트처리기 = ወደብ_ሰንጠረዥ.get(Integer.valueOf(መድረሻ_የወደብ_ቁጥር));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ሂደት_እሴት_ምዝግብ(ውሂብ, ይዘት_ጀምር, ይዘት_ርዝመት);
        return true;
    }
}

