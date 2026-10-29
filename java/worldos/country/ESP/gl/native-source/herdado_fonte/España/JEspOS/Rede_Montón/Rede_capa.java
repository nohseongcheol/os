// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.Rede_Montón;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Rede_capa {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proceso_VALOR_introdución(byte[] datos, int Executar_2, int duración_VALOR);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void rexistrarse_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void rexistrarse_IP(int caso_VALOR, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(caso_VALOR & 0xff), 처리기);
    }

    public void rexistrarse_usuario_datos_lección(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void rexistrarse_transmisión_control(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] marco_ÍNDICE) {
        if (!Rede_Ferramentas.Tecnoloxía_da_información_TI_Ethernet_marco(marco_ÍNDICE)) {
            return false;
        }
        int 종류 = Rede_Ferramentas.Ethernet_MAIÚSCULA_protocolo(marco_ÍNDICE);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proceso_VALOR_introdución(marco_ÍNDICE, 14, marco_ÍNDICE.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(marco_ÍNDICE, 14);
    }

    private boolean 상호통신망받기(byte[] datos, int Executar_2) {
        if (!Rede_Ferramentas.상호통신망규약사판인가(datos, Executar_2)) {
            return false;
        }
        int Cabeceira_duración = (datos[Executar_2] & 0x0f) * 4;
        int 전체길이 = Rede_Ferramentas.큰순서짧은정수(datos, Executar_2 + 2);
        if (전체길이 < Cabeceira_duración || Executar_2 + 전체길이 > datos.length) {
            return false;
        }
        int caso_VALOR = datos[Executar_2 + 9] & 0xff;
        int Contido_START = Executar_2 + Cabeceira_duración;
        int Contido_duración = 전체길이 - Cabeceira_duración;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(caso_VALOR));
        if (직접처리기 != null) {
            직접처리기.Proceso_VALOR_introdución(datos, Contido_START, Contido_duración);
            return true;
        }
        if (Contido_duración < 4) {
            return false;
        }
        int destino_número_do_porto = Rede_Ferramentas.큰순서짧은정수(datos, Contido_START + 2);
        Map<Integer, 자료처리기> porto_táboa = caso_VALOR == 17 ? 사용자자료단위처리기 : caso_VALOR == 6 ? 전송제어처리기 : null;
        if (porto_táboa == null) {
            return false;
        }
        자료처리기 포트처리기 = porto_táboa.get(Integer.valueOf(destino_número_do_porto));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proceso_VALOR_introdución(datos, Contido_START, Contido_duración);
        return true;
    }
}

