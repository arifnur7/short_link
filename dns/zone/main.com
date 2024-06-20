$TTL    604800
@       IN      SOA     ns.main.com. hostmaster.main.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ns.main.com.
ns      IN      A       127.0.0.1
