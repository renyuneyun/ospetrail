# Operating System & Package Error Trail (ospetrail)
- - - - - -

Operating System & Package Error Trail (ospetrail) intends to supports Linux users to deal with OS errors easier.

It compares the error with regards to the package versions and environment. Therefore, the user can more easily pin down the cause of the error, and act accordingly (e.g. downgrade or upgrade packages to an appropriate version).


## Current situation

This software is in early stage, and is currently built for my necessity. It only supports archlinux at the moment.

Currently, ospetrail records operating system (kernel) version and package versions, and allows the user to add custom comments.
It can also list existing records.

Data are stored to `~/logs/ospetrail/`, as a [Turtle](https://www.w3.org/TR/turtle/) file (`db.ttl`).

### How to use

It uses poetry to manage dependencies. Run `poetry install` to set up the eivironment.

Run the following command to get help:

```
poetry run ospetrail/__main__.py --help
```

### Potential TODOs

[ ] Correctly package it
[ ] Compare records and check the problematic version(s)
[ ] Update or append to existing records
[ ] Provide an OWL ontology
    [ ] Easier maintainance through Owlready2 (?)
[ ] Provide a standard vocabulary of errors
[ ] Provide ways to customize the vocabulary
[ ] Retrospectively add records
[ ] Run as daemon and monitor behaviours (e.g. systemd journals) to automatically add records

## License

Copyright 2022 Rui Zhao (renyuneyun)

This software is licensed under Apache License, Version 2.0. See [LICENSE] file or     http://www.apache.org/licenses/LICENSE-2.0 for more details.