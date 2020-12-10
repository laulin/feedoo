Feedo

# What is Feedo ? 

Feedo is a ETL, for Extract, Transform and Load. Basically; it gets data from files or database, process it thanks to pipelines and store data to a file or a database. It is very versatile and processing brick can be added without pain.

The purpose of Feedo is generic :

* ETL to convert database to another one
* Alerting like elastalert
* Gather information from agent like Fluentbit
* SIEM with correlation rule
* Intrusion detection thanks AI
* ...

The Feedo main purpose is for Security Operational Center (SOC). But I you need to play with data, you need Feedo as friend :)

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
Now exec feedo :

```bash

you@computer:>feedo
my_pypeline[1607608082]: {'log': 'my log'}

```
It works ! You ran your first *pipeline*.

# You said pipeline ?


