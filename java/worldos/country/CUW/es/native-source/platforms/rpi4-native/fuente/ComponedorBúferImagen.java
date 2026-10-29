// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Gestiona recorte, composición de franjas y fondo bajo el puntero. El código de la placa accede a la memoria de pantalla real. */
public final class ComponedorBúferImagen {
    static int valorAnchura, valorAltura, esComposiciónEnCurso, valorFronteraIzquierdo, fronteraSuperior, valorFronteraDerecho, valorFronteraInferior;
    static int coordenadaHorizontalPuntero, coordenadaVerticalPuntero, formaPuntero;
    static int bajoContador, altoContador;
    static int[] píxelesCompuesto = new int[32 * 1920];
    static int[] fondoPuntero = new int[21 * 21];
    static int[] límitesRecortado = new int[4];
    public static void preparar(int extensiónRangoAnchura, int longitud) {
        valorAnchura = extensiónRangoAnchura; valorAltura = longitud; esComposiciónEnCurso = 0; formaPuntero = 0;
        bajoContador = 0; altoContador = 0;
    }
    public static int obtenerAnchura() { return valorAnchura; }
    public static int obtenerAltura() { return valorAltura; }
    public static int obtenerBajoContador() { return bajoContador; }
    public static int obtenerAltoContador() { return altoContador; }
    public static int valorRecortar(int índiceOrdinal) { return límitesRecortado[índiceOrdinal]; }
    static int añadirLongitudPositivo(int iniciarValor, int longitud) {
        if (iniciarValor > 2147483647 - longitud) return 2147483647;
        return iniciarValor + longitud;
    }
    public static int recortar(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int longitud) {
        if (valorAnchura == 0 || extensiónRangoAnchura <= 0 || longitud <= 0) return 0;
        int derecho = añadirLongitudPositivo(posiciónHorizontal, extensiónRangoAnchura), ladoInferior = añadirLongitudPositivo(posiciónVertical, longitud);
        int ladoIzquierdo = esComposiciónEnCurso != 0 ? valorFronteraIzquierdo : 0, ladoSuperior = esComposiciónEnCurso != 0 ? fronteraSuperior : 0;
        int posiciónHorizontalMáximo = esComposiciónEnCurso != 0 ? valorFronteraDerecho : valorAnchura, posiciónVerticalMáximo = esComposiciónEnCurso != 0 ? valorFronteraInferior : valorAltura;
        if (posiciónHorizontal < ladoIzquierdo) posiciónHorizontal = ladoIzquierdo;
        if (posiciónVertical < ladoSuperior) posiciónVertical = ladoSuperior;
        if (derecho > posiciónHorizontalMáximo) derecho = posiciónHorizontalMáximo;
        if (ladoInferior > posiciónVerticalMáximo) ladoInferior = posiciónVerticalMáximo;
        if (derecho <= posiciónHorizontal || ladoInferior <= posiciónVertical) return 0;
        límitesRecortado[0] = posiciónHorizontal; límitesRecortado[1] = posiciónVertical;
        límitesRecortado[2] = derecho - posiciónHorizontal; límitesRecortado[3] = ladoInferior - posiciónVertical;
        return 1;
    }
    public static int ponerEnMarcha(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int longitud) {
        if (esComposiciónEnCurso != 0 || longitud > 32 || recortar(posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, longitud) == 0) return 0;
        valorFronteraIzquierdo = límitesRecortado[0]; fronteraSuperior = límitesRecortado[1];
        valorFronteraDerecho = valorFronteraIzquierdo + límitesRecortado[2]; valorFronteraInferior = fronteraSuperior + límitesRecortado[3];
        esComposiciónEnCurso = 1; return 1;
    }
    static boolean bitPuntero(int posiciónHorizontal, int posiciónVertical, int valorForma) {
        if (valorForma == 1) return posiciónHorizontal >= 0 && posiciónHorizontal <= posiciónVertical / 2 && posiciónVertical < 16;
        if (valorForma == 3) posiciónHorizontal = 20 - posiciónHorizontal;
        int valorDiferencia = posiciónHorizontal - posiciónVertical; if (valorDiferencia < 0) valorDiferencia = -valorDiferencia;
        return (valorDiferencia <= 1 && posiciónHorizontal >= 3 && posiciónHorizontal <= 17) ||
            (posiciónHorizontal >= 2 && posiciónHorizontal <= 8 && posiciónVertical >= 2 && posiciónVertical <= 8 && (posiciónHorizontal <= 3 || posiciónVertical <= 3)) ||
            (posiciónHorizontal >= 12 && posiciónHorizontal <= 18 && posiciónVertical >= 12 && posiciónVertical <= 18 && (posiciónHorizontal >= 17 || posiciónVertical >= 17));
    }
    static int píxelPuntero(int posiciónHorizontal, int posiciónVertical) {
        if (bitPuntero(posiciónHorizontal, posiciónVertical, formaPuntero)) return 2;
        for (int línea = -1; línea <= 1; línea++) for (int entradaElementoRanura = -1; entradaElementoRanura <= 1; entradaElementoRanura++)
            if (bitPuntero(posiciónHorizontal + entradaElementoRanura, posiciónVertical + línea, formaPuntero)) return 1;
        return 0;
    }
    static void píxelPresentar(int posiciónHorizontal, int posiciónVertical, int valorColor) {
        int entradaElementoRanura = posiciónHorizontal - coordenadaHorizontalPuntero, línea = posiciónVertical - coordenadaVerticalPuntero;
        if (formaPuntero != 0 && entradaElementoRanura >= 0 && línea >= 0 && entradaElementoRanura < 21 && línea < 21) {
            fondoPuntero[línea * 21 + entradaElementoRanura] = valorColor;
            int valorPunto = píxelPuntero(entradaElementoRanura, línea); if (valorPunto != 0) valorColor = valorPunto == 2 ? 0xffffff : 0x101010;
        }
        if (Placa.leerPíxelPresentar(posiciónHorizontal, posiciónVertical) != valorColor) {
            Placa.escribirPíxelPresentar(posiciónHorizontal, posiciónVertical, valorColor);
            bajoContador++; if (bajoContador == 0) altoContador++;
        }
    }
    public static void terminar() {
        if (esComposiciónEnCurso == 0) return;
        for (int línea = fronteraSuperior; línea < valorFronteraInferior; línea++) for (int entradaElementoRanura = valorFronteraIzquierdo; entradaElementoRanura < valorFronteraDerecho; entradaElementoRanura++)
            píxelPresentar(entradaElementoRanura, línea, píxelesCompuesto[(línea - fronteraSuperior) * 1920 + entradaElementoRanura]);
        esComposiciónEnCurso = 0;
    }
    public static int píxel(int posiciónHorizontal, int posiciónVertical, int valorColor) {
        if (posiciónHorizontal < 0 || posiciónVertical < 0 || posiciónHorizontal >= valorAnchura || posiciónVertical >= valorAltura) return 0;
        if (esComposiciónEnCurso != 0) {
            if (posiciónHorizontal >= valorFronteraIzquierdo && posiciónHorizontal < valorFronteraDerecho && posiciónVertical >= fronteraSuperior && posiciónVertical < valorFronteraInferior)
                píxelesCompuesto[(posiciónVertical - fronteraSuperior) * 1920 + posiciónHorizontal] = valorColor;
        } else píxelPresentar(posiciónHorizontal, posiciónVertical, valorColor);
        return 0;
    }
    public static void rellenarRectángulo(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int longitud, int valorColor) {
        if (recortar(posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, longitud) == 0) return;
        posiciónHorizontal = límitesRecortado[0]; posiciónVertical = límitesRecortado[1]; extensiónRangoAnchura = límitesRecortado[2]; longitud = límitesRecortado[3];
        for (int línea = posiciónVertical; línea < posiciónVertical + longitud; línea++) for (int entradaElementoRanura = posiciónHorizontal; entradaElementoRanura < posiciónHorizontal + extensiónRangoAnchura; entradaElementoRanura++) {
            if (esComposiciónEnCurso != 0) píxelesCompuesto[(línea - fronteraSuperior) * 1920 + entradaElementoRanura] = valorColor;
            else píxelPresentar(entradaElementoRanura, línea, valorColor);
        }
    }
    public static void puntero(int posiciónHorizontal, int posiciónVertical, int valorForma) {
        if (valorAnchura == 0) return;
        int posiciónHorizontalNuevo = posiciónHorizontal - (valorForma >= 2 ? 10 : 0), posiciónVerticalNuevo = posiciónVertical - (valorForma >= 2 ? 10 : 0);
        if (formaPuntero == valorForma && coordenadaHorizontalPuntero == posiciónHorizontalNuevo && coordenadaVerticalPuntero == posiciónVerticalNuevo) return;
        if (formaPuntero != 0) for (int línea = 0; línea < 21; línea++) for (int entradaElementoRanura = 0; entradaElementoRanura < 21; entradaElementoRanura++) {
            int operandoPrimero = coordenadaHorizontalPuntero + entradaElementoRanura, valorTres = coordenadaVerticalPuntero + línea;
            if (operandoPrimero >= 0 && valorTres >= 0 && operandoPrimero < valorAnchura && valorTres < valorAltura) Placa.escribirPíxelPresentar(operandoPrimero, valorTres, fondoPuntero[línea * 21 + entradaElementoRanura]);
        }
        formaPuntero = valorForma; coordenadaHorizontalPuntero = posiciónHorizontalNuevo; coordenadaVerticalPuntero = posiciónVerticalNuevo;
        if (valorForma != 0) for (int línea = 0; línea < 21; línea++) for (int entradaElementoRanura = 0; entradaElementoRanura < 21; entradaElementoRanura++) {
            int operandoPrimero = coordenadaHorizontalPuntero + entradaElementoRanura, valorTres = coordenadaVerticalPuntero + línea;
            if (operandoPrimero >= 0 && valorTres >= 0 && operandoPrimero < valorAnchura && valorTres < valorAltura) {
                fondoPuntero[línea * 21 + entradaElementoRanura] = Placa.leerPíxelPresentar(operandoPrimero, valorTres);
                int valorPunto = píxelPuntero(entradaElementoRanura, línea); if (valorPunto != 0) Placa.escribirPíxelPresentar(operandoPrimero, valorTres, valorPunto == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
