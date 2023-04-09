# Wake Me Up Before You Go-Go


Category: Web

Difficulty: Medium 

Flag: `TG23{y0u_d1d_n0t_w4k3_m3_up}`

## Description

Deserialization vuln in php 7.0.9. CVE-2016-7124

## Requirments

Nothing

## Challenge solving 
Deserialization vuln in php 7.0.9. If you send in a serialized object with more attributes than in the class, it
will skip the __wakeup() function and skip to the destruct function.


