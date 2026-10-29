// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ገጽ_እሴት 연결과 መጻፊያ 시 복사를 제공한다. */
public final class ገጽ_አስተዳዳሪ {
    public static final int የገጽ_መጠን = 4096;

    private static final class ገጽ_እሴት {
        private byte[] ውሂብ = new byte[የገጽ_መጠን];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class አድራሻ_ቦታ {
        private final Map<Integer, ገጽ_እሴት> ገጽ_ሰንጠረዥ = new HashMap<Integer, ገጽ_እሴት>();
    }

    public አድራሻ_ቦታ 새주소공간() {
        return new አድራሻ_ቦታ();
    }

    public void ካርታ_ገጽ(አድራሻ_ቦታ 공간, int ምናባዊ_አድራሻ, boolean 쓰기가능) {
        int መረጃ_ጠቆመ = 쪽번호(ምናባዊ_አድራሻ);
        ገጽ_እሴት 새쪽 = new ገጽ_እሴት();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ገጽ_ሰንጠረዥ.put(Integer.valueOf(መረጃ_ጠቆመ), 새쪽);
    }

    public አድራሻ_ቦታ 쓰기시복사복제(አድራሻ_ቦታ 원본) {
        አድራሻ_ቦታ 복제본 = new አድራሻ_ቦታ();
        for (Map.Entry<Integer, ገጽ_እሴት> ምዝግብ_እሴት : 원본.ገጽ_ሰንጠረዥ.entrySet()) {
            ገጽ_እሴት 공유쪽 = ምዝግብ_እሴት.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ገጽ_ሰንጠረዥ.put(ምዝግብ_እሴት.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(አድራሻ_ቦታ 공간, int ምናባዊ_አድራሻ) {
        ገጽ_እሴት ዓላማ = አግኝ_ገጽ(공간, ምናባዊ_አድራሻ);
        return ዓላማ.ውሂብ[Math.floorMod(ምናባዊ_አድራሻ, የገጽ_መጠን)];
    }

    public void ጻፍ_ባይት_እሴት(አድራሻ_ቦታ 공간, int ምናባዊ_አድራሻ, byte እሴት) {
        int መረጃ_ጠቆመ = 쪽번호(ምናባዊ_አድራሻ);
        ገጽ_እሴት ዓላማ = አግኝ_ገጽ(공간, ምናባዊ_አድራሻ);
        if (!ዓላማ.쓰기가능) {
            if (!ዓላማ.쓰기시복사) {
                throw new IllegalStateException("ማንበቢያ 전용 쪽입니다.");
            }
            ዓላማ = ፍጠር_ግላዊ_ገጽ(공간, መረጃ_ጠቆመ, ዓላማ);
        }
        ዓላማ.ውሂብ[Math.floorMod(ምናባዊ_አድራሻ, የገጽ_መጠን)] = እሴት;
    }

    public void 범위개인쓰기(አድራሻ_ቦታ 공간, int ጀምር_አድራሻ, int መጠን) {
        if (መጠን < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ጨርስ_አድራሻ = Math.addExact(ጀምር_አድራሻ, መጠን);
        for (int አድራሻ = ጀምር_አድራሻ; አድራሻ < ጨርስ_አድራሻ; አድራሻ = (쪽번호(አድራሻ) + 1) * የገጽ_መጠን) {
            int መረጃ_ጠቆመ = 쪽번호(አድራሻ);
            ገጽ_እሴት ዓላማ = አግኝ_ገጽ(공간, አድራሻ);
            if (ዓላማ.쓰기시복사) {
                ፍጠር_ግላዊ_ገጽ(공간, መረጃ_ጠቆመ, ዓላማ);
            } else {
                ዓላማ.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(አድራሻ_ቦታ 공간, int ጀምር_አድራሻ, byte[] ውሂብ) {
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < ውሂብ.length; መረጃ_ጠቆመ++) {
            ጻፍ_ባይት_እሴት(공간, ጀምር_አድራሻ + መረጃ_ጠቆመ, ውሂብ[መረጃ_ጠቆመ]);
        }
    }

    private ገጽ_እሴት ፍጠር_ግላዊ_ገጽ(አድራሻ_ቦታ 공간, int መረጃ_ጠቆመ, ገጽ_እሴት 공유쪽) {
        ገጽ_እሴት ግላዊ_ገጽ = new ገጽ_እሴት();
        ግላዊ_ገጽ.ውሂብ = Arrays.copyOf(공유쪽.ውሂብ, 공유쪽.ውሂብ.length);
        ግላዊ_ገጽ.쓰기가능 = true;
        ግላዊ_ገጽ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ገጽ_ሰንጠረዥ.put(Integer.valueOf(መረጃ_ጠቆመ), ግላዊ_ገጽ);
        return ግላዊ_ገጽ;
    }

    private ገጽ_እሴት አግኝ_ገጽ(አድራሻ_ቦታ 공간, int አድራሻ) {
        ገጽ_እሴት ዓላማ = 공간.ገጽ_ሰንጠረዥ.get(Integer.valueOf(쪽번호(አድራሻ)));
        if (ዓላማ == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ዓላማ;
    }

    private int 쪽번호(int አድራሻ) {
        if (አድራሻ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return አድራሻ / የገጽ_መጠን;
    }
}

