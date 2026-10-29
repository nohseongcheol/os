// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB paġna_VALUE 연결과 kiteb 시 복사를 제공한다. */
public final class paġna_maniġer {
    public static final int daqs_tal_paġna = 4096;

    private static final class paġna_VALUE {
        private byte[] data = new byte[daqs_tal_paġna];
        private int Referenza_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_SPACE {
        private final Map<Integer, paġna_VALUE> paġna_tabella = new HashMap<Integer, paġna_VALUE>();
    }

    public ADDRESS_SPACE 새주소공간() {
        return new ADDRESS_SPACE();
    }

    public void MAP_paġna(ADDRESS_SPACE 공간, int indirizz_virtwali, boolean 쓰기가능) {
        int INDEX = 쪽번호(indirizz_virtwali);
        paġna_VALUE 새쪽 = new paġna_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.paġna_tabella.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_SPACE 쓰기시복사복제(ADDRESS_SPACE 원본) {
        ADDRESS_SPACE 복제본 = new ADDRESS_SPACE();
        for (Map.Entry<Integer, paġna_VALUE> entrata_VALUE : 원본.paġna_tabella.entrySet()) {
            paġna_VALUE 공유쪽 = entrata_VALUE.getValue();
            공유쪽.Referenza_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.paġna_tabella.put(entrata_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_SPACE 공간, int indirizz_virtwali) {
        paġna_VALUE mira = sab_paġna(공간, indirizz_virtwali);
        return mira.data[Math.floorMod(indirizz_virtwali, daqs_tal_paġna)];
    }

    public void kiteb_byte_VALUE(ADDRESS_SPACE 공간, int indirizz_virtwali, byte VALUE) {
        int INDEX = 쪽번호(indirizz_virtwali);
        paġna_VALUE mira = sab_paġna(공간, indirizz_virtwali);
        if (!mira.쓰기가능) {
            if (!mira.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            mira = ħalaq_privat_paġna(공간, INDEX, mira);
        }
        mira.data[Math.floorMod(indirizz_virtwali, daqs_tal_paġna)] = VALUE;
    }

    public void 범위개인쓰기(ADDRESS_SPACE 공간, int Bidu_ADDRESS, int daqqas) {
        if (daqqas < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ttermina_ADDRESS = Math.addExact(Bidu_ADDRESS, daqqas);
        for (int ADDRESS = Bidu_ADDRESS; ADDRESS < ttermina_ADDRESS; ADDRESS = (쪽번호(ADDRESS) + 1) * daqs_tal_paġna) {
            int INDEX = 쪽번호(ADDRESS);
            paġna_VALUE mira = sab_paġna(공간, ADDRESS);
            if (mira.쓰기시복사) {
                ħalaq_privat_paġna(공간, INDEX, mira);
            } else {
                mira.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ADDRESS_SPACE 공간, int Bidu_ADDRESS, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            kiteb_byte_VALUE(공간, Bidu_ADDRESS + INDEX, data[INDEX]);
        }
    }

    private paġna_VALUE ħalaq_privat_paġna(ADDRESS_SPACE 공간, int INDEX, paġna_VALUE 공유쪽) {
        paġna_VALUE privat_paġna = new paġna_VALUE();
        privat_paġna.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        privat_paġna.쓰기가능 = true;
        privat_paġna.쓰기시복사 = false;
        공유쪽.Referenza_COUNT--;
        공간.paġna_tabella.put(Integer.valueOf(INDEX), privat_paġna);
        return privat_paġna;
    }

    private paġna_VALUE sab_paġna(ADDRESS_SPACE 공간, int ADDRESS) {
        paġna_VALUE mira = 공간.paġna_tabella.get(Integer.valueOf(쪽번호(ADDRESS)));
        if (mira == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return mira;
    }

    private int 쪽번호(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / daqs_tal_paġna;
    }
}

