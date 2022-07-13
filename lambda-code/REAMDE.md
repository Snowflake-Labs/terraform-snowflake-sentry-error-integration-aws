# Lambda Proxy

## Testing

```bash
# Navigate to the lambda-code
cd /path/to/lambda-code/

# Activate the venv
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements-dev.txt

# Run the test
python -m pytest test.py
```
