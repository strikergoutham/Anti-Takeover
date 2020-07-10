# Anti-Takeover
Anti-Takeover is a sub domain monitoring tool for (blue/purple) team / internal security team which uses cloud flare. Currently Anti-Takeover monitors more than a dozen third party services for dangling subdomain pointers.


![Anti-Takeover](/Screenshots/antitakeover_1.PNG)

Anti-Takeover is a subdomain takeover monitoring tool But for Blue team/internal security team who manages DNS config on cloudflare. Currently it has capability to check 15+ external services for possible dangling/takeover issues.

## Features :

> Monitors more than a dozen external service pointed CNAME records for subdomain takeover issues.

> Capability to scan either a single cloudflare group or multiples one(single account).

> Capability to monitor for newly added sub domains.

> Integration with slack for realtime alerts/notification. 

## Architecture :

Rough high level architecture of the tool is shown below :

![Anti-Takeover](/Screenshots/antitakeover_2.PNG)

## Setup :

### Prerequisites :

>> Requires Python 3

>> Runs on both Windows / Linux .

>> install dependencies :
```bash
pip3 install requests
```
#### setup Environment variable CF_APIKEY with the cloudflare API key.
```bash
export CF_APIKEY="yourapikeyhere"
```
#### setup the required options in the config.conf file.
Example Config File :

```bash
[Properties]
CF_EMAIL = <Your_cloudflare_registered_email>  #REQUIRED 
CF_MonitorSingleAccount = false #REQUIRED values : false / true ( true : monitors only single CF account. false : monitors every account associated with email ID )          
CF_AccountID = <your_cloudflareAccountID>   #REQUIRED if CF_MonitorSingleAccount set to true
Monitor_Mode = 1      #REQUIRED ( values : 1 or 2 ( 1 - complete notification , 2 - delta notification )
slack_integration = true        #REQUIRED ( values : false / true (case sensitive) )
slack_Webhook = https://hooks.slack.com/services/yourslackwebhookurl  #REQUIRED if slack_integration is true
```



