// Python -> SVC -> Java RAM files / loopback and external IPv4 UDP / framebuffer.
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/mperrno.h"
#include "invoke.h"
#include "NetworkABI.h"
static intptr_t checked(intptr_t result) { if (result < 0) mp_raise_OSError(-result); return result; }
static const char *pathArgument(mp_obj_t value) {
    size_t itemCount; const char *path = mp_obj_str_get_data(value, &itemCount);
    if (!itemCount || itemCount > 63) mp_raise_OSError(36 /* ENAMETOOLONG */);
    for (size_t ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) if (!path[ordinalIndex]) mp_raise_OSError(MP_EINVAL);
    return path;
}
static mp_obj_t readFile(mp_obj_t name) {
    intptr_t fileHandle = checked(userInvoke(3, (uintptr_t)pathArgument(name), 0, 0, 0, 0, 0));
    // Allocate before opening would need a maximum-sized buffer. Protect fd across allocation failure.
    nlr_buf_t nonLocalReturn;
    if (nlr_push(&nonLocalReturn) == 0) {
        size_t size = checked(userInvoke(9, fileHandle, 0, 0, 0, 0, 0));
        vstr_t data; vstr_init_len(&data, size);
        intptr_t result = userInvoke(2, fileHandle, (uintptr_t)data.buf, size, 0, 0, 0);
        checked(result); data.len = result;
        mp_obj_t value = mp_obj_new_bytes_from_vstr(&data);
        nlr_pop(); userInvoke(4, fileHandle, 0, 0, 0, 0, 0); return value;
    }
    userInvoke(4, fileHandle, 0, 0, 0, 0, 0); nlr_jump(nonLocalReturn.ret_val);
}
static MP_DEFINE_CONST_FUN_OBJ_1(fileReaderObject, readFile);
static mp_obj_t readStandardInput(mp_obj_t capacityLimit) {
    mp_int_t size=mp_obj_get_int(capacityLimit);
    if(size<0||size>16384) mp_raise_OSError(MP_EINVAL);
    vstr_t data; vstr_init_len(&data,size);
    intptr_t itemCount=userInvoke(2,0,(uintptr_t)data.buf,size,0,0,0);
    if(itemCount<0) { vstr_clear(&data); checked(itemCount); }
    data.len=itemCount; return mp_obj_new_bytes_from_vstr(&data);
}
static MP_DEFINE_CONST_FUN_OBJ_1(standardInputReaderObject, readStandardInput);
static mp_obj_t writeFile(mp_obj_t name, mp_obj_t contentValue) {
    const char *path = pathArgument(name);
    mp_buffer_info_t data; mp_get_buffer_raise(contentValue, &data, MP_BUFFER_READ);
    if (data.len > 16384) mp_raise_OSError(MP_EFBIG);
    intptr_t fileHandle = checked(userInvoke(3, (uintptr_t)path, 577, 0, 0, 0, 0));
    intptr_t entryCount = userInvoke(1, fileHandle, (uintptr_t)data.buf, data.len, 0, 0, 0);
    userInvoke(4, fileHandle, 0, 0, 0, 0, 0); return mp_obj_new_int(checked(entryCount));
}
static MP_DEFINE_CONST_FUN_OBJ_2(fileWriterObject, writeFile);
static mp_obj_t removeFile(mp_obj_t name) { checked(userInvoke(11, (uintptr_t)pathArgument(name), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(fileRemoverObject, removeFile);
static mp_obj_t paintRectangle(size_t itemCount, const mp_obj_t *argumentArray) {
    (void)itemCount; unsigned firstValue[5]; for (unsigned ordinalIndex = 0; ordinalIndex < 5; ordinalIndex++) firstValue[ordinalIndex] = mp_obj_get_int(argumentArray[ordinalIndex]);
    checked(screenRectangle(firstValue[0], firstValue[1], firstValue[2], firstValue[3], firstValue[4])); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(rectangleObject, 5, 5, paintRectangle);
static mp_obj_t readScreenSize(void) {
    mp_obj_t size[2] = {mp_obj_new_int(checked(readScreenWidth())), mp_obj_new_int(checked(readScreenHeight()))};
    return mp_obj_new_tuple(2, size);
}
static MP_DEFINE_CONST_FUN_OBJ_0(screenSizeObject, readScreenSize);
static mp_obj_t waitForScreenInput(void) { return mp_obj_new_int(checked(waitForScreenKey())); }
static MP_DEFINE_CONST_FUN_OBJ_0(screenWaitObject, waitForScreenInput);
static mp_obj_t clockValue(void) { return mp_obj_new_int_from_uint(userInvoke(7, 0, 0, 0, 0, 0, 0)); }
static MP_DEFINE_CONST_FUN_OBJ_0(clockObject, clockValue);
static mp_obj_t udpOpen(mp_obj_t portNumber) {
    int dataPosition = mp_obj_get_int(portNumber); if (dataPosition < 0 || dataPosition > 65535) mp_raise_OSError(MP_EINVAL);
    intptr_t fileHandle = checked(userInvoke(32, AF_INET, SOCK_DGRAM, 0, 0, 0, 0));
    struct pk_sockaddr_in firstValue = {0}; firstValue.sin_family = AF_INET; firstValue.sin_port = pk_htons(dataPosition); firstValue.sin_addr.s_addr = 0;
    intptr_t result = userInvoke(33, fileHandle, (uintptr_t)&firstValue, sizeof(firstValue), 0, 0, 0);
    if (result < 0) { userInvoke(4, fileHandle, 0, 0, 0, 0, 0); checked(result); }
    return mp_obj_new_int(fileHandle);
}
static MP_DEFINE_CONST_FUN_OBJ_1(udpOpenObj, udpOpen);
static mp_obj_t udpSend(mp_obj_t fileHandle, mp_obj_t portNumber, mp_obj_t contentValue) {
    int dataPosition = mp_obj_get_int(portNumber); if (dataPosition < 1 || dataPosition > 65535) mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data; mp_get_buffer_raise(contentValue, &data, MP_BUFFER_READ);
    struct pk_sockaddr_in firstValue = {0}; firstValue.sin_family = AF_INET; firstValue.sin_port = pk_htons(dataPosition); firstValue.sin_addr.s_addr = pk_htonl(0x7f000001);
    return mp_obj_new_int(checked(userInvoke(34, mp_obj_get_int(fileHandle), (uintptr_t)data.buf, data.len, 0, (uintptr_t)&firstValue, sizeof(firstValue))));
}
static MP_DEFINE_CONST_FUN_OBJ_3(udpSendObj, udpSend);
static uint32_t readInternetAddress(mp_obj_t value) {
    size_t lengthValue; const char *text=mp_obj_str_get_data(value,&lengthValue);
    unsigned currentPosition=0; uint32_t address=0;
    for(unsigned subpartValue=0;subpartValue<4;subpartValue++) {
        unsigned value=0,digitCount=0;
        while(currentPosition<lengthValue&&text[currentPosition]>='0'&&text[currentPosition]<='9') {
            value=value*10+text[currentPosition++]-'0'; if(++digitCount>3||value>255)mp_raise_OSError(MP_EINVAL);
        }
        if(!digitCount)mp_raise_OSError(MP_EINVAL);
        address=address<<8|value;
        if(subpartValue<3&&(currentPosition>=lengthValue||text[currentPosition++]!='.'))mp_raise_OSError(MP_EINVAL);
    }
    if(currentPosition!=lengthValue)mp_raise_OSError(MP_EINVAL);
    return address;
}
static mp_obj_t udpSendto(size_t entryCount, const mp_obj_t *argumentArray) {
    (void)entryCount; uint32_t address=readInternetAddress(argumentArray[1]);
    int portNumber=mp_obj_get_int(argumentArray[2]);if(portNumber<1||portNumber>65535)mp_raise_OSError(MP_EINVAL);
    mp_buffer_info_t data;mp_get_buffer_raise(argumentArray[3],&data,MP_BUFFER_READ);
    struct pk_sockaddr_in targetValue={0};targetValue.sin_family=AF_INET;targetValue.sin_port=pk_htons(portNumber);targetValue.sin_addr.s_addr=pk_htonl(address);
    return mp_obj_new_int(checked(userInvoke(34,mp_obj_get_int(argumentArray[0]),(uintptr_t)data.buf,data.len,0,(uintptr_t)&targetValue,sizeof(targetValue))));
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(udpSendtoObj,4,4,udpSendto);
static mp_obj_t udpRecv(mp_obj_t fileHandle) {
    unsigned char data[512]; struct pk_sockaddr_in peerValue; pk_socklen_t lengthData = sizeof(peerValue);
    intptr_t size = checked(userInvoke(35, mp_obj_get_int(fileHandle), (uintptr_t)data, 512, 0, (uintptr_t)&peerValue, (uintptr_t)&lengthData));
    mp_obj_t values[2] = {mp_obj_new_bytes(data, size), MP_OBJ_NEW_SMALL_INT(pk_htons(peerValue.sin_port))};
    return mp_obj_new_tuple(2, values);
}
static MP_DEFINE_CONST_FUN_OBJ_1(udpRecvObj, udpRecv);
static mp_obj_t udpClose(mp_obj_t fileHandle) { checked(userInvoke(4, mp_obj_get_int(fileHandle), 0, 0, 0, 0, 0)); return mp_const_none; }
static MP_DEFINE_CONST_FUN_OBJ_1(udpCloseObj, udpClose);
static mp_obj_t openStream(void) {
    return mp_obj_new_int(checked(userInvoke(32,InternetFamily,StreamNetwork,streamTransportProtocol,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_0(streamOpenerObject,openStream);
static mp_obj_t connectStream(mp_obj_t endpoint,mp_obj_t addressText,mp_obj_t index) {
    int portNumber=mp_obj_get_int(index); if(portNumber<1||portNumber>65535)mp_raise_OSError(MP_EINVAL);
    struct InternetSocketAddress address={0}; address.addressFamily=InternetFamily;
    address.portNumber=networkShort(portNumber); address.InternetAddress.addressValue=networkInteger(readInternetAddress(addressText));
    checked(userInvoke(37,mp_obj_get_int(endpoint),(uintptr_t)&address,sizeof(address),0,0,0));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(streamConnectorObject,connectStream);
static mp_obj_t readStream(mp_obj_t endpoint,mp_obj_t capacityLimit) {
    int lengthValue=mp_obj_get_int(capacityLimit); if(lengthValue<1||lengthValue>512)mp_raise_OSError(MP_EINVAL);
    unsigned char data[512];
    intptr_t itemCount=checked(userInvoke(2,mp_obj_get_int(endpoint),(uintptr_t)data,lengthValue,0,0,0));
    return mp_obj_new_bytes(data,itemCount);
}
static MP_DEFINE_CONST_FUN_OBJ_2(streamReaderObject,readStream);
static mp_obj_t writeStream(mp_obj_t endpoint,mp_obj_t contentValue) {
    mp_buffer_info_t data; mp_get_buffer_raise(contentValue,&data,MP_BUFFER_READ);
    return mp_obj_new_int(checked(userInvoke(1,mp_obj_get_int(endpoint),(uintptr_t)data.buf,data.len,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_2(streamWriterObject,writeStream);
static mp_obj_t waitTemporarily(mp_obj_t timeValue) {
    checked(userInvoke(17,mp_obj_get_int(timeValue),0,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(waitObject,waitTemporarily);
static mp_obj_t entryKind(mp_obj_t name) {
    return mp_obj_new_int(checked(userInvoke(18,(uintptr_t)pathArgument(name),0,0,0,0,0)));
}
static MP_DEFINE_CONST_FUN_OBJ_1(entryKindObject,entryKind);
static mp_obj_t createDirectory(mp_obj_t name) {
    checked(userInvoke(18,(uintptr_t)pathArgument(name),1,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(directoryCreatorObject,createDirectory);
static mp_obj_t removeDirectory(mp_obj_t name) {
    checked(userInvoke(18,(uintptr_t)pathArgument(name),2,0,0,0,0)); return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(directoryRemoverObject,removeDirectory);
static const mp_rom_map_elem_t moduleNames[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_jkoros) },
    { MP_ROM_QSTR(MP_QSTR_tcp_open), MP_ROM_PTR(&streamOpenerObject) },
    { MP_ROM_QSTR(MP_QSTR_tcp_connect), MP_ROM_PTR(&streamConnectorObject) },
    { MP_ROM_QSTR(MP_QSTR_tcp_read), MP_ROM_PTR(&streamReaderObject) },
    { MP_ROM_QSTR(MP_QSTR_tcp_write), MP_ROM_PTR(&streamWriterObject) },
    { MP_ROM_QSTR(MP_QSTR_sleep_ms), MP_ROM_PTR(&waitObject) },
    { MP_ROM_QSTR(MP_QSTR_path_kind), MP_ROM_PTR(&entryKindObject) },
    { MP_ROM_QSTR(MP_QSTR_mkdir), MP_ROM_PTR(&directoryCreatorObject) },
    { MP_ROM_QSTR(MP_QSTR_rmdir), MP_ROM_PTR(&directoryRemoverObject) },
    { MP_ROM_QSTR(MP_QSTR_stdin), MP_ROM_PTR(&standardInputReaderObject) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&fileReaderObject) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&fileWriterObject) },
    { MP_ROM_QSTR(MP_QSTR_remove), MP_ROM_PTR(&fileRemoverObject) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&rectangleObject) },
    { MP_ROM_QSTR(MP_QSTR_screen_size), MP_ROM_PTR(&screenSizeObject) },
    { MP_ROM_QSTR(MP_QSTR_wait_key), MP_ROM_PTR(&screenWaitObject) },
    { MP_ROM_QSTR(MP_QSTR_ticks_ms), MP_ROM_PTR(&clockObject) },
    { MP_ROM_QSTR(MP_QSTR_udp_open), MP_ROM_PTR(&udpOpenObj) },
    { MP_ROM_QSTR(MP_QSTR_udp_send), MP_ROM_PTR(&udpSendObj) },
    { MP_ROM_QSTR(MP_QSTR_udp_sendto), MP_ROM_PTR(&udpSendtoObj) },
    { MP_ROM_QSTR(MP_QSTR_udp_recv), MP_ROM_PTR(&udpRecvObj) },
    { MP_ROM_QSTR(MP_QSTR_udp_close), MP_ROM_PTR(&udpCloseObj) },
};
static MP_DEFINE_CONST_DICT(moduleGlobals, moduleNames);
const mp_obj_module_t jkoros_module = { .base = {&mp_type_module}, .globals = (mp_obj_dict_t *)&moduleGlobals };
MP_REGISTER_MODULE(MP_QSTR_jkoros, jkoros_module);
