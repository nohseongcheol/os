// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package افغانستان.JAfgOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB مخ_ارزښت 연결과 لوستل_2 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int 쪽크기 = 4096;

    private static final class مخ_ارزښت {
        private byte[] اومتوک = new byte[쪽크기];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class پته_تشې_پټۍ {
        private final Map<Integer, مخ_ارزښت> مخ_لښتيال = new HashMap<Integer, مخ_ارزښت>();
    }

    public پته_تشې_پټۍ 새주소공간() {
        return new پته_تشې_پټۍ();
    }

    public void 쪽연결(پته_تشې_پټۍ 공간, int نېغه_پته, boolean 쓰기가능) {
        int لړیال = 쪽번호(نېغه_پته);
        مخ_ارزښت 새쪽 = new مخ_ارزښت();
        새쪽.쓰기가능 = 쓰기가능;
        공간.مخ_لښتيال.put(Integer.valueOf(لړیال), 새쪽);
    }

    public پته_تشې_پټۍ 쓰기시복사복제(پته_تشې_پټۍ 원본) {
        پته_تشې_پټۍ 복제본 = new پته_تشې_پټۍ();
        for (Map.Entry<Integer, مخ_ارزښت> ننوت_ارزښت : 원본.مخ_لښتيال.entrySet()) {
            مخ_ارزښت 공유쪽 = ننوت_ارزښت.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.مخ_لښتيال.put(ننوت_ارزښت.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(پته_تشې_پټۍ 공간, int نېغه_پته) {
        مخ_ارزښت 대상 = 쪽찾기(공간, نېغه_پته);
        return 대상.اومتوک[Math.floorMod(نېغه_پته, 쪽크기)];
    }

    public void ليکل_بايټ_ارزښت(پته_تشې_پټۍ 공간, int نېغه_پته, byte ارزښت) {
        int لړیال = 쪽번호(نېغه_پته);
        مخ_ارزښت 대상 = 쪽찾기(공간, نېغه_پته);
        if (!대상.쓰기가능) {
            if (!대상.쓰기시복사) {
                throw new IllegalStateException("لوستل 전용 쪽입니다.");
            }
            대상 = 개인쪽만들기(공간, لړیال, 대상);
        }
        대상.اومتوک[Math.floorMod(نېغه_پته, 쪽크기)] = ارزښت;
    }

    public void 범위개인쓰기(پته_تشې_پټۍ 공간, int پيل_پته, int کچ) {
        if (کچ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int پاى_پته = Math.addExact(پيل_پته, کچ);
        for (int پته = پيل_پته; پته < پاى_پته; پته = (쪽번호(پته) + 1) * 쪽크기) {
            int لړیال = 쪽번호(پته);
            مخ_ارزښت 대상 = 쪽찾기(공간, پته);
            if (대상.쓰기시복사) {
                개인쪽만들기(공간, لړیال, 대상);
            } else {
                대상.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(پته_تشې_پټۍ 공간, int پيل_پته, byte[] اومتوک) {
        for (int لړیال = 0; لړیال < اومتوک.length; لړیال++) {
            ليکل_بايټ_ارزښت(공간, پيل_پته + لړیال, اومتوک[لړیال]);
        }
    }

    private مخ_ارزښت 개인쪽만들기(پته_تشې_پټۍ 공간, int لړیال, مخ_ارزښت 공유쪽) {
        مخ_ارزښت ځاني_مخ = new مخ_ارزښت();
        ځاني_مخ.اومتوک = Arrays.copyOf(공유쪽.اومتوک, 공유쪽.اومتوک.length);
        ځاني_مخ.쓰기가능 = true;
        ځاني_مخ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.مخ_لښتيال.put(Integer.valueOf(لړیال), ځاني_مخ);
        return ځاني_مخ;
    }

    private مخ_ارزښت 쪽찾기(پته_تشې_پټۍ 공간, int پته) {
        مخ_ارزښت 대상 = 공간.مخ_لښتيال.get(Integer.valueOf(쪽번호(پته)));
        if (대상 == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return 대상;
    }

    private int 쪽번호(int پته) {
        if (پته < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return پته / 쪽크기;
    }
}

