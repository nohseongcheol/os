// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ELesotho.JLsoOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ikhasi_ixabiso 연결과 Bhala 시 복사를 제공한다. */
public final class ikhasi_umphathi {
    public static final int ubungakanani_bekhasi = 4096;

    private static final class ikhasi_ixabiso {
        private byte[] iingcombolo = new byte[ubungakanani_bekhasi];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class idilesi_isithuba {
        private final Map<Integer, ikhasi_ixabiso> ikhasi_itheyibhile = new HashMap<Integer, ikhasi_ixabiso>();
    }

    public idilesi_isithuba 새주소공간() {
        return new idilesi_isithuba();
    }

    public void beka_emephini_ikhasi(idilesi_isithuba 공간, int idilesi_enembonakalo_yenyani, boolean 쓰기가능) {
        int indeksa = 쪽번호(idilesi_enembonakalo_yenyani);
        ikhasi_ixabiso 새쪽 = new ikhasi_ixabiso();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ikhasi_itheyibhile.put(Integer.valueOf(indeksa), 새쪽);
    }

    public idilesi_isithuba 쓰기시복사복제(idilesi_isithuba 원본) {
        idilesi_isithuba 복제본 = new idilesi_isithuba();
        for (Map.Entry<Integer, ikhasi_ixabiso> ufako_nkcukacha_ixabiso : 원본.ikhasi_itheyibhile.entrySet()) {
            ikhasi_ixabiso 공유쪽 = ufako_nkcukacha_ixabiso.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ikhasi_itheyibhile.put(ufako_nkcukacha_ixabiso.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(idilesi_isithuba 공간, int idilesi_enembonakalo_yenyani) {
        ikhasi_ixabiso ithagethi = fumana_ikhasi(공간, idilesi_enembonakalo_yenyani);
        return ithagethi.iingcombolo[Math.floorMod(idilesi_enembonakalo_yenyani, ubungakanani_bekhasi)];
    }

    public void bhala_ibhayithi_ixabiso(idilesi_isithuba 공간, int idilesi_enembonakalo_yenyani, byte ixabiso) {
        int indeksa = 쪽번호(idilesi_enembonakalo_yenyani);
        ikhasi_ixabiso ithagethi = fumana_ikhasi(공간, idilesi_enembonakalo_yenyani);
        if (!ithagethi.쓰기가능) {
            if (!ithagethi.쓰기시복사) {
                throw new IllegalStateException("Funda 전용 쪽입니다.");
            }
            ithagethi = yila_yabucala_ikhasi(공간, indeksa, ithagethi);
        }
        ithagethi.iingcombolo[Math.floorMod(idilesi_enembonakalo_yenyani, ubungakanani_bekhasi)] = ixabiso;
    }

    public void 범위개인쓰기(idilesi_isithuba 공간, int qala_idilesi, int Ubukhulu) {
        if (Ubukhulu < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int phela_idilesi = Math.addExact(qala_idilesi, Ubukhulu);
        for (int idilesi = qala_idilesi; idilesi < phela_idilesi; idilesi = (쪽번호(idilesi) + 1) * ubungakanani_bekhasi) {
            int indeksa = 쪽번호(idilesi);
            ikhasi_ixabiso ithagethi = fumana_ikhasi(공간, idilesi);
            if (ithagethi.쓰기시복사) {
                yila_yabucala_ikhasi(공간, indeksa, ithagethi);
            } else {
                ithagethi.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(idilesi_isithuba 공간, int qala_idilesi, byte[] iingcombolo) {
        for (int indeksa = 0; indeksa < iingcombolo.length; indeksa++) {
            bhala_ibhayithi_ixabiso(공간, qala_idilesi + indeksa, iingcombolo[indeksa]);
        }
    }

    private ikhasi_ixabiso yila_yabucala_ikhasi(idilesi_isithuba 공간, int indeksa, ikhasi_ixabiso 공유쪽) {
        ikhasi_ixabiso yabucala_ikhasi = new ikhasi_ixabiso();
        yabucala_ikhasi.iingcombolo = Arrays.copyOf(공유쪽.iingcombolo, 공유쪽.iingcombolo.length);
        yabucala_ikhasi.쓰기가능 = true;
        yabucala_ikhasi.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ikhasi_itheyibhile.put(Integer.valueOf(indeksa), yabucala_ikhasi);
        return yabucala_ikhasi;
    }

    private ikhasi_ixabiso fumana_ikhasi(idilesi_isithuba 공간, int idilesi) {
        ikhasi_ixabiso ithagethi = 공간.ikhasi_itheyibhile.get(Integer.valueOf(쪽번호(idilesi)));
        if (ithagethi == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ithagethi;
    }

    private int 쪽번호(int idilesi) {
        if (idilesi < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return idilesi / ubungakanani_bekhasi;
    }
}

