// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB page_VALUE 연결과 sumulat 시 복사를 제공한다. */
public final class page_tagapamahala {
    public static final int laki_ng_pahina = 4096;

    private static final class page_VALUE {
        private byte[] data = new byte[laki_ng_pahina];
        private int Sanggunian_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class email_SPACE {
        private final Map<Integer, page_VALUE> page_talahanayan = new HashMap<Integer, page_VALUE>();
    }

    public email_SPACE 새주소공간() {
        return new email_SPACE();
    }

    public void MAP_page(email_SPACE 공간, int birtuwal_na_adres, boolean 쓰기가능) {
        int INDEX = 쪽번호(birtuwal_na_adres);
        page_VALUE 새쪽 = new page_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.page_talahanayan.put(Integer.valueOf(INDEX), 새쪽);
    }

    public email_SPACE 쓰기시복사복제(email_SPACE 원본) {
        email_SPACE 복제본 = new email_SPACE();
        for (Map.Entry<Integer, page_VALUE> pagpasok_VALUE : 원본.page_talahanayan.entrySet()) {
            page_VALUE 공유쪽 = pagpasok_VALUE.getValue();
            공유쪽.Sanggunian_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.page_talahanayan.put(pagpasok_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(email_SPACE 공간, int birtuwal_na_adres) {
        page_VALUE layunin = FIND_page(공간, birtuwal_na_adres);
        return layunin.data[Math.floorMod(birtuwal_na_adres, laki_ng_pahina)];
    }

    public void sumulat_byte_VALUE(email_SPACE 공간, int birtuwal_na_adres, byte VALUE) {
        int INDEX = 쪽번호(birtuwal_na_adres);
        page_VALUE layunin = FIND_page(공간, birtuwal_na_adres);
        if (!layunin.쓰기가능) {
            if (!layunin.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            layunin = Create_Pribado_page(공간, INDEX, layunin);
        }
        layunin.data[Math.floorMod(birtuwal_na_adres, laki_ng_pahina)] = VALUE;
    }

    public void 범위개인쓰기(email_SPACE 공간, int Start_email, int sukat_82232621) {
        if (sukat_82232621 < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int tapusin_email = Math.addExact(Start_email, sukat_82232621);
        for (int email = Start_email; email < tapusin_email; email = (쪽번호(email) + 1) * laki_ng_pahina) {
            int INDEX = 쪽번호(email);
            page_VALUE layunin = FIND_page(공간, email);
            if (layunin.쓰기시복사) {
                Create_Pribado_page(공간, INDEX, layunin);
            } else {
                layunin.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(email_SPACE 공간, int Start_email, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            sumulat_byte_VALUE(공간, Start_email + INDEX, data[INDEX]);
        }
    }

    private page_VALUE Create_Pribado_page(email_SPACE 공간, int INDEX, page_VALUE 공유쪽) {
        page_VALUE Pribado_page = new page_VALUE();
        Pribado_page.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        Pribado_page.쓰기가능 = true;
        Pribado_page.쓰기시복사 = false;
        공유쪽.Sanggunian_COUNT--;
        공간.page_talahanayan.put(Integer.valueOf(INDEX), Pribado_page);
        return Pribado_page;
    }

    private page_VALUE FIND_page(email_SPACE 공간, int email) {
        page_VALUE layunin = 공간.page_talahanayan.get(Integer.valueOf(쪽번호(email)));
        if (layunin == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return layunin;
    }

    private int 쪽번호(int email) {
        if (email < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return email / laki_ng_pahina;
    }
}

