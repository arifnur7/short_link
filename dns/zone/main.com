$ttl 86400
@      IN      SOA  ns.main.com. hostmaster.main.com.(
                    202 ; Serial
                    600 ; Refresh
                    3600 ; Retry
                    12378237) ; Expire

@      IN      NS  ns.name.com.
ns     IN      A   127.0.0.1