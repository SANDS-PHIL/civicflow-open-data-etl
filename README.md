# CivicFlow Open Data ETL Skeleton

A proof-of-concept Extract, Transform, Load (ETL) pipeline designed to help local governments streamline public data workflows. This skeleton is intended for **public data only** and must not be used with internal, secure, or sensitive APIs without proper authorization and security review.

## Purpose

This project provides a reusable skeleton for building ETL pipelines that:
- Extract data from public REST APIs
- Transform and validate the data using Pydantic models
- Load the cleaned data into CSV or Parquet files for downstream analysis

It is designed to be easily adapted for various public datasets (e.g., building consents, resource consents, planning applications) by modifying the Pydantic models and mapping the API response.

## Disclaimer

⚠️ **IMPORTANT**: This is a proof-of-concept for **public data only**. 
- Do NOT use this pipeline with internal, confidential, or secure government systems without explicit authorization.
- Always ensure you have the right to access and redistribute any data you process.
- This code does not include authentication, encryption, or other security measures required for sensitive data.
- Users are responsible for complying with all relevant data protection laws and regulations (e.g., Privacy Act 2020 in New Zealand).

## Technical Stack

- Python 3.10+
- [requests](https://pypi.org/project/requests/) for HTTP calls
- [pandas](https://pypi.org/project/pandas/) for data manipulation
- [pydantic](https://pypi.org/project/pydantic/) (v2) for data validation
- [python-dotenv](https://pypi.org/project/python-dotenv/) for environment variable management
- Standard [logging](https://docs.python.org/3/library/logging.html) for structured logs

## Project Structure

```
.
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── main.py               # ETL pipeline orchestrator
└── src
    ├── __init__.py       # Package initializer
    ├── models.py         # Pydantic models for data validation
    ├── extract.py        # Data extraction logic
    ├── transform.py      # Data transformation and validation
    └── load.py           # Data loading (CSV/Parquet)
```

## Installation

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   # Edit .env to set API_URL (and optionally OUTPUT_FORMAT, OUTPUT_PATH)
   ```

## Usage

Run the ETL pipeline:
```bash
python main.py
```

The pipeline will:
1. Extract data from the API endpoint specified in `API_URL` (defaults to a public placeholder API)
2. Transform and validate the data using the Pydantic model in `src/models.py`
3. Load the cleaned data to a file specified by `OUTPUT_PATH` (defaults to `output/data.csv`)

### Configuration

All configuration is done via environment variables (set in `.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `API_URL` | The public API endpoint to fetch data from | `https://jsonplaceholder.typicode.com/posts` |
| `API_KEY` | API key if required (not used in the mock) | (empty) |
| `OUTPUT_FORMAT` | Output file format: `csv` or `parquet` | `csv` |
| `OUTPUT_PATH` | Full path to the output file | `output/data.csv` (or `output/data.parquet` if format is parquet) |

## Development

### Adding a New Dataset

1. Update the Pydantic model in `src/models.py` to match the target dataset's schema.
2. Modify the mapping logic in `src/transform.py` to map API response fields to the model fields.
3. Adjust any data cleaning or validation rules as needed.
4. Update the `.env.example` with the new API endpoint (if different).

### Running Tests

Currently, there are no unit tests. To test locally:
1. Ensure you have a public API endpoint that returns JSON data.
2. Set `API_URL` in your `.env` to that endpoint.
3. Run `python main.py` and check the output directory for the resulting file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (if included).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue in the repository.