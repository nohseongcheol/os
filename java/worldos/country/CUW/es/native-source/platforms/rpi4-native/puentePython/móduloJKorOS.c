// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "invocar.h"
#include "ABIRed.h"
static intptr_t comprobado(intptr_t resultado) { if (resultado < 0) mp_raise_OSError(-resultado); return resultado; }
static const char *argumentoRuta(mp_obj_t valor) {
    size_t númeroElementosElementoLista; const char *ruta = mp_obj_str_get_data(valor, &númeroElementosElementoLista);
    if (!númeroElementosElementoLista || númeroElementosElementoLista > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) if (!ruta[índiceOrdinal]) mp_raise_OSError(MP_EINVAL);
    return ruta;
}
static mp_obj_t leerArchivo(mp_obj_t nombre) {
    intptr_t manejadorArchivo = comprobado(invocarUsuario(3, (uintptr_t)argumentoRuta(nombre), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t retornarLocalNoCondición;
    if (nlr_push(&retornarLocalNoCondición) == 0) {
        size_t tamaño = comprobado(invocarUsuario(9, manejadorArchivo, 0, 0, 0, 0, 0));
        vstr_t Datos; vstr_init_len(&Datos, tamaño);
        intptr_t resultado = invocarUsuario(2, manejadorArchivo, (uintptr_t)Datos.buf, tamaño, 0, 0, 0);
        comprobado(resultado); Datos.len = resultado;
        mp_obj_t valor = mp_obj_new_bytes_from_vstr(&Datos);
        nlr_pop(); invocarUsuario(4, manejadorArchivo, 0, 0, 0, 0, 0); return valor;
    }
    invocarUsuario(4, manejadorArchivo, 0, 0, 0, 0, 0); nlr_jump(retornarLocalNoCondición.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetoLectorArchivo, leerArchivo);
static mp_obj_t leerEntradaEstándar(mp_obj_t límiteCapacidad) {
    mp_int_t tamaño=mp_obj_get_int(límiteCapacidad);
    if(tamaño<0||tamaño>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t Datos; vstr_init_len(&Datos,tamaño);
    intptr_t númeroElementosElementoLista=invocarUsuario(2,0,(uintptr_t)Datos.buf,tamaño,0,0,0);
    if(númeroElementosElementoLista<0) { vstr_clear(&Datos); comprobado(númeroElementosElementoLista); }
    Datos.len=númeroElementosElementoLista; return mp_obj_new_bytes_from_vstr(&Datos);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetoLectorEntradaEstándar, leerEntradaEstándar);
static mp_obj_t escribirArchivo(mp_obj_t nombre, mp_obj_t valorContenidoValor) {
    const char *ruta = argumentoRuta(nombre);
    mp_buffer_info_t Datos; mp_get_buffer_raise(valorContenidoValor, &Datos, MP_BUFFER_READ);
    if (Datos.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t manejadorArchivo = comprobado(invocarUsuario(3, (uintptr_t)ruta, 577, 0, 0, 0, 0));
    intptr_t númeroElementosEntradaElemento = invocarUsuario(1, manejadorArchivo, (uintptr_t)Datos.buf, Datos.len, 0, 0, 0);
    invocarUsuario(4, manejadorArchivo, 0, 0, 0, 0, 0); return mp_obj_new_int(comprobado(númeroElementosEntradaElemento));
}
static MP_DEFINE_CONST_FUN_OBJ_2(objetoEscritorArchivo, escribirArchivo);
static mp_obj_t eliminarArchivo(mp_obj_t nombre) { comprobado(invocarUsuario(11, (uintptr_t)argumentoRuta(nombre), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(objetoEliminadorArchivo, eliminarArchivo);
static mp_obj_t rectánguloPintar(size_t númeroElementosElementoLista, const mp_obj_t *arregloArgumento) {
    (void)númeroElementosElementoLista; unsigned valorPrimero[5]; for (unsigned índiceOrdinal = 0; índiceOrdinal < 5; índiceOrdinal++) valorPrimero[índiceOrdinal] = mp_obj_get_int(arregloArgumento[índiceOrdinal]);
    comprobado(rectánguloPantalla(valorPrimero[0], valorPrimero[1], valorPrimero[2], valorPrimero[3], valorPrimero[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(objetoRectángulo, 5, 5, rectánguloPintar);
static mp_obj_t leerTamañoPantalla(void) {
    mp_obj_t tamaño[2] = {mp_obj_new_int(comprobado(leerAnchuraPantalla())), mp_obj_new_int(comprobado(leerAlturaPantalla()))};
    return mp_obj_new_tuple(2, tamaño);
}
static MP_DEFINE_CONST_FUN_OBJ_0(objetoTamañoPantalla, leerTamañoPantalla);
static mp_obj_t esperarEntradaPantallaPara(void) { return mp_obj_new_int(comprobado(esperarTeclaPantallaPara())); }
static MP_DEFINE_CONST_FUN_OBJ_0(objetoEsperarPantalla, esperarEntradaPantallaPara);
static mp_obj_t valorReloj(void) { return mp_obj_new_int_from_uint(invocarUsuario(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(objetoReloj, valorReloj);
static mp_obj_t abrirUDP(mp_obj_t númeroPuerto) {
    int posiciónDatos = mp_obj_get_int(númeroPuerto); if (posiciónDatos < 0 || posiciónDatos > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t manejadorArchivo = comprobado(invocarUsuario(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in valorPrimero = {0}; valorPrimero.sin_family = AF_INET; valorPrimero.sin_port = pk_htons(posiciónDatos); valorPrimero.sin_addr.s_addr = 0;
    intptr_t resultado = invocarUsuario(33, manejadorArchivo, (uintptr_t)&valorPrimero, sizeof(valorPrimero), 0, 0, 0);
    if (resultado < 0) { invocarUsuario(4, manejadorArchivo, 0, 0, 0, 0, 0); comprobado(resultado); }
    return mp_obj_new_int(manejadorArchivo);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetoValorAbrirUDP, abrirUDP);
static mp_obj_t enviarUDP(mp_obj_t manejadorArchivo, mp_obj_t númeroPuerto, mp_obj_t valorContenidoValor) {
    int posiciónDatos = mp_obj_get_int(númeroPuerto); if (posiciónDatos < 1 || posiciónDatos > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Datos; mp_get_buffer_raise(valorContenidoValor, &Datos, MP_BUFFER_READ);
    struct pk_sockaddr_in valorPrimero = {0}; valorPrimero.sin_family = AF_INET; valorPrimero.sin_port = pk_htons(posiciónDatos); valorPrimero.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(comprobado(invocarUsuario(34, mp_obj_get_int(manejadorArchivo), (uintptr_t)Datos.buf, Datos.len, 0, (uintptr_t)&valorPrimero, sizeof(valorPrimero))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(objetoValorEnviarUDP, enviarUDP);
static uint32_t leerDirecciónInternet(mp_obj_t valor) {
    size_t longitud; const char *texto=mp_obj_str_get_data(valor,&longitud);
    unsigned posiciónActual=0; uint32_t dirección=0;
    for(unsigned valorSubparte=0;valorSubparte<4;valorSubparte++) {
        unsigned valor=0,númeroElementosDígito=0;
        while(posiciónActual<longitud&&texto[posiciónActual]>='0'&&texto[posiciónActual]<='9') {
            valor=valor*10+texto[posiciónActual++]-'0'; if(++númeroElementosDígito>3||valor>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!númeroElementosDígito)mp_raise_OSError(MP_EINVAL);
        dirección=dirección<<8|valor;
        if(valorSubparte<3&&(posiciónActual>=longitud||texto[posiciónActual++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(posiciónActual!=longitud)mp_raise_OSError(MP_EINVAL);
    return dirección;
}
static mp_obj_t enviarAUDP(size_t númeroElementosEntradaElemento, const mp_obj_t *arregloArgumento) {
    (void)númeroElementosEntradaElemento; uint32_t dirección=leerDirecciónInternet(arregloArgumento[1]);
    int númeroPuerto=mp_obj_get_int(arregloArgumento[2]);if(númeroPuerto<1||númeroPuerto>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t Datos;mp_get_buffer_raise(arregloArgumento[3],&Datos,MP_BUFFER_READ);
    struct pk_sockaddr_in valorObjetivo={0};valorObjetivo.sin_family=AF_INET;valorObjetivo.sin_port=pk_htons(númeroPuerto);valorObjetivo.sin_addr.s_addr=pk_htonl(dirección);
    return mp_obj_new_int(comprobado(invocarUsuario(34,mp_obj_get_int(arregloArgumento[0]),(uintptr_t)Datos.buf,Datos.len,0,(uintptr_t)&valorObjetivo,sizeof(valorObjetivo))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(objetoValorEnviarAUDP,4,4,enviarAUDP);
static mp_obj_t operaciónRecepciónUDP(mp_obj_t manejadorArchivo) {
    unsigned char Datos[512]; struct pk_sockaddr_in valorParRed; pk_socklen_t datosLongitud = sizeof(valorParRed);
    intptr_t tamaño = comprobado(invocarUsuario(35, mp_obj_get_int(manejadorArchivo), (uintptr_t)Datos, 512, 0, (uintptr_t)&valorParRed, (uintptr_t)&datosLongitud));
    mp_obj_t valores[2] = {mp_obj_new_bytes(Datos, tamaño), MP_OBJ_NEW_SMALL_INT(pk_htons(valorParRed.sin_port))};
    return mp_obj_new_tuple(2, valores);
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetoValorOperaciónRecepciónUDP, operaciónRecepciónUDP);
static mp_obj_t cerrarUDP(mp_obj_t manejadorArchivo) { comprobado(invocarUsuario(4, mp_obj_get_int(manejadorArchivo), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(objetoValorCerrarUDP, cerrarUDP);
static mp_obj_t abrirFlujo(void) {
    return mp_obj_new_int(comprobado(invocarUsuario(32,FamiliaInternet,RedFlujo,protocoloTransporteFlujo,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(objetoAbridorFlujo,abrirFlujo);
static mp_obj_t conectarFlujo(mp_obj_t extremo,mp_obj_t textoDirección,mp_obj_t número) {
    int númeroPuerto=mp_obj_get_int(número); if(númeroPuerto<1||númeroPuerto>65535)mp_raise_OSError(MP_EINVAL);
    struct DirecciónConectorRedInternet dirección={0}; dirección.familiaDirección=FamiliaInternet;
    dirección.númeroPuerto=cortoRed(númeroPuerto); dirección.DirecciónInternet.valorDirección=enteroValorRed(leerDirecciónInternet(textoDirección));
    comprobado(invocarUsuario(37,mp_obj_get_int(extremo),(uintptr_t)&dirección,sizeof(dirección),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(objetoConectorFlujo,conectarFlujo);
static mp_obj_t leerFlujo(mp_obj_t extremo,mp_obj_t límiteCapacidad) {
    int longitud=mp_obj_get_int(límiteCapacidad); if(longitud<1||longitud>512)mp_raise_OSError(MP_EINVAL);
    unsigned char Datos[512];
    intptr_t númeroElementosElementoLista=comprobado(invocarUsuario(2,mp_obj_get_int(extremo),(uintptr_t)Datos,longitud,0,0,0));
    return mp_obj_new_bytes(Datos,númeroElementosElementoLista);
}
static MP_DEFINE_CONST_FUN_OBJ_2(objetoLectorFlujo,leerFlujo);
static mp_obj_t escribirFlujo(mp_obj_t extremo,mp_obj_t valorContenidoValor) {
    mp_buffer_info_t Datos; mp_get_buffer_raise(valorContenidoValor,&Datos,MP_BUFFER_READ);
    return mp_obj_new_int(comprobado(invocarUsuario(1,mp_obj_get_int(extremo),(uintptr_t)Datos.buf,Datos.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(objetoEscritorFlujo,escribirFlujo);
static mp_obj_t esperarTemporalmente(mp_obj_t valorTiempo) {
    comprobado(invocarUsuario(17,mp_obj_get_int(valorTiempo),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(esperarObjeto,esperarTemporalmente);
static mp_obj_t claseTipoEntradaElemento(mp_obj_t nombre) {
    return mp_obj_new_int(comprobado(invocarUsuario(18,(uintptr_t)argumentoRuta(nombre),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetoClaseTipoEntradaElemento,claseTipoEntradaElemento);
static mp_obj_t crearDirectorio(mp_obj_t nombre) {
    comprobado(invocarUsuario(18,(uintptr_t)argumentoRuta(nombre),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetoCreadorDirectorio,crearDirectorio);
static mp_obj_t eliminarDirectorio(mp_obj_t nombre) {
    comprobado(invocarUsuario(18,(uintptr_t)argumentoRuta(nombre),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(objetoEliminadorDirectorio,eliminarDirectorio);
static const mp_rom_map_elem_t nombresMódulo[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&objetoAbridorFlujo) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&objetoConectorFlujo) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&objetoLectorFlujo) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&objetoEscritorFlujo) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&esperarObjeto) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&objetoClaseTipoEntradaElemento) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&objetoCreadorDirectorio) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&objetoEliminadorDirectorio) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&objetoLectorEntradaEstándar) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&objetoLectorArchivo) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&objetoEscritorArchivo) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&objetoEliminadorArchivo) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&objetoRectángulo) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&objetoTamañoPantalla) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&objetoEsperarPantalla) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&objetoReloj) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&objetoValorAbrirUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&objetoValorEnviarUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&objetoValorEnviarAUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&objetoValorOperaciónRecepciónUDP) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&objetoValorCerrarUDP) },
};
static MP_DEFINE_CONST_DICT(variablesGlobalesMódulo, nombresMódulo);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&variablesGlobalesMódulo };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
