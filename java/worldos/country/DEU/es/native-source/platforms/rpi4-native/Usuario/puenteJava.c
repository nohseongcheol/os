#include "../denominación/nombresEnlazarMáquina.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Archivo/Salida/인수는 construirTodos EL0 SVC를 거친다.
#include "invocar.h"
#include "java-resources.h"
#include "Paquete.h"
typedef uintptr_t palabraMáquina;
static int valorCategoría;
static int activoJAR, desplazarJAR;
static palabraMáquina argumentoReenviado[8][257];
static unsigned sustitutoUnicodePendiente;
extern int32_t entradaElementoJava(void);
static intptr_t invocar(unsigned númeroElementosElementoLista, palabraMáquina valorPrimero, palabraMáquina valorSegundo, palabraMáquina códigoCarácter) {
    return invocarUsuario(númeroElementosElementoLista, valorPrimero, valorSegundo, códigoCarácter, 0, 0, 0);
}
static void valoresByte(const char *posiciónDatos, size_t númeroElementosElementoLista) { invocar(1, 1, (palabraMáquina)posiciónDatos, númeroElementosElementoLista); }
static void carácter(unsigned códigoCarácter) {
    unsigned char Datos[4]; unsigned númeroElementosElementoLista = 0;
    if (códigoCarácter < 128) Datos[númeroElementosElementoLista++] = códigoCarácter;
    else if (códigoCarácter < 2048) { Datos[númeroElementosElementoLista++] = 0xc0 | (códigoCarácter >> 6); Datos[númeroElementosElementoLista++] = 0x80 | (códigoCarácter & 63); }
    else if (códigoCarácter < 65536) { Datos[númeroElementosElementoLista++] = 0xe0 | (códigoCarácter >> 12); Datos[númeroElementosElementoLista++] = 0x80 | ((códigoCarácter >> 6) & 63); Datos[númeroElementosElementoLista++] = 0x80 | (códigoCarácter & 63); }
    else { Datos[númeroElementosElementoLista++] = 0xf0 | (códigoCarácter >> 18); Datos[númeroElementosElementoLista++] = 0x80 | ((códigoCarácter >> 12) & 63); Datos[númeroElementosElementoLista++] = 0x80 | ((códigoCarácter >> 6) & 63); Datos[númeroElementosElementoLista++] = 0x80 | (códigoCarácter & 63); }
    valoresByte((const char *)Datos, númeroElementosElementoLista);
}
palabraMáquina carácterHerramienta(palabraMáquina valor) {
    unsigned códigoCarácter = valor;
    if (sustitutoUnicodePendiente) {
        unsigned parteAlto = sustitutoUnicodePendiente; sustitutoUnicodePendiente = 0;
        if (códigoCarácter >= 0xdc00 && códigoCarácter <= 0xdfff) { carácter(0x10000 + ((parteAlto - 0xd800) << 10) + códigoCarácter - 0xdc00); return 1; }
        carácter(0xfffd);
    }
    if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdbff) sustitutoUnicodePendiente = códigoCarácter;
    else carácter(códigoCarácter > 0x10ffff || (códigoCarácter >= 0xdc00 && códigoCarácter <= 0xdfff) ? 0xfffd : códigoCarácter);
    return 1;
}
palabraMáquina imprimirHerramienta(palabraMáquina valor) {
    const palabraMáquina *datosCadena = (const palabraMáquina *)valor;
    for (palabraMáquina índiceOrdinal = 0; índiceOrdinal < datosCadena[0]; índiceOrdinal++) carácterHerramienta(datosCadena[índiceOrdinal + 1]);
    return datosCadena[0];
}
static int ruta(palabraMáquina referenciaObjeto, char datosResultado[512]) {
    const palabraMáquina *valorPrimero = (const palabraMáquina *)referenciaObjeto;
    unsigned capacidadUsado = 0;
    for (palabraMáquina índiceOrdinal = 1; índiceOrdinal <= valorPrimero[0] && valorPrimero[índiceOrdinal]; índiceOrdinal++) {
        unsigned códigoCarácter = valorPrimero[índiceOrdinal];
        // UTF-16 -> UTF-8. 기존 도구의 char[] modoMétodo 경로와 호환한다.
        if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdbff && índiceOrdinal < valorPrimero[0] && valorPrimero[índiceOrdinal + 1] >= 0xdc00 && valorPrimero[índiceOrdinal + 1] <= 0xdfff)
            { unsigned valorBajo = valorPrimero[++índiceOrdinal]; códigoCarácter = 0x10000 + ((códigoCarácter - 0xd800) << 10) + valorBajo - 0xdc00; }
        else if (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdfff) return -22;
        unsigned númeroElementosElementoLista = códigoCarácter < 128 ? 1 : códigoCarácter < 2048 ? 2 : códigoCarácter < 65536 ? 3 : 4;
        if (capacidadUsado + númeroElementosElementoLista > 511) return -36;
        if (númeroElementosElementoLista == 1) datosResultado[capacidadUsado++] = códigoCarácter;
        else {
            datosResultado[capacidadUsado++] = (númeroElementosElementoLista == 2 ? 0xc0 : númeroElementosElementoLista == 3 ? 0xe0 : 0xf0) | (códigoCarácter >> (6 * (númeroElementosElementoLista - 1)));
            for (unsigned ordinalInterior = númeroElementosElementoLista - 1; ordinalInterior; ordinalInterior--) datosResultado[capacidadUsado++] = 0x80 | ((códigoCarácter >> (6 * (ordinalInterior - 1))) & 63);
        }
    }
    datosResultado[capacidadUsado] = 0; return capacidadUsado ? 0 : -22;
}
palabraMáquina abrirHerramienta(palabraMáquina nombre, palabraMáquina bitsConfiguración) {
    char posiciónDatos[512]; int error = ruta(nombre, posiciónDatos);
    return (uint32_t)(error ? error : invocar(3, (palabraMáquina)posiciónDatos, bitsConfiguración, 0));
}
palabraMáquina cerrarHerramienta(palabraMáquina manejadorArchivo) { return (uint32_t)invocar(4, manejadorArchivo, 0, 0); }
palabraMáquina byteLeerHerramienta(palabraMáquina manejadorArchivo) {
    unsigned char valorSegundo; intptr_t númeroElementosElementoLista = invocar(2, manejadorArchivo, (palabraMáquina)&valorSegundo, 1);
    return (uint32_t)(númeroElementosElementoLista == 1 ? valorSegundo : númeroElementosElementoLista == 0 ? 256 : númeroElementosElementoLista);
}
palabraMáquina byteEscribirHerramienta(palabraMáquina manejadorArchivo, palabraMáquina valor) {
    unsigned char valorSegundo = valor; return (uint32_t)invocar(1, manejadorArchivo, (palabraMáquina)&valorSegundo, 1);
}
palabraMáquina leerHerramienta(palabraMáquina nombre, palabraMáquina direcciónDatosDestino) {
    if (activoJAR) {
        char posiciónDatos[512]; int error = ruta(nombre, posiciónDatos); if (error) return (uint32_t)error;
        unsigned númeroElementosElementoLista = 0; while (posiciónDatos[númeroElementosElementoLista]) númeroElementosElementoLista++;
        if (númeroElementosElementoLista >= 6) for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista - 6; índiceOrdinal++) if (posiciónDatos[índiceOrdinal] == '.') posiciónDatos[índiceOrdinal] = '/';
        unsigned char valoresByte[16384]; palabraMáquina *posiciónValorDestino = (palabraMáquina *)direcciónDatosDestino;
        int númeroElementosRecibido = leerJAR(posiciónDatos, valoresByte, posiciónValorDestino[0] < sizeof(valoresByte) ? posiciónValorDestino[0] : sizeof(valoresByte));
        if (númeroElementosRecibido >= 0) { for (int índiceOrdinal = 0; índiceOrdinal < númeroElementosRecibido; índiceOrdinal++) posiciónValorDestino[índiceOrdinal + 1] = valoresByte[índiceOrdinal]; return númeroElementosRecibido; }
        if (númeroElementosRecibido != -2) return (uint32_t)númeroElementosRecibido;
    }
    int manejadorArchivo = activoJAR ? -2 : (int32_t)abrirHerramienta(nombre, 0);
    if (manejadorArchivo < 0) {
        char posiciónDatos[512]; int error = ruta(nombre, posiciónDatos); if (error) return (uint32_t)error;
        for (unsigned índiceOrdinal = 0; índiceOrdinal < sizeof(listaClaseJava) / sizeof(listaClaseJava[0]); índiceOrdinal++) {
            const char *desfaseSiguiente = listaClaseJava[índiceOrdinal].nombre; unsigned ordinalInterior = 0;
            while (posiciónDatos[ordinalInterior] && posiciónDatos[ordinalInterior] == desfaseSiguiente[ordinalInterior]) ordinalInterior++;
            if (posiciónDatos[ordinalInterior] || desfaseSiguiente[ordinalInterior]) continue;
            palabraMáquina *posiciónValorDestino = (palabraMáquina *)direcciónDatosDestino;
            if (posiciónValorDestino[0] < listaClaseJava[índiceOrdinal].tamaño) return (uint32_t)-27;
            for (ordinalInterior = 0; ordinalInterior < listaClaseJava[índiceOrdinal].tamaño; ordinalInterior++) posiciónValorDestino[ordinalInterior + 1] = listaClaseJava[índiceOrdinal].Datos[ordinalInterior];
            return listaClaseJava[índiceOrdinal].tamaño;
        }
        return (uint32_t)manejadorArchivo;
    }
    palabraMáquina *valorPrimero = (palabraMáquina *)direcciónDatosDestino;
    intptr_t tamaño = invocar(9, manejadorArchivo, 0, 0), importeCompletado = 0;
    if (tamaño < 0 || (palabraMáquina)tamaño > valorPrimero[0]) { cerrarHerramienta(manejadorArchivo); return (uint32_t)(tamaño < 0 ? tamaño : -27); }
    unsigned char bloqueDatos[256];
    while (importeCompletado < tamaño) {
        intptr_t númeroElementosElementoLista = invocar(2, manejadorArchivo, (palabraMáquina)bloqueDatos, tamaño - importeCompletado < 256 ? tamaño - importeCompletado : 256);
        if (númeroElementosElementoLista <= 0) { cerrarHerramienta(manejadorArchivo); return (uint32_t)(númeroElementosElementoLista ? númeroElementosElementoLista : -5); }
        for (intptr_t índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) valorPrimero[1 + importeCompletado + índiceOrdinal] = bloqueDatos[índiceOrdinal];
        importeCompletado += númeroElementosElementoLista;
    }
    cerrarHerramienta(manejadorArchivo); return importeCompletado;
}
palabraMáquina escribirHerramienta(palabraMáquina nombre, palabraMáquina datosOriginal, palabraMáquina númeroElementosEntradaElemento) {
    const palabraMáquina *valorPrimero = (const palabraMáquina *)datosOriginal;
    if (númeroElementosEntradaElemento > valorPrimero[0] || númeroElementosEntradaElemento > 16384) return (uint32_t)-27;
    int manejadorArchivo = (int32_t)abrirHerramienta(nombre, 577); if (manejadorArchivo < 0) return (uint32_t)manejadorArchivo;
    unsigned char bloqueDatos[256]; palabraMáquina importeCompletado = 0;
    while (importeCompletado < númeroElementosEntradaElemento) {
        palabraMáquina númeroElementosElementoLista = númeroElementosEntradaElemento - importeCompletado < 256 ? númeroElementosEntradaElemento - importeCompletado : 256;
        for (palabraMáquina índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) bloqueDatos[índiceOrdinal] = valorPrimero[1 + importeCompletado + índiceOrdinal];
        intptr_t resultado = invocar(1, manejadorArchivo, (palabraMáquina)bloqueDatos, númeroElementosElementoLista);
        if (resultado <= 0) { cerrarHerramienta(manejadorArchivo); return (uint32_t)(resultado ? resultado : -5); }
        importeCompletado += resultado;
    }
    cerrarHerramienta(manejadorArchivo); return númeroElementosEntradaElemento;
}
palabraMáquina númeroArgumentosHerramienta(void) { return invocar(15, UINTPTR_MAX, 0, 0) - (activoJAR ? desplazarJAR : 0); }
palabraMáquina argumentoHerramienta(palabraMáquina índiceBuscar) {
    static const palabraMáquina valorVacíoEstado[1] = {0};
    if (índiceBuscar >= 8) return (palabraMáquina)valorVacíoEstado;
    unsigned char entrada[256]; intptr_t númeroElementosElementoLista;
    if (activoJAR && índiceBuscar == 0) { const char *posiciónDatos = principalJAR(); númeroElementosElementoLista = 0; while (posiciónDatos[númeroElementosElementoLista] && númeroElementosElementoLista < 255) { entrada[númeroElementosElementoLista] = posiciónDatos[númeroElementosElementoLista]; númeroElementosElementoLista++; } }
    else númeroElementosElementoLista = invocar(15, índiceBuscar + (activoJAR ? desplazarJAR : 0), (palabraMáquina)entrada, sizeof(entrada));
    if (númeroElementosElementoLista < 0) return (palabraMáquina)valorVacíoEstado;
    palabraMáquina *datosResultado = argumentoReenviado[índiceBuscar]; unsigned númeroElementosEntradaElemento = 0;
    for (intptr_t índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista;) {
        unsigned códigoCarácter = entrada[índiceOrdinal++], tieneMás = códigoCarácter < 128 ? 0 : códigoCarácter >= 0xc2 && códigoCarácter < 0xe0 ? 1 : códigoCarácter < 0xf0 && códigoCarácter >= 0xe0 ? 2 : códigoCarácter >= 0xf0 && códigoCarácter <= 0xf4 ? 3 : 4;
        if (tieneMás == 4 || índiceOrdinal + tieneMás > númeroElementosElementoLista) { datosResultado[++númeroElementosEntradaElemento] = 0xfffd; continue; }
        unsigned datosMínimo = tieneMás == 1 ? 128 : tieneMás == 2 ? 2048 : tieneMás == 3 ? 65536 : 0;
        if (tieneMás) códigoCarácter &= (1u << (6 - tieneMás)) - 1;
        unsigned ordinalInterior = 0;
        while (ordinalInterior < tieneMás && (entrada[índiceOrdinal] & 0xc0) == 0x80) { códigoCarácter = (códigoCarácter << 6) | (entrada[índiceOrdinal++] & 63); ordinalInterior++; }
        if (ordinalInterior != tieneMás || códigoCarácter < datosMínimo || códigoCarácter > 0x10ffff || (códigoCarácter >= 0xd800 && códigoCarácter <= 0xdfff)) códigoCarácter = 0xfffd;
        if (códigoCarácter >= 65536) { códigoCarácter -= 65536; datosResultado[++númeroElementosEntradaElemento] = 0xd800 | (códigoCarácter >> 10); datosResultado[++númeroElementosEntradaElemento] = 0xdc00 | (códigoCarácter & 1023); }
        else datosResultado[++númeroElementosEntradaElemento] = códigoCarácter;
    }
    datosResultado[0] = númeroElementosEntradaElemento; return (palabraMáquina)datosResultado;
}
palabraMáquina claseTipoHerramienta(void) { return valorCategoría; }
void paradaFatalNúcleo(const char *textoNotificación) {
    const char *posiciónDatos = textoNotificación; while (*posiciónDatos) posiciónDatos++;
    valoresByte("Java tool runtime error: ", 25); valoresByte(textoNotificación, posiciónDatos - textoNotificación); carácter(10);
    invocar(6, 1, 0, 0); for (;;) {}
}
int iniciarProgramaUsuario(int modoMétodo) {
    valorCategoría = modoMétodo;
    unsigned char entradaElementoPrimero[256]; intptr_t númeroElementosElementoLista = invocar(15, 0, (palabraMáquina)entradaElementoPrimero, sizeof(entradaElementoPrimero));
    if (modoMétodo == 2 || (modoMétodo == 1 && númeroElementosElementoLista == 4 && entradaElementoPrimero[0] == '-' && entradaElementoPrimero[1] == 'j' && entradaElementoPrimero[2] == 'a' && entradaElementoPrimero[3] == 'r')) {
        desplazarJAR = modoMétodo == 2 ? 0 : 1;
        char nombreEntradaElementoArchivo[256]; intptr_t datosLongitud = invocar(15, desplazarJAR, (palabraMáquina)nombreEntradaElementoArchivo, sizeof(nombreEntradaElementoArchivo));
        if (datosLongitud <= 0 || abrirJAR(nombreEntradaElementoArchivo) < 0) {
            static const char error[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            valoresByte(error, sizeof(error) - 1); return 1;
        }
        activoJAR = 1;
    }
    int resultado = entradaElementoJava();
    if (sustitutoUnicodePendiente) carácter(0xfffd);
    return resultado;
}

// UDP는 propio 커널의 SVC를 통과하며 elementoListaActual 127.0.0.1만 제공한다.
struct direcciónJava { uint16_t familia, númeroPuerto; uint32_t dirección; unsigned char valorCero[8]; };
static struct direcciónJava direcciónUDP(unsigned númeroPuerto) {
    struct direcciónJava valorPrimero = {2, (uint16_t)((númeroPuerto << 8) | (númeroPuerto >> 8)), 0x0100007f, {0}}; return valorPrimero;
}
palabraMáquina abrirUDPHerramienta(palabraMáquina númeroPuerto) {
    intptr_t manejadorArchivo = invocar(32, 2, 2, 17); if (manejadorArchivo < 0) return (uint32_t)manejadorArchivo;
    struct direcciónJava valorPrimero = direcciónUDP(númeroPuerto);
    valorPrimero.dirección = 0;
    intptr_t valorEstadoValor = invocar(33, manejadorArchivo, (palabraMáquina)&valorPrimero, sizeof(valorPrimero));
    if (valorEstadoValor < 0) { cerrarHerramienta(manejadorArchivo); return (uint32_t)valorEstadoValor; }
    return manejadorArchivo;
}
palabraMáquina enviarUDPHerramienta(palabraMáquina manejadorArchivo, palabraMáquina númeroPuerto, palabraMáquina valorArreglo, palabraMáquina longitud) {
    const palabraMáquina *direcciónOriginal = (const palabraMáquina *)valorArreglo; unsigned char Datos[512];
    if (longitud > 512 || longitud > direcciónOriginal[0]) return (uint32_t)-90;
    for (palabraMáquina índiceOrdinal = 0; índiceOrdinal < longitud; índiceOrdinal++) Datos[índiceOrdinal] = direcciónOriginal[índiceOrdinal + 1];
    struct direcciónJava valorPrimero = direcciónUDP(númeroPuerto);
    return (uint32_t)invocarUsuario(34, manejadorArchivo, (palabraMáquina)Datos, longitud, 0, (palabraMáquina)&valorPrimero, sizeof(valorPrimero));
}
static uint32_t ordenByteInverso(uint32_t númeroElementosElementoLista) { return (númeroElementosElementoLista>>24)|((númeroElementosElementoLista>>8)&0xff00)|((númeroElementosElementoLista<<8)&0xff0000)|(númeroElementosElementoLista<<24); }
palabraMáquina direcciónEnviarUDPHerramienta(palabraMáquina manejadorArchivo, palabraMáquina dirección, palabraMáquina númeroPuerto, palabraMáquina valorArreglo, palabraMáquina longitud) {
    const palabraMáquina *direcciónOriginal = (const palabraMáquina *)valorArreglo; unsigned char Datos[512];
    if (longitud > 512 || longitud > direcciónOriginal[0]) return (uint32_t)-90;
    for (palabraMáquina índiceOrdinal = 0; índiceOrdinal < longitud; índiceOrdinal++) Datos[índiceOrdinal] = direcciónOriginal[índiceOrdinal + 1];
    struct direcciónJava valorPrimero = direcciónUDP(númeroPuerto); valorPrimero.dirección = ordenByteInverso(dirección);
    return (uint32_t)invocarUsuario(34, manejadorArchivo, (palabraMáquina)Datos, longitud, 0, (palabraMáquina)&valorPrimero, sizeof(valorPrimero));
}
palabraMáquina conectarHerramienta(palabraMáquina manejadorArchivo, palabraMáquina dirección, palabraMáquina númeroPuerto) {
    struct direcciónJava valorPrimero = direcciónUDP(númeroPuerto); valorPrimero.dirección = ordenByteInverso(dirección);
    uint32_t ponerEnMarcha = invocar(7, 0, 0, 0);
    for (;;) {
        intptr_t resultado = invocar(37, manejadorArchivo, (palabraMáquina)&valorPrimero, sizeof(valorPrimero));
        if (resultado != -115) return (uint32_t)resultado;
        if ((uint32_t)(invocar(7, 0, 0, 0) - ponerEnMarcha) >= 1000) return (uint32_t)-110;
    }
}
palabraMáquina operaciónRecepciónUDPHerramienta(palabraMáquina manejadorArchivo, palabraMáquina valorArreglo, palabraMáquina capacidadBúfer) {
    palabraMáquina *direcciónDestino = (palabraMáquina *)valorArreglo; unsigned char Datos[512];
    if (capacidadBúfer > 512 || direcciónDestino[0] < 514) return (uint32_t)-90;
    struct direcciónJava valorPrimero; unsigned datosLongitud = sizeof(valorPrimero);
    intptr_t númeroElementosElementoLista = invocarUsuario(35, manejadorArchivo, (palabraMáquina)Datos, capacidadBúfer, 0, (palabraMáquina)&valorPrimero, (palabraMáquina)&datosLongitud);
    if (númeroElementosElementoLista >= 0) { for (intptr_t índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) direcciónDestino[índiceOrdinal + 1] = Datos[índiceOrdinal]; direcciónDestino[513] = (valorPrimero.númeroPuerto << 8 | valorPrimero.númeroPuerto >> 8) & 65535; direcciónDestino[514] = ordenByteInverso(valorPrimero.dirección); }
    return (uint32_t)númeroElementosElementoLista;
}
palabraMáquina puertoUDPHerramienta(palabraMáquina manejadorArchivo) {
    struct direcciónJava valorPrimero; unsigned datosLongitud = sizeof(valorPrimero);
    intptr_t valorDevuelto = invocar(36, manejadorArchivo, (palabraMáquina)&valorPrimero, (palabraMáquina)&datosLongitud);
    return (uint32_t)(valorDevuelto < 0 ? valorDevuelto : (valorPrimero.númeroPuerto << 8 | valorPrimero.númeroPuerto >> 8) & 65535);
}
palabraMáquina milisegundosTranscurridosHerramienta(void) { return (uint32_t)invocar(7, 0, 0, 0); }
palabraMáquina anchuraPantallaHerramienta(void) { return (uint32_t)leerAnchuraPantalla(); }
palabraMáquina alturaPantallaHerramienta(void) { return (uint32_t)leerAlturaPantalla(); }
palabraMáquina esperarGráficosHerramienta(void) { return (uint32_t)esperarTeclaPantallaPara(); }
palabraMáquina rectánguloHerramienta(palabraMáquina coordenadaCoordenadaHorizontal, palabraMáquina coordenadaCoordenadaVertical, palabraMáquina valorAnchuraSolicitado, palabraMáquina valorAlturaSolicitado, palabraMáquina colorPíxel) {
    return (uint32_t)invocarUsuario(13, coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical, colorPíxel, valorAnchuraSolicitado, valorAlturaSolicitado, 0);
}

palabraMáquina flujoHerramienta(palabraMáquina acción,palabraMáquina manejadorArchivo,palabraMáquina valor){
    if(acción==0)return (uint32_t)invocar(32,2,1,6);
    struct direcciónJava valorPrimero=direcciónUDP(valor);
    if(acción==1){valorPrimero.dirección=0;intptr_t valorDevuelto=invocar(33,manejadorArchivo,(palabraMáquina)&valorPrimero,sizeof(valorPrimero));return (uint32_t)(valorDevuelto<0?valorDevuelto:invocar(38,manejadorArchivo,4,0));}
    if(acción==2)return (uint32_t)invocar(37,manejadorArchivo,(palabraMáquina)&valorPrimero,sizeof(valorPrimero));
    if(acción==3)return (uint32_t)invocar(39,manejadorArchivo,0,0);
    if(acción==4)return puertoUDPHerramienta(manejadorArchivo);
    if(acción==5)return (uint32_t)invocar(40,manejadorArchivo,0,0);
    return (uint32_t)-22;
}
palabraMáquina gUIHerramienta(palabraMáquina acción,palabraMáquina valorIdentificador,palabraMáquina valorPrimero,palabraMáquina valorSegundo,palabraMáquina códigoCarácter,palabraMáquina datosDestino){return (uint32_t)invocarUsuario(20,acción,valorIdentificador,valorPrimero,valorSegundo,códigoCarácter,datosDestino);}
palabraMáquina textoGUIHerramienta(palabraMáquina valorIdentificador,palabraMáquina valorArreglo,palabraMáquina númeroElementosElementoLista){
    const palabraMáquina *direcciónOriginal=(const palabraMáquina *)valorArreglo;uint32_t Datos[127];unsigned númeroElementosEntradaElemento=0;
    if(númeroElementosElementoLista>direcciónOriginal[0])return (uint32_t)-22;
    for(palabraMáquina índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++){unsigned codificaciónEstadoCarácter=direcciónOriginal[índiceOrdinal+1];if(codificaciónEstadoCarácter>=0xd800&&codificaciónEstadoCarácter<=0xdbff&&índiceOrdinal+1<númeroElementosElementoLista){unsigned valorBajo=direcciónOriginal[++índiceOrdinal+1];if(valorBajo<0xdc00||valorBajo>0xdfff)return (uint32_t)-22;codificaciónEstadoCarácter=0x10000+((codificaciónEstadoCarácter-0xd800)<<10)+valorBajo-0xdc00;}if(númeroElementosEntradaElemento==127)return (uint32_t)-22;Datos[númeroElementosEntradaElemento++]=codificaciónEstadoCarácter;}
    return (uint32_t)invocarUsuario(21,valorIdentificador,(palabraMáquina)Datos,númeroElementosEntradaElemento,0,0,0);
}
