# Django Template

This is a Django project template with microservices architecture. 
It is designed to be used in a Docker Swarm.

## Development Setup

## Production Setup

## Architecture

For using celery uncomment related requirements, and in core/celery.py and core/__init__.py uncomment the code

For postgis uncomment-related requirements and uncomment code related to glob in core/settings.py. Also add "gdal" to line 22 in the Dockerfile

### Testing

The project comes with VCR and Django Test Framework setup.

Write your tests in the `<your_app>/tests` directory. 

#### Sample Test

```python
import vcr
import requests
import json
from django.test import SimpleTestCase

my_vcr = vcr.VCR(
    cassette_library_dir="cassettes/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
    record_mode="once",
    filter_headers=["authorization"],
)

class SearchViewTests(SimpleTestCase):

    @my_vcr.use_cassette()
    def test_search_view_post(self):
        url = "http://localhost:8000/api/search/"

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": "test"}),
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        # Adjust the following assertions based on your actual response
        self.assertIn("search_id", response_data)
        self.assertIsInstance(response_data["search_id"], str)
```
