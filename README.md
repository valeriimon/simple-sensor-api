# Simple Sensor API written in Fast API

## Run project via docker

```bash
docker-compose up
```


## Run project locally

Generate and activate venv

```bash
python3 -m venv .venv
source .venv/bin/activate -- Linux
```

Install packages

```bash
pip install -r requirements.txt
```

Run project

```bash
uvicorn main:app --reload
```

## License

[MIT](https://choosealicense.com/licenses/mit/)