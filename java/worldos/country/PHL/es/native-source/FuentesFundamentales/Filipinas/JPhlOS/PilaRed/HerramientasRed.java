// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Filipinas.JPhlOS.PilaRed;

/** Herramientas de orden de bytes y suma de comprobación compartidas por las capas Ethernet/ARP/IPv4/ICMP/UDP. */
public final class HerramientasRed {
    private HerramientasRed() {
    }

    public static int cortoOrdenBytesGrande(byte[] Datos, int posición) {
        comprobarRango(Datos, posición, 2);
        return ((Datos[posición] & 0xff) << 8) | (Datos[posición + 1] & 0xff);
    }

    public static long enteroValorOrdenBytesGrande(byte[] Datos, int posición) {
        comprobarRango(Datos, posición, 4);
        return ((long) (Datos[posición] & 0xff) << 24)
                | ((long) (Datos[posición + 1] & 0xff) << 16)
                | ((long) (Datos[posición + 2] & 0xff) << 8)
                | (Datos[posición + 3] & 0xffL);
    }

    public static int sumaComprobaciónInternet(byte[] Datos, int ponerEnMarcha, int longitud) {
        comprobarRango(Datos, ponerEnMarcha, longitud);
        long valorTotalSuma = 0;
        int terminación = ponerEnMarcha + longitud;
        int posición = ponerEnMarcha;
        while (posición + 1 < terminación) {
            valorTotalSuma += cortoOrdenBytesGrande(Datos, posición);
            posición += 2;
        }
        if (posición < terminación) {
            valorTotalSuma += (Datos[posición] & 0xff) << 8;
        }
        while ((valorTotalSuma >>> 16) != 0) {
            valorTotalSuma = (valorTotalSuma & 0xffff) + (valorTotalSuma >>> 16);
        }
        return (int) (~valorTotalSuma) & 0xffff;
    }

    public static boolean esMarcoEthernet(byte[] Datos) {
        return Datos != null && Datos.length >= 14;
    }

    public static int protocoloSuperiorEthernet(byte[] Datos) {
        if (!esMarcoEthernet(Datos)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return cortoOrdenBytesGrande(Datos, 12);
    }

    public static boolean esProtocolo4VersiónIP(byte[] Datos, int posición) {
        if (Datos == null || posición < 0 || Datos.length - posición < 20) {
            return false;
        }
        int valorVersión = (Datos[posición] >>> 4) & 0xf;
        int longitudEncabezado = (Datos[posición] & 0xf) * 4;
        return valorVersión == 4 && longitudEncabezado >= 20 && Datos.length - posición >= longitudEncabezado;
    }

    private static void comprobarRango(byte[] Datos, int ponerEnMarcha, int longitud) {
        if (Datos == null || ponerEnMarcha < 0 || longitud < 0 || ponerEnMarcha > Datos.length - longitud) {
            throw new IllegalArgumentException("PilaRed Datos 범위를 벗어났습니다.");
        }
    }
}

