/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <conversión_de_direcciones/orden_de_octetos.h>
#include <sistema/syscall.h>
#include <sistema/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_crear_extremo_de_comunicación = 1, SC_asociar_dirección_local = 2, SC_conectar_con_extremo_remoto = 3, SC_preparar_recepción_de_conexiones = 4,
    SC_aceptar_conexión = 5, SC_obtener_dirección_local = 6, SC_obtener_dirección_remota = 7,
    SC_enviar = 9, SC_recibir = 10, SC_enviar_a_destino = 11, SC_recibir_con_dirección_de_origen = 12,
    SC_cerrar_sentido_de_comunicación = 13, SC_configurar_opción_del_extremo = 14
};

static long socket_call(long call, unsigned long *argumentos)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)argumentos, 0, 0, 0, 0));
}

uint16_t convertir_16_bits_a_orden_de_red(uint16_t valor) { return (uint16_t)((valor << 8) | (valor >> 8)); }
uint16_t convertir_16_bits_a_orden_de_máquina(uint16_t valor) { return convertir_16_bits_a_orden_de_red(valor); }
uint32_t convertir_32_bits_a_orden_de_red(uint32_t valor)
{
    return ((valor & 0x000000ffU) << 24) | ((valor & 0x0000ff00U) << 8) |
           ((valor & 0x00ff0000U) >> 8) | ((valor & 0xff000000U) >> 24);
}
uint32_t convertir_32_bits_a_orden_de_máquina(uint32_t valor) { return convertir_32_bits_a_orden_de_red(valor); }

int crear_extremo_de_comunicación(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_crear_extremo_de_comunicación, a);
}

int asociar_dirección_local(int descriptor_del_archivo, const struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección longitud)
{
    unsigned long a[3] = {(unsigned long)descriptor_del_archivo, (unsigned long)address, longitud};
    return (int)socket_call(SC_asociar_dirección_local, a);
}

int conectar_con_extremo_remoto(int descriptor_del_archivo, const struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección longitud)
{
    unsigned long a[3] = {(unsigned long)descriptor_del_archivo, (unsigned long)address, longitud};
    return (int)socket_call(SC_conectar_con_extremo_remoto, a);
}

int preparar_recepción_de_conexiones(int descriptor_del_archivo, int backlog)
{
    unsigned long a[2] = {(unsigned long)descriptor_del_archivo, (unsigned long)backlog};
    return (int)socket_call(SC_preparar_recepción_de_conexiones, a);
}

int aceptar_conexión(int descriptor_del_archivo, struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *longitud)
{
    unsigned long a[3] = {(unsigned long)descriptor_del_archivo, (unsigned long)address, (unsigned long)longitud};
    return (int)socket_call(SC_aceptar_conexión, a);
}

int obtener_dirección_local(int descriptor_del_archivo, struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *longitud)
{
    unsigned long a[3] = {(unsigned long)descriptor_del_archivo, (unsigned long)address, (unsigned long)longitud};
    return (int)socket_call(SC_obtener_dirección_local, a);
}

int obtener_dirección_remota(int descriptor_del_archivo, struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *longitud)
{
    unsigned long a[3] = {(unsigned long)descriptor_del_archivo, (unsigned long)address, (unsigned long)longitud};
    return (int)socket_call(SC_obtener_dirección_remota, a);
}

ssize_t enviar(int descriptor_del_archivo, const void *memoria_intermedia_de_transferencia_2, size_t longitud, int flags)
{
    unsigned long a[4] = {(unsigned long)descriptor_del_archivo, (unsigned long)memoria_intermedia_de_transferencia_2, longitud, (unsigned long)flags};
    return (ssize_t)socket_call(SC_enviar, a);
}

ssize_t recibir(int descriptor_del_archivo, void *memoria_intermedia_de_transferencia_2, size_t longitud, int flags)
{
    unsigned long a[4] = {(unsigned long)descriptor_del_archivo, (unsigned long)memoria_intermedia_de_transferencia_2, longitud, (unsigned long)flags};
    return (ssize_t)socket_call(SC_recibir, a);
}

ssize_t enviar_a_destino(int descriptor_del_archivo, const void *memoria_intermedia_de_transferencia_2, size_t longitud, int flags,
               const struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección address_length)
{
    unsigned long a[6] = {(unsigned long)descriptor_del_archivo, (unsigned long)memoria_intermedia_de_transferencia_2, longitud,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_enviar_a_destino, a);
}

ssize_t recibir_con_dirección_de_origen(int descriptor_del_archivo, void *memoria_intermedia_de_transferencia_2, size_t longitud, int flags,
                 struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *address_length)
{
    unsigned long a[6] = {(unsigned long)descriptor_del_archivo, (unsigned long)memoria_intermedia_de_transferencia_2, longitud,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_recibir_con_dirección_de_origen, a);
}

int cerrar_sentido_de_comunicación(int descriptor_del_archivo, int how)
{
    unsigned long a[2] = {(unsigned long)descriptor_del_archivo, (unsigned long)how};
    return (int)socket_call(SC_cerrar_sentido_de_comunicación, a);
}

int configurar_opción_del_extremo(int descriptor_del_archivo, int level, int option_name,
               const void *option_value, tipo_de_longitud_de_dirección option_len)
{
    unsigned long a[5] = {(unsigned long)descriptor_del_archivo, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_configurar_opción_del_extremo, a);
}
