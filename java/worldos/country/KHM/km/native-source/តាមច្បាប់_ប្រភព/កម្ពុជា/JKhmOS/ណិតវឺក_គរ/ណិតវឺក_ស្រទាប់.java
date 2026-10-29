// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ណិតវឺក_គរ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ណិតវឺក_ស្រទាប់ {
    @FunctionalInterface
    public interface 자료처리기 {
        void ដំណើរការ_តំលៃ_ការបញ្ចូល(byte[] ទិន្នន័យ, int រត់, int ប្រវែង_តំលៃ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ចុះឈ្មោះ_អ៊ីនធឺណិតប្រូតូកូល(int ករណី_តំលៃ, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ករណី_តំលៃ & 0xff), 처리기);
    }

    public void ចុះឈ្មោះ_អ្នកប្រើ_ទិន្នន័យ_ឯកតា(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void ចុះឈ្មោះ_ការបញ្ជូន_អង្គបញ្ជា(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] រូប_សន្ទស្សន៏) {
        if (!ណិតវឺក_ឧបករណ៍.이더넷틀인가(រូប_សន្ទស្សន៏)) {
            return false;
        }
        int 종류 = ណិតវឺក_ឧបករណ៍.이더넷상위규약(រូប_សន្ទស្សន៏);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ដំណើរការ_តំលៃ_ការបញ្ចូល(រូប_សន្ទស្សន៏, 14, រូប_សន្ទស្សន៏.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(រូប_សន្ទស្សន៏, 14);
    }

    private boolean 상호통신망받기(byte[] ទិន្នន័យ, int រត់) {
        if (!ណិតវឺក_ឧបករណ៍.상호통신망규약사판인가(ទិន្នន័យ, រត់)) {
            return false;
        }
        int បឋមកថា_ប្រវែង = (ទិន្នន័យ[រត់] & 0x0f) * 4;
        int 전체길이 = ណិតវឺក_ឧបករណ៍.큰순서짧은정수(ទិន្នន័យ, រត់ + 2);
        if (전체길이 < បឋមកថា_ប្រវែង || រត់ + 전체길이 > ទិន្នន័យ.length) {
            return false;
        }
        int ករណី_តំលៃ = ទិន្នន័យ[រត់ + 9] & 0xff;
        int មាតិកា_ផ្តើម = រត់ + បឋមកថា_ប្រវែង;
        int មាតិកា_ប្រវែង = 전체길이 - បឋមកថា_ប្រវែង;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ករណី_តំលៃ));
        if (직접처리기 != null) {
            직접처리기.ដំណើរការ_តំលៃ_ការបញ្ចូល(ទិន្នន័យ, មាតិកា_ផ្តើម, មាតិកា_ប្រវែង);
            return true;
        }
        if (មាតិកា_ប្រវែង < 4) {
            return false;
        }
        int ទិសដៅ_លេខរន្ធ = ណិតវឺក_ឧបករណ៍.큰순서짧은정수(ទិន្នន័យ, មាតិកា_ផ្តើម + 2);
        Map<Integer, 자료처리기> ច្រក_តារាង = ករណី_តំលៃ == 17 ? 사용자자료단위처리기 : ករណី_តំលៃ == 6 ? 전송제어처리기 : null;
        if (ច្រក_តារាង == null) {
            return false;
        }
        자료처리기 포트처리기 = ច្រក_តារាង.get(Integer.valueOf(ទិសដៅ_លេខរន្ធ));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ដំណើរការ_តំលៃ_ការបញ្ចូល(ទិន្នន័យ, មាតិកា_ផ្តើម, មាតិកា_ប្រវែង);
        return true;
    }
}

