# Anti-Takeover
Anti-Takeover is a sub domain monitoring tool for (blue/purple) team / internal security team which uses cloud flare. Currently Anti-Takeover monitors more than a dozen third party services for dangling subdomain pointers.


![Anti-Takeover](/Screenshots/antitakeover_1.PNG)

Anti-Takeover is a subdomain takeover monitoring tool But for Blue team/internal security team who manages DNS config on cloudflare. Currently it has capability to check 15+ external services for possible dangling/takeover issues.

## Features:

> Monitors more than a dozen external service pointed CNAME records for subdomain takeover issues.

> Capability to scan either a single cloudflare group or multiples one(single account).

> Capability to monitor for newly added sub domains.

> Integration with slack for realtime alerts/notification. 

## Architecture

Rough high level architecture of the tool is shown below :

![Anti-Takeover](/Screenshots/antitakeover_2.PNG)
