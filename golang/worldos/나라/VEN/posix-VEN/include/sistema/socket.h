#ifndef _include_sistema_socket
#define _include_sistema_socket

#include <definiciones_básicas.h>
#include <sistema/tipos_de_datos.h>

typedef unsigned short tipo_de_familia_de_direcciones;

struct dirección_de_extremo_de_comunicación {
    tipo_de_familia_de_direcciones familia_de_direcciones_del_extremo;
    char datos_de_dirección[14];
};

#define familia_de_direcciones_sin_especificar 0
#define código_de_familia_de_direcciones_entre_redes 2
#define familia_de_protocolos_entre_redes código_de_familia_de_direcciones_entre_redes

#define extremo_de_flujo_de_datos 1
#define extremo_de_datagramas 2

#define detener_recepción 0
#define detener_envío 1
#define detener_ambos_sentidos 2

#ifdef __cplusplus
extern "C" {
#endif
int crear_extremo_de_comunicación(int domain, int type, int protocol);
int asociar_dirección_local(int descriptor_del_archivo, const struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección address_len);
int conectar_con_extremo_remoto(int descriptor_del_archivo, const struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección address_len);
int preparar_recepción_de_conexiones(int descriptor_del_archivo, int backlog);
int aceptar_conexión(int descriptor_del_archivo, struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *address_len);
int obtener_dirección_local(int descriptor_del_archivo, struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *address_len);
int obtener_dirección_remota(int descriptor_del_archivo, struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *address_len);
ssize_t enviar(int descriptor_del_archivo, const void *memoria_intermedia_de_transferencia_2, size_t longitud, int flags);
ssize_t recibir(int descriptor_del_archivo, void *memoria_intermedia_de_transferencia_2, size_t longitud, int flags);
ssize_t enviar_a_destino(int descriptor_del_archivo, const void *message, size_t longitud, int flags,
               const struct dirección_de_extremo_de_comunicación *dest_addr, tipo_de_longitud_de_dirección dest_len);
ssize_t recibir_con_dirección_de_origen(int descriptor_del_archivo, void *memoria_intermedia_de_transferencia_2, size_t longitud, int flags,
                 struct dirección_de_extremo_de_comunicación *address, tipo_de_longitud_de_dirección *address_len);
int cerrar_sentido_de_comunicación(int descriptor_del_archivo, int how);
int configurar_opción_del_extremo(int descriptor_del_archivo, int level, int option_name,
               const void *option_value, tipo_de_longitud_de_dirección option_len);
#ifdef __cplusplus
}
#endif

#endif
