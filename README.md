![](images/logo_small.png?raw=true) Feedo 

![](images/sponsor.png?raw=true) Sponsored by [Spartan conseil](https://www.spartan-conseil.fr/)


# What is Feedo ? 

Feedo is a ETL, for Extract, Transform and Load. Basically; it gets data from files or database, process it thanks to pipelines and store data to a file or a database. It is very versatile and processing brick can be added without pain.

The purpose of Feedo is generic :

* ETL to convert database to another one
* Alerting like elastalert
* Gather information from agent like Fluentbit
* SIEM with correlation rule
* Intrusion detection thanks AI
* ...

The Feedo's design is for Security Operational Center (SOC). But I you need to play with data, you need Feedo as friend :)

# Why ?

They are many reasons why I decided to build Feedo.

Firstly, I work with RethinkDB (https://rethinkdb.com/) as main database. It is amazingly easy to use, with enough performance for my needs. But the main drawback is about community tools. Briefly, they are no connector to work with, especially with Fluentd ,Fluentbit or a clone of Elastalert. 

Here we are : the second point ! I really appreciate Fluent familiy, especially Fluentbit fully written in C. Nevertheless, a drawback arrive when we talk about plugins or modifications. I worked many years with Fluentd and it can become painful when you need something was not shipped with.

So a *sort* of **Python** version a Fluent with rules and easy extension seems to me a good idea !

# Installation

The installation is very easy :

```bash
pip3 install feedo
```

# First run

You just install Feedo and you want to test ? Let's do a basic example !

Create a file at */etc/feedo/default.yaml* and copy-paste that :

```yaml
pipelines:
  "pipeline#1":
    - name : input_dummy
      tag : "my_pypeline"
      data : {"log":"my log"}

    - name : output_stdout
      match : "*"
```
Now execute feedo :

```bash

you@computer:>feedo
my_pypeline[1607608082]: {'log': 'my log'}

```
It works ! You ran your first *pipeline*.

# You said pipeline ?

**Keep in mind previous example, I will reuse it now.**

The heart of the processing is based on *pipeline*. It is similar to *pipe* operator in Unix system : every action do a basic operation and forward data to the following action :


```bash

you@computer:>cat /var/log/auth.log | head | grep "sudo"

```

Feedo do processing like this but add a *tag* to data. This way following action can decide to process the data (if it *match*) or just forward it to the next action. Tag is added by the data producer ("my_pipeline" in input_dummy) and other action will try to match (" * " in output_stdout). In the Feedo context, we call data *Event*. Indeed diffent : Event contains data, called record (dict), an unix timestamp and the tag.

Actions are categorized in four case : input, output, filter and parser. 

## Input

Input produces events in the pipeline, including tag.

### input_dummy

It is useful for testing purpose and forward events base on dicts. 

parameters : 

* tag : events' tag
* data : a dict or a list of dict with fact

example:

```yaml
- name : input_dummy
  tag : "my_pypeline"
  data : {"log":"my log"}
```

### input_file

It watch a path and load file if :

* The file exists on the startup
* The file was create (written and closed)

parameters :

* tag : events' tag
* watch_path : the path watched, typically a directory
* path_pattern : provide a pattern which must match when a file is found with watch_path
* remove=False : remove the file once read

example:

```yaml
- name : input_file
  tag : "logs"
  watch_path : /var/log
  path_pattern : /var/log/stuff.*.log
```

### input_forward

Based on [Fluentbit-server-py](https://github.com/laulin/fluentbit-server-py), it allow to received event from Fluentbit agent using the forward protocol.
It support authentication using shared key and TLS. No tag parameter is available since it is provided by the agent.

parameters :

* host="localhost" : Used to bind socket server
* port=24224 : Port used to bind the server
* tls_enable=False : Used to enable TLS support
* key_file=None : if TLS enabled, path to the key file
* crt_file=None : if TLS enabled, path to the certificate file
* shared_key=None : defined a shared key between servers an nodes. If set, enable authentication
* server_hostname="" : define the hostname, useful for shared_key authentication

**Warning** : if you exposed the port to internet, use authentication and TLS. If you can, add firewall rule to decrease surface attack. BE CAREFUL !

example:

```yaml
- name : input_forward
  port: 24224
  host : 0.0.0.0
  tls_enable : true
  key_file : /etc/tls/foo.key
  crt_file : /etc/tls/foo.crt
  shared_key : my_pr1vate_sh4red_K3y
  server_hostname : foo.com
```

# icons

Thanks to flaticon.com !

<div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>