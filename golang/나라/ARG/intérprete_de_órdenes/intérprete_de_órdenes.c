/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <conversión_de_direcciones/orden_de_octetos.h>
#include <errno.h>
#include <fcntl.h>
#include <entre_redes/dirección.h>
#include <definiciones_básicas.h>
#include <sistema/socket.h>
#include <sistema/stat.h>
#include <sistema/identidad_del_sistema.h>
#include <sistema/espera_de_hijos.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { capacidad_de_la_línea_de_entrada = 512, máximo_de_argumentos = 16, máximo_anidamiento_de_archivos_de_órdenes = 4 };
static int profundidad_de_anidamiento;
struct flujo_de_entrada {
    int descriptor_de_entrada;
    char memoria_intermedia_de_transferencia_2[256];
    size_t posición;
    size_t longitud;
};

static size_t longitud_del_texto_en_octetos(const char *texto)
{
    size_t longitud = 0;
    while (texto[longitud] != '\0')
        longitud++;
    return longitud;
}

static int textos_iguales(const char *izquierda, const char *derecha)
{
    size_t posición = 0;
    while (izquierda[posición] == derecha[posición]) {
        if (izquierda[posición] == '\0')
            return 1;
        posición++;
    }
    return 0;
}

static void escribir_texto(const char *texto)
{
    size_t longitud = longitud_del_texto_en_octetos(texto);
    while (longitud > 0U) {
        ssize_t cantidad_de_octetos_escritos = escribir(STDOUT_FILENO, texto, longitud);
        if (cantidad_de_octetos_escritos <= 0)
            return;
        texto += cantidad_de_octetos_escritos;
        longitud -= (size_t)cantidad_de_octetos_escritos;
    }
}

static void escribir_entero(int valor)
{
    char caracteres_de_los_dígitos[16];
    unsigned int cantidad_de_dígitos;
    unsigned int magnitud_sin_signo;

    if (valor < 0) {
        escribir_texto("-");
        magnitud_sin_signo = (unsigned int)(-(valor + 1)) + 1U;
    } else {
        magnitud_sin_signo = (unsigned int)valor;
    }
    cantidad_de_dígitos = 0;
    do {
        caracteres_de_los_dígitos[cantidad_de_dígitos++] = (char)('0' + magnitud_sin_signo % 10U);
        magnitud_sin_signo /= 10U;
    } while (magnitud_sin_signo != 0U);
    while (cantidad_de_dígitos > 0U) {
        cantidad_de_dígitos--;
        (void)escribir(STDOUT_FILENO, &caracteres_de_los_dígitos[cantidad_de_dígitos], 1);
    }
}

static void informar_del_error(const char *operación)
{
    escribir_texto("error: ");
    escribir_texto(operación);
    escribir_texto(" errno=");
    escribir_entero(errno);
    escribir_texto("\n");
}

static int leer_línea_de_entrada(struct flujo_de_entrada *entrada, char *línea_de_entrada, size_t capacidad)
{
    size_t posición = 0;
    int línea_de_entrada_inválida = 0;
    char carácter;
    ssize_t octetos_leídos;
    if (capacidad < 2U)
        return -2;
    for (;;) {
        if (entrada->posición == entrada->longitud) {
            octetos_leídos = leer(entrada->descriptor_de_entrada, entrada->memoria_intermedia_de_transferencia_2, sizeof(entrada->memoria_intermedia_de_transferencia_2));
            if (octetos_leídos < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (octetos_leídos == 0) {
                if (posición == 0 && !línea_de_entrada_inválida)
                    return -1;
                break;
            }
            entrada->longitud = (size_t)octetos_leídos;
            entrada->posición = 0;
        }
        carácter = entrada->memoria_intermedia_de_transferencia_2[entrada->posición++];
        if (carácter == '\n')
            break;
        if (entrada->descriptor_de_entrada == STDIN_FILENO && carácter == 4) {
            if (posición == 0 && !línea_de_entrada_inválida)
                return -1;
            break;
        }
        if (entrada->descriptor_de_entrada == STDIN_FILENO && (carácter == 8 || carácter == 127)) {
            if (posición > 0) {
                do {
                    posición--;
                } while (posición > 0 && ((unsigned char)línea_de_entrada[posición] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (carácter == '\r')
            continue;
        if (carácter == '\0') {
            línea_de_entrada_inválida = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (posición + 1U < capacidad)
            línea_de_entrada[posición++] = carácter;
        else
            línea_de_entrada_inválida = 1;
    }
    línea_de_entrada[posición] = '\0';
    return línea_de_entrada_inválida ? -2 : (int)posición;
}

static int separar_argumentos(char *línea_de_entrada, char **argumentos)
{
    int cantidad_de_argumentos = 0;
    char *posición_actual = línea_de_entrada;
    char *posición_de_salida = línea_de_entrada;

    while (*posición_actual != '\0') {
        char comilla = '\0';
        while (*posición_actual == ' ' || *posición_actual == '\t')
            posición_actual++;
        if (*posición_actual == '\0' || *posición_actual == '#')
            break;
        if (cantidad_de_argumentos == máximo_de_argumentos - 1)
            return -1;
        argumentos[cantidad_de_argumentos++] = posición_de_salida;
        while (*posición_actual != '\0') {
            char carácter = *posición_actual++;
            if (comilla == '\0' && (carácter == ' ' || carácter == '\t'))
                break;
            if (carácter == '\\' && comilla != '\'') {
                if (*posición_actual == '\0')
                    return -1;
                *posición_de_salida++ = *posición_actual++;
            } else if (carácter == '\'' || carácter == '"') {
                if (comilla == '\0')
                    comilla = carácter;
                else if (comilla == carácter)
                    comilla = '\0';
                else
                    *posición_de_salida++ = carácter;
            } else {
                *posición_de_salida++ = carácter;
            }
        }
        if (comilla != '\0')
            return -1;
        *posición_de_salida++ = '\0';
    }
    argumentos[cantidad_de_argumentos] = (char *)0;
    return cantidad_de_argumentos;
}

static void mostrar_ayuda(void)
{
    size_t posición;
    escribir_texto(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    escribir_texto("Native command proposals (ASCII aliases remain available):\n");
    for (posición = 0; posición < sizeof(órdenes_de_referencia) / sizeof(órdenes_de_referencia[0]); posición++) {
        escribir_texto(alias_locales_de_órdenes[posición]);
        escribir_texto(" = ");
        escribir_texto(órdenes_de_referencia[posición]);
        escribir_texto("\n");
    }
}

static int coincide_la_orden(const char *texto, const char *orden)
{
    size_t posición;
    if (textos_iguales(texto, orden))
        return 1;
    for (posición = 0; posición < sizeof(órdenes_de_referencia) / sizeof(órdenes_de_referencia[0]); posición++)
        if (textos_iguales(orden, órdenes_de_referencia[posición]))
            return textos_iguales(texto, alias_locales_de_órdenes[posición]);
    return 0;
}

static int interpretar_entrada(int descriptor_de_entrada);

static int interpretar_archivo_de_órdenes(const char *nombre_del_archivo)
{
    int descriptor_del_archivo_2;
    int estado;
    if (profundidad_de_anidamiento >= máximo_anidamiento_de_archivos_de_órdenes) {
        escribir_texto("source: nesting limit\n");
        return 0;
    }
    descriptor_del_archivo_2 = abrir(nombre_del_archivo, O_RDONLY);
    if (descriptor_del_archivo_2 < 0) {
        informar_del_error(nombre_del_archivo);
        return 0;
    }
    profundidad_de_anidamiento++;
    estado = interpretar_entrada(descriptor_del_archivo_2);
    profundidad_de_anidamiento--;
    (void)cerrar(descriptor_del_archivo_2);
    return estado;
}

static void mostrar_argumentos(int cantidad_de_argumentos, char **argumentos)
{
    int posición;
    for (posición = 1; posición < cantidad_de_argumentos; posición++) {
        if (posición != 1)
            escribir_texto(" ");
        escribir_texto(argumentos[posición]);
    }
    escribir_texto("\n");
}

static void mostrar_directorio_actual(void)
{
    char ruta[128];
    if (obtener_ruta_del_directorio_de_trabajo(ruta, sizeof(ruta)) == (char *)0) {
        informar_del_error("pwd");
        return;
    }
    escribir_texto(ruta);
    escribir_texto("\n");
}

static void mostrar_contenido_del_archivo(const char *nombre_del_archivo)
{
    char memoria_intermedia_de_transferencia_2[128];
    int descriptor_del_archivo_2 = abrir(nombre_del_archivo, O_RDONLY);
    ssize_t octetos_leídos;

    if (descriptor_del_archivo_2 < 0) {
        informar_del_error("cat");
        return;
    }
    while ((octetos_leídos = leer(descriptor_del_archivo_2, memoria_intermedia_de_transferencia_2, sizeof(memoria_intermedia_de_transferencia_2))) > 0)
        (void)escribir(STDOUT_FILENO, memoria_intermedia_de_transferencia_2, (size_t)octetos_leídos);
    if (octetos_leídos < 0)
        informar_del_error("cat/read");
    (void)cerrar(descriptor_del_archivo_2);
    escribir_texto("\n");
}

static void mostrar_información_del_archivo(const char *nombre_del_archivo)
{
    struct estado_del_archivo estado;
    if (estado_del_archivo(nombre_del_archivo, &estado) < 0) {
        informar_del_error("stat");
        return;
    }
    escribir_texto("size=");
    escribir_entero((int)estado.st_size);
    escribir_texto(S_ISDIR(estado.st_mode) ? " type=directory\n" : " type=file\n");
}

static void mostrar_identificadores_de_procesos(void)
{
    escribir_texto("pid=");
    escribir_entero((int)obtener_identificador_de_proceso());
    escribir_texto(" ppid=");
    escribir_entero((int)obtener_identificador_del_padre());
    escribir_texto("\n");
}

static void mostrar_identidad_del_sistema(void)
{
    struct utsname identidad_del_sistema;
    if (obtener_información_del_sistema(&identidad_del_sistema) < 0) {
        informar_del_error("uname");
        return;
    }
    escribir_texto(identidad_del_sistema.sysname);
    escribir_texto(" ");
    escribir_texto(identidad_del_sistema.release);
    escribir_texto(" ");
    escribir_texto(identidad_del_sistema.machine);
    escribir_texto("\n");
}

static void ejecutar_programa(int cantidad_de_argumentos, char **argumentos)
{
    pid_t identificador_del_proceso_hijo;
    int estado_de_terminación_del_hijo = 0;

    if (cantidad_de_argumentos < 2) {
        escribir_texto("usage: run FILE [ARGS...]\n");
        return;
    }
    identificador_del_proceso_hijo = bifurcar_proceso();
    if (identificador_del_proceso_hijo < 0) {
        informar_del_error("fork");
        return;
    }
    if (identificador_del_proceso_hijo == 0) {
        sustituir_programa_en_ejecución(argumentos[1], &argumentos[1], (char *const *)0);
        informar_del_error("execve");
        terminar_inmediatamente(127);
    }
    if (esperar_hijo_indicado(identificador_del_proceso_hijo, &estado_de_terminación_del_hijo, 0) < 0) {
        informar_del_error("waitpid");
        return;
    }
    escribir_texto("exit-status=");
    escribir_entero(WEXITSTATUS(estado_de_terminación_del_hijo));
    escribir_texto("\n");
}

static void probar_retorno_del_datagrama(const char *mensaje)
{
    struct dirección_de_extremo_entre_redes dirección_de_recepción = {0};
    struct dirección_de_extremo_entre_redes dirección_del_remitente = {0};
    tipo_de_longitud_de_dirección longitud_de_la_dirección_del_remitente = sizeof(dirección_del_remitente);
    char datos_recibidos[96];
    size_t longitud_del_mensaje_en_octetos = longitud_del_texto_en_octetos(mensaje);
    int extremo_receptor = -1;
    int extremo_emisor = -1;
    ssize_t cantidad_de_octetos_recibidos;

    if (longitud_del_mensaje_en_octetos >= sizeof(datos_recibidos)) {
        escribir_texto("udp: message exceeds 95 bytes\n");
        return;
    }
    extremo_receptor = crear_extremo_de_comunicación(código_de_familia_de_direcciones_entre_redes, extremo_de_datagramas, protocolo_de_datagramas_de_usuario);
    extremo_emisor = crear_extremo_de_comunicación(código_de_familia_de_direcciones_entre_redes, extremo_de_datagramas, protocolo_de_datagramas_de_usuario);
    if (extremo_receptor < 0 || extremo_emisor < 0) {
        informar_del_error("socket");
        goto cerrar_extremos_de_comunicación;
    }
    dirección_de_recepción.familia_de_direcciones_entre_redes = código_de_familia_de_direcciones_entre_redes;
    dirección_de_recepción.número_de_puerto_de_comunicación = convertir_16_bits_a_orden_de_red(40404);
    dirección_de_recepción.contenido_de_dirección_entre_redes.valor_de_dirección = convertir_32_bits_a_orden_de_red(dirección_de_retorno_local);
    if (asociar_dirección_local(extremo_receptor, (const struct dirección_de_extremo_de_comunicación *)&dirección_de_recepción, sizeof(dirección_de_recepción)) < 0) {
        informar_del_error("bind");
        goto cerrar_extremos_de_comunicación;
    }
    if (conectar_con_extremo_remoto(extremo_emisor, (const struct dirección_de_extremo_de_comunicación *)&dirección_de_recepción, sizeof(dirección_de_recepción)) < 0) {
        informar_del_error("connect");
        goto cerrar_extremos_de_comunicación;
    }
    if (enviar(extremo_emisor, mensaje, longitud_del_mensaje_en_octetos, 0) != (ssize_t)longitud_del_mensaje_en_octetos) {
        informar_del_error("send");
        goto cerrar_extremos_de_comunicación;
    }
    cantidad_de_octetos_recibidos = recibir_con_dirección_de_origen(extremo_receptor, datos_recibidos, sizeof(datos_recibidos) - 1U, 0,
                         (struct dirección_de_extremo_de_comunicación *)&dirección_del_remitente, &longitud_de_la_dirección_del_remitente);
    if (cantidad_de_octetos_recibidos < 0) {
        informar_del_error("recvfrom");
        goto cerrar_extremos_de_comunicación;
    }
    datos_recibidos[cantidad_de_octetos_recibidos] = '\0';
    escribir_texto("udp-received: ");
    escribir_texto(datos_recibidos);
    escribir_texto("\n");

cerrar_extremos_de_comunicación:
    if (extremo_emisor >= 0)
        (void)cerrar(extremo_emisor);
    if (extremo_receptor >= 0)
        (void)cerrar(extremo_receptor);
}

static int interpretar_entrada(int descriptor_de_entrada)
{
    char línea_de_entrada[capacidad_de_la_línea_de_entrada];
    char *argumentos[máximo_de_argumentos];
    struct flujo_de_entrada entrada = {0};
    entrada.descriptor_de_entrada = descriptor_de_entrada;

    for (;;) {
        int cantidad_de_argumentos;
        int estado;
        if (descriptor_de_entrada == STDIN_FILENO)
            escribir_texto("worldos$ ");
        estado = leer_línea_de_entrada(&entrada, línea_de_entrada, sizeof(línea_de_entrada));
        if (estado == -1)
            return 0;
        if (estado == -2) {
            escribir_texto("input rejected: overlong or binary line\n");
            continue;
        }
        cantidad_de_argumentos = separar_argumentos(línea_de_entrada, argumentos);
        if (cantidad_de_argumentos < 0) {
            escribir_texto("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (cantidad_de_argumentos == 0)
            continue;
        if (coincide_la_orden(argumentos[0], "help"))
            mostrar_ayuda();
        else if (coincide_la_orden(argumentos[0], "echo"))
            mostrar_argumentos(cantidad_de_argumentos, argumentos);
        else if (coincide_la_orden(argumentos[0], "pwd"))
            mostrar_directorio_actual();
        else if (coincide_la_orden(argumentos[0], "cd")) {
            if (cantidad_de_argumentos < 2)
                escribir_texto("usage: cd PATH\n");
            else if (cambiar_directorio_de_trabajo(argumentos[1]) < 0)
                informar_del_error("cd");
        } else if (coincide_la_orden(argumentos[0], "cat")) {
            if (cantidad_de_argumentos < 2)
                escribir_texto("usage: cat FILE\n");
            else
                mostrar_contenido_del_archivo(argumentos[1]);
        } else if (coincide_la_orden(argumentos[0], "stat")) {
            if (cantidad_de_argumentos < 2)
                escribir_texto("usage: stat FILE\n");
            else
                mostrar_información_del_archivo(argumentos[1]);
        } else if (coincide_la_orden(argumentos[0], "pid"))
            mostrar_identificadores_de_procesos();
        else if (coincide_la_orden(argumentos[0], "uname"))
            mostrar_identidad_del_sistema();
        else if (coincide_la_orden(argumentos[0], "run"))
            ejecutar_programa(cantidad_de_argumentos, argumentos);
        else if (coincide_la_orden(argumentos[0], "udp"))
            probar_retorno_del_datagrama(cantidad_de_argumentos >= 2 ? argumentos[1] : "ping");
        else if (coincide_la_orden(argumentos[0], "source")) {
            if (cantidad_de_argumentos < 2)
                escribir_texto("usage: source FILE\n");
            else if (interpretar_archivo_de_órdenes(argumentos[1]))
                return 1;
        } else if (coincide_la_orden(argumentos[0], "exit"))
            return 1;
        else
            escribir_texto("unknown command; type help\n");
    }
}

int main(void)
{
    escribir_texto("WORLDOS-SHELL:READY\n");
    (void)interpretar_entrada(STDIN_FILENO);
    escribir_texto("WORLDOS-SHELL:EXIT\n");
    return 0;
}
