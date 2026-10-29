/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "remoteValue.h"
#include "cryptographySupport.h"
#include "profile.h"
#include "../networkStack/networkStack.h"
/* The allocator/PRNG module descriptors are part of this pinned port's ABI. */
#define ASSH_PV
#include <assh/assh_session.h>
#include <assh/assh_context.h>
#include <assh/assh_service.h>
#include <assh/assh_transport.h>
#include <assh/assh_userauth_server.h>
#include <assh/assh_connection.h>
#include <assh/assh_kex.h>
#include <assh/assh_key.h>
#include <assh/assh_sign.h>
#include <assh/assh_cipher.h>
#include <assh/assh_mac.h>
#include <assh/assh_compress.h>
#include <assh/assh_alloc.h>
#include <assh/assh_prng.h>
#include <assh/mod_builtin.h>
#include <assh/assh_event.h>
#include <string.h>
extern uintptr_t boardMillis(void);
extern uintptr_t boardPutc(uintptr_t);
static struct assh_context_s *contextValue;
static struct assh_session_s *connection;
static struct assh_channel_s *channelEntry;
static int listeningEndpoint=-1,peerValue=-1,isAuthenticated,shellStarted,commandType,endState=-1,willClose,startupError,shellWaiting;
static uintptr_t connectionTime,reconnectTime,closingTime;
static unsigned char inputLine[8192],outputLine[65536];
static unsigned inputHead,inputCount,outputHead,outputCount,previousOutput;
static void diagnosticValue(const char *wordText,unsigned value) {
    while(*wordText)boardPutc(*wordText++);
    char digitValue[12];unsigned number=0;do{digitValue[number++]='0'+value%10;value/=10;}while(value);
    while(number)boardPutc(digitValue[--number]);boardPutc(10);
}
static assh_status_t prepareMemory(void *data,void **address,size_t size,enum assh_alloc_type_e kindValue) {
    (void)data;(void)kindValue;
    if(!size){releaseRemote(*address);*address=0;return ASSH_OK;}
    void *newAddress=reallocateRemote(*address,size);
    if(!newAddress)return ASSH_ERR_MEM;*address=newAddress;return ASSH_OK;
}
static assh_status_t prepareRandom(struct assh_context_s *data,const struct assh_buffer_s *seedValue) {
    (void)data;(void)seedValue;unsigned char tests[32];int result=remoteRandom(tests,sizeof(tests));memset(tests,0,sizeof(tests));
    return result?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t readRandom(struct assh_context_s *data,uint8_t *result,size_t lengthValue,uint_fast8_t kindValue) {
    (void)data;(void)kindValue;if(lengthValue>65536)return ASSH_ERR_CRYPTO;
    return remoteRandom(result,lengthValue)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void randomEnd(struct assh_context_s *data){(void)data;}
static const struct assh_prng_s randomGenerator={prepareRandom,readRandom,randomEnd};
static void closeConnection(void) {
    isAuthenticated=shellStarted=0;channelEntry=0;
    if(connection)assh_session_release(connection);connection=0;
    if(peerValue>=0)closeNetwork(peerValue);peerValue=-1;commandType=0;endState=-1;willClose=0;
    inputHead=inputCount=outputHead=outputCount=previousOutput=0;reconnectTime=boardMillis()+250;
}
int feedRemoteInput(const unsigned char *data,unsigned number) {
    if(number>sizeof(inputLine)-inputCount)return -11;
    for(unsigned ordinalIndex=0;ordinalIndex<number;ordinalIndex++)inputLine[(inputHead+inputCount++)%sizeof(inputLine)]=data[ordinalIndex];return number;
}
int remoteInput(void) {
    if(!inputCount)return -1;int characterValue=inputLine[inputHead];inputHead=(inputHead+1)%sizeof(inputLine);inputCount--;return characterValue;
}
void remoteOutput(unsigned char characterValue) {
    if(!shellStarted||willClose)return;
    unsigned appendMode=characterValue==10&&previousOutput!=13;
    if(outputCount+1+appendMode>sizeof(outputLine)){willClose=2;return;}
    if(appendMode)outputLine[(outputHead+outputCount++)%sizeof(outputLine)]=13;
    outputLine[(outputHead+outputCount++)%sizeof(outputLine)]=characterValue;previousOutput=characterValue;
}
uintptr_t boardEndRemoteCommand(uintptr_t stateValue){if(shellStarted&&commandType)endState=(int)stateValue;return 0;}
uintptr_t boardRemoteWait(uintptr_t stateValue){shellWaiting=stateValue!=0;return 0;}
static int prepareShell(void) {
    if(listeningEndpoint>=0)return 0;
    if(!contextValue){
        assh_status_t error=assh_context_create(&contextValue,ASSH_SERVER,prepareMemory,0,&randomGenerator,0);
        if(error)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *methodMode[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        error=assh_algo_register(contextValue,ASSH_SAFETY_WEAK,methodMode);
        if(!error)error=assh_service_register_va(contextValue,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *keyMaterial=deviceKey;
        if(!error)error=assh_key_load(contextValue,assh_context_keys(contextValue),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&keyMaterial,sizeof(deviceKey));
        if(error){diagnosticValue("SSH init error ",error);assh_context_release(contextValue);contextValue=0;return -5;}
    }
    int portValue=createSocketEndpoint(1);if(portValue<0)return portValue;reuseSocketAddress(portValue);
    int result=netBind(portValue,0,22);if(!result)result=netListen(portValue);
    if(result<0){closeNetwork(portValue);return result;}listeningEndpoint=portValue;return 0;
}
uintptr_t boardRemoteControl(uintptr_t kindValue,uintptr_t action) {
    if(kindValue==1)return(uint32_t)controlRemoteDisplay(action);
    if(action==0){closeConnection();if(listeningEndpoint>=0)closeNetwork(listeningEndpoint);listeningEndpoint=-1;return 0;}
    if(action==1){startupError=prepareShell();return(uint32_t)startupError;}
    return(uint32_t)(listeningEndpoint>=0?1:startupError);
}
void prepareRemote(void){startupError=prepareShell();controlRemoteDisplay(1);}
static int matchingWord(const struct assh_cbuffer_s *data,const char *wordText) {
    size_t lengthValue=strlen(wordText);return data->size==lengthValue&&!memcmp(data->data,wordText,lengthValue);
}
static int terminalRequest(const struct assh_cbuffer_s *data) {
    if(data->size<24)return 0;
    const unsigned char *dataPosition=data->data;unsigned lengthValue=assh_load_u32(dataPosition);
    if(lengthValue>128||data->size<lengthValue+24)return 0;
    unsigned modeValue=assh_load_u32(dataPosition+4+lengthValue+16);
    return modeValue<=2048&&data->size==lengthValue+24+modeValue;
}
static void handleRequest(struct assh_event_request_s *event) {
    if(!isAuthenticated||event->ch!=channelEntry||!channelEntry)return;
    if(matchingWord(&event->type,"pty-req")) {
        if(!shellStarted&&terminalRequest(&event->rq_data))event->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(matchingWord(&event->type,"window-change")) {
        if(shellStarted&&event->rq_data.size==16)event->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(shellStarted||!shellWaiting)return;
    const unsigned char *command=0;unsigned lengthValue=0;
    if(matchingWord(&event->type,"exec")) {
        if(event->rq_data.size<4)return;
        lengthValue=assh_load_u32(event->rq_data.data);
        if(!lengthValue||lengthValue>2048||event->rq_data.size!=lengthValue+4)return;
        command=event->rq_data.data+4;
        for(unsigned ordinalIndex=0;ordinalIndex<lengthValue;ordinalIndex++)if(!command[ordinalIndex])return;
        commandType=1;
    }else if(!matchingWord(&event->type,"shell")||event->rq_data.size)return;
    if(sizeof(inputLine)-inputCount<lengthValue+2)return;
    const unsigned char erasedValue=21,ending=13;
    feedRemoteInput(&erasedValue,1);if(lengthValue)feedRemoteInput(command,lengthValue);feedRemoteInput(&ending,1);
    shellStarted=1;event->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!commandType){const char *README="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*README)remoteOutput(*README++);}
}
void inspectRemote(void) {
    inspectRemoteDisplay();
    if(listeningEndpoint<0)return;
    uintptr_t nowValue=boardMillis();
    if(peerValue<0){if(nowValue<reconnectTime)return;peerValue=netAccept(listeningEndpoint);if(peerValue<0)return;
        connectionTime=nowValue;assh_status_t error=assh_session_create(contextValue,&connection);
        if(error){connection=0;diagnosticValue("SSH session error ",error);closeConnection();return;}}
    if((!isAuthenticated&&nowValue-connectionTime>30000)||willClose==2||(willClose&&nowValue>=closingTime)){closeConnection();return;}
    if(channelEntry&&shellStarted&&!willClose) {
        if(outputCount){size_t number=sizeof(outputLine)-outputHead;if(number>outputCount)number=outputCount;if(number>2048)number=2048;
            assh_status_t error=assh_channel_data(channelEntry,outputLine+outputHead,&number);
            if(!error){outputHead=(outputHead+number)%sizeof(outputLine);outputCount-=number;}
            else if(error!=ASSH_NO_DATA){closeConnection();return;}
        }
        if(endState>=0&&!outputCount){unsigned char stateValue[4];assh_store_u32(stateValue,(uint32_t)endState);
            if(assh_request(connection,channelEntry,"exit-status",11,stateValue,4,0)||assh_channel_eof(channelEntry)||assh_channel_close(channelEntry)) {closeConnection();return;}
            willClose=1;closingTime=nowValue+3000;
        }
    }
    for(unsigned sequenceValue=0;sequenceValue<16;sequenceValue++) {
        struct assh_event_s event;
        if(!assh_event_get(connection,&event,nowValue/1000)){closeConnection();return;}
        assh_status_t error=ASSH_OK;int restBriefly=0,disconnectEndpoint=0;
        switch(event.id) {
        case ASSH_EVENT_READ: {
            int number=netRead(peerValue,event.transport.read.buf.data,event.transport.read.buf.size);
            if(number>0)event.transport.read.transferred=number;
            else if(number==-11)restBriefly=1;else disconnectEndpoint=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int number=netWrite(peerValue,event.transport.write.buf.data,event.transport.write.buf.size);
            if(number>0)event.transport.write.transferred=number;
            else if(number==-11)restBriefly=1;else disconnectEndpoint=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            event.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(event.userauth_server.methods.retries>3)event.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *data=&event.userauth_server.password;
            if(matchingWord(&data->username,"user")&&data->password.size<=256&&!data->new_password.size) {
                unsigned char summaryValue[32];remoteSummary(data->password.data,data->password.size,summaryValue);
                unsigned differenceValue=0;for(unsigned ordinalIndex=0;ordinalIndex<32;ordinalIndex++)differenceValue|=summaryValue[ordinalIndex]^shellPasswordSummary[ordinalIndex];memset(summaryValue,0,32);
                if(!differenceValue)data->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: isAuthenticated=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *data=&event.connection.channel_open;
            if(isAuthenticated&&!channelEntry&&shellWaiting&&matchingWord(&data->type,"session")&&!data->rq_data.size) {
                data->reply=ASSH_CONNECTION_REPLY_SUCCESS;data->pkt_size=4096;
                data->win_size=-1;channelEntry=data->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: handleRequest(&event.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *data=&event.connection.channel_data;
            if(!shellStarted||data->ch!=channelEntry||data->ext){disconnectEndpoint=1;break;}
            unsigned number=data->data.size;if(number>sizeof(inputLine)-inputCount)number=sizeof(inputLine)-inputCount;
            for(unsigned ordinalIndex=0;ordinalIndex<number;ordinalIndex++)if(data->data.data[ordinalIndex]==4){endState=0;number=ordinalIndex;data->transferred=data->data.size;break;}
            feedRemoteInput(data->data.data,number);if(!data->transferred)data->transferred=number;
            if(!number&&endState<0)restBriefly=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: channelEntry=0;shellStarted=0;willClose=1;closingTime=nowValue+1000;break;
        case ASSH_EVENT_SESSION_ERROR: isAuthenticated=shellStarted=0;diagnosticValue("SSH error ",event.session.error.code);disconnectEndpoint=1;break;
        case ASSH_EVENT_DISCONNECT: disconnectEndpoint=1;break;
        default: break;
        }
        assh_event_done(connection,&event,error);
        if(disconnectEndpoint){closeConnection();return;}if(restBriefly)return;
    }
}
