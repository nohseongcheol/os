/* COSL: native console adapter. SSH protocol/crypto is provided by LGPL libassh.
 * No POSIX process, filesystem or socket helpers from libassh are linked.
 */
#include "दूरस्_थ_मूल्य.h"
#include "कूटलेखन_समर्थन.h"
#include "प्रोफाइल.h"
#include "../संचारजाळे_स्टॅक/संचारजाळे_स्टॅक.h"
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
extern uintptr_t बोर्ड_मिलिसेकंद(void);
extern uintptr_t बोर्ड_वर्णलिहा(uintptr_t);
static struct assh_context_s *संदर्भ_मूल्य;
static struct assh_session_s *कनेक्शन_e05f319b;
static struct assh_channel_s *चॅनल_प्रविष्टी;
static int ऐकणे_संचारटोक=-1,समकक्ष_मूल्य=-1,आहे_प्रमाणित,शेल_सुरूझालेले,आज्ञा_टाइप_करा,शेवट_करा_राज्य=-1,होईल_मिटवा,बूट_त्रुटी,शेल_प्रतीक्षारत;
static uintptr_t कनेक्शन_वेळ,पुन्हाजोडा_वेळ,बंदकरणे_वेळ;
static unsigned char आदान_ओळ[8192],प्रदान_ओळ[65536];
static unsigned आदान_शीर्ष,आदान_संख्या,प्रदान_शीर्ष,प्रदान_संख्या,मागील_प्रदान;
static void निदान_मूल्य(const char *शब्द_मजकूर,unsigned मूल्य) {
    while(*शब्द_मजकूर)बोर्ड_वर्णलिहा(*शब्द_मजकूर++);
    char अंक_मूल्य[12];unsigned संख्या=0;do{अंक_मूल्य[संख्या++]='0'+मूल्य%10;मूल्य/=10;}while(मूल्य);
    while(संख्या)बोर्ड_वर्णलिहा(अंक_मूल्य[--संख्या]);बोर्ड_वर्णलिहा(10);
}
static assh_status_t तयार_करणे_स्मृती(void *डेटा,void **पत्ता,size_t आकार,enum assh_alloc_type_e प्रकार_मूल्य) {
    (void)डेटा;(void)प्रकार_मूल्य;
    if(!आकार){दूरस्_थ_रिलीज(*पत्ता);*पत्ता=0;return ASSH_OK;}
    void *नवे_पत्ता=पुनर्वाटपकरा_दूरस्_थ(*पत्ता,आकार);
    if(!नवे_पत्ता)return ASSH_ERR_MEM;*पत्ता=नवे_पत्ता;return ASSH_OK;
}
static assh_status_t तयार_करणे_यादृच्छिक(struct assh_context_s *डेटा,const struct assh_buffer_s *सीड_मूल्य) {
    (void)डेटा;(void)सीड_मूल्य;unsigned char चाचण्या[32];int मोजमाप=दूरस्_थ_यादृच्छिक(चाचण्या,sizeof(चाचण्या));memset(चाचण्या,0,sizeof(चाचण्या));
    return मोजमाप?ASSH_ERR_CRYPTO:ASSH_OK;
}
static assh_status_t यादृच्छिक_वाचा(struct assh_context_s *डेटा,uint8_t *मोजमाप,size_t लांबी_मूल्य,uint_fast8_t प्रकार_मूल्य) {
    (void)डेटा;(void)प्रकार_मूल्य;if(लांबी_मूल्य>65536)return ASSH_ERR_CRYPTO;
    return दूरस्_थ_यादृच्छिक(मोजमाप,लांबी_मूल्य)?ASSH_ERR_CRYPTO:ASSH_OK;
}
static void यादृच्छिक_शेवट_करा(struct assh_context_s *डेटा){(void)डेटा;}
static const struct assh_prng_s यादृच्छिक_निर्माता={तयार_करणे_यादृच्छिक,यादृच्छिक_वाचा,यादृच्छिक_शेवट_करा};
static void कनेक्शन_मिटवा(void) {
    आहे_प्रमाणित=शेल_सुरूझालेले=0;चॅनल_प्रविष्टी=0;
    if(कनेक्शन_e05f319b)assh_session_release(कनेक्शन_e05f319b);कनेक्शन_e05f319b=0;
    if(समकक्ष_मूल्य>=0)संचारजाळे_मिटवा(समकक्ष_मूल्य);समकक्ष_मूल्य=-1;आज्ञा_टाइप_करा=0;शेवट_करा_राज्य=-1;होईल_मिटवा=0;
    आदान_शीर्ष=आदान_संख्या=प्रदान_शीर्ष=प्रदान_संख्या=मागील_प्रदान=0;पुन्हाजोडा_वेळ=बोर्ड_मिलिसेकंद()+250;
}
int फीड_दूरस्_थ_आदान(const unsigned char *डेटा,unsigned संख्या) {
    if(संख्या>sizeof(आदान_ओळ)-आदान_संख्या)return -11;
    for(unsigned क्रमांक_अनुक्रमणिका=0;क्रमांक_अनुक्रमणिका<संख्या;क्रमांक_अनुक्रमणिका++)आदान_ओळ[(आदान_शीर्ष+आदान_संख्या++)%sizeof(आदान_ओळ)]=डेटा[क्रमांक_अनुक्रमणिका];return संख्या;
}
int दूरस्_थ_आदान(void) {
    if(!आदान_संख्या)return -1;int वर्ण_मूल्य=आदान_ओळ[आदान_शीर्ष];आदान_शीर्ष=(आदान_शीर्ष+1)%sizeof(आदान_ओळ);आदान_संख्या--;return वर्ण_मूल्य;
}
void दूरस्_थ_प्रदान(unsigned char वर्ण_मूल्य) {
    if(!शेल_सुरूझालेले||होईल_मिटवा)return;
    unsigned शेवटीजोडा_मोड=वर्ण_मूल्य==10&&मागील_प्रदान!=13;
    if(प्रदान_संख्या+1+शेवटीजोडा_मोड>sizeof(प्रदान_ओळ)){होईल_मिटवा=2;return;}
    if(शेवटीजोडा_मोड)प्रदान_ओळ[(प्रदान_शीर्ष+प्रदान_संख्या++)%sizeof(प्रदान_ओळ)]=13;
    प्रदान_ओळ[(प्रदान_शीर्ष+प्रदान_संख्या++)%sizeof(प्रदान_ओळ)]=वर्ण_मूल्य;मागील_प्रदान=वर्ण_मूल्य;
}
uintptr_t बोर्ड_शेवट_करा_दूरस्_थ_आज्ञा(uintptr_t राज्य_मूल्य){if(शेल_सुरूझालेले&&आज्ञा_टाइप_करा)शेवट_करा_राज्य=(int)राज्य_मूल्य;return 0;}
uintptr_t बोर्ड_दूरस्_थ_प्रतीक्षा_करा(uintptr_t राज्य_मूल्य){शेल_प्रतीक्षारत=राज्य_मूल्य!=0;return 0;}
static int तयार_करणे_शेल(void) {
    if(ऐकणे_संचारटोक>=0)return 0;
    if(!संदर्भ_मूल्य){
        assh_status_t त्रुटी=assh_context_create(&संदर्भ_मूल्य,ASSH_SERVER,तयार_करणे_स्मृती,0,&यादृच्छिक_निर्माता,0);
        if(त्रुटी)return -5;
        /* Explicit allowlist: no CBC, chacha20-poly1305, SHA1 MAC or compression.
         * Classic AES-CTR + HMAC-SHA256 avoids the affected Terrapin modes.
         */
        const struct assh_algo_s *पद्धत_मोड[]={
            &assh_kex_builtin_sha2_nistp256.algo_wk.algo,
            &assh_sign_builtin_nistp256.algo_wk.algo,
            &assh_cipher_builtin_aes128_ctr.algo,
            &assh_mac_builtin_sha256.algo,&assh_compress_none.algo,0};
        त्रुटी=assh_algo_register(संदर्भ_मूल्य,ASSH_SAFETY_WEAK,पद्धत_मोड);
        if(!त्रुटी)त्रुटी=assh_service_register_va(संदर्भ_मूल्य,&assh_service_userauth_server,&assh_service_connection,NULL);
        const uint8_t *कळ_सामग्री=मोबाइल_कळ;
        if(!त्रुटी)त्रुटी=assh_key_load(संदर्भ_मूल्य,assh_context_keys(संदर्भ_मूल्य),&assh_key_builtin_ecdsa_nist,
            ASSH_ALGO_SIGN,ASSH_KEY_FMT_PV_PEM_ASN1,&कळ_सामग्री,sizeof(मोबाइल_कळ));
        if(त्रुटी){निदान_मूल्य("SSH init error ",त्रुटी);assh_context_release(संदर्भ_मूल्य);संदर्भ_मूल्य=0;return -5;}
    }
    int पॉर्ट_मूल्य=संचारद्वार_संचारटोक_तयार_करा(1);if(पॉर्ट_मूल्य<0)return पॉर्ट_मूल्य;पुनर्वापर_संचारद्वार_पत्ता(पॉर्ट_मूल्य);
    int मोजमाप=जाळे_बाइंड_करा(पॉर्ट_मूल्य,0,22);if(!मोजमाप)मोजमाप=जाळे_ऐका(पॉर्ट_मूल्य);
    if(मोजमाप<0){संचारजाळे_मिटवा(पॉर्ट_मूल्य);return मोजमाप;}ऐकणे_संचारटोक=पॉर्ट_मूल्य;return 0;
}
uintptr_t बोर्ड_शॅडोइंग(uintptr_t प्रकार_मूल्य,uintptr_t कृती) {
    if(प्रकार_मूल्य==1)return(uint32_t)नियंत्रण_दूरस्_थ_प्रदर्शन(कृती);
    if(कृती==0){कनेक्शन_मिटवा();if(ऐकणे_संचारटोक>=0)संचारजाळे_मिटवा(ऐकणे_संचारटोक);ऐकणे_संचारटोक=-1;return 0;}
    if(कृती==1){बूट_त्रुटी=तयार_करणे_शेल();return(uint32_t)बूट_त्रुटी;}
    return(uint32_t)(ऐकणे_संचारटोक>=0?1:बूट_त्रुटी);
}
void तयार_करणे_दूरस्_थ(void){बूट_त्रुटी=तयार_करणे_शेल();नियंत्रण_दूरस्_थ_प्रदर्शन(1);}
static int जुळणारे_शब्द(const struct assh_cbuffer_s *डेटा,const char *शब्द_मजकूर) {
    size_t लांबी_मूल्य=strlen(शब्द_मजकूर);return डेटा->size==लांबी_मूल्य&&!memcmp(डेटा->data,शब्द_मजकूर,लांबी_मूल्य);
}
static int टर्मिनल_विनंती(const struct assh_cbuffer_s *डेटा) {
    if(डेटा->size<24)return 0;
    const unsigned char *डेटा_स्थान=डेटा->data;unsigned लांबी_मूल्य=assh_load_u32(डेटा_स्थान);
    if(लांबी_मूल्य>128||डेटा->size<लांबी_मूल्य+24)return 0;
    unsigned मोड_मूल्य=assh_load_u32(डेटा_स्थान+4+लांबी_मूल्य+16);
    return मोड_मूल्य<=2048&&डेटा->size==लांबी_मूल्य+24+मोड_मूल्य;
}
static void हाताळा_विनंती(struct assh_event_request_s *इव्हेंट) {
    if(!आहे_प्रमाणित||इव्हेंट->ch!=चॅनल_प्रविष्टी||!चॅनल_प्रविष्टी)return;
    if(जुळणारे_शब्द(&इव्हेंट->type,"pty-req")) {
        if(!शेल_सुरूझालेले&&टर्मिनल_विनंती(&इव्हेंट->rq_data))इव्हेंट->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(जुळणारे_शब्द(&इव्हेंट->type,"window-change")) {
        if(शेल_सुरूझालेले&&इव्हेंट->rq_data.size==16)इव्हेंट->reply=ASSH_CONNECTION_REPLY_SUCCESS;
        return;
    }
    if(शेल_सुरूझालेले||!शेल_प्रतीक्षारत)return;
    const unsigned char *आदेश=0;unsigned लांबी_मूल्य=0;
    if(जुळणारे_शब्द(&इव्हेंट->type,"exec")) {
        if(इव्हेंट->rq_data.size<4)return;
        लांबी_मूल्य=assh_load_u32(इव्हेंट->rq_data.data);
        if(!लांबी_मूल्य||लांबी_मूल्य>2048||इव्हेंट->rq_data.size!=लांबी_मूल्य+4)return;
        आदेश=इव्हेंट->rq_data.data+4;
        for(unsigned क्रमांक_अनुक्रमणिका=0;क्रमांक_अनुक्रमणिका<लांबी_मूल्य;क्रमांक_अनुक्रमणिका++)if(!आदेश[क्रमांक_अनुक्रमणिका])return;
        आज्ञा_टाइप_करा=1;
    }else if(!जुळणारे_शब्द(&इव्हेंट->type,"shell")||इव्हेंट->rq_data.size)return;
    if(sizeof(आदान_ओळ)-आदान_संख्या<लांबी_मूल्य+2)return;
    const unsigned char पुसलेले_मूल्य=21,शेवट=13;
    फीड_दूरस्_थ_आदान(&पुसलेले_मूल्य,1);if(लांबी_मूल्य)फीड_दूरस्_थ_आदान(आदेश,लांबी_मूल्य);फीड_दूरस्_थ_आदान(&शेवट,1);
    शेल_सुरूझालेले=1;इव्हेंट->reply=ASSH_CONNECTION_REPLY_SUCCESS;
    if(!आज्ञा_टाइप_करा){const char *वापरमार्गदर्शिका_eb81d7d9="\r\njkoros SSH: shared native console; Ctrl-D disconnects.\r\n";while(*वापरमार्गदर्शिका_eb81d7d9)दूरस्_थ_प्रदान(*वापरमार्गदर्शिका_eb81d7d9++);}
}
void तपासा_दूरस्_थ(void) {
    तपासा_दूरस्_थ_प्रदर्शन();
    if(ऐकणे_संचारटोक<0)return;
    uintptr_t आत्ता_मूल्य=बोर्ड_मिलिसेकंद();
    if(समकक्ष_मूल्य<0){if(आत्ता_मूल्य<पुन्हाजोडा_वेळ)return;समकक्ष_मूल्य=जाळे_स्वीकारा(ऐकणे_संचारटोक);if(समकक्ष_मूल्य<0)return;
        कनेक्शन_वेळ=आत्ता_मूल्य;assh_status_t त्रुटी=assh_session_create(संदर्भ_मूल्य,&कनेक्शन_e05f319b);
        if(त्रुटी){कनेक्शन_e05f319b=0;निदान_मूल्य("SSH session error ",त्रुटी);कनेक्शन_मिटवा();return;}}
    if((!आहे_प्रमाणित&&आत्ता_मूल्य-कनेक्शन_वेळ>30000)||होईल_मिटवा==2||(होईल_मिटवा&&आत्ता_मूल्य>=बंदकरणे_वेळ)){कनेक्शन_मिटवा();return;}
    if(चॅनल_प्रविष्टी&&शेल_सुरूझालेले&&!होईल_मिटवा) {
        if(प्रदान_संख्या){size_t संख्या=sizeof(प्रदान_ओळ)-प्रदान_शीर्ष;if(संख्या>प्रदान_संख्या)संख्या=प्रदान_संख्या;if(संख्या>2048)संख्या=2048;
            assh_status_t त्रुटी=assh_channel_data(चॅनल_प्रविष्टी,प्रदान_ओळ+प्रदान_शीर्ष,&संख्या);
            if(!त्रुटी){प्रदान_शीर्ष=(प्रदान_शीर्ष+संख्या)%sizeof(प्रदान_ओळ);प्रदान_संख्या-=संख्या;}
            else if(त्रुटी!=ASSH_NO_DATA){कनेक्शन_मिटवा();return;}
        }
        if(शेवट_करा_राज्य>=0&&!प्रदान_संख्या){unsigned char राज्य_मूल्य[4];assh_store_u32(राज्य_मूल्य,(uint32_t)शेवट_करा_राज्य);
            if(assh_request(कनेक्शन_e05f319b,चॅनल_प्रविष्टी,"exit-status",11,राज्य_मूल्य,4,0)||assh_channel_eof(चॅनल_प्रविष्टी)||assh_channel_close(चॅनल_प्रविष्टी)) {कनेक्शन_मिटवा();return;}
            होईल_मिटवा=1;बंदकरणे_वेळ=आत्ता_मूल्य+3000;
        }
    }
    for(unsigned क्रम_मूल्य_e9fa7815=0;क्रम_मूल्य_e9fa7815<16;क्रम_मूल्य_e9fa7815++) {
        struct assh_event_s इव्हेंट;
        if(!assh_event_get(कनेक्शन_e05f319b,&इव्हेंट,आत्ता_मूल्य/1000)){कनेक्शन_मिटवा();return;}
        assh_status_t त्रुटी=ASSH_OK;int उर्वरित_क्षणभर=0,डिस्कनेक्ट_संचारटोक=0;
        switch(इव्हेंट.id) {
        case ASSH_EVENT_READ: {
            int संख्या=जाळे_वाचा(समकक्ष_मूल्य,इव्हेंट.transport.read.buf.data,इव्हेंट.transport.read.buf.size);
            if(संख्या>0)इव्हेंट.transport.read.transferred=संख्या;
            else if(संख्या==-11)उर्वरित_क्षणभर=1;else डिस्कनेक्ट_संचारटोक=1;
            break;
        }
        case ASSH_EVENT_WRITE: {
            int संख्या=जाळे_लिहा(समकक्ष_मूल्य,इव्हेंट.transport.write.buf.data,इव्हेंट.transport.write.buf.size);
            if(संख्या>0)इव्हेंट.transport.write.transferred=संख्या;
            else if(संख्या==-11)उर्वरित_क्षणभर=1;else डिस्कनेक्ट_संचारटोक=1;
            break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_METHODS:
            इव्हेंट.userauth_server.methods.methods=ASSH_USERAUTH_METHOD_PASSWORD;
            if(इव्हेंट.userauth_server.methods.retries>3)इव्हेंट.userauth_server.methods.retries=3;
            break;
        case ASSH_EVENT_USERAUTH_SERVER_PASSWORD: {
            struct assh_event_userauth_server_password_s *डेटा=&इव्हेंट.userauth_server.password;
            if(जुळणारे_शब्द(&डेटा->username,"user")&&डेटा->password.size<=256&&!डेटा->new_password.size) {
                unsigned char सारांश_मूल्य[32];दूरस्_थ_सारांश(डेटा->password.data,डेटा->password.size,सारांश_मूल्य);
                unsigned फरक_मूल्य=0;for(unsigned क्रमांक_अनुक्रमणिका=0;क्रमांक_अनुक्रमणिका<32;क्रमांक_अनुक्रमणिका++)फरक_मूल्य|=सारांश_मूल्य[क्रमांक_अनुक्रमणिका]^शेल_पासवर्ड_सारांश[क्रमांक_अनुक्रमणिका];memset(सारांश_मूल्य,0,32);
                if(!फरक_मूल्य)डेटा->result=ASSH_SERVER_PWSTATUS_SUCCESS;
            }break;
        }
        case ASSH_EVENT_USERAUTH_SERVER_SUCCESS: आहे_प्रमाणित=1;break;
        case ASSH_EVENT_CHANNEL_OPEN: {
            struct assh_event_channel_open_s *डेटा=&इव्हेंट.connection.channel_open;
            if(आहे_प्रमाणित&&!चॅनल_प्रविष्टी&&शेल_प्रतीक्षारत&&जुळणारे_शब्द(&डेटा->type,"session")&&!डेटा->rq_data.size) {
                डेटा->reply=ASSH_CONNECTION_REPLY_SUCCESS;डेटा->pkt_size=4096;
                डेटा->win_size=-1;चॅनल_प्रविष्टी=डेटा->ch;
            }break;
        }
        case ASSH_EVENT_REQUEST: हाताळा_विनंती(&इव्हेंट.connection.request);break;
        case ASSH_EVENT_CHANNEL_DATA: {
            struct assh_event_channel_data_s *डेटा=&इव्हेंट.connection.channel_data;
            if(!शेल_सुरूझालेले||डेटा->ch!=चॅनल_प्रविष्टी||डेटा->ext){डिस्कनेक्ट_संचारटोक=1;break;}
            unsigned संख्या=डेटा->data.size;if(संख्या>sizeof(आदान_ओळ)-आदान_संख्या)संख्या=sizeof(आदान_ओळ)-आदान_संख्या;
            for(unsigned क्रमांक_अनुक्रमणिका=0;क्रमांक_अनुक्रमणिका<संख्या;क्रमांक_अनुक्रमणिका++)if(डेटा->data.data[क्रमांक_अनुक्रमणिका]==4){शेवट_करा_राज्य=0;संख्या=क्रमांक_अनुक्रमणिका;डेटा->transferred=डेटा->data.size;break;}
            फीड_दूरस्_थ_आदान(डेटा->data.data,संख्या);if(!डेटा->transferred)डेटा->transferred=संख्या;
            if(!संख्या&&शेवट_करा_राज्य<0)उर्वरित_क्षणभर=1;
            break;
        }
        case ASSH_EVENT_CHANNEL_EOF: break; /* stdin EOF does not close stdout. */
        case ASSH_EVENT_CHANNEL_CLOSE:
        case ASSH_EVENT_CHANNEL_ABORT: चॅनल_प्रविष्टी=0;शेल_सुरूझालेले=0;होईल_मिटवा=1;बंदकरणे_वेळ=आत्ता_मूल्य+1000;break;
        case ASSH_EVENT_SESSION_ERROR: आहे_प्रमाणित=शेल_सुरूझालेले=0;निदान_मूल्य("SSH error ",इव्हेंट.session.error.code);डिस्कनेक्ट_संचारटोक=1;break;
        case ASSH_EVENT_DISCONNECT: डिस्कनेक्ट_संचारटोक=1;break;
        default: break;
        }
        assh_event_done(कनेक्शन_e05f319b,&इव्हेंट,त्रुटी);
        if(डिस्कनेक्ट_संचारटोक){कनेक्शन_मिटवा();return;}if(उर्वरित_क्षणभर)return;
    }
}
