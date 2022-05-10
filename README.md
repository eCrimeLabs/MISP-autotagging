# MISP autotagging
When working with MISP we have experienced that in some situations you need to put one or more local tags on events from various organizations typically based on that you trust data created by this and want to add additional automatization based on events from the source.

So we are please to announce a small tool that might assist organizations using  MISP to make the feature of automatically adding local tagging to events from specific organizations UUID’s.

The tools has the features of either adding or removing a set of predefined

## Configuration
rename the "config.py.template" to "config.py" and add in you MISP data and the organzation UUID and tags to work with, as the tool supports multiple tags you should be able to add as many as needed.

```
misp_url='https://<MISP-URL>'
misp_key='<MISP API KEY>'
misp_verifycert=True

dict_orgtags = {
    '00000000-0000-0000-0000-000000000000': ['ecrimelabs:tag=1', 'ecrimelabs:tag=2'],
    '11111111-1111-1111-1111-111111111111': ['ecrimelabs:tag=3']
}
```

## Running the tool:

```
# venv/bin/python3 misp-autotagging.py -h
eCrimeLabs MISP autotagging tool
usage: misp-autotagging.py [-h] [-a] [-r] [-d DAYS]

optional arguments:
  -h, --help            show this help message and exit
  -a, --add             Add local tags to Event(s)
  -r, --remove          Remove local tags to Event(s)
  -d DAYS, --days DAYS  Number of days to look back for events (Default: 2)
```

The below adds as example the tags to organizations for events created within the last 20 days
```
# venv/bin/python3 misp-autotagging.py -a -d 20
eCrimeLabs MISP autotagging tool
 + Remove local tags to Event(s)
   - 2022-05-10 16:00:51 UTC - Successfully added local tag: ecrimelabs:custom-tag=1 to Event UUID: c303c3c9-8623-45cd-9173-c61de12635b0
   - 2022-05-10 16:00:51 UTC - Successfully added local tag: ecrimelabs:custom-tag=2 to Event UUID: c303c3c9-8623-45cd-9173-c61de12635b0
```
