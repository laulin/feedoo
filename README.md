![](images/logo_small.png?raw=true) feedoo 

![](images/sponsor.png?raw=true) Sponsored by [Spartan conseil](https://www.spartan-conseil.fr/)


# What is feedoo ? 

feedoo is an ETL, for Extract, Transform and Load. Basically, it gets data from files or database, process it thanks to pipelines and store data to a file or a database. It is very versatile and processing brick can be added without pain.

The purpose of feedoo is generic :

* ETL to convert database to another one
* Alerting like elastalert
* Gather information from agent like Fluentbit
* SIEM with correlation rule
* Intrusion detection thanks AI
* ...

The feedoo's design is for **S**ecurity **O**perational **C**enter (**SOC**). But if you need to play with data, you need feedoo as friend :)

# Why ?

They are many reasons why I decided to build feedoo.

Firstly, I work with [RethinkDB](https://rethinkdb.com/) as main database. It is amazingly easy to use, with enough performance for my needs. But the main drawback is about community tools. Briefly, they are no connector to work with, especially with Fluentd, Fluentbit or a clone of Elastalert. 

Here we are: the second point ! I really appreciate Fluent family, especially Fluentbit fully written in C. Nevertheless, a drawback arrive when we talk about plugins or modifications. I worked many years with Fluentd and it can become painful when you need something was not shipped with.

So a *sort* of **Python** version a Fluent with rules and easy extension seems to me a good idea !

# Installation

The installation is very easy :

```bash
pip3 install feedoo
```

# First run

You just install feedoo and you want to test ? Let's do a basic example !

Create a file at `/etc/feedoo/default.yaml` and copy-paste that :

```yaml
pipelines:
  "pipeline#1":
    - name : input_dummy
      tag : "my_pypeline"
      data : {"log":"my log"}

    - name : output_stdout
      match : "*"
```
Now execute feedoo :

```bash
you@computer:>feedoo
my_pypeline[1607608082]: {'log': 'my log'}
```
It works ! :tada: You ran your first _**pipeline**_.

# You said pipeline ?

**Keep in mind previous example, I will reuse it now.**

The heart of the processing is based on _**pipeline**_. It is similar to _**pipe**_ operator in Unix system : every action do a basic operation and forward data to the following action :


```bash
you@computer:>cat /var/log/auth.log | head | grep "sudo"
```

feedoo do processing like this but add a _tag_ to data. This way following action can decide to process the data (if it _match_) or just forward it to the next action. Tag is added by the data producer ("my_pipeline" in input_dummy) and other action will try to match (" * " in output_stdout). In the feedoo context, we call data *Event*. Indeed diffent : Event contains data, called record (dict), an unix timestamp and the tag.

Actions are categorized in four cases : 
1. input
1. output
1. filter
1. parser

## Input

Input produces events in the pipeline, including tag. If an input receives a event it forwards it to next action.

### input_dummy

It is useful for testing purpose and forward events base on dicts. 

Parameters : 

* `tag` : events' tag
* `data` : a dict or a list of dict with fact

Example:

```yaml
- name : input_dummy
  tag : "my_pypeline"
  data : {"log":"my log"}
```

### input_file

It watch a path and load file if :

* The file exists on the startup
* The file was create (written and closed)

Parameters :

* `tag` : events' tag
* `watch_path` : the path watched, typically a directory
* `path_pattern` : provide a pattern which must match when a file is found with watch_path
* `remove=False` : remove the file once read

Example:

```yaml
- name : input_file
  tag : "logs"
  watch_path : /var/log
  path_pattern : /var/log/stuff.*.log
```

### input_forward

Based on [Fluentbit-server-py](https://github.com/laulin/fluentbit-server-py), it allows to received event from Fluentbit agent using the forward protocol.
It support authentication using shared key and TLS. No tag parameter is available since it is provided by the agent.

Parameters :

* `host="localhost"` : Used to bind socket server
* `port=24224` : Port used to bind the server
* `tls_enable=False` : Used to enable TLS support
* `key_file=None` : if TLS enabled, path to the key file
* `crt_file=None` : if TLS enabled, path to the certificate file
* `shared_key=None` : defined a shared key between servers an nodes. If set, enable authentication
* `server_hostname=""` : define the hostname, useful for shared_key authentication

**Warning** : if you exposed the port to internet, use authentication and TLS. If you can, add firewall rule to decrease surface attack. BE CAREFUL !

Example:

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

### input_sqlite

This input use a SQLite database as input. It works with time serie : each table is base on time (ex : log_%Y%m%d) and a field is an 
unix timestamp (int or float). 

Parameters :

* `tag` : tag used for generated event
* `window` : time in second of processing window
* `time_key` : field use in database as timestamp
* `table_name_match` : Pattern (unix style) for find table (ex : log_*)
* `filename` : SQLite database path
* `fields` : dict of field name and sql type as value (ie TEXT, FLOAT, INTEGER, BLOB)
* `offset=0` : Time in second of working time offset. Can be useful to process data in an other time zone or remove old tables
* `remove=False` : If True, remove data once read
* `reload_position=False` : If True, reload data from the last known time (0 by default). Otherwise, start at current time.
* `db_path=None` : file path to store internal state. None means only RAM is used.

Example:

```yaml
- name : input_sqlite
  tag: "log"
  table_name_match : "log_*"
  filename : "/my/path/test.db"
  fields :
    timestamp : INTEGER
    line : TEXT
  time_key : timestamp
```

### input_rethinkdb

This input use a RethinkDB database as input. It works with time serie : each table is base on time (ex : log_%Y%m%d) and a field is an 
unix timestamp (int or float). 

Parameters :

* `tag` : tag used for generated event
* `window` : time in second of processing window
* `timestamp_index` : field use in database as timestamp
* `table_name_match` : Pattern (unix style) for find table (ex : log_*)
* `ip=localhost` : Rethinkdb instance IP
* `port=28015` : Rethinkdb instance port
* `database_name=test` : Rethinkdb database name
* `wait_connection=30` : Wait time for database warm up
* `offset=0` : Time in second of working time offset. Can be useful to process data in an other time zone or remove old tables
* `remove=False` : If True, remove data once read
* `reload_position=False` : If True, reload data from the last known time (0 by default). Otherwise, start at current time.
* `db_path=None` : file path to store internal state. None means only RAM is used.

Example:

```yaml
- name : input_rethinkdb
  tag: "log"
  table_name_match : "log_*"
  ip: foo.bar.com
  timestamp_index : timestamp
  window: 60
```

## Output

It exports events out of the pipeline. It can be file, database, etc.

### output_archive

It stores in buffer event and it writes buffer in file. 

Parameters :

* `match` : pattern to match tag
* `time_key` : used to extract time to interpolate path_template
* `path_template` : Template of the file path
* `buffer_size=1000` : Number of event stored before flush
* `timeout_flush=60` : Flush buffer after timeout, in second
* `db_path=None` : file path to store internal state. None means only RAM is used.

Example :

```yaml
- name : output_archive
  time_key : timestamp
  path_template : "/archives/{source}/log-%Y%m%d.json"
  match : mylog
```

Notes :

* if the example received the event contains record `{"timestamp":1607618046, "source":foo, "data":"test"}`, the path will be `/archives/foo/log-20201210.json`

### output_rethinkdb

Store events in [RethinkDB](https://rethinkdb.com/) as time serie.

Parameters

* `match` : pattern to match tag
* `time_key` : used to extract time to interpolate `table_template`
* `table_template` : Template of the table name
* `buffer_size=1000` : Number of event stored before flush
* `database="test"` : database name
* `ip="localhost"` : f set, change the database destination ip
* `port=None` : if set, change the database destination port
* `wait_connection=30` : used to wait the database warmup
* `timeout_flush=60` : Flush buffer after timeout, in second
* `db_path=None` : file path to store internal state. None means only RAM is used.

Example:

```yaml
- name : output_rethinkdb
  time_key : timestamp
  table_template : "log-%Y%m%d"
  database : test
  ip : rethink.com
  port : 28015
  match : my_log
```

### output_stdout

Display event in stdout.

Parameters

* `match` : pattern to match tag

Example:

```yaml
- name : output_stdout
  match : my_log
```

### output_sqlite

Store events in Sqlite database. Only defined fields are stored in event, others are dropped. If a field is missing, the document is dropped.

Parameters

* `match` : pattern to match tag
* `time_key` : field use for time serie.
* `table_template` : template string used to generate table names
* `fields` : dict of field name / Sqlite type. Sqlite types are REAL, TEXT, INTEGER or BLOB. 
* `filename` : Sqlite filename. Can be :memory: to save in RAM.
* `buffer_size=1000` : Number of event stored before flush
* `timeout_flush=60` : Flush buffer after timeout, in second
* `db_path=None` : file path to store internal state. None means only RAM is used.

Example:

```yaml
- name : output_sqlite
  match : my_log
  table_template: "log_%Y%m%d"
  fields:
    timestamp: INTEGER
    line: TEXT
  filename: "/tmp/test.db"
  db_path : "/tmp/test.pos.db"
```

## Parser

A parser take an event et parse one field with a specific format : `regex`, `json`, etc.

### parser_json

Read a field and add new fields to existing event.

Parameters :

* `match` : pattern to match tag
* `key` : Key to be parsed
* `mode="merge"` : A string that can be "merge", "tree" or "add"

Example of modes :

* `merge` :  {"key":"Z", "value":'{"aaa": "bb"}'} -> {"key":"Z", "aaa":"bb"}
* `add` :  {"key":"Z", "value":'{"aaa": "bb"}'} -> {"key":"Z", "value":'{"aaa": "bb"}', "aaa":"bb"}`
* `tree` :  {"key":"Z", "value":'{"aaa": "bb"}'} -> {"key":"Z", "value":{"aaa":"bb"}}

Example :

```yaml
- name : parser_json
  match : my_log
  key : json_log
  mode : add
```

### parser_regex

Read a field and add new fields to existing event.

Parameters :

* `match` : pattern to match tag
* `key` : Key to be parsed
* `regex` : define the behaviour. Use name group to create field
* `mode="merge"` : A string that can be "merge", "tree" or "add"

Example of modes :

* `merge` :  {"key":"Z", "value":'{"aaa": "bb"}'} -> {"key":"Z", "aaa":"bb"}`
* `add` :  {"key":"Z", "value":'{"aaa": "bb"}'} -> {"key":"Z", "value":'{"aaa": "bb"}', "aaa":"bb"}
* `tree` :  {"key":"Z", "value":'{"aaa": "bb"}'} -> {"key":"Z", "value":{"aaa":"bb"}}

Example :

```yaml
- name : parser_regex
  match : my_log
  key : line
  mode : merge
  regex : ".+?(?P<name>\\{.+\\})"
```
## Filter

Process event, may create or delete events.

## filter_change

This action will monitor a certain field and match if that field changes. The field must change with respect to the last event with the same query_key.

Parameters :

* `match` : pattern to match tag
* `tag` : tag used to generate new event on change
* `alert` : dict used to generate new event on change
* `compare_key` : key monitored to find change
* `query_key` : key used to group type of event
* `ignore_null=True` : ignore if compare_key is missing. If ignore_null if false, missing compare_key is a valid state
* `db_path=None` : file path to store internal state. None means only RAM is used.

Example :

```yaml
- name : filter_change
  match : my_log
  tag : my_alert
  alert : 
    title : The hostname change of status
    priority : 2
  compare_key : status
  query_key : hostname
```

if events are :

* `{"hostname":"foo.bar", "status":"on"}`
* `{"hostname":"foo.bar", "status":"off"}`

Then a new event will be created on second event

### filter_date

This action performs a time parsing and allows to change the time format. Under the hook, it use [Chronyk](https://github.com/KoffeinFlummi/Chronyk) library so feel free refere about time format.

Parameters :

* `match` : pattern to match tag
* `key` : define the key to be parsed
* `format=None` : define the output format of key's value. None means unix timestamps

Example :

```yaml
- name : filter_date
  match : date
```

Event likes `{"date":"Fri, 11 Dec 2020 08:30:13 +0000"}` become `{"date":1607675413}`

It takes a date and convert it to timestamp

### filter_remove_keys

This action remove one or more key in event.

Parameters :

* `match` : pattern to match tag
* `keys` : on string or a list of string to describe keys to be removed.

Example :

```yaml
- name : filter_remove_keys
  match : date
  keys : 
    - A
    - B
```

Event likes `{"A":1, "B":2, "C":3}` become `{"C":3}`

### filter_retag

This action change the event's tag with a value in event or with a constant value.

Parameters :

* `match` : pattern to match tag
* `value` : New tag if key doesn't exist or if key=None
* `key=None`: event value used to retag event. Use value parameter if missing

Example :

```yaml
- name : filter_retag
  match : my_log
  value : generic_log
  key : source
```

If event looks like `{"source":"auth", "data":"xxx"}`, the new tag will be "auth".
If event looks like `{"data":"xxx"}`, the new tag will be "generic_log".

### filter_frequency

This action matches when there are at least a certain number of events in a given time frame. This may be counted on a per-query_key basis.

Parameters :

* `match` : pattern to match tag
* `tag` : tag used to generate new event on change
* `alert` : dict used to generate new event on change
* `num_events` : match if number of event during the time frame if higher or equal to this value
* `timeframe` : duration of the time windows in seconds
* `query_key=None` : key used to group type of event
* `db_path=None` : file path to store internal state. None means only RAM is used.

Example :

```yaml
- name : filter_frequency
  match : my_log
  tag : my_alert
  alert : 
    title : The hostname change of status too often
    priority : 1
  query_key : hostname
  num_events : 10
  timeframe : 60
```

### filter_spike

This action matches when the volume of events during a given time period is spike_height times larger or smaller than during the previous time period. 
It uses two sliding windows to compare the current and reference frequency of events. We will call this two windows “reference” and “current”. A query
key and a field value can be defined. 

Parameters :

* `match` : pattern to match tag
* `tag` : tag used to generate new event on change
* `alert` : dict used to generate new event on change
* `spike_height` : define the factor between current and reference that create an event
* `spike_type` : define the spike direction : up, down or both
* `timeframe` : duration of the time windows in seconds
* `query_key=None` : key used to group type of event
* `field_value=None` : When set, uses the value of the field in the document and not the number of matching documents. This is useful to monitor for example a temperature sensor and raise an alarm if the temperature grows too fast. Note that the means of the field on the reference and current windows are used to determine if the spike_height value is reached
* `db_path=None` : file path to store internal state. None means only RAM is used.
* `threshold_ref=10` : minimum number of event in the reference frame to be evaluated
* `threshold_cur=10` : minimum number of event in the current frame to be evaluated

Example :

```yaml
- name : filter_spike
  match : my_log
  tag : temperature_alert
  alert : 
    title : The temperature rise to quickly
    priority : 1
  spike_height : 2
  spike_type : up
  field_value : temperature
  timeframe : 60
```

### filter_flatline

This action matches when the total number of events is under a given threshold for a time period.

Parameters :

* `match` : pattern to match tag
* `tag` : tag used to generate new event on change
* `alert` : dict used to generate new event on change
* `threshold` : minimum number of event in the frame (other wise, rise an alert)
* `timeframe` : duration of the time windows in seconds
* `query_key=None` : key used to group type of event
* `forget_keys=True` : set to false to keep tracking existing query key (emit alert for ever if no event come back).
* `db_path=None` : file path to store internal state. None means only RAM is used.


Example :

```yaml
- name : filter_flaline
  match : my_log
  tag : heartbeat_down
  alert : 
    title : No more heartbeat !
    priority : 3
  threshold : 1
  field_value : source
  timeframe : 60
```

# icons

Thanks to flaticon.com !

<div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>