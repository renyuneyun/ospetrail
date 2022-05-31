# Operating System & Package Error Trail (ospetrail)

Operating System & Package Error Trail (ospetrail) intends to supports Linux users to deal with OS errors easier.

It compares the error with regards to the package versions and environment. Therefore, the user can more easily pin down the cause of the error, and act accordingly (e.g. downgrade or upgrade packages to appropriate versions).

## Motivation

I use archlinux as my main OS/distro, on a raletively new laptop. There were/are various issues/bugs on it, an I had to manually try to figure out the cause of the errors and avoid or resolve them. They are often due to package versions (updates) and/or combination of software versions.

This situation is more several when I initially received the machine, which was the first batch of Lenovo Yoga 14s 2021, which in turn was one of the early laptops with 11 gen Intel Core CPUs. The problems have significantly reduced with time going on, but still happens occasionally – in particular, the video driver and/or the graphical environment.

I'm tired of and no longer have enough time to deal with such situations, and try different combinations. In particular, after having set up snapper, I have a better choice to just revert to a specific version to temporarily avoid issues. Still, I can't avoid it all the time, because an earlier version could be problematic (maybe in a different way) as well.

I had a script to record the errors and package (and kernel) versions for me to use, but the recording is largely unstructured. The basic goal of ospetrail is to replace that script, and hopefully can support comparing as well.

## Current situation

This software is in early stage, and is currently built for my necessity. It only supports archlinux at the moment.

Currently, ospetrail records operating system (kernel) version and package versions, and allows the user to add custom comments.
It can also list existing records.

Data are stored to `~/logs/ospetrail/`, as a [Turtle](https://www.w3.org/TR/turtle/) file (`db.ttl`). (Yet the ontology is not defined.)

### How to use

It uses poetry to manage dependencies. Run `poetry install` to set up the eivironment.

Run the following command to get help:

```
poetry run ospetrail/__main__.py --help
```

### Potential TODOs

- [ ] Correctly package it
- [ ] Compare records and check the problematic version(s)
- [ ] Update or append to existing records
- [ ] Provide an OWL ontology
    - [ ] Easier maintainance through Owlready2 (?)
- [ ] Provide a standard vocabulary of errors
- [ ] Provide ways to customize the vocabulary
- [ ] Retrospectively add records
- [ ] Run as daemon and monitor behaviours (e.g. systemd journals) to automatically add records

## License

Copyright 2022 Rui Zhao (renyuneyun)

This software is licensed under Apache License, Version 2.0. See the [LICENSE](LICENSE) file or     http://www.apache.org/licenses/LICENSE-2.0 for more details.