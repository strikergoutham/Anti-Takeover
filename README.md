# Anti-Takeover
Anti-Takeover is a sub domain monitoring tool for (blue/purple) team / internal security team which uses cloud flare. Currently Anti-Takeover monitors more than a dozen third party services for dangling subdomain pointers.


![Anti-Takeover](/Screenshots/antitakeover_1.PNG)

Anti-Takeover is a subdomain takeover monitoring tool But for Blue team/internal security team who manages DNS config on cloudflare. Currently it has capability to check 15+ external services for possible dangling/takeover issues.

## Features :

> Monitors more than a dozen external service pointed CNAME records for subdomain takeover issues.

> Capability to scan either a single cloudflare group or multiples one(single account).

> Capability to monitor for newly added sub domains.

> Integration with slack for realtime alerts/notification. 

## Overview :

Rough high level Overview of the tool is shown below :

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
#### Option Details :
##### CF_EMAIL - This is the email associated with the cloudflare account.

##### CF_MonitorSingleAccount - 

                          Values :
                                    > true
                                    > false
                          Description : 
                                    if set to false, one needs to provide cloud flare account ID specifically in ####CF_AccountID for which monitoring is required. By default , /its set to true. which monitors all accounts which are associated with the email.
##### CF_AccountID -

                          Values: AccountID of the cloudflare which requires monitoring.
                          Description :
                                      This needs to be provided if CF_MonitorSIngleAccount is set to true.
##### Monitor_Mode - 
                          Values:
                                > 1
                                > 2
                          Description :
                                  if set to '1', for each scan, all the dangling/ misconfigured cname results are notified to the user.
                                  if set to '2', Only newly added cnames which are misconfigured which were not present in previous scans are notified / alerted. ( for base scan /first scan even if value is set to 2, it does a full scan.)
                                  
##### slack_integration - 
                          Values:
                                > true
                                > false
                                
                           Description :
                                  If value is set to 'true' slack alerts / notifications are trigerred.
                                  if set to 'false' slack notifications are disabled.

##### slack_Webhook -
                          Values : slack web hook URL.
                          
                          Description : Slack web Hook URL generated for recieving incoming messages from anti-takeover.This is mandatory if slack_integration is set to value /'true'.
                                  
##### Note: All options are case sensitive!

#### Now you are ready to run Auto-Takeover! Set it up as cron job for real time monitoring or run it as a standalone script.

        >> Results are stored in files named "edgecases.json" and "vulnerable.json". ( Edge case scenarios are stored in edgecases.json.)
        >> Removing both the files after the base scan / any scan , triggers in full scan .
        
#### Snapshot of test results:
![Anti-Takeover](/Screenshots/antitakeover_3.PNG)
        
        
Feel free to Fork the project, contribute, add new rules / notify for addition of new subdomains.( will be updated over the time.)        

##### Developed with ♥️ by: Goutham Madhwaraj
##### Do not use this tool for any malicious purpose. I am not responsible for any damage you cause / any non desirable consequences with the help of this tool.
