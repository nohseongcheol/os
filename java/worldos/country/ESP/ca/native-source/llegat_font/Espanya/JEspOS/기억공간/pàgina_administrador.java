// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB pàgina_VALOR 연결과 Escriptura 시 복사를 제공한다. */
public final class pàgina_administrador {
    public static final int mida_de_la_pàgina = 4096;

    private static final class pàgina_VALOR {
        private byte[] dades = new byte[mida_de_la_pàgina];
        private int Referència_COMPT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADREÇA_espai {
        private final Map<Integer, pàgina_VALOR> pàgina_taula = new HashMap<Integer, pàgina_VALOR>();
    }

    public ADREÇA_espai 새주소공간() {
        return new ADREÇA_espai();
    }

    public void MAP_pàgina(ADREÇA_espai 공간, int virtual_ADREÇA, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtual_ADREÇA);
        pàgina_VALOR 새쪽 = new pàgina_VALOR();
        새쪽.쓰기가능 = 쓰기가능;
        공간.pàgina_taula.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADREÇA_espai 쓰기시복사복제(ADREÇA_espai 원본) {
        ADREÇA_espai 복제본 = new ADREÇA_espai();
        for (Map.Entry<Integer, pàgina_VALOR> introducció_VALOR : 원본.pàgina_taula.entrySet()) {
            pàgina_VALOR 공유쪽 = introducció_VALOR.getValue();
            공유쪽.Referència_COMPT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.pàgina_taula.put(introducció_VALOR.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte tancar_byte_VALOR(ADREÇA_espai 공간, int virtual_ADREÇA) {
        pàgina_VALOR objectiu = BUSCA_pàgina(공간, virtual_ADREÇA);
        return objectiu.dades[Math.floorMod(virtual_ADREÇA, mida_de_la_pàgina)];
    }

    public void escriure_byte_VALOR(ADREÇA_espai 공간, int virtual_ADREÇA, byte VALOR) {
        int INDEX = 쪽번호(virtual_ADREÇA);
        pàgina_VALOR objectiu = BUSCA_pàgina(공간, virtual_ADREÇA);
        if (!objectiu.쓰기가능) {
            if (!objectiu.쓰기시복사) {
                throw new IllegalStateException("Lectura 전용 쪽입니다.");
            }
            objectiu = Crear_Privat_pàgina(공간, INDEX, objectiu);
        }
        objectiu.dades[Math.floorMod(virtual_ADREÇA, mida_de_la_pàgina)] = VALOR;
    }

    public void Privat_interval_escriure(ADREÇA_espai 공간, int Inici_ADREÇA, int Mida) {
        if (Mida < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int finalitzar_ADREÇA = Math.addExact(Inici_ADREÇA, Mida);
        for (int Adreça = Inici_ADREÇA; Adreça < finalitzar_ADREÇA; Adreça = (쪽번호(Adreça) + 1) * mida_de_la_pàgina) {
            int INDEX = 쪽번호(Adreça);
            pàgina_VALOR objectiu = BUSCA_pàgina(공간, Adreça);
            if (objectiu.쓰기시복사) {
                Crear_Privat_pàgina(공간, INDEX, objectiu);
            } else {
                objectiu.쓰기가능 = true;
            }
        }
    }

    public void interval_escriure(ADREÇA_espai 공간, int Inici_ADREÇA, byte[] dades) {
        for (int INDEX = 0; INDEX < dades.length; INDEX++) {
            escriure_byte_VALOR(공간, Inici_ADREÇA + INDEX, dades[INDEX]);
        }
    }

    private pàgina_VALOR Crear_Privat_pàgina(ADREÇA_espai 공간, int INDEX, pàgina_VALOR 공유쪽) {
        pàgina_VALOR Privat_pàgina = new pàgina_VALOR();
        Privat_pàgina.dades = Arrays.copyOf(공유쪽.dades, 공유쪽.dades.length);
        Privat_pàgina.쓰기가능 = true;
        Privat_pàgina.쓰기시복사 = false;
        공유쪽.Referència_COMPT--;
        공간.pàgina_taula.put(Integer.valueOf(INDEX), Privat_pàgina);
        return Privat_pàgina;
    }

    private pàgina_VALOR BUSCA_pàgina(ADREÇA_espai 공간, int Adreça) {
        pàgina_VALOR objectiu = 공간.pàgina_taula.get(Integer.valueOf(쪽번호(Adreça)));
        if (objectiu == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return objectiu;
    }

    private int 쪽번호(int Adreça) {
        if (Adreça < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return Adreça / mida_de_la_pàgina;
    }
}

