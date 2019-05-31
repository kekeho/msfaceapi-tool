# mface

Utils for Microsft Face API


## Build

```sh
docker build -t mface .
```

### Usage

```sh
docker run -i -v /path/to/images_dir:/images:ro -v /path/to/result.json:/code/mface_result mface
```

then, result json written in /path/to/result.json
