// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ihuakwụkwọ_valuu 연결과 Chekwaa_ozi 시 복사를 제공한다. */
public final class ihuakwụkwọ_njikwa {
    public static final int ụhàrà_ihuakwụkwọ = 4096;

    private static final class ihuakwụkwọ_valuu {
        private byte[] datà = new byte[ụhàrà_ihuakwụkwọ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class àdreèsì_ohere {
        private final Map<Integer, ihuakwụkwọ_valuu> ihuakwụkwọ_tebùl = new HashMap<Integer, ihuakwụkwọ_valuu>();
    }

    public àdreèsì_ohere 새주소공간() {
        return new àdreèsì_ohere();
    }

    public void gosi_na_maapụ_ihuakwụkwọ(àdreèsì_ohere 공간, int adreèsi_ndịnuchè, boolean 쓰기가능) {
        int indèks = 쪽번호(adreèsi_ndịnuchè);
        ihuakwụkwọ_valuu 새쪽 = new ihuakwụkwọ_valuu();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ihuakwụkwọ_tebùl.put(Integer.valueOf(indèks), 새쪽);
    }

    public àdreèsì_ohere 쓰기시복사복제(àdreèsì_ohere 원본) {
        àdreèsì_ohere 복제본 = new àdreèsì_ohere();
        for (Map.Entry<Integer, ihuakwụkwọ_valuu> ndebà_valuu : 원본.ihuakwụkwọ_tebùl.entrySet()) {
            ihuakwụkwọ_valuu 공유쪽 = ndebà_valuu.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ihuakwụkwọ_tebùl.put(ndebà_valuu.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(àdreèsì_ohere 공간, int adreèsi_ndịnuchè) {
        ihuakwụkwọ_valuu ebenlereanya = chọta_ihuakwụkwọ(공간, adreèsi_ndịnuchè);
        return ebenlereanya.datà[Math.floorMod(adreèsi_ndịnuchè, ụhàrà_ihuakwụkwọ)];
    }

    public void dee_baịtị_valuu(àdreèsì_ohere 공간, int adreèsi_ndịnuchè, byte valuu) {
        int indèks = 쪽번호(adreèsi_ndịnuchè);
        ihuakwụkwọ_valuu ebenlereanya = chọta_ihuakwụkwọ(공간, adreèsi_ndịnuchè);
        if (!ebenlereanya.쓰기가능) {
            if (!ebenlereanya.쓰기시복사) {
                throw new IllegalStateException("Wepụta_ọzi 전용 쪽입니다.");
            }
            ebenlereanya = mepụta_keonwē_ihuakwụkwọ(공간, indèks, ebenlereanya);
        }
        ebenlereanya.datà[Math.floorMod(adreèsi_ndịnuchè, ụhàrà_ihuakwụkwọ)] = valuu;
    }

    public void 범위개인쓰기(àdreèsì_ohere 공간, int Mbido_àdreèsì, int Ụhara) {
        if (Ụhara < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int mèdebe_àdreèsì = Math.addExact(Mbido_àdreèsì, Ụhara);
        for (int àdreèsì = Mbido_àdreèsì; àdreèsì < mèdebe_àdreèsì; àdreèsì = (쪽번호(àdreèsì) + 1) * ụhàrà_ihuakwụkwọ) {
            int indèks = 쪽번호(àdreèsì);
            ihuakwụkwọ_valuu ebenlereanya = chọta_ihuakwụkwọ(공간, àdreèsì);
            if (ebenlereanya.쓰기시복사) {
                mepụta_keonwē_ihuakwụkwọ(공간, indèks, ebenlereanya);
            } else {
                ebenlereanya.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(àdreèsì_ohere 공간, int Mbido_àdreèsì, byte[] datà) {
        for (int indèks = 0; indèks < datà.length; indèks++) {
            dee_baịtị_valuu(공간, Mbido_àdreèsì + indèks, datà[indèks]);
        }
    }

    private ihuakwụkwọ_valuu mepụta_keonwē_ihuakwụkwọ(àdreèsì_ohere 공간, int indèks, ihuakwụkwọ_valuu 공유쪽) {
        ihuakwụkwọ_valuu keonwē_ihuakwụkwọ = new ihuakwụkwọ_valuu();
        keonwē_ihuakwụkwọ.datà = Arrays.copyOf(공유쪽.datà, 공유쪽.datà.length);
        keonwē_ihuakwụkwọ.쓰기가능 = true;
        keonwē_ihuakwụkwọ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ihuakwụkwọ_tebùl.put(Integer.valueOf(indèks), keonwē_ihuakwụkwọ);
        return keonwē_ihuakwụkwọ;
    }

    private ihuakwụkwọ_valuu chọta_ihuakwụkwọ(àdreèsì_ohere 공간, int àdreèsì) {
        ihuakwụkwọ_valuu ebenlereanya = 공간.ihuakwụkwọ_tebùl.get(Integer.valueOf(쪽번호(àdreèsì)));
        if (ebenlereanya == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ebenlereanya;
    }

    private int 쪽번호(int àdreèsì) {
        if (àdreèsì < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return àdreèsì / ụhàrà_ihuakwụkwọ;
    }
}

