// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB páxina_VALOR 연결과 Escritura 시 복사를 제공한다. */
public final class páxina_xefe {
    public static final int tamaño_da_páxina = 4096;

    private static final class páxina_VALOR {
        private byte[] datos = new byte[tamaño_da_páxina];
        private int Material_de_referencia_CONTAR = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ENDEREZO_espazo {
        private final Map<Integer, páxina_VALOR> páxina_táboa = new HashMap<Integer, páxina_VALOR>();
    }

    public ENDEREZO_espazo 새주소공간() {
        return new ENDEREZO_espazo();
    }

    public void MAP_páxina(ENDEREZO_espazo 공간, int enderezo_virtual, boolean 쓰기가능) {
        int ÍNDICE = 쪽번호(enderezo_virtual);
        páxina_VALOR 새쪽 = new páxina_VALOR();
        새쪽.쓰기가능 = 쓰기가능;
        공간.páxina_táboa.put(Integer.valueOf(ÍNDICE), 새쪽);
    }

    public ENDEREZO_espazo 쓰기시복사복제(ENDEREZO_espazo 원본) {
        ENDEREZO_espazo 복제본 = new ENDEREZO_espazo();
        for (Map.Entry<Integer, páxina_VALOR> introdución_VALOR : 원본.páxina_táboa.entrySet()) {
            páxina_VALOR 공유쪽 = introdución_VALOR.getValue();
            공유쪽.Material_de_referencia_CONTAR++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.páxina_táboa.put(introdución_VALOR.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ENDEREZO_espazo 공간, int enderezo_virtual) {
        páxina_VALOR obxectivo_VALOR = Busca_páxina(공간, enderezo_virtual);
        return obxectivo_VALOR.datos[Math.floorMod(enderezo_virtual, tamaño_da_páxina)];
    }

    public void escribir_byte_VALOR(ENDEREZO_espazo 공간, int enderezo_virtual, byte VALOR) {
        int ÍNDICE = 쪽번호(enderezo_virtual);
        páxina_VALOR obxectivo_VALOR = Busca_páxina(공간, enderezo_virtual);
        if (!obxectivo_VALOR.쓰기가능) {
            if (!obxectivo_VALOR.쓰기시복사) {
                throw new IllegalStateException("Lectura 전용 쪽입니다.");
            }
            obxectivo_VALOR = crear_Privado_páxina(공간, ÍNDICE, obxectivo_VALOR);
        }
        obxectivo_VALOR.datos[Math.floorMod(enderezo_virtual, tamaño_da_páxina)] = VALOR;
    }

    public void Privado_intervalo_escribir(ENDEREZO_espazo 공간, int START_ENDEREZO, int Tamaño) {
        if (Tamaño < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int finalizar_ENDEREZO = Math.addExact(START_ENDEREZO, Tamaño);
        for (int ENDEREZO = START_ENDEREZO; ENDEREZO < finalizar_ENDEREZO; ENDEREZO = (쪽번호(ENDEREZO) + 1) * tamaño_da_páxina) {
            int ÍNDICE = 쪽번호(ENDEREZO);
            páxina_VALOR obxectivo_VALOR = Busca_páxina(공간, ENDEREZO);
            if (obxectivo_VALOR.쓰기시복사) {
                crear_Privado_páxina(공간, ÍNDICE, obxectivo_VALOR);
            } else {
                obxectivo_VALOR.쓰기가능 = true;
            }
        }
    }

    public void intervalo_escribir(ENDEREZO_espazo 공간, int START_ENDEREZO, byte[] datos) {
        for (int ÍNDICE = 0; ÍNDICE < datos.length; ÍNDICE++) {
            escribir_byte_VALOR(공간, START_ENDEREZO + ÍNDICE, datos[ÍNDICE]);
        }
    }

    private páxina_VALOR crear_Privado_páxina(ENDEREZO_espazo 공간, int ÍNDICE, páxina_VALOR 공유쪽) {
        páxina_VALOR Privado_páxina = new páxina_VALOR();
        Privado_páxina.datos = Arrays.copyOf(공유쪽.datos, 공유쪽.datos.length);
        Privado_páxina.쓰기가능 = true;
        Privado_páxina.쓰기시복사 = false;
        공유쪽.Material_de_referencia_CONTAR--;
        공간.páxina_táboa.put(Integer.valueOf(ÍNDICE), Privado_páxina);
        return Privado_páxina;
    }

    private páxina_VALOR Busca_páxina(ENDEREZO_espazo 공간, int ENDEREZO) {
        páxina_VALOR obxectivo_VALOR = 공간.páxina_táboa.get(Integer.valueOf(쪽번호(ENDEREZO)));
        if (obxectivo_VALOR == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return obxectivo_VALOR;
    }

    private int 쪽번호(int ENDEREZO) {
        if (ENDEREZO < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ENDEREZO / tamaño_da_páxina;
    }
}

