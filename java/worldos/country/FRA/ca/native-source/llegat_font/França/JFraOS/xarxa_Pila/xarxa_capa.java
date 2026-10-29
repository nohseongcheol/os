// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package França.JFraOS.xarxa_Pila;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP rebre_VALOR 분배를 한곳에서 관리한다. */
public final class xarxa_capa {
    @FunctionalInterface
    public interface 자료처리기 {
        void Procés_VALOR_introducció(byte[] dades, int Executa_2, int durada_VALOR);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registrar_se_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registrar_se_IP(int cas_VALOR, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(cas_VALOR & 0xff), 처리기);
    }

    public void registrar_se_usuari_dades_lliçó(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void registrar_se_transmissió_control(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean rebre_Ethernet(byte[] marc_INDEX) {
        if (!xarxa_Eines.tecnologies_de_la_informació_Ethernet_marc(marc_INDEX)) {
            return false;
        }
        int 종류 = xarxa_Eines.Ethernet_MAJUSC_protocol(marc_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Procés_VALOR_introducció(marc_INDEX, 14, marc_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && rebre_núvol_paquet(marc_INDEX, 14);
    }

    private boolean rebre_núvol_paquet(byte[] dades, int Executa_2) {
        if (!xarxa_Eines.상호통신망규약사판인가(dades, Executa_2)) {
            return false;
        }
        int Capçalera_durada = (dades[Executa_2] & 0x0f) * 4;
        int total_durada = xarxa_Eines.큰순서짧은정수(dades, Executa_2 + 2);
        if (total_durada < Capçalera_durada || Executa_2 + total_durada > dades.length) {
            return false;
        }
        int cas_VALOR = dades[Executa_2 + 9] & 0xff;
        int contingut_Inici = Executa_2 + Capçalera_durada;
        int contingut_durada = total_durada - Capçalera_durada;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(cas_VALOR));
        if (직접처리기 != null) {
            직접처리기.Procés_VALOR_introducció(dades, contingut_Inici, contingut_durada);
            return true;
        }
        if (contingut_durada < 4) {
            return false;
        }
        int destinació_número_de_port = xarxa_Eines.큰순서짧은정수(dades, contingut_Inici + 2);
        Map<Integer, 자료처리기> port_taula = cas_VALOR == 17 ? 사용자자료단위처리기 : cas_VALOR == 6 ? 전송제어처리기 : null;
        if (port_taula == null) {
            return false;
        }
        자료처리기 포트처리기 = port_taula.get(Integer.valueOf(destinació_número_de_port));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Procés_VALOR_introducció(dades, contingut_Inici, contingut_durada);
        return true;
    }
}

