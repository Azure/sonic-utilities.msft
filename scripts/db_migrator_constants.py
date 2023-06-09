RESTAPI = {
        "config": {
            "client_auth": "true", 
            "log_level": "info", 
            "allow_insecure": "false"
        }, 
        "certs": {
            "server_key": "/etc/sonic/credentials/restapiserver.key", 
            "ca_crt": "/etc/sonic/credentials/AME_ROOT_CERTIFICATE.pem", 
            "server_crt": "/etc/sonic/credentials/restapiserver.crt", 
            "client_crt_cname": "client.restapi.sonic.gbl"
        }
    }

TELEMETRY = {
    "gnmi": {
        "client_auth": "true", 
        "log_level": "2", 
        "port": "50051"
    }, 
    "certs": {
        "server_key": "/etc/sonic/telemetry/streamingtelemetryserver.key", 
        "ca_crt": "/etc/sonic/telemetry/dsmsroot.cer", 
        "server_crt": "/etc/sonic/telemetry/streamingtelemetryserver.cer"
    }
}

CONSOLE_SWITCH = {
    "console_mgmt": {
        "enabled": "no"
    }
}
