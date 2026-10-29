// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Uruguay.JUryOS.PilaRed;

import java.util.HashMap;
import java.util.Map;

/** Centraliza la distribución de recepción de Ethernet, ARP, IPv4, ICMP, UDP y TCP. */
public final class CapaRed {
    @FunctionalInterface
    public interface manejadorEventoDatos {
        void entradaElementoValorProceso(byte[] Datos, int ponerEnMarcha, int longitud);
    }

    private final Map<Integer, manejadorEventoDatos> ManejadorEventoEthernet = new HashMap<Integer, manejadorEventoDatos>();
    private final Map<Integer, manejadorEventoDatos> ManejadorEventoProtocoloInternet = new HashMap<Integer, manejadorEventoDatos>();
    private final Map<Integer, manejadorEventoDatos> manejadorEventoUnidadDatosUsuario = new HashMap<Integer, manejadorEventoDatos>();
    private final Map<Integer, manejadorEventoDatos> ManejadorEventoControlTransmisión = new HashMap<Integer, manejadorEventoDatos>();

    public void registroEthernet(int valorClaseTipo, manejadorEventoDatos ManejadorEvento) {
        ManejadorEventoEthernet.put(Integer.valueOf(valorClaseTipo & 0xffff), ManejadorEvento);
    }

    public void registroProtocoloInternet(int valorContrato, manejadorEventoDatos ManejadorEvento) {
        ManejadorEventoProtocoloInternet.put(Integer.valueOf(valorContrato & 0xff), ManejadorEvento);
    }

    public void registroUnidadDatosUsuario(int puertoEquipoFísico, manejadorEventoDatos ManejadorEvento) {
        manejadorEventoUnidadDatosUsuario.put(Integer.valueOf(puertoEquipoFísico & 0xffff), ManejadorEvento);
    }

    public void registroControlTransmisión(int puertoEquipoFísico, manejadorEventoDatos ManejadorEvento) {
        ManejadorEventoControlTransmisión.put(Integer.valueOf(puertoEquipoFísico & 0xffff), ManejadorEvento);
    }

    public boolean recibirEthernet(byte[] índiceMarco) {
        if (!HerramientasRed.esMarcoEthernet(índiceMarco)) {
            return false;
        }
        int valorClaseTipo = HerramientasRed.protocoloSuperiorEthernet(índiceMarco);
        manejadorEventoDatos ManejadorEventoDirecto = ManejadorEventoEthernet.get(Integer.valueOf(valorClaseTipo));
        if (ManejadorEventoDirecto != null) {
            ManejadorEventoDirecto.entradaElementoValorProceso(índiceMarco, 14, índiceMarco.length - 14);
            return true;
        }
        return valorClaseTipo == 0x0800 && recibirPaqueteDatosInternet(índiceMarco, 14);
    }

    private boolean recibirPaqueteDatosInternet(byte[] Datos, int ponerEnMarcha) {
        if (!HerramientasRed.esProtocolo4VersiónIP(Datos, ponerEnMarcha)) {
            return false;
        }
        int longitudEncabezado = (Datos[ponerEnMarcha] & 0x0f) * 4;
        int longitudTotal = HerramientasRed.cortoOrdenBytesGrande(Datos, ponerEnMarcha + 2);
        if (longitudTotal < longitudEncabezado || ponerEnMarcha + longitudTotal > Datos.length) {
            return false;
        }
        int valorContrato = Datos[ponerEnMarcha + 9] & 0xff;
        int iniciarContenidoValor = ponerEnMarcha + longitudEncabezado;
        int longitudContenidoValor = longitudTotal - longitudEncabezado;
        manejadorEventoDatos ManejadorEventoDirecto = ManejadorEventoProtocoloInternet.get(Integer.valueOf(valorContrato));
        if (ManejadorEventoDirecto != null) {
            ManejadorEventoDirecto.entradaElementoValorProceso(Datos, iniciarContenidoValor, longitudContenidoValor);
            return true;
        }
        if (longitudContenidoValor < 4) {
            return false;
        }
        int númeroPuertoDestino = HerramientasRed.cortoOrdenBytesGrande(Datos, iniciarContenidoValor + 2);
        Map<Integer, manejadorEventoDatos> tablaPuerto = valorContrato == 17 ? manejadorEventoUnidadDatosUsuario : valorContrato == 6 ? ManejadorEventoControlTransmisión : null;
        if (tablaPuerto == null) {
            return false;
        }
        manejadorEventoDatos manejadorEventoPuerto = tablaPuerto.get(Integer.valueOf(númeroPuertoDestino));
        if (manejadorEventoPuerto == null) {
            return false;
        }
        manejadorEventoPuerto.entradaElementoValorProceso(Datos, iniciarContenidoValor, longitudContenidoValor);
        return true;
    }
}

