$TTL 86400
@   IN  SOA ns.sec.com. hostmaster.sec.com. (
        2024062001 ; Serial (YYYYMMDDNN format)
        3600       ; Refresh
        1800       ; Retry
        604800     ; Expire
        86400 )    ; Minimum TTL
@       IN  NS      ns.sec.com.
ns      IN  A       127.0.0.1
@       IN  A       127.0.0.1
