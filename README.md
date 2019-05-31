# mface

Utils for Microsft Face API

## Build

### 1. Edit api_config.json

- `"subscription_key"`: `YOUR_KEY`
- `"face_api_url"`: `ENDPOINT_URL`

### 2. Build container

```sh
docker build -t mface .
```

## Usage

```sh
docker run -i -v /path/to/images_dir:/images:ro -v /path/to/result.json:/code/mface_result mface
```

then, result json written in /path/to/result.json
